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
