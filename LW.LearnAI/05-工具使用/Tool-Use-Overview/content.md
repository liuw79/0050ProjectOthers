# Tool Use with Claude | Claude 工具使用

> Source: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview

---

Claude is capable of interacting with tools and functions, allowing you to extend Claude's capabilities to perform a wider variety of tasks.

**Claude 能够与工具和函数交互，让你能够扩展 Claude 的能力以执行更多种类的任务。**

---

## How Tool Use Works | 工具使用如何工作

Claude supports two types of tools:

**Claude 支持两种类型的工具：**

### 1. Client Tools | 1. 客户端工具

Tools that execute on your systems:
- User-defined custom tools that you create and implement
- Anthropic-defined tools like computer use and text editor

**在你的系统上执行的工具：**
- 用户定义的自定义工具（你创建和实现）
- Anthropic 定义的工具，如电脑使用和文本编辑器

### 2. Server Tools | 2. 服务器端工具

Tools that execute on Anthropic's servers:
- Web search and web fetch tools
- Must be specified in the API request but don't require implementation

**在 Anthropic 服务器上执行的工具：**
- 网络搜索和网络获取工具
- 必须在 API 请求中指定，但不需要实现

---

## Client Tool Workflow | 客户端工具工作流程

```
1. Provide Claude with tools and a user prompt
   ↓
2. Claude decides to use a tool
   ↓
3. Execute the tool and return results
   ↓
4. Claude uses tool result to formulate a response
```

```
1. 向 Claude 提供工具和用户提示
   ↓
2. Claude 决定使用工具
   ↓
3. 执行工具并返回结果
   ↓
4. Claude 使用工具结果形成响应
```

---

## Basic Example | 基本示例

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }],
    messages=[{
        "role": "user",
        "content": "What is the weather like in San Francisco?"
    }]
)
```

### Response | 响应

```json
{
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "text",
      "text": "I'll check the current weather in San Francisco for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ]
}
```

---

## Return Tool Results | 返回工具结果

```python
response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    tools=[...],
    messages=[
        {"role": "user", "content": "What is the weather like in San Francisco?"},
        {"role": "assistant", "content": [...]},  # Previous response with tool_use
        {
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
                "content": "15 degrees"
            }]
        }
    ]
)
```

---

## Tool Types | 工具类型

### Single Tool | 单一工具

Basic tool invocation with one function.

**使用一个函数的基本工具调用。**

### Parallel Tool Use | 并行工具使用

Claude can call multiple tools in a single response.

**Claude 可以在单个响应中调用多个工具。**

```json
{
  "content": [
    {"type": "tool_use", "name": "get_weather", "input": {"location": "NYC"}},
    {"type": "tool_use", "name": "get_time", "input": {"timezone": "America/New_York"}}
  ]
}
```

**Important**: Return all tool results in a single user message.

**重要**：在单个用户消息中返回所有工具结果。

### Sequential Tools | 顺序工具

Some tasks require calling tools in sequence, using output of one as input to another.

**某些任务需要按顺序调用工具，将一个工具的输出作为另一个工具的输入。**

---

## Chain of Thought Tool Use | 链式思考工具使用

By default, Claude Opus is prompted to think before making tool calls. For Sonnet/Haiku:

**默认情况下，Claude Opus 会在进行工具调用之前进行思考。对于 Sonnet/Haiku：**

```
Answer the user's request using relevant tools (if they are available).
Before calling a tool, do some analysis. First, think about which tool is relevant.
Second, go through each required parameter and determine if the user has provided enough information.
If all required parameters are present, proceed with the tool call.
BUT, if one value is missing, ask the user to provide it instead of invoking the function.
```

```
使用相关工具回答用户的请求（如果可用）。
在调用工具之前，做一些分析。首先，思考哪个工具是相关的。
其次，检查每个必需参数，确定用户是否提供了足够的信息。
如果所有必需参数都存在，继续工具调用。
但是，如果缺少某个值，请用户提供它，而不是调用函数。
```

---

## JSON Mode | JSON 模式

Use tools to get JSON output even without intending to run it:

**使用工具获取 JSON 输出，即使不打算运行它：**

```python
tools=[{
    "name": "record_summary",
    "description": "Record summary of an image using well-structured JSON.",
    "input_schema": {
        "type": "object",
        "properties": {
            "key_colors": {...},
            "description": {...}
        }
    }
}],
tool_choice={"type": "tool", "name": "record_summary"}
```

---

## Pricing | 定价

Tool use is priced based on:
1. Total input tokens (including tools parameter)
2. Output tokens generated
3. Server-side tool usage (e.g., web search charges)

**工具使用的定价基于：**
1. 总输入 tokens（包括 tools 参数）
2. 生成的输出 tokens
3. 服务器端工具使用（如网络搜索收费）

### Token Overhead | Token 开销

| Model | Tool Choice | System Prompt Tokens |
|-------|-------------|---------------------|
| Claude Opus 4.1 | `auto`, `none` | 346 |
| Claude Opus 4.1 | `any`, `tool` | 313 |
| Claude Sonnet 3.7 | `auto`, `none` | 346 |
| Claude Sonnet 3.7 | `any`, `tool` | 313 |
| Claude Haiku 3.5 | `auto`, `none` | 264 |
| Claude Haiku 3.5 | `any`, `tool` | 340 |

| 模型 | 工具选择 | 系统提示 Tokens |
|------|----------|-----------------|
| Claude Opus 4.1 | `auto`, `none` | 346 |
| Claude Opus 4.1 | `any`, `tool` | 313 |
| Claude Sonnet 3.7 | `auto`, `none` | 346 |
| Claude Sonnet 3.7 | `any`, `tool` | 313 |
| Claude Haiku 3.5 | `auto`, `none` | 264 |
| Claude Haiku 3.5 | `any`, `tool` | 340 |

---

## Related Resources | 相关资源

- [How to Implement Tool Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
- [Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use)
- [Web Search Tool](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool)
