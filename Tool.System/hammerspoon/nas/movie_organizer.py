#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电影目录整理工具
实施电影目录全面排查后的整理计划
"""

import os
import sys
import shutil
import re
import json
from datetime import datetime
from pathlib import Path
import logging

class MovieOrganizer:
    def __init__(self, movie_base_path):
        self.movie_base_path = Path(movie_base_path)
        self.setup_logging()
        self.stats = {
            'processed': 0,
            'renamed': 0,
            'moved': 0,
            'errors': 0,
            'collections_organized': 0
        }
        
    def setup_logging(self):
        """设置日志记录"""
        log_dir = Path(__file__).parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'movie_organization_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def check_movie_directory(self):
        """检查电影目录是否存在和可访问"""
        if not self.movie_base_path.exists():
            self.logger.error(f"电影目录不存在: {self.movie_base_path}")
            return False
            
        if not self.movie_base_path.is_dir():
            self.logger.error(f"路径不是目录: {self.movie_base_path}")
            return False
            
        try:
            list(self.movie_base_path.iterdir())
            self.logger.info(f"电影目录检查通过: {self.movie_base_path}")
            return True
        except PermissionError:
            self.logger.error(f"没有访问权限: {self.movie_base_path}")
            return False
            
    def clean_empty_directories(self):
        """清理空目录"""
        self.logger.info("开始清理空目录...")
        empty_dirs = []
        
        for root, dirs, files in os.walk(self.movie_base_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):
                        empty_dirs.append(dir_path)
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"无法检查目录 {dir_path}: {e}")
                    
        for empty_dir in empty_dirs:
            try:
                empty_dir.rmdir()
                self.logger.info(f"删除空目录: {empty_dir}")
            except OSError as e:
                self.logger.warning(f"无法删除空目录 {empty_dir}: {e}")
                
        return len(empty_dirs)
        
    def organize_collections(self):
        """整理合集目录"""
        self.logger.info("开始整理合集目录...")
        collections_dir = self.movie_base_path / "[合集]"
        collections_dir.mkdir(exist_ok=True)
        
        collection_patterns = [
            r'.*合集.*',
            r'.*系列.*',
            r'.*collection.*',
            r'.*trilogy.*',
            r'.*saga.*'
        ]
        
        moved_collections = 0
        
        for item in self.movie_base_path.iterdir():
            if item.is_dir() and item.name != "[合集]":
                for pattern in collection_patterns:
                    if re.search(pattern, item.name, re.IGNORECASE):
                        target_path = collections_dir / item.name
                        if not target_path.exists():
                            try:
                                shutil.move(str(item), str(target_path))
                                self.logger.info(f"移动合集: {item.name} -> [合集]/{item.name}")
                                moved_collections += 1
                                self.stats['moved'] += 1
                            except OSError as e:
                                self.logger.error(f"移动合集失败 {item.name}: {e}")
                                self.stats['errors'] += 1
                        break
                        
        self.stats['collections_organized'] = moved_collections
        return moved_collections
        
    def standardize_naming(self):
        """标准化命名"""
        self.logger.info("开始标准化命名...")
        renamed_count = 0
        
        # 定义命名规范化规则
        naming_rules = [
            # 移除多余的空格
            (r'\s+', ' '),
            # 标准化年份格式
            (r'\((\d{4})\)', r'(\1)'),
            # 移除多余的点号
            (r'\.{2,}', '.'),
            # 标准化分辨率标记
            (r'\b(4K|2160p)\b', '4K'),
            (r'\b1080p\b', '1080p'),
            (r'\b720p\b', '720p'),
        ]
        
        for item in self.movie_base_path.iterdir():
            if item.is_dir():
                original_name = item.name
                new_name = original_name
                
                # 应用命名规则
                for pattern, replacement in naming_rules:
                    new_name = re.sub(pattern, replacement, new_name)
                    
                # 清理首尾空格
                new_name = new_name.strip()
                
                if new_name != original_name and new_name:
                    new_path = item.parent / new_name
                    if not new_path.exists():
                        try:
                            item.rename(new_path)
                            self.logger.info(f"重命名: {original_name} -> {new_name}")
                            renamed_count += 1
                            self.stats['renamed'] += 1
                        except OSError as e:
                            self.logger.error(f"重命名失败 {original_name}: {e}")
                            self.stats['errors'] += 1
                            
        return renamed_count
        
    def organize_by_decade(self):
        """按年代整理电影"""
        self.logger.info("开始按年代整理电影...")
        
        # 创建年代目录
        decades = ['1990s', '2000s', '2010s', '2020s']
        for decade in decades:
            decade_dir = self.movie_base_path / f"[{decade}]"
            decade_dir.mkdir(exist_ok=True)
            
        year_pattern = r'\((\d{4})\)'
        organized_count = 0
        
        for item in self.movie_base_path.iterdir():
            if item.is_dir() and not item.name.startswith('['):
                match = re.search(year_pattern, item.name)
                if match:
                    year = int(match.group(1))
                    decade = None
                    
                    if 1990 <= year <= 1999:
                        decade = '1990s'
                    elif 2000 <= year <= 2009:
                        decade = '2000s'
                    elif 2010 <= year <= 2019:
                        decade = '2010s'
                    elif 2020 <= year <= 2029:
                        decade = '2020s'
                        
                    if decade:
                        decade_dir = self.movie_base_path / f"[{decade}]"
                        target_path = decade_dir / item.name
                        
                        if not target_path.exists():
                            try:
                                shutil.move(str(item), str(target_path))
                                self.logger.info(f"移动到年代目录: {item.name} -> [{decade}]/{item.name}")
                                organized_count += 1
                                self.stats['moved'] += 1
                            except OSError as e:
                                self.logger.error(f"移动到年代目录失败 {item.name}: {e}")
                                self.stats['errors'] += 1
                                
        return organized_count
        
    def generate_report(self):
        """生成整理报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = {
            'timestamp': timestamp,
            'movie_base_path': str(self.movie_base_path),
            'statistics': self.stats,
            'summary': {
                'total_operations': sum(self.stats.values()) - self.stats['errors'],
                'success_rate': f"{((sum(self.stats.values()) - self.stats['errors']) / max(sum(self.stats.values()), 1) * 100):.1f}%"
            }
        }
        
        # 保存JSON报告
        report_file = Path(__file__).parent / f'movie_organization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"整理报告已保存: {report_file}")
        return report
        
    def run_full_organization(self):
        """执行完整的电影目录整理"""
        self.logger.info("开始电影目录完整整理...")
        
        if not self.check_movie_directory():
            return False
            
        try:
            # 第一阶段：清理和预处理
            self.logger.info("=== 第一阶段：清理和预处理 ===")
            empty_dirs_cleaned = self.clean_empty_directories()
            self.logger.info(f"清理了 {empty_dirs_cleaned} 个空目录")
            
            # 第二阶段：命名标准化
            self.logger.info("=== 第二阶段：命名标准化 ===")
            renamed_count = self.standardize_naming()
            self.logger.info(f"重命名了 {renamed_count} 个目录")
            
            # 第三阶段：合集整理
            self.logger.info("=== 第三阶段：合集整理 ===")
            collections_moved = self.organize_collections()
            self.logger.info(f"整理了 {collections_moved} 个合集")
            
            # 第四阶段：年代分类（可选）
            # decade_organized = self.organize_by_decade()
            # self.logger.info(f"按年代整理了 {decade_organized} 部电影")
            
            # 生成报告
            report = self.generate_report()
            self.logger.info("电影目录整理完成！")
            self.logger.info(f"处理统计: {self.stats}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"整理过程中发生错误: {e}")
            return False

def main():
    """主函数"""
    # 默认电影目录路径
    default_movie_path = "/Volumes/video/电影"
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        movie_path = sys.argv[1]
    else:
        movie_path = default_movie_path
        
    print(f"电影目录整理工具")
    print(f"目标目录: {movie_path}")
    print("-" * 50)
    
    organizer = MovieOrganizer(movie_path)
    success = organizer.run_full_organization()
    
    if success:
        print("\n✅ 电影目录整理成功完成！")
        return 0
    else:
        print("\n❌ 电影目录整理失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())