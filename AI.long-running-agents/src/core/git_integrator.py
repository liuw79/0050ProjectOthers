import os
from git import Repo, GitCommandError
from typing import List, Dict
from dataclasses import dataclass

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
