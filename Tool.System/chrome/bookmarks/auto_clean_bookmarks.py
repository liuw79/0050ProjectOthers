#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome书签自动清理工具
自动移除重复书签，保留最新的版本
"""

import json
import os
import shutil
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

def extract_bookmarks_with_parent(node, bookmarks_list=None, path="", parent_node=None, parent_index=None):
    """递归提取所有书签，包含父节点信息"""
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
            'parent_node': parent_node,
            'parent_index': parent_index,
            'node': node
        }
        bookmarks_list.append(bookmark)
    
    elif node.get('type') == 'folder':
        # 这是一个文件夹，递归处理子项
        folder_name = node.get('name', '')
        new_path = f"{path}/{folder_name}" if path else folder_name
        
        children = node.get('children', [])
        for i, child in enumerate(children):
            extract_bookmarks_with_parent(child, bookmarks_list, new_path, node, i)
    
    return bookmarks_list

def find_duplicates(bookmarks):
    """查找重复书签"""
    url_groups = defaultdict(list)
    
    # 按URL分组
    for bookmark in bookmarks:
        url = bookmark['url'].strip().lower()
        if url:
            url_groups[url].append(bookmark)
    
    # 找出重复项
    duplicate_groups = []
    for url, group in url_groups.items():
        if len(group) > 1:
            duplicate_groups.append({
                'type': 'url_duplicate',
                'key': url,
                'bookmarks': group,
                'count': len(group)
            })
    
    return duplicate_groups

def remove_duplicates(data, duplicate_groups):
    """移除重复书签，保留最新的"""
    removed_count = 0
    removal_log = []
    
    for group in duplicate_groups:
        bookmarks = group['bookmarks']
        if len(bookmarks) <= 1:
            continue
        
        # 按添加时间排序，保留最新的
        bookmarks.sort(key=lambda x: int(x['date_added']) if x['date_added'].isdigit() else 0, reverse=True)
        
        # 保留第一个（最新的），删除其余的
        keep_bookmark = bookmarks[0]
        to_remove = bookmarks[1:]
        
        print(f"🔍 处理重复组: {group['key'][:50]}...")
        print(f"   保留: {keep_bookmark['name']} (路径: {keep_bookmark['path']})")
        
        for bookmark in to_remove:
            if remove_bookmark_from_parent(bookmark):
                removed_count += 1
                removal_log.append({
                    'name': bookmark['name'],
                    'url': bookmark['url'],
                    'path': bookmark['path'],
                    'date_added': bookmark['date_added']
                })
                print(f"   删除: {bookmark['name']} (路径: {bookmark['path']})")
    
    return removed_count, removal_log

def remove_bookmark_from_parent(bookmark):
    """从父节点中移除指定书签"""
    try:
        parent_node = bookmark['parent_node']
        parent_index = bookmark['parent_index']
        
        if parent_node and 'children' in parent_node and parent_index is not None:
            children = parent_node['children']
            if parent_index < len(children) and children[parent_index] == bookmark['node']:
                children.pop(parent_index)
                
                # 更新后续书签的索引
                for i in range(parent_index, len(children)):
                    # 这里需要更新其他书签的parent_index，但由于我们是一次性处理，
                    # 而且按照从后往前的顺序删除，所以暂时不需要更新
                    pass
                
                return True
    except Exception as e:
        print(f"⚠️  删除书签时出错: {e}")
    
    return False

def save_cleaned_bookmarks(data, suffix="cleaned"):
    """保存清理后的书签"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned_file = f"Bookmarks_{suffix}_{timestamp}.json"
    
    try:
        with open(cleaned_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 清理后的书签已保存: {cleaned_file}")
        return cleaned_file
    except Exception as e:
        print(f"❌ 保存清理后书签失败: {e}")
        return None

def backup_original(bookmarks_path):
    """备份原始书签文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"Bookmarks_backup_{timestamp}.json"
    
    try:
        shutil.copy2(bookmarks_path, backup_file)
        print(f"✅ 原始书签已备份: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return None

def save_removal_log(removal_log):
    """保存删除日志"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"removal_log_{timestamp}.txt"
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Chrome书签清理日志\n")
            f.write("=" * 40 + "\n")
            f.write(f"清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"删除书签数: {len(removal_log)}\n")
            f.write("\n" + "=" * 40 + "\n\n")
            
            for i, item in enumerate(removal_log, 1):
                f.write(f"{i}. 标题: {item['name']}\n")
                f.write(f"   URL: {item['url']}\n")
                f.write(f"   路径: {item['path']}\n")
                f.write(f"   添加时间: {item['date_added']}\n")
                f.write("\n")
        
        print(f"📝 删除日志已保存: {log_file}")
        return log_file
    except Exception as e:
        print(f"❌ 保存删除日志失败: {e}")
        return None

def main():
    """主函数"""
    print("🧹 Chrome书签自动清理工具")
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
        extract_bookmarks_with_parent(root_node, all_bookmarks, root_name)
    
    total_bookmarks = len(all_bookmarks)
    print(f"📊 总共找到 {total_bookmarks} 个书签")
    
    # 查找重复项
    print(f"🔍 正在分析重复书签...")
    duplicate_groups = find_duplicates(all_bookmarks)
    
    if not duplicate_groups:
        print(f"✅ 没有发现重复书签，无需清理")
        return
    
    duplicate_count = sum(group['count'] - 1 for group in duplicate_groups)
    print(f"🔍 发现 {len(duplicate_groups)} 组重复书签，共 {duplicate_count} 个重复项")
    
    # 创建备份
    print(f"💾 正在创建备份...")
    backup_file = backup_original(bookmarks_path)
    if not backup_file:
        print("❌ 无法创建备份，停止清理操作")
        return
    
    # 移除重复项
    print(f"🧹 开始清理重复书签...")
    removed_count, removal_log = remove_duplicates(data, duplicate_groups)
    
    if removed_count > 0:
        print(f"✅ 成功移除 {removed_count} 个重复书签")
        
        # 保存清理后的书签
        cleaned_file = save_cleaned_bookmarks(data)
        
        # 保存删除日志
        log_file = save_removal_log(removal_log)
        
        # 询问是否应用到Chrome
        print(f"\n📋 清理完成!")
        print(f"备份文件: {backup_file}")
        print(f"清理后文件: {cleaned_file}")
        print(f"删除日志: {log_file}")
        
        print(f"\n⚠️  注意: 清理后的文件已生成，但尚未应用到Chrome")
        print(f"如需应用，请:")
        print(f"1. 关闭Chrome浏览器")
        print(f"2. 运行: cp '{cleaned_file}' '{bookmarks_path}'")
        print(f"3. 重新启动Chrome")
        
    else:
        print(f"⚠️  没有成功移除任何书签")

if __name__ == "__main__":
    main()