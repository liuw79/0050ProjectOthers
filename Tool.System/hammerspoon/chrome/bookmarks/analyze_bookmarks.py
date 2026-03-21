#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome书签重复分析工具 - 非交互式版本
直接分析并生成报告
"""

import json
import os
from datetime import datetime
from collections import defaultdict

def load_bookmarks(bookmarks_path):
    """加载Chrome书签文件"""
    try:
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 无法读取书签文件: {e}")
        return None

def extract_bookmarks(node, bookmarks_list=None, path=""):
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
            'id': node.get('id', '')
        }
        bookmarks_list.append(bookmark)
    
    elif node.get('type') == 'folder':
        # 这是一个文件夹，递归处理子项
        folder_name = node.get('name', '')
        new_path = f"{path}/{folder_name}" if path else folder_name
        
        for child in node.get('children', []):
            extract_bookmarks(child, bookmarks_list, new_path)
    
    return bookmarks_list

def find_duplicates(bookmarks):
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
    
    return duplicate_groups

def generate_report(duplicate_groups, total_bookmarks, bookmarks_path):
    """生成重复书签报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"duplicate_bookmarks_report_{timestamp}.txt"
    
    duplicate_count = sum(group['count'] - 1 for group in duplicate_groups)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("Chrome书签重复检测报告\n")
        f.write("=" * 50 + "\n")
        f.write(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"书签文件: {bookmarks_path}\n")
        f.write(f"总书签数: {total_bookmarks}\n")
        f.write(f"重复组数: {len(duplicate_groups)}\n")
        f.write(f"重复书签数: {duplicate_count}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        
        if duplicate_groups:
            for i, group in enumerate(duplicate_groups, 1):
                f.write(f"重复组 {i}: {group['type']}\n")
                f.write(f"重复数量: {group['count']}\n")
                if group['type'] == 'url_duplicate':
                    f.write(f"重复URL: {group['key']}\n")
                else:
                    f.write(f"重复标题+URL: {group['key']}\n")
                f.write("-" * 30 + "\n")
                
                for j, bookmark in enumerate(group['bookmarks']):
                    f.write(f"  [{j+1}] 标题: {bookmark['name']}\n")
                    f.write(f"      URL: {bookmark['url']}\n")
                    f.write(f"      路径: {bookmark['path']}\n")
                    f.write(f"      添加时间: {bookmark['date_added']}\n")
                    f.write("\n")
                
                f.write("\n")
        else:
            f.write("✅ 没有发现重复书签\n")
    
    return report_file, duplicate_count

def main():
    """主函数"""
    print("🔍 Chrome书签重复分析工具")
    print("=" * 40)
    
    # Chrome书签路径
    home = os.path.expanduser("~")
    bookmarks_path = os.path.join(
        home, "Library/Application Support/Google/Chrome/Default/Bookmarks"
    )
    
    # 检查书签文件是否存在
    if not os.path.exists(bookmarks_path):
        print(f"❌ 找不到Chrome书签文件: {bookmarks_path}")
        print("请确保Chrome已安装并至少运行过一次")
        return
    
    print(f"📚 正在加载书签文件...")
    
    # 加载书签
    data = load_bookmarks(bookmarks_path)
    if not data:
        return
    
    print(f"✅ 书签文件加载成功")
    
    # 提取所有书签
    all_bookmarks = []
    for root_name, root_node in data['roots'].items():
        extract_bookmarks(root_node, all_bookmarks, root_name)
    
    total_bookmarks = len(all_bookmarks)
    print(f"📊 总共找到 {total_bookmarks} 个书签")
    
    # 查找重复项
    print(f"🔍 正在分析重复书签...")
    duplicate_groups = find_duplicates(all_bookmarks)
    
    # 生成报告
    report_file, duplicate_count = generate_report(duplicate_groups, total_bookmarks, bookmarks_path)
    
    # 显示结果
    print(f"\n📊 分析结果:")
    print(f"总书签数: {total_bookmarks}")
    print(f"重复组数: {len(duplicate_groups)}")
    print(f"重复书签数: {duplicate_count}")
    
    if duplicate_groups:
        print(f"\n🔍 发现重复书签!")
        print(f"📝 详细报告已保存: {report_file}")
        
        # 显示前几个重复组的概要
        print(f"\n📋 重复书签概要 (前5组):")
        for i, group in enumerate(duplicate_groups[:5], 1):
            print(f"  {i}. {group['type']} - {group['count']} 个重复")
            if group['type'] == 'url_duplicate':
                # 显示URL的域名
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(group['key']).netloc
                    print(f"     域名: {domain}")
                except:
                    print(f"     URL: {group['key'][:50]}...")
            
            # 显示书签标题
            titles = [b['name'] for b in group['bookmarks'][:3]]
            print(f"     标题: {', '.join(titles)}")
            if len(group['bookmarks']) > 3:
                print(f"     ... 还有 {len(group['bookmarks']) - 3} 个")
            print()
        
        if len(duplicate_groups) > 5:
            print(f"  ... 还有 {len(duplicate_groups) - 5} 组重复书签")
        
        print(f"\n💡 建议:")
        print(f"1. 查看详细报告: {report_file}")
        print(f"2. 运行完整清理脚本: python3 chrome_bookmark_cleaner.py")
        print(f"3. 或手动在Chrome中删除重复书签")
    else:
        print(f"\n✅ 恭喜! 没有发现重复书签")
        print(f"📝 分析报告已保存: {report_file}")

if __name__ == "__main__":
    main()