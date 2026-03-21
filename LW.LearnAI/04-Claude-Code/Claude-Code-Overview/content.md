# Claude Code Overview | Claude Code 概览

> Source: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview

---

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands. By integrating directly with your development environment, Claude Code streamlines your workflow without requiring additional servers or complex setup.

**Claude Code 是一个代理编码工具，它存在于你的终端中，理解你的代码库，并通过自然语言命令帮助你更快地编码。通过直接集成到你的开发环境中，Claude Code 简化了你的工作流程，无需额外的服务器或复杂的设置。**

---

## Key Capabilities | 核心能力

- **Editing files and fixing bugs** across your codebase
- **编辑文件和修复 bug** - 在整个代码库中

- **Answering questions** about your code's architecture and logic
- **回答问题** - 关于代码的架构和逻辑

- **Executing and fixing tests**, linting, and other commands
- **执行和修复测试**、linting 和其他命令

- **Searching through git history**, resolving merge conflicts, and creating commits and PRs
- **搜索 git 历史**、解决合并冲突、创建提交和 PR

---

## System Requirements | 系统要求

| Requirement | Details |
|-------------|---------|
| **Operating Systems** | macOS 10.15+, Ubuntu 20.04+/Debian 10+, Windows via WSL |
| **Hardware** | 4GB RAM minimum |
| **Software** | Node.js 18+, git 2.23+ (optional), GitHub/GitLab CLI (optional), ripgrep (optional) |
| **Network** | Internet connection required |

| 要求 | 详情 |
|------|------|
| **操作系统** | macOS 10.15+, Ubuntu 20.04+/Debian 10+, Windows 通过 WSL |
| **硬件** | 4GB RAM 最低 |
| **软件** | Node.js 18+, git 2.23+（可选）, GitHub/GitLab CLI（可选）, ripgrep（可选） |
| **网络** | 需要互联网连接 |

---

## Core Features | 核心功能

### Security and Privacy by Design | 设计上的安全和隐私

- **Direct API connection**: Queries go straight to Anthropic's API
- **直接 API 连接**：查询直接发送到 Anthropic 的 API

- **Works where you work**: Operates directly in your terminal
- **在你工作的地方工作**：直接在你的终端中操作

- **Understands context**: Maintains awareness of your entire project structure
- **理解上下文**：保持对整个项目结构的感知

- **Takes action**: Performs real operations like editing files and creating commits
- **采取行动**：执行实际操作，如编辑文件和创建提交

### From Questions to Solutions | 从问题到解决方案

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed.

**Claude Code 直接在你的终端中操作，理解你的项目上下文并采取实际行动。无需手动将文件添加到上下文 - Claude 会根据需要探索你的代码库。**

---

## CLI Commands | CLI 命令

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Run one-off query | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude config` | Configure settings | `claude config set --global theme dark` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure MCP servers | See MCP tutorials |

| 命令 | 描述 | 示例 |
|------|------|------|
| `claude` | 启动交互式 REPL | `claude` |
| `claude "query"` | 以初始提示启动 | `claude "explain this project"` |
| `claude -p "query"` | 运行一次性查询 | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | 处理管道内容 | `cat logs.txt \| claude -p "explain"` |
| `claude config` | 配置设置 | `claude config set --global theme dark` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude mcp` | 配置 MCP 服务器 | 参见 MCP 教程 |

### CLI Flags | CLI 标志

- `--print` or `-p`: Print response without interactive mode
- `--print` 或 `-p`：无交互模式打印响应

- `--verbose`: Enable verbose logging
- `--verbose`：启用详细日志

- `--dangerously-skip-permissions`: Skip permission prompts (only in Docker)
- `--dangerously-skip-permissions`：跳过权限提示（仅在 Docker 中）

---

## Slash Commands | 斜杠命令

| Command | Purpose |
|---------|---------|
| `/bug` | Report bugs (sends conversation to Anthropic) |
| `/clear` | Clear conversation history |
| `/compact` | Compact conversation to save context space |
| `/config` | View/modify configuration |
| `/cost` | Show token usage statistics |
| `/doctor` | Check installation health |
| `/help` | Get usage help |
| `/init` | Initialize project with CLAUDE.md guide |
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from your account |
| `/pr_comments` | View pull request comments |
| `/review` | Request code review |
| `/terminal-setup` | Install Shift+Enter key binding |
| `/vim` | Enter vim mode |

| 命令 | 目的 |
|------|------|
| `/bug` | 报告 bug（发送对话给 Anthropic） |
| `/clear` | 清除对话历史 |
| `/compact` | 压缩对话以节省上下文空间 |
| `/config` | 查看/修改配置 |
| `/cost` | 显示 token 使用统计 |
| `/doctor` | 检查安装健康状况 |
| `/help` | 获取使用帮助 |
| `/init` | 使用 CLAUDE.md 指南初始化项目 |
| `/login` | 切换 Anthropic 账户 |
| `/logout` | 从账户登出 |
| `/pr_comments` | 查看 pull request 评论 |
| `/review` | 请求代码审查 |
| `/terminal-setup` | 安装 Shift+Enter 键绑定 |
| `/vim` | 进入 vim 模式 |

---

## Permission System | 权限系统

| Tool Type | Example | Approval Required | "Yes, don't ask again" |
|-----------|---------|-------------------|------------------------|
| **Read-only** | File reads, LS, Grep | No | N/A |
| **Bash Commands** | Shell execution | Yes | Permanently per project |
| **File Modification** | Edit/write files | Yes | Until session end |

| 工具类型 | 示例 | 需要批准 | "是，不再询问" |
|----------|------|----------|----------------|
| **只读** | 文件读取、LS、Grep | 否 | 不适用 |
| **Bash 命令** | Shell 执行 | 是 | 每个项目永久 |
| **文件修改** | 编辑/写入文件 | 是 | 直到会话结束 |

### Available Tools | 可用工具

| Tool | Description | Permission |
|------|-------------|------------|
| AgentTool | Runs sub-agent for multi-step tasks | No |
| BashTool | Executes shell commands | Yes |
| GlobTool | Finds files by pattern | No |
| GrepTool | Searches file contents | No |
| LSTool | Lists files and directories | No |
| FileReadTool | Reads file contents | No |
| FileEditTool | Makes targeted edits | Yes |
| FileWriteTool | Creates/overwrites files | Yes |

| 工具 | 描述 | 权限 |
|------|------|------|
| AgentTool | 运行子代理处理多步骤任务 | 否 |
| BashTool | 执行 shell 命令 | 是 |
| GlobTool | 按模式查找文件 | 否 |
| GrepTool | 搜索文件内容 | 否 |
| LSTool | 列出文件和目录 | 否 |
| FileReadTool | 读取文件内容 | 否 |
| FileEditTool | 进行有针对性的编辑 | 是 |
| FileWriteTool | 创建/覆盖文件 | 是 |

---

## Configuration | 配置

### Global Configuration | 全局配置

| Key | Value | Description |
|-----|-------|-------------|
| `autoUpdaterStatus` | `disabled`/`enabled` | Enable auto-updater |
| `preferredNotifChannel` | `iterm2`, `iterm2_with_bell`, `terminal_bell`, `notifications_disabled` | Notification preference |
| `theme` | `dark`, `light`, `light-daltonized`, `dark-daltonized` | Color theme |
| `verbose` | `true`/`false` | Show full outputs |

| 键 | 值 | 描述 |
|----|----|----|
| `autoUpdaterStatus` | `disabled`/`enabled` | 启用自动更新器 |
| `preferredNotifChannel` | `iterm2`, `iterm2_with_bell`, `terminal_bell`, `notifications_disabled` | 通知偏好 |
| `theme` | `dark`, `light`, `light-daltonized`, `dark-daltonized` | 颜色主题 |
| `verbose` | `true`/`false` | 显示完整输出 |

### Project Configuration | 项目配置

| Key | Value | Description |
|-----|-------|-------------|
| `allowedTools` | array of tools | Tools that run without approval |
| `ignorePatterns` | array of glob strings | Files/directories to ignore |

| 键 | 值 | 描述 |
|----|----|----|
| `allowedTools` | 工具数组 | 无需批准即可运行的工具 |
| `ignorePatterns` | glob 字符串数组 | 要忽略的文件/目录 |

---

## Cost Management | 成本管理

Typical usage: **$5-10 per developer per day**, can exceed $100/hour during intensive use.

**典型使用：**每位开发者每天 $5-10**，在密集使用期间可能超过 $100/小时。**

### Track Costs | 跟踪成本

- Use `/cost` to see current session usage
- 使用 `/cost` 查看当前会话使用量

- Review cost summary when exiting
- 退出时查看成本摘要

- Check Anthropic Console for historical usage
- 在 Anthropic 控制台查看历史使用量

### Reduce Token Usage | 减少 Token 使用

- **Compact conversations**: Use `/compact` when context gets large
- **压缩对话**：当上下文变大时使用 `/compact`

- **Write specific queries**: Avoid vague requests
- **编写具体查询**：避免模糊请求

- **Break down tasks**: Split large tasks into focused interactions
- **分解任务**：将大型任务拆分为聚焦的交互

- **Clear history**: Use `/clear` to reset context
- **清除历史**：使用 `/clear` 重置上下文

---

## Third-Party API Connections | 第三方 API 连接

### Amazon Bedrock

```bash
export ANTHROPIC_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

### Google Vertex AI

```bash
export ANTHROPIC_BASE_URL=https://us-east5-aiplatform.googleapis.com/v1
export ANTHROPIC_VERTEX_BASE_URL=https://us-east5-aiplatform.googleapis.com/v1
```

---

## Initialize Your Project | 初始化你的项目

For first-time users:

**对于首次用户：**

1. Start Claude Code with `claude`
2. 使用 `claude` 启动 Claude Code

3. Try a simple command like `summarize this project`
4. 尝试一个简单的命令，如 `summarize this project`

5. Generate a CLAUDE.md project guide with `/init`
6. 使用 `/init` 生成 CLAUDE.md 项目指南

7. Ask Claude to commit the generated CLAUDE.md file
8. 让 Claude 提交生成的 CLAUDE.md 文件

---

## Related Resources | 相关资源

- [MCP Configuration](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/mcp)
- [Tutorials](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials)
- [Troubleshooting](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/troubleshooting)
