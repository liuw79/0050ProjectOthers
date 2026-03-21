#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钢琴教程进阶分类器
将"其他教材"进一步细分为更专业的分类
"""

import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

class AdvancedPianoClassifier:
    def __init__(self):
        # 教程基础路径
        self.tutorial_base_path = Path('/Volumes/video/教程')
        self.piano_zone_path = self.tutorial_base_path / '钢琴教程专区'
        self.other_materials_path = self.piano_zone_path / '📦 其他教材'
        
        # 新的细分分类
        self.advanced_categories = {
            '🎼 古典音乐': {
                'keywords': ['古典', '古典音乐', '鉴赏', '音乐鉴赏', '轻音乐'],
                'description': '古典音乐鉴赏和轻音乐'
            },
            '🎹 流行钢琴': {
                'keywords': ['流行', '好歌', '名曲', '演奏', '轻松弹', '拿手曲目'],
                'description': '流行歌曲和名曲演奏'
            },
            '🎵 演奏技巧': {
                'keywords': ['演奏技巧', '技巧', '进阶', '布格缪勒'],
                'description': '钢琴演奏技巧和进阶教程'
            },
            '🎤 编曲伴奏': {
                'keywords': ['编曲', '伴奏', '即兴'],
                'description': '编曲和即兴伴奏'
            },
            '👨‍🏫 大师课程': {
                'keywords': ['大师', '讲堂', '刘诗昆', '周铭孙', '林文信'],
                'description': '钢琴大师课程和名师教学'
            },
            '📚 教学方法': {
                'keywords': ['教学', '学钢琴', '认知', '学习法', '要领', '决窍'],
                'description': '钢琴教学方法和学习理论'
            },
            '🎹 电子琴': {
                'keywords': ['电子琴'],
                'description': '电子琴教程'
            },
            '📖 教材曲谱': {
                'keywords': ['教材', '曲谱', '一加一'],
                'description': '钢琴教材和曲谱资源'
            },
            '🎯 分级教程': {
                'keywords': ['初级', '中级', '高级', '入门'],
                'description': '按难度分级的综合教程'
            },
            '🎵 特定曲目': {
                'keywords': ['梦中的婚礼'],
                'description': '特定曲目教学'
            }
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = Path(f'logs/advanced_piano_classification_{timestamp}.log')
        log_file.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log(self, message):
        """记录日志"""
        self.logger.info(message)
        print(message)
    
    def categorize_tutorial(self, tutorial_name):
        """对教程进行细分分类"""
        tutorial_name_lower = tutorial_name.lower()
        
        # 按优先级进行分类
        for category, config in self.advanced_categories.items():
            for keyword in config['keywords']:
                if keyword in tutorial_name_lower:
                    return category, keyword
        
        # 未匹配到特定分类，保持在其他教材
        return '📦 其他教材', None
    
    def analyze_current_structure(self):
        """分析当前其他教材的结构"""
        self.log("🔍 分析当前其他教材目录结构...")
        
        if not self.other_materials_path.exists():
            self.log(f"❌ 其他教材目录不存在: {self.other_materials_path}")
            return []
        
        tutorials = []
        for item in self.other_materials_path.iterdir():
            if item.is_dir():
                category, keyword = self.categorize_tutorial(item.name)
                tutorials.append({
                    'name': item.name,
                    'path': item,
                    'suggested_category': category,
                    'keyword': keyword
                })
        
        # 统计分类建议
        category_stats = {}
        for tutorial in tutorials:
            cat = tutorial['suggested_category']
            category_stats[cat] = category_stats.get(cat, 0) + 1
        
        self.log(f"📊 发现 {len(tutorials)} 个教程，分类建议:")
        for category, count in category_stats.items():
            if category != '📦 其他教材':
                self.log(f"   {category}: {count}个")
        
        remaining_count = category_stats.get('📦 其他教材', 0)
        if remaining_count > 0:
            self.log(f"   保持在其他教材: {remaining_count}个")
        
        return tutorials
    
    def create_new_categories(self, simulate=True):
        """创建新的分类目录"""
        mode = "模拟" if simulate else "实际"
        self.log(f"🏗️ {mode}创建新分类目录...")
        
        created_categories = []
        
        for category, config in self.advanced_categories.items():
            if category == '📦 其他教材':  # 跳过原有分类
                continue
                
            category_path = self.piano_zone_path / category
            
            if not simulate:
                category_path.mkdir(exist_ok=True)
                self.log(f"✅ 创建目录: {category}")
            else:
                self.log(f"📋 计划创建: {category} - {config['description']}")
            
            created_categories.append(category)
        
        return created_categories
    
    def reclassify_tutorials(self, tutorials, simulate=True):
        """重新分类教程"""
        mode = "模拟" if simulate else "实际"
        self.log(f"🔄 {mode}重新分类教程...")
        
        moved_count = 0
        operations = []
        
        for tutorial in tutorials:
            if tutorial['suggested_category'] == '📦 其他教材':
                continue  # 保持在原位置
            
            source_path = tutorial['path']
            target_category_path = self.piano_zone_path / tutorial['suggested_category']
            target_path = target_category_path / tutorial['name']
            
            operation = {
                'action': 'move',
                'source': source_path,
                'destination': target_path,
                'category': tutorial['suggested_category'],
                'keyword': tutorial['keyword']
            }
            operations.append(operation)
            
            if not simulate:
                try:
                    # 确保目标目录存在
                    target_category_path.mkdir(exist_ok=True)
                    
                    # 移动教程
                    shutil.move(str(source_path), str(target_path))
                    match_info = f" (匹配: {tutorial['keyword']})" if tutorial['keyword'] else ""
                    self.log(f"✅ 移动: {tutorial['name']} → {tutorial['suggested_category']}{match_info}")
                    moved_count += 1
                except Exception as e:
                    self.log(f"❌ 移动失败: {tutorial['name']} - {e}")
            else:
                match_info = f" (匹配: {tutorial['keyword']})" if tutorial['keyword'] else ""
                self.log(f"📋 计划移动: {tutorial['name']} → {tutorial['suggested_category']}{match_info}")
                moved_count += 1
        
        return operations, moved_count
    
    def run(self, simulate=True):
        """运行进阶分类流程"""
        mode = "模拟运行" if simulate else "实际执行"
        self.log(f"🚀 开始钢琴教程进阶分类 - {mode}")
        
        # 分析当前结构
        tutorials = self.analyze_current_structure()
        
        if not tutorials:
            self.log("ℹ️ 其他教材目录为空或不存在")
            return
        
        # 创建新分类目录
        created_categories = self.create_new_categories(simulate)
        
        # 重新分类教程
        operations, moved_count = self.reclassify_tutorials(tutorials, simulate)
        
        # 统计信息
        category_stats = {}
        for op in operations:
            category = op['category']
            category_stats[category] = category_stats.get(category, 0) + 1
        
        remaining_count = len(tutorials) - moved_count
        
        self.log(f"\n📊 分类统计:")
        self.log(f"   总教程数: {len(tutorials)}")
        self.log(f"   重新分类: {moved_count}个")
        self.log(f"   保持原位: {remaining_count}个")
        
        if category_stats:
            self.log(f"\n📋 新分类分布:")
            for category, count in category_stats.items():
                self.log(f"   {category}: {count}个")
        
        if simulate:
            self.log("\n⚠️ 这是模拟运行，没有实际修改文件")
            self.log("如需实际执行，请运行: python3 advanced_piano_classifier.py --execute")
        else:
            self.log(f"\n🎉 进阶分类完成!")
            self.log(f"钢琴教程现在有更细致的专业分类，便于查找和学习")

def main():
    import sys
    
    # 检查命令行参数
    execute_mode = '--execute' in sys.argv or '-e' in sys.argv
    
    classifier = AdvancedPianoClassifier()
    
    if execute_mode:
        print("🚀 执行模式: 实际执行文件操作")
        classifier.run(simulate=False)
    else:
        classifier.run(simulate=True)

if __name__ == '__main__':
    main()