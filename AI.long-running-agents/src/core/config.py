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
