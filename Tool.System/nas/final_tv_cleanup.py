#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终清理电视目录中的发布组标识和技术参数
"""

import os
import re
from pathlib import Path

def clean_release_groups_and_tech_params(tv_directory):
    """清理发布组标识和技术参数"""
    tv_path = Path(tv_directory)
    
    print("🧹 开始清理发布组标识和技术参数...")
    
    # 发布组标识列表
    release_groups = [
        'PTHome', 'PTH', 'CHDWEB', 'HHWEB', 'ROCCaT', 'DBTV', 'FLUX', 
        'TOMMY', 'CMCTV', 'QHstudIo', 'cXcY', 'OurTV', 'SDHF.LZ'
    ]
    
    # 技术参数列表
    tech_params = [
        'BluRay', 'Blu.ray', 'x264', 'x265', 'H264', 'H265', 'H.264', 'H.265',
        'DTS', 'AAC', 'DDP5.1', 'Atmos', '1080p', '2160p', '720p', '4K',
        'HDTV', 'WEB-DL', 'WEBRip', 'BDRip', 'DVDRip', 'HEVC', '10bit'
    ]
    
    cleaned_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        new_name = folder_name
        
        # 移除发布组标识
        for group in release_groups:
            # 匹配各种格式：.GROUP、-GROUP、GROUP、[GROUP]等
            patterns = [
                rf'\.{re.escape(group)}(?=\s|\[|$)',
                rf'-{re.escape(group)}(?=\s|\[|$)',
                rf'\s{re.escape(group)}(?=\s|\[|$)',
                rf'\[{re.escape(group)}\]',
                rf'￡{re.escape(group)}'
            ]
            
            for pattern in patterns:
                new_name = re.sub(pattern, '', new_name, flags=re.IGNORECASE)
        
        # 移除技术参数
        for param in tech_params:
            patterns = [
                rf'\.{re.escape(param)}(?=\.|\s|\[|$)',
                rf'-{re.escape(param)}(?=\.|\s|\[|$)',
                rf'\s{re.escape(param)}(?=\.|\s|\[|$)',
                rf'\[{re.escape(param)}\]'
            ]
            
            for pattern in patterns:
                new_name = re.sub(pattern, '', new_name, flags=re.IGNORECASE)
        
        # 清理多余的点号、空格和连字符
        new_name = re.sub(r'\.+', '.', new_name)  # 多个点号合并为一个
        new_name = re.sub(r'\s+', ' ', new_name)   # 多个空格合并为一个
        new_name = re.sub(r'-+', '-', new_name)   # 多个连字符合并为一个
        new_name = re.sub(r'\.$', '', new_name)   # 移除末尾的点号
        new_name = re.sub(r'\s+\[', ' [', new_name)  # 确保评分前有空格
        new_name = new_name.strip()  # 移除首尾空格
        
        # 修复一些特殊情况
        new_name = re.sub(r'Season\s+(\d+)\s*\.', r'Season \1.', new_name)  # 修复Season格式
        new_name = re.sub(r'\s+\.', '.', new_name)  # 移除点号前的空格
        
        if new_name != folder_name:
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 清理成功: {folder_name}")
                    print(f"      -> {new_name}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ❌ 清理失败: {folder_name} - {e}")
            else:
                print(f"  ⚠️ 目标文件夹已存在，跳过: {new_name}")
                
    print(f"🧹 发布组和技术参数清理完成，处理了 {cleaned_count} 个文件夹")
    return cleaned_count

def final_quality_check(tv_directory):
    """最终质量检查"""
    tv_path = Path(tv_directory)
    
    print("\n🔍 进行最终质量检查...")
    
    issues = []
    perfect_folders = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        folder_issues = []
        
        # 检查是否有中文名称
        if not re.search(r'[\u4e00-\u9fff]', folder_name):
            folder_issues.append("缺少中文名称")
            
        # 检查是否有评分信息
        if not re.search(r'\[(无评分|IMDB:[\d.]+)\]', folder_name):
            folder_issues.append("缺少评分信息")
            
        # 检查是否还有技术参数残留
        tech_remnants = ['x264', 'x265', 'H264', 'H265', 'BluRay', 'WEB-DL', '1080p', '2160p']
        for tech in tech_remnants:
            if tech.lower() in folder_name.lower():
                folder_issues.append(f"技术参数残留: {tech}")
                break
                
        # 检查是否还有发布组残留
        group_remnants = ['PTH', 'CHDWEB', 'HHWEB', 'ROCCaT', 'DBTV']
        for group in group_remnants:
            if group in folder_name:
                folder_issues.append(f"发布组残留: {group}")
                break
        
        if folder_issues:
            issues.append(f"{folder_name}: {', '.join(folder_issues)}")
        else:
            perfect_folders += 1
    
    total_folders = len([f for f in tv_path.iterdir() if f.is_dir()])
    
    print(f"📊 质量检查结果：")
    print(f"  总文件夹数: {total_folders}")
    print(f"  完美标准化: {perfect_folders} ({perfect_folders/total_folders*100:.1f}%)")
    print(f"  仍有问题: {len(issues)} ({len(issues)/total_folders*100:.1f}%)")
    
    if issues:
        print(f"\n⚠️ 仍需处理的问题（显示前5个）：")
        for issue in issues[:5]:
            print(f"  {issue}")
        if len(issues) > 5:
            print(f"  ... 还有 {len(issues) - 5} 个问题")
    
    return len(issues), perfect_folders

def main():
    tv_directory = "/Volumes/video/电视"
    
    if not os.path.exists(tv_directory):
        print(f"❌ 错误：电视目录不存在 - {tv_directory}")
        return
        
    print("🎯 开始最终清理电视目录...")
    print("=" * 50)
    
    # 清理发布组标识和技术参数
    cleaned_count = clean_release_groups_and_tech_params(tv_directory)
    
    # 最终质量检查
    issues_count, perfect_count = final_quality_check(tv_directory)
    
    print("\n" + "=" * 50)
    print(f"🎉 电视目录最终清理完成！")
    print(f"✅ 本次清理了 {cleaned_count} 个文件夹")
    print(f"🏆 {perfect_count} 个文件夹达到完美标准")
    
    if issues_count == 0:
        print("🎊 恭喜！电视目录已完全标准化！")
    else:
        print(f"⚠️ 还有 {issues_count} 个文件夹需要手动调整")
    
    # 最终统计
    print("\n📈 最终统计：")
    folder_count = len([f for f in Path(tv_directory).iterdir() if f.is_dir()])
    file_count = len([f for f in Path(tv_directory).iterdir() if f.is_file()])
    print(f"  📁 文件夹总数: {folder_count}")
    print(f"  📄 散落文件: {file_count}")
    print(f"  🎯 标准化率: {perfect_count/folder_count*100:.1f}%")

if __name__ == "__main__":
    main()