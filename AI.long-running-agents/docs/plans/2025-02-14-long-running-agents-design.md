# 长运行代理开发系统设计文档

**日期：** 2025-02-14
**状态：** 设计中
**基于：** Anthropic "Effective harnesses for long-running agents"

---

## 1. 需求确认

### 1.1 项目目的
**类型：** 生产就绪框架
- 构建一个可复用的系统，用于部署实际的长运行代理应用

### 1.2 应用场景
**类型：** 项目规划与执行
- 需要长时间思考、规划和执行的项目级任务
- 代理需要在多个会话中持续取得进展

### 1.3 技术栈
**选择：** Python (原生)
- 轻量级、部署简单
- 适合快速开发和调试

**LLM 后端：** 多模型支持
- 设计抽象层支持多个 LLM 提供商
- 可配置的模型切换
- 支持：Anthropic Claude、OpenAI GPT、其他兼容 API

**用户界面：** CLI + 可选 Web Dashboard
- 核心功能通过命令行接口提供
- 可选的 Web 界面用于可视化监控和交互
- 满足开发者和普通用户不同需求

**目录结构：** 标准 Python 项目结构
```
AI.long-running-agents/
├── src/                  # 源代码
│   ├── __init__.py
│   ├── agents/           # 代理模块
│   ├── core/             # 核心组件
│   ├── tools/            # 工具集成
│   └── utils/            # 工具函数
├── tests/                # 测试
├── docs/                 # 文档
├── examples/             # 示例项目
├── config/               # 配置文件
├── pyproject.toml        # 项目配置
├── requirements.txt      # 依赖
└── README.md
```

**核心功能模块：**
1. **代理管理** - 管理初始化代理和编码代理的生命周期
2. **功能清单管理** - 解析和管理 feature_list.json 文件
3. **Git 集成** - 与 git 仓库交互，管理提交和版本
4. **测试执行** - 集成测试工具，执行端到端测试

**测试工具：** Puppeteer
- 文章中使用的工具
- 通过 MCP 服务器集成
- 支持截图和页面交互
- 验证端到端功能

### 1.4 核心特性需求
需要支持以下四个核心特性：
1. **人机交互介入** - 支持用户与运行中的代理进行交互
2. **状态监控与观察性** - 实时监控代理状态、进度和性能指标
3. **生命周期管理** - 支持暂停、恢复、取消和错误重试
4. **状态持久化** - 保存和恢复代理执行状态

---

## 2. 架构选择

### 2.1 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| 事件驱动架构 | 天然支持状态持久化、易于扩展、优秀观察性 | 需处理事件顺序和幂等性 |
| 状态机架构 | 状态转换清晰、生命周期管理直观 | 复杂场景下状态爆炸、灵活性低 |
| Actor模型架构 | 天然并发隔离、分布式扩展性好 | 实现复杂度高、调试难度大 |

### 2.2 最终选择
**方案：** 基于文章推荐的双代理架构

**选择理由：**
- 经过实际验证（Anthropic内部使用）
- 简单直接，易于理解
- git、JSON文件都是成熟的工具
- 天然支持状态持久化和生命周期管理

---

## 3. 双代理架构设计

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    双代理开发系统                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  初始化代理       │  首次   │  编码代理        │  后续    │
│  │  (Initializer)   │ ──────► │  (Coding Agent)  │ ─────►   │
│  └──────────────────┘         └──────────────────┘         │
│         │                              │                     │
│         │ 创建                         │ 每次会话增量推进     │
│         ▼                              ▼                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    项目环境                           │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │  • feature_list.json     (功能清单，200+项功能)      │    │
│  │  • claude-progress.txt  (进度日志)                  │    │
│  │  • init.sh               (环境启动脚本)              │    │
│  │  • git仓库               (版本控制)                  │    │
│  │  • 测试工具               (端到端验证)              │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 代理类型

#### 初始化代理 (Initializer Agent)
**职责：** 首次运行时设置开发环境

**创建的组件：**
- `init.sh` - 启动开发服务器的脚本
- `claude-progress.txt` - 记录代理工作进度的日志文件
- `feature_list.json` - 功能需求清单（基于用户提示扩展）
- 初始 git 仓库和第一次提交

#### 编码代理 (Coding Agent)
**职责：** 每次会话增量推进项目进度

**行为：**
- 一次只处理一个功能（增量开发）
- 会话结束时提交 git commit
- 更新进度文件
- 标记已完成的功能

---

## 4. 核心组件详细设计

### 4.1 功能清单 (feature_list.json)

**格式：** JSON

**结构：**
```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
}
```

**关键规则：**
- 初始化代理根据用户提示生成完整的功能列表（如 200+ 功能）
- 所有功能初始状态为 `passes: false`
- 编码代理只能修改 `passes` 字段，不能删除或编辑功能描述
- 使用 JSON 而非 Markdown，降低模型错误修改的可能性

### 4.2 进度日志 (claude-progress.txt)

**格式：** 纯文本

**用途：**
- 人类可读的会话摘要
- 记录每个会话完成了什么
- 配合 git 历史帮助新会话快速了解状态

**约束：** 强指令提示代理不要随意修改或删除历史记录

### 4.3 Git 版本控制

**用途：**
- 版本控制和状态恢复
- 可以回滚错误的代码更改
- 通过提交历史了解项目进展

**流程：**
- 初始化代理：创建初始仓库和第一次提交
- 编码代理：每次会话结束时提交，带描述性消息

### 4.4 环境启动脚本 (init.sh)

**用途：**
- 标准化开发环境启动
- 启动开发服务器
- 设置必要的环境变量

**优势：**
- 代理不需要每次都重新弄清楚如何运行应用
- 确保环境一致性

### 4.5 测试工具

**类型：** 浏览器自动化工具（如 Puppeteer、Playwright）

**选择：** Puppeteer
- 文章中使用的工具
- 通过 MCP 服务器集成
- 支持截图和页面交互
- 验证端到端功能

### 4.6 代理管理器 (Agent Manager)

**职责：**
- 管理初始化代理和编码代理的创建和执行
- 协调代理之间的状态传递
- 处理代理的生命周期事件（启动、暂停、恢复、停止）

**核心类：**
```python
class AgentManager:
    def __init__(self, config: Config)
    def create_initializer(self) -> InitializerAgent
    def create_coder(self) -> CodingAgent
    def run_session(self, agent: Agent) -> SessionResult
    def pause_session(self, session_id: str)
    def resume_session(self, session_id: str)
    def cancel_session(self, session_id: str)
```

### 4.7 功能清单管理器 (Feature List Manager)

**职责：**
- 加载和解析 feature_list.json
- 查询未完成的功能
- 更新功能状态
- 验证功能清单的完整性

**核心类：**
```python
class FeatureListManager:
    def load(self, path: str) -> List[Feature]
    def get_pending(self) -> List[Feature]
    def get_feature(self, id: str) -> Optional[Feature]
    def update_status(self, id: str, passes: bool)
    def validate(self) -> bool
```

### 4.8 Git 集成器 (Git Integrator)

**职责：**
- 初始化 git 仓库
- 创建提交
- 查看提交历史
- 回滚到指定提交

**核心类：**
```python
class GitIntegrator:
    def __init__(self, repo_path: str)
    def init_repo(self)
    def commit(self, message: str, files: List[str])
    def get_log(self, limit: int = 20) -> List[CommitInfo]
    def rollback(self, commit_hash: str)
    def get_current_state(self) -> str
```

### 4.9 测试执行器 (Test Executor)

**职责：**
- 执行端到端测试
- 使用 Puppeteer 进行浏览器自动化
- 截图和验证功能
- 返回测试结果

**核心类：**
```python
class TestExecutor:
    def __init__(self, browser_config: BrowserConfig)
    def setup_browser(self)
    def run_test(self, test: Feature) -> TestResult
    def take_screenshot(self, path: str)
    def teardown_browser(self)
    def run_basic_verification(self) -> bool
```

---

## 5. 会话工作流程

### 5.1 编码代理标准流程

每次会话遵循以下步骤：

```
1. pwd → 了解工作目录
2. read claude-progress.txt → 了解近期工作
3. read feature_list.json → 选择下一个功能
4. git log --oneline -20 → 查看提交历史
5. run init.sh → 启动开发服务器
6. 端到端测试基础功能 → 确保环境正常
7. 实现一个新功能
8. git commit → 提交更改
9. update claude-progress.txt → 更新进度
10. update feature_list.json → 标记功能状态
```

### 5.2 典型会话示例

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.
<Starts work on a new feature>
```

---

## 6. CLI 接口设计

### 6.1 主要命令

```bash
# 初始化新项目
long-agents init <project-name> --prompt "描述项目需求"

# 启动初始化代理
long-agents initializer run

# 启动编码代理
long-agents coder run

# 查看项目状态
long-agents status

# 查看功能清单
long-agents features list
long-agents features show <id>

# 管理会话
long-agents session list
long-agents session pause <id>
long-agents session resume <id>
long-agents session cancel <id>

# Git 操作
long-agents git log
long-agents git commit --message "描述"

# 启动 Web Dashboard
long-agents dashboard
```

### 6.2 配置文件

配置文件位于 `config/long-agents.yaml`：

```yaml
# LLM 配置
llm:
  provider: anthropic  # anthropic, openai, custom
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-5-20250929
  max_tokens: 4096

# 项目配置
project:
  work_dir: ./workspace
  feature_list_path: ./feature_list.json
  progress_file: ./claude-progress.txt
  init_script: ./init.sh

# 测试配置
test:
  tool: puppeteer
  headless: true
  screenshot_dir: ./screenshots

# Git 配置
git:
  auto_commit: true
  commit_message_format: "feat: {description}"
```

---

## 7. Web Dashboard 设计

### 7.1 功能模块

| 页面 | 功能 |
|------|------|
| 仪表板 | 项目概览、进度统计、最近活动 |
| 功能列表 | 查看所有功能、筛选状态、查看详情 |
| 会话管理 | 查看运行中的会话、暂停/恢复/取消 |
| Git 历史 | 查看提交记录、代码差异 |
| 日志查看 | 实时查看代理运行日志 |
| 配置 | 管理项目配置、API 密钥 |

### 7.2 技术栈

- **后端：** FastAPI (Python)
- **前端：** 简单的 HTML + JavaScript (或可选框架如 Vue/React)
- **实时更新：** WebSocket
- **样式：** Tailwind CSS (可选)

### 7.3 API 设计

```python
# RESTful API
GET  /api/status          # 获取项目状态
GET  /api/features        # 获取功能列表
GET  /api/features/{id}    # 获取单个功能详情
POST /api/features/{id}/status  # 更新功能状态

GET  /api/sessions        # 获取会话列表
POST /api/sessions/{id}/pause   # 暂停会话
POST /api/sessions/{id}/resume  # 恢复会话
POST /api/sessions/{id}/cancel  # 取消会话

GET  /api/git/log        # 获取 Git 日志
GET  /api/git/diff/{hash}    # 获取提交差异

# WebSocket
WS   /api/logs            # 实时日志流
```

---

## 8. 数据流设计

### 8.1 初始化流程

```
用户输入项目提示
    ↓
CLI 解析命令
    ↓
AgentManager 创建 InitializerAgent
    ↓
InitializerAgent:
    1. 分析项目需求
    2. 生成功能清单 (feature_list.json)
    3. 创建 init.sh 脚本
    4. 初始化 git 仓库
    5. 创建初始提交
    6. 创建 claude-progress.txt
    ↓
完成，返回项目路径
```

### 8.2 编码会话流程

```
用户启动编码会话
    ↓
AgentManager 创建 CodingAgent
    ↓
CodingAgent 标准流程:
    1. pwd → 获取工作目录
    2. read claude-progress.txt → 了解进度
    3. read feature_list.json → 选择功能
    4. git log → 查看历史
    5. run init.sh → 启动环境
    6. TestExecutor.run_basic_verification() → 验证基础功能
    7. 实现新功能
    8. TestExecutor.run_test() → 测试新功能
    9. GitIntegrator.commit() → 提交更改
    10. 更新 claude-progress.txt
    11. 更新 feature_list.json (passes=true)
    ↓
会话完成，返回结果
```

### 8.3 错误处理策略

| 错误类型 | 处理策略 |
|---------|---------|
| LLM API 调用失败 | 重试 3 次，指数退避，然后报告错误 |
| 功能清单损坏 | 验证并提示用户，使用备用副本 |
| Git 操作失败 | 检查 git 状态，提示用户解决冲突 |
| 测试失败 | 记录失败，截图，不标记为完成 |
| 环境启动失败 | 检查 init.sh，提供详细错误信息 |
| 会话中断 | 保存当前状态，允许恢复 |

---

## 9. 失败模式与解决方案

| 问题 | 初始化代理行为 | 编码代理行为 |
|------|---------------|-------------|
| Claude 过早宣布项目完成 | 设置功能清单文件：根据输入规范，设置包含端到端功能描述的结构化 JSON 文件 | 在会话开始时阅读功能清单文件。选择一个功能开始工作 |
| Claude 留下有错误或未记录进度的环境 | 编写初始 git 仓库和进度记录文件 | 在会话开始时阅读进度记录文件和 git 提交日志，并在开发服务器上运行基本测试以捕获任何未记录的错误。在会话结束时编写 git 提交和进度更新 |
| Claude 过早将功能标记为完成 | 设置功能清单文件 | 自我验证所有功能。仅在仔细测试后将功能标记为"通过" |
| Claude 必须花时间弄清楚如何运行应用 | 编写一个可以运行开发服务器的 `init.sh` 脚本 | 在会话开始时阅读 `init.sh` |

---

## 10. 未决问题 / 待确认

（根据讨论持续更新）

---

## 11. 更新日志

| 时间 | 更新内容 |
|------|---------|
| 2025-02-14 07:45 | 初始设计文档创建 - 确认项目目的、应用场景、技术栈、核心特性 |
| 2025-02-14 07:50 | 添加架构选择和双代理架构设计 |
| 2025-02-14 07:55 | 添加核心组件详细设计（功能清单、进度日志、Git、init.sh、测试工具） |
| 2025-02-14 08:00 | 添加会话工作流程和典型会话示例 |
| 2025-02-14 08:05 | 添加失败模式与解决方案表格 |
| 2025-02-14 08:10 | 确认 LLM 后端为多模型支持 |
| 2025-02-14 08:15 | 确认用户界面为 CLI + 可选 Web |
| 2025-02-14 08:20 | 确认目录结构为标准 Python 项目结构 |
| 2025-02-14 08:25 | 确认核心功能模块：代理管理、功能清单管理、Git 集成、测试执行 |
| 2025-02-14 08:30 | 确认测试工具为 Puppeteer |
| 2025-02-14 08:35 | 添加核心模块详细设计（代理管理器、功能清单管理器、Git 集成器、测试执行器） |
| 2025-02-14 08:40 | 添加 CLI 接口设计和 Web Dashboard 设计 |
| 2025-02-14 08:45 | 添加数据流设计和错误处理策略 |
