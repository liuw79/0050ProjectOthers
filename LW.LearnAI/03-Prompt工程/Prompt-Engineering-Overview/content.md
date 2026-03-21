# Prompt Engineering Overview | Prompt 工程概览

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

---

While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models here.

**这些技巧广泛适用于所有 Claude 模型，你也可以在这里找到针对扩展思考模型的特定提示技巧。**

---

## Before Prompt Engineering | 在 Prompt 工程之前

This guide assumes that you have:

**本指南假设你已经具备：**

1. A clear definition of the success criteria for your use case
2. **明确划分你用例的成功标准**

3. Some ways to empirically test against those criteria
4. **针对这些标准的实证测试方法**

5. A first draft prompt you want to improve
6. **你想要改进的初版提示词**

If not, we highly suggest you spend time establishing that first. Check out Define your success criteria and Create strong empirical evaluations for tips and guidance.

**如果没有，我们强烈建议你先花时间建立这些基础。请查看"定义成功标准"和"创建强实证评估"获取技巧和指导。**

### Prompt Generator | 提示词生成器

Don't have a first draft prompt? Try the prompt generator in the Anthropic Console!

**没有初版提示词？试试 Anthropic 控制台中的提示词生成器！**

---

## When to Prompt Engineer | 何时进行 Prompt 工程

This guide focuses on success criteria that are controllable through prompt engineering. Not every success criteria or failing eval is best solved by prompt engineering. For example, latency and cost can be sometimes more easily improved by selecting a different model.

**本指南专注于可以通过提示词工程控制的成功标准。并非所有成功标准或评估失败都最适合通过提示词工程解决。例如，延迟和成本有时可以通过选择不同的模型来更容易地改进。**

### Prompting vs. Finetuning | 提示词工程 vs. 微调

Prompt engineering is far faster than other methods of model behavior control, such as finetuning, and can often yield leaps in performance in far less time.

**提示词工程比其他模型行为控制方法（如微调）快得多，并且通常可以在更短的时间内实现性能飞跃。**

Here are some reasons to consider prompt engineering over finetuning:

**以下是选择提示词工程而非微调的一些理由：**

| Advantage | Description |
|---------|-------------|
| **Resource efficiency** | Fine-tuning requires high-end GPUs and large memory, while prompt engineering only needs text input |
| **资源效率** | 微调需要高端 GPU 和大内存，而提示词工程只需要文本输入 |

| **Cost-effectiveness** | For cloud-based AI services, fine-tuning incurs significant costs. Prompt engineering uses the base model, which is typically cheaper |
| **成本效益** | 对于云端 AI 服务，微调会产生大量成本。提示词工程使用基础模型，通常更便宜 |

| **Maintaining model updates** | When providers update models, fine-tuned versions might need retraining. Prompts usually work across versions without changes |
| **模型更新维护** | 当提供商更新模型时，微调版本可能需要重新训练。提示词通常可以跨版本工作而无需更改 |

| **Time-saving** | Fine-tuning can take hours or even days. In contrast, prompt engineering provides nearly instantaneous results |
| **节省时间** | 微调可能需要数小时甚至数天。相比之下，提示词工程几乎可以即时获得结果 |

| **Minimal data needs** | Fine-tuning needs substantial task-specific, labeled data. Prompt engineering works with few-shot or even zero-shot learning |
| **最小数据需求** | 微调需要大量特定任务的标注数据。提示词工程可以使用少样本甚至零样本学习 |

| **Flexibility & rapid iteration** | Quickly try various approaches, tweak prompts, and see immediate results |
| **灵活性和快速迭代** | 快速尝试各种方法，调整提示词，并立即看到结果 |

| **Domain adaptation** | Easily adapt models to new domains by providing domain-specific context in prompts |
| **领域适应** | 通过在提示词中提供特定领域的上下文，轻松将模型适应到新领域 |

| **Comprehension improvements** | Prompt engineering is far more effective than finetuning at helping models better understand and utilize external content |
| **理解改进** | 提示词工程比微调更有效地帮助模型更好地理解和利用外部内容 |

| **Preserves general knowledge** | Fine-tuning risks catastrophic forgetting. Prompt engineering maintains the model's broad capabilities |
| **保留通用知识** | 微调存在灾难性遗忘的风险。提示词工程保持了模型的广泛能力 |

| **Transparency** | Prompts are human-readable, showing exactly what information the model receives |
| **透明度** | 提示词是人类可读的，准确显示模型接收到的信息 |

---

## How to Prompt Engineer | 如何进行 Prompt 工程

The prompt engineering pages in this section have been organized from most broadly effective techniques to more specialized techniques. When troubleshooting performance, we suggest you try these techniques in order:

**本节的提示词工程页面已按照从最广泛有效的技术到更专业的技术的顺序组织。在排查性能问题时，我们建议你按顺序尝试这些技术：**

1. **Prompt generator** - Use the Anthropic Console tool
2. **提示词生成器** - 使用 Anthropic 控制台工具

3. **Be clear and direct** - Give explicit instructions
4. **清晰直接** - 给出明确的指令

5. **Use examples (multishot)** - Provide 3-5 relevant examples
6. **使用示例（多样本）** - 提供 3-5 个相关示例

7. **Let Claude think (CoT)** - Enable step-by-step reasoning
8. **让 Claude 思考（CoT）** - 启用逐步推理

9. **Use XML tags** - Structure your prompts clearly
10. **使用 XML 标签** - 清晰地结构化你的提示词

11. **Give Claude a role** - Set expertise via system prompts
12. **赋予 Claude 角色** - 通过系统提示词设定专业知识

13. **Prefill Claude's response** - Control output format
14. **预填 Claude 响应** - 控制输出格式

15. **Chain complex prompts** - Break down complex tasks
16. **链式复杂提示词** - 分解复杂任务

17. **Long context tips** - Optimize for 200k context window
18. **长上下文技巧** - 针对 200k 上下文窗口优化

---

## Prompt Engineering Tutorial | Prompt 工程教程

If you're an interactive learner, you can dive into our interactive tutorials instead!

**如果你是交互式学习者，可以深入我们的交互式教程！**

### GitHub Prompting Tutorial | GitHub 提示词教程

An example-filled tutorial that covers the prompt engineering concepts found in our docs.

**一个充满示例的教程，涵盖了我们文档中的提示词工程概念。**

### Google Sheets Prompting Tutorial | Google Sheets 提示词教程

A lighter weight version of our prompt engineering tutorial via an interactive spreadsheet.

**通过交互式电子表格提供的轻量版提示词工程教程。**

---

## Quick Reference | 快速参考

| Technique | Best For | Key Tip |
|-----------|----------|---------|
| **Be clear & direct** | All tasks | Explain exactly what you want |
| **清晰直接** | 所有任务 | 准确解释你想要什么 |
| **Multishot** | Structured outputs | 3-5 diverse examples in `<example>` tags |
| **多样本** | 结构化输出 | 在 `<example>` 标签中提供 3-5 个多样化示例 |
| **Chain of thought** | Complex reasoning | Use `<thinking>` tags to separate reasoning |
| **链式思考** | 复杂推理 | 使用 `<thinking>` 标签分离推理 |
| **XML tags** | Multi-part prompts | Structure with `<instructions>`, `<data>`, etc. |
| **XML 标签** | 多部分提示词 | 用 `<instructions>`、`<data>` 等结构化 |
| **Role prompting** | Domain-specific tasks | Set role in `system` parameter |
| **角色提示** | 特定领域任务 | 在 `system` 参数中设置角色 |
| **Prefilling** | Format control | Start response with `{` or tag |
| **预填** | 格式控制 | 用 `{` 或标签开始响应 |

---

## Related Resources | 相关资源

- [Claude 4 Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
