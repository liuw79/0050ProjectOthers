# Anthropic 官方指南文档库

> 采集时间：2026年3月6日
> 来源：https://docs.anthropic.com

## 文档格式

每个文档包含 **content.md** 文件，采用**双语段落对照**格式：
- 一段英文，一段中文
- 便于对照学习和翻译参考

## 目录结构

```
LW.LearnAI/
├── 01-入门指南/              # Getting Started
├── 02-模型概览/              # Models Overview
├── 03-Prompt工程/            # Prompt Engineering
├── 04-Claude-Code/           # Claude Code
├── 05-工具使用/              # Tools & MCP
├── 06-高级功能/              # Advanced Features
└── 07-Skills构建/            # Skills Building Guide
```

## 文档列表

### 01-入门指南
| 文档 | 双语版 |
|------|--------|
| Welcome to Claude | [content.md](01-入门指南/Welcome-to-Claude/content.md) |

### 02-模型概览
| 文档 | 双语版 |
|------|--------|
| Models Overview | [content.md](02-模型概览/Models-Overview/content.md) |

### 03-Prompt工程
| 文档 | 双语版 |
|------|--------|
| Prompt Engineering Overview | [content.md](03-Prompt工程/Prompt-Engineering-Overview/content.md) |
| Be Clear and Direct | [content.md](03-Prompt工程/Be-Clear-and-Direct/content.md) |
| Multishot Prompting | [content.md](03-Prompt工程/Multishot-Prompting/content.md) |
| Chain of Thought | [content.md](03-Prompt工程/Chain-of-Thought/content.md) |
| Use XML Tags | [content.md](03-Prompt工程/Use-XML-Tags/content.md) |
| System Prompts | [content.md](03-Prompt工程/System-Prompts/content.md) |
| Prefill Response | [content.md](03-Prompt工程/Prefill-Response/content.md) |

### 04-Claude-Code
| 文档 | 双语版 |
|------|--------|
| Claude Code Overview | [content.md](04-Claude-Code/Claude-Code-Overview/content.md) |

### 05-工具使用
| 文档 | 双语版 |
|------|--------|
| Tool Use Overview | [content.md](05-工具使用/Tool-Use-Overview/content.md) |
| Model Context Protocol (MCP) | [content.md](05-工具使用/MCP/content.md) |

### 06-高级功能
| 文档 | 双语版 |
|------|--------|
| Extended Thinking | [content.md](06-高级功能/Extended-Thinking/content.md) |

### 07-Skills构建
| 文档 | 双语版 |
|------|--------|
| Skills Building Complete Guide | [content.md](07-Skills构建/Skills-Building-Guide/content.md) |

---

## 核心要点速查

### Prompt 工程九大技巧
1. **清晰直接** - 明确告诉 Claude 你想要什么
2. **使用示例** - 提供 3-5 个相关示例
3. **链式思考** - 让 Claude 逐步思考复杂问题
4. **XML 标签** - 用标签结构化你的提示词
5. **角色设定** - 通过 system prompt 赋予 Claude 角色
6. **预填响应** - 控制 Claude 输出格式
7. **链式提示** - 复杂任务拆分为多个步骤
8. **长上下文技巧** - 有效利用 200k 上下文窗口
9. **扩展思考技巧** - 针对支持 extended thinking 的模型

### Skills 构建核心要点
1. **文件结构**：`SKILL.md`（必需）+ `scripts/` + `references/` + `assets/`
2. **YAML 前置数据**：`name` + `description`（必须包含 WHAT + WHEN）
3. **渐进式披露**：三级加载系统优化 token 使用
4. **命名规范**：kebab-case，无空格无大写
5. **MCP + Skills**：MCP 提供连接，Skills 提供知识

### 模型选择
| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Claude Opus 4.1 | 最智能 | 复杂任务、高精度需求 |
| Claude Sonnet 4 | 高性能平衡 | 大多数场景 |
| Claude Sonnet 3.7 | 支持扩展思考 | 需要深度推理的任务 |
| Claude Haiku 3.5 | 最快速度 | 简单任务、高吞吐量 |

---

## 参考资源

- [Anthropic 官方文档](https://docs.anthropic.com)
- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [Anthropic Cookbook (GitHub)](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Courses](https://github.com/anthropics/courses)
- [Skills 构建完整指南 PDF](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- [MCP 官方文档](https://modelcontextprotocol.io)
