#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名电视目录中缺少中文名称的文件夹
"""

import os
import subprocess
from pathlib import Path

def batch_rename_tv_folders():
    tv_directory = "/Volumes/video/电视"
    
    # 需要重命名的文件夹映射
    rename_mapping = [
        ("How the Universe Works Season 1 2010 [无评分]", "宇宙是如何运行的.How.the.Universe.Works.Season.1.2010 [无评分]"),
        ("Inside The Human Body 2011 [无评分]", "人体内旅行.Inside.The.Human.Body.2011 [无评分]"),
        ("Inside.Planet.Earth.2009 [无评分]", "地球内部之旅.Inside.Planet.Earth.2009 [无评分]"),
        ("Jade.Japan.45.Day.Itinerary.2022.NGB [无评分]", "翡翠日本.Jade.Japan.45.Day.Itinerary.2022.NGB [无评分]"),
        ("Kyūkyoku [无评分]", "究极.Kyūkyoku [无评分]"),
        ("Lie.To.Me.Season 1.2Audio.19977 [无评分]", "别对我撒谎.Lie.To.Me.Season.1.2Audio.19977 [无评分]"),
        ("Like.A.Flowing.River.2020.Season 2 [无评分]", "大江大河.Like.A.Flowing.River.2020.Season.2 [无评分]"),
        ("Lost.in.Space.2018.Season 1.CsS [无评分]", "迷失太空.Lost.in.Space.2018.Season.1.CsS [无评分]"),
        ("Love.Death.&.Robots.Season 1 [无评分]", "爱死亡和机器人.Love.Death.&.Robots.Season.1 [无评分]"),
        ("Masters.of.Sex.Season 1.DD5.1 [无评分]", "性爱大师.Masters.of.Sex.Season.1.DD5.1 [无评分]"),
        ("Mexico Earth's Festival of Life 2017 GER..DIY.mulpsn [无评分]", "墨西哥.地球生命节.Mexico.Earths.Festival.of.Life.2017.GER.DIY.mulpsn [无评分]"),
        ("Mom.Season 1-5.AMZN.NTb [无评分]", "老妈.Mom.Season.1-5.AMZN.NTb [无评分]"),
        ("My.Chief.and.My.Regiment.2009 [无评分]", "我的团长我的团.My.Chief.and.My.Regiment.2009 [无评分]"),
        ("Once.Upon.a.Bite.Season 1.2018 [无评分]", "风味人间.Once.Upon.a.Bite.Season.1.2018 [无评分]"),
        ("One.Strange.Rock.2018.Season 1 [无评分]", "奇异星球.One.Strange.Rock.2018.Season.1 [无评分]"),
        ("Qin.Empire.Alliance.Season 3.2017.PuTao [无评分]", "大秦帝国.联盟.Qin.Empire.Alliance.Season.3.2017.PuTao [无评分]"),
        ("Soul.2020.DSNP.EVO [无评分]", "心灵奇旅.Soul.2020.DSNP.EVO [无评分]"),
        ("Space.Force.Season 1.2020 [无评分]", "太空部队.Space.Force.Season.1.2020 [无评分]"),
        ("Star.Trek.Picard.Season 1 [无评分]", "星际迷航.皮卡德.Star.Trek.Picard.Season.1 [无评分]"),
        ("Suits.Season.1.4.DTC [无评分]", "金装律师.Suits.Season.1.4.DTC [无评分]"),
        ("The.Grand.Tour.Season 3.AMZN.Ao [无评分]", "大巡游.The.Grand.Tour.Season.3.AMZN.Ao [无评分]"),
        ("The.Movies.Season 1.GUACAMOLE [无评分]", "电影.The.Movies.Season.1.GUACAMOLE [无评分]"),
        ("Three.Kingdoms.2010.WiKi [无评分]", "三国.Three.Kingdoms.2010.WiKi [无评分]"),
        ("Tiny.World.Season 1 [无评分]", "小小世界.Tiny.World.Season.1 [无评分]"),
        ("Tokyo.Love.Story.1991.Season 1.LPCM.CHD [无评分]", "东京爱情故事.Tokyo.Love.Story.1991.Season.1.LPCM.CHD [无评分]"),
        ("Word.of.Honor.2021.HDCTV [无评分]", "山河令.Word.of.Honor.2021.HDCTV [无评分]")
    ]
    
    print("🚀 开始批量重命名电视文件夹...")
    print("=" * 50)
    
    renamed_count = 0
    
    for old_name, new_name in rename_mapping:
        old_path = Path(tv_directory) / old_name
        new_path = Path(tv_directory) / new_name
        
        if old_path.exists():
            if not new_path.exists():
                try:
                    old_path.rename(new_path)
                    print(f"✅ 重命名成功: {old_name}")
                    print(f"   -> {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ 重命名失败: {old_name} - {e}")
            else:
                print(f"⚠️ 目标已存在，跳过: {new_name}")
        else:
            print(f"🔍 文件夹不存在，跳过: {old_name}")
    
    print("\n" + "=" * 50)
    print(f"🎉 批量重命名完成！总共处理了 {renamed_count} 个文件夹")
    
    # 最终统计
    print("\n📊 最终统计：")
    total_folders = len([f for f in Path(tv_directory).iterdir() if f.is_dir()])
    print(f"  📁 文件夹总数: {total_folders}")
    
    # 检查还有没有缺少中文名称的文件夹
    import re
    folders_without_chinese = []
    for folder in Path(tv_directory).iterdir():
        if folder.is_dir() and not re.search(r'[\u4e00-\u9fff]', folder.name):
            folders_without_chinese.append(folder.name)
    
    if folders_without_chinese:
        print(f"  ⚠️ 仍缺少中文名称: {len(folders_without_chinese)} 个")
        print("  需要处理的文件夹：")
        for folder in folders_without_chinese[:5]:
            print(f"    - {folder}")
        if len(folders_without_chinese) > 5:
            print(f"    ... 还有 {len(folders_without_chinese) - 5} 个")
    else:
        print("  🎊 所有文件夹都有中文名称！")

if __name__ == "__main__":
    batch_rename_tv_folders()