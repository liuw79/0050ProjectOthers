#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教程目录重构工具
按学习内容类型重新组织教程目录结构
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime
import re

class TutorialReorganizer:
    def __init__(self, tutorial_dir):
        self.tutorial_dir = Path(tutorial_dir)
        self.backup_dir = self.tutorial_dir.parent / "教程_备份"
        self.reorganization_plan = {
            '音乐艺术': {
                'keywords': ['钢琴', 'piano', '音乐', 'music', '乐理', '简谱', '五线谱', '吉他', 'guitar', '小提琴', 'violin', '声乐', '唱歌'],
                'subfolders': ['钢琴教程', '吉他教程', '声乐教程', '乐理基础', '其他乐器']
            },
            '编程技术': {
                'keywords': ['python', 'java', 'javascript', 'coding', '编程', '代码', 'web', 'html', 'css', 'react', 'vue', 'node'],
                'subfolders': ['前端开发', '后端开发', '移动开发', '数据科学', '算法数据结构']
            },
            '设计创意': {
                'keywords': ['photoshop', 'ps', 'ai', 'illustrator', 'design', '设计', '美工', 'ui', 'ux', '平面设计', '视频剪辑', 'pr', 'ae'],
                'subfolders': ['平面设计', 'UI/UX设计', '视频制作', '3D建模', '摄影后期']
            },
            '语言学习': {
                'keywords': ['english', '英语', '日语', '韩语', '法语', '德语', '西班牙语', 'japanese', 'korean', 'french'],
                'subfolders': ['英语学习', '日语学习', '韩语学习', '其他语言']
            },
            '职业技能': {
                'keywords': ['office', 'excel', 'word', 'ppt', 'powerpoint', '办公', '职场', '管理', '营销', '财务', '会计'],
                'subfolders': ['办公软件', '职场技能', '财务会计', '市场营销', '项目管理']
            },
            '学科教育': {
                'keywords': ['数学', 'math', '物理', 'physics', '化学', 'chemistry', '生物', 'biology', '历史', 'history', '地理'],
                'subfolders': ['数学', '物理', '化学', '生物', '文史地理']
            },
            '生活技能': {
                'keywords': ['烹饪', '料理', 'cooking', '健身', 'fitness', '瑜伽', 'yoga', '化妆', 'makeup', '手工', 'diy'],
                'subfolders': ['烹饪美食', '健身运动', '美容化妆', '手工制作', '生活百科']
            },
            '其他教程': {
                'keywords': [],  # 兜底分类
                'subfolders': ['未分类教程']
            }
        }
        
    def analyze_current_structure(self):
        """分析当前教程目录结构"""
        print("🔍 分析当前教程目录结构...")
        
        current_structure = {
            'total_folders': 0,
            'total_files': 0,
            'folder_list': [],
            'size_analysis': {}
        }
        
        if not self.tutorial_dir.exists():
            print(f"❌ 教程目录不存在: {self.tutorial_dir}")
            return current_structure
            
        for item in self.tutorial_dir.iterdir():
            if item.is_dir():
                current_structure['total_folders'] += 1
                folder_info = {
                    'name': item.name,
                    'path': str(item),
                    'size': self._get_folder_size(item),
                    'file_count': self._count_files(item)
                }
                current_structure['folder_list'].append(folder_info)
                
        # 按大小排序
        current_structure['folder_list'].sort(key=lambda x: x['size'], reverse=True)
        
        print(f"📊 当前结构统计:")
        print(f"   - 总文件夹数: {current_structure['total_folders']}")
        print(f"   - 最大的5个文件夹:")
        for folder in current_structure['folder_list'][:5]:
            size_gb = folder['size'] / (1024**3)
            print(f"     • {folder['name']}: {size_gb:.1f}GB ({folder['file_count']}个文件)")
            
        return current_structure
        
    def categorize_folders(self, current_structure):
        """根据关键词对文件夹进行分类"""
        print("\n📋 开始分类文件夹...")
        
        categorization_result = {}
        uncategorized = []
        
        for folder in current_structure['folder_list']:
            folder_name = folder['name'].lower()
            categorized = False
            
            # 跳过高维学堂
            if '高维学堂' in folder['name']:
                print(f"⏭️  跳过: {folder['name']} (按要求排除)")
                continue
                
            for category, config in self.reorganization_plan.items():
                if category == '其他教程':  # 跳过兜底分类
                    continue
                    
                for keyword in config['keywords']:
                    if keyword in folder_name:
                        if category not in categorization_result:
                            categorization_result[category] = []
                        categorization_result[category].append(folder)
                        categorized = True
                        print(f"✅ {folder['name']} → {category} (匹配关键词: {keyword})")
                        break
                        
                if categorized:
                    break
                    
            if not categorized:
                uncategorized.append(folder)
                print(f"❓ {folder['name']} → 未分类")
                
        # 未分类的放入其他教程
        if uncategorized:
            categorization_result['其他教程'] = uncategorized
            
        return categorization_result
        
    def generate_reorganization_plan(self, categorization_result):
        """生成重构计划"""
        print("\n📝 生成重构计划...")
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'source_dir': str(self.tutorial_dir),
            'backup_dir': str(self.backup_dir),
            'categories': {},
            'statistics': {
                'total_categories': len(categorization_result),
                'total_folders_to_move': sum(len(folders) for folders in categorization_result.values()),
                'estimated_time': '30-60分钟'
            }
        }
        
        for category, folders in categorization_result.items():
            total_size = sum(folder['size'] for folder in folders)
            plan['categories'][category] = {
                'folder_count': len(folders),
                'total_size_gb': round(total_size / (1024**3), 2),
                'folders': [{
                    'name': folder['name'],
                    'current_path': folder['path'],
                    'new_path': str(self.tutorial_dir / category / self._determine_subfolder(folder['name'], category)),
                    'size_gb': round(folder['size'] / (1024**3), 2)
                } for folder in folders]
            }
            
        # 保存计划到文件
        plan_file = self.tutorial_dir.parent / f"tutorial_reorganization_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
            
        print(f"📄 重构计划已保存: {plan_file}")
        
        # 显示计划摘要
        print("\n📊 重构计划摘要:")
        for category, info in plan['categories'].items():
            print(f"   📁 {category}: {info['folder_count']}个文件夹, {info['total_size_gb']}GB")
            
        return plan
        
    def _determine_subfolder(self, folder_name, category):
        """确定子文件夹分类"""
        folder_name_lower = folder_name.lower()
        
        if category == '音乐艺术':
            if any(kw in folder_name_lower for kw in ['钢琴', 'piano']):
                return '钢琴教程'
            elif any(kw in folder_name_lower for kw in ['吉他', 'guitar']):
                return '吉他教程'
            elif any(kw in folder_name_lower for kw in ['声乐', '唱歌', '歌唱']):
                return '声乐教程'
            elif any(kw in folder_name_lower for kw in ['乐理', '简谱', '五线谱']):
                return '乐理基础'
            else:
                return '其他乐器'
                
        elif category == '编程技术':
            if any(kw in folder_name_lower for kw in ['html', 'css', 'javascript', 'react', 'vue', 'web']):
                return '前端开发'
            elif any(kw in folder_name_lower for kw in ['python', 'java', 'node', 'backend']):
                return '后端开发'
            elif any(kw in folder_name_lower for kw in ['android', 'ios', 'mobile', 'app']):
                return '移动开发'
            elif any(kw in folder_name_lower for kw in ['data', 'ai', 'ml', 'machine']):
                return '数据科学'
            else:
                return '算法数据结构'
                
        # 其他分类的默认子文件夹
        subfolders = self.reorganization_plan.get(category, {}).get('subfolders', ['未分类'])
        return subfolders[0]  # 返回第一个子文件夹作为默认
        
    def create_backup(self):
        """创建备份"""
        print(f"\n💾 创建备份到: {self.backup_dir}")
        
        if self.backup_dir.exists():
            print("⚠️  备份目录已存在，跳过备份创建")
            return True
            
        try:
            # 只备份目录结构，不复制文件内容（节省时间和空间）
            self._create_structure_backup(self.tutorial_dir, self.backup_dir)
            print("✅ 备份创建完成")
            return True
        except Exception as e:
            print(f"❌ 备份创建失败: {e}")
            return False
            
    def _create_structure_backup(self, src, dst):
        """创建目录结构备份（不复制文件内容）"""
        dst.mkdir(parents=True, exist_ok=True)
        
        # 保存目录结构信息
        structure_info = {
            'timestamp': datetime.now().isoformat(),
            'original_structure': []
        }
        
        for item in src.iterdir():
            if item.is_dir():
                structure_info['original_structure'].append({
                    'name': item.name,
                    'path': str(item),
                    'size': self._get_folder_size(item)
                })
                
        # 保存结构信息到JSON文件
        with open(dst / 'original_structure.json', 'w', encoding='utf-8') as f:
            json.dump(structure_info, f, ensure_ascii=False, indent=2)
            
    def execute_reorganization(self, plan, dry_run=True):
        """执行重构（默认为模拟运行）"""
        if dry_run:
            print("\n🔍 模拟运行重构计划...")
        else:
            print("\n🚀 开始执行重构计划...")
            
        success_count = 0
        error_count = 0
        
        for category, info in plan['categories'].items():
            category_dir = self.tutorial_dir / category
            
            if not dry_run:
                category_dir.mkdir(exist_ok=True)
                
            print(f"\n📁 处理分类: {category}")
            
            for folder_info in info['folders']:
                src_path = Path(folder_info['current_path'])
                dst_path = Path(folder_info['new_path'])
                
                if dry_run:
                    print(f"   📋 {src_path.name} → {dst_path.relative_to(self.tutorial_dir)}")
                    success_count += 1
                else:
                    try:
                        # 创建目标子目录
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # 移动文件夹
                        shutil.move(str(src_path), str(dst_path))
                        print(f"   ✅ {src_path.name} → {dst_path.relative_to(self.tutorial_dir)}")
                        success_count += 1
                    except Exception as e:
                        print(f"   ❌ 移动失败 {src_path.name}: {e}")
                        error_count += 1
                        
        print(f"\n📊 重构完成统计:")
        print(f"   ✅ 成功: {success_count}")
        print(f"   ❌ 失败: {error_count}")
        
        if not dry_run and error_count == 0:
            print("\n🎉 教程目录重构完成！")
            self._generate_final_report()
            
    def _generate_final_report(self):
        """生成最终报告"""
        report_file = self.tutorial_dir.parent / f"tutorial_reorganization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("教程目录重构完成报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"重构时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"目标目录: {self.tutorial_dir}\n")
            f.write(f"备份目录: {self.backup_dir}\n\n")
            
            f.write("新的目录结构:\n")
            for category_dir in self.tutorial_dir.iterdir():
                if category_dir.is_dir():
                    f.write(f"📁 {category_dir.name}/\n")
                    for subfolder in category_dir.iterdir():
                        if subfolder.is_dir():
                            f.write(f"   📁 {subfolder.name}/\n")
                            for item in subfolder.iterdir():
                                if item.is_dir():
                                    f.write(f"      📁 {item.name}\n")
                                    
        print(f"📄 最终报告已保存: {report_file}")
        
    def _get_folder_size(self, folder_path):
        """获取文件夹大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
        except (OSError, PermissionError):
            pass
        return total_size
        
    def _count_files(self, folder_path):
        """统计文件夹中的文件数量"""
        count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                count += len(filenames)
        except (OSError, PermissionError):
            pass
        return count
        
    def run_full_reorganization(self, execute=False):
        """运行完整的重构流程"""
        print("🎯 教程目录重构工具")
        print("=" * 50)
        
        # 1. 分析当前结构
        current_structure = self.analyze_current_structure()
        if current_structure['total_folders'] == 0:
            print("❌ 没有找到需要重构的文件夹")
            return
            
        # 2. 分类文件夹
        categorization_result = self.categorize_folders(current_structure)
        
        # 3. 生成重构计划
        plan = self.generate_reorganization_plan(categorization_result)
        
        # 4. 创建备份
        if execute and not self.create_backup():
            print("❌ 备份创建失败，终止重构")
            return
            
        # 5. 执行重构
        self.execute_reorganization(plan, dry_run=not execute)
        
        if not execute:
            print("\n💡 这是模拟运行，如需实际执行重构，请运行:")
            print(f"   python3 tutorial_reorganizer.py --execute")
            
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='教程目录重构工具')
    parser.add_argument('--tutorial-dir', default='/Volumes/video/教程', help='教程目录路径')
    parser.add_argument('--execute', action='store_true', help='实际执行重构（默认为模拟运行）')
    
    args = parser.parse_args()
    
    reorganizer = TutorialReorganizer(args.tutorial_dir)
    reorganizer.run_full_reorganization(execute=args.execute)
    
if __name__ == '__main__':
    main()