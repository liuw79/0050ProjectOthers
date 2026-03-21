# All Models Overview | 模型总览

> Source: https://docs.anthropic.com/en/docs/about-claude/models

---

Claude is a family of state-of-the-art large language models developed by Anthropic.

**Claude 是 Anthropic 开发的最先进的大型语言模型系列。**

---

## Model Names | 模型名称

| Model | Anthropic API | AWS Bedrock | GCP Vertex AI |
|-------|---------------|-------------|---------------|
| Claude 3.7 Sonnet | `claude-3-7-sonnet-20250219` (`claude-3-7-sonnet-latest`) | `anthropic.claude-3-7-sonnet-20250219-v1:0` | `claude-3-7-sonnet@20250219` |
| Claude 3.5 Haiku | `claude-3-5-haiku-20241022` (`claude-3-5-haiku-latest`) | `anthropic.claude-3-5-haiku-20241022-v1:0` | `claude-3-5-haiku@20241022` |
| Claude 3.5 Sonnet v2 | `claude-3-5-sonnet-20241022` (`claude-3-5-sonnet-latest`) | `anthropic.claude-3-5-sonnet-20241022-v2:0` | `claude-3-5-sonnet-v2@20241022` |
| Claude 3.5 Sonnet | `claude-3-5-sonnet-20240620` | `anthropic.claude-3-5-sonnet-20240620-v1:0` | `claude-3-5-sonnet-v1@20240620` |
| Claude 3 Opus | `claude-3-opus-20240229` (`claude-3-opus-latest`) | `anthropic.claude-3-opus-20240229-v1:0` | `claude-3-opus@20240229` |
| Claude 3 Sonnet | `claude-3-sonnet-20240229` | `anthropic.claude-3-sonnet-20240229-v1:0` | `claude-3-sonnet@20240229` |
| Claude 3 Haiku | `claude-3-haiku-20240307` | `anthropic.claude-3-haiku-20240307-v1:0` | `claude-3-haiku@20240307` |

For convenience during development and testing, we offer **`-latest` aliases** for our models (e.g., `claude-3-7-sonnet-latest`). These aliases automatically point to the most recent snapshot of a given model.

**为方便开发和测试，我们为模型提供**`-latest` 别名**（例如 `claude-3-7-sonnet-latest`）。** 这些别名自动指向给定模型的最新快照。

**Warning**: While useful for experimentation, we recommend using specific model versions (e.g., `claude-3-7-sonnet-20250219`) in production applications to ensure consistent behavior.

**警告**：虽然对实验有用，但我们建议在生产应用程序中使用特定模型版本（例如 `claude-3-7-sonnet-20250219`）以确保一致的行为。

---

## Model Comparison Table | 模型对比表

| Feature | Claude 3.7 Sonnet | Claude 3.5 Sonnet | Claude 3.5 Haiku | Claude 3 Opus | Claude 3 Haiku |
|---------|-------------------|-------------------|------------------|---------------|----------------|
| **Description** | Our most intelligent model | Previous most intelligent model | Our fastest model | Powerful model for complex tasks | Fastest and most compact |
| **描述** | 最智能的模型 | 之前最智能的模型 | 最快的模型 | 复杂任务的强大模型 | 最快最紧凑 |

| **Strengths** | Highest intelligence with toggleable extended thinking | High level of intelligence and capability | Intelligence at blazing speeds | Top-level intelligence, fluency | Quick and accurate targeted performance |
| **优势** | 最高智能，支持可切换的扩展思考 | 高水平的智能和能力 | 极速的智能响应 | 顶级智能、流畅性 | 快速准确的目标性能 |

| **Multilingual** | Yes | Yes | Yes | Yes | Yes |
| **多语言** | 是 | 是 | 是 | 是 | 是 |

| **Vision** | Yes | Yes | Yes | Yes | Yes |
| **视觉** | 是 | 是 | 是 | 是 | 是 |

| **Extended thinking** | Yes | No | No | No | No |
| **扩展思考** | 是 | 否 | 否 | 否 | 否 |

| **Comparative latency** | Fast | Fast | Fastest | Moderately fast | Fastest |
| **延迟对比** | 快 | 快 | 最快 | 中等快 | 最快 |

| **Context window** | 200K | 200K | 200K | 200K | 200K |
| **上下文窗口** | 200K | 200K | 200K | 200K | 200K |

| **Cost (Input/Output per 1M tokens)** | $3.00 / $15.00 | $3.00 / $15.00 | $0.80 / $4.00 | $15.00 / $75.00 | $0.25 / $1.25 |
| **价格（输入/输出每百万tokens）** | $3.00 / $15.00 | $3.00 / $15.00 | $0.80 / $4.00 | $15.00 / $75.00 | $0.25 / $1.25 |

| **Training data cut-off** | Nov 2024 | Apr 2024 | July 2024 | Aug 2023 | Aug 2023 |
| **训练数据截止** | 2024年11月 | 2024年4月 | 2024年7月 | 2023年8月 | 2023年8月 |

---

## Prompt and Output Performance | 提示词和输出性能

Claude 3.7 Sonnet excels in:

**Claude 3.7 Sonnet 擅长：**

- **Benchmark performance**: Top-tier results in reasoning, coding, multilingual tasks, long-context handling, honesty, and image processing.
- **基准测试性能**：在推理、编码、多语言任务、长上下文处理、诚实度和图像处理方面取得顶级结果。

- **Engaging responses**: Claude models are ideal for applications that require rich, human-like interactions.
- **引人入胜的响应**：Claude 模型非常适合需要丰富、类人交互的应用程序。

- **Output quality**: When migrating from previous model generations to Claude 3.7 Sonnet, you may notice larger improvements in overall performance.
- **输出质量**：从之前的模型迁移到 Claude 3.7 Sonnet 时，你可能会注意到整体性能有更大的提升。

---

## Tips for Choosing a Model | 模型选择建议

| Model | Best For | 模型 | 最佳用途 |
|-------|----------|-------|----------|
| **Claude 3.7 Sonnet** | Complex tasks requiring deep reasoning | **Claude 3.7 Sonnet** | 需要深度推理的复杂任务 |
| **Claude 3.5 Sonnet** | Great balance of performance and cost | **Claude 3.5 Sonnet** | 性能和成本的良好平衡 |
| **Claude 3.5 Haiku** | High-volume, latency-sensitive applications | **Claude 3.5 Haiku** | 高吞吐量、延迟敏感的应用 |
| **Claude 3 Opus** | Tasks requiring maximum capability regardless of cost | **Claude 3 Opus** | 不考虑成本的最大能力任务 |
| **Claude 3 Haiku** | Simple, fast tasks with minimal cost | **Claude 3 Haiku** | 简单、快速的低成本任务 |

---

## Related Resources | 相关资源

- [Pricing](https://docs.anthropic.com/en/docs/about-claude/pricing)
- [Migrating to Claude 4](https://docs.anthropic.com/en/docs/about-claude/migrating-to-claude-4)
