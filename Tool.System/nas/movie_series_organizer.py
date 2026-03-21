#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电影系列整理器
自动识别和整理系列电影到专门的系列目录中
"""

import os
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/movie_series_organization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MovieSeriesOrganizer:
    def __init__(self, movie_base_path: str):
        self.movie_base_path = Path(movie_base_path)
        self.series_base_path = self.movie_base_path / "[系列]"
        self.stats = {
            'processed': 0,
            'moved': 0,
            'series_created': 0,
            'errors': 0
        }
        
        # 系列电影识别规则
        self.series_patterns = {
            # 中文系列
            '战狼系列': [r'战狼', r'Wolf\s*Warriors?'],
            '唐人街探案系列': [r'唐人街探案', r'Detective\s*Chinatown'],
            '叶问系列': [r'叶问', r'Ip\s*Man'],
            '功夫熊猫系列': [r'功夫熊猫', r'Kung\s*Fu\s*Panda'],
            '速度与激情系列': [r'速度与激情', r'Fast\s*(&|and)\s*Furious', r'The\s*Fast\s*and\s*the\s*Furious'],
            
            # 英文系列
            'Marvel复仇者联盟系列': [r'Avengers?', r'复仇者联盟'],
            'Marvel蜘蛛侠系列': [r'Spider[\-\s]*Man', r'蜘蛛侠'],
            'Marvel钢铁侠系列': [r'Iron\s*Man', r'钢铁侠'],
            'Marvel美国队长系列': [r'Captain\s*America', r'美国队长'],
            'Marvel雷神系列': [r'Thor(?!\s*Ragnarok)', r'雷神'],
            'Marvel X战警系列': [r'X[\-\s]*Men', r'X战警'],
            
            'DC蝙蝠侠系列': [r'Batman', r'蝙蝠侠', r'Dark\s*Knight'],
            'DC超人系列': [r'Superman', r'超人', r'Man\s*of\s*Steel'],
            
            '星球大战系列': [r'Star\s*Wars', r'星球大战'],
            '星际迷航系列': [r'Star\s*Trek', r'星际迷航'],
            '侏罗纪系列': [r'Jurassic', r'侏罗纪'],
            '异形系列': [r'Alien(?!s)', r'异形'],
            '异形大战铁血战士系列': [r'Aliens?\s*vs?\.?\s*Predators?', r'AVP'],
            '铁血战士系列': [r'Predators?', r'铁血战士'],
            '终结者系列': [r'Terminators?', r'终结者'],
            '黑客帝国系列': [r'Matrix', r'黑客帝国'],
            '变形金刚系列': [r'Transformers?', r'变形金刚'],
            
            '印第安纳琼斯系列': [r'Indiana\s*Jones', r'夺宝奇兵'],
            '碟中谍系列': [r'Mission[\s:]*Impossible', r'碟中谍'],
            '007系列': [r'James\s*Bond', r'007', r'Bond'],
            '谍影重重系列': [r'Bourne', r'谍影重重'],
            '虎胆龙威系列': [r'Die\s*Hard', r'虎胆龙威'],
            
            '指环王系列': [r'Lord\s*of\s*the\s*Rings', r'指环王'],
            '霍比特人系列': [r'Hobbit', r'霍比特人'],
            '哈利波特系列': [r'Harry\s*Potter', r'哈利[·\s]*波特'],
            
            '洛奇系列': [r'Rocky', r'洛奇'],
            '第一滴血系列': [r'Rambo', r'第一滴血'],
            '疯狂的麦克斯系列': [r'Mad\s*Max', r'疯狂的麦克斯'],
            
            '加勒比海盗系列': [r'Pirates\s*of\s*the\s*Caribbean', r'加勒比海盗'],
            '玩具总动员系列': [r'Toy\s*Story', r'玩具总动员'],
            '怪物史莱克系列': [r'Shrek', r'怪物史莱克'],
            '冰河世纪系列': [r'Ice\s*Age', r'冰河世纪'],
            '马达加斯加系列': [r'Madagascar', r'马达加斯加'],
            
            '这个男人来自地球系列': [r'这个男人来自地球', r'The\s*Man\s*from\s*Earth']
        }
    
    def identify_series(self, movie_name: str) -> str:
        """识别电影所属系列"""
        for series_name, patterns in self.series_patterns.items():
            for pattern in patterns:
                if re.search(pattern, movie_name, re.IGNORECASE):
                    return series_name
        return None
    
    def create_series_directory(self, series_name: str) -> Path:
        """创建系列目录"""
        series_path = self.series_base_path / series_name
        series_path.mkdir(parents=True, exist_ok=True)
        return series_path
    
    def move_to_series(self, movie_path: Path, series_name: str) -> bool:
        """将电影移动到系列目录"""
        try:
            series_dir = self.create_series_directory(series_name)
            target_path = series_dir / movie_path.name
            
            if target_path.exists():
                logger.warning(f"目标路径已存在: {target_path}")
                return False
            
            shutil.move(str(movie_path), str(target_path))
            logger.info(f"移动到系列: {movie_path.name} -> {series_name}/{movie_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"移动失败 {movie_path.name}: {e}")
            return False
    
    def organize_series(self, dry_run: bool = False) -> Dict:
        """整理系列电影"""
        logger.info("=== 开始系列电影整理 ===")
        
        if not self.movie_base_path.exists():
            logger.error(f"电影目录不存在: {self.movie_base_path}")
            return self.stats
        
        # 获取所有电影目录
        movie_dirs = [d for d in self.movie_base_path.iterdir() 
                     if d.is_dir() and not d.name.startswith('.') and not d.name.startswith('[')]
        
        logger.info(f"找到 {len(movie_dirs)} 个电影目录")
        
        series_movies = {}
        
        for movie_dir in movie_dirs:
            self.stats['processed'] += 1
            series_name = self.identify_series(movie_dir.name)
            
            if series_name:
                if series_name not in series_movies:
                    series_movies[series_name] = []
                series_movies[series_name].append(movie_dir)
                logger.info(f"识别系列: {movie_dir.name} -> {series_name}")
        
        # 移动系列电影
        for series_name, movies in series_movies.items():
            if len(movies) >= 2:  # 只有2部以上才创建系列
                logger.info(f"\n处理系列: {series_name} ({len(movies)}部电影)")
                
                if not dry_run:
                    self.stats['series_created'] += 1
                    
                for movie_path in movies:
                    if not dry_run:
                        if self.move_to_series(movie_path, series_name):
                            self.stats['moved'] += 1
                        else:
                            self.stats['errors'] += 1
                    else:
                        logger.info(f"[模拟] 将移动: {movie_path.name} -> {series_name}")
            else:
                logger.info(f"系列 {series_name} 只有1部电影，不创建系列目录")
        
        return self.stats
    
    def generate_report(self) -> str:
        """生成整理报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"movie_series_organization_report_{timestamp}.json"
        
        report_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'movie_base_path': str(self.movie_base_path),
            'series_base_path': str(self.series_base_path),
            'statistics': self.stats,
            'summary': {
                'total_operations': self.stats['moved'] + self.stats['errors'],
                'success_rate': f"{(self.stats['moved'] / max(1, self.stats['moved'] + self.stats['errors'])) * 100:.1f}%"
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"整理报告已保存: {report_file}")
        return report_file

def main():
    movie_path = "/Volumes/video/电影"
    
    if not os.path.exists(movie_path):
        print(f"❌ 电影目录不存在: {movie_path}")
        return
    
    organizer = MovieSeriesOrganizer(movie_path)
    
    # 先进行模拟运行
    print("\n🔍 模拟运行 - 预览系列整理计划...")
    organizer.organize_series(dry_run=True)
    
    # 询问是否执行
    response = input("\n是否执行系列整理? (y/N): ")
    if response.lower() == 'y':
        print("\n🚀 开始执行系列整理...")
        stats = organizer.organize_series(dry_run=False)
        organizer.generate_report()
        
        print(f"\n✅ 系列整理完成！")
        print(f"处理统计: {stats}")
    else:
        print("\n❌ 已取消系列整理")

if __name__ == "__main__":
    main()