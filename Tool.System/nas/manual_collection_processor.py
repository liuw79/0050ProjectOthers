#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动处理Piano.tutorial.collection目录
"""

import os
import shutil
from pathlib import Path

def process_piano_collection():
    """处理Piano.tutorial.collection目录"""
    
    # 路径定义
    collection_path = Path('/Volumes/video/教程/钢琴教程专区/📦 其他教材/Piano.tutorial.collection')
    piano_zone_path = Path('/Volumes/video/教程/钢琴教程专区')
    
    # 分类映射
    category_mapping = {
        # 小汤系列
        '小汤一册': '🎹 小汤系列',
        '小汤二册': '🎹 小汤系列', 
        '小汤三册': '🎹 小汤系列',
        '小汤四册': '🎹 小汤系列',
        '小汤五册': '🎹 小汤系列',
        '02于斯课堂-【小汤】汤普森简易钢琴教程123册 高清 价值398元--2.36GB': '🎹 小汤系列',
        '03于斯课堂{大汤｝约翰汤普森现代钢琴教程12册 高清': '🎹 小汤系列',
        
        # 车尔尼系列
        '06于斯课堂-车尔尼作品599 51课时 高清 价值198元--1.01GB': '🎼 车尔尼系列',
        '15《车尔尼849钢琴流畅练习曲》49集+配套教材 价值298元--175MB': '🎼 车尔尼系列',
        
        # 哈农练指法
        '05于斯课堂-《哈农钢琴练指法》 钢琴教学视频  34节课 高清 价值198元--948M': '🎵 哈农练指法',
        '14 《哈农钢琴练指法第二版》高清 价值398元--3.95GB《电脑观看》': '🎵 哈农练指法',
        '20 方百里教学视频合集': '🎵 哈农练指法',
        '音阶和弦琶音-琴拿手': '🎵 哈农练指法',
        
        # 拜厄教程
        '04 于斯课堂-《拜厄钢琴基本教程》初级钢琴入门高清教学视频-2.92G 111课时 高清 价值298元--2.92GB': '📚 拜厄教程',
        '09 孩子们的拜厄 价值188元--1.34GB《电脑观看》': '📚 拜厄教程',
        '菲伯尔钢琴基础': '📚 拜厄教程',
        '07于斯课堂-菲伯尔钢琴基础教程100节 钢琴考级 钢琴入门 高清 价值298元--2.34GB': '📚 拜厄教程',
        '16 巴斯蒂安第1套 高清 价值298元--4.17GB': '📚 拜厄教程',
        '17 巴斯蒂安第2套 高清 价值298元--4.13GB': '📚 拜厄教程',
        '18 巴斯蒂安第3套 高清 价值298元--4.12GB': '📚 拜厄教程',
        '于斯课堂-巴斯蒂安钢琴教程第一册2.2G 88课时 198元': '📚 拜厄教程',
        '小贝零基础钢琴教学': '📚 拜厄教程',
        '25 教你巧学钢琴-陆佳': '📚 拜厄教程',
        '10 钢琴基础教程全套1-4 高清 价值888元--25.77GB': '📚 拜厄教程',
        '12 幼儿钢琴入门 高清 价值398元--12.83GB《电脑观看》': '📚 拜厄教程',
        
        # 考级教程
        '全国钢琴考级26张光盘原版视频': '🎭 考级教程',
        '周铭孙《全国钢琴演奏考级》': '🎭 考级教程',
        '08于斯课堂-上音钢琴考级1-10视频教程 高清  价值288元--3.38GB': '🎭 考级教程',
        
        # 乐理基础
        '23 陈俊宇《钢琴乐理的秘密》': '🎓 乐理基础',
        '宋大叔教音乐最新全集': '🎓 乐理基础',
        
        # 其他教材
        '初级': '📦 其他教材',
        '中级': '📦 其他教材', 
        '高级': '📦 其他教材',
        '钢琴一加一全套（4套教程共1100元)': '📦 其他教材',
        '钢琴自学-梦中的婚礼': '📦 其他教材',
        '刘诗昆《教你弹钢琴全集》': '📦 其他教材',
        '周铭孙《教钢琴与学钢琴的要领与决窍》': '📦 其他教材',
        '22 林文信钢琴『电子琴』视频教学教程全套': '📦 其他教材',
        '21 林文信钢琴教学合集': '📦 其他教材',
        '24 钢琴教材和曲谱': '📦 其他教材',
        '小贝编曲课': '📦 其他教材',
        '小贝即兴伴奏课': '📦 其他教材',
        '13 长江钢琴2015大师讲堂 高清 价值988元--31.37GB': '📦 其他教材',
        '19周广仁，王海波-布格缪勒钢琴进阶25曲》【49集全】': '📦 其他教材'
    }
    
    print("🚀 开始处理Piano.tutorial.collection目录")
    
    if not collection_path.exists():
        print(f"❌ 目录不存在: {collection_path}")
        return
    
    # 获取所有子目录
    subdirs = [d for d in collection_path.iterdir() if d.is_dir()]
    print(f"📊 发现 {len(subdirs)} 个子目录")
    
    moved_count = 0
    
    for subdir in subdirs:
        subdir_name = subdir.name
        
        # 查找对应的分类
        target_category = category_mapping.get(subdir_name)
        
        if target_category:
            # 目标路径
            target_category_path = piano_zone_path / target_category
            target_path = target_category_path / subdir_name
            
            # 确保目标分类目录存在
            target_category_path.mkdir(exist_ok=True)
            
            try:
                # 移动目录
                shutil.move(str(subdir), str(target_path))
                print(f"✅ 移动: {subdir_name} → {target_category}")
                moved_count += 1
            except Exception as e:
                print(f"❌ 移动失败: {subdir_name} - {e}")
        else:
            print(f"⚠️ 未找到分类: {subdir_name}")
    
    print(f"\n📊 处理完成，共移动 {moved_count} 个目录")
    
    # 检查是否还有剩余内容
    remaining_items = list(collection_path.iterdir())
    remaining_dirs = [item for item in remaining_items if item.is_dir()]
    
    if remaining_dirs:
        print(f"\n⚠️ 还有 {len(remaining_dirs)} 个目录未处理:")
        for item in remaining_dirs:
            print(f"   - {item.name}")
    else:
        print("\n🎉 所有目录都已处理完成!")
        
        # 如果只剩下文件，可以删除整个collection目录
        if not remaining_dirs:
            try:
                # 删除剩余文件和目录
                shutil.rmtree(collection_path)
                print(f"🗑️ 已删除空的集合目录: {collection_path.name}")
            except Exception as e:
                print(f"⚠️ 删除集合目录失败: {e}")

if __name__ == '__main__':
    process_piano_collection()