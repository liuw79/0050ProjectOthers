# The Complete Guide to Building Skills for Claude | Claude Skills 构建完整指南

> Source: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
> Released: January 29, 2026 | 33 Pages

> 来源：https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
> 发布日期：2026年1月29日 | 33页

---

## Table of Contents | 目录

1. [Introduction | 简介](#introduction--简介)
2. [Fundamentals | 基础知识](#fundamentals--基础知识)
3. [Planning and Design | 规划与设计](#planning-and-design--规划与设计)
4. [Testing and Iteration | 测试与迭代](#testing-and-iteration--测试与迭代)
5. [Distribution and Sharing | 分发与共享](#distribution-and-sharing--分发与共享)
6. [Patterns and Troubleshooting | 模式与故障排除](#patterns-and-troubleshooting--模式与故障排除)
7. [Resources and References | 资源与参考](#resources-and-references--资源与参考)

---

## Introduction | 简介

A **skill** is a set of instructions - packaged as a simple folder - that teaches Claude how to handle specific tasks or workflows. Skills are one of the most powerful ways to customize Claude for your specific needs.

**Skill（技能）** 是一组指令——打包成简单的文件夹——教会 Claude 如何处理特定任务或工作流程。Skills 是根据你的特定需求定制 Claude 最强大的方式之一。

Instead of re-explaining your preferences, processes, and domain expertise in every conversation, skills let you teach Claude once and benefit every time.

**无需在每次对话中重新解释你的偏好、流程和领域专业知识，Skills 让你只需教 Claude 一次，每次都能受益。**

### What You'll Learn | 你将学到什么

- Technical requirements and best practices for skill structure
- Skill 结构的技术要求和最佳实践

- Patterns for standalone skills and MCP-enhanced workflows
- 独立 Skills 和 MCP 增强工作流程的模式

- Patterns we've seen work well across different use cases
- 我们在不同用例中看到的成功模式

- How to test, iterate, and distribute your skills
- 如何测试、迭代和分发你的 Skills

### Who This Is For | 适合谁

- Developers who want Claude to follow specific workflows consistently
- 希望 Claude 一致遵循特定工作流程的开发者

- Power users who want Claude to follow specific workflows
- 希望 Claude 遵循特定工作流程的高级用户

- Teams looking to standardize how Claude works across their organization
- 希望在组织中标准化 Claude 工作方式的团队

### What You'll Get | 你将获得什么

By the end, you'll be able to build a functional skill in a single sitting. Expect about **15-30 minutes** to build and test your first working skill using the skill-creator.

**完成后，你将能够在一次会话中构建一个功能性的 Skill。使用 skill-creator 构建和测试你的第一个工作 Skill 大约需要**15-30 分钟**。**

---

## Fundamentals | 基础知识

### What is a Skill? | 什么是 Skill？

A skill is a folder containing:

**Skill 是一个包含以下内容的文件夹：**

```
your-skill-name/
├── SKILL.md        # Required - main skill file
├── scripts/        # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/     # Optional - documentation
│   ├── api-guide.md
│   └── examples/
└── assets/         # Optional - templates, etc.
    └── report-template.md
```

```
your-skill-name/
├── SKILL.md        # 必需 - 主 Skill 文件
├── scripts/        # 可选 - 可执行代码
│   ├── process_data.py
│   └── validate.sh
├── references/     # 可选 - 文档
│   ├── api-guide.md
│   └── examples/
└── assets/         # 可选 - 模板等
    └── report-template.md
```

### Core Design Principles | 核心设计原则

#### 1. Progressive Disclosure | 1. 渐进式披露

Skills use a three-level system:

**Skills 使用三级系统：**

| Level | Content | When Loaded |
|-------|---------|-------------|
| **Level 1** | YAML frontmatter | Always in Claude's system prompt |
| **Level 2** | SKILL.md body | When Claude thinks the skill is relevant |
| **Level 3** | Linked files | On-demand, as needed |

| 级别 | 内容 | 何时加载 |
|------|------|----------|
| **第一级** | YAML 前置数据 | 始终在 Claude 的系统提示中 |
| **第二级** | SKILL.md 正文 | 当 Claude 认为 Skill 相关时 |
| **第三级** | 链接文件 | 按需加载 |

This minimizes token usage while maintaining specialized expertise.

**这最小化了 token 使用量，同时保持专业化的专业知识。**

#### 2. Composability | 2. 可组合性

Claude can load multiple skills simultaneously. Your skill should work well alongside others.

**Claude 可以同时加载多个 Skills。你的 Skill 应该能与其他 Skills 协同工作。**

#### 3. Portability | 3. 可移植性

Skills work identically across **Claude.ai**, **Claude Code**, and **API**. Create once, use everywhere.

**Skills 在**Claude.ai**、**Claude Code** 和 **API** 中完全相同地工作。一次创建，随处使用。**

### Skills + MCP: The Kitchen Analogy | Skills + MCP：厨房类比

- **MCP** provides the professional kitchen: access to tools, ingredients, and equipment
- **MCP** 提供专业厨房：访问工具、食材和设备

- **Skills** provide the recipes: step-by-step instructions on how to create something valuable
- **Skills** 提供食谱：关于如何创造有价值内容的分步指令

Together, they enable users to accomplish complex tasks without figuring out every step themselves.

**两者结合，让用户能够完成复杂任务，而无需自己弄清楚每一步。**

---

## Planning and Design | 规划与设计

### Start with Use Cases | 从用例开始

Before writing any code, identify 2-3 concrete use cases your skill should enable.

**在编写任何代码之前，确定你的 Skill 应该支持的 2-3 个具体用例。**

**Good Use Case Definition:**

**良好的用例定义：**

```
Use Case: Project Sprint Planning
Trigger: User says "help me plan this sprint" or "create sprint tasks"

Steps:
1. Fetch current project status from Linear (via MCP)
2. Analyze team velocity and capacity
3. Suggest task prioritization
4. Create tasks in Linear with proper labels and estimates

Result: Fully planned sprint with tasks created
```

```
用例：项目冲刺规划
触发：用户说"帮我规划这个冲刺"或"创建冲刺任务"

步骤：
1. 从 Linear 获取当前项目状态（通过 MCP）
2. 分析团队速度和容量
3. 建议任务优先级
4. 在 Linear 中创建带有正确标签和估算的任务

结果：创建完整的冲刺计划
```

### Common Skill Use Case Categories | 常见 Skill 用例类别

| Category | Description | Example |
|----------|-------------|---------|
| **1. Document & Asset Creation** | Creating consistent, high-quality output | frontend-design skill |
| **2. Workflow Automation** | Multi-step processes with consistent methodology | skill-creator skill |
| **3. MCP Enhancement** | Workflow guidance to enhance MCP tool access | sentry-code-review skill |

| 类别 | 描述 | 示例 |
|------|------|------|
| **1. 文档和资产创建** | 创建一致、高质量的输出 | frontend-design skill |
| **2. 工作流程自动化** | 具有一致方法论的多步骤流程 | skill-creator skill |
| **3. MCP 增强** | 增强 MCP 工具访问的工作流程指导 | sentry-code-review skill |

### Technical Requirements | 技术要求

#### Critical Rules | 关键规则

**SKILL.md naming:**
- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted (SKILL.MD, skill.md, etc.)

**SKILL.md 命名：**
- 必须完全匹配 `SKILL.md`（区分大小写）
- 不接受变体（SKILL.MD, skill.md 等）

**Skill folder naming:**
- Use kebab-case: `notion-project-setup` ✅
- No spaces: `Notion Project Setup` ❌
- No underscores: `notion_project_setup` ❌
- No capitals: `NotionProjectSetup` ❌

**Skill 文件夹命名：**
- 使用 kebab-case：`notion-project-setup` ✅
- 不能有空格：`Notion Project Setup` ❌
- 不能有下划线：`notion_project_setup` ❌
- 不能有大写：`NotionProjectSetup` ❌

**No README.md inside skill folder:**
- All documentation goes in SKILL.md or references/

**Skill 文件夹内不要有 README.md：**
- 所有文档放在 SKILL.md 或 references/ 中

#### YAML Frontmatter: The Most Important Part | YAML 前置数据：最重要的部分

**Minimal Required Format:**

**最小必需格式：**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Field Requirements:**

**字段要求：**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | kebab-case only, matches folder name |
| `description` | Yes | What it does + When to use it (under 1024 chars, no XML tags) |
| `license` | Optional | MIT, Apache-2.0, etc. |
| `metadata` | Optional | author, version, mcp-server |

| 字段 | 必需 | 描述 |
|------|------|------|
| `name` | 是 | 仅 kebab-case，匹配文件夹名称 |
| `description` | 是 | 它做什么 + 何时使用（低于 1024 字符，无 XML 标签） |
| `license` | 否 | MIT, Apache-2.0 等 |
| `metadata` | 否 | author, version, mcp-server |

**Good Description Examples:**

**良好的描述示例：**

```yaml
# Good - specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Good - includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".
```

```yaml
# 好 - 具体且可操作
description: 分析 Figma 设计文件并生成开发者交接文档。当用户上传 .fig 文件、要求"设计规范"、"组件文档"或"设计到代码交接"时使用。

# 好 - 包含触发短语
description: 管理 Linear 项目工作流程，包括冲刺规划、任务创建和状态跟踪。当用户提到"sprint"、"Linear tasks"、"project planning"或要求"create tickets"时使用。
```

**Bad Description Examples:**

**糟糕的描述示例：**

```yaml
# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation systems.
```

```yaml
# 太模糊
description: 帮助处理项目。

# 缺少触发条件
description: 创建复杂的多页文档系统。
```

### Writing the Main Instructions | 编写主要指令

**Recommended Structure:**

**推荐结构：**

```markdown
---
name: your-skill
description: [...]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

## Examples

### Example 1: [common scenario]
User says: "Set up a new marketing campaign"

Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters

Result: Campaign created with confirmation link

## Troubleshooting

### Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

```markdown
---
name: your-skill
description: [...]
---

# 你的 Skill 名称

## 指令

### 步骤 1：[第一个主要步骤]
清楚解释会发生什么。

示例：
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

预期输出：[描述成功的样子]

## 示例

### 示例 1：[常见场景]
用户说："设置一个新的营销活动"

操作：
1. 通过 MCP 获取现有活动
2. 使用提供的参数创建新活动

结果：活动已创建，附带确认链接

## 故障排除

### 错误：[常见错误消息]
原因：[为什么会发生]
解决方案：[如何修复]
```

---

## Testing and Iteration | 测试与迭代

### Testing Approaches | 测试方法

| Approach | Best For |
|----------|----------|
| **Manual testing in Claude.ai** | Fast iteration, no setup |
| **Scripted testing in Claude Code** | Repeatable validation |
| **Programmatic testing via API** | Systematic evaluation |

| 方法 | 最适合 |
|------|--------|
| **在 Claude.ai 中手动测试** | 快速迭代，无需设置 |
| **在 Claude Code 中脚本测试** | 可重复的验证 |
| **通过 API 进行程序化测试** | 系统性评估 |

### Recommended Testing Approach | 推荐的测试方法

#### 1. Triggering Tests | 1. 触发测试

**Goal:** Ensure your skill loads at the right times.

**目标：** 确保 Skill 在正确的时间加载。

```
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
```

```
应该触发：
- "帮我在 ProjectHub 设置一个新的工作空间"
- "我需要在 ProjectHub 创建一个项目"
- "为 Q4 规划初始化一个 ProjectHub 项目"

不应该触发：
- "旧金山的天气怎么样？"
- "帮我写 Python 代码"
```

#### 2. Functional Tests | 2. 功能测试

**Goal:** Verify the skill produces correct outputs.

**目标：** 验证 Skill 产生正确的输出。

```
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
- Project created in ProjectHub
- 5 tasks created with correct properties
- All tasks linked to project
- No API errors
```

```
测试：创建包含 5 个任务的项目
给定：项目名称"Q4 规划"，5 个任务描述
当：Skill 执行工作流程
那么：
- 在 ProjectHub 中创建了项目
- 创建了 5 个具有正确属性的任务
- 所有任务链接到项目
- 没有 API 错误
```

#### 3. Performance Comparison | 3. 性能比较

| Metric | Without Skill | With Skill |
|--------|---------------|------------|
| User instructions | Each time | None |
| Back-and-forth messages | 15 | 2 |
| Failed API calls | 3 | 0 |
| Tokens consumed | 12,000 | 6,000 |

| 指标 | 没有 Skill | 有 Skill |
|------|------------|----------|
| 用户指令 | 每次 | 无 |
| 来回消息 | 15 | 2 |
| 失败的 API 调用 | 3 | 0 |
| 消耗的 Tokens | 12,000 | 6,000 |

### Using the skill-creator Skill | 使用 skill-creator Skill

The skill-creator skill can help you build and iterate on skills in 15-30 minutes.

**skill-creator skill 可以帮助你在 15-30 分钟内构建和迭代 Skills。**

**Capabilities:**
- Generate skills from natural language descriptions
- Produce properly formatted SKILL.md with frontmatter
- Flag common issues
- Suggest test cases

**功能：**
- 从自然语言描述生成 Skills
- 生成正确格式的 SKILL.md 和前置数据
- 标记常见问题
- 建议测试用例

**Usage:**

**用法：**

```
"Use the skill-creator skill to help me build a skill for [your use case]"
```

```
"使用 skill-creator skill 帮我为[你的用例]构建一个 skill"
```

### Iteration Based on Feedback | 基于反馈的迭代

| Signal | Solution |
|--------|----------|
| **Undertriggering** | Add more detail and keywords to description |
| **Overtriggering** | Add negative triggers, be more specific |
| **Execution issues** | Improve instructions, add error handling |

| 信号 | 解决方案 |
|------|----------|
| **触发不足** | 在描述中添加更多细节和关键词 |
| **过度触发** | 添加负面触发条件，更加具体 |
| **执行问题** | 改进指令，添加错误处理 |

---

## Distribution and Sharing | 分发与共享

### Current Distribution Model (January 2026) | 当前分发模型（2026年1月）

**Individual Users:**

**个人用户：**

1. Download the skill folder
2. 下载 Skill 文件夹

3. Zip the folder (if needed)
4. 压缩文件夹（如果需要）

5. Upload to Claude.ai via Settings > Capabilities > Skills
6. 通过设置 > 功能 > Skills 上传到 Claude.ai

7. Or place in Claude Code skills directory
8. 或放置在 Claude Code skills 目录中

**Organization-level Skills:**
- Admins can deploy skills workspace-wide
- Automatic updates
- Centralized management

**组织级 Skills：**
- 管理员可以在工作区范围内部署 Skills
- 自动更新
- 集中管理

### Skills via API | 通过 API 使用 Skills

**Key capabilities:**
- `/v1/skills` endpoint for listing and managing skills
- Add skills to Messages API requests via `container.skills` parameter
- Works with the Claude Agent SDK

**关键功能：**
- `/v1/skills` 端点用于列出和管理 Skills
- 通过 `container.skills` 参数将 Skills 添加到 Messages API 请求
- 与 Claude Agent SDK 配合使用

**Note:** Skills in the API require the Code Execution Tool beta.

**注意：** API 中的 Skills 需要 Code Execution Tool beta。

### Positioning Your Skill | 定位你的 Skill

**Focus on outcomes, not features:**

**专注于结果，而非功能：**

✅ Good:
```
"The ProjectHub skill enables teams to set up complete project workspaces in seconds — including pages, databases, and templates — instead of spending 30 minutes on manual setup."
```

✅ 好：
```
"ProjectHub skill 让团队能够在几秒钟内设置完整的项目工作空间——包括页面、数据库和模板——而不是花30分钟手动设置。"
```

❌ Bad:
```
"The ProjectHub skill is a folder containing YAML frontmatter and Markdown instructions that calls our MCP server tools."
```

❌ 差：
```
"ProjectHub skill 是一个包含 YAML 前置数据和 Markdown 指令的文件夹，它调用我们的 MCP 服务器工具。"
```

---

## Patterns and Troubleshooting | 模式与故障排除

### Pattern 1: Sequential Workflow Orchestration | 模式 1：顺序工作流程编排

Use when: Users need multi-step processes in a specific order.

**适用场景：用户需要按特定顺序的多步骤流程。**

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
```

```markdown
## 工作流程：新客户入职

### 步骤 1：创建账户
调用 MCP 工具：`create_customer`
参数：name, email, company

### 步骤 2：设置支付
调用 MCP 工具：`setup_payment_method`
等待：支付方式验证

### 步骤 3：创建订阅
调用 MCP 工具：`create_subscription`
参数：plan_id, customer_id（来自步骤 1）
```

### Pattern 2: Multi-MCP Coordination | 模式 2：多 MCP 协调

Use when: Workflows span multiple services.

**适用场景：工作流程跨越多个服务。**

```markdown
## Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications

## Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets

## Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to tasks
```

```markdown
## 阶段 1：设计导出（Figma MCP）
1. 从 Figma 导出设计资产
2. 生成设计规范

## 阶段 2：资产存储（Drive MCP）
1. 在 Drive 中创建项目文件夹
2. 上传所有资产

## 阶段 3：任务创建（Linear MCP）
1. 创建开发任务
2. 将资产链接附加到任务
```

### Pattern 3: Iterative Refinement | 模式 3：迭代优化

Use when: Output quality improves with iteration.

**适用场景：输出质量随迭代提高。**

```markdown
## Iterative Report Creation

### Initial Draft
1. Fetch data via MCP
2. Generate first draft report

### Quality Check
1. Run validation script
2. Identify issues

### Refinement Loop
1. Address each issue
2. Regenerate affected sections
3. Re-validate
```

```markdown
## 迭代报告创建

### 初始草稿
1. 通过 MCP 获取数据
2. 生成初稿报告

### 质量检查
1. 运行验证脚本
2. 识别问题

### 优化循环
1. 解决每个问题
2. 重新生成受影响的部分
3. 重新验证
```

### Troubleshooting | 故障排除

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill won't upload | File not named exactly SKILL.md | Rename to SKILL.md (case-sensitive) |
| Invalid frontmatter | YAML formatting issue | Add `---` delimiters |
| Invalid skill name | Name has spaces or capitals | Use kebab-case |
| Skill doesn't trigger | Description too generic | Add trigger phrases |
| Skill triggers too often | Description too broad | Add negative triggers, be more specific |

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Skill 无法上传 | 文件名不是完全匹配 SKILL.md | 重命名为 SKILL.md（区分大小写） |
| 前置数据无效 | YAML 格式问题 | 添加 `---` 分隔符 |
| Skill 名称无效 | 名称有空格或大写 | 使用 kebab-case |
| Skill 不触发 | 描述太通用 | 添加触发短语 |
| Skill 触发太频繁 | 描述太宽泛 | 添加负面触发条件，更加具体 |

---

## Resources and References | 资源与参考

### Official Documentation | 官方文档

- [Best Practices Guide](https://docs.anthropic.com)
- [Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-skills/skills/overview)
- [API Reference](https://docs.anthropic.com/en/api)
- [MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)

### Example Skills | 示例 Skills

- **GitHub**: [anthropics/skills](https://github.com/anthropics/skills)
- **Partner Skills Directory**: Asana, Atlassian, Canva, Figma, Sentry, Zapier
- **合作伙伴 Skills 目录**：Asana, Atlassian, Canva, Figma, Sentry, Zapier

### Quick Checklist | 快速检查清单

**Before Upload:**

**上传前：**

- [ ] Folder named in kebab-case
- [ ] 文件夹使用 kebab-case 命名

- [ ] SKILL.md file exists (exact spelling)
- [ ] SKILL.md 文件存在（精确拼写）

- [ ] YAML frontmatter has `---` delimiters
- [ ] YAML 前置数据有 `---` 分隔符

- [ ] name field: kebab-case, no spaces, no capitals
- [ ] name 字段：kebab-case，无空格，无大写

- [ ] description includes WHAT and WHEN
- [ ] description 包含做什么和何时使用

- [ ] No XML tags (`< >`) anywhere
- [ ] 任何地方都没有 XML 标签（`< >`）

- [ ] Instructions are clear and actionable
- [ ] 指令清晰可操作

---

## Enterprise Success Cases | 企业成功案例

| Company | Application | Result |
|---------|-------------|--------|
| Rakuten | Accounting & financial workflow automation | 8-hour tasks reduced to 1 hour |
| Notion | Seamless Claude-Notion collaboration | Faster Q&A to action, more predictable results |

| 公司 | 应用 | 结果 |
|------|------|------|
| Rakuten | 会计和财务工作流程自动化 | 8小时任务减少到1小时 |
| Notion | 无缝的 Claude-Notion 协作 | 更快从问答到行动，结果更可预测 |

---

> "Claude Skills may be more influential than MCP" — Simon Willison

> "Claude Skills 可能比 MCP 更有影响力" — Simon Willison
