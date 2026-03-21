#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电视目录视频文件清理工具
专门处理电视目录下直接存放的视频文件名
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

def clean_tv_filename(filename):
    """
    清理电视视频文件名中的技术参数
    """
    # 保存原始文件名
    original = filename
    
    # 获取文件扩展名
    name, ext = os.path.splitext(filename)
    
    # 技术参数模式
    tech_patterns = [
        r'\b(?:BluRay|BDRip|DVDRip|HDRip|WEBRip|WEBDL|WEB-DL|BDRemux|Remux)\b',
        r'\b(?:x264|x265|H264|H265|HEVC|AVC|VC1)\b',
        r'\b(?:1080p|720p|480p|2160p|4K|UHD|FHD|HD|1080i|UHDTV|HDTV1080P)\b',
        r'\b(?:DTS|AC3|AAC|FLAC|TrueHD|Atmos|DD\+?|DDP|DTS-HD|MA|AAC22\.2)\b',
        r'\b(?:5\.1|7\.1|2\.0|50FPS)\b',
        r'\b(?:10bit|8bit)\b',
        r'\b(?:HDR|HDR10|DV|Dolby|Vision|HLG)\b',
        r'\b(?:Rerip|REPACK)\b',
        r'\b(?:Netflix|Netfilx|ATVP|NF|NHK|BS4K)\b',
        r'\b(?:Complete|WEBrip|HDTV)\b',
        r'\b(?:TV)\b',
        r'\.[0-9]{8}\.',  # 日期格式
        r'\b(?:Kyūkyoku|Gaido)\b',  # 日文节目名
        r'\b(?:国粤双语中字)\b',  # 中文字幕标识
    ]
    
    # 应用清理规则
    for pattern in tech_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # 清理多余的点、空格和连字符
    name = re.sub(r'[.\-_]+', '.', name)
    name = re.sub(r'^[.\-_]+|[.\-_]+$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    # 重新组合文件名
    cleaned = name + ext
    
    return cleaned if cleaned != original else None

def main():
    """
    主函数
    """
    tv_dir = Path('/Volumes/video/电视')
    
    if not tv_dir.exists():
        logger.error(f"目录不存在: {tv_dir}")
        return
    
    logger.info("开始清理电视目录视频文件...")
    logger.info("=" * 60)
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    # 只处理视频文件
    video_extensions = {'.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m2ts', '.ts'}
    
    for file_path in tv_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            try:
                cleaned_name = clean_tv_filename(file_path.name)
                
                if cleaned_name and cleaned_name != file_path.name:
                    new_path = file_path.parent / cleaned_name
                    
                    # 检查新文件名是否已存在
                    if new_path.exists():
                        logger.warning(f"⚠️  跳过（目标文件已存在）: {file_path.name}")
                        skipped_count += 1
                        continue
                    
                    # 重命名文件
                    file_path.rename(new_path)
                    logger.info(f"✅ 重命名: {file_path.name} -> {cleaned_name}")
                    renamed_count += 1
                else:
                    logger.info(f"⏭️  跳过（无需更改）: {file_path.name}")
                    skipped_count += 1
                    
            except Exception as e:
                logger.error(f"❌ 错误处理文件 {file_path.name}: {e}")
                error_count += 1
    
    logger.info("=" * 60)
    logger.info("电视视频文件清理完成！")
    logger.info(f"重命名: {renamed_count} 个文件")
    logger.info(f"跳过: {skipped_count} 个文件")
    logger.info(f"错误: {error_count} 个文件")
    logger.info(f"总计: {renamed_count + skipped_count + error_count} 个文件")

if __name__ == '__main__':
    main()