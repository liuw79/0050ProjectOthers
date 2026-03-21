# Claude Code 使用指南

## 概述
Claude Code 是 Anthropic 公司开发的 AI 编程助手命令行工具，可以在终端中直接与 Claude AI 进行交互。

## 重要说明
✅ **Claude Code 现已正式发布！**

正确的包名是：`@anthropic-ai/claude-code`

⚠️ **注意**：之前测试的包名都是错误的：
- ❌ `@anthropic-ai/claude-cli` (错误)
- ❌ `claude-cli` (错误)
- ❌ `claude-code` (错误)
- ❌ `@anthropic/claude-cli` (错误)
- ✅ `@anthropic-ai/claude-code` (正确)

## 安装方法

### 系统要求 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/setup" index="3">3</mcreference>
- **操作系统**：macOS 10.15+, Ubuntu 20.04+/Debian 10+, 或 Windows 10+ (需要 WSL 1, WSL 2, 或 Git for Windows)
- **硬件**：4GB+ RAM
- **软件**：Node.js 18+
- **网络**：需要互联网连接进行认证和AI处理
- **Shell**：在 Bash, Zsh 或 Fish 中效果最佳

### 标准安装 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/overview" index="2">2</mcreference>

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 导航到你的项目目录
cd your-awesome-project

# 开始使用 Claude
claude
```

### Windows 安装选项 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/setup" index="3">3</mcreference>

**选项1：在 WSL 中使用 Claude Code**
- 支持 WSL 1 和 WSL 2

**选项2：在原生 Windows 上使用 Git Bash**
- 需要安装 Git for Windows
- 对于便携式 Git 安装，需要指定 bash.exe 的路径

## 认证方式 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/setup" index="3">3</mcreference>

Claude Code 提供以下认证选项：

1. **Anthropic Console**（默认选项）
   - 通过 Anthropic Console 连接并完成 OAuth 流程
   - 需要在 console.anthropic.com 激活计费

2. **Claude App（Pro 或 Max 计划）**
   - 订阅 Claude 的 Pro 或 Max 计划
   - 统一订阅包含 Claude Code 和网页界面
   - 使用 Claude.ai 账户登录

3. **企业平台**
   - 配置 Claude Code 使用 Amazon Bedrock 或 Google Vertex AI
   - 适用于企业部署

## 主要功能 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/overview" index="2">2</mcreference>

### 核心能力
- **从描述构建功能**：用简单的英语告诉 Claude 你想构建什么，它会制定计划、编写代码并确保正常工作
- **调试和修复问题**：描述错误或粘贴错误消息，Claude Code 会分析代码库、识别问题并实施修复
- **导航任何代码库**：询问团队代码库的任何问题，获得深思熟虑的答案
- **自动化繁琐任务**：修复 lint 问题、解决合并冲突、编写发布说明

### 为什么开发者喜欢 Claude Code <mcreference link="https://docs.anthropic.com/en/docs/claude-code/overview" index="2">2</mcreference>
- **在终端中工作**：不是另一个聊天窗口或IDE，Claude Code 在你已经工作的地方与你相遇
- **采取行动**：Claude Code 可以直接编辑文件、运行命令和创建提交
- **Unix 哲学**：Claude Code 是可组合和可脚本化的
- **企业就绪**：使用 Anthropic 的 API，或在 AWS 或 GCP 上托管

## 推荐终端软件（Mac）

### 1. iTerm2（强烈推荐）✅ 已安装
- **下载地址**: https://iterm2.com/
- **特点**: 
  - 支持分屏和标签页
  - 丰富的主题和配色方案
  - 支持图片显示和截图粘贴
  - 强大的搜索功能
  - 支持热键快速调出
  - 自动补全和历史记录
- **安装**: `brew install --cask iterm2` ✅ 安装成功
- **使用提示**: 安装后可在Applications文件夹中找到iTerm.app，建议替代系统自带终端使用
- **暗色模式设置**:
  1. 打开iTerm2 → 按 `Cmd + ,` 打开偏好设置
  2. 选择 `Profiles` → `Colors`
  3. 在 `Color Presets` 下拉菜单中选择暗色主题：
     - `Dark Background` (经典暗色)
     - `Solarized Dark` (护眼暗色)
     - `Dracula` (流行暗色主题)
  4. 点击右下角的 `Set as Default` 设为默认
- **贴图功能**:
  1. **截图粘贴**: 截图后直接按 `Cmd + V` 粘贴到终端
  2. **拖拽图片**: 直接将图片文件拖拽到iTerm2窗口中
  3. **显示图片**: 使用 `imgcat` 命令显示图片文件
     ```bash
     # 安装imgcat（如果未安装）
     curl -L https://iterm2.com/utilities/imgcat > /usr/local/bin/imgcat
     chmod +x /usr/local/bin/imgcat
     
     # 显示图片
     imgcat image.png
     ```
  4. **启用图片显示**: 
      - **最新版本**：图片显示功能默认已启用，无需额外设置
      - **高级设置**：Preferences → Advanced → 搜索 "Show inline images at Retina resolution" 可调整显示效果
      - **验证方法**：直接在终端中按 `Cmd+V` 粘贴截图或使用 `imgcat` 命令测试
      - **注意**：iTerm2 3.2.0+ 版本已内置支持图片显示，支持PNG、GIF、PDF等多种格式

### 2. Warp（现代化终端）
- **下载地址**: https://www.warp.dev/
- **特点**:
  - 现代化UI设计
  - 内置AI助手
  - 支持块编辑模式
  - 智能补全
  - 支持协作功能
- **安装**: `brew install --cask warp`

### 3. Hyper（基于Electron）
- **下载地址**: https://hyper.is/
- **特点**:
  - 基于Web技术构建
  - 高度可定制
  - 丰富的插件生态
  - 支持主题和扩展
- **安装**: `brew install --cask hyper`

### 4. Alacritty（高性能）
- **下载地址**: https://alacritty.org/
- **特点**:
  - 使用GPU加速
  - 极快的渲染速度
  - 配置文件驱动
  - 跨平台支持
- **安装**: `brew install --cask alacritty`

### 推荐配置
对于Claude Code使用，推荐iTerm2配合以下设置：
1. 启用"Paste images as base64"功能支持截图粘贴
2. 设置合适的字体大小和配色方案
3. 配置热键快速调出终端
4. 启用分屏功能便于多任务处理

## 替代方案

如果无法使用 Claude Code，以下是其他选择：

### 1. 使用 Claude 网页版
- 访问：https://claude.ai
- 需要 Claude Pro 或 Max 订阅
- 功能完整，支持代码编辑

### 2. 使用 Cursor IDE
- 下载：https://cursor.sh
- 内置 Claude 3.5 Sonnet
- 专为编程设计的 AI IDE

### 3. 使用 VS Code 扩展
- 搜索 "Claude" 相关扩展
- 或使用 "Continue" 扩展配置 Claude API

### 4. 直接使用 Anthropic API
```bash
# 安装 Python SDK
pip install anthropic

# 或使用 Node.js SDK
npm install @anthropic-ai/sdk
```

## 疑难解答：`claude` 命令无法识别

### 问题描述
在 PowerShell 中运行 `claude` 命令时出现错误：
```
claude : 无法将"claude"项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

### 解决方案

#### 方案1：检查包是否存在
```powershell
# 搜索可用的 Claude 相关包
npm search claude

# 检查已安装的全局包
npm list -g --depth=0
```

#### 方案2：手动修复 PATH 环境变量
```powershell
# 1. 获取 npm 全局路径
$npmPath = npm config get prefix
Write-Host "npm 全局路径: $npmPath"

# 2. 检查 PATH 是否包含 npm 路径
$env:PATH -split ';' | Where-Object { $_ -like "*npm*" }

# 3. 如果没有，手动添加
$env:PATH += ";$npmPath"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")

# 4. 重启 PowerShell 终端
```

#### 方案3：使用完整路径运行
```powershell
# 如果 claude.cmd 存在，使用完整路径
& "C:\Users\用户名\AppData\Roaming\npm\claude.cmd" --version
```

## 网络环境要求
- 需要稳定的海外网络环境
- 建议使用美国、英国或加拿大的 VPN 节点
- 确保可以访问 anthropic.com 域名

## 费用说明 <mcreference link="https://www.helicone.ai/blog/evaluating-claude-code" index="5">5</mcreference>

### API 定价
- **输入 tokens**：每百万 tokens $3
- **输出 tokens**：每百万 tokens $15（包含思考 tokens）

### 实际使用成本
- **轻度使用**：每个开发者每天 $5-10
- **中度使用**：每个开发者每天 $20-40
- **密集使用**：每小时可能超过 $100

### 订阅选项
- **Claude Pro**：$20/月（包含 Claude Code 和网页界面）
- **Claude Max**：$200/月（企业版）
- **Anthropic Console API**：按使用量计费

### 成本管理技巧 <mcreference link="https://www.helicone.ai/blog/evaluating-claude-code" index="5">5</mcreference>
- 使用 `/compact` 减少上下文大小
- 将复杂任务分解为更小、更专注的交互
- 在不相关任务之间使用 `/clear`
- 考虑在更广泛推广之前先从小试点组开始

## 注意事项

1. **正式发布**：Claude Code 现已正式发布，包名为 `@anthropic-ai/claude-code` <mcreference link="https://www.npmjs.com/package/@anthropic-ai/claude-code" index="1">1</mcreference>
2. **网络环境**：需要稳定的海外网络环境才能正常使用
3. **订阅要求**：需要付费订阅或 API 计费才能使用
4. **Windows 支持**：需要 WSL 或 Git Bash 环境 <mcreference link="https://docs.anthropic.com/en/docs/claude-code/setup" index="3">3</mcreference>
5. **响应时间**：相比 IDE 集成工具可能响应较慢 <mcreference link="https://www.helicone.ai/blog/evaluating-claude-code" index="5">5</mcreference>
6. **安全性**：代码会发送到 Anthropic 服务器进行处理，但有多层权限保护 <mcreference link="https://www.helicone.ai/blog/evaluating-claude-code" index="5">5</mcreference>

## 常见问题

### Q: 为什么之前无法安装 Claude CLI？
A: 之前使用了错误的包名。正确的包名是 `@anthropic-ai/claude-code`，而不是 `@anthropic-ai/claude-cli` 或其他变体。

### Q: 有免费的 Claude 使用方式吗？
A: Claude 网页版提供有限的免费使用，但完整功能需要付费订阅。

### Q: 如何在中国大陆使用 Claude？
A: 需要使用 VPN 连接海外网络，并且需要海外手机号注册账户。

## 基本使用 <mcreference link="https://medium.com/@dan.avila7/claude-code-from-zero-to-hero-bebe2436ac32" index="4">4</mcreference>

### 初始化项目
```bash
# 使用 /init 命令生成 CLAUDE.md 项目指南
/init
```

### 基本命令
- `/help` - 查看所有可用命令
- `/clear` - 重置对话上下文
- `/config` - 修改 Claude Code 的初始配置
- `/ide` - 连接到你的 IDE（VS Code, Cursor, Windsorf 或 JetBrains）
- `/compact` - 减少上下文大小以节省成本

### 使用示例
```bash
# 了解项目
> what does this project do?
> explain the folder structure

# 代码修改
> Create a GitHub Action that automatically creates releases

# 安全扫描（Unix 风格）
cat package.json | claude -p "review this file for security vulnerabilities" > security_report.txt
```

### 自定义斜杠命令 <mcreference link="https://medium.com/@dan.avila7/claude-code-from-zero-to-hero-bebe2436ac32" index="4">4</mcreference>

创建可重用的提示：
```bash
# 创建项目命令（团队共享）
mkdir -p .claude/commands
echo "Analyze this code for security vulnerabilities:" > .claude/commands/security-review.md

# 使用命令
> /project:security-review

# 个人命令（仅自己使用）
echo "Optimize this code:" > ~/.claude/commands/optimize.md
> /user:optimize
```

## 更新日志
- 2025-01-15：发现并更正正确的包名 `@anthropic-ai/claude-code`
- 2025-01-15：添加完整的安装指南和使用说明
- 2025-01-15：添加费用说明和成本管理技巧

---

如需更多帮助，请参考：
- [Anthropic 官方文档](https://docs.anthropic.com)
- [Claude 网页版](https://claude.ai)
- [Cursor IDE](https://cursor.sh)