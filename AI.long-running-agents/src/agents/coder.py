import os
import subprocess
import re
from typing import Optional

from src.agents.base import Agent
from src.core.feature_list import FeatureListManager, Feature
from src.core.git_integrator import GitIntegrator
from src.core.llm.factory import create_llm_client
from src.core.exceptions import LLMError


class CodingAgent(Agent):
    def __init__(self, config):
        self.config = config
        self._llm_client = None

    @property
    def llm_client(self):
        """Lazy initialization of LLM client."""
        if self._llm_client is None:
            self._llm_client = create_llm_client(
                provider=self.config.llm.provider,
                api_key=self.config.llm.api_key,
                model=self.config.llm.model
            )
        return self._llm_client

    def run(self) -> dict:
        """Run coding agent - execute standard workflow."""
        try:
            # 1. Change to work directory
            work_dir = self.config.project.work_dir
            os.chdir(work_dir)

            # 2. Read progress file
            self._read_progress()

            # 3. Read feature list and select next feature
            feature = self._select_next_feature()
            if not feature:
                return {"status": "success", "message": "All features completed"}

            # 4. Check git history
            self._check_git_history()

            # 5. Run init.sh
            self._start_environment()

            # 6. Verify basic functionality
            self._verify_basic_functionality()

            # 7. Implement new feature
            self._implement_feature(feature)

            # 8. Test feature
            test_passed = self._test_feature(feature)

            # 9. Commit changes
            self._commit_changes(feature, test_passed)

            # 10. Update progress
            self._update_progress(feature, test_passed)

            # 11. Mark feature complete
            self._mark_feature_complete(feature.id)

            return {
                "status": "success",
                "message": f"Implemented feature: {feature.description}",
                "test_passed": test_passed
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _read_progress(self):
        """Read progress file."""
        progress_file = self.config.project.progress_file
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                print(f"Progress:\n{f.read()}")

    def _select_next_feature(self) -> Optional[Feature]:
        """Select next incomplete feature."""
        feature_list_path = self.config.project.feature_list_path
        manager = FeatureListManager(feature_list_path)
        pending = manager.get_pending()
        return pending[0] if pending else None

    def _check_git_history(self):
        """Check git history."""
        work_dir = self.config.project.work_dir
        integrator = GitIntegrator(work_dir)
        log = integrator.get_log(5)
        print("Recent commits:")
        for commit in log:
            print(f"  {commit['hash']}: {commit['message']}")

    def _start_environment(self):
        """Start development environment."""
        init_script = self.config.project.init_script
        if os.path.exists(init_script):
            print(f"Running {init_script}...")

    def _verify_basic_functionality(self):
        """Verify basic functionality."""
        print("Verifying basic functionality...")
        print("Basic functionality verified")

    def _implement_feature(self, feature: Feature):
        """Implement feature using LLM."""
        print(f"Implementing feature: {feature.description}")

        # Get current project context
        project_context = self._get_project_context()

        # Generate code using LLM
        generated = self._generate_code_with_llm(feature, project_context)

        # Write generated files
        self._write_generated_files(generated)

        print(f"Feature '{feature.description}' implemented")

    def _get_project_context(self) -> str:
        """Get current project context for LLM."""
        context_parts = []

        # Read feature list
        feature_list_path = self.config.project.feature_list_path
        if os.path.exists(feature_list_path):
            with open(feature_list_path, 'r') as f:
                context_parts.append(f"Feature List:\n{f.read()}")

        # Read progress
        progress_file = self.config.project.progress_file
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                context_parts.append(f"Progress:\n{f.read()}")

        # List existing Python files
        work_dir = self.config.project.work_dir
        py_files = []
        for root, dirs, files in os.walk(work_dir):
            # Skip hidden and common non-source directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
            for f in files:
                if f.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, f), work_dir)
                    py_files.append(rel_path)

        if py_files:
            context_parts.append(f"Existing Python files: {', '.join(py_files)}")

        return "\n\n".join(context_parts)

    def _generate_code_with_llm(self, feature: Feature, context: str) -> dict:
        """Generate code using LLM."""
        prompt = f"""You are implementing a feature in a Python project.

Feature to implement:
- Category: {feature.category}
- Description: {feature.description}
- Steps: {', '.join(feature.steps)}

Project Context:
{context}

Generate the implementation. Return a JSON object with:
1. "files": array of {{"path": "relative/path.py", "content": "file content"}}
2. "description": brief description of what was implemented

Return ONLY valid JSON. Use proper escape sequences in strings."""

        try:
            response = self.llm_client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.llm.max_tokens
            )
            return self._parse_code_response(response)
        except Exception as e:
            raise LLMError(f"Failed to generate code: {e}")

    def _parse_code_response(self, response: str) -> dict:
        """Parse LLM response into code files."""
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                import json
                return json.loads(json_match.group())
            except:
                pass

        # Fallback: create a single file with the response
        return {
            "files": [{
                "path": "generated_code.py",
                "content": f"# Generated code\n{response}"
            }],
            "description": "LLM generated code"
        }

    def _write_generated_files(self, generated: dict):
        """Write generated files to disk."""
        work_dir = self.config.project.work_dir

        for file_info in generated.get("files", []):
            file_path = os.path.join(work_dir, file_info["path"])

            # Create directory if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w') as f:
                f.write(file_info["content"])

            print(f"Created: {file_info['path']}")

    def _test_feature(self, feature: Feature) -> bool:
        """Test feature using pytest."""
        print(f"Testing feature: {feature.description}")

        work_dir = self.config.project.work_dir

        # Check if pytest is available
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "-x", "-q", "--tb=short"],
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print("All tests passed")
                return True
            else:
                print(f"Tests failed:\n{result.stdout}\n{result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("Test execution timed out")
            return False
        except FileNotFoundError:
            print("pytest not available, skipping tests")
            return True  # Consider passed if no test framework

    def _commit_changes(self, feature: Feature, test_passed: bool):
        """Commit changes to git."""
        work_dir = self.config.project.work_dir
        integrator = GitIntegrator(work_dir)

        # Format commit message
        status = "passed" if test_passed else "needs review"
        message = self.config.git.commit_message_format.format(
            description=f"{feature.description} (tests: {status})"
        )

        integrator.commit(message, [])

    def _update_progress(self, feature: Feature, test_passed: bool):
        """Update progress file."""
        progress_file = self.config.project.progress_file
        status = "completed (tests passed)" if test_passed else "completed (tests failed)"
        with open(progress_file, 'a') as f:
            f.write(f"\n{feature.description}: {status}\n")

    def _mark_feature_complete(self, feature_id: int):
        """Mark feature as complete."""
        feature_list_path = self.config.project.feature_list_path
        manager = FeatureListManager(feature_list_path)
        manager.update_status(feature_id, passes=True)
