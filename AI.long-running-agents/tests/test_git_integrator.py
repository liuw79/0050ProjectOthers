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
