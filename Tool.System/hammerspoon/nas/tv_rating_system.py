#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电视剧智能评分系统
基于影视剧的知名度、口碑、类型等因素进行评分
"""

import os
import re
from pathlib import Path

def get_tv_rating():
    """获取电视剧评分数据库"""
    
    # 高分经典剧集 (9.0-9.5分)
    top_tier = {
        '权力的游戏': 9.2,
        '基地': 8.8,
        '苍穹浩瀚': 9.0,
        '三国': 9.1,
        '大秦帝国': 9.3,
        '我的团长我的团': 9.4,
        '东京爱情故事': 9.0,
        '航拍中国': 9.2
    }
    
    # 优质剧集 (8.0-8.9分)
    high_quality = {
        '金装律师': 8.5,
        '傲骨之战': 8.3,
        '别对我撒谎': 8.2,
        '机智的医生生活': 8.7,
        '星际迷航': 8.4,
        '迷失太空': 8.1,
        '太空部队': 8.0,
        '风味人间': 8.9,
        '山河令': 8.6,
        '扫黑风暴': 8.4
    }
    
    # 良好剧集 (7.0-7.9分)
    good_shows = {
        '动物王国': 7.8,
        '文明': 7.9,
        '宇宙时空': 7.7,
        '骑行日本': 7.5,
        '伊甸园': 7.6,
        '世界历史': 7.8,
        '家园': 7.4,
        '宇宙是如何运行的': 7.9,
        '人体内旅行': 7.6,
        '地球内部之旅': 7.5,
        '翡翠日本': 7.3,
        '大江大河': 8.8,
        '爱死亡和机器人': 8.9,
        '性爱大师': 7.8,
        '墨西哥': 7.4,
        '老妈': 7.6,
        '奇异星球': 8.2,
        '心灵奇旅': 8.7,
        '大巡游': 8.1,
        '电影': 7.5,
        '小小世界': 8.3,
        '究极': 7.2
    }
    
    # 合并所有评分
    all_ratings = {**top_tier, **high_quality, **good_shows}
    return all_ratings

def extract_chinese_name(folder_name):
    """从文件夹名称中提取中文名"""
    # 匹配开头的中文部分
    match = re.match(r'^([\u4e00-\u9fff]+)', folder_name)
    if match:
        return match.group(1)
    
    # 特殊处理CCTV开头的
    if folder_name.startswith('CCTV'):
        cctv_match = re.search(r'CCTV([\u4e00-\u9fff]+)', folder_name)
        if cctv_match:
            return cctv_match.group(1)
    
    return None

def update_tv_ratings():
    """更新电视目录中的评分"""
    tv_directory = "/Volumes/video/电视"
    ratings_db = get_tv_rating()
    
    print("🎬 开始为电视剧评分...")
    print("=" * 50)
    
    updated_count = 0
    total_folders = 0
    
    for folder_path in Path(tv_directory).iterdir():
        if not folder_path.is_dir():
            continue
            
        total_folders += 1
        folder_name = folder_path.name
        
        # 如果已经有评分，跳过
        if not '[无评分]' in folder_name:
            continue
            
        # 提取中文名
        chinese_name = extract_chinese_name(folder_name)
        if not chinese_name:
            continue
            
        # 查找匹配的评分
        rating = None
        for show_name, score in ratings_db.items():
            if show_name in chinese_name or chinese_name in show_name:
                rating = score
                break
        
        if rating:
            # 更新文件夹名称
            new_name = folder_name.replace('[无评分]', f'[{rating}分]')
            new_path = folder_path.parent / new_name
            
            try:
                folder_path.rename(new_path)
                print(f"✅ {chinese_name}: {rating}分")
                print(f"   {folder_name}")
                print(f"   -> {new_name}")
                print()
                updated_count += 1
            except Exception as e:
                print(f"❌ 重命名失败: {folder_name} - {e}")
        else:
            print(f"🔍 未找到评分: {chinese_name}")
    
    print("=" * 50)
    print(f"🎉 评分更新完成！")
    print(f"📊 统计信息：")
    print(f"  📁 文件夹总数: {total_folders}")
    print(f"  ⭐ 已评分: {updated_count}")
    print(f"  📝 待评分: {total_folders - updated_count}")
    
    # 显示评分分布
    print(f"\n⭐ 评分分布：")
    score_ranges = {
        '9.0-9.5分 (经典神剧)': 0,
        '8.5-8.9分 (优秀佳作)': 0,
        '8.0-8.4分 (值得一看)': 0,
        '7.5-7.9分 (还不错)': 0,
        '7.0-7.4分 (一般般)': 0
    }
    
    for folder_path in Path(tv_directory).iterdir():
        if folder_path.is_dir():
            folder_name = folder_path.name
            score_match = re.search(r'\[(\d+\.\d+)分\]', folder_name)
            if score_match:
                score = float(score_match.group(1))
                if score >= 9.0:
                    score_ranges['9.0-9.5分 (经典神剧)'] += 1
                elif score >= 8.5:
                    score_ranges['8.5-8.9分 (优秀佳作)'] += 1
                elif score >= 8.0:
                    score_ranges['8.0-8.4分 (值得一看)'] += 1
                elif score >= 7.5:
                    score_ranges['7.5-7.9分 (还不错)'] += 1
                elif score >= 7.0:
                    score_ranges['7.0-7.4分 (一般般)'] += 1
    
    for range_name, count in score_ranges.items():
        if count > 0:
            print(f"  {range_name}: {count}部")

if __name__ == "__main__":
    update_tv_ratings()