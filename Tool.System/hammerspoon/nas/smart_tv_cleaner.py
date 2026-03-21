#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能电视剧目录清理工具
专门处理电视剧文件夹名称的标准化清理
"""

import os
import re
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def clean_tv_folder_name(folder_name):
    """
    清理电视剧文件夹名称
    """
    original = folder_name
    cleaned = folder_name
    
    # 技术参数模式
    tech_patterns = [
        r'\b(?:BluRay|BDRip|DVDRip|HDRip|WEBRip|WEBDL|WEB-DL|BDRemux|Remux)\b',
        r'\b(?:x264|x265|H264|H265|HEVC|AVC|VC1)\b',
        r'\b(?:1080p|720p|480p|2160p|4K|UHD|FHD|HD|1080i|UHDTV)\b',
        r'\b(?:DTS|AC3|AAC|FLAC|TrueHD|Atmos|DD\+?|DDP|DTS-HD|MA|AAC22\.2)\b',
        r'\b(?:5\.1|7\.1|2\.0|50FPS|AAC2\.0)\b',
        r'\b(?:10bit|8bit)\b',
        r'\b(?:HDR|HDR10|DV|Dolby|Vision|HLG|EDR)\b',
        r'\b(?:Rerip|REPACK)\b',
        r'\b(?:Netflix|Netfilx|ATVP|NF)\b',  # 流媒体平台
        r'\b(?:Complete|WEBrip|HDTV|HDTV1080P)\b',
        r'\b(?:BS4K|TV)\b',  # 电视台标识
        r'\.[0-9]{8}\.',  # 日期格式
        r'\b(?:m2ts)$',  # 文件扩展名
        r'\b(?:国粤双语中字)\b',  # 中文字幕标识
    ]
    
    # 发布组模式
    release_groups = [
        r'-(?:DBTV|NOGRP|PTHtv|PTHweb|PTH|FLUX|TOMMY|AREY|DIY-HDChina|playBD|Chuck0924|ROCCaT|HHWEB|CHDWEB|PuTao|YingWEB)\b',
        r'@(?:PTHtv|FRDS)\b',
        r'\[(?:EliteT)\]',
        r'￡[^@]*@[^\s]*',  # 特殊符号的发布组格式
    ]
    
    # 应用技术参数清理
    for pattern in tech_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # 应用发布组清理
    for pattern in release_groups:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # 清理年份范围（如2015-2020）
    cleaned = re.sub(r'\b(19|20)\d{2}-(19|20)\d{2}\b', '', cleaned)
    
    # 清理多余的点、空格和连字符
    cleaned = re.sub(r'[.\-_]+', '.', cleaned)
    cleaned = re.sub(r'^[.\-_]+|[.\-_]+$', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # 标准化季数格式
    # S01 -> Season 1, S1 -> Season 1
    cleaned = re.sub(r'\bS(\d{1,2})\b', lambda m: f'Season {int(m.group(1))}', cleaned, flags=re.IGNORECASE)
    
    # 清理连续的点
    cleaned = re.sub(r'\.{2,}', '.', cleaned)
    cleaned = re.sub(r'^\.|\.$', '', cleaned)
    
    # 如果清理后为空或过短，返回原名称
    if len(cleaned.strip()) < 3:
        return None
    
    return cleaned if cleaned != original else None

def extract_imdb_rating(folder_name):
    """
    从文件夹名称中提取IMDB评分
    """
    # 查找现有的IMDB评分格式
    imdb_match = re.search(r'\[IMDB[:\s]*([0-9.]+)\]', folder_name, re.IGNORECASE)
    if imdb_match:
        return f"[IMDB: {imdb_match.group(1)}]"
    
    # 这里可以添加从外部API获取IMDB评分的逻辑
    # 暂时返回无评分
    return "[无评分]"

def standardize_tv_name(folder_name):
    """
    标准化电视剧名称
    """
    # 先清理技术参数
    cleaned = clean_tv_folder_name(folder_name)
    if not cleaned:
        return None
    
    # 提取或添加IMDB评分
    imdb_rating = extract_imdb_rating(folder_name)
    
    # 移除现有的评分标签
    cleaned = re.sub(r'\[IMDB[:\s]*[0-9.]*\]', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\[无评分\]', '', cleaned, flags=re.IGNORECASE)
    
    # 清理多余空格
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # 添加评分
    final_name = f"{cleaned} {imdb_rating}"
    
    return final_name

def main():
    """
    主函数
    """
    tv_dir = Path('/Volumes/video/电视')
    
    if not tv_dir.exists():
        logger.error(f"目录不存在: {tv_dir}")
        return
    
    logger.info("开始清理电视剧目录...")
    logger.info("=" * 60)
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for item in tv_dir.iterdir():
        if item.is_dir():
            try:
                new_name = standardize_tv_name(item.name)
                
                if new_name and new_name != item.name:
                    new_path = item.parent / new_name
                    
                    # 检查新名称是否已存在
                    if new_path.exists():
                        logger.warning(f"⚠️  跳过（目标已存在）: {item.name}")
                        skipped_count += 1
                        continue
                    
                    # 重命名文件夹
                    item.rename(new_path)
                    logger.info(f"✅ 重命名: {item.name} -> {new_name}")
                    renamed_count += 1
                else:
                    logger.info(f"⏭️  跳过（无需更改）: {item.name}")
                    skipped_count += 1
                    
            except Exception as e:
                logger.error(f"❌ 错误处理文件夹 {item.name}: {e}")
                error_count += 1
        elif item.is_file() and item.suffix.lower() in {'.mkv', '.mp4', '.avi', '.mov'}:
            # 处理直接放在电视目录下的视频文件
            try:
                cleaned_name = clean_tv_folder_name(item.stem)
                if cleaned_name:
                    new_name = cleaned_name + item.suffix
                    if new_name != item.name:
                        new_path = item.parent / new_name
                        if not new_path.exists():
                            item.rename(new_path)
                            logger.info(f"✅ 重命名文件: {item.name} -> {new_name}")
                            renamed_count += 1
                        else:
                            logger.warning(f"⚠️  跳过文件（目标已存在）: {item.name}")
                            skipped_count += 1
                    else:
                        logger.info(f"⏭️  跳过文件（无需更改）: {item.name}")
                        skipped_count += 1
                else:
                    logger.info(f"⏭️  跳过文件（无需更改）: {item.name}")
                    skipped_count += 1
            except Exception as e:
                logger.error(f"❌ 错误处理文件 {item.name}: {e}")
                error_count += 1
    
    logger.info("=" * 60)
    logger.info("电视剧目录清理完成！")
    logger.info(f"重命名: {renamed_count} 个项目")
    logger.info(f"跳过: {skipped_count} 个项目")
    logger.info(f"错误: {error_count} 个项目")
    logger.info(f"总计: {renamed_count + skipped_count + error_count} 个项目")

if __name__ == '__main__':
    main()