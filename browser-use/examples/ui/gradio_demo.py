import asyncio
import os
from dataclasses import dataclass
from typing import List, Optional

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
# Import DeepSeek model - Using the correct case
# from langchain_deepseek import DeepSeek # Previous attempt
# from langchain_community.chat_models.deepseek import ChatDeepseek # Previous attempt
from langchain_deepseek import ChatDeepSeek # Correct import with correct case
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Local module imports
from browser_use import Agent

load_dotenv()

# --- Debugging --- 
# print(f"DEEPSEEK_API_KEY from environment: {os.environ.get('DEEPSEEK_API_KEY')}") # Old debug print
loaded_key = os.environ.get('DEEPSEEK_API_KEY')
print(f"DEEPSEEK_API_KEY from environment: '{loaded_key}' (Type: {type(loaded_key)})')") # New debug print with quotes and type
# --- End Debugging ---

@dataclass
class ActionResult:
	is_done: bool
	extracted_content: Optional[str]
	error: Optional[str]
	include_in_memory: bool


@dataclass
class AgentHistoryList:
	all_results: List[ActionResult]
	all_model_outputs: List[dict]


def parse_agent_history(history_str: str) -> None:
	console = Console()

	# Split the content into sections based on ActionResult entries
	sections = history_str.split('ActionResult(')

	for i, section in enumerate(sections[1:], 1):  # Skip first empty section
		# Extract relevant information
		content = ''
		if 'extracted_content=' in section:
			content = section.split('extracted_content=')[1].split(',')[0].strip("'")

		if content:
			header = Text(f'Step {i}', style='bold blue')
			panel = Panel(content, title=header, border_style='blue')
			console.print(panel)
			console.print()


async def run_browser_task(
	task: str,
	# Parameter for DeepSeek API Key (from UI)
	api_key_ui: str, # DEEPSEEK_API_KEY
	model: str = 'deepseek-chat', # Changed default model to a Deepseek model
	headless: bool = True,
) -> str:
	# Prioritize getting API key from environment variable (.env file)
	api_key = os.environ.get('DEEPSEEK_API_KEY')

	# If not found in environment, use the key provided in the UI
	if not api_key or not api_key.strip():
		api_key = api_key_ui

	# Check if we have a key from either source
	if not api_key or not api_key.strip():
		return 'Please provide DeepSeek API Key either in the UI or in the .env file (DEEPSEEK_API_KEY)'

	# Set the environment variable (might be redundant if already set, but ensures consistency)
	os.environ['DEEPSEEK_API_KEY'] = api_key

	try:
		agent = Agent(
			task=task,
			# Use ChatDeepSeek class with correct case
			llm=ChatDeepSeek(model=model),
		)
		result = await agent.run()
		# Parse the result to return only the final extracted content
		if result and hasattr(result, 'all_results') and result.all_results:
			final_result = result.all_results[-1]
			if final_result.is_done and final_result.error is None and final_result.extracted_content:
				return final_result.extracted_content
			elif final_result.error:
				return f"Agent finished with error: {final_result.error}"
			else:
				# If done but no content or error, return a generic message or raw result
				return "Agent finished, but no specific content extracted or error reported."
		else:
			# If result format is unexpected, return raw result string
			return str(result)
	except Exception as e:
		# Consider more specific error handling for DeepSeek if needed
		return f'Error during agent execution: {str(e)}'


def create_ui():
	# State to store the current running task
	current_task = gr.State(None) 

	with gr.Blocks(title='Browser Use GUI') as interface:
		gr.Markdown('# Browser Use Task Automation')

		with gr.Row():
			with gr.Column():
				# Updated input for DeepSeek API Key
				api_key_ds = gr.Textbox(label='DeepSeek API Key', placeholder='Enter your DeepSeek API Key...', type='password')
				task = gr.Textbox(
					label='Task Description',
					placeholder='E.g., Find flights from New York to London for next week',
					lines=3,
				)
				# Updated model choices for DeepSeek
				model = gr.Dropdown(choices=['deepseek-chat', 'deepseek-coder'], label='Model', value='deepseek-chat')
				headless = gr.Checkbox(label='Run Headless', value=True)
				# Add Stop button alongside Run button
				with gr.Row():
					submit_btn = gr.Button('Run Task')
					# Initial state: Stop button disabled
					stop_btn = gr.Button('Stop Task', interactive=False) 

			with gr.Column():
				output = gr.Textbox(label='Output', lines=10, interactive=False)

		# Define function for the Stop button
		async def stop_task_action(task_handle):
			print("[DEBUG] stop_task_action called.") # Debug print
			output_msg = "No active task to stop."
			should_cancel = False
			if task_handle and not task_handle.done():
				print(f"[DEBUG] Attempting to cancel task: {task_handle}") # Debug print
				try:
					task_handle.cancel()
					print("[DEBUG] task_handle.cancel() called.") # Debug print
					# Give cancellation a moment to propagate
					await asyncio.sleep(0.1)
					print("[DEBUG] asyncio.sleep(0.1) finished.") # Debug print 
					output_msg = "Stop request sent. Task may take time to fully cancel."
					should_cancel = True
				except Exception as e:
					# Print the full exception to the terminal for debugging
					print(f"[ERROR] Exception during task cancellation: {e!r}") # Debug print with repr
					import traceback
					traceback.print_exc() # Print full traceback to terminal
					output_msg = f"Error trying to cancel task: {e}"
			else:
				print("[DEBUG] No exception caught during cancellation attempt.") # Debug print
			
			# Reset state and button interactivity
			print(f"[DEBUG] Returning UI updates. Output message: {output_msg}") # Debug print
			return {
				current_task: None, # Clear the stored task
				output: gr.update(value=output_msg),
				submit_btn: gr.update(interactive=True), # Re-enable Run
				stop_btn: gr.update(interactive=False)  # Disable Stop
			}

		# Wrap the original async function for running and cancellation handling
		async def run_task_wrapper(task_desc, ds_key_ui, model_name, run_headless):
			# Disable Run, Enable Stop
			yield {
				submit_btn: gr.update(interactive=False), 
				stop_btn: gr.update(interactive=True),
				output: gr.update(value="Task starting...") # Initial message
			}
			
			task_future = None
			result = "Task did not complete." # Default result
			try:
				# Create the task
				task_future = asyncio.create_task(
					run_browser_task(task_desc, ds_key_ui, model_name, run_headless)
				)
				# Store the task handle in the state
				yield {current_task: task_future} 

				# Await the task completion
				result = await task_future

			except asyncio.CancelledError:
				result = "Task cancelled by user."
			except Exception as e:
				result = f"Error during task execution: {str(e)}"
			finally:
				# Task finished (completed, cancelled, or failed)
				# Re-enable Run, Disable Stop, update output
				yield {
					current_task: None, # Clear task handle from state
					output: gr.update(value=result),
					submit_btn: gr.update(interactive=True), 
					stop_btn: gr.update(interactive=False)
				}

		# Link Run button click to the wrapper function
		submit_btn.click(
			fn=run_task_wrapper,
			# Inputs now include task state
			inputs=[task, api_key_ds, model, headless], 
			# Outputs update state and UI elements
			outputs=[output, submit_btn, stop_btn, current_task] 
		)

		# Link Stop button click to its action
		stop_btn.click(
			fn=stop_task_action,
			# Input is the current task handle from state
			inputs=[current_task], 
			# Outputs update state and UI elements
			outputs=[output, submit_btn, stop_btn, current_task] 
		)

	return interface


if __name__ == '__main__':
	demo = create_ui()
	demo.launch()
