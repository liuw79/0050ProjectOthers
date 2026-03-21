#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画文件夹重命名脚本
功能：
1. 添加IMDB评分到文件夹名称
2. 清理技术参数信息（如BluRay.x264.DTS-WiKi等）
3. 标准化文件夹命名格式
"""

import os
import re
import shutil
from pathlib import Path

# IMDB评分数据库
IMDB_RATINGS = {
    # 经典动画评分
    '瑞克和莫蒂': 9.3,
    'Rick and Morty': 9.3,
    '海贼王': 9.0,
    'One Piece': 9.0,
    '新世纪福音战士': 8.5,
    'Neon Genesis Evangelion': 8.5,
    '千与千寻': 9.3,
    'Spirited Away': 9.3,
    '龙猫': 8.2,
    'My Neighbor Totoro': 8.2,
    '魔女宅急便': 7.8,
    'Kiki\'s Delivery Service': 7.8,
    '幽灵公主': 8.4,
    'Princess Mononoke': 8.4,
    '天空之城': 8.0,
    'Castle in the Sky': 8.0,
    '风之谷': 8.1,
    'Nausicaä of the Valley of the Wind': 8.1,
    '红猪': 7.7,
    'Porco Rosso': 7.7,
    '猫的报恩': 7.1,
    'The Cat Returns': 7.1,
    '哈利波特': 7.6,  # 系列平均
    'Harry Potter': 7.6,
    '汤姆和杰瑞': 8.6,  # 经典版本
    'Tom and Jerry': 8.6,
    '怪诞小镇': 8.9,
    'Gravity Falls': 8.9,
    '阿凡达降气神通': 9.3,
    'Avatar The Last Airbender': 9.3,
    '超人总动员': 8.0,
    'The Incredibles': 8.0,
    '玩具总动员': 8.3,
    'Toy Story': 8.3,
    '寻梦环游记': 8.4,
    'Coco': 8.4,
    '冰雪奇缘': 7.4,
    'Frozen': 7.4,
    '疯狂动物城': 8.0,
    'Zootopia': 8.0,
    '机器人总动员': 8.4,
    'WALL-E': 8.4,
    '飞屋环游记': 8.3,
    'Up': 8.3,
    '怪兽电力公司': 8.1,
    'Monsters Inc': 8.1,
    '海底总动员': 8.2,
    'Finding Nemo': 8.2,
    '功夫熊猫': 7.6,
    'Kung Fu Panda': 7.6,
    '驯龙高手': 8.1,
    'How to Train Your Dragon': 8.1,
    '哥斯拉大战金刚': 6.3,
    'Godzilla vs Kong': 6.3,
    '魔法满屋': 7.2,
    'Encanto': 7.2,
    '心灵奇旅': 8.0,
    'Soul': 8.0,
    '1/2的魔法': 7.4,
    'Onward': 7.4,
    '夏日友晴天': 7.4,
    'Luca': 7.4,
    '青春变形记': 7.0,
    'Turning Red': 7.0,
    '光年正传': 5.1,
    'Lightyear': 5.1,
    '奇异世界': 5.7,
    'Strange World': 5.7,
    '小美人鱼': 7.2,  # 2023版
    'The Little Mermaid': 7.2,
    '元素': 7.0,
    'Elemental': 7.0,
    '蜘蛛侠：纵横宇宙': 8.7,
    'Spider-Man: Across the Spider-Verse': 8.7,
    '超级马里奥兄弟大电影': 7.0,
    'The Super Mario Bros Movie': 7.0,
}

# 需要清理的技术参数模式
TECH_PATTERNS = [
    # 视频编码格式
    r'BluRay\.x264\.DTS-WiKi',
    r'BluRay\.x265\.DTS',
    r'BluRay\.H264',
    r'BluRay\.H265',
    r'BluRay\.HEVC',
    r'BluRay\.x264',
    r'BluRay\.x265',
    r'BluRay(?:\.Remux)?',
    r'UHD\.BluRay',
    r'WEB-DL\.x264',
    r'WEB-DL\.x265',
    r'WEB-DL\.H264',
    r'WEB-DL\.H265',
    r'WEBRip\.x264',
    r'WEBRip\.x265',
    r'BDRip\.x264',
    r'BDRip\.x265',
    r'DVDRip\.x264',
    r'HDRip\.x264',
    r'HMAX\.WEB-DL',
    r'NF\.WEB-DL',
    r'Bilibili\.WEB-DL',
    
    # 编码器和格式
    r'\.x264(?:\..*?)?',
    r'\.x265(?:\..*?)?',
    r'\.H264(?:\..*?)?',
    r'\.H265(?:\..*?)?',
    r'\.HEVC(?:\..*?)?',
    r'\.AVC(?:\..*?)?',
    r'\.MPEG-2(?:\..*?)?',
    r'10bit',
    r'8bit',
    
    # 分辨率
    r'\d{3,4}[pi]',  # 1080p, 720p, 480i等
    r'2160p',
    r'4K',
    r'UHD',
    
    # 音频格式
    r'DTS-HD(?:\.MA)?',
    r'DTS-MA',
    r'DTS(?:\.\d+)?(?:\.\d+Audio)?',
    r'TrueHD(?:\.\d+\.\d+)?',
    r'Atmos',
    r'AC3',
    r'AAC',
    r'FLAC',
    r'DD5\.1',
    r'DDP5\.1',
    r'DTSHD-MA5\.1',
    r'\d+Audio',
    r'\d+\.\d+Audio',
    
    # HDR和色彩
    r'HDR(?:10)?',
    r'Dolby\.Vision',
    r'DV',
    
    # 发布组和标识
    r'￡[^\s]+',  # 特殊符号开头的发布组
    r'@[A-Za-z0-9]+',  # @符号的发布组
    r'-[A-Z]{2,}$',  # 结尾的发布组标识
    r'-[A-Za-z0-9]+$',  # 结尾的发布组
    r'\[[A-Za-z0-9]+\]',  # 方括号内的发布组
    r'\([A-Za-z0-9]+\)',  # 圆括号内的发布组
    
    # 其他技术参数
    r'Remux',
    r'BDrip',
    r'WEBrip',
    r'DVDrip',
    r'HDrip',
    r'mUHD',
    r'GREENOTEA',
    r'PTH(?:web)?',
    r'WiKi',
    r'FRDS',
    r'BeiTai',
    r'HDS',
    r'cXcY',
    r'OurBits',
    r'CMCT小鱼',
    r'小鱼',
    
    # 语言和字幕
    r'\d+语',  # 如"四语"
    r'中英字幕',
    r'英字幕',
    r'中字幕',
    r'字幕',
    r'Mandarin',
    r'CHS',
    r'CHT',
    r'DYGC',
    
    # 年份后的技术参数（保留年份）
    r'(?<=\d{4})\.(?:BluRay|WEB-DL|BDRip|DVDRip|HDRip)',
    
    # 清理多余的点和空格
    r'\.{2,}',  # 多个连续的点
    r'\s+',  # 多余空格
    r'\.$',  # 结尾的点
    r'^\.',  # 开头的点
]

def clean_folder_name(folder_name):
    """清理文件夹名称中的技术参数"""
    cleaned_name = folder_name
    
    # 先处理特殊字符和符号
    cleaned_name = re.sub(r'￡[^\s]+', ' ', cleaned_name)  # 特殊符号发布组
    cleaned_name = re.sub(r'@[A-Za-z0-9]+', ' ', cleaned_name)  # @符号发布组
    
    # 处理常见的技术参数组合
    tech_combos = [
        r'WEB-DL\.[^\s]*H265[^\s]*',
        r'WEB-DL\.[^\s]*H264[^\s]*',
        r'WEB-DL\.[^\s]*x265[^\s]*',
        r'WEB-DL\.[^\s]*x264[^\s]*',
        r'BluRay\.[^\s]*x265[^\s]*',
        r'BluRay\.[^\s]*x264[^\s]*',
        r'BluRay\.[^\s]*H265[^\s]*',
        r'BluRay\.[^\s]*H264[^\s]*',
    ]
    
    for combo in tech_combos:
        cleaned_name = re.sub(combo, ' ', cleaned_name, flags=re.IGNORECASE)
    
    # 按顺序应用清理模式
    for pattern in TECH_PATTERNS:
        cleaned_name = re.sub(pattern, ' ', cleaned_name, flags=re.IGNORECASE)
    
    # 将点号替换为空格（保持单词分离）
    cleaned_name = re.sub(r'\.', ' ', cleaned_name)
    
    # 清理多余的空格
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    
    # 清理开头和结尾的空格和特殊字符
    cleaned_name = cleaned_name.strip(' .-')
    
    return cleaned_name

def find_imdb_rating(folder_name):
    """根据文件夹名称查找IMDB评分"""
    # 清理后的名称用于匹配
    clean_name = clean_folder_name(folder_name).lower()
    
    # 直接匹配
    for title, rating in IMDB_RATINGS.items():
        if title.lower() in clean_name or clean_name in title.lower():
            return rating
    
    # 模糊匹配关键词
    keywords_mapping = {
        '宫崎骏': 8.5,  # 宫崎骏作品平均评分
        'ghibli': 8.5,
        'studio ghibli': 8.5,
        '吉卜力': 8.5,
        '皮克斯': 8.0,  # 皮克斯平均评分
        'pixar': 8.0,
        '迪士尼': 7.5,  # 迪士尼动画平均评分
        'disney': 7.5,
        '梦工厂': 7.3,  # 梦工厂平均评分
        'dreamworks': 7.3,
    }
    
    for keyword, rating in keywords_mapping.items():
        if keyword in clean_name:
            return rating
    
    return None

def format_folder_name(original_name, imdb_rating=None):
    """格式化文件夹名称"""
    # 清理技术参数
    clean_name = clean_folder_name(original_name)
    
    # 如果有IMDB评分，添加到名称中
    if imdb_rating:
        # 检查是否已经包含评分
        if not re.search(r'\[\d+\.\d+\]', clean_name):
            clean_name = f"{clean_name} [{imdb_rating}]"
    
    return clean_name

def rename_animation_folders(base_path):
    """批量重命名动画文件夹"""
    base_path = Path(base_path)
    
    if not base_path.exists():
        print(f"错误：路径 {base_path} 不存在")
        return
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    print(f"开始处理目录：{base_path}")
    print("=" * 60)
    
    # 获取所有子文件夹
    folders = [f for f in base_path.iterdir() if f.is_dir()]
    
    for folder in sorted(folders):
        original_name = folder.name
        
        # 查找IMDB评分
        imdb_rating = find_imdb_rating(original_name)
        
        # 格式化新名称
        new_name = format_folder_name(original_name, imdb_rating)
        
        if new_name != original_name:
            new_path = folder.parent / new_name
            
            # 检查新路径是否已存在
            if new_path.exists():
                print(f"⚠️  跳过：{original_name} -> 目标路径已存在")
                skipped_count += 1
                continue
            
            try:
                # 重命名文件夹
                folder.rename(new_path)
                rating_info = f" [IMDB: {imdb_rating}]" if imdb_rating else " [无评分]"
                print(f"✅ 重命名：{original_name} -> {new_name}{rating_info}")
                renamed_count += 1
            except Exception as e:
                print(f"❌ 错误：重命名 {original_name} 失败 - {e}")
                error_count += 1
        else:
            rating_info = f" [IMDB: {imdb_rating}]" if imdb_rating else " [无评分]"
            print(f"⏭️  无需更改：{original_name}{rating_info}")
            skipped_count += 1
    
    print("=" * 60)
    print(f"处理完成！")
    print(f"重命名：{renamed_count} 个文件夹")
    print(f"跳过：{skipped_count} 个文件夹")
    print(f"错误：{error_count} 个文件夹")
    print(f"总计：{len(folders)} 个文件夹")

def preview_changes(base_path):
    """预览重命名更改（不实际执行）"""
    base_path = Path(base_path)
    
    if not base_path.exists():
        print(f"错误：路径 {base_path} 不存在")
        return
    
    print(f"预览重命名更改：{base_path}")
    print("=" * 60)
    
    folders = [f for f in base_path.iterdir() if f.is_dir()]
    
    for folder in sorted(folders):
        original_name = folder.name
        imdb_rating = find_imdb_rating(original_name)
        new_name = format_folder_name(original_name, imdb_rating)
        
        if new_name != original_name:
            rating_info = f" [IMDB: {imdb_rating}]" if imdb_rating else " [无评分]"
            print(f"📝 {original_name} -> {new_name}{rating_info}")
        else:
            rating_info = f" [IMDB: {imdb_rating}]" if imdb_rating else " [无评分]"
            print(f"⏭️  {original_name}{rating_info}")

# 动画目录路径
ANIMATION_PATH = "/Volumes/video/动画"

if __name__ == "__main__":
    import sys
    
    print("动画文件夹重命名工具 - 增强版技术参数清理")
    print(f"处理目录: {ANIMATION_PATH}")
    print("="*50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        # 预览模式
        print("🔍 预览模式")
        preview_changes(ANIMATION_PATH)
    else:
        # 直接执行重命名
        print("🚀 执行重命名操作")
        rename_animation_folders(ANIMATION_PATH)