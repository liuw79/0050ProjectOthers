#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电视目录标准化整理工具
按照标准化流程对电视目录进行完整的分析、分类和整理
"""

import os
import re
import shutil
from pathlib import Path
import json
from datetime import datetime

class TVOrganizer:
    def __init__(self, tv_directory):
        self.tv_directory = Path(tv_directory)
        self.analysis_report = {
            'total_folders': 0,
            'total_files': 0,
            'loose_files': [],
            'folders_without_chinese': [],
            'folders_with_issues': [],
            'categorization_suggestions': {},
            'quality_assessment': {},
            'space_usage': {}
        }
        
    def analyze_directory(self):
        """阶段一：目录分析"""
        print("🔍 开始电视目录分析...")
        
        # 统计基础信息
        folders = []
        loose_files = []
        
        for item in self.tv_directory.iterdir():
            if item.is_dir():
                folders.append(item)
                self.analysis_report['total_folders'] += 1
            else:
                loose_files.append(item)
                self.analysis_report['total_files'] += 1
                
        self.analysis_report['loose_files'] = [f.name for f in loose_files]
        
        # 分析文件夹命名问题
        for folder in folders:
            folder_name = folder.name
            
            # 检查是否包含中文
            if not re.search(r'[\u4e00-\u9fff]', folder_name):
                self.analysis_report['folders_without_chinese'].append(folder_name)
                
            # 检查其他问题
            issues = []
            if '[无评分]' not in folder_name and 'IMDB' not in folder_name:
                issues.append('缺少评分信息')
            if not re.search(r'Season \d+|S\d+', folder_name):
                issues.append('可能缺少季数信息')
                
            if issues:
                self.analysis_report['folders_with_issues'].append({
                    'name': folder_name,
                    'issues': issues
                })
                
        print(f"📊 分析完成：{self.analysis_report['total_folders']}个文件夹，{self.analysis_report['total_files']}个散落文件")
        return self.analysis_report
        
    def categorize_content(self):
        """阶段三：内容分类"""
        print("📁 开始内容分类分析...")
        
        categories = {
            '纪录片': [],
            '美剧': [],
            '英剧': [],
            '韩剧': [],
            '日剧': [],
            '国产剧': [],
            '综艺节目': [],
            '其他': []
        }
        
        # 纪录片关键词
        documentary_keywords = [
            'Planet', 'Earth', 'Universe', 'History', 'Civilisation', 'Cosmos',
            'Human Body', 'Documentary', 'BBC', 'National Geographic', 'Discovery',
            '地球', '宇宙', '历史', '文明', '纪录', '探索'
        ]
        
        # 美剧关键词
        us_series_keywords = [
            'Game of Thrones', 'Foundation', 'House of', 'Breaking Bad',
            'The Walking Dead', 'Stranger Things', 'Friends', 'The Office'
        ]
        
        # 韩剧关键词
        korean_series_keywords = [
            'Hospital Playlist', 'Squid Game', 'Kingdom', 'Crash Landing',
            '医院', '鱿鱼', '王国', '爱的'
        ]
        
        for folder in self.tv_directory.iterdir():
            if not folder.is_dir():
                continue
                
            folder_name = folder.name.lower()
            
            # 分类逻辑
            if any(keyword.lower() in folder_name for keyword in documentary_keywords):
                categories['纪录片'].append(folder.name)
            elif any(keyword.lower() in folder_name for keyword in korean_series_keywords):
                categories['韩剧'].append(folder.name)
            elif any(keyword.lower() in folder_name for keyword in us_series_keywords):
                categories['美剧'].append(folder.name)
            elif 'japan' in folder_name or 'japanese' in folder_name:
                categories['日剧'].append(folder.name)
            else:
                categories['其他'].append(folder.name)
                
        self.analysis_report['categorization_suggestions'] = categories
        
        # 打印分类结果
        for category, items in categories.items():
            if items:
                print(f"  {category}: {len(items)}个")
                
        return categories
        
    def assess_quality(self):
        """阶段四：质量评估"""
        print("🗑️ 开始质量评估...")
        
        quality_assessment = {
            '建议删除': [],
            '考虑删除': [],
            '必须保留': [],
            '需要整理': []
        }
        
        # 重新扫描当前散落文件（因为之前可能已经移动了一些）
        current_loose_files = []
        for item in self.tv_directory.iterdir():
            if item.is_file():
                current_loose_files.append(item.name)
        
        # 评估散落文件
        for file_name in current_loose_files:
            file_path = self.tv_directory / file_name
            if not file_path.exists():
                continue
            file_size = file_path.stat().st_size / (1024**3)  # GB
            
            if file_name.endswith(('.nfo', '.jpg', '.png', '-thumb.jpg')):
                quality_assessment['考虑删除'].append({
                    'name': file_name,
                    'reason': '元数据文件，可能不需要',
                    'size_gb': round(file_size, 2)
                })
            elif file_size > 20:  # 大于20GB的单个文件
                quality_assessment['需要整理'].append({
                    'name': file_name,
                    'reason': '大文件需要放入合适文件夹',
                    'size_gb': round(file_size, 2)
                })
                
        # 评估文件夹
        for folder in self.tv_directory.iterdir():
            if not folder.is_dir():
                continue
                
            folder_size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file()) / (1024**3)
            
            if folder_size < 0.1:  # 小于100MB
                quality_assessment['考虑删除'].append({
                    'name': folder.name,
                    'reason': '文件夹过小，可能是无用内容',
                    'size_gb': round(folder_size, 2)
                })
            elif folder_size > 100:  # 大于100GB
                quality_assessment['必须保留'].append({
                    'name': folder.name,
                    'reason': '大型内容，具有保留价值',
                    'size_gb': round(folder_size, 2)
                })
                
        self.analysis_report['quality_assessment'] = quality_assessment
        
        # 打印评估结果
        for category, items in quality_assessment.items():
            if items:
                print(f"  {category}: {len(items)}项")
                total_size = sum(item['size_gb'] for item in items)
                print(f"    总大小: {total_size:.1f}GB")
                
        return quality_assessment
        
    def organize_loose_files(self):
        """整理散落文件"""
        print("📦 开始整理散落文件...")
        
        organized_count = 0
        
        for file_name in self.analysis_report['loose_files']:
            file_path = self.tv_directory / file_name
            
            # 跳过小文件和元数据文件
            if file_name.endswith(('.nfo', '.jpg', '.png', '-thumb.jpg')):
                continue
                
            # 为大视频文件创建文件夹
            if file_path.suffix.lower() in ['.mkv', '.mp4', '.avi', '.m2ts', '.ts']:
                file_size = file_path.stat().st_size / (1024**3)
                
                if file_size > 1:  # 大于1GB的视频文件
                    # 创建以文件名命名的文件夹
                    folder_name = file_path.stem
                    # 清理文件夹名称
                    folder_name = re.sub(r'\.(mkv|mp4|avi|m2ts|ts)$', '', folder_name, flags=re.IGNORECASE)
                    
                    new_folder = self.tv_directory / f"{folder_name} [无评分]"
                    
                    if not new_folder.exists():
                        new_folder.mkdir()
                        shutil.move(str(file_path), str(new_folder / file_name))
                        print(f"  ✅ 移动文件: {file_name} -> {new_folder.name}/")
                        organized_count += 1
                        
        print(f"📦 散落文件整理完成，处理了 {organized_count} 个文件")
        return organized_count
        
    def add_chinese_names(self):
        """为缺少中文名称的文件夹添加中文名称"""
        print("🏷️ 开始添加中文名称...")
        
        # 常见英文到中文的映射
        name_mapping = {
            'Game of Thrones': '权力的游戏',
            'Foundation': '基地',
            'Civilisation': '文明',
            'Cosmos': '宇宙',
            'Planet Earth': '地球脉动',
            'Human Body': '人体奥秘',
            'Hospital Playlist': '机智的医生生活',
            'Clarksons Farm': '克拉克森的农场',
            'Crime Crackdown': '扫黑风暴',
            'Eden Untamed Planet': '伊甸园：野性星球',
            'How the Universe Works': '宇宙是如何运行的',
            'History Of World': '世界历史',
            'Cycle Around Japan': '日本骑行之旅',
            'Inside Planet Earth': '地球内部探秘',
            'Inside The Human Body': '人体内部之旅'
        }
        
        renamed_count = 0
        
        for folder_name in self.analysis_report['folders_without_chinese']:
            folder_path = self.tv_directory / folder_name
            
            if not folder_path.exists():
                continue
                
            # 查找匹配的中文名称
            chinese_name = None
            for english, chinese in name_mapping.items():
                if english.lower() in folder_name.lower():
                    chinese_name = chinese
                    break
                    
            if chinese_name:
                # 构建新的文件夹名称
                new_name = folder_name
                
                # 在开头添加中文名称
                if not new_name.startswith(chinese_name):
                    new_name = f"{chinese_name}.{new_name}"
                    
                new_folder_path = self.tv_directory / new_name
                
                if not new_folder_path.exists():
                    folder_path.rename(new_folder_path)
                    print(f"  ✅ 重命名: {folder_name} -> {new_name}")
                    renamed_count += 1
                    
        print(f"🏷️ 中文名称添加完成，处理了 {renamed_count} 个文件夹")
        return renamed_count
        
    def generate_report(self):
        """生成整理报告"""
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"tv_organization_report_{report_time}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_report, f, ensure_ascii=False, indent=2)
            
        print(f"📋 整理报告已保存: {report_file}")
        return report_file
        
    def run_full_organization(self):
        """运行完整的标准化整理流程"""
        print("🚀 开始电视目录标准化整理...")
        print("=" * 50)
        
        # 阶段一：目录分析
        self.analyze_directory()
        print()
        
        # 阶段二：文件重命名（散落文件整理）
        self.organize_loose_files()
        print()
        
        # 添加中文名称
        self.add_chinese_names()
        print()
        
        # 阶段三：内容分类
        self.categorize_content()
        print()
        
        # 阶段四：质量评估
        self.assess_quality()
        print()
        
        # 生成报告
        self.generate_report()
        
        print("=" * 50)
        print("✅ 电视目录标准化整理完成！")
        
        return self.analysis_report

def main():
    tv_directory = "/Volumes/video/电视"
    
    if not os.path.exists(tv_directory):
        print(f"❌ 错误：电视目录不存在 - {tv_directory}")
        return
        
    organizer = TVOrganizer(tv_directory)
    organizer.run_full_organization()

if __name__ == "__main__":
    main()