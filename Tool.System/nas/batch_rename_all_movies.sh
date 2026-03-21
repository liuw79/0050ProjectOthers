#!/bin/bash

# 电影批量重命名脚本 - 完整版
# 处理所有剩余的英文电影目录

# set -e # 注释掉严格模式，允许脚本继续执行

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
SUCCESS_COUNT=0
SKIP_COUNT=0
ERROR_COUNT=0

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 重命名函数
rename_item() {
    local old_name="$1"
    local new_name="$2"
    
    if [[ ! -e "$old_name" ]]; then
        log_warning "文件/目录不存在: $old_name"
        ((SKIP_COUNT++))
        return 1
    fi
    
    if [[ -e "$new_name" ]]; then
        log_warning "目标已存在，跳过: $new_name"
        ((SKIP_COUNT++))
        return 1
    fi
    
    if mv "$old_name" "$new_name" 2>/dev/null; then
        log_success "重命名: $old_name -> $new_name"
        ((SUCCESS_COUNT++))
        return 0
    else
        log_error "重命名失败: $old_name"
        ((ERROR_COUNT++))
        return 1
    fi
}

log_info "开始批量重命名所有英文电影..."
log_info "工作目录: $(pwd)"

# 电影重命名列表
log_info "开始处理电影重命名..."

# 处理第一批电影
rename_item "Moana.2.2024.4K.BluRay.DoVi.x265.10bit.Atmos.TrueHD7.1-WiKi" "海洋奇缘2 Moana 2 (2024)"
rename_item "Sin.City.A.Dame.to.Kill.For.2014.1080p.BluRay.x265.10bit.DTS-PTH" "罪恶之城2 Sin City A Dame to Kill For (2014)"
rename_item "Extended Collector's Edition Disc 1 (2009)" "指环王 Extended Collector's Edition Disc 1 (2009)"
rename_item "I Can Only Imagine (2018)" "我只能想象 I Can Only Imagine (2018)"
rename_item "If You Are the One (2008)" "非诚勿扰 If You Are the One (2008)"
rename_item "Ikiru (1952)" "生之欲 Ikiru (1952)"
rename_item "In the Mood for Love (2000)" "花样年华 In the Mood for Love (2000)"
rename_item "Incendies (2010)" "焦土之城 Incendies (2010)"
rename_item "Inception (2010)" "盗梦空间 Inception (2010)"
rename_item "Indiana Jones and the Last Crusade (1989)" "夺宝奇兵3 Indiana Jones and the Last Crusade (1989)"
rename_item "Inglourious Basterds (2009)" "无耻混蛋 Inglourious Basterds (2009)"
rename_item "Interstellar (2014)" "星际穿越 Interstellar (2014)"
rename_item "It's a Wonderful Life (1946)" "生活多美好 It's a Wonderful Life (1946)"
rename_item "Joker (2019)" "小丑 Joker (2019)"
rename_item "Journey.to.the.West.The.Demons.Strike.Back.2017.720p.BluRay.x264-WiKi (2017)" "西游伏妖篇 Journey to the West The Demons Strike Back (2017)"
rename_item "Jurassic World (2015)" "侏罗纪世界 Jurassic World (2015)"
rename_item "Jurassic.Park.1993.1080p.BluRay.DTS.2Aduio.x265-10bit-HDS (1993)" "侏罗纪公园 Jurassic Park (1993)"
rename_item "Jurassic.Park.III.2001.1080p.BluRay.DTS.2Aduio.x265-10bit-HDS (2001)" "侏罗纪公园3 Jurassic Park III (2001)"
rename_item "Just Heroes (1989)" "义胆群英 Just Heroes (1989)"
rename_item "Justice.My.Foot.1992.1080p.BluRay.x264-WiKi (1992)" "审死官 Justice My Foot (1992)"
rename_item "King of Comedy (1999)" "喜剧之王 King of Comedy (1999)"
rename_item "King.of.Beggars.1992.720p.BluRay.x264-WiKi (1992)" "武状元苏乞儿 King of Beggars (1992)"
rename_item "Knives Out (2019)" "利刃出鞘 Knives Out (2019)"
rename_item "La La Land (2016)" "爱乐之城 La La Land (2016)"
rename_item "Lawrence of Arabia (1962)" "阿拉伯的劳伦斯 Lawrence of Arabia (1962)"
rename_item "Life Is Beautiful (1997)" "美丽人生 Life Is Beautiful (1997)"
rename_item "Life of Pi (2012)" "少年派的奇幻漂流 Life of Pi (2012)"
rename_item "Love Actually (2003)" "真爱至上 Love Actually (2003)"
rename_item "Mad Max Fury Road (2015)" "疯狂的麦克斯4 Mad Max Fury Road (2015)"
rename_item "Memento (2000)" "记忆碎片 Memento (2000)"
rename_item "Minari (2020)" "米纳里 Minari (2020)"
rename_item "Moonlight (2016)" "月光男孩 Moonlight (2016)"
rename_item "My Neighbor Totoro (1988)" "龙猫 My Neighbor Totoro (1988)"
rename_item "No Country for Old Men (2007)" "老无所依 No Country for Old Men (2007)"
rename_item "Nomadland (2020)" "无依之地 Nomadland (2020)"
rename_item "Once Upon a Time in Hollywood (2019)" "好莱坞往事 Once Upon a Time in Hollywood (2019)"
rename_item "Once Upon a Time in the West (1968)" "西部往事 Once Upon a Time in the West (1968)"
rename_item "Parasite (2019)" "寄生虫 Parasite (2019)"
rename_item "Psycho (1960)" "惊魂记 Psycho (1960)"
rename_item "Pulp Fiction (1994)" "低俗小说 Pulp Fiction (1994)"
rename_item "Roma (2018)" "罗马 Roma (2018)"
rename_item "Saving Private Ryan (1998)" "拯救大兵瑞恩 Saving Private Ryan (1998)"
rename_item "Schindler's List (1993)" "辛德勒的名单 Schindler's List (1993)"
rename_item "Se7en (1995)" "七宗罪 Se7en (1995)"
rename_item "Shutter Island (2010)" "禁闭岛 Shutter Island (2010)"
rename_item "Spirited Away (2001)" "千与千寻 Spirited Away (2001)"
rename_item "Star Wars The Empire Strikes Back (1980)" "星球大战2 Star Wars The Empire Strikes Back (1980)"
rename_item "Star.Trek.VIII.First.Contact (1996)" "星际迷航8 Star Trek VIII First Contact (1996)"
rename_item "Star.Trek.X.Nemesis (2002)" "星际迷航10 Star Trek X Nemesis (2002)"
rename_item "Suk.Suk (2020)" "叔叔 Suk Suk (2020)"
rename_item "Sully (2016)" "萨利机长 Sully (2016)"
rename_item "Summer Detective 2019 (2019)" "夏日侦探 Summer Detective (2019)"
rename_item "Sunset Blvd. (1950)" "日落大道 Sunset Blvd (1950)"
rename_item "Systemsprenger 2019 (2019)" "系统破坏者 Systemsprenger (2019)"
rename_item "Talvisota elokuvan kuvaukset Keuruulla (1989)" "冬季战争 Talvisota (1989)"
rename_item "The Accountant (2016)" "会计刺客 The Accountant (2016)"
rename_item "The Apartment (1960)" "公寓春光 The Apartment (1960)"
rename_item "The Aviator 2004 (2004)" "飞行家 The Aviator (2004)"
rename_item "The Best Offer (2013)" "最佳出价 The Best Offer (2013)"
rename_item "The Blind Side (2009)" "弱点 The Blind Side (2009)"
rename_item "The Boat (1981)" "从海底出击 The Boat (1981)"
rename_item "The Boss Baby (2017)" "宝贝老板 The Boss Baby (2017)"
rename_item "The Bridges of Madison County (1995)" "廊桥遗梦 The Bridges of Madison County (1995)"
rename_item "The Corporation (2003)" "公司 The Corporation (2003)"
rename_item "The Croods - A New Age (2020)" "疯狂原始人2 The Croods A New Age (2020)"
rename_item "The Farewell (2019)" "别告诉她 The Farewell (2019)"
rename_item "The Father (2020)" "困在时间里的父亲 The Father (2020)"
rename_item "The Good, the Bad and the Ugly (1966)" "黄金三镖客 The Good the Bad and the Ugly (1966)"
rename_item "The Great Dictator (1940)" "大独裁者 The Great Dictator (1940)"
rename_item "The Intouchables (2011)" "触不可及 The Intouchables (2011)"
rename_item "The Invisible Man (2020)" "隐形人 The Invisible Man (2020)"
rename_item "The Kid (1921)" "寻子遇仙记 The Kid (1921)"
rename_item "The Lives of Others (2006)" "窃听风暴 The Lives of Others (2006)"
rename_item "The Lucky Guy (1998)" "行运一条龙 The Lucky Guy (1998)"
rename_item "THE LUNCHBOX (2013)" "午餐盒 The Lunchbox (2013)"
rename_item "The Man from Earth - Holocene (2017)" "这个男人来自地球2 The Man from Earth Holocene (2017)"
rename_item "The Mermaid (2016)" "美人鱼 The Mermaid (2016)"
rename_item "The Old Guard (2020)" "永生守卫 The Old Guard (2020)"
rename_item "The Piano (1993)" "钢琴课 The Piano (1993)"
rename_item "The Piano Teacher (2001)" "钢琴教师 The Piano Teacher (2001)"
rename_item "The Sting (1973)" "骗中骗 The Sting (1973)"
rename_item "The Swordsman In Double Flag Town - Blu-ray™ (1991)" "双旗镇刀客 The Swordsman In Double Flag Town (1991)"
rename_item "The Tourist (2010)" "致命伴旅 The Tourist (2010)"
rename_item "The Wandering Earth II (2023)" "流浪地球2 The Wandering Earth II (2023)"
rename_item "The Wolf of Wall Street (2013)" "华尔街之狼 The Wolf of Wall Street (2013)"
rename_item "The Yellow Sea 2010 (2010)" "黄海 The Yellow Sea (2010)"
rename_item "The.Beach.2000.Open.Matte.1080p.WEB-DL.DD5.1.H.264-spartanec163 (2000)" "海滩 The Beach (2000)"
rename_item "The.God.of.Cookery.1996.720p.HDTV.x264.2Audio-HDCTV (1996)" "食神 The God of Cookery (1996)"
rename_item "The.Human.Centipede.2009.BluRay.1080p.DTS.x264-CHD (2009)" "人体蜈蚣 The Human Centipede (2009)"
rename_item "The.Kings.Man (2021)" "王牌特工：源起 The King's Man (2021)"
rename_item "The.Lost.World.Jurassic.Park.1997.1080p.BluRay.DTS.2Aduio.x265-10bit-HDS (1997)" "侏罗纪公园2 The Lost World Jurassic Park (1997)"
rename_item "Time of the Gypsies (1988)" "流浪者之歌 Time of the Gypsies (1988)"
rename_item "Togo (2019)" "多哥 Togo (2019)"
rename_item "Tomorrowland (2015)" "明日世界 Tomorrowland (2015)"
rename_item "Tropic.Thunder.Directors.Cut (2008)" "热带惊雷 Tropic Thunder Directors Cut (2008)"
rename_item "Umibe.no.Etranger (2020)" "海边的异邦人 Umibe no Etranger (2020)"
rename_item "Un.sac.de.billes (2017)" "一袋弹珠 Un sac de billes (2017)"
rename_item "Under the Open Sky (2021)" "在蓝天下 Under the Open Sky (2021)"
rename_item "Up (2009)" "飞屋环游记 Up (2009)"
rename_item "Vettai (2012)" "猎人 Vettai (2012)"
rename_item "Vive L'Amour (1995)" "爱情万岁 Vive L'Amour (1995)"
rename_item "Vychislitel AKA The Calculator [2014] 1080p BluRay - HJ (2014)" "计算器 The Calculator (2014)"
rename_item "WALL·E (2008)" "机器人总动员 WALL-E (2008)"
rename_item "Western Stars (2019)" "西部明星 Western Stars (2019)"
rename_item "What a Wonderful Family 2 2017 1080p BluRay DD5.1 x265-10bit-HDS (2017)" "家族之苦2 What a Wonderful Family 2 (2017)"
rename_item "What a Wonderful Family 3 My Wife My Life 2018 1080p BluRay DTS x264-HDS (2018)" "家族之苦3 What a Wonderful Family 3 (2018)"
rename_item "When.Fortune.Smiles.1990.BluRay.720p.DTS x264-CHD (1990)" "笑傲江湖 When Fortune Smiles (1990)"
rename_item "Whiplash (2014)" "爆裂鼓手 Whiplash (2014)"
rename_item "Wild Bill (2011)" "狂野比尔 Wild Bill (2011)"
rename_item "Witness for the Prosecution (1957)" "控方证人 Witness for the Prosecution (1957)"
rename_item "Yi Yi (2000) (2000)" "一一 Yi Yi (2000)"
rename_item "Your Name. (2016)" "你的名字 Your Name (2016)"
rename_item "Your Place or Mine (1998)" "你的地方还是我的地方 Your Place or Mine (1998)"
rename_item "Zack.Snyders.Justice.League.2021.4K.UHD.BluRay.ATMOS.HDR.x265-W4NK3R (2021)" "扎克·施奈德版正义联盟 Zack Snyder's Justice League (2021)"

# 统计结果
log_info "\n=== 重命名完成统计 ==="
log_success "成功重命名: $SUCCESS_COUNT 个"
log_warning "跳过处理: $SKIP_COUNT 个"
log_error "处理失败: $ERROR_COUNT 个"

# 最终目录统计
log_info "\n=== 最终目录统计 ==="
TOTAL_COUNT=$(ls | wc -l | tr -d ' ')
CHINESE_COUNT=$(ls | grep -c '^[\u4e00-\u9fff]' || echo "0")
ENGLISH_COUNT=$(ls | grep -E '^[A-Z]' | grep -v 'HEVC编码\|CMCT\|RARBG' | wc -l | tr -d ' ')

log_info "总目录数: $TOTAL_COUNT"
log_info "中文名目录: $CHINESE_COUNT 个 ($(echo "scale=1; $CHINESE_COUNT * 100 / $TOTAL_COUNT" | bc -l 2>/dev/null || echo "0")%)"
log_info "剩余英文目录: $ENGLISH_COUNT 个"

log_success "电影批量重命名完成！"