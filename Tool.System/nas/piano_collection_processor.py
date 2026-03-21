#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钢琴教程集合目录处理器
专门处理Piano.tutorial.collection等集合目录的深度分类
"""

import os
import shutil
from pathlib import Path
import logging
from datetime import datetime

class PianoCollectionProcessor:
    def __init__(self):
        # 教程基础路径
        self.tutorial_base_path = Path('/Volumes/video/教程')
        self.piano_zone_path = self.tutorial_base_path / '钢琴教程专区'
        
        # 钢琴教程细分分类
        self.piano_categories = {
            '🎹 小汤系列': {
                'keywords': ['小汤', '汤普森', 'thompson'],
                'description': '汤普森简易钢琴教程系列'
            },
            '🎼 车尔尼系列': {
                'keywords': ['车尔尼', 'czerny', '299', '599', '849', '740'],
                'description': '车尔尼钢琴练习曲系列'
            },
            '📚 拜厄教程': {
                'keywords': ['拜厄', 'beyer', '基础入门'],
                'description': '拜厄钢琴基本教程'
            },
            '🎪 巴赫作品': {
                'keywords': ['巴赫', 'bach', '创意曲', '平均律'],
                'description': '巴赫钢琴作品集'
            },
            '🎵 哈农练指法': {
                'keywords': ['哈农', 'hanon', '练指法', '方百里'],
                'description': '哈农钢琴练指法'
            },
            '🎓 乐理基础': {
                'keywords': ['乐理', '音乐理论', '基础知识', '音乐奥秘'],
                'description': '音乐理论和乐理基础知识'
            },
            '🎭 考级教程': {
                'keywords': ['考级', '等级', 'grade', '音协', '央音'],
                'description': '钢琴考级相关教程'
            },
            '📦 其他教材': {
                'keywords': [],  # 兜底分类
                'description': '其他钢琴教材和内容'
            }
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = Path(f'logs/piano_collection_processing_{timestamp}.log')
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
    
    def find_collection_directories(self):
        """查找需要处理的集合目录"""
        self.log("🔍 查找需要处理的集合目录...")
        
        collection_dirs = []
        
        # 在其他教材分类中查找集合目录
        other_materials_path = self.piano_zone_path / '📦 其他教材'
        if other_materials_path.exists():
            for item in other_materials_path.iterdir():
                if item.is_dir():
                    item_name = item.name.lower()
                    if ('collection' in item_name or 
                        'tutorial' in item_name and len(list(item.iterdir())) > 5):
                        collection_dirs.append(item)
                        self.log(f"📁 发现集合目录: {item.name}")
        
        return collection_dirs
    
    def categorize_subdirectory(self, subdir):
        """对子目录进行分类"""
        subdir_name = subdir.name.lower()
        
        # 按优先级进行分类
        for category, config in self.piano_categories.items():
            if category == '📦 其他教材':  # 跳过兜底分类
                continue
                
            for keyword in config['keywords']:
                if keyword in subdir_name:
                    return category, keyword
        
        # 未匹配到特定分类，返回其他教材
        return '📦 其他教材', None
    
    def process_collection_directory(self, collection_dir, simulate=True):
        """处理单个集合目录"""
        mode = "模拟" if simulate else "实际"
        self.log(f"🔄 {mode}处理集合目录: {collection_dir.name}")
        
        operations = []
        
        try:
            subdirs = [d for d in collection_dir.iterdir() if d.is_dir()]
            self.log(f"📊 发现 {len(subdirs)} 个子目录")
            
            for subdir in subdirs:
                category, keyword = self.categorize_subdirectory(subdir)
                
                # 目标路径
                target_category_path = self.piano_zone_path / category
                target_path = target_category_path / subdir.name
                
                operation = {
                    'action': 'move',
                    'source': subdir,
                    'destination': target_path,
                    'category': category,
                    'keyword': keyword
                }
                operations.append(operation)
                
                if not simulate:
                    # 确保目标分类目录存在
                    target_category_path.mkdir(exist_ok=True)
                    
                    try:
                        shutil.move(str(subdir), str(target_path))
                        match_info = f" (匹配: {keyword})" if keyword else ""
                        self.log(f"✅ 移动: {subdir.name} → {category}{match_info}")
                    except Exception as e:
                        self.log(f"❌ 移动失败: {subdir.name} - {e}")
                else:
                    match_info = f" (匹配: {keyword})" if keyword else ""
                    self.log(f"📋 计划移动: {subdir.name} → {category}{match_info}")
            
            # 如果集合目录已空，删除它
            if not simulate:
                remaining_items = list(collection_dir.iterdir())
                if not remaining_items or all(not item.is_dir() for item in remaining_items):
                    try:
                        shutil.rmtree(collection_dir)
                        self.log(f"🗑️ 删除空的集合目录: {collection_dir.name}")
                    except Exception as e:
                        self.log(f"⚠️ 删除集合目录失败: {e}")
                        
        except Exception as e:
            self.log(f"❌ 处理集合目录时出错: {e}")
        
        return operations
    
    def run(self, simulate=True):
        """运行集合目录处理流程"""
        mode = "模拟运行" if simulate else "实际执行"
        self.log(f"🚀 开始钢琴教程集合目录处理 - {mode}")
        
        # 查找集合目录
        collection_dirs = self.find_collection_directories()
        
        if not collection_dirs:
            self.log("ℹ️ 未发现需要处理的集合目录")
            return
        
        all_operations = []
        
        # 处理每个集合目录
        for collection_dir in collection_dirs:
            operations = self.process_collection_directory(collection_dir, simulate)
            all_operations.extend(operations)
        
        # 统计信息
        total_moves = len(all_operations)
        category_stats = {}
        for op in all_operations:
            category = op['category']
            category_stats[category] = category_stats.get(category, 0) + 1
        
        self.log(f"\n📊 处理统计:")
        self.log(f"   总移动数: {total_moves}")
        for category, count in category_stats.items():
            self.log(f"   {category}: {count}个")
        
        if simulate:
            self.log("\n⚠️ 这是模拟运行，没有实际修改文件")
            self.log("如需实际执行，请运行: python3 piano_collection_processor.py --execute")
        else:
            self.log(f"\n🎉 集合目录处理完成!")

def main():
    import sys
    
    # 检查命令行参数
    execute_mode = '--execute' in sys.argv or '-e' in sys.argv
    
    processor = PianoCollectionProcessor()
    
    if execute_mode:
        print("🚀 强制执行模式: 直接执行文件操作")
        processor.run(simulate=False)
    else:
        processor.run(simulate=True)

if __name__ == '__main__':
    main()