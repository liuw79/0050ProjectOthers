"""项目注册表 - 管理所有已知项目"""
import json
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


# 注册表文件位置
REGISTRY_FILE = Path.home() / ".long-agents" / "projects.json"


@dataclass
class ProjectInfo:
    name: str
    path: str
    description: str
    created_at: str
    last_accessed: str


class ProjectRegistry:
    """项目注册表"""

    def __init__(self):
        self._ensure_registry()

    def _ensure_registry(self):
        """确保注册表文件存在"""
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not REGISTRY_FILE.exists():
            self._save({"projects": {}})

    def _load(self) -> dict:
        """加载注册表"""
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)

    def _save(self, data: dict):
        """保存注册表"""
        with open(REGISTRY_FILE, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def register(self, name: str, path: str, description: str = ""):
        """注册新项目"""
        data = self._load()
        now = datetime.now().isoformat()

        data["projects"][name] = {
            "path": str(path),
            "description": description,
            "created_at": now,
            "last_accessed": now
        }
        self._save(data)

    def update_accessed(self, name: str):
        """更新最后访问时间"""
        data = self._load()
        if name in data["projects"]:
            data["projects"][name]["last_accessed"] = datetime.now().isoformat()
            self._save(data)

    def get(self, name: str) -> Optional[ProjectInfo]:
        """获取项目信息"""
        data = self._load()
        if name in data["projects"]:
            p = data["projects"][name]
            return ProjectInfo(
                name=name,
                path=p["path"],
                description=p.get("description", ""),
                created_at=p.get("created_at", ""),
                last_accessed=p.get("last_accessed", "")
            )
        return None

    def list_all(self) -> List[ProjectInfo]:
        """列出所有项目"""
        data = self._load()
        projects = []
        for name, p in data["projects"].items():
            projects.append(ProjectInfo(
                name=name,
                path=p["path"],
                description=p.get("description", ""),
                created_at=p.get("created_at", ""),
                last_accessed=p.get("last_accessed", "")
            ))
        # 按最后访问时间排序
        projects.sort(key=lambda x: x.last_accessed, reverse=True)
        return projects

    def remove(self, name: str) -> bool:
        """移除项目"""
        data = self._load()
        if name in data["projects"]:
            del data["projects"][name]
            self._save(data)
            return True
        return False

    def find_by_path(self, path: str) -> Optional[ProjectInfo]:
        """根据路径查找项目"""
        data = self._load()
        path_str = str(path)
        for name, p in data["projects"].items():
            if p["path"] == path_str:
                return self.get(name)
        return None
