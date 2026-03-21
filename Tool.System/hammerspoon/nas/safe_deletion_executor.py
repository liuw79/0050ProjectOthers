#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全删除执行器
基于智能分析结果，安全地删除可以自动删除的项目
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class SafeDeletionExecutor:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.deletion_log = []
        self.backup_dir = self.target_dir / "_deletion_backup"
        
    def execute_safe_deletions(self, dry_run=True):
        """执行安全删除操作"""
        print(f"🔍 开始安全删除分析: {self.target_dir}")
        print(f"{'🧪 模拟模式' if dry_run else '🚨 实际删除模式'}")
        print("=" * 60)
        
        # 查找可以安全删除的项目
        safe_deletions = self._find_safe_deletions()
        
        if not safe_deletions:
            print("✅ 没有发现可以安全删除的项目")
            return
        
        print(f"\n📋 发现 {len(safe_deletions)} 个可安全删除的项目:")
        
        total_size = 0
        for item in safe_deletions:
            size_str = self._format_size(item['size'])
            total_size += item['size']
            print(f"  - {item['name']} ({size_str}) - {item['reason']}")
        
        print(f"\n💾 总计可释放空间: {self._format_size(total_size)}")
        
        if dry_run:
            print("\n🧪 这是模拟运行，没有实际删除任何文件")
            print("💡 如需实际执行删除，请运行: python3 safe_deletion_executor.py --execute")
            return
        
        # 实际执行删除
        self._execute_deletions(safe_deletions)
    
    def _find_safe_deletions(self):
        """查找可以安全删除的项目"""
        safe_deletions = []
        
        for item in self.target_dir.iterdir():
            if item.is_dir():
                # 检查是否为空文件夹
                if self._is_empty_folder(item):
                    safe_deletions.append({
                        'path': item,
                        'name': item.name,
                        'type': 'empty_folder',
                        'reason': '空文件夹',
                        'size': 0
                    })
                    continue
                
                # 检查是否为过小且无视频内容的文件夹
                folder_size = self._get_folder_size(item)
                video_count = self._count_video_files(item)
                
                if folder_size < 100 * 1024 * 1024 and video_count == 0:  # 小于100MB且无视频
                    safe_deletions.append({
                        'path': item,
                        'name': item.name,
                        'type': 'small_no_video',
                        'reason': f'过小文件夹({self._format_size(folder_size)})且无视频内容',
                        'size': folder_size
                    })
            
            elif item.is_file():
                # 检查元数据文件
                if self._is_metadata_file(item):
                    file_size = item.stat().st_size
                    safe_deletions.append({
                        'path': item,
                        'name': item.name,
                        'type': 'metadata_file',
                        'reason': '元数据文件',
                        'size': file_size
                    })
        
        return safe_deletions
    
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
    
    def _is_metadata_file(self, file_path):
        """检查是否为元数据文件"""
        metadata_patterns = [
            '.nfo', '.xml', '.txt', '.DS_Store', 'Thumbs.db',
            '-thumb.jpg', '-poster.jpg'
        ]
        
        file_name = file_path.name.lower()
        return any(pattern.lower() in file_name for pattern in metadata_patterns)
    
    def _execute_deletions(self, deletions):
        """执行实际删除操作"""
        print(f"\n🚨 开始执行删除操作...")
        
        # 创建备份目录
        if not self.backup_dir.exists():
            self.backup_dir.mkdir()
        
        success_count = 0
        error_count = 0
        
        for item in deletions:
            try:
                item_path = item['path']
                
                # 记录删除日志
                self.deletion_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'path': str(item_path),
                    'type': item['type'],
                    'reason': item['reason'],
                    'size': item['size']
                })
                
                # 执行删除
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"✅ 已删除文件夹: {item_path.name}")
                else:
                    item_path.unlink()
                    print(f"✅ 已删除文件: {item_path.name}")
                
                success_count += 1
                
            except Exception as e:
                print(f"❌ 删除失败: {item_path.name} - {str(e)}")
                error_count += 1
        
        # 保存删除日志
        self._save_deletion_log()
        
        print(f"\n📊 删除操作完成:")
        print(f"  ✅ 成功删除: {success_count} 个项目")
        print(f"  ❌ 删除失败: {error_count} 个项目")
        
        if success_count > 0:
            total_freed = sum(item['size'] for item in deletions[:success_count])
            print(f"  💾 释放空间: {self._format_size(total_freed)}")
    
    def _save_deletion_log(self):
        """保存删除日志"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.target_dir / f"deletion_log_{timestamp}.json"
        
        log_data = {
            'deletion_time': datetime.now().isoformat(),
            'target_directory': str(self.target_dir),
            'deleted_items': self.deletion_log
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 删除日志已保存: {log_file}")
    
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

def main():
    import sys
    
    # 默认电视目录
    tv_dir = "/Volumes/video/电视"
    
    if not os.path.exists(tv_dir):
        print(f"❌ 目录不存在: {tv_dir}")
        return
    
    # 检查是否为实际执行模式
    execute_mode = '--execute' in sys.argv
    
    executor = SafeDeletionExecutor(tv_dir)
    executor.execute_safe_deletions(dry_run=not execute_mode)
    
    if not execute_mode:
        print("\n⚠️ 重要提醒:")
        print("1. 这是安全的模拟运行，没有实际删除任何文件")
        print("2. 请仔细检查上述列表，确认可以删除")
        print("3. 如确认无误，请运行: python3 safe_deletion_executor.py --execute")
        print("4. 删除操作将生成详细日志文件")

if __name__ == "__main__":
    main()