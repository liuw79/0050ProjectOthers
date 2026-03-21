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
