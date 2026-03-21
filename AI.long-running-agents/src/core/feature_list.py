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
