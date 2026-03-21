#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome书签重复清理工具
功能：
1. 分析Chrome书签文件
2. 检测重复书签（基于URL和标题）
3. 生成清理报告
4. 安全地移除重复书签
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse
import shutil

class ChromeBookmarkCleaner:
    def __init__(self, bookmarks_path=None):
        if bookmarks_path is None:
            # 默认Chrome书签路径
            home = os.path.expanduser("~")
            self.bookmarks_path = os.path.join(
                home, "Library/Application Support/Google/Chrome/Default/Bookmarks"
            )
        else:
            self.bookmarks_path = bookmarks_path
        
        self.duplicates = []
        self.stats = {
            'total_bookmarks': 0,
            'duplicate_groups': 0,
            'duplicates_found': 0,
            'duplicates_removed': 0
        }
    
    def load_bookmarks(self):
        """加载Chrome书签文件"""
        try:
            with open(self.bookmarks_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 无法读取书签文件: {e}")
            return None
    
    def extract_bookmarks(self, node, bookmarks_list=None, path=""):
        """递归提取所有书签"""
        if bookmarks_list is None:
            bookmarks_list = []
        
        if node.get('type') == 'url':
            # 这是一个书签
            bookmark = {
                'name': node.get('name', ''),
                'url': node.get('url', ''),
                'path': path,
                'date_added': node.get('date_added', ''),
                'id': node.get('id', ''),
                'node': node  # 保存原始节点引用
            }
            bookmarks_list.append(bookmark)
            self.stats['total_bookmarks'] += 1
        
        elif node.get('type') == 'folder':
            # 这是一个文件夹，递归处理子项
            folder_name = node.get('name', '')
            new_path = f"{path}/{folder_name}" if path else folder_name
            
            for child in node.get('children', []):
                self.extract_bookmarks(child, bookmarks_list, new_path)
        
        return bookmarks_list
    
    def find_duplicates(self, bookmarks):
        """查找重复书签"""
        url_groups = defaultdict(list)
        title_url_groups = defaultdict(list)
        
        # 按URL分组
        for bookmark in bookmarks:
            url = bookmark['url'].strip().lower()
            if url:
                url_groups[url].append(bookmark)
        
        # 按标题+URL分组（更严格的重复检测）
        for bookmark in bookmarks:
            key = f"{bookmark['name'].strip().lower()}|{bookmark['url'].strip().lower()}"
            if key:
                title_url_groups[key].append(bookmark)
        
        # 找出重复项
        duplicate_groups = []
        
        # URL重复
        for url, group in url_groups.items():
            if len(group) > 1:
                duplicate_groups.append({
                    'type': 'url_duplicate',
                    'key': url,
                    'bookmarks': group,
                    'count': len(group)
                })
        
        # 标题+URL完全重复
        for key, group in title_url_groups.items():
            if len(group) > 1:
                # 检查是否已经在URL重复中
                url = key.split('|')[1]
                if not any(d['key'] == url and d['type'] == 'url_duplicate' for d in duplicate_groups):
                    duplicate_groups.append({
                        'type': 'exact_duplicate',
                        'key': key,
                        'bookmarks': group,
                        'count': len(group)
                    })
        
        self.stats['duplicate_groups'] = len(duplicate_groups)
        self.stats['duplicates_found'] = sum(group['count'] - 1 for group in duplicate_groups)
        
        return duplicate_groups
    
    def generate_report(self, duplicate_groups):
        """生成重复书签报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"duplicate_bookmarks_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Chrome书签重复检测报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"书签文件: {self.bookmarks_path}\n")
            f.write(f"总书签数: {self.stats['total_bookmarks']}\n")
            f.write(f"重复组数: {self.stats['duplicate_groups']}\n")
            f.write(f"重复书签数: {self.stats['duplicates_found']}\n")
            f.write("\n" + "=" * 50 + "\n\n")
            
            for i, group in enumerate(duplicate_groups, 1):
                f.write(f"重复组 {i}: {group['type']}\n")
                f.write(f"重复数量: {group['count']}\n")
                f.write(f"识别键: {group['key']}\n")
                f.write("-" * 30 + "\n")
                
                for j, bookmark in enumerate(group['bookmarks']):
                    f.write(f"  [{j+1}] 标题: {bookmark['name']}\n")
                    f.write(f"      URL: {bookmark['url']}\n")
                    f.write(f"      路径: {bookmark['path']}\n")
                    f.write(f"      添加时间: {bookmark['date_added']}\n")
                    f.write("\n")
                
                f.write("\n")
        
        print(f"📊 重复书签报告已生成: {report_file}")
        return report_file
    
    def remove_duplicates(self, data, duplicate_groups, keep_strategy='newest'):
        """移除重复书签"""
        removed_count = 0
        
        for group in duplicate_groups:
            bookmarks = group['bookmarks']
            if len(bookmarks) <= 1:
                continue
            
            # 选择保留策略
            if keep_strategy == 'newest':
                # 保留最新添加的
                bookmarks.sort(key=lambda x: int(x['date_added']) if x['date_added'].isdigit() else 0, reverse=True)
            elif keep_strategy == 'oldest':
                # 保留最早添加的
                bookmarks.sort(key=lambda x: int(x['date_added']) if x['date_added'].isdigit() else 0)
            elif keep_strategy == 'first':
                # 保留第一个（按发现顺序）
                pass
            
            # 保留第一个，删除其余的
            to_remove = bookmarks[1:]
            
            for bookmark in to_remove:
                if self.remove_bookmark_from_data(data, bookmark):
                    removed_count += 1
        
        self.stats['duplicates_removed'] = removed_count
        return removed_count
    
    def remove_bookmark_from_data(self, data, bookmark_to_remove):
        """从数据结构中移除指定书签"""
        def remove_from_node(node):
            if 'children' in node:
                children = node['children']
                for i, child in enumerate(children):
                    if (child.get('type') == 'url' and 
                        child.get('url') == bookmark_to_remove['url'] and
                        child.get('name') == bookmark_to_remove['name']):
                        children.pop(i)
                        return True
                    elif child.get('type') == 'folder':
                        if remove_from_node(child):
                            return True
            return False
        
        # 在所有根节点中查找并移除
        for root_name, root_node in data['roots'].items():
            if remove_from_node(root_node):
                return True
        
        return False
    
    def save_cleaned_bookmarks(self, data):
        """保存清理后的书签"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cleaned_file = f"Bookmarks_cleaned_{timestamp}.json"
        
        try:
            with open(cleaned_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ 清理后的书签已保存: {cleaned_file}")
            return cleaned_file
        except Exception as e:
            print(f"❌ 保存清理后书签失败: {e}")
            return None
    
    def backup_original(self):
        """备份原始书签文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"Bookmarks_backup_{timestamp}.json"
        
        try:
            shutil.copy2(self.bookmarks_path, backup_file)
            print(f"✅ 原始书签已备份: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return None
    
    def apply_cleaned_bookmarks(self, cleaned_file):
        """应用清理后的书签到Chrome"""
        try:
            # 再次备份当前书签
            backup_file = self.backup_original()
            if not backup_file:
                print("❌ 无法创建备份，取消应用操作")
                return False
            
            # 复制清理后的文件到Chrome书签位置
            shutil.copy2(cleaned_file, self.bookmarks_path)
            print("✅ 清理后的书签已应用到Chrome")
            print("⚠️  请重启Chrome浏览器以查看更改")
            return True
        except Exception as e:
            print(f"❌ 应用清理后书签失败: {e}")
            return False
    
    def run_analysis(self):
        """运行完整的分析流程"""
        print("🔍 开始分析Chrome书签...")
        
        # 加载书签
        data = self.load_bookmarks()
        if not data:
            return None
        
        print(f"📚 书签文件加载成功")
        
        # 提取所有书签
        all_bookmarks = []
        for root_name, root_node in data['roots'].items():
            self.extract_bookmarks(root_node, all_bookmarks, root_name)
        
        print(f"📊 总共找到 {self.stats['total_bookmarks']} 个书签")
        
        # 查找重复项
        duplicate_groups = self.find_duplicates(all_bookmarks)
        
        if duplicate_groups:
            print(f"🔍 发现 {self.stats['duplicate_groups']} 组重复书签")
            print(f"📝 总共 {self.stats['duplicates_found']} 个重复书签")
            
            # 生成报告
            report_file = self.generate_report(duplicate_groups)
            
            return {
                'data': data,
                'duplicate_groups': duplicate_groups,
                'report_file': report_file,
                'stats': self.stats
            }
        else:
            print("✅ 没有发现重复书签")
            return {
                'data': data,
                'duplicate_groups': [],
                'report_file': None,
                'stats': self.stats
            }
    
    def run_cleanup(self, keep_strategy='newest', apply_to_chrome=False):
        """运行完整的清理流程"""
        # 先运行分析
        result = self.run_analysis()
        if not result or not result['duplicate_groups']:
            return result
        
        print(f"\n🧹 开始清理重复书签...")
        print(f"📋 保留策略: {keep_strategy}")
        
        # 移除重复项
        removed_count = self.remove_duplicates(
            result['data'], 
            result['duplicate_groups'], 
            keep_strategy
        )
        
        if removed_count > 0:
            print(f"✅ 已移除 {removed_count} 个重复书签")
            
            # 保存清理后的书签
            cleaned_file = self.save_cleaned_bookmarks(result['data'])
            
            if cleaned_file and apply_to_chrome:
                # 应用到Chrome
                self.apply_cleaned_bookmarks(cleaned_file)
            
            result['cleaned_file'] = cleaned_file
            result['removed_count'] = removed_count
        else:
            print("⚠️  没有移除任何书签")
        
        return result

def main():
    """主函数"""
    print("Chrome书签重复清理工具")
    print("=" * 30)
    
    cleaner = ChromeBookmarkCleaner()
    
    # 检查书签文件是否存在
    if not os.path.exists(cleaner.bookmarks_path):
        print(f"❌ 找不到Chrome书签文件: {cleaner.bookmarks_path}")
        print("请确保Chrome已安装并至少运行过一次")
        return
    
    print("选择操作模式:")
    print("1. 仅分析重复书签（不修改）")
    print("2. 分析并清理重复书签（生成清理后文件）")
    print("3. 分析、清理并应用到Chrome（⚠️ 会修改Chrome书签）")
    
    try:
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1':
            # 仅分析
            result = cleaner.run_analysis()
            
        elif choice == '2':
            # 分析并清理
            print("\n选择保留策略:")
            print("1. 保留最新添加的书签")
            print("2. 保留最早添加的书签")
            print("3. 保留第一个发现的书签")
            
            strategy_choice = input("请选择 (1-3): ").strip()
            strategy_map = {'1': 'newest', '2': 'oldest', '3': 'first'}
            strategy = strategy_map.get(strategy_choice, 'newest')
            
            result = cleaner.run_cleanup(keep_strategy=strategy, apply_to_chrome=False)
            
        elif choice == '3':
            # 分析、清理并应用
            print("⚠️  警告: 此操作将直接修改Chrome书签文件")
            print("建议先关闭Chrome浏览器")
            confirm = input("确认继续? (y/N): ").strip().lower()
            
            if confirm == 'y':
                print("\n选择保留策略:")
                print("1. 保留最新添加的书签")
                print("2. 保留最早添加的书签")
                print("3. 保留第一个发现的书签")
                
                strategy_choice = input("请选择 (1-3): ").strip()
                strategy_map = {'1': 'newest', '2': 'oldest', '3': 'first'}
                strategy = strategy_map.get(strategy_choice, 'newest')
                
                result = cleaner.run_cleanup(keep_strategy=strategy, apply_to_chrome=True)
            else:
                print("操作已取消")
                return
        else:
            print("无效选择")
            return
        
        # 显示最终统计
        if result:
            print(f"\n📊 最终统计:")
            print(f"总书签数: {result['stats']['total_bookmarks']}")
            print(f"重复组数: {result['stats']['duplicate_groups']}")
            print(f"发现重复: {result['stats']['duplicates_found']}")
            if 'removed_count' in result:
                print(f"已移除: {result['removed_count']}")
    
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()