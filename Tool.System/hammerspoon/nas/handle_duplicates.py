#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理重复文件夹的专用脚本
"""

import os
import shutil
import re

def get_folder_size(folder_path):
    """获取文件夹大小（GB）"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
    except Exception as e:
        print(f"计算大小时出错: {e}")
    return total_size / (1024*1024*1024)  # 转换为GB

def normalize_for_comparison(name):
    """标准化名称用于比较"""
    # 移除评分信息
    normalized = re.sub(r'\s*\[[^\]]*\]', '', name)
    normalized = re.sub(r'\s*\([^\)]*\)', '', normalized)
    
    # 转换为小写
    normalized = normalized.lower()
    
    # 移除常见分隔符
    normalized = re.sub(r'[.\-_\s]+', ' ', normalized)
    
    # 移除技术参数
    tech_patterns = [
        r'webdl', r'bluray', r'web', r'dl', r'complete', r'collection',
        r'全集', r'合集', r'系列', r'series'
    ]
    
    for pattern in tech_patterns:
        normalized = re.sub(pattern, ' ', normalized, flags=re.IGNORECASE)
    
    # 清理空格
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def find_manual_duplicates(animation_path):
    """手动查找重复文件夹"""
    folders = []
    for item in os.listdir(animation_path):
        item_path = os.path.join(animation_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
    
    # 手动定义已知的重复组
    known_duplicates = [
        # 哈利波特系列
        ['哈利波特', 'harry potter'],
        # 可以添加更多已知重复
    ]
    
    duplicates = []
    
    for duplicate_keywords in known_duplicates:
        matching_folders = []
        for folder in folders:
            normalized = normalize_for_comparison(folder)
            for keyword in duplicate_keywords:
                if keyword.lower() in normalized:
                    matching_folders.append(folder)
                    break
        
        if len(matching_folders) > 1:
            duplicates.append(matching_folders)
    
    return duplicates

def handle_duplicates_manual(animation_path):
    """手动处理重复文件夹"""
    print(f"检查重复文件夹: {animation_path}")
    print("="*60)
    
    duplicates = find_manual_duplicates(animation_path)
    
    if not duplicates:
        print("未发现重复文件夹")
        return
    
    for i, duplicate_group in enumerate(duplicates):
        print(f"\n重复组 {i+1}:")
        folder_info = []
        
        for j, folder in enumerate(duplicate_group):
            folder_path = os.path.join(animation_path, folder)
            size = get_folder_size(folder_path)
            folder_info.append((folder, size, folder_path))
            print(f"  {j+1}. {folder} ({size:.2f} GB)")
        
        # 自动选择保留最大的文件夹
        folder_info.sort(key=lambda x: x[1], reverse=True)
        keep_folder = folder_info[0]
        
        print(f"\n保留最大的文件夹: {keep_folder[0]} ({keep_folder[1]:.2f} GB)")
        
        # 删除其他文件夹
        for folder_name, size, folder_path in folder_info[1:]:
            print(f"删除: {folder_name} ({size:.2f} GB)")
            try:
                shutil.rmtree(folder_path)
                print(f"✅ 已删除: {folder_name}")
            except Exception as e:
                print(f"❌ 删除失败: {folder_name} - {e}")
    
    print("\n" + "="*60)
    print("重复文件夹处理完成！")

if __name__ == "__main__":
    animation_path = "/Volumes/video/动画"
    
    if os.path.exists(animation_path):
        handle_duplicates_manual(animation_path)
    else:
        print(f"错误: 目录不存在 - {animation_path}")