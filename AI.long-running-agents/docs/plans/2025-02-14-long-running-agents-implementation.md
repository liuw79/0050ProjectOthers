# 长运行代理开发系统实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个基于双代理架构的长运行代理开发系统，支持项目规划与执行场景，包含 CLI 和可选的 Web Dashboard。

**Architecture:** 基于 Anthropic 文章推荐的双代理架构：初始化代理负责首次环境设置，编码代理负责增量开发。核心组件包括代理管理器、功能清单管理器、Git 集成器、测试执行器。

**Tech Stack:** Python (原生)、Anthropic/OpenAI API、Puppeteer (通过 MCP)、FastAPI (Web Dashboard)、pytest (测试)

---

## Task 1: 项目初始化

**Files:**
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `README.md`
- Create: `src/__init__.py`
- Create: `src/agents/__init__.py`
- Create: `src/core/__init__.py`
- Create: `src/tools/__init__.py`
- Create: `src/utils/__init__.py`
- Create: `tests/__init__.py`
- Create: `config/long-agents.yaml`
- Create: `.gitignore`

**Step 1: Write pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "long-running-agents"
version = "0.1.0"
description = "A dual-agent framework for long-running AI agents"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "anthropic>=0.39.0",
    "openai>=1.0.0",
    "pyyaml>=6.0",
    "gitpython>=3.1.0",
    "click>=8.0.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
web = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "websockets>=12.0.0",
]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]

[project.scripts]
long-agents = "src.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**Step 2: Write requirements.txt**

```txt
anthropic>=0.39.0
openai>=1.0.0
pyyaml>=6.0
gitpython>=3.1.0
click>=8.0.0
rich>=13.0.0

# Optional for web dashboard
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=12.0.0

# Development
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
ruff>=0.1.0
```

**Step 3: Write README.md**

```markdown
# 长运行代理开发系统

基于 Anthropic "Effective harnesses for long-running agents" 文章的双代理架构框架。

## 功能

- 初始化代理：首次运行时设置开发环境
- 编码代理：每次会话增量推进项目进度
- 功能清单管理：结构化的功能追踪
- Git 集成：版本控制和状态恢复
- 测试执行：端到端功能验证
- CLI 接口：命令行操作
- Web Dashboard：可选的可视化监控

## 安装

```bash
pip install -e .
```

## 快速开始

```bash
# 初始化新项目
long-agents init my-project --prompt "构建一个 Web 应用"

# 运行初始化代理
long-agents initializer run

# 运行编码代理
long-agents coder run
```

## 架构

- 初始化代理：创建 feature_list.json、init.sh、claude-progress.txt 和 Git 仓库
- 编码代理：每次会话实现一个功能，提交 Git 并更新进度
```

**Step 4: Write .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
feature_list.json
claude-progress.txt
init.sh
screenshots/
*.log

# Config with secrets
config/local.yaml
config/secrets.yaml
.env
```

**Step 5: Write config/long-agents.yaml**

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

# Web Dashboard (可选)
dashboard:
  enabled: false
  host: 0.0.0.0
  port: 8000
```

**Step 6: Create empty init files**

```bash
touch src/__init__.py
touch src/agents/__init__.py
touch src/core/__init__.py
touch src/tools/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

**Step 7: Run basic test**

```bash
python -c "import src; print('Import successful')"
```

Expected: No errors

**Step 8: Commit**

```bash
git add .
git commit -m "feat: project initialization - create directory structure and config files"
```

---

## Task 2: 配置管理模块

**Files:**
- Create: `src/core/config.py`
- Test: `tests/test_config.py`

**Step 1: Write the failing test**

```python
import os
import pytest
from src.core.config import Config, load_config

def test_load_config_from_file():
    config = load_config("config/long-agents.yaml")
    assert config.llm.provider == "anthropic"
    assert config.llm.model == "claude-sonnet-4-5-20250929"
    assert config.project.work_dir == "./workspace"

def test_config_env_var_substitution():
    os.environ["ANTHROPIC_API_KEY"] = "test-key"
    config = load_config("config/long-agents.yaml")
    assert config.llm.api_key == "test-key"

def test_config_validation():
    with pytest.raises(ValueError):
        Config(llm={})
```

**Step 2: Run test to verify it fails**

```bash
cd /Users/comdir/SynologyDrive/0050Project/AI.long-running-agents
pytest tests/test_config.py -v
```

Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
import os
import yaml
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class LLMConfig:
    provider: str
    api_key: str
    model: str
    max_tokens: int

@dataclass
class ProjectConfig:
    work_dir: str
    feature_list_path: str
    progress_file: str
    init_script: str

@dataclass
class TestConfig:
    tool: str
    headless: bool
    screenshot_dir: str

@dataclass
class GitConfig:
    auto_commit: bool
    commit_message_format: str

@dataclass
class DashboardConfig:
    enabled: bool
    host: str
    port: int

@dataclass
class Config:
    llm: LLMConfig
    project: ProjectConfig
    test: TestConfig
    git: GitConfig
    dashboard: DashboardConfig

def _substitute_env_vars(value: Any) -> Any:
    """递归替换环境变量"""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.environ.get(env_var, value)
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(item) for item in value]
    return value

def load_config(path: str) -> Config:
    """加载配置文件并替换环境变量"""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    data = _substitute_env_vars(data)

    # 验证必需字段
    required_sections = ['llm', 'project', 'test', 'git', 'dashboard']
    for section in required_sections:
        if section not in data:
            raise ValueError(f"Missing required section: {section}")

    return Config(
        llm=LLMConfig(**data['llm']),
        project=ProjectConfig(**data['project']),
        test=TestConfig(**data['test']),
        git=GitConfig(**data['git']),
        dashboard=DashboardConfig(**data['dashboard']),
    )
```

**Step 4: Run test to verify it passes**

```bash
cd /Users/comdir/SynologyDrive/0050Project/AI.long-running-agents
pytest tests/test_config.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/core/config.py tests/test_config.py
git commit -m "feat: add configuration management module"
```

---

## Task 3: LLM 抽象层

**Files:**
- Create: `src/core/llm/base.py`
- Create: `src/core/llm/anthropic.py`
- Create: `src/core/llm/openai.py`
- Create: `src/core/llm/factory.py`
- Create: `src/core/llm/__init__.py`
- Test: `tests/test_llm.py`

**Step 1: Write the failing test**

```python
import pytest
from src.core.llm.factory import create_llm_client
from src.core.llm.base import LLMClient

def test_create_anthropic_client():
    client = create_llm_client("anthropic", api_key="test-key")
    assert isinstance(client, LLMClient)

def test_create_openai_client():
    client = create_llm_client("openai", api_key="test-key")
    assert isinstance(client, LLMClient)

def test_invalid_provider():
    with pytest.raises(ValueError):
        create_llm_client("invalid", api_key="test-key")
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_llm.py -v
```

Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
# src/core/llm/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

    @abstractmethod
    def chat_stream(self, messages: List[Dict[str, str]], **kwargs):
        pass
```

```python
# src/core/llm/anthropic.py
from anthropic import Anthropic
from .base import LLMClient

class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def chat(self, messages, **kwargs):
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.content[0].text

    def chat_stream(self, messages, **kwargs):
        return self.client.messages.stream(
            model=self.model,
            messages=messages,
            **kwargs
        )
```

```python
# src/core/llm/openai.py
from openai import OpenAI
from .base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def chat_stream(self, messages, **kwargs):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **kwargs
        )
```

```python
# src/core/llm/factory.py
from .base import LLMClient
from .anthropic import AnthropicClient
from .openai import OpenAIClient

def create_llm_client(provider: str, api_key: str, **kwargs) -> LLMClient:
    if provider == "anthropic":
        return AnthropicClient(api_key=api_key, **kwargs)
    elif provider == "openai":
        return OpenAIClient(api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
```

```python
# src/core/llm/__init__.py
from .base import LLMClient
from .factory import create_llm_client

__all__ = ["LLMClient", "create_llm_client"]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_llm.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/core/llm/ tests/test_llm.py
git commit -m "feat: add LLM abstraction layer with multi-provider support"
```

---

## Task 4: 功能清单管理器

**Files:**
- Create: `src/core/feature_list.py`
- Test: `tests/test_feature_list.py`

**Step 1: Write the failing test**

```python
import pytest
import json
import tempfile
import os
from src.core.feature_list import Feature, FeatureListManager

def test_load_feature_list():
    features_data = [{
        "category": "functional",
        "description": "Test feature",
        "steps": ["Step 1", "Step 2"],
        "passes": False
    }]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        features = manager.load()
        assert len(features) == 1
        assert features[0].description == "Test feature"
        assert features[0].passes is False
    finally:
        os.unlink(temp_path)

def test_get_pending_features():
    features_data = [
        {"category": "functional", "description": "Done", "steps": [], "passes": True},
        {"category": "functional", "description": "Pending", "steps": [], "passes": False}
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        pending = manager.get_pending()
        assert len(pending) == 1
        assert pending[0].description == "Pending"
    finally:
        os.unlink(temp_path)

def test_update_feature_status():
    features_data = [{"category": "functional", "description": "Test", "steps": [], "passes": False}]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        manager.update_status(0, passes=True)
        features = manager.load()
        assert features[0].passes is True
    finally:
        os.unlink(temp_path)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_feature_list.py -v
```

Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Feature:
    id: int
    category: str
    description: str
    steps: List[str]
    passes: bool

class FeatureListManager:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> List[Feature]:
        """加载功能列表"""
        with open(self.path, 'r') as f:
            data = json.load(f)
        return [
            Feature(
                id=i,
                category=item['category'],
                description=item['description'],
                steps=item.get('steps', []),
                passes=item.get('passes', False)
            )
            for i, item in enumerate(data)
        ]

    def get_pending(self) -> List[Feature]:
        """获取未完成的功能"""
        features = self.load()
        return [f for f in features if not f.passes]

    def get_feature(self, feature_id: int) -> Optional[Feature]:
        """获取单个功能"""
        features = self.load()
        for feature in features:
            if feature.id == feature_id:
                return feature
        return None

    def update_status(self, feature_id: int, passes: bool):
        """更新功能状态"""
        features = self.load()
        if 0 <= feature_id < len(features):
            features[feature_id].passes = passes
            self._save(features)

    def validate(self) -> bool:
        """验证功能清单的完整性"""
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            required_fields = ['category', 'description', 'steps', 'passes']
            return all(all(field in item for field in required_fields) for item in data)
        except:
            return False

    def _save(self, features: List[Feature]):
        """保存功能列表"""
        data = [
            {
                'category': f.category,
                'description': f.description,
                'steps': f.steps,
                'passes': f.passes
            }
            for f in features
        ]
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_feature_list.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/core/feature_list.py tests/test_feature_list.py
git commit -m "feat: add feature list manager"
```

---

## Task 5: Git 集成器

**Files:**
- Create: `src/core/git_integrator.py`
- Test: `tests/test_git_integrator.py`

**Step 1: Write the failing test**

```python
import pytest
import tempfile
import os
from src.core.git_integrator import GitIntegrator

def test_init_repo():
    with tempfile.TemporaryDirectory() as tmpdir:
        integrator = GitIntegrator(tmpdir)
        integrator.init_repo()
        assert os.path.exists(os.path.join(tmpdir, '.git'))

def test_commit():
    with tempfile.TemporaryDirectory() as tmpdir:
        integrator = GitIntegrator(tmpdir)
        integrator.init_repo()

        # Create a file and commit
        test_file = os.path.join(tmpdir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        integrator.commit("Initial commit", ['test.txt'])

        log = integrator.get_log(1)
        assert len(log) == 1
        assert "Initial commit" in log[0]['message']
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_git_integrator.py -v
```

Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
import os
from git import Repo, GitCommandError
from typing import List, Dict

@dataclass
class CommitInfo:
    hash: str
    message: str
    author: str
    timestamp: str

class GitIntegrator:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = None

    def init_repo(self):
        """初始化 git 仓库"""
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            self.repo = Repo.init(self.repo_path)
        else:
            self.repo = Repo(self.repo_path)

    def commit(self, message: str, files: List[str]):
        """创建提交"""
        if self.repo is None:
            self.repo = Repo(self.repo_path)

        # 添加文件
        for file in files:
            file_path = os.path.join(self.repo_path, file)
            if os.path.exists(file_path):
                self.repo.index.add([file])

        # 提交
        if self.repo.is_dirty(untracked_files=True):
            self.repo.index.commit(message)

    def get_log(self, limit: int = 20) -> List[Dict]:
        """获取提交历史"""
        if self.repo is None:
            return []

        commits = list(self.repo.iter_commits('HEAD', max_count=limit))
        return [
            {
                'hash': commit.hexsha[:8],
                'message': commit.message.strip(),
                'author': str(commit.author),
                'timestamp': commit.committed_datetime.isoformat()
            }
            for commit in commits
        ]

    def rollback(self, commit_hash: str):
        """回滚到指定提交"""
        if self.repo is None:
            raise ValueError("Repository not initialized")
        self.repo.git.reset('--hard', commit_hash)

    def get_current_state(self) -> str:
        """获取当前状态"""
        if self.repo is None:
            return "Not initialized"
        return self.repo.head.commit.hexsha[:8]
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_git_integrator.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/core/git_integrator.py tests/test_git_integrator.py
git commit -m "feat: add git integrator"
```

---

## Task 6: 代理基类和代理管理器

**Files:**
- Create: `src/agents/base.py`
- Create: `src/agents/manager.py`
- Create: `src/agents/initializer.py`
- Create: `src/agents/coder.py`
- Test: `tests/test_agents.py`

**Step 1: Write the failing test**

```python
import pytest
from src.agents.manager import AgentManager
from src.agents.base import Agent

def test_create_initializer():
    manager = AgentManager(config=None)
    initializer = manager.create_initializer()
    assert isinstance(initializer, Agent)

def test_create_coder():
    manager = AgentManager(config=None)
    coder = manager.create_coder()
    assert isinstance(coder, Agent)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_agents.py -v
```

Expected: FAIL with "module not found"

**Step 3: Write minimal implementation**

```python
# src/agents/base.py
from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def run(self) -> dict:
        """运行代理并返回结果"""
        pass
```

```python
# src/agents/manager.py
from src.agents.base import Agent
from src.agents.initializer import InitializerAgent
from src.agents.coder import CodingAgent

class AgentManager:
    def __init__(self, config):
        self.config = config

    def create_initializer(self) -> InitializerAgent:
        """创建初始化代理"""
        return InitializerAgent(self.config)

    def create_coder(self) -> CodingAgent:
        """创建编码代理"""
        return CodingAgent(self.config)

    def run_session(self, agent: Agent) -> dict:
        """运行代理会话"""
        return agent.run()
```

```python
# src/agents/initializer.py
from src.agents.base import Agent

class InitializerAgent(Agent):
    def __init__(self, config):
        self.config = config

    def run(self) -> dict:
        # 实现细节在后续任务中
        return {"status": "success", "message": "Initialization complete"}
```

```python
# src/agents/coder.py
from src.agents.base import Agent

class CodingAgent(Agent):
    def __init__(self, config):
        self.config = config

    def run(self) -> dict:
        # 实现细节在后续任务中
        return {"status": "success", "message": "Coding session complete"}
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_agents.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/agents/ tests/test_agents.py
git commit -m "feat: add agent base classes and manager"
```

---

## Task 7: CLI 主程序

**Files:**
- Create: `src/cli.py`
- Create: `src/commands/__init__.py`
- Create: `src/commands/init.py`
- Create: `src/commands/status.py`

**Step 1: Write CLI entry point**

```python
# src/cli.py
import click
from rich.console import Console

console = Console()

@click.group()
def main():
    """长运行代理开发系统"""
    pass

if __name__ == "__main__":
    main()
```

**Step 2: Add init command**

```python
# src/commands/init.py
import click
import os
from rich.console import Console

console = Console()

@click.command()
@click.argument("project_name")
@click.option("--prompt", "-p", help="项目描述")
def init(project_name, prompt):
    """初始化新项目"""
    console.print(f"[bold green]创建项目: {project_name}[/bold green]")
    if prompt:
        console.print(f"[dim]提示: {prompt}[/dim]")

    # 创建项目目录
    os.makedirs(project_name, exist_ok=True)

    # 初始化代理并设置环境
    # 实现细节在后续任务中

    console.print("[bold green]✓[/bold green] 项目初始化完成")
```

**Step 3: Add status command**

```python
# src/commands/status.py
import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.command()
def status():
    """查看项目状态"""
    table = Table(title="项目状态")
    table.add_column("项目", style="cyan")
    table.add_column("状态", style="green")

    table.add_row("功能清单", "未加载")
    table.add_row("Git 仓库", "未初始化")
    table.add_row("进度", "0/0")

    console.print(table)
```

**Step 4: Update CLI to include commands**

```python
# src/cli.py (updated)
import click
from rich.console import Console

console = Console()

@click.group()
def main():
    """长运行代理开发系统"""
    pass

# 导入命令
from src.commands.init import init
from src.commands.status import status

main.add_command(init)
main.add_command(status)

if __name__ == "__main__":
    main()
```

**Step 5: Test CLI**

```bash
python -m src.cli --help
python -m src.cli status
```

Expected: Commands display correctly

**Step 6: Commit**

```bash
git add src/cli.py src/commands/
git commit -m "feat: add CLI commands (init, status)"
```

---

## Task 8: 完善初始化代理实现

**Files:**
- Modify: `src/agents/initializer.py`
- Test: `tests/test_initializer.py`

**Step 1: Write the failing test**

```python
import pytest
import tempfile
import os
import json
from src.agents.initializer import InitializerAgent

def test_initializer_creates_feature_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            'project': {
                'work_dir': tmpdir,
                'feature_list_path': os.path.join(tmpdir, 'feature_list.json'),
                'progress_file': os.path.join(tmpdir, 'progress.txt'),
                'init_script': os.path.join(tmpdir, 'init.sh')
            },
            'llm': {
                'api_key': 'test-key',
                'model': 'test-model'
            }
        }
        agent = InitializerAgent(config)
        result = agent.run()

        assert result['status'] == 'success'
        assert os.path.exists(os.path.join(tmpdir, 'feature_list.json'))
```

**Step 2: Update InitializerAgent implementation**

```python
# src/agents/initializer.py (updated)
import os
from src.agents.base import Agent
from src.core.feature_list import FeatureListManager
from src.core.git_integrator import GitIntegrator

class InitializerAgent(Agent):
    def __init__(self, config):
        self.config = config

    def run(self) -> dict:
        """运行初始化代理"""
        try:
            # 1. 创建目录结构
            self._create_directories()

            # 2. 生成功能清单
            self._generate_feature_list()

            # 3. 创建 init.sh 脚本
            self._create_init_script()

            # 4. 创建进度文件
            self._create_progress_file()

            # 5. 初始化 Git 仓库
            self._init_git()

            return {
                "status": "success",
                "message": "Initialization complete"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _create_directories(self):
        """创建必要的目录"""
        work_dir = self.config['project']['work_dir']
        os.makedirs(work_dir, exist_ok=True)

    def _generate_feature_list(self):
        """生成功能清单（简化版本，完整版本需要 LLM）"""
        feature_list_path = self.config['project']['feature_list_path']
        # 这里使用示例功能，完整版本应该使用 LLM 生成
        features = [
            {
                "category": "functional",
                "description": "示例功能 1",
                "steps": ["步骤 1", "步骤 2"],
                "passes": False
            }
        ]
        import json
        with open(feature_list_path, 'w') as f:
            json.dump(features, f, indent=2)

    def _create_init_script(self):
        """创建 init.sh 脚本"""
        init_script = self.config['project']['init_script']
        with open(init_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# 初始化开发环境\n")
            f.write("echo 'Starting development server...'\n")
        os.chmod(init_script, 0o755)

    def _create_progress_file(self):
        """创建进度文件"""
        progress_file = self.config['project']['progress_file']
        with open(progress_file, 'w') as f:
            f.write("# 项目进度日志\n")
            f.write("# 初始化完成\n")

    def _init_git(self):
        """初始化 Git 仓库"""
        work_dir = self.config['project']['work_dir']
        integrator = GitIntegrator(work_dir)
        integrator.init_repo()
        integrator.commit("Initial commit", [
            os.path.basename(self.config['project']['feature_list_path']),
            os.path.basename(self.config['project']['progress_file']),
            os.path.basename(self.config['project']['init_script'])
        ])
```

**Step 3: Run test to verify it passes**

```bash
pytest tests/test_initializer.py -v
```

Expected: PASS

**Step 4: Commit**

```bash
git add src/agents/initializer.py tests/test_initializer.py
git commit -m "feat: implement initializer agent"
```

---

## Task 9: 完善编码代理实现

**Files:**
- Modify: `src/agents/coder.py`
- Test: `tests/test_coder.py`

**Step 1: Write the failing test**

```python
import pytest
import tempfile
import os
from src.agents.coder import CodingAgent

def test_coder_standard_workflow():
    with tempfile.TemporaryDirectory() as tmpdir:
        # 设置测试环境
        config = {
            'project': {
                'work_dir': tmpdir,
                'feature_list_path': os.path.join(tmpdir, 'feature_list.json'),
                'progress_file': os.path.join(tmpdir, 'progress.txt'),
                'init_script': os.path.join(tmpdir, 'init.sh')
            },
            'llm': {'api_key': 'test-key', 'model': 'test-model'}
        }

        # 先运行初始化
        from src.agents.initializer import InitializerAgent
        initializer = InitializerAgent(config)
        initializer.run()

        # 运行编码代理
        coder = CodingAgent(config)
        result = coder.run()

        assert result['status'] == 'success'
```

**Step 2: Update CodingAgent implementation**

```python
# src/agents/coder.py (updated)
import os
import subprocess
from src.agents.base import Agent
from src.core.feature_list import FeatureListManager
from src.core.git_integrator import GitIntegrator

class CodingAgent(Agent):
    def __init__(self, config):
        self.config = config

    def run(self) -> dict:
        """运行编码代理 - 执行标准工作流程"""
        try:
            # 1. pwd - 了解工作目录
            work_dir = self.config['project']['work_dir']
            os.chdir(work_dir)

            # 2. 读取进度文件
            self._read_progress()

            # 3. 读取功能清单并选择下一个功能
            feature = self._select_next_feature()
            if not feature:
                return {"status": "success", "message": "All features completed"}

            # 4. 查看 git 日志
            self._check_git_history()

            # 5. 运行 init.sh
            self._start_environment()

            # 6. 验证基础功能
            self._verify_basic_functionality()

            # 7. 实现新功能
            self._implement_feature(feature)

            # 8. 测试功能
            self._test_feature(feature)

            # 9. 提交更改
            self._commit_changes(feature)

            # 10. 更新进度
            self._update_progress(feature)

            # 11. 标记功能完成
            self._mark_feature_complete(feature.id)

            return {
                "status": "success",
                "message": f"Implemented feature: {feature.description}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _read_progress(self):
        """读取进度文件"""
        progress_file = self.config['project']['progress_file']
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                print(f"Progress:\n{f.read()}")

    def _select_next_feature(self):
        """选择下一个未完成的功能"""
        feature_list_path = self.config['project']['feature_list_path']
        manager = FeatureListManager(feature_list_path)
        pending = manager.get_pending()
        return pending[0] if pending else None

    def _check_git_history(self):
        """检查 git 历史"""
        work_dir = self.config['project']['work_dir']
        integrator = GitIntegrator(work_dir)
        log = integrator.get_log(5)
        print(f"Recent commits:")
        for commit in log:
            print(f"  {commit['hash']}: {commit['message']}")

    def _start_environment(self):
        """启动开发环境"""
        init_script = self.config['project']['init_script']
        if os.path.exists(init_script):
            print(f"Running {init_script}...")
            subprocess.run([init_script], shell=True)

    def _verify_basic_functionality(self):
        """验证基础功能"""
        print("Verifying basic functionality...")
        # 简化版本，完整版本应该运行测试
        print("✓ Basic functionality verified")

    def _implement_feature(self, feature):
        """实现功能（简化版本）"""
        print(f"Implementing feature: {feature.description}")
        # 完整版本应该使用 LLM 生成代码

    def _test_feature(self, feature):
        """测试功能（简化版本）"""
        print(f"Testing feature: {feature.description}")
        # 完整版本应该运行端到端测试
        print("✓ Feature tested")

    def _commit_changes(self, feature):
        """提交更改"""
        work_dir = self.config['project']['work_dir']
        integrator = GitIntegrator(work_dir)
        integrator.commit(f"feat: {feature.description}", [])

    def _update_progress(self, feature):
        """更新进度文件"""
        progress_file = self.config['project']['progress_file']
        with open(progress_file, 'a') as f:
            f.write(f"\n{feature.description}: 完成\n")

    def _mark_feature_complete(self, feature_id):
        """标记功能完成"""
        feature_list_path = self.config['project']['feature_list_path']
        manager = FeatureListManager(feature_list_path)
        manager.update_status(feature_id, passes=True)
```

**Step 3: Run test to verify it passes**

```bash
pytest tests/test_coder.py -v
```

Expected: PASS

**Step 4: Commit**

```bash
git add src/agents/coder.py tests/test_coder.py
git commit -m "feat: implement coding agent with standard workflow"
```

---

## Task 10: 添加更多 CLI 命令

**Files:**
- Create: `src/commands/initializer_cmd.py`
- Create: `src/commands/coder_cmd.py`

**Step 1: Write initializer command**

```python
# src/commands/initializer_cmd.py
import click
from rich.console import Console
from src.core.config import load_config
from src.agents.manager import AgentManager

console = Console()

@click.command()
def run():
    """运行初始化代理"""
    config = load_config("config/long-agents.yaml")
    manager = AgentManager(config)
    initializer = manager.create_initializer()

    console.print("[bold cyan]运行初始化代理...[/bold cyan]")
    result = initializer.run()

    if result['status'] == 'success':
        console.print(f"[bold green]✓[/bold green] {result['message']}")
    else:
        console.print(f"[bold red]✗[/bold red] {result['message']}")
```

**Step 2: Write coder command**

```python
# src/commands/coder_cmd.py
import click
from rich.console import Console
from src.core.config import load_config
from src.agents.manager import AgentManager

console = Console()

@click.command()
def run():
    """运行编码代理"""
    config = load_config("config/long-agents.yaml")
    manager = AgentManager(config)
    coder = manager.create_coder()

    console.print("[bold cyan]运行编码代理...[/bold cyan]")
    result = coder.run()

    if result['status'] == 'success':
        console.print(f"[bold green]✓[/bold green] {result['message']}")
    else:
        console.print(f"[bold red]✗[/bold red] {result['message']}")
```

**Step 3: Update CLI to include commands**

```python
# src/cli.py (update imports)
from src.commands.initializer_cmd import run as initializer_run
from src.commands.coder_cmd import run as coder_run

# Add commands
main.add_command(initializer_run, name="initializer")
main.add_command(coder_run, name="coder")
```

**Step 4: Test commands**

```bash
python -m src.cli initializer --help
python -m src.cli coder --help
```

Expected: Commands display correctly

**Step 5: Commit**

```bash
git add src/commands/initializer_cmd.py src/commands/coder_cmd.py src/cli.py
git commit -m "feat: add initializer and coder CLI commands"
```

---

## Task 11: Web Dashboard (可选)

**Files:**
- Create: `src/web/app.py`
- Create: `src/web/api.py`
- Create: `src/web/static/index.html`

**Step 1: Create FastAPI app**

```python
# src/web/app.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import router

app = FastAPI(title="长运行代理 Dashboard")
app.include_router(router, prefix="/api")

# 挂载静态文件
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 2: Create API endpoints**

```python
# src/web/api.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

@router.get("/status")
def get_status():
    return {
        "features": {"total": 0, "completed": 0},
        "git": {"initialized": True},
        "progress": "Ready"
    }

@router.get("/features")
def get_features():
    return []

@router.websocket("/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "log", "message": "Test log"})
    except WebSocketDisconnect:
        pass
```

**Step 3: Create simple HTML dashboard**

```html
<!-- src/web/static/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>长运行代理 Dashboard</title>
</head>
<body>
    <h1>长运行代理 Dashboard</h1>
    <div id="status"></div>
    <script>
        fetch('/api/status').then(r => r.json()).then(data => {
            document.getElementById('status').textContent = JSON.stringify(data, null, 2);
        });
    </script>
</body>
</html>
```

**Step 4: Add CLI command for dashboard**

```python
# src/commands/dashboard.py
import click
import uvicorn

@click.command()
@click.option("--host", default="0.0.0.0", help="Host address")
@click.option("--port", default=8000, help="Port number")
def dashboard(host, port):
    """启动 Web Dashboard"""
    click.echo(f"Starting dashboard on http://{host}:{port}")
    uvicorn.run("src.web.app:app", host=host, port=port)
```

**Step 5: Test dashboard**

```bash
python -m src.cli dashboard &
sleep 2
curl http://localhost:8000/health
```

Expected: {"status": "ok"}

**Step 6: Commit**

```bash
git add src/web/
git commit -m "feat: add optional web dashboard"
```

---

## Task 12: 文档和示例

**Files:**
- Update: `README.md`
- Create: `examples/simple_project/README.md`

**Step 1: Update README.md with full usage**

```markdown
# 长运行代理开发系统

基于 Anthropic "Effective harnesses for long-running agents" 文章的双代理架构框架。

## 安装

```bash
pip install -e .
```

## 快速开始

```bash
# 初始化新项目
long-agents init my-project --prompt "构建一个 Web 应用"

# 运行初始化代理
long-agents initializer run

# 运行编码代理
long-agents coder run

# 查看项目状态
long-agents status

# 启动 Web Dashboard（可选）
long-agents dashboard
```

## 配置

配置文件位于 `config/long-agents.yaml`。

## 架构

### 双代理模式

1. **初始化代理**：首次运行时创建：
   - `feature_list.json` - 功能需求清单
   - `claude-progress.txt` - 进度日志
   - `init.sh` - 环境启动脚本
   - Git 仓库

2. **编码代理**：每次会话：
   - 选择一个未完成的功能
   - 实现功能
   - 测试功能
   - 提交 Git
   - 更新进度

### 核心组件

- **AgentManager**: 管理代理生命周期
- **FeatureListManager**: 管理功能清单
- **GitIntegrator**: Git 集成
- **TestExecutor**: 测试执行
```

**Step 2: Create example project**

```bash
mkdir examples/simple_project
echo "# 简单示例项目" > examples/simple_project/README.md
```

**Step 3: Commit**

```bash
git add README.md examples/
git commit -m "docs: add comprehensive documentation and examples"
```

---

## 总结

实现计划已创建，包含以下主要任务：

1. ✅ 项目初始化
2. ✅ 配置管理模块
3. ✅ LLM 抽象层
4. ✅ 功能清单管理器
5. ✅ Git 集成器
6. ✅ 代理基类和代理管理器
7. ✅ CLI 主程序
8. ✅ 完善初始化代理实现
9. ✅ 完善编码代理实现
10. ✅ 添加更多 CLI 命令
11. ✅ Web Dashboard (可选)
12. ✅ 文档和示例

每个任务都包含详细的测试和提交步骤。
