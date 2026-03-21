#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能动画文件夹清理工具
功能：
1. 彻底清理技术参数
2. 保持合理的文件名格式
3. 添加IMDB评分
4. 处理重复文件夹
5. 智能空格处理
"""

import os
import re
import shutil
from datetime import datetime

# 动画IMDB评分数据库
IMDB_RATINGS = {
    # 经典动画系列
    '瑞克和莫蒂': 9.3, 'rick and morty': 9.3, 'rick morty': 9.3,
    '海贼王': 9.0, 'one piece': 9.0,
    '新世纪福音战士': 9.3, 'evangelion': 9.3, 'neon genesis evangelion': 9.3,
    '猫和老鼠': 8.6, 'tom and jerry': 8.6, 'tom jerry': 8.6,
    '龙珠': 8.7, 'dragon ball': 8.7, 'dragonball': 8.7,
    '火影忍者': 8.7, 'naruto': 8.7,
    '死神': 8.2, 'bleach': 8.2,
    '进击的巨人': 9.0, 'attack on titan': 9.0, 'shingeki no kyojin': 9.0,
    '鬼灭之刃': 8.7, 'demon slayer': 8.7, 'kimetsu no yaiba': 8.7,
    '我的英雄学院': 8.5, 'my hero academia': 8.5, 'boku no hero academia': 8.5,
    
    # 吉卜力工作室
    '吉卜力': 8.5, 'ghibli': 8.5, 'studio ghibli': 8.5,
    '千与千寻': 9.3, 'spirited away': 9.3,
    '龙猫': 8.2, 'totoro': 8.2, 'my neighbor totoro': 8.2,
    '天空之城': 8.0, 'castle in the sky': 8.0, 'laputa': 8.0,
    '魔女宅急便': 7.8, 'kiki delivery service': 7.8,
    '风之谷': 8.1, 'nausicaa': 8.1,
    '幽灵公主': 8.4, 'princess mononoke': 8.4, 'mononoke hime': 8.4,
    '哈尔的移动城堡': 8.2, 'howl moving castle': 8.2,
    
    # 迪士尼/皮克斯
    '玩具总动员': 8.3, 'toy story': 8.3,
    '冰雪奇缘': 7.4, 'frozen': 7.4,
    '狮子王': 8.5, 'lion king': 8.5,
    '美女与野兽': 8.0, 'beauty and the beast': 8.0,
    '小美人鱼': 7.6, 'little mermaid': 7.6,
    '阿拉丁': 8.0, 'aladdin': 8.0,
    '超人总动员': 8.0, 'incredibles': 8.0,
    '怪物公司': 8.1, 'monsters inc': 8.1,
    '寻梦环游记': 8.4, 'coco': 8.4,
    '疯狂动物城': 8.0, 'zootopia': 8.0,
    '魅力四射': 7.2, 'encanto': 7.2,
    
    # 梦工厂
    '怪物史莱克': 7.9, 'shrek': 7.9,
    '马达加斯加': 6.9, 'madagascar': 6.9,
    '功夫熊猫': 7.6, 'kung fu panda': 7.6,
    '驯龙高手': 8.1, 'how to train your dragon': 8.1,
    
    # 其他经典
    '哈利波特': 7.6, 'harry potter': 7.6,
    '指环王': 8.8, 'lord of the rings': 8.8,
    '蜘蛛侠': 7.3, 'spider man': 7.3, 'spiderman': 7.3,
    '蝙蝠侠': 7.5, 'batman': 7.5,
    '超人': 7.3, 'superman': 7.3,
    '变形金刚': 7.0, 'transformers': 7.0,
    '小黄人': 6.4, 'minions': 6.4, 'despicable me': 6.4,
    '冰河世纪': 7.5, 'ice age': 7.5,
    '里约大冒险': 6.9, 'rio': 6.9,
    '兰戈': 7.2, 'rango': 7.2,
    '机器人总动员': 8.4, 'wall e': 8.4, 'walle': 8.4,
    '飞屋环游记': 8.3, 'up': 8.3,
    '头脑特工队': 8.1, 'inside out': 8.1,
    '料理鼠王': 8.1, 'ratatouille': 8.1,
    '海底总动员': 8.2, 'finding nemo': 8.2,
    '汽车总动员': 7.2, 'cars': 7.2,
    '勇敢传说': 7.1, 'brave': 7.1,
    '无敌破坏王': 7.7, 'wreck it ralph': 7.7,
    '大英雄6': 7.8, 'big hero 6': 7.8,
    '奇迹男孩': 7.9, 'wonder': 7.9,
    '小王子': 7.7, 'little prince': 7.7,
    '你的名字': 8.2, 'your name': 8.2, 'kimi no na wa': 8.2,
    '天气之子': 7.5, 'weathering with you': 7.5,
    '声之形': 8.1, 'silent voice': 8.1, 'koe no katachi': 8.1,
    '言叶之庭': 7.4, 'garden of words': 7.4,
    '秒速5厘米': 7.6, '5 centimeters per second': 7.6,
    '云之彼端': 6.9, 'place promised': 6.9,
    '攻壳机动队': 8.0, 'ghost in the shell': 8.0,
    '阿基拉': 8.0, 'akira': 8.0,
    '钢之炼金术师': 9.1, 'fullmetal alchemist': 9.1,
    '死亡笔记': 8.9, 'death note': 8.9,
    '一拳超人': 8.7, 'one punch man': 8.7,
    '东京喰种': 7.8, 'tokyo ghoul': 7.8,
    '约定的梦幻岛': 8.5, 'promised neverland': 8.5,
    '咒术回战': 8.6, 'jujutsu kaisen': 8.6,
    '间谍过家家': 8.3, 'spy family': 8.3,
    '链锯人': 8.8, 'chainsaw man': 8.8,
    '辉夜大小姐': 8.4, 'kaguya sama': 8.4,
    '紫罗兰永恒花园': 8.5, 'violet evergarden': 8.5,
    '你遭难了吗': 6.8, 'are you lost': 6.8,
    '工作细胞': 7.6, 'cells at work': 7.6,
    '关于我转生变成史莱姆这档事': 8.1, 'that time i got reincarnated as a slime': 8.1,
    '无职转生': 8.4, 'mushoku tensei': 8.4,
    '盾之勇者成名录': 7.6, 'rising of the shield hero': 7.6,
    '为美好的世界献上祝福': 8.1, 'konosuba': 8.1,
    'overlord': 7.9,
    '幼女战记': 7.7, 'saga of tanya the evil': 7.7,
    '异世界四重奏': 7.2, 'isekai quartet': 7.2,
    '重新来过': 8.2, 're zero': 8.2,
    '刀剑神域': 7.6, 'sword art online': 7.6,
    '加速世界': 7.2, 'accel world': 7.2,
    '约会大作战': 7.1, 'date a live': 7.1,
    '魔法禁书目录': 7.3, 'index': 7.3,
    '某科学的超电磁炮': 7.8, 'railgun': 7.8,
    '学园都市': 7.0, 'academy city': 7.0,
    '食戟之灵': 8.1, 'food wars': 8.1, 'shokugeki no soma': 8.1,
    '黑子的篮球': 8.2, 'kuroko basketball': 8.2,
    '排球少年': 8.7, 'haikyuu': 8.7,
    '网球王子': 8.1, 'prince of tennis': 8.1,
    '灌篮高手': 9.0, 'slam dunk': 9.0,
    '足球小将': 7.8, 'captain tsubasa': 7.8,
    '棒球大联盟': 8.3, 'major': 8.3,
    '头文字d': 8.5, 'initial d': 8.5,
    '湾岸midnight': 7.6, 'wangan midnight': 7.6,
    '极速车魂': 7.4, 'redline': 7.4,
    '高达': 7.8, 'gundam': 7.8,
    '新世纪evangelion': 9.3,
    '机动战士': 7.8, 'mobile suit': 7.8,
    '超时空要塞': 7.5, 'macross': 7.5,
    '银河英雄传说': 9.0, 'legend of galactic heroes': 9.0,
    '星际牛仔': 8.8, 'cowboy bebop': 8.8,
    '三一万能侠': 7.2, 'trigun': 7.2,
    '黑礁': 8.1, 'black lagoon': 8.1,
    '寄生兽': 8.3, 'parasyte': 8.3,
    '东京残响': 7.8, 'terror in resonance': 7.8,
    '心理测量者': 8.2, 'psycho pass': 8.2,
    '攻壳机动队sac': 8.5, 'ghost in the shell sac': 8.5,
    '银魂': 8.7, 'gintama': 8.7,
    '妖精的尾巴': 7.9, 'fairy tail': 7.9,
    '七大罪': 7.7, 'seven deadly sins': 7.7,
    '黑色四叶草': 8.2, 'black clover': 8.2,
    '我的英雄学院': 8.5,
    '炎炎消防队': 7.7, 'fire force': 7.7,
    '灵能百分百': 8.6, 'mob psycho 100': 8.6,
    '一人之下': 8.0, 'the outcast': 8.0,
    '狐妖小红娘': 8.2, 'fox spirit matchmaker': 8.2,
    '全职高手': 8.1, 'the king avatar': 8.1,
    '斗罗大陆': 7.8, 'soul land': 7.8,
    '斗破苍穹': 7.6, 'battle through the heavens': 7.6,
    '完美世界': 7.5, 'perfect world': 7.5,
    '武庚纪': 7.7, 'wugengji': 7.7,
    '秦时明月': 8.0, 'qin moon': 8.0,
    '天行九歌': 7.9, 'nine songs of the moving heavens': 7.9,
    '画江湖': 7.6, 'drawing jianghu': 7.6,
    '镇魂街': 8.1, 'rakshasa street': 8.1,
    '端脑': 7.4, '端脑': 7.4,
    '雄兵连': 7.8, 'super god': 7.8,
    '西行纪': 7.5, 'monkey king hero is back': 7.5,
    '大圣归来': 7.8, 'monkey king hero is back': 7.8,
    '哪吒': 7.4, 'nezha': 7.4,
    '白蛇': 7.0, 'white snake': 7.0,
    '姜子牙': 6.9, 'legend of deification': 6.9,
    '熊出没': 6.5, 'boonie bears': 6.5,
    '喜羊羊': 6.0, 'pleasant goat': 6.0,
    '大头儿子': 6.2, 'big head son': 6.2,
    '蜡笔小新': 8.2, 'crayon shin chan': 8.2,
    '樱桃小丸子': 8.0, 'chibi maruko chan': 8.0,
    '哆啦a梦': 8.2, 'doraemon': 8.2,
    '名侦探柯南': 8.9, 'detective conan': 8.9, 'case closed': 8.9,
    '数码宝贝': 7.9, 'digimon': 7.9,
    '宠物小精灵': 8.9, 'pokemon': 8.9,
    '游戏王': 7.3, 'yu gi oh': 7.3,
    '美少女战士': 7.8, 'sailor moon': 7.8,
    '圣斗士星矢': 8.3, 'saint seiya': 8.3,
    '北斗神拳': 8.1, 'fist of the north star': 8.1,
    '城市猎人': 7.8, 'city hunter': 7.8,
    '鲁邦三世': 7.6, 'lupin iii': 7.6,
    '柯南': 8.9, 'conan': 8.9,
    '金田一': 8.1, 'kindaichi': 8.1,
    '棋魂': 8.1, 'hikaru no go': 8.1,
    '网球王子': 8.1,
    '足球小将': 7.8,
    '灌篮高手': 9.0,
    '棒球英豪': 8.4, 'touch': 8.4,
    '足球风云': 7.9, 'captain tsubasa': 7.9,
    '头文字d': 8.5,
    '湾岸midnight': 7.6,
    '极速车魂': 7.4,
    '高达seed': 8.0, 'gundam seed': 8.0,
    '高达00': 8.1, 'gundam 00': 8.1,
    '高达w': 7.9, 'gundam wing': 7.9,
    '高达g': 7.6, 'gundam g': 7.6,
    '高达x': 7.4, 'gundam x': 7.4,
    '高达age': 6.8, 'gundam age': 6.8,
    '高达铁血': 7.5, 'gundam iron blooded orphans': 7.5,
    '高达创战者': 7.3, 'gundam build fighters': 7.3,
    '机动战士高达': 7.8,
    '机动战士z高达': 8.2, 'mobile suit zeta gundam': 8.2,
    '机动战士zz高达': 7.6, 'mobile suit gundam zz': 7.6,
    '机动战士高达逆袭的夏亚': 7.8, 'chars counterattack': 7.8,
    '机动战士高达f91': 7.1, 'gundam f91': 7.1,
    '机动战士v高达': 7.3, 'victory gundam': 7.3,
    '超时空要塞': 7.5,
    '超时空要塞plus': 7.8, 'macross plus': 7.8,
    '超时空要塞7': 7.2, 'macross 7': 7.2,
    '超时空要塞zero': 7.6, 'macross zero': 7.6,
    '超时空要塞frontier': 7.9, 'macross frontier': 7.9,
    '超时空要塞delta': 7.1, 'macross delta': 7.1,
    '银河英雄传说': 9.0,
    '银河英雄传说die neue these': 8.1, 'legend of galactic heroes die neue these': 8.1,
    '星际牛仔': 8.8,
    '星际牛仔天国之门': 7.8, 'cowboy bebop movie': 7.8,
    '三一万能侠': 7.2,
    '三一万能侠badlands rumble': 7.4, 'trigun badlands rumble': 7.4,
    '黑礁': 8.1,
    '黑礁roberta血迹': 8.3, 'black lagoon robertas blood trail': 8.3,
    '寄生兽': 8.3,
    '寄生兽生命的准则': 8.3, 'parasyte maxim': 8.3,
    '东京残响': 7.8,
    '心理测量者': 8.2,
    '心理测量者2': 7.5, 'psycho pass 2': 7.5,
    '心理测量者3': 7.2, 'psycho pass 3': 7.2,
    '心理测量者ss': 7.8, 'psycho pass sinners of the system': 7.8,
    '攻壳机动队sac': 8.5,
    '攻壳机动队sac 2nd gig': 8.7, 'ghost in the shell sac 2nd gig': 8.7,
    '攻壳机动队sac solid state society': 8.1, 'ghost in the shell sac solid state society': 8.1,
    '攻壳机动队arise': 7.2, 'ghost in the shell arise': 7.2,
    '攻壳机动队sac 2045': 6.8, 'ghost in the shell sac 2045': 6.8,
    '银魂': 8.7,
    '银魂延长战': 8.8, 'gintama enchousen': 8.8,
    '银魂完结篇': 9.0, 'gintama kanketsu hen': 9.0,
    '银魂银之魂篇': 9.1, 'gintama shirogane no tamashii hen': 9.1,
    '银魂the final': 8.9, 'gintama the final': 8.9,
    '妖精的尾巴': 7.9,
    '妖精的尾巴final season': 7.8, 'fairy tail final season': 7.8,
    '七大罪': 7.7,
    '七大罪戒律的复活': 6.9, 'seven deadly sins revival of the commandments': 6.9,
    '七大罪神之怒': 6.1, 'seven deadly sins wrath of the gods': 6.1,
    '七大罪龙之审判': 5.8, 'seven deadly sins dragons judgement': 5.8,
    '黑色四叶草': 8.2,
    '我的英雄学院': 8.5,
    '我的英雄学院第二季': 8.6, 'my hero academia season 2': 8.6,
    '我的英雄学院第三季': 8.7, 'my hero academia season 3': 8.7,
    '我的英雄学院第四季': 8.5, 'my hero academia season 4': 8.5,
    '我的英雄学院第五季': 8.2, 'my hero academia season 5': 8.2,
    '我的英雄学院第六季': 8.8, 'my hero academia season 6': 8.8,
    '炎炎消防队': 7.7,
    '炎炎消防队贰之章': 7.9, 'fire force season 2': 7.9,
    '灵能百分百': 8.6,
    '灵能百分百ii': 8.8, 'mob psycho 100 ii': 8.8,
    '灵能百分百iii': 8.9, 'mob psycho 100 iii': 8.9,
}

# 需要清理的技术参数模式（更全面）
TECH_PATTERNS = [
    # 视频源和质量（更严格的匹配）
    r'BluRay(?:\.Remux)?(?:\.x26[45])?(?:\.DTS)?',
    r'UHD\.BluRay(?:\.x26[45])?',
    r'WEB-?DL(?:\.x26[45])?(?:\.H26[45])?',
    r'WEBDL(?:\.x26[45])?(?:\.H26[45])?',  # 添加无连字符版本
    r'WEBRip(?:\.x26[45])?',
    r'BDRip(?:\.x26[45])?',
    r'DVDRip(?:\.x264)?',
    r'HDRip(?:\.x264)?',
    r'HMAX\.WEB-DL',
    r'NF\.WEB-DL',
    r'Bilibili\.WEB-DL',
    r'PTHweb',
    r'PTH',
    r'MNHD',
    r'FLUX',
    r'mUHD',
    r'PTHOME',
    r'PTHome',
    
    # 编码格式
    r'x26[45](?:\.10bit)?',
    r'H\.?26[45](?:\.10bit)?',  # 支持H264和H.264
    r'HEVC(?:\.10bit)?',
    r'AVC(?:\.10bit)?',
    r'MPEG-2',
    r'10bit',
    r'8bit',
    
    # 分辨率
    r'\d{3,4}[pi]',  # 1080p, 720p, 480i等
    r'2160p',
    r'4K',
    r'UHD',
    
    # 音频格式
    r'DTS(?:-HD)?(?:\.MA)?(?:\.\d+)?(?:\.\d+Audio)?',
    r'TrueHD(?:\.\d+\.\d+)?',
    r'Atmos',
    r'AC3',
    r'AAC',
    r'FLAC',
    r'DD[P]?\d+\.\d+',
    r'DTSHD-MA\d+\.\d+',
    r'\d+Audio',
    r'\d+\.\d+Audio',
    r'\d+语',  # 如"四语"
    
    # HDR和色彩
    r'HDR(?:10)?',
    r'Dolby\.Vision',
    r'DV',
    
    # 发布组和标识
    r'￡[^\s]+',
    r'@[A-Za-z0-9]+',
    r'-[A-Z]{2,}$',
    r'-[A-Za-z0-9]+$',
    r'\[[A-Za-z0-9]+\]',
    r'\([A-Za-z0-9]+\)',
    
    # 其他技术参数
    r'Remux',
    r'mUHD',
    r'GREENOTEA',
    r'WiKi',
    r'FRDS',
    r'BeiTai',
    r'HDS',
    r'cXcY',
    r'OurBits',
    r'CMCT小鱼',
    r'小鱼',
    
    # 语言和字幕
    r'中英字幕',
    r'英字幕',
    r'中字幕',
    r'字幕',
    r'Mandarin',
    r'CHS',
    r'CHT',
    r'DYGC',
    
    # 年份范围（如20142016）
    r'\d{4}\d{4}',  # 连续的年份
    
    # 特殊字符和格式
    r'\¿',  # 特殊字符
    r'TX',   # 可能的发布组
]

def normalize_name_for_matching(name):
    """标准化名称用于匹配"""
    # 转换为小写
    normalized = name.lower()
    
    # 移除常见分隔符
    normalized = re.sub(r'[.\-_\s]+', ' ', normalized)
    
    # 移除数字和特殊字符（保留基本字母）
    normalized = re.sub(r'[^a-zA-Z\u4e00-\u9fff\s]', ' ', normalized)
    
    # 清理多余空格
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def find_imdb_rating(folder_name):
    """查找IMDB评分"""
    normalized = normalize_name_for_matching(folder_name)
    
    # 直接匹配
    if normalized in IMDB_RATINGS:
        return IMDB_RATINGS[normalized]
    
    # 部分匹配
    for key, rating in IMDB_RATINGS.items():
        if key in normalized or normalized in key:
            return rating
    
    # 分词匹配
    words = normalized.split()
    for key, rating in IMDB_RATINGS.items():
        key_words = key.split()
        if len(set(words) & set(key_words)) >= min(2, len(key_words)):
            return rating
    
    return None

def clean_tech_params(name):
    """智能清理技术参数"""
    cleaned = name
    
    # 应用所有清理模式
    for pattern in TECH_PATTERNS:
        cleaned = re.sub(pattern, ' ', cleaned, flags=re.IGNORECASE)
    
    # 将点号替换为空格
    cleaned = re.sub(r'\.', ' ', cleaned)
    
    # 清理多余的空格和特殊字符
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'^[\s.-]+|[\s.-]+$', '', cleaned)
    
    return cleaned.strip()

def generate_clean_name(folder_name):
    """生成清理后的文件名"""
    # 移除所有现有的评分信息和重复标签
    base_name = re.sub(r'\s*\[[^\]]*\]', '', folder_name)
    base_name = re.sub(r'\s*\([^\)]*\)', '', base_name)
    
    # 清理技术参数
    cleaned = clean_tech_params(base_name)
    
    # 进一步清理空格和特殊字符
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # 查找IMDB评分
    rating = find_imdb_rating(cleaned)
    
    # 添加评分信息（只添加一次）
    if rating:
        final_name = f"{cleaned} [IMDB: {rating}]"
    else:
        final_name = f"{cleaned} [无评分]"
    
    return final_name

def find_duplicate_folders(animation_path):
    """查找重复的文件夹"""
    folders = []
    duplicates = []
    
    for item in os.listdir(animation_path):
        item_path = os.path.join(animation_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
    
    # 按清理后的名称分组
    name_groups = {}
    for folder in folders:
        # 移除所有评分信息和括号内容
        clean_base = re.sub(r'\s*\[[^\]]*\]', '', folder)
        clean_base = re.sub(r'\s*\([^\)]*\)', '', clean_base)
        clean_base = clean_tech_params(clean_base)
        clean_base = normalize_name_for_matching(clean_base)
        
        # 进一步标准化：移除常见的变体
        clean_base = re.sub(r'\s*(complete|collection|series|全集|合集)\s*', ' ', clean_base, flags=re.IGNORECASE)
        clean_base = re.sub(r'\s+', ' ', clean_base).strip()
        
        if clean_base not in name_groups:
            name_groups[clean_base] = []
        name_groups[clean_base].append(folder)
    
    # 找出重复项
    for clean_name, folder_list in name_groups.items():
        if len(folder_list) > 1:
            duplicates.append(folder_list)
    
    return duplicates

def handle_duplicates(animation_path, duplicates):
    """处理重复文件夹"""
    for duplicate_group in duplicates:
        print(f"\n发现重复文件夹组：")
        for i, folder in enumerate(duplicate_group):
            folder_path = os.path.join(animation_path, folder)
            size = sum(os.path.getsize(os.path.join(dirpath, filename))
                      for dirpath, dirnames, filenames in os.walk(folder_path)
                      for filename in filenames) / (1024*1024*1024)  # GB
            print(f"  {i+1}. {folder} ({size:.2f} GB)")
        
        # 自动选择保留最大的文件夹
        sizes = []
        for folder in duplicate_group:
            folder_path = os.path.join(animation_path, folder)
            size = sum(os.path.getsize(os.path.join(dirpath, filename))
                      for dirpath, dirnames, filenames in os.walk(folder_path)
                      for filename in filenames)
            sizes.append(size)
        
        keep_index = sizes.index(max(sizes))
        keep_folder = duplicate_group[keep_index]
        
        print(f"自动保留最大的文件夹: {keep_folder}")
        
        # 删除其他文件夹
        for i, folder in enumerate(duplicate_group):
            if i != keep_index:
                folder_path = os.path.join(animation_path, folder)
                print(f"删除重复文件夹: {folder}")
                shutil.rmtree(folder_path)

def smart_clean_animation_folders(animation_path):
    """智能清理动画文件夹"""
    print(f"开始智能清理动画文件夹: {animation_path}")
    print("="*60)
    
    # 1. 处理重复文件夹
    print("\n🔍 检查重复文件夹...")
    duplicates = find_duplicate_folders(animation_path)
    if duplicates:
        print(f"发现 {len(duplicates)} 组重复文件夹")
        handle_duplicates(animation_path, duplicates)
    else:
        print("未发现重复文件夹")
    
    # 2. 重命名文件夹
    print("\n🚀 开始重命名文件夹...")
    
    folders = []
    for item in os.listdir(animation_path):
        item_path = os.path.join(animation_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for folder_name in sorted(folders):
        try:
            new_name = generate_clean_name(folder_name)
            
            if new_name != folder_name:
                old_path = os.path.join(animation_path, folder_name)
                new_path = os.path.join(animation_path, new_name)
                
                # 检查新名称是否已存在
                if os.path.exists(new_path):
                    print(f"⚠️  跳过（目标已存在）: {folder_name}")
                    skipped_count += 1
                    continue
                
                os.rename(old_path, new_path)
                print(f"✅ 重命名: {folder_name} -> {new_name}")
                renamed_count += 1
            else:
                print(f"⏭️  跳过（无需更改）: {folder_name}")
                skipped_count += 1
                
        except Exception as e:
            print(f"❌ 错误: {folder_name} - {str(e)}")
            error_count += 1
    
    print("\n" + "="*60)
    print("智能清理完成！")
    print(f"重命名: {renamed_count} 个文件夹")
    print(f"跳过: {skipped_count} 个文件夹")
    print(f"错误: {error_count} 个文件夹")
    print(f"总计: {len(folders)} 个文件夹")
    
    return renamed_count, skipped_count, error_count

if __name__ == "__main__":
    animation_path = "/Volumes/video/动画"
    
    print("智能动画文件夹清理工具")
    print(f"处理目录: {animation_path}")
    print("功能: 清理技术参数 + 添加IMDB评分 + 处理重复文件夹")
    print("="*60)
    
    if os.path.exists(animation_path):
        smart_clean_animation_folders(animation_path)
    else:
        print(f"错误: 目录不存在 - {animation_path}")