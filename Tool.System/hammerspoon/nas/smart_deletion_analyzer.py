#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能删除建议分析器
分析目录中可以删除的文件和文件夹，提供安全的删除建议
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json

class SmartDeletionAnalyzer:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.deletion_suggestions = {
            'auto_delete': [],      # 可以自动删除的安全项目
            'suggest_delete': [],   # 建议删除但需确认的项目
            'manual_review': []     # 需要人工审核的项目
        }
        
        # 定义各种模式
        self.metadata_patterns = [
            r'\.nfo$', r'\.xml$', r'-thumb\.jpg$', r'-poster\.jpg$',
            r'\.DS_Store$', r'Thumbs\.db$', r'\.txt$'
        ]
        
        self.temp_patterns = [
            r'\.tmp$', r'\.temp$', r'\.cache$', r'\.part$'
        ]
        
        self.sample_patterns = [
            r'sample', r'preview', r'trailer', r'rarbg\.txt$'
        ]
        
        self.release_patterns = [
            r'readme', r'nfo', r'proof', r'covers?'
        ]
        
        self.low_quality_indicators = [
            r'480p', r'360p', r'cam', r'ts', r'tc', r'dvdscr'
        ]
        
        self.outdated_formats = [
            r'\.rmvb$', r'\.rm$', r'\.vcd$', r'\.dat$'
        ]
    
    def analyze_directory(self):
        """分析目录并生成删除建议"""
        print(f"🔍 开始分析目录: {self.target_dir}")
        print("=" * 60)
        
        for item in self.target_dir.iterdir():
            if item.is_file():
                self._analyze_file(item)
            elif item.is_dir():
                self._analyze_folder(item)
        
        self._generate_report()
        return self.deletion_suggestions
    
    def _analyze_file(self, file_path):
        """分析单个文件"""
        file_name = file_path.name.lower()
        file_size = file_path.stat().st_size
        
        # 检查元数据文件
        if any(re.search(pattern, file_name, re.IGNORECASE) for pattern in self.metadata_patterns):
            self.deletion_suggestions['auto_delete'].append({
                'path': str(file_path),
                'type': 'metadata_file',
                'reason': '元数据文件，可安全删除',
                'size': file_size
            })
            return
        
        # 检查临时文件
        if any(re.search(pattern, file_name, re.IGNORECASE) for pattern in self.temp_patterns):
            self.deletion_suggestions['auto_delete'].append({
                'path': str(file_path),
                'type': 'temp_file',
                'reason': '临时文件，可安全删除',
                'size': file_size
            })
            return
        
        # 检查样本文件
        if any(re.search(pattern, file_name, re.IGNORECASE) for pattern in self.sample_patterns):
            self.deletion_suggestions['suggest_delete'].append({
                'path': str(file_path),
                'type': 'sample_file',
                'reason': '样本/预览文件，建议删除',
                'size': file_size
            })
            return
        
        # 检查过时格式
        if any(re.search(pattern, file_name, re.IGNORECASE) for pattern in self.outdated_formats):
            self.deletion_suggestions['manual_review'].append({
                'path': str(file_path),
                'type': 'outdated_format',
                'reason': '过时格式文件，建议人工审核',
                'size': file_size
            })
    
    def _analyze_folder(self, folder_path):
        """分析文件夹"""
        folder_name = folder_path.name.lower()
        
        # 检查空文件夹
        if self._is_empty_folder(folder_path):
            self.deletion_suggestions['auto_delete'].append({
                'path': str(folder_path),
                'type': 'empty_folder',
                'reason': '空文件夹，可安全删除',
                'size': 0
            })
            return
        
        # 检查过小文件夹
        folder_size = self._get_folder_size(folder_path)
        if folder_size < 100 * 1024 * 1024:  # 小于100MB
            video_files = self._count_video_files(folder_path)
            if video_files == 0:
                self.deletion_suggestions['auto_delete'].append({
                    'path': str(folder_path),
                    'type': 'small_folder',
                    'reason': f'过小文件夹({self._format_size(folder_size)})且无视频内容',
                    'size': folder_size
                })
                return
        
        # 检查发布说明文件夹
        if any(re.search(pattern, folder_name, re.IGNORECASE) for pattern in self.release_patterns):
            self.deletion_suggestions['suggest_delete'].append({
                'path': str(folder_path),
                'type': 'release_folder',
                'reason': '发布说明文件夹，建议删除',
                'size': folder_size
            })
            return
        
        # 检查低质量版本
        if any(re.search(pattern, folder_name, re.IGNORECASE) for pattern in self.low_quality_indicators):
            self.deletion_suggestions['manual_review'].append({
                'path': str(folder_path),
                'type': 'low_quality',
                'reason': '可能是低质量版本，建议人工审核',
                'size': folder_size
            })
            return
        
        # 检查异常大小
        if folder_size > 200 * 1024 * 1024 * 1024:  # 大于200GB
            self.deletion_suggestions['manual_review'].append({
                'path': str(folder_path),
                'type': 'oversized',
                'reason': f'异常大小({self._format_size(folder_size)})，建议人工审核',
                'size': folder_size
            })
        elif folder_size < 500 * 1024 * 1024 and self._count_video_files(folder_path) == 0:  # 小于500MB且无视频
            self.deletion_suggestions['suggest_delete'].append({
                'path': str(folder_path),
                'type': 'suspicious_small',
                'reason': f'可疑的小文件夹({self._format_size(folder_size)})且无视频内容',
                'size': folder_size
            })
    
    def _is_empty_folder(self, folder_path):
        """检查是否为空文件夹"""
        try:
            return len(list(folder_path.iterdir())) == 0
        except:
            return False
    
    def _get_folder_size(self, folder_path):
        """获取文件夹大小"""
        total_size = 0
        try:
            for item in folder_path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except:
            pass
        return total_size
    
    def _count_video_files(self, folder_path):
        """统计视频文件数量"""
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.m4v', '.ts', '.m2ts'}
        count = 0
        try:
            for item in folder_path.rglob('*'):
                if item.is_file() and item.suffix.lower() in video_extensions:
                    count += 1
        except:
            pass
        return count
    
    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f}KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f}MB"
        else:
            return f"{size_bytes/(1024**3):.1f}GB"
    
    def _generate_report(self):
        """生成删除建议报告"""
        print("\n📊 删除建议分析报告")
        print("=" * 60)
        
        # 统计各类别数量和大小
        categories = {
            'auto_delete': '🗑️ 可自动删除',
            'suggest_delete': '⚠️ 建议删除',
            'manual_review': '🔍 需人工审核'
        }
        
        total_items = 0
        total_size = 0
        
        for category, items in self.deletion_suggestions.items():
            if items:
                category_size = sum(item['size'] for item in items)
                total_items += len(items)
                total_size += category_size
                
                print(f"\n{categories[category]}:")
                print(f"  项目数量: {len(items)}")
                print(f"  总大小: {self._format_size(category_size)}")
                
                # 显示前5个项目作为示例
                for i, item in enumerate(items[:5]):
                    print(f"  - {Path(item['path']).name} ({self._format_size(item['size'])}) - {item['reason']}")
                
                if len(items) > 5:
                    print(f"  ... 还有 {len(items) - 5} 个项目")
        
        print(f"\n📈 总计:")
        print(f"  可删除项目: {total_items}")
        print(f"  可释放空间: {self._format_size(total_size)}")
        
        # 保存详细报告到文件
        self._save_detailed_report()
    
    def _save_detailed_report(self):
        """保存详细报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"deletion_analysis_{timestamp}.json"
        
        report_data = {
            'analysis_time': datetime.now().isoformat(),
            'target_directory': str(self.target_dir),
            'suggestions': self.deletion_suggestions,
            'summary': {
                'total_items': sum(len(items) for items in self.deletion_suggestions.values()),
                'total_size': sum(sum(item['size'] for item in items) for items in self.deletion_suggestions.values())
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细报告已保存: {report_file}")

def main():
    # 默认分析电视目录
    tv_dir = "/Volumes/video/电视"
    
    if not os.path.exists(tv_dir):
        print(f"❌ 目录不存在: {tv_dir}")
        return
    
    analyzer = SmartDeletionAnalyzer(tv_dir)
    suggestions = analyzer.analyze_directory()
    
    print("\n✅ 分析完成！")
    print("\n💡 使用建议:")
    print("1. 查看生成的JSON报告文件获取详细信息")
    print("2. 先处理'可自动删除'类别的安全项目")
    print("3. 仔细审核'建议删除'类别的项目")
    print("4. 人工检查'需人工审核'类别的项目")
    print("5. 建议分批次执行删除操作")

if __name__ == "__main__":
    main()