#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的电视目录标准化处理脚本
解决所有遗留问题，确保真正的100%标准化
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

def get_chinese_name_mapping():
    """获取英文到中文的映射表"""
    return {
        'Animal.Kingdom': '动物王国',
        'Civilisation': '文明',
        'Cosmos.Possible.Worlds': '宇宙时空.可能的世界',
        'Crime.Crackdown': '扫黑风暴',
        'Cycle.Around.Japan': '骑行日本',
        'Eden.Untamed.Planet': '伊甸园.未驯服的星球',
        'Foundation': '基地',
        'Game.of.Thrones': '权力的游戏',
        'History Of World': '世界历史',
        'Home': '家园',
        'Hospital.Playlist': '机智的医生生活',
        'How the Universe Works': '宇宙是如何运行的',
        'Inside The Human Body': '人体内旅行',
        'Inside.Planet.Earth': '地球内部之旅',
        'Jade.Japan': '翡翠日本',
        'Kyūkyoku': '究极',
        'Lie.To.Me': '别对我撒谎',
        'Like.A.Flowing.River': '大江大河',
        'Lost.in.Space': '迷失太空',
        'Love.Death.&.Robots': '爱死亡和机器人',
        'Masters.of.Sex': '性爱大师',
        'Mexico Earth\'s Festival of Life': '墨西哥.地球生命节',
        'Mom': '老妈',
        'My.Chief.and.My.Regiment': '我的团长我的团',
        'Once.Upon.a.Bite': '风味人间',
        'One.Strange.Rock': '奇异星球',
        'Qin.Empire.Alliance': '大秦帝国.联盟',
        'Soul': '心灵奇旅',
        'Space.Force': '太空部队',
        'Star.Trek.Picard': '星际迷航.皮卡德',
        'Suits': '金装律师',
        'The.Grand.Tour': '大巡游',
        'The.Movies': '电影',
        'Three.Kingdoms': '三国',
        'Tiny.World': '小小世界',
        'Tokyo.Love.Story': '东京爱情故事',
        'Word.of.Honor': '山河令'
    }

def remove_duplicates(tv_directory):
    """移除重复文件夹，保留较好的版本"""
    tv_path = Path(tv_directory)
    
    print("🔍 检查并移除重复文件夹...")
    
    # 按基础名称分组
    groups = defaultdict(list)
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        
        # 提取基础名称（去除季数、集数、年份等）
        base_name = re.sub(r'\.(Season|S)\s*\d+.*', '', folder_name)
        base_name = re.sub(r'\s*\[.*?\]$', '', base_name)
        base_name = re.sub(r'\.(\d{4}).*', '', base_name)
        base_name = re.sub(r'\.E\d+.*', '', base_name)
        
        groups[base_name].append(folder)
    
    removed_count = 0
    
    for base_name, folders in groups.items():
        if len(folders) > 1:
            print(f"  发现重复: {base_name} ({len(folders)}个版本)")
            
            # 选择最好的版本（优先选择有中文名的、较短的、没有技术参数的）
            best_folder = None
            best_score = -1
            
            for folder in folders:
                score = 0
                name = folder.name
                
                # 有中文名加分
                if re.search(r'[\u4e00-\u9fff]', name):
                    score += 10
                    
                # 较短的名称加分
                score += max(0, 200 - len(name))
                
                # 没有技术参数加分
                tech_params = ['H.264', 'x264', 'DDP5.1', 'BluRay']
                if not any(param in name for param in tech_params):
                    score += 5
                    
                # 有Season格式加分
                if 'Season' in name:
                    score += 3
                    
                if score > best_score:
                    best_score = score
                    best_folder = folder
            
            # 删除其他版本
            for folder in folders:
                if folder != best_folder:
                    try:
                        shutil.rmtree(folder)
                        print(f"    ✅ 删除重复: {folder.name}")
                        removed_count += 1
                    except Exception as e:
                        print(f"    ❌ 删除失败: {folder.name} - {e}")
                        
            print(f"    🏆 保留最佳: {best_folder.name}")
    
    print(f"🔍 重复文件夹处理完成，删除了 {removed_count} 个重复项")
    return removed_count

def add_chinese_names(tv_directory):
    """为缺少中文名称的文件夹添加中文名"""
    tv_path = Path(tv_directory)
    chinese_mapping = get_chinese_name_mapping()
    
    print("\n🈶 为缺少中文名称的文件夹添加中文名...")
    
    renamed_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        
        # 检查是否已有中文名称（排除CCTV等特殊情况）
        if re.search(r'[\u4e00-\u9fff]', folder_name) and not folder_name.startswith('CCTV'):
            continue
            
        # 查找匹配的英文名称
        new_name = None
        
        for english_name, chinese_name in chinese_mapping.items():
            if folder_name.startswith(english_name):
                # 构建新名称：中文名.英文名.其他部分
                remaining = folder_name[len(english_name):]
                if remaining.startswith('.'):
                    remaining = remaining[1:]
                    
                if remaining:
                    new_name = f"{chinese_name}.{english_name}.{remaining}"
                else:
                    new_name = f"{chinese_name}.{english_name}"
                break
        
        if new_name:
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 添加中文名: {folder_name}")
                    print(f"      -> {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"  ❌ 重命名失败: {folder_name} - {e}")
            else:
                print(f"  ⚠️ 目标文件夹已存在，跳过: {new_name}")
    
    print(f"🈶 中文名称添加完成，处理了 {renamed_count} 个文件夹")
    return renamed_count

def clean_remaining_issues(tv_directory):
    """清理剩余的命名问题"""
    tv_path = Path(tv_directory)
    
    print("\n🧹 清理剩余的命名问题...")
    
    cleaned_count = 0
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        folder_name = folder.name
        new_name = folder_name
        
        # 修复季数格式
        new_name = re.sub(r'Season\s+(\d+)E(\d+)', r'Season \1.E\2', new_name)
        new_name = re.sub(r'Ep(\d+)\.(\d+)', r'E\1-\2', new_name)
        
        # 清理多余的空格和点号
        new_name = re.sub(r'\s+', ' ', new_name)
        new_name = re.sub(r'\.+', '.', new_name)
        new_name = re.sub(r'\s+\.', '.', new_name)
        new_name = re.sub(r'\.\s+', '.', new_name)
        new_name = new_name.strip()
        
        # 确保评分格式正确
        new_name = re.sub(r'\s*\[\s*(无评分|IMDB:[\d.]+)\s*\]\s*$', r' [\1]', new_name)
        
        if new_name != folder_name:
            new_folder_path = tv_path / new_name
            
            if not new_folder_path.exists():
                try:
                    folder.rename(new_folder_path)
                    print(f"  ✅ 格式修复: {folder_name}")
                    print(f"      -> {new_name}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ❌ 修复失败: {folder_name} - {e}")
    
    print(f"🧹 格式清理完成，处理了 {cleaned_count} 个文件夹")
    return cleaned_count

def final_validation(tv_directory):
    """最终验证标准化结果"""
    tv_path = Path(tv_directory)
    
    print("\n🔍 进行最终验证...")
    
    total_folders = 0
    perfect_folders = 0
    issues = []
    
    for folder in tv_path.iterdir():
        if not folder.is_dir():
            continue
            
        total_folders += 1
        folder_name = folder.name
        folder_issues = []
        
        # 检查中文名称
        if not re.search(r'[\u4e00-\u9fff]', folder_name):
            folder_issues.append("缺少中文名称")
            
        # 检查评分信息
        if not re.search(r'\[(无评分|IMDB:[\d.]+)\]$', folder_name):
            folder_issues.append("缺少评分信息")
            
        # 检查技术参数残留
        tech_params = ['x264', 'x265', 'H.264', 'H.265', 'DDP5.1', 'BluRay']
        for param in tech_params:
            if param in folder_name:
                folder_issues.append(f"技术参数残留: {param}")
                break
                
        # 检查发布组残留
        release_groups = ['PTH', 'CHDWEB', 'HHWEB', 'ROCCaT']
        for group in release_groups:
            if group in folder_name:
                folder_issues.append(f"发布组残留: {group}")
                break
        
        if folder_issues:
            issues.append(f"{folder_name}: {', '.join(folder_issues)}")
        else:
            perfect_folders += 1
    
    standardization_rate = (perfect_folders / total_folders * 100) if total_folders > 0 else 0
    
    print(f"📊 最终验证结果：")
    print(f"  📁 总文件夹数: {total_folders}")
    print(f"  🏆 完美标准化: {perfect_folders}")
    print(f"  🎯 标准化率: {standardization_rate:.1f}%")
    print(f"  ⚠️ 仍有问题: {len(issues)}")
    
    if issues:
        print(f"\n❌ 未解决的问题：")
        for issue in issues[:10]:  # 只显示前10个
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... 还有 {len(issues) - 10} 个问题")
    
    return standardization_rate, len(issues)

def main():
    tv_directory = "/Volumes/video/电视"
    
    if not os.path.exists(tv_directory):
        print(f"❌ 错误：电视目录不存在 - {tv_directory}")
        return
        
    print("🚀 开始完整的电视目录标准化处理...")
    print("=" * 60)
    
    total_changes = 0
    
    # 1. 移除重复文件夹
    total_changes += remove_duplicates(tv_directory)
    
    # 2. 添加中文名称
    total_changes += add_chinese_names(tv_directory)
    
    # 3. 清理剩余问题
    total_changes += clean_remaining_issues(tv_directory)
    
    # 4. 最终验证
    standardization_rate, remaining_issues = final_validation(tv_directory)
    
    print("\n" + "=" * 60)
    print(f"🎉 电视目录标准化处理完成！")
    print(f"✅ 总共处理了 {total_changes} 项")
    print(f"🎯 最终标准化率: {standardization_rate:.1f}%")
    
    if remaining_issues == 0:
        print("🎊 恭喜！电视目录已达到100%标准化！")
    else:
        print(f"⚠️ 还有 {remaining_issues} 个问题需要进一步处理")
    
    # 清理系统文件
    ds_store_path = Path(tv_directory) / '.DS_Store'
    if ds_store_path.exists():
        try:
            ds_store_path.unlink()
            print("🗑️ 已清理 .DS_Store 文件")
        except:
            pass

if __name__ == "__main__":
    main()