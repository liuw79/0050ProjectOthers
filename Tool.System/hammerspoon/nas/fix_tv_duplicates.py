#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复电视目录中的重复季数标识问题
"""

import os
import re
from pathlib import Path

def fix_duplicate_seasons(tv_directory):
    """修复重复的季数标识"""
    tv_path = Path(tv_directory)
    
    print("🔧 开始修复重复季数标识...")
    
    fixed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        new_name = folder_name
        
        # 修复 "Season X.Season Y" 格式
        # 例如: "老友记.Friends.Season 1.Season 10" -> "老友记.Friends.Season 1-10"
        season_pattern = r'Season (\d+)\.Season (\d+)'
        match = re.search(season_pattern, new_name)
        if match:
            season1, season2 = match.groups()
            if season1 == season2:
                # 如果是相同季数，只保留一个
                new_name = re.sub(season_pattern, f'Season {season1}', new_name)
            else:
                # 如果是不同季数，合并为范围
                new_name = re.sub(season_pattern, f'Season {season1}-{season2}', new_name)
        
        # 修复 "第一季...Season X" 格式
        # 例如: "CCTV航拍中国.第一季第二集.海南.Aerial.China.Season 1E02" -> "CCTV航拍中国.第一季第二集.海南.Aerial.China.S01E02"
        chinese_season_pattern = r'第一季.*?Season (\d+)E(\d+)'
        match = re.search(chinese_season_pattern, new_name)
        if match:
            season_num, episode_num = match.groups()
            # 将Season格式改为S格式，避免与中文季数冲突
            new_name = re.sub(r'Season (\d+)E(\d+)', f'S{season_num.zfill(2)}E{episode_num.zfill(2)}', new_name)
        
        # 修复其他重复格式
        # 移除多余的Season标识
        new_name = re.sub(r'Season (\d+).*?Season \1(?!\d)', f'Season \1', new_name)
        
        if new_name != folder_name:
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 修复成功: {folder_name} -> {new_name}")
                    fixed_count += 1
                except Exception as e:
                    print(f"  ❌ 修复失败: {folder_name} - {e}")
            else:
                print(f"  ⚠️ 目标文件夹已存在，跳过: {new_name}")
                
    print(f"🔧 重复季数修复完成，处理了 {fixed_count} 个文件夹")
    return fixed_count

def clean_remaining_metadata(tv_directory):
    """清理剩余的元数据文件"""
    tv_path = Path(tv_directory)
    
    print("\n🗑️ 清理剩余元数据文件...")
    
    metadata_files = []
    for item in tv_path.iterdir():
        if item.is_file() and item.name == '.DS_Store':
            metadata_files.append(item)
            
    if metadata_files:
        for file in metadata_files:
            try:
                file.unlink()
                print(f"  ✅ 已删除: {file.name}")
            except Exception as e:
                print(f"  ❌ 删除失败: {file.name} - {e}")
                
        print(f"🗑️ 元数据清理完成，删除了 {len(metadata_files)} 个文件")
    else:
        print("没有发现需要清理的元数据文件")
        
    return len(metadata_files)

def check_naming_consistency(tv_directory):
    """检查命名一致性"""
    tv_path = Path(tv_directory)
    
    print("\n📋 检查命名一致性...")
    
    issues = []
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        
        # 检查是否缺少中文名称
        if not re.search(r'[\u4e00-\u9fff]', folder_name):
            issues.append(f"缺少中文名称: {folder_name}")
            
        # 检查是否有技术参数残留
        tech_params = ['BluRay', 'x264', 'x265', 'H264', 'H265', 'DTS', 'AAC', '1080p', '2160p', 'HDTV', 'WEB-DL']
        for param in tech_params:
            if param in folder_name:
                issues.append(f"技术参数残留 ({param}): {folder_name}")
                break
                
        # 检查是否有发布组标识残留
        release_groups = ['DBTV', 'PTH', 'FLUX', 'TOMMY', 'ROCCaT', 'HHWEB', 'CHDWEB', 'CMCTV']
        for group in release_groups:
            if group in folder_name:
                issues.append(f"发布组标识残留 ({group}): {folder_name}")
                break
    
    if issues:
        print(f"发现 {len(issues)} 个命名问题：")
        for issue in issues[:10]:  # 只显示前10个
            print(f"  ⚠️ {issue}")
        if len(issues) > 10:
            print(f"  ... 还有 {len(issues) - 10} 个问题")
    else:
        print("✅ 命名检查通过，没有发现问题")
        
    return len(issues)

def main():
    tv_directory = "/Volumes/video/电视"
    
    if not os.path.exists(tv_directory):
        print(f"❌ 错误：电视目录不存在 - {tv_directory}")
        return
        
    print("🚀 开始修复电视目录剩余问题...")
    print("=" * 50)
    
    total_fixes = 0
    
    # 1. 修复重复季数标识
    total_fixes += fix_duplicate_seasons(tv_directory)
    
    # 2. 清理剩余元数据
    total_fixes += clean_remaining_metadata(tv_directory)
    
    # 3. 检查命名一致性
    issues_count = check_naming_consistency(tv_directory)
    
    print("\n" + "=" * 50)
    print(f"✅ 电视目录修复完成！总共修复了 {total_fixes} 项")
    
    if issues_count > 0:
        print(f"⚠️ 仍有 {issues_count} 个命名问题需要手动处理")
    else:
        print("🎉 电视目录已完全标准化！")
    
    # 最终统计
    print("\n📊 最终统计：")
    folder_count = len([f for f in Path(tv_directory).iterdir() if f.is_dir()])
    file_count = len([f for f in Path(tv_directory).iterdir() if f.is_file()])
    print(f"  文件夹数量: {folder_count}")
    print(f"  散落文件数量: {file_count}")

if __name__ == "__main__":
    main()