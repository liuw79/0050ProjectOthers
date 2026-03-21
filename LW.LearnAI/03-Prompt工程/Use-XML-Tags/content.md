# Use XML Tags to Structure Your Prompts | 使用 XML 标签结构化提示词

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags

---

When your prompts involve multiple components like context, instructions, and examples, XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs.

**当你的提示词涉及多个组件（如上下文、指令和示例）时，XML 标签可以成为颠覆性的工具。** 它们帮助 Claude 更准确地解析你的提示词，从而产生更高质量的输出。

**XML tip**: Use tags like `<instructions>`, `<example>`, and `<formatting>` to clearly separate different parts of your prompt. This prevents Claude from mixing up instructions with examples or context.

**XML 提示**：使用 `<instructions>`、`<example>` 和 `<formatting>` 等标签清晰分隔提示词的不同部分。这可以防止 Claude 将指令与示例或上下文混淆。

---

## Why Use XML Tags? | 为什么使用 XML 标签？

| Benefit | Description |
|---------|-------------|
| **Clarity** | Clearly separate different parts of your prompt and ensure your prompt is well structured |
| **清晰性** | 清晰分隔提示词的不同部分，确保提示词结构良好 |

| **Accuracy** | Reduce errors caused by Claude misinterpreting parts of your prompt |
| **准确性** | 减少 Claude 误解提示词部分导致的错误 |

| **Flexibility** | Easily find, add, remove, or modify parts of your prompt without rewriting everything |
| **灵活性** | 轻松查找、添加、删除或修改提示词的部分，而无需重写所有内容 |

| **Parseability** | Having Claude use XML tags in its output makes it easier to extract specific parts of its response by post-processing |
| **可解析性** | 让 Claude 在输出中使用 XML 标签，便于通过后处理提取响应的特定部分 |

---

There are no canonical "best" XML tags that Claude has been trained with in particular, although we recommend that your tag names make sense with the information they surround.

**没有特定的"最佳" XML 标签是 Claude 特别训练过的，但我们建议你的标签名称与它们包围的信息有意义地相关。**

---

## Tagging Best Practices | 标签使用最佳实践

### 1. Be Consistent | 1. 保持一致

Use the same tag names throughout your prompts, and refer to those tag names when talking about the content (e.g, `Using the contract in <contract> tags...`)

**在提示词中使用相同的标签名称，并在谈论内容时引用这些标签名称（例如，"使用 <contract> 标签中的合同..."）**

### 2. Nest Tags | 2. 嵌套标签

You should nest tags `<outer><inner></inner></outer>` for hierarchical content.

**对于分层内容，你应该嵌套标签 `<outer><inner></inner></outer>`。**

**Power user tip**: Combine XML tags with other techniques like multishot prompting (`<examples>`) or chain of thought (`<thinking>`, `<answer>`). This creates super-structured, high-performance prompts.

**高级用户提示**：将 XML 标签与其他技术结合使用，如多样本提示（`<examples>`）或链式思考（`<thinking>`、`<answer>`）。这可以创建超级结构化、高性能的提示词。

---

## Examples | 示例

### Example 1: Generating Financial Reports | 示例 1：生成财务报告

Without XML tags, Claude misunderstands the task and generates a report that doesn't match the required structure or tone. After substitution, there is also a chance that Claude misunderstands where one section (like the Q1 report example) stops and another begins.

**不使用 XML 标签，Claude 会误解任务并生成不符合所需结构或语气的报告。替换后，Claude 还可能误解一个部分（如 Q1 报告示例）在哪里结束，另一个部分在哪里开始。**

#### Without XML Tags | 不使用 XML 标签

```
You're a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors. Include sections on Revenue Growth, Profit Margins, and Cash Flow, like with this example from last year: {{Q1_REPORT}}. Use data points from this spreadsheet: {{SPREADSHEET_DATA}}. The report should be extremely concise, to the point, professional, and in list format. It should highlight both strengths and areas for improvement.

你是 AcmeCorp 的财务分析师。为我们的投资者生成一份 Q2 财务报告。包括收入增长、利润率和现金流部分，就像去年这个例子一样：{{Q1_REPORT}}。使用这个电子表格中的数据点：{{SPREADSHEET_DATA}}。报告应该极其简洁、切中要害、专业，采用列表格式。它应该突出优势和需要改进的地方。
```

#### With XML Tags | 使用 XML 标签

```
You're a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors.

你是 AcmeCorp 的财务分析师。为我们的投资者生成一份 Q2 财务报告。

AcmeCorp is a B2B SaaS company. Our investors value transparency and actionable insights.

AcmeCorp 是一家 B2B SaaS 公司。我们的投资者重视透明度和可操作的洞察。

Use this data for your report:
<data>{{SPREADSHEET_DATA}}</data>

使用这些数据生成报告：
<data>{{SPREADSHEET_DATA}}</data>

<instructions>
1. Include sections: Revenue Growth, Profit Margins, Cash Flow.
2. Highlight strengths and areas for improvement.
</instructions>

<instructions>
1. 包括以下部分：收入增长、利润率、现金流。
2. 突出优势和需要改进的地方。
</instructions>

Make your tone concise and professional. Follow this structure:
<formatting_example>{{Q1_REPORT}}</formatting_example>

使你的语气简洁专业。遵循此结构：
<formatting_example>{{Q1_REPORT}}</formatting_example>
```

---

### Example 2: Legal Contract Analysis | 示例 2：法律合同分析

Without XML tags, Claude's analysis is disorganized and misses key points. With tags, it provides a structured, thorough analysis that a legal team can act on.

**不使用 XML 标签，Claude 的分析是混乱的，会遗漏关键点。使用标签后，它提供了法律团队可以采取行动的结构化、彻底的分析。**

#### Without XML Tags | 不使用 XML 标签

```
Analyze this software licensing agreement for potential risks and liabilities: {{CONTRACT}}. Focus on indemnification, limitation of liability, and IP ownership clauses. Also, note any unusual or concerning terms. Here's our standard contract for reference: {{STANDARD_CONTRACT}}. Give a summary of findings and recommendations for our legal team.

分析这份软件许可协议的潜在风险和责任：{{CONTRACT}}。关注赔偿、责任限制和知识产权所有权条款。还要注意任何不寻常或令人担忧的条款。这是我们的标准合同供参考：{{STANDARD_CONTRACT}}。为我们的法律团队提供发现和建议的摘要。
```

#### With XML Tags | 使用 XML 标签

```
Analyze this software licensing agreement for legal risks and liabilities.

分析这份软件许可协议的法律风险和责任。

We're a multinational enterprise considering this agreement for our core data infrastructure.

我们是一家正在考虑将此协议用于核心数据基础设施的跨国企业。

<agreement>{{CONTRACT}}</agreement>

<agreement>{{CONTRACT}}</agreement>

This is our standard contract for reference:
<standard_contract>{{STANDARD_CONTRACT}}</standard_contract>

这是我们的标准合同供参考：
<standard_contract>{{STANDARD_CONTRACT}}</standard_contract>

<instructions>
1. Analyze these clauses:
   - Indemnification
   - Limitation of liability
   - IP ownership
2. Note unusual or concerning terms.
3. Compare to our standard contract.
4. Summarize findings in <findings> tags.
5. List actionable recommendations in <recommendations> tags.
</instructions>

<instructions>
1. 分析以下条款：
   - 赔偿
   - 责任限制
   - 知识产权所有权
2. 注意不寻常或令人担忧的条款。
3. 与我们的标准合同进行比较。
4. 在 <findings> 标签中总结发现。
5. 在 <recommendations> 标签中列出可操作的建议。
</instructions>
```

---

## Key Takeaways | 关键要点

1. **Use meaningful tag names** - Tag names should describe their content
2. **使用有意义的标签名称** - 标签名称应该描述其内容

3. **Be consistent** - Use the same tags throughout your prompts
4. **保持一致** - 在提示词中使用相同的标签

5. **Nest when appropriate** - Use hierarchical structure for complex content
6. **适当时嵌套** - 对复杂内容使用分层结构

7. **Reference tags in instructions** - Tell Claude to use specific tags like "put your answer in <answer> tags"
8. **在指令中引用标签** - 告诉 Claude 使用特定标签，如"将你的答案放在 <answer> 标签中"

9. **Combine with other techniques** - XML tags work great with multishot and chain of thought
10. **与其他技术结合** - XML 标签与多样本和链式思考配合得很好

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [Chain of Thought](./Chain-of-Thought/content.md)
- [Multishot Prompting](./Multishot-Prompting/content.md)
