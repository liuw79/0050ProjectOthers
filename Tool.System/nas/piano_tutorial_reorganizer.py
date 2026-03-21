#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钢琴教程目录重构工具
专门针对钢琴学习内容进行细分分类
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class PianoTutorialReorganizer:
    def __init__(self, tutorial_base_path="/Volumes/video/教程"):
        self.tutorial_base_path = Path(tutorial_base_path)
        self.backup_path = Path("./backup")
        self.log_file = None
        
        # 钢琴教程细分分类
        self.piano_categories = {
            '🎹 小汤系列': {
                'keywords': ['小汤', '汤普森', 'thompson', '小汤姆森'],
                'description': '汤普森简易钢琴教程系列'
            },
            '🎼 车尔尼系列': {
                'keywords': ['车尔尼', '599', '849', '299', '740', 'czerny'],
                'description': '车尔尼钢琴练习曲系列'
            },
            '📚 拜厄教程': {
                'keywords': ['拜厄', 'beyer', '基础', '入门', '初学'],
                'description': '拜厄钢琴基本教程'
            },
            '🎵 哈农练指法': {
                'keywords': ['哈农', 'hanon', '指法', '手指', '练指', '基本功', '方百里'],
                'description': '哈农钢琴练指法'
            },
            '👨‍🏫 布格缪勒作品': {
                'keywords': ['布格缪勒', '布格穆勒', 'burgmuller', '25首', '18首'],
                'description': '布格缪勒钢琴进阶练习曲'
            },
            '🎪 巴赫作品': {
                'keywords': ['巴赫', 'bach', '创意曲', '小前奏曲', '平均律'],
                'description': '巴赫钢琴作品集'
            },
            '🎨 流行曲目': {
                'keywords': ['流行', '现代', '爵士', 'pop', 'jazz', '动漫', '影视'],
                'description': '流行音乐和现代钢琴曲目'
            },
            '🎓 乐理基础': {
                'keywords': ['乐理', '音乐奥秘', '理论', '基础知识', '音乐理论'],
                'description': '音乐理论和乐理基础知识'
            },
            '📦 其他教材': {
                'keywords': ['piano', '钢琴', '教程', '教材', '练习'],
                'description': '其他钢琴教材和内容'
            }
        }
        
        # 需要删除的非钢琴教程关键词
        self.non_piano_keywords = [
            'photoshop', 'ps', 'ai', 'illustrator', 'design', '设计', '美工',
            'python', 'java', 'javascript', 'coding', '编程', '代码', 'web',
            'english', '英语', '日语', '韩语', 'french', 'german',
            'office', 'excel', 'word', 'ppt', '办公', '职场',
            '数学', 'math', '物理', 'physics', '化学', 'biology',
            '烹饪', 'cooking', '健身', 'fitness', '瑜伽', '化妆',
            '吉他', 'guitar', '小提琴', 'violin', '声乐', '唱歌'
        ]
        
        # 需要保留的音乐教程（即使不明确是钢琴）
        self.keep_music_keywords = [
            '音乐奥秘', '乐理', '方百里', '哈农', '鲍释贤'
        ]
        
    def setup_logging(self):
        """设置日志记录"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_dir = Path('./logs')
        log_dir.mkdir(exist_ok=True)
        
        self.log_file = log_dir / f'piano_reorganization_{timestamp}.log'
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
                
    def scan_tutorial_directories(self):
        """扫描教程目录"""
        self.log("🔍 开始扫描教程目录...")
        
        if not self.tutorial_base_path.exists():
            self.log(f"❌ 教程目录不存在: {self.tutorial_base_path}")
            return [], []
            
        piano_tutorials = []
        non_piano_tutorials = []
        
        try:
            for item in self.tutorial_base_path.iterdir():
                if not item.is_dir():
                    continue
                    
                folder_name = item.name.lower()
                
                # 跳过高维学堂
                if '高维学堂' in item.name:
                    self.log(f"⏭️  保持不变: {item.name}")
                    continue
                    
                # 判断是否为钢琴相关
                is_piano = any(keyword in folder_name for keyword in ['钢琴', 'piano'])
                
                # 判断是否为需要保留的音乐教程
                is_keep_music = any(keyword in folder_name for keyword in self.keep_music_keywords)
                
                # 判断是否为非钢琴教程
                is_non_piano = any(keyword in folder_name for keyword in self.non_piano_keywords)
                
                if is_piano or is_keep_music:
                    piano_tutorials.append(item)
                    self.log(f"🎹 钢琴/音乐教程: {item.name}")
                elif is_non_piano:
                    non_piano_tutorials.append(item)
                    self.log(f"❌ 非钢琴教程: {item.name}")
                    
        except Exception as e:
            self.log(f"❌ 扫描目录时出错: {e}")
            
        self.log(f"📊 扫描完成: 钢琴教程 {len(piano_tutorials)} 个, 非钢琴教程 {len(non_piano_tutorials)} 个")
        return piano_tutorials, non_piano_tutorials
        
    def process_collection_directory(self, collection_dir, categorized):
        """处理集合目录，将其子目录分类到不同分类中"""
        self.log(f"🔄 处理集合目录: {collection_dir.name}")
        
        try:
            subdirs = [d for d in collection_dir.iterdir() if d.is_dir()]
            for subdir in subdirs:
                subdir_name = subdir.name.lower()
                sub_categorized = False
                
                # 为子目录分类
                for category, config in self.piano_categories.items():
                    if category == '📦 其他教材':  # 跳过兜底分类
                        continue
                        
                    for keyword in config['keywords']:
                        if keyword in subdir_name:
                            if category not in categorized:
                                categorized[category] = []
                            categorized[category].append(subdir)
                            self.log(f"✅ {subdir.name} (来自{collection_dir.name}) → {category} (匹配: {keyword})")
                            sub_categorized = True
                            break
                            
                    if sub_categorized:
                        break
                        
                # 未分类的子目录放入其他教材
                if not sub_categorized:
                    if '📦 其他教材' not in categorized:
                        categorized['📦 其他教材'] = []
                    categorized['📦 其他教材'].append(subdir)
                    self.log(f"❓ {subdir.name} (来自{collection_dir.name}) → 📦 其他教材")
                    
        except Exception as e:
            self.log(f"⚠️ 处理集合目录时出错: {e}")
    
    def categorize_piano_tutorials(self, piano_tutorials):
        """对钢琴教程进行细分分类"""
        self.log("🎯 开始对钢琴教程进行细分分类...")
        
        categorized = {}
        
        for tutorial in piano_tutorials:
            folder_name = tutorial.name.lower()
            categorized_flag = False
            
            # 特殊处理鲍释贤教程 - 需要拆分到不同分类
            if '鲍释贤' in folder_name:
                self.process_collection_directory(tutorial, categorized)
                categorized_flag = True
            
            # 特殊处理Piano.tutorial.collection等集合目录
            elif 'piano.tutorial.collection' in folder_name or 'collection' in folder_name:
                self.process_collection_directory(tutorial, categorized)
                categorized_flag = True
            
            # 常规分类处理
            if not categorized_flag:
                # 按优先级进行分类
                for category, config in self.piano_categories.items():
                    if category == '📦 其他教材':  # 跳过兜底分类
                        continue
                        
                    for keyword in config['keywords']:
                        if keyword in folder_name:
                            if category not in categorized:
                                categorized[category] = []
                            categorized[category].append(tutorial)
                            self.log(f"✅ {tutorial.name} → {category} (匹配: {keyword})")
                            categorized_flag = True
                            break
                            
                    if categorized_flag:
                        break
                        
                # 未分类的放入其他教材
                if not categorized_flag:
                    if '📦 其他教材' not in categorized:
                        categorized['📦 其他教材'] = []
                    categorized['📦 其他教材'].append(tutorial)
                    self.log(f"❓ {tutorial.name} → 📦 其他教材")
                
        return categorized
        
    def create_new_structure(self, categorized, simulate=True):
        """创建新的目录结构"""
        mode = "模拟" if simulate else "实际"
        self.log(f"🏗️  开始{mode}创建新的钢琴教程目录结构...")
        
        new_base = self.tutorial_base_path / "钢琴教程专区"
        
        if not simulate:
            new_base.mkdir(exist_ok=True)
            
        operations = []
        
        for category, tutorials in categorized.items():
            category_path = new_base / category
            
            if not simulate:
                category_path.mkdir(exist_ok=True)
                
            self.log(f"📁 创建分类目录: {category} ({len(tutorials)}个教程)")
            
            for tutorial in tutorials:
                new_path = category_path / tutorial.name
                operation = {
                    'action': 'move',
                    'source': tutorial,
                    'destination': new_path,
                    'category': category
                }
                operations.append(operation)
                
                if not simulate:
                    try:
                        shutil.move(str(tutorial), str(new_path))
                        self.log(f"✅ 移动: {tutorial.name} → {category}")
                    except Exception as e:
                        self.log(f"❌ 移动失败: {tutorial.name} - {e}")
                else:
                    self.log(f"📋 计划移动: {tutorial.name} → {category}")
                    
        return operations
        
    def delete_non_piano_tutorials(self, non_piano_tutorials, simulate=True):
        """删除非钢琴教程"""
        mode = "模拟" if simulate else "实际"
        self.log(f"🗑️  开始{mode}删除非钢琴教程...")
        
        deleted_operations = []
        
        for tutorial in non_piano_tutorials:
            # 跳过高维学堂
            if '高维学堂' in tutorial.name:
                continue
                
            operation = {
                'action': 'delete',
                'target': tutorial,
                'name': tutorial.name
            }
            deleted_operations.append(operation)
            
            if not simulate:
                try:
                    if tutorial.is_dir():
                        shutil.rmtree(tutorial)
                    else:
                        tutorial.unlink()
                    self.log(f"🗑️  已删除: {tutorial.name}")
                except Exception as e:
                    self.log(f"❌ 删除失败: {tutorial.name} - {e}")
            else:
                self.log(f"📋 计划删除: {tutorial.name}")
                
        return deleted_operations
        
    def generate_report(self, categorized, deleted_operations, operations):
        """生成重构报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = Path(f'piano_reorganization_report_{timestamp}.json')
        
        # 统计信息
        total_piano = sum(len(tutorials) for tutorials in categorized.values())
        total_deleted = len(deleted_operations)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_piano_tutorials': total_piano,
                'total_deleted_tutorials': total_deleted,
                'categories_created': len(categorized)
            },
            'piano_categories': {},
            'deleted_tutorials': [op['name'] for op in deleted_operations],
            'operations': {
                'moves': len([op for op in operations if op['action'] == 'move']),
                'deletions': len(deleted_operations)
            }
        }
        
        # 详细分类信息
        for category, tutorials in categorized.items():
            report['piano_categories'][category] = {
                'count': len(tutorials),
                'tutorials': [t.name for t in tutorials],
                'description': self.piano_categories.get(category, {}).get('description', '')
            }
            
        # 保存报告
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        self.log(f"📄 重构报告已保存: {report_file}")
        return report_file
        
    def show_preview(self, categorized, non_piano_tutorials):
        """显示重构预览"""
        self.log("\n🎯 钢琴教程目录重构预览")
        self.log("=" * 60)
        
        self.log("\n🏗️  新的钢琴教程目录结构:")
        self.log("教程/")
        self.log("├── 钢琴教程专区/")
        
        total_piano = 0
        for category, tutorials in categorized.items():
            total_piano += len(tutorials)
            self.log(f"│   ├── {category}/  ({len(tutorials)}个教程)")
            for tutorial in tutorials[:2]:  # 只显示前2个
                self.log(f"│   │   ├── {tutorial.name[:50]}...")
            if len(tutorials) > 2:
                self.log(f"│   │   └── ... 还有{len(tutorials)-2}个教程")
                
        self.log("├── 高维学堂/  (保持不变)")
        
        self.log(f"\n🗑️  将要删除的非钢琴教程 ({len([t for t in non_piano_tutorials if '高维学堂' not in t.name])}个):")
        for tutorial in non_piano_tutorials:
            if '高维学堂' not in tutorial.name:
                self.log(f"   ❌ {tutorial.name}")
                
        self.log(f"\n📊 统计信息:")
        self.log(f"   钢琴教程总数: {total_piano}")
        self.log(f"   删除教程数: {len([t for t in non_piano_tutorials if '高维学堂' not in t.name])}")
        self.log(f"   分类数量: {len(categorized)}")
        
    def run(self, simulate=True):
        """运行重构流程"""
        self.setup_logging()
        
        mode = "模拟运行" if simulate else "实际执行"
        self.log(f"🚀 开始钢琴教程目录重构 - {mode}")
        
        # 1. 扫描目录
        piano_tutorials, non_piano_tutorials = self.scan_tutorial_directories()
        
        if not piano_tutorials and not non_piano_tutorials:
            self.log("❌ 未找到任何教程目录")
            return
            
        # 2. 分类钢琴教程
        categorized = self.categorize_piano_tutorials(piano_tutorials)
        
        # 3. 显示预览
        self.show_preview(categorized, non_piano_tutorials)
        
        if simulate:
            self.log("\n⚠️  这是模拟运行，没有实际修改文件")
            self.log("如需实际执行，请运行: python3 piano_tutorial_reorganizer.py --execute")
        else:
            # 4. 创建新结构
            operations = self.create_new_structure(categorized, simulate=False)
            
            # 5. 删除非钢琴教程
            deleted_operations = self.delete_non_piano_tutorials(non_piano_tutorials, simulate=False)
            
            # 6. 生成报告
            report_file = self.generate_report(categorized, deleted_operations, operations)
            
            self.log(f"\n🎉 钢琴教程目录重构完成!")
            self.log(f"📄 详细报告: {report_file}")
            
def main():
    import sys
    
    # 检查命令行参数
    execute_mode = '--execute' in sys.argv or '-e' in sys.argv
    force_mode = '--force' in sys.argv or '-f' in sys.argv
    
    reorganizer = PianoTutorialReorganizer()
    
    if execute_mode:
        if force_mode:
            print("🚀 强制执行模式: 直接执行文件操作")
            reorganizer.run(simulate=False)
        else:
            print("⚠️  警告: 即将执行实际的文件操作!")
            print("这将移动钢琴教程到新目录并删除非钢琴教程")
            confirm = input("确认继续? (输入 'YES' 确认): ")
            
            if confirm == 'YES':
                reorganizer.run(simulate=False)
            else:
                print("❌ 操作已取消")
    else:
        reorganizer.run(simulate=True)
        
if __name__ == '__main__':
    main()