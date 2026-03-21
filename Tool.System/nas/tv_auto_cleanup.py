#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电视目录自动化清理和整理工具
"""

import os
import re
from pathlib import Path

def auto_cleanup_metadata_files(tv_directory):
    """自动清理元数据文件"""
    tv_path = Path(tv_directory)
    
    metadata_extensions = ['.nfo', '-thumb.jpg', '.jpg', '.png']
    metadata_files = []
    
    print("🗑️ 开始自动清理元数据文件...")
    
    # 查找所有元数据文件
    for item in tv_path.iterdir():
        if item.is_file():
            if any(item.name.endswith(ext) for ext in metadata_extensions) or item.name == '.DS_Store':
                metadata_files.append(item)
                
    if metadata_files:
        print(f"发现 {len(metadata_files)} 个元数据文件")
        deleted_count = 0
        for file in metadata_files:
            try:
                file.unlink()
                print(f"  ✅ 已删除: {file.name}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ 删除失败: {file.name} - {e}")
                
        print(f"🗑️ 元数据清理完成，删除了 {deleted_count} 个文件")
    else:
        print("没有发现需要清理的元数据文件")
        
    return len(metadata_files)

def auto_add_chinese_names(tv_directory):
    """自动为缺少中文名称的文件夹添加中文名称"""
    tv_path = Path(tv_directory)
    
    print("\n🏷️ 开始自动添加缺失的中文名称...")
    
    # 扩展的中英文映射
    name_mapping = {
        'Clarksons.Farm': '克拉克森的农场',
        'Game of Thrones': '权力的游戏',
        'Foundation': '基地',
        'Civilisation': '文明',
        'Cosmos': '宇宙',
        'Planet Earth': '地球脉动',
        'Human Body': '人体奥秘',
        'Hospital Playlist': '机智的医生生活',
        'Crime Crackdown': '扫黑风暴',
        'Eden Untamed Planet': '伊甸园：野性星球',
        'How the Universe Works': '宇宙是如何运行的',
        'History Of World': '世界历史',
        'Cycle Around Japan': '日本骑行之旅',
        'Inside Planet Earth': '地球内部探秘',
        'Inside The Human Body': '人体内部之旅',
        'Three Kingdoms': '三国',
        'Animal Kingdom': '动物王国',
        'Friends': '老友记',
        'Suits': '金装律师',
        'Lie To Me': '别对我撒谎',
        'The Grand Tour': '大巡游',
        'Mom': '老妈',
        'Once Upon a Bite': '风味人间',
        'Word of Honor': '山河令',
        'Home': '家园',
        'Lost in Space': '太空迷航',
        'Star Trek Picard': '星际迷航：皮卡德',
        'Tokyo Love Story': '东京爱情故事',
        'The Movies': '电影',
        'Masters of Sex': '性爱大师',
        'Space Force': '太空部队',
        'Love Death & Robots': '爱，死亡和机器人',
        'Tiny World': '小小世界',
        'House of the Dragon': '龙之家族',
        'Jade Japan': '日本玉石之旅'
    }
    
    renamed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        
        # 检查是否包含中文
        if re.search(r'[\u4e00-\u9fff]', folder_name):
            continue
            
        # 查找匹配的中文名称
        chinese_name = None
        for english, chinese in name_mapping.items():
            if english.lower() in folder_name.lower():
                chinese_name = chinese
                break
                
        if chinese_name:
            # 构建新的文件夹名称
            new_name = f"{chinese_name}.{folder_name}"
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 重命名成功: {folder_name} -> {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"  ❌ 重命名失败: {folder_name} - {e}")
                    
    print(f"🏷️ 中文名称添加完成，处理了 {renamed_count} 个文件夹")
    return renamed_count

def auto_fix_season_format(tv_directory):
    """自动修复季数格式"""
    tv_path = Path(tv_directory)
    
    print("\n📺 开始自动修复季数格式...")
    
    renamed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        new_name = folder_name
        
        # 修复各种季数格式
        # S01 -> Season 1
        new_name = re.sub(r'\.S(\d+)', r'.Season \1', new_name)
        new_name = re.sub(r'S(\d+)\.', r'Season \1.', new_name)
        new_name = re.sub(r'^S(\d+)', r'Season \1', new_name)
        
        # 第X季 -> Season X
        new_name = re.sub(r'第(\d+)季', r'Season \1', new_name)
        new_name = re.sub(r'\.第(\d+)季', r'.Season \1', new_name)
        
        # Season 01 -> Season 1 (去掉前导零)
        new_name = re.sub(r'Season 0(\d+)', r'Season \1', new_name)
        
        if new_name != folder_name:
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 修复成功: {folder_name} -> {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"  ❌ 修复失败: {folder_name} - {e}")
                    
    print(f"📺 季数格式修复完成，处理了 {renamed_count} 个文件夹")
    return renamed_count

def add_missing_ratings(tv_directory):
    """为缺少评分信息的文件夹添加[无评分]标识"""
    tv_path = Path(tv_directory)
    
    print("\n⭐ 开始添加缺失的评分信息...")
    
    renamed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        
        # 检查是否已有评分信息
        if '[无评分]' in folder_name or '[IMDB:' in folder_name or 'IMDB:' in folder_name:
            continue
            
        # 添加[无评分]标识
        new_name = f"{folder_name} [无评分]"
        new_folder_path = tv_path / new_name
        
        if not new_folder_path.exists():
            try:
                folder.rename(new_folder_path)
                print(f"  ✅ 添加评分标识: {folder_name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"  ❌ 添加失败: {folder_name} - {e}")
                
    print(f"⭐ 评分信息添加完成，处理了 {renamed_count} 个文件夹")
    return renamed_count

def remove_small_folders(tv_directory):
    """移除过小的文件夹（可能是无用内容）"""
    tv_path = Path(tv_directory)
    
    print("\n🗑️ 开始检查并移除过小的文件夹...")
    
    removed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        # 计算文件夹大小
        try:
            folder_size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file()) / (1024**3)  # GB
            
            if folder_size < 0.1:  # 小于100MB
                print(f"  发现过小文件夹: {folder.name} ({folder_size:.2f}GB)")
                
                # 检查是否为空文件夹或只包含很小的文件
                files_in_folder = list(folder.rglob('*'))
                if len(files_in_folder) == 0 or folder_size < 0.01:  # 空文件夹或小于10MB
                    try:
                        import shutil
                        shutil.rmtree(folder)
                        print(f"  ✅ 已删除过小文件夹: {folder.name}")
                        removed_count += 1
                    except Exception as e:
                        print(f"  ❌ 删除失败: {folder.name} - {e}")
                        
        except Exception as e:
            print(f"  ❌ 无法计算文件夹大小: {folder.name} - {e}")
            
    print(f"🗑️ 过小文件夹清理完成，删除了 {removed_count} 个文件夹")
    return removed_count

def main():
    tv_directory = "/Volumes/video/电视"
    
    if not os.path.exists(tv_directory):
        print(f"❌ 错误：电视目录不存在 - {tv_directory}")
        return
        
    print("🚀 开始电视目录自动化整理...")
    print("=" * 50)
    
    total_changes = 0
    
    # 1. 清理元数据文件
    total_changes += auto_cleanup_metadata_files(tv_directory)
    
    # 2. 添加中文名称
    total_changes += auto_add_chinese_names(tv_directory)
    
    # 3. 修复季数格式
    total_changes += auto_fix_season_format(tv_directory)
    
    # 4. 添加评分信息
    total_changes += add_missing_ratings(tv_directory)
    
    # 5. 移除过小文件夹
    total_changes += remove_small_folders(tv_directory)
    
    print("\n" + "=" * 50)
    print(f"✅ 电视目录自动化整理完成！总共处理了 {total_changes} 项")
    
    # 最终统计
    print("\n📊 最终统计：")
    folder_count = len([f for f in Path(tv_directory).iterdir() if f.is_dir()])
    file_count = len([f for f in Path(tv_directory).iterdir() if f.is_file()])
    print(f"  文件夹数量: {folder_count}")
    print(f"  散落文件数量: {file_count}")

if __name__ == "__main__":
    main()