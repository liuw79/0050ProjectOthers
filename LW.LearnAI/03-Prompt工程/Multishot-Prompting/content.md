# Use Examples (Multishot Prompting) | 使用示例（多样本提示）

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting

---

Examples are your secret weapon shortcut for getting Claude to generate exactly what you need. By providing a few well-crafted examples in your prompt, you can dramatically improve the accuracy, consistency, and quality of Claude's outputs.

**示例是你让 Claude 精确生成所需内容的秘密武器捷径。** 只要在提示词中提供几个精心设计的示例，就能大幅提高 Claude 输出的准确性、一致性和质量。

---

This technique, known as **few-shot** or **multishot prompting**, is particularly effective for tasks that require structured outputs or adherence to specific formats.

这种技术被称为**少样本（few-shot）**或**多样本提示（multishot prompting）**，对于需要结构化输出或遵循特定格式的任务特别有效。

**Power up your prompts**: Include 3-5 diverse, relevant examples to show Claude exactly what you want. More examples = better performance, especially for complex tasks.

**强化你的提示词**：包含 3-5 个多样化、相关的示例，向 Claude 展示你确切想要什么。示例越多 = 效果越好，特别是对于复杂任务。

---

## Why Use Examples? | 为什么使用示例？

| Benefit | Description | 优势 | 描述 |
|---------|-------------|------|------|
| **Accuracy** | Examples reduce misinterpretation of instructions | **准确性** | 示例减少对指令的误解 |
| **Consistency** | Examples enforce uniform structure and style | **一致性** | 示例强制执行统一的结构和风格 |
| **Performance** | Well-chosen examples boost Claude's ability to handle complex tasks | **性能** | 精心选择的示例提升 Claude 处理复杂任务的能力 |

---

## Crafting Effective Examples | 制作有效的示例

For maximum effectiveness, make sure that your examples are:

为了达到最大效果，请确保你的示例：

- **Relevant**: Your examples mirror your actual use case
- **相关性**：示例反映你的实际用例

- **Diverse**: Your examples cover edge cases and potential challenges, and vary enough that Claude doesn't inadvertently pick up on unintended patterns
- **多样性**：示例涵盖边缘情况和潜在挑战，并且足够多样化，以免 Claude 意外学到非预期的模式

- **Clear**: Your examples are wrapped in `<example>` tags (if multiple, nested within `<examples>` tags) for structure
- **清晰性**：示例用 `<example>` 标签包装（如果有多个，嵌套在 `<examples>` 标签内）以保持结构

**Tip**: Ask Claude to evaluate your examples for relevance, diversity, or clarity. Or have Claude generate more examples based on your initial set.

**提示**：让 Claude 评估你的示例的相关性、多样性或清晰度。或者让 Claude 基于你的初始示例集生成更多示例。

---

## Example: Analyzing Customer Feedback | 示例：分析客户反馈

### Without Examples | 不使用示例

```
Analyze this customer feedback and categorize the issues. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low).

Here is the feedback: {{FEEDBACK}}
```

**Claude's Response:**

```
Here's the analysis of the customer feedback:

Issue: UI/UX
Sentiment: Negative
Priority: High
The customer is frustrated with the new dashboard design...

Issue: Integration
Sentiment: Positive
Priority: Medium
The customer is pleased with the existing Salesforce integration...

[Long explanations for each item - 每项都有冗长的解释]
```

Notice that in the "no examples" version, Claude does not list multiple options for each category, despite its written analysis indicating that there are multiple categories for certain feedback. It also includes a long explanation when we may not want it to.

注意，在"无示例"版本中，尽管 Claude 的书面分析表明某些反馈有多个类别，但它并没有为每个类别列出多个选项。它还包含了我们可能不需要的冗长解释。

---

### With Examples | 使用示例

```
Our CS team is overwhelmed with unstructured feedback. Your task is to analyze feedback and categorize issues for our product and engineering teams.

Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other.
Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low).

Here is an example:
<example>
Input: The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!
Category: UI/UX, Performance
Sentiment: Negative
Priority: High
</example>

Now, analyze this feedback: {{FEEDBACK}}
```

**Claude's Response:**

```
1. The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!
Category: UI/UX, Performance
Sentiment: Negative
Priority: High

2. Love the Salesforce integration! But it'd be great if you could add Hubspot too.
Category: Integration, Feature Request
Sentiment: Positive
Priority: Medium

[Clean, consistent formatting for all items - 所有项目干净、一致的格式]
```

---

## Key Takeaways | 关键要点

1. **3-5 examples is optimal** - Too few won't provide enough guidance; too many may confuse
2. **3-5 个示例是最佳的** - 太少无法提供足够指导；太多可能会造成混淆

3. **Use consistent formatting** - Wrap examples in `<example>` tags
4. **使用一致的格式** - 用 `<example>` 标签包装示例

5. **Cover edge cases** - Include examples that demonstrate handling of tricky situations
6. **涵盖边缘情况** - 包含展示处理棘手情况的示例

7. **Match your desired output** - Examples should show exactly the format and style you want
8. **匹配你想要的输出** - 示例应该准确展示你想要的格式和风格

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [GitHub Prompting Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
