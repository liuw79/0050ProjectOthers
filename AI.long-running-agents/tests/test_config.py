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
    with pytest.raises(TypeError):
        Config(llm={})
