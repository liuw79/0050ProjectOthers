#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电视目录质量分析器
分析电视目录中可能存在质量问题的内容
"""

import os
import re
from pathlib import Path
from datetime import datetime

class TVQualityAnalyzer:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.quality_issues = {
            'low_rating': [],           # 评分过低
            'oversized': [],            # 异常大小
            'low_quality_indicators': [], # 低质量标识
            'suspicious_naming': [],     # 可疑命名
            'no_rating': []             # 无评分
        }
    
    def analyze_quality(self):
        """分析目录质量问题"""
        print(f"🔍 开始分析电视目录质量: {self.target_dir}")
        print("=" * 60)
        
        for item in self.target_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_') and not item.name.endswith('.json'):
                self._analyze_folder(item)
        
        self._generate_quality_report()
        return self.quality_issues
    
    def _analyze_folder(self, folder_path):
        """分析单个文件夹"""
        folder_name = folder_path.name
        folder_size = self._get_folder_size(folder_path)
        
        # 提取评分
        rating = self._extract_rating(folder_name)
        
        # 检查评分问题
        if rating is None:
            self.quality_issues['no_rating'].append({
                'name': folder_name,
                'size': folder_size,
                'issue': '缺少评分信息'
            })
        elif rating < 7.5:
            self.quality_issues['low_rating'].append({
                'name': folder_name,
                'size': folder_size,
                'rating': rating,
                'issue': f'评分过低({rating}分)'
            })
        
        # 检查异常大小 (>200GB)
        if folder_size > 200 * 1024 * 1024 * 1024:
            self.quality_issues['oversized'].append({
                'name': folder_name,
                'size': folder_size,
                'rating': rating,
                'issue': f'异常大小({self._format_size(folder_size)})'
            })
        
        # 检查低质量标识
        low_quality_patterns = [
            r'480p', r'360p', r'cam', r'ts', r'tc', r'dvdscr',
            r'sample', r'preview', r'trailer', r'guacamole',
            r'dtg', r'season\.1\.4', r'wiki'
        ]
        
        for pattern in low_quality_patterns:
            if re.search(pattern, folder_name, re.IGNORECASE):
                self.quality_issues['low_quality_indicators'].append({
                    'name': folder_name,
                    'size': folder_size,
                    'rating': rating,
                    'issue': f'包含低质量标识: {pattern}',
                    'pattern': pattern
                })
                break
        
        # 检查可疑命名
        suspicious_patterns = [
            r'[^a-zA-Z0-9一-鿿\.\-\[\]\(\)\s&]',  # 特殊字符
            r'\b(copy|backup|temp|test)\b',        # 临时文件标识
            r'\d{8,}',                             # 长数字串
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, folder_name, re.IGNORECASE):
                self.quality_issues['suspicious_naming'].append({
                    'name': folder_name,
                    'size': folder_size,
                    'rating': rating,
                    'issue': f'可疑命名模式: {pattern}'
                })
                break
    
    def _extract_rating(self, folder_name):
        """提取评分"""
        # 匹配 [X.X分] 格式
        rating_match = re.search(r'\[([0-9]\.[0-9])分\]', folder_name)
        if rating_match:
            return float(rating_match.group(1))
        
        # 检查是否为无评分
        if '[无评分]' in folder_name:
            return None
        
        return None
    
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
    
    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f}MB"
        else:
            return f"{size_bytes/(1024**3):.1f}GB"
    
    def _generate_quality_report(self):
        """生成质量分析报告"""
        print("\n📊 电视目录质量分析报告")
        print("=" * 60)
        
        # 统计各类问题
        total_issues = sum(len(issues) for issues in self.quality_issues.values())
        
        if total_issues == 0:
            print("✅ 未发现明显的质量问题")
            return
        
        print(f"\n⚠️ 发现 {total_issues} 个潜在质量问题:")
        
        # 评分过低的内容
        if self.quality_issues['low_rating']:
            print(f"\n📉 评分过低 ({len(self.quality_issues['low_rating'])}个):")
            for item in sorted(self.quality_issues['low_rating'], key=lambda x: x['rating']):
                print(f"  - {item['name']} ({item['rating']}分, {self._format_size(item['size'])})")
        
        # 异常大小的内容
        if self.quality_issues['oversized']:
            print(f"\n📦 异常大小 ({len(self.quality_issues['oversized'])}个):")
            for item in sorted(self.quality_issues['oversized'], key=lambda x: x['size'], reverse=True):
                rating_str = f"{item['rating']}分" if item['rating'] else "无评分"
                print(f"  - {item['name']} ({self._format_size(item['size'])}, {rating_str})")
        
        # 低质量标识
        if self.quality_issues['low_quality_indicators']:
            print(f"\n🔍 低质量标识 ({len(self.quality_issues['low_quality_indicators'])}个):")
            for item in self.quality_issues['low_quality_indicators']:
                rating_str = f"{item['rating']}分" if item['rating'] else "无评分"
                print(f"  - {item['name']} ({rating_str}, {self._format_size(item['size'])})")
                print(f"    问题: {item['issue']}")
        
        # 可疑命名
        if self.quality_issues['suspicious_naming']:
            print(f"\n❓ 可疑命名 ({len(self.quality_issues['suspicious_naming'])}个):")
            for item in self.quality_issues['suspicious_naming']:
                rating_str = f"{item['rating']}分" if item['rating'] else "无评分"
                print(f"  - {item['name']} ({rating_str})")
        
        # 无评分内容统计
        if self.quality_issues['no_rating']:
            print(f"\n📋 无评分内容 ({len(self.quality_issues['no_rating'])}个):")
            print(f"  建议使用评分系统为这些内容添加评分")
        
        # 质量建议
        print("\n💡 质量改进建议:")
        
        if self.quality_issues['low_rating']:
            print("  📉 评分过低内容:")
            print("    - 考虑删除评分低于7.0的内容以节省空间")
            print("    - 重新评估评分标准，确保评分准确性")
        
        if self.quality_issues['oversized']:
            print("  📦 异常大小内容:")
            print("    - 检查是否包含不必要的额外内容")
            print("    - 考虑压缩或重新编码以减小文件大小")
        
        if self.quality_issues['low_quality_indicators']:
            print("  🔍 低质量标识内容:")
            print("    - 检查是否为低质量版本")
            print("    - 考虑寻找更高质量的替代版本")
        
        if self.quality_issues['no_rating']:
            print("  📋 无评分内容:")
            print("    - 运行评分系统为这些内容添加评分")
            print("    - 优先处理知名度高的内容")
        
        # 保存详细报告
        self._save_quality_report()
    
    def _save_quality_report(self):
        """保存质量分析报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"quality_analysis_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"电视目录质量分析报告\n")
            f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"目标目录: {self.target_dir}\n")
            f.write("=" * 60 + "\n\n")
            
            for category, items in self.quality_issues.items():
                if items:
                    f.write(f"{category.upper()} ({len(items)}个):\n")
                    for item in items:
                        f.write(f"  - {item['name']}\n")
                        if 'issue' in item:
                            f.write(f"    问题: {item['issue']}\n")
                        if 'rating' in item and item['rating']:
                            f.write(f"    评分: {item['rating']}分\n")
                        f.write(f"    大小: {self._format_size(item['size'])}\n")
                    f.write("\n")
        
        print(f"\n💾 详细报告已保存: {report_file}")

def main():
    # 默认分析电视目录
    tv_dir = "/Volumes/video/电视"
    
    if not os.path.exists(tv_dir):
        print(f"❌ 目录不存在: {tv_dir}")
        return
    
    analyzer = TVQualityAnalyzer(tv_dir)
    quality_issues = analyzer.analyze_quality()
    
    print("\n✅ 质量分析完成！")
    print("\n📋 后续建议:")
    print("1. 查看生成的详细报告文件")
    print("2. 优先处理评分过低的内容")
    print("3. 检查异常大小的文件夹")
    print("4. 为无评分内容添加评分")
    print("5. 考虑删除或替换低质量内容")

if __name__ == "__main__":
    main()