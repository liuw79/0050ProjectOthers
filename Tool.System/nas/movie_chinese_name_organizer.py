#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电影中文名标准化工具
功能：将英文名电影重命名为中文名，提升浏览体验
作者：Assistant
创建时间：2025-01-24
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path

class MovieChineseNameOrganizer:
    def __init__(self, movie_dir="/Volumes/video/电影"):
        self.movie_dir = Path(movie_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"logs/movie_chinese_name_organization_{self.timestamp}.log"
        self.report_file = f"movie_chinese_name_organization_report_{self.timestamp}.json"
        
        # 确保日志目录存在
        os.makedirs("logs", exist_ok=True)
        
        # 统计信息
        self.stats = {
            "total_processed": 0,
            "renamed_count": 0,
            "skipped_count": 0,
            "error_count": 0,
            "renamed_movies": [],
            "skipped_movies": [],
            "errors": []
        }
        
        # 英文名到中文名的映射字典
        self.name_mapping = {
            # 经典电影
            "12 Angry Men": "十二怒汉",
            "1917": "1917",
            "A Clockwork Orange": "发条橙",
            "Alien": "异形",
            "Aliens": "异形2",
            "Amadeus": "莫扎特传",
            "Apocalypse Now": "现代启示录",
            "Avatar": "阿凡达",
            "Back to the Future": "回到未来",
            "Blade Runner": "银翼杀手",
            "Casablanca": "卡萨布兰卡",
            "Citizen Kane": "公民凯恩",
            "Dune": "沙丘",
            "E.T. the Extra-Terrestrial": "E.T.外星人",
            "Forrest Gump": "阿甘正传",
            "Gladiator": "角斗士",
            "Gone with the Wind": "乱世佳人",
            "Goodfellas": "好家伙",
            "Inception": "盗梦空间",
            "Interstellar": "星际穿越",
            "Jaws": "大白鲨",
            "Joker": "小丑",
            "Lawrence of Arabia": "阿拉伯的劳伦斯",
            "The Matrix": "黑客帝国",
            "Matrix": "黑客帝国",
            "Parasite": "寄生虫",
            "Psycho": "惊魂记",
            "Pulp Fiction": "低俗小说",
            "Schindler's List": "辛德勒的名单",
            "The Shawshank Redemption": "肖申克的救赎",
            "Shawshank Redemption": "肖申克的救赎",
            "Singin' in the Rain": "雨中曲",
            "Star Wars": "星球大战",
            "Taxi Driver": "出租车司机",
            "Terminator": "终结者",
            "The Dark Knight": "蝙蝠侠：黑暗骑士",
            "The Godfather": "教父",
            "The Lord of the Rings": "指环王",
            "The Shining": "闪灵",
            "The Wizard of Oz": "绿野仙踪",
            "Titanic": "泰坦尼克号",
            "Vertigo": "迷魂记",
            
            # 动作电影
            "Die Hard": "虎胆龙威",
            "Fast & Furious": "速度与激情",
            "John Wick": "疾速追杀",
            "Mad Max": "疯狂的麦克斯",
            "Mission Impossible": "碟中谍",
            "Rambo": "第一滴血",
            "Rocky": "洛奇",
            "Top Gun": "壮志凌云",
            
            # 科幻电影
            "Aliens": "异形2",
            "Arrival": "降临",
            "Ex Machina": "机械姬",
            "Gravity": "地心引力",
            "Her": "她",
            "Minority Report": "少数派报告",
            "The Martian": "火星救援",
            "Total Recall": "全面回忆",
            
            # 恐怖电影
            "Halloween": "月光光心慌慌",
            "Nightmare on Elm Street": "猛鬼街",
            "Scream": "惊声尖叫",
            "The Exorcist": "驱魔人",
            "The Thing": "怪形",
            
            # 喜剧电影
            "Airplane!": "空前绝后满天飞",
            "Anchorman": "王牌播音员",
            "Borat": "波拉特",
            "Dumb and Dumber": "阿呆与阿瓜",
            "Ghostbusters": "捉鬼敢死队",
            "Groundhog Day": "土拨鼠之日",
            "Home Alone": "小鬼当家",
            "The Hangover": "宿醉",
            "Zoolander": "超级名模",
            
            # 动画电影
            "Finding Nemo": "海底总动员",
            "Frozen": "冰雪奇缘",
            "Inside Out": "头脑特工队",
            "Lion King": "狮子王",
            "Monsters Inc": "怪兽电力公司",
            "Shrek": "怪物史莱克",
            "Spirited Away": "千与千寻",
            "Toy Story": "玩具总动员",
            "Up": "飞屋环游记",
            "WALL-E": "机器人总动员",
            
            # 剧情电影
            "A Beautiful Mind": "美丽心灵",
            "Beautiful Mind": "美丽心灵",
            "Dead Poets Society": "死亡诗社",
            "Good Will Hunting": "心灵捕手",
            "The Green Mile": "绿里奇迹",
            "Green Mile": "绿里奇迹",
            "Life is Beautiful": "美丽人生",
            "One Flew Over the Cuckoo's Nest": "飞越疯人院",
            "Rain Man": "雨人",
            "Saving Private Ryan": "拯救大兵瑞恩",
            "The Pianist": "钢琴家",
            "The Pursuit of Happyness": "当幸福来敲门",
            
            # 更多经典电影
            "Braveheart": "勇敢的心",
            "Cast Away": "荒岛余生",
            "Chicago": "芝加哥",
            "Crash": "撞车",
            "The Departed": "无间道风云",
            "Departed": "无间道风云",
            "Django Unchained": "被解救的姜戈",
            "Fight Club": "搏击俱乐部",
            "Heat": "盗火线",
            "Her": "她",
            "Kill Bill": "杀死比尔",
            "Leon": "这个杀手不太冷",
            "Memento": "记忆碎片",
            "No Country for Old Men": "老无所依",
            "Oldboy": "老男孩",
            "The Prestige": "致命魔术",
            "Prestige": "致命魔术",
            "Reservoir Dogs": "落水狗",
            "Se7en": "七宗罪",
            "Seven": "七宗罪",
            "The Silence of the Lambs": "沉默的羔羊",
            "Silence of the Lambs": "沉默的羔羊",
            "There Will Be Blood": "血色将至",
            "The Usual Suspects": "非常嫌疑犯",
            "Usual Suspects": "非常嫌疑犯",
            "American Beauty": "美国丽人",
            "L.A. Confidential": "洛城机密",
            "Requiem for a Dream": "梦之安魂曲",
            "Eternal Sunshine of the Spotless Mind": "暖暖内含光",
            "Lost in Translation": "迷失东京",
            "The Royal Tenenbaums": "天才一族",
            "Fargo": "冰血暴",
            "The Big Lebowski": "谋杀绿脚趾",
            "Burn After Reading": "阅后即焚",
            "True Grit": "大地惊雷",
            "Inside Llewyn Davis": "醉乡民谣",
            "Birdman": "鸟人",
            "Whiplash": "爆裂鼓手",
            "La La Land": "爱乐之城",
            "Moonlight": "月光男孩",
            "The Shape of Water": "水形物语",
            "Three Billboards Outside Ebbing, Missouri": "三块广告牌",
            "Green Book": "绿皮书",
            "Nomadland": "无依之地",
            "Minari": "米纳里",
            "CODA": "健听女孩",
            "Everything Everywhere All at Once": "瞬息全宇宙",
            "The Banshees of Inisherin": "伊尼舍林的报丧女妖",
            "Tár": "塔尔",
            "The Fabelmans": "造梦之家",
            "Top Gun: Maverick": "壮志凌云：独行侠",
            "Elvis": "猫王",
            "The Batman": "新蝙蝠侠",
            "Dune: Part Two": "沙丘2",
            "Oppenheimer": "奥本海默",
            "Barbie": "芭比",
            "Killers of the Flower Moon": "花月杀手",
            "The Zone of Interest": "关注区",
            "Past Lives": "过往人生",
            "Anatomy of a Fall": "坠落的审判",
            "The Holdovers": "留校联盟",
            "American Fiction": "美国小说",
            "Maestro": "指挥家",
            "Ferrari": "法拉利",
            "Napoleon": "拿破仑",
            "The Creator": "造物主",
            "Air": "飞人乔丹",
            "Cocaine Bear": "可卡因熊",
            "M3GAN": "机械姬",
            "Scream VI": "惊声尖叫6",
            "John Wick: Chapter 4": "疾速追杀4",
            "Fast X": "速度与激情10",
            "Transformers: Rise of the Beasts": "变形金刚：超能勇士崛起",
            "Spider-Man: Across the Spider-Verse": "蜘蛛侠：纵横宇宙",
            "Guardians of the Galaxy Vol. 3": "银河护卫队3",
            "The Flash": "闪电侠",
            "Indiana Jones and the Dial of Destiny": "夺宝奇兵5：命运转盘",
            "Mission: Impossible – Dead Reckoning Part One": "碟中谍7：致命清算（上）",
            "Elemental": "疯狂元素城",
            "The Little Mermaid": "小美人鱼",
            "Peter Pan & Wendy": "小飞侠彼得潘与温蒂",
            "The Super Mario Bros. Movie": "超级马力欧兄弟大电影",
            "Dungeons & Dragons: Honor Among Thieves": "龙与地下城：侠盗荣耀",
            "65": "65",
            "Creed III": "奎迪3",
            "Ant-Man and the Wasp: Quantumania": "蚁人与黄蜂女：量子狂潮",
            "Avatar: The Way of Water": "阿凡达：水之道",
            "Black Panther: Wakanda Forever": "黑豹2：瓦坎达万岁",
            "Thor: Love and Thunder": "雷神4：爱与雷霆",
            "Doctor Strange in the Multiverse of Madness": "奇异博士2：疯狂多元宇宙",
            "Morbius": "莫比亚斯：暗夜博士",
            "The Northman": "北欧人",
            "Sonic the Hedgehog 2": "刺猬索尼克2",
            "Fantastic Beasts: The Secrets of Dumbledore": "神奇动物：邓布利多之谜",
            "The Bad Guys": "坏蛋联盟",
            "Turning Red": "青春变形记",
            "Encanto": "魅力四射",
            "West Side Story": "西区故事",
            "Spider-Man: No Way Home": "蜘蛛侠：英雄无归",
            "The Matrix Resurrections": "黑客帝国：矩阵重启",
            "Eternals": "永恒族",
            "No Time to Die": "007：无暇赴死",
            "Venom: Let There Be Carnage": "毒液2：屠杀开始",
            "Shang-Chi and the Legend of the Ten Rings": "尚气与十环传奇",
            "Free Guy": "失控玩家",
            "The Suicide Squad": "X特遣队：全员集结",
            "Black Widow": "黑寡妇",
            "F9: The Fast Saga": "速度与激情9",
            "A Quiet Place Part II": "寂静之地2",
            "Cruella": "黑白魔女库伊拉",
            "Godzilla vs. Kong": "哥斯拉大战金刚",
            "Zack Snyder's Justice League": "扎克·施奈德版正义联盟",
            "Wonder Woman 1984": "神奇女侠1984",
            "Mulan": "花木兰",
            "Tenet": "信条",
            "Soul": "心灵奇旅",
            "Onward": "1/2的魔法",
            "Birds of Prey": "猛禽小队和哈莉·奎茵",
            "Bad Boys for Life": "绝地战警：疾速追击",
            
            # 战争电影
            "Apocalypse Now": "现代启示录",
            "Black Hawk Down": "黑鹰坠落",
            "Full Metal Jacket": "全金属外壳",
            "Hacksaw Ridge": "血战钢锯岭",
            "Platoon": "野战排",
            "We Were Soldiers": "我们曾经是战士",
            
            # 传记电影
            "Gandhi": "甘地传",
            "Malcolm X": "马尔科姆·X",
            "Patton": "巴顿将军",
            "Ray": "雷",
            "Walk the Line": "与歌同行",
            
            # 犯罪电影
            "Casino": "赌场",
            "Donnie Brasco": "忠奸人",
            "Scarface": "疤面煞星",
            "The Untouchables": "铁面无私",
            
            # 浪漫电影
            "Casablanca": "卡萨布兰卡",
            "Ghost": "人鬼情未了",
            "Notebook": "恋恋笔记本",
            "Roman Holiday": "罗马假日",
            "Sleepless in Seattle": "西雅图夜未眠",
            "Titanic": "泰坦尼克号",
            "When Harry Met Sally": "当哈利遇到莎莉",
            
            # 音乐电影
            "Bohemian Rhapsody": "波西米亚狂想曲",
            "La La Land": "爱乐之城",
            "Mamma Mia": "妈妈咪呀",
            "Moulin Rouge": "红磨坊",
            "Sound of Music": "音乐之声",
            
            # 体育电影
            "Field of Dreams": "梦幻之地",
            "Moneyball": "点球成金",
            "Remember the Titans": "冲锋陷阵",
            "Rudy": "鲁迪",
            
            # 西部电影
            "Butch Cassidy and the Sundance Kid": "虎豹小霸王",
            "Dances with Wolves": "与狼共舞",
            "Good Bad and Ugly": "黄金三镖客",
            "Magnificent Seven": "豪勇七蛟龙",
            "Unforgiven": "不可饶恕",
            
            # 家庭电影
            "E.T.": "E.T.外星人",
            "Goonies": "七宝奇谋",
            "Princess Bride": "公主新娘",
            "Wizard of Oz": "绿野仙踪"
        }
    
    def log_message(self, message):
        """记录日志消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def extract_movie_title(self, folder_name):
        """从文件夹名称中提取电影标题"""
        # 移除年份、分辨率、编码等信息
        title = folder_name
        
        # 移除年份 (1900-2099)
        title = re.sub(r'\b(19|20)\d{2}\b', '', title)
        
        # 移除分辨率信息
        title = re.sub(r'\b(720p|1080p|2160p|4K|UHD|HDR|DV|IMAX)\b', '', title, flags=re.IGNORECASE)
        
        # 移除编码信息
        title = re.sub(r'\b(x264|x265|H264|H265|HEVC|AVC|WEB-DL|BluRay|BDRip|DVDRip)\b', '', title, flags=re.IGNORECASE)
        
        # 移除音频信息
        title = re.sub(r'\b(DDP5\.1|DTS|AAC|AC3|Atmos|TrueHD)\b', '', title, flags=re.IGNORECASE)
        
        # 移除发布组信息
        title = re.sub(r'-[A-Za-z0-9]+$', '', title)
        
        # 移除多余的点、空格和连字符
        title = re.sub(r'[.\-_]+', ' ', title)
        title = title.strip()
        
        return title
    
    def find_chinese_name(self, english_title):
        """查找英文标题对应的中文名"""
        # 清理标题
        clean_title = english_title.strip()
        
        # 直接匹配
        if clean_title in self.name_mapping:
            return self.name_mapping[clean_title]
        
        # 精确匹配（考虑常见变体）
        for eng_name, chi_name in self.name_mapping.items():
            # 完全匹配
            if eng_name.lower() == clean_title.lower():
                return chi_name
            
            # 匹配主标题（去除副标题）
            main_title = clean_title.split(' - ')[0].split(': ')[0]
            if eng_name.lower() == main_title.lower():
                return chi_name
            
            # 匹配系列电影（如 Star Wars）
            if len(eng_name.split()) > 1 and eng_name.lower() in clean_title.lower():
                # 确保是完整词匹配，避免误匹配
                words = eng_name.lower().split()
                title_words = clean_title.lower().split()
                if all(word in title_words for word in words):
                    return chi_name
        
        return None
    
    def should_skip_folder(self, folder_name):
        """判断是否应该跳过该文件夹"""
        skip_patterns = [
            r'^\[合集\]',  # 合集目录
            r'^\[系列\]',  # 系列目录
            r'^\.',       # 隐藏文件夹
            r'^@',        # 特殊标记文件夹
        ]
        
        for pattern in skip_patterns:
            if re.match(pattern, folder_name):
                return True
        
        # 如果已经是中文名，跳过
        if re.search(r'[\u4e00-\u9fff]', folder_name):
            return True
        
        return False
    
    def rename_movie(self, old_path, new_name):
        """重命名电影文件夹"""
        try:
            parent_dir = old_path.parent
            new_path = parent_dir / new_name
            
            # 检查新路径是否已存在
            if new_path.exists():
                self.log_message(f"目标路径已存在，跳过重命名: {new_path}")
                return False
            
            # 执行重命名
            old_path.rename(new_path)
            self.log_message(f"重命名成功: {old_path.name} -> {new_name}")
            return True
            
        except Exception as e:
            self.log_message(f"重命名失败: {old_path.name} -> {new_name}, 错误: {str(e)}")
            return False
    
    def process_movies(self, dry_run=True):
        """处理电影目录中的所有电影"""
        self.log_message(f"开始电影中文名标准化 - {'模拟运行' if dry_run else '实际执行'}")
        self.log_message(f"目标目录: {self.movie_dir}")
        
        if not self.movie_dir.exists():
            self.log_message(f"错误: 电影目录不存在 - {self.movie_dir}")
            return
        
        # 获取所有电影文件夹
        movie_folders = []
        for item in self.movie_dir.iterdir():
            if item.is_dir() and not self.should_skip_folder(item.name):
                movie_folders.append(item)
        
        self.log_message(f"找到 {len(movie_folders)} 个需要处理的电影文件夹")
        
        # 处理每个电影文件夹
        for folder_path in movie_folders:
            self.stats["total_processed"] += 1
            folder_name = folder_path.name
            
            # 提取电影标题
            movie_title = self.extract_movie_title(folder_name)
            
            # 查找中文名
            chinese_name = self.find_chinese_name(movie_title)
            
            if chinese_name:
                # 构建新的文件夹名（保留原有的技术信息）
                # 提取年份
                year_match = re.search(r'\b(19|20)\d{2}\b', folder_name)
                year = year_match.group() if year_match else ""
                
                # 提取分辨率信息
                resolution_match = re.search(r'\b(720p|1080p|2160p|4K|UHD)\b', folder_name, re.IGNORECASE)
                resolution = resolution_match.group() if resolution_match else ""
                
                # 构建新名称
                new_name = chinese_name
                if year:
                    new_name += f" ({year})"
                if resolution:
                    new_name += f" {resolution}"
                
                if dry_run:
                    self.log_message(f"[模拟] 将重命名: {folder_name} -> {new_name}")
                    self.stats["renamed_movies"].append({
                        "original": folder_name,
                        "new_name": new_name,
                        "chinese_title": chinese_name
                    })
                    self.stats["renamed_count"] += 1
                else:
                    if self.rename_movie(folder_path, new_name):
                        self.stats["renamed_movies"].append({
                            "original": folder_name,
                            "new_name": new_name,
                            "chinese_title": chinese_name
                        })
                        self.stats["renamed_count"] += 1
                    else:
                        self.stats["errors"].append({
                            "folder": folder_name,
                            "error": "重命名失败"
                        })
                        self.stats["error_count"] += 1
            else:
                self.log_message(f"未找到中文名映射: {folder_name} (提取标题: {movie_title})")
                self.stats["skipped_movies"].append({
                    "folder": folder_name,
                    "extracted_title": movie_title,
                    "reason": "未找到中文名映射"
                })
                self.stats["skipped_count"] += 1
        
        # 生成报告
        self.generate_report()
        
        # 输出统计信息
        self.log_message("\n=== 处理统计 ===")
        self.log_message(f"总处理数量: {self.stats['total_processed']}")
        self.log_message(f"重命名数量: {self.stats['renamed_count']}")
        self.log_message(f"跳过数量: {self.stats['skipped_count']}")
        self.log_message(f"错误数量: {self.stats['error_count']}")
        
        if self.stats['total_processed'] > 0:
            success_rate = (self.stats['renamed_count'] / self.stats['total_processed']) * 100
            self.log_message(f"成功率: {success_rate:.1f}%")
    
    def generate_report(self):
        """生成详细报告"""
        report = {
            "timestamp": self.timestamp,
            "summary": self.stats,
            "details": {
                "renamed_movies": self.stats["renamed_movies"],
                "skipped_movies": self.stats["skipped_movies"],
                "errors": self.stats["errors"]
            }
        }
        
        with open(self.report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.log_message(f"详细报告已生成: {self.report_file}")

def main():
    organizer = MovieChineseNameOrganizer()
    
    print("电影中文名标准化工具")
    print("=" * 50)
    print("1. 模拟运行 (推荐，先查看效果)")
    print("2. 实际执行")
    print("3. 退出")
    
    while True:
        choice = input("\n请选择操作 (1-3): ").strip()
        
        if choice == "1":
            organizer.process_movies(dry_run=True)
            break
        elif choice == "2":
            confirm = input("确认要执行实际重命名操作吗？(yes/no): ").strip().lower()
            if confirm in ['yes', 'y', '是']:
                organizer.process_movies(dry_run=False)
            else:
                print("操作已取消")
            break
        elif choice == "3":
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()