# Building with Extended Thinking | 使用扩展思考构建

> Source: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking

---

Extended thinking gives Claude enhanced reasoning capabilities for complex tasks, while providing varying levels of transparency into its step-by-step thought process before it delivers its final answer.

**扩展思考为 Claude 提供了增强的推理能力来处理复杂任务，同时在其给出最终答案之前提供不同程度的逐步思考过程透明度。**

---

## Supported Models | 支持的模型

Extended thinking is supported in the following models:

**以下模型支持扩展思考：**

- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Sonnet 3.7 (`claude-3-7-sonnet-20250219`)

---

## How Extended Thinking Works | 扩展思考如何工作

When extended thinking is turned on, Claude creates `thinking` content blocks where it outputs its internal reasoning. Claude incorporates insights from this reasoning before crafting a final response.

**当扩展思考开启时，Claude 会创建 `thinking` 内容块来输出其内部推理。Claude 在制定最终响应之前会整合这些推理的见解。**

The API response will include `thinking` content blocks, followed by `text` content blocks.

**API 响应将包含 `thinking` 内容块，后面跟着 `text` 内容块。**

### How to Use Extended Thinking | 如何使用扩展思考

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[
        {"role": "user", "content": "Solve this complex problem..."}
    ]
)
```

### Key Parameters | 关键参数

| Parameter | Description |
|-----------|-------------|
| `type` | Set to `"enabled"` to turn on extended thinking |
| `budget_tokens` | Maximum tokens for internal reasoning (must be less than max_tokens) |

| 参数 | 描述 |
|------|------|
| `type` | 设置为 `"enabled"` 以开启扩展思考 |
| `budget_tokens` | 内部推理的最大 token 数（必须小于 max_tokens） |

### Budget Guidelines | 预算指南

- **Minimum budget**: 1,024 tokens
- **最小预算**：1,024 tokens

- **Starting point**: Begin at minimum and increase incrementally
- **起始点**：从最小开始，逐步增加

- **Complex tasks**: Start with larger budgets (16k+ tokens)
- **复杂任务**：使用更大的预算（16k+ tokens）

- **Large budgets (>32k)**: Use batch processing to avoid timeout issues
- **大预算（>32k）**：使用批处理以避免超时问题

---

## Summarized Thinking (Claude 4 Models) | 摘要思考（Claude 4 模型）

With extended thinking enabled, the Messages API for Claude 4 models returns a **summary** of Claude's full thinking process.

**启用扩展思考后，Claude 4 模型的 Messages API 会返回 Claude 完整思考过程的**摘要**。**

**Important considerations:**
- You're charged for the **full thinking tokens** generated, not the summary tokens
- The billed output token count will **not match** the tokens you see in the response
- The first few lines of thinking output are more verbose for prompt engineering purposes

**重要注意事项：**
- 你需要为**完整的思考 tokens** 付费，而不是摘要 tokens
- 计费的输出 token 数量**不匹配**你在响应中看到的 tokens
- 思考输出的前几行更详细，便于提示词工程

---

## Interleaved Thinking (Claude 4 Models) | 交织思考（Claude 4 模型）

Extended thinking with tool use in Claude 4 models supports **interleaved thinking**, which enables Claude to think between tool calls.

**Claude 4 模型中的扩展思考与工具使用支持**交织思考**，使 Claude 能够在工具调用之间进行思考。**

**Benefits:**
- Reason about tool call results before deciding next steps
- Chain multiple tool calls with reasoning steps in between
- Make more nuanced decisions based on intermediate results

**优势：**
- 在决定下一步之前对工具调用结果进行推理
- 在推理步骤之间链接多个工具调用
- 基于中间结果做出更细致的决策

**To enable**: Add the beta header `interleaved-thinking-2025-05-14` to your API request.

**启用方法**：在 API 请求中添加 beta 头 `interleaved-thinking-2025-05-14`。

---

## Extended Thinking with Tool Use | 扩展思考与工具使用

When using extended thinking with tool use:

**当使用扩展思考与工具使用时：**

1. **Tool choice limitation**: Only supports `tool_choice: {"type": "auto"}` or `tool_choice: {"type": "none"}`
2. **Preserve thinking blocks**: Must pass thinking blocks back to the API for the last assistant message

1. **工具选择限制**：只支持 `tool_choice: {"type": "auto"}` 或 `tool_choice: {"type": "none"}`
2. **保留思考块**：必须将思考块传回 API 用于最后一个助手消息

```python
# After tool use, include the thinking blocks
messages.append({
    "role": "assistant",
    "content": [
        {"type": "thinking", "thinking": "...", "signature": "..."},
        {"type": "tool_use", "id": "...", "name": "...", "input": {...}}
    ]
})
messages.append({
    "role": "user",
    "content": [{"type": "tool_result", "tool_use_id": "...", "content": "..."}]
})
```

---

## Thinking Encryption | 思考加密

Full thinking content is encrypted and returned in the `signature` field for verification.

**完整的思考内容被加密并在 `signature` 字段中返回以进行验证。**

**Key points:**
- `signature` values are significantly longer in Claude 4 than in previous models
- The `signature` field is opaque and should not be interpreted or parsed
- Values are compatible across platforms (Anthropic APIs, Amazon Bedrock, Vertex AI)

**关键点：**
- `signature` 值在 Claude 4 中比以前的模型长得多
- `signature` 字段是不透明的，不应被解释或解析
- 值在平台之间兼容（Anthropic APIs, Amazon Bedrock, Vertex AI）

### Thinking Redaction | 思考编辑

Occasionally Claude's internal reasoning will be flagged by safety systems. When this occurs, it's returned as a `redacted_thinking` block.

**有时 Claude 的内部推理会被安全系统标记。当这种情况发生时，它会作为 `redacted_thinking` 块返回。**

- Redacted blocks are decrypted when passed back to the API
- Claude can continue its response without losing context
- Consider informing users that some reasoning may be encrypted for safety

- 编辑块在传回 API 时会被解密
- Claude 可以继续其响应而不会丢失上下文
- 考虑告知用户某些推理可能因安全原因被加密

---

## Pricing | 定价

| Model | Base Input | Cache Writes | Cache Hits | Output |
|-------|------------|--------------|------------|--------|
| Claude Opus 4.1 | $15 / MTok | $18.75 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Opus 4 | $15 / MTok | $18.75 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Sonnet 4 | $3 / MTok | $3.75 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 3.7 | $3 / MTok | $3.75 / MTok | $0.30 / MTok | $15 / MTok |

**Charges apply to:**
- Tokens used during thinking (output tokens)
- Thinking blocks from the last assistant turn included in subsequent requests (input tokens)
- Standard text output tokens

**费用适用于：**
- 思考期间使用的 tokens（输出 tokens）
- 后续请求中包含的上一个助手轮次的思考块（输入 tokens）
- 标准文本输出 tokens

---

## Best Practices | 最佳实践

### Working with Budgets | 处理预算

1. **Start small**: Begin at 1,024 tokens and increase as needed
2. **从小开始**：从 1,024 tokens 开始，根据需要增加

3. **Complex tasks**: Use 16k+ tokens for thorough analysis
4. **复杂任务**：使用 16k+ tokens 进行彻底分析

5. **Monitor usage**: Track thinking token usage to optimize costs
6. **监控使用**：跟踪思考 token 使用情况以优化成本

### Performance Considerations | 性能考虑

1. **Response times**: Be prepared for longer response times
2. **响应时间**：准备好更长的响应时间

3. **Streaming required**: When `max_tokens` > 21,333, streaming is required
4. **需要流式传输**：当 `max_tokens` > 21,333 时，需要流式传输

5. **Large budgets**: Use batch processing for budgets above 32k
6. **大预算**：对于 32k 以上的预算使用批处理

### Feature Compatibility | 功能兼容性

- **Not compatible with**: `temperature`, `top_k` modifications, forced tool use, pre-filling
- **不兼容**：`temperature`、`top_k` 修改、强制工具使用、预填

- **Compatible with**: `top_p` values between 1 and 0.95
- **兼容**：`top_p` 值在 1 到 0.95 之间

### Usage Guidelines | 使用指南

- **Task selection**: Use for complex tasks benefiting from step-by-step reasoning
- **任务选择**：用于需要逐步推理的复杂任务

- **Context handling**: API automatically ignores thinking blocks from previous turns
- **上下文处理**：API 自动忽略之前轮次的思考块

- **Prompt engineering**: Review extended thinking prompting tips for best results
- **提示词工程**：查看扩展思考提示技巧以获得最佳结果

---

## Related Resources | 相关资源

- [Extended Thinking Tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips)
- [Chain of Thought Prompting](../03-Prompt工程/Chain-of-Thought/content.md)
