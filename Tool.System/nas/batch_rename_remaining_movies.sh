#!/bin/bash

# 批量重命名剩余英文电影目录脚本
# 处理之前脚本遗漏的电影目录
# 作者：Assistant
# 日期：$(date +%Y-%m-%d)

# 设置目标目录
TARGET_DIR="/Volumes/video/电影"

# 检查目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "错误：目标目录不存在: $TARGET_DIR"
    exit 1
fi

# 进入目标目录
cd "$TARGET_DIR" || exit 1

echo "开始处理剩余英文电影目录"
echo "目标目录: $TARGET_DIR"
echo "时间: $(date)"
echo "="*50

# 计数器
SUCCESS_COUNT=0
SKIP_COUNT=0
FAIL_COUNT=0

# 重命名函数
rename_movie() {
    local old_name="$1"
    local new_name="$2"
    
    # 检查原目录是否存在
    if [ -d "$old_name" ]; then
        # 检查目标目录是否已存在
        if [ -d "$new_name" ]; then
            echo "⚠️  目标已存在，跳过: $old_name -> $new_name"
            ((SKIP_COUNT++))
        else
            # 执行重命名
            if mv "$old_name" "$new_name" 2>/dev/null; then
                echo "✅ 重命名成功: $old_name -> $new_name"
                ((SUCCESS_COUNT++))
            else
                echo "❌ 重命名失败: $old_name -> $new_name"
                ((FAIL_COUNT++))
            fi
        fi
    else
        echo "⚠️  原目录不存在: $old_name"
        ((SKIP_COUNT++))
    fi
}

# 执行重命名操作
process_renames() {
    # 处理剩余的电影目录
    rename_movie "Extended Collector's Edition Disc 1 (2009)" "指环王扩展收藏版光盘1 Extended Collector's Edition Disc 1 (2009)"
    rename_movie "Journey.to.the.West.The.Demons.Strike.Back.2017.720p.BluRay.x264-WiKi (2017)" "西游伏妖篇 Journey to the West The Demons Strike Back (2017)"
    rename_movie "Justice.My.Foot.1992.1080p.BluRay.x264-WiKi (1992)" "审死官 Justice My Foot (1992)"
    rename_movie "King.of.Beggars.1992.720p.BluRay.x264-WiKi (1992)" "武状元苏乞儿 King of Beggars (1992)"
    rename_movie "King.of.Comedy.1999.HDTV.720p.AC3.2Audio.x264-CHDTV (1999)" "喜剧之王 King of Comedy (1999)"
    rename_movie "Kis.Uykusu (2014)" "冬眠 Kis Uykusu (2014)"
    rename_movie "Knockout - Blu-ray™ (2020)" "拳击手 Knockout (2020)"
    rename_movie "Koe.no.katachi (2016)" "声之形 Koe no katachi (2016)"
    rename_movie "L.A. Confidential (1997)" "洛城机密 L.A. Confidential (1997)"
    rename_movie "La.grande.bellezza (2013)" "绝美之城 La grande bellezza (2013)"
    rename_movie "Lawyer.Lawyer.1997.720p.HDTV.x264-XXFANS (1997)" "算死草 Lawyer Lawyer (1997)"
    rename_movie "Leap Year 2010 (2010)" "闰年 Leap Year (2010)"
    rename_movie "Léon - The Professional - Extended Edition (1994)" "这个杀手不太冷：导演剪辑版 Léon The Professional Extended Edition (1994)"
    rename_movie "Like Stars on Earth (2007)" "地球上的星星 Like Stars on Earth (2007)"
    rename_movie "Look Out, Officer! (1990)" "师兄撞鬼 Look Out Officer (1990)"
    rename_movie "Love.is.Love.1990.Blu-ray.720p.x264.DTS.DD51.DualAudio.MySilu (1990)" "阿飞正传 Love is Love (1990)"
    rename_movie "M (1931)" "M就是凶手 M (1931)"
    rename_movie "MADE IN HONG KONG (1997)" "香港制造 Made in Hong Kong (1997)"
    rename_movie "Merry Christmas Mr. Lawrence (1983)" "圣诞快乐劳伦斯先生 Merry Christmas Mr. Lawrence (1983)"
    rename_movie "Monty Python and the Holy Grail (1975)" "巨蟒与圣杯 Monty Python and the Holy Grail (1975)"
    rename_movie "My People, My Country (2019)" "我和我的祖国 My People My Country (2019)"
    rename_movie "Netemo sametemo 2018 (2018)" "昼颜 Netemo sametemo (2018)"
    rename_movie "News of the World 2020 (2020)" "世界新闻 News of the World (2020)"
    rename_movie "Nightmare Alley (2021) 1080p HDR Encode (2021)" "玉面情魔 Nightmare Alley (2021)"
    rename_movie "Oldboy.2003.1080p.TWN.Blu-ray.AVC.DTS-HD.MA.5.1-hc@PTHome (2003)" "老男孩 Oldboy (2003)"
    rename_movie "Once Upon a Time in America (1984)" "美国往事 Once Upon a Time in America (1984)"
    rename_movie "Once Upon a Time in the West (1968)" "西部往事 Once Upon a Time in the West (1968)"
    rename_movie "Osaka.Loan.Shark (2021)" "大阪放贷人 Osaka Loan Shark (2021)"
    rename_movie "Paths of Glory (1957)" "光荣之路 Paths of Glory (1957)"
    rename_movie "Perfume - The Story of a Murderer (2006)" "香水：一个杀手的故事 Perfume The Story of a Murderer (2006)"
    rename_movie "Police Story - Lockdown (2013)" "警察故事2013 Police Story Lockdown (2013)"
    rename_movie "Police.Story.I (1985)" "警察故事 Police Story I (1985)"
    rename_movie "Police.Story.II (1988)" "警察故事续集 Police Story II (1988)"
    rename_movie "Police.Story.III.Super.Cop (1992)" "警察故事3：超级警察 Police Story III Super Cop (1992)"
    rename_movie "Police.Story.IV.First.Strike (1996)" "警察故事4：简单任务 Police Story IV First Strike (1996)"
    rename_movie "Raiders of the Lost Ark (1981)" "夺宝奇兵 Raiders of the Lost Ark (1981)"
    rename_movie "Raiders of the Lost Ark 1981 (1981)" "夺宝奇兵 Raiders of the Lost Ark (1981)"
    rename_movie "Redeeming Love (2022)" "救赎之爱 Redeeming Love (2022)"
    rename_movie "Royal.Tramp.1992.BluRay.720p.AC3.2Audio.x264-CHD (1992)" "鹿鼎记 Royal Tramp (1992)"
    rename_movie "Royal.Tramp.2.1992.BluRay.720p.AC3.2Audio.x264-CHD (1992)" "鹿鼎记2：神龙教 Royal Tramp 2 (1992)"
    rename_movie "Running.on.Empty (1988)" "不归路 Running on Empty (1988)"
    rename_movie "Salyut-7 (2017)" "礼炮7号 Salyut-7 (2017)"
    rename_movie "Scary Movie (2000)" "惊声尖笑 Scary Movie (2000)"
    rename_movie "Scary Movie 2 (2001)" "惊声尖笑2 Scary Movie 2 (2001)"
    rename_movie "Scary Movie 3 (2003)" "惊声尖笑3 Scary Movie 3 (2003)"
    rename_movie "Scent.of.a.Woman.1992.1080p.BluRay.x264.DTS-FiDELiO (1992)" "闻香识女人 Scent of a Woman (1992)"
    rename_movie "Shattered.2021 (2022)" "破碎 Shattered (2022)"
    rename_movie "Sicario - Blu-ray (2015)" "边境杀手 Sicario (2015)"
    rename_movie "Sixty.Million.Dollar.Man.1995.720p.BluRay.x264-WiKi (1995)" "百变星君 Sixty Million Dollar Man (1995)"
    rename_movie "Song of the Sea (2014)" "海洋之歌 Song of the Sea (2014)"
    rename_movie "SoulMate 2016 (2016)" "七月与安生 SoulMate (2016)"
    rename_movie "Spider-Man - Across The Spider-Verse (2023)" "蜘蛛侠：纵横宇宙 Spider-Man Across The Spider-Verse (2023)"
    rename_movie "Spider-Man - Into the Spider-Verse (2018)" "蜘蛛侠：平行宇宙 Spider-Man Into the Spider-Verse (2018)"
    rename_movie "Spider-Man.3 (2007)" "蜘蛛侠3 Spider-Man 3 (2007)"
    rename_movie "Star Trek (2009)" "星际迷航 Star Trek (2009)"
    rename_movie "Star Trek Beyond (2016)" "星际迷航3：超越星辰 Star Trek Beyond (2016)"
    rename_movie "Star Trek II - The Wrath of Khan (1982)" "星际迷航2：可汗怒吼 Star Trek II The Wrath of Khan (1982)"
    rename_movie "Star Trek III - The Search for Spock (1984)" "星际迷航3：石破天惊 Star Trek III The Search for Spock (1984)"
    rename_movie "Star Trek Into Darkness (2013)" "星际迷航：暗黑无界 Star Trek Into Darkness (2013)"
    rename_movie "Star Trek IV - The Voyage Home (1986)" "星际迷航4：抢救未来 Star Trek IV The Voyage Home (1986)"
    rename_movie "Star Trek VI - The Undiscovered Country (1991)" "星际迷航6：未来之城 Star Trek VI The Undiscovered Country (1991)"
    rename_movie "Star.Trek.I.The.Motion.Picture (1979)" "星际迷航1：无限太空 Star Trek I The Motion Picture (1979)"
    rename_movie "Star.Trek.IX.Insurrection (1998)" "星际迷航9：起义 Star Trek IX Insurrection (1998)"
    rename_movie "Star.Trek.VII.Generations (1994)" "星际迷航7：日换星移 Star Trek VII Generations (1994)"
    rename_movie "Star.Trek.VIII.First.Contact (1996)" "星际迷航8：第一类接触 Star Trek VIII First Contact (1996)"
    rename_movie "Star.Trek.X.Nemesis (2002)" "星际迷航10：复仇女神 Star Trek X Nemesis (2002)"
    rename_movie "Suk.Suk (2020)" "叔·叔 Suk Suk (2020)"
    rename_movie "Summer Detective 2019 (2019)" "夏日侦探 Summer Detective (2019)"
    rename_movie "Sunset Blvd. (1950)" "日落大道 Sunset Blvd (1950)"
    rename_movie "Systemsprenger 2019 (2019)" "系统破坏者 Systemsprenger (2019)"
    rename_movie "Talvisota elokuvan kuvaukset Keuruulla (1989)" "塔尔维索塔电影拍摄 Talvisota elokuvan kuvaukset Keuruulla (1989)"
    rename_movie "THE LUNCHBOX (2013)" "午餐盒 The Lunchbox (2013)"
    rename_movie "The Tourist (2010)" "游客 The Tourist (2010)"
    rename_movie "The Yellow Sea 2010 (2010)" "黄海 The Yellow Sea (2010)"
    rename_movie "The.Beach.2000.Open.Matte.1080p.WEB-DL.DD5.1.H.264-spartanec163 (2000)" "海滩 The Beach (2000)"
    rename_movie "The.God.of.Cookery.1996.720p.HDTV.x264.2Audio-HDCTV (1996)" "食神 The God of Cookery (1996)"
    rename_movie "The.Human.Centipede.2009.BluRay.1080p.DTS.x264-CHD (2009)" "人体蜈蚣 The Human Centipede (2009)"
    rename_movie "The.Kings.Man (2021)" "王牌特工：源起 The Kings Man (2021)"
    rename_movie "The.Swordsman In Double Flag Town - Blu-ray™ (1991)" "双旗镇刀客 The Swordsman In Double Flag Town (1991)"
    rename_movie "Time of the Gypsies (1988)" "流浪者之歌 Time of the Gypsies (1988)"
    rename_movie "Tropic.Thunder.Directors.Cut (2008)" "热带惊雷：导演剪辑版 Tropic Thunder Directors Cut (2008)"
    rename_movie "Umibe.no.Etranger (2020)" "海边的异邦人 Umibe no Etranger (2020)"
    rename_movie "Un.sac.de.billes (2017)" "一袋弹珠 Un sac de billes (2017)"
    rename_movie "Under the Open Sky (2021)" "在蓝天下 Under the Open Sky (2021)"
    rename_movie "Vettai (2012)" "猎人 Vettai (2012)"
    rename_movie "Vive L'Amour (1995)" "爱情万岁 Vive L'Amour (1995)"
    rename_movie "Vychislitel AKA The Calculator [2014] 1080p BluRay - HJ (2014)" "计算器 Vychislitel AKA The Calculator (2014)"
    rename_movie "WALL·E (2008)" "机器人总动员 WALL·E (2008)"
    rename_movie "Western Stars (2019)" "西部明星 Western Stars (2019)"
    rename_movie "What a Wonderful Family 2 2017 1080p BluRay DD5.1 x265-10bit-HDS (2017)" "家族之苦2 What a Wonderful Family 2 (2017)"
    rename_movie "What a Wonderful Family 3 My Wife My Life 2018 1080p BluRay DTS x264-HDS (2018)" "家族之苦3 What a Wonderful Family 3 (2018)"
    rename_movie "When.Fortune.Smiles.1990.BluRay.720p.DTS x264-CHD (1990)" "笑傲江湖 When Fortune Smiles (1990)"
    rename_movie "Witness for the Prosecution (1957)" "控方证人 Witness for the Prosecution (1957)"
    rename_movie "Yi Yi (2000) (2000)" "一一 Yi Yi (2000)"
    rename_movie "Your Place or Mine (1998)" "你的地方还是我的地方 Your Place or Mine (1998)"
    rename_movie "Zack.Snyders.Justice.League.2021.4K.UHD.BluRay.ATMOS.HDR.x265-W4NK3R (2021)" "扎克·施奈德版正义联盟 Zack Snyders Justice League (2021)"
    
    # 处理一些特殊格式的目录
    rename_movie "Incendies (2010)" "烈火焚身 Incendies (2010)"
    rename_movie "Indiana Jones and the Last Crusade (1989)" "夺宝奇兵3：圣战奇兵 Indiana Jones and the Last Crusade (1989)"
    rename_movie "It's a Wonderful Life (1946)" "生活多美好 It's a Wonderful Life (1946)"
}

# 执行重命名
process_renames

echo
echo "="*50
echo "批量重命名完成统计:"
echo "✅ 成功重命名: $SUCCESS_COUNT 个"
echo "⏭️  跳过处理: $SKIP_COUNT 个"
echo "❌ 处理失败: $FAIL_COUNT 个"
echo "总计处理: $((SUCCESS_COUNT + SKIP_COUNT + FAIL_COUNT)) 个"
echo "完成时间: $(date)"
echo "="*50

# 显示剩余英文目录
echo
echo "检查剩余英文目录..."
REMAINING=$(ls | grep -E "^[A-Z]" | grep -v "HEVC编码\|CMCT\|RARBG" | wc -l)
echo "剩余英文目录数量: $REMAINING"

if [ $REMAINING -gt 0 ]; then
    echo "剩余英文目录列表:"
    ls | grep -E "^[A-Z]" | grep -v "HEVC编码\|CMCT\|RARBG" | head -20
    if [ $REMAINING -gt 20 ]; then
        echo "... 还有 $((REMAINING - 20)) 个目录"
    fi
fi

echo
echo "脚本执行完成！"