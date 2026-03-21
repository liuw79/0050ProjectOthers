#!/bin/bash

# 清理重复的英文电影目录脚本
# 删除已经重命名为中文的英文目录
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

echo "开始清理重复的英文电影目录"
echo "目标目录: $TARGET_DIR"
echo "时间: $(date)"
echo "="*50

# 计数器
DELETED_COUNT=0
SKIP_COUNT=0
ERROR_COUNT=0

# 清理函数
cleanup_duplicate() {
    local english_dir="$1"
    local chinese_dir="$2"
    
    # 检查英文目录是否存在
    if [ ! -d "$english_dir" ]; then
        echo "⚠️  英文目录不存在: $english_dir"
        ((SKIP_COUNT++))
        return
    fi
    
    # 检查中文目录是否存在
    if [ ! -d "$chinese_dir" ]; then
        echo "⚠️  中文目录不存在，保留英文目录: $english_dir"
        ((SKIP_COUNT++))
        return
    fi
    
    # 检查英文目录是否为空或只有少量文件
    local english_files=$(find "$english_dir" -type f | wc -l)
    local chinese_files=$(find "$chinese_dir" -type f | wc -l)
    
    echo "📊 $english_dir: $english_files 个文件"
    echo "📊 $chinese_dir: $chinese_files 个文件"
    
    # 如果中文目录文件更多，删除英文目录
    if [ $chinese_files -gt $english_files ]; then
        echo "🗑️  删除英文目录: $english_dir (文件较少)"
        if rm -rf "$english_dir" 2>/dev/null; then
            ((DELETED_COUNT++))
            echo "✅ 删除成功"
        else
            echo "❌ 删除失败"
            ((ERROR_COUNT++))
        fi
    else
        echo "⚠️  保留英文目录: $english_dir (文件数量相同或更多)"
        ((SKIP_COUNT++))
    fi
    
    echo "---"
}

# 执行清理操作
process_cleanup() {
    # 处理每个重复的电影目录
    cleanup_duplicate "Extended Collector's Edition Disc 1 (2009)" "指环王扩展收藏版光盘1 Extended Collector's Edition Disc 1 (2009)"
    cleanup_duplicate "Ikiru (1952)" "生之欲 Ikiru (1952)"
    cleanup_duplicate "In the Mood for Love (2000)" "花样年华 In the Mood for Love (2000)"
    cleanup_duplicate "Inception (2010)" "盗梦空间 Inception (2010)"
    cleanup_duplicate "Inglourious Basterds (2009)" "无耻混蛋 Inglourious Basterds (2009)"
    cleanup_duplicate "Interstellar (2014)" "星际穿越 Interstellar (2014)"
    cleanup_duplicate "It's a Wonderful Life (1946)" "生活多美好 It's a Wonderful Life (1946)"
    cleanup_duplicate "Joker (2019)" "小丑 Joker (2019)"
    cleanup_duplicate "Just Heroes (1989)" "义胆群英 Just Heroes (1989)"
    cleanup_duplicate "King of Comedy (1999)" "喜剧之王 King of Comedy (1999)"
    cleanup_duplicate "Klaus (2019)" "克劳斯：圣诞节的秘密 Klaus (2019)"
    cleanup_duplicate "Ladies Market (2021)" "女人街 Ladies Market (2021)"
    cleanup_duplicate "Leap (2020)" "飞奔去月球 Leap (2020)"
    cleanup_duplicate "Life of Pi (2012)" "少年派的奇幻漂流 Life of Pi (2012)"
    cleanup_duplicate "Love on Delivery (1994)" "破坏之王 Love on Delivery (1994)"
    cleanup_duplicate "Love Will Tear Us Apart (2021)" "爱情神话 Love Will Tear Us Apart (2021)"
    cleanup_duplicate "Love, Rosie (2014)" "爱你，罗茜 Love Rosie (2014)"
    cleanup_duplicate "Loving Vincent (2017)" "至爱梵高·星空之谜 Loving Vincent (2017)"
    cleanup_duplicate "Luca (2021)" "夏日友晴天 Luca (2021)"
    cleanup_duplicate "Made in Italy (2020)" "意大利制造 Made in Italy (2020)"
    cleanup_duplicate "Man in Love (2021)" "恋爱中的男人 Man in Love (2021)"
    cleanup_duplicate "Memento (2000)" "记忆碎片 Memento (2000)"
    cleanup_duplicate "Metropolis (1927)" "大都会 Metropolis (1927)"
    cleanup_duplicate "Moana (2016)" "海洋奇缘 Moana (2016)"
    cleanup_duplicate "Modern Times (1936)" "摩登时代 Modern Times (1936)"
    cleanup_duplicate "Moon Man (2022)" "独行月球 Moon Man (2022)"
    cleanup_duplicate "Mulan (2020)" "花木兰 Mulan (2020)"
    cleanup_duplicate "New Police Story (2004)" "新警察故事 New Police Story (2004)"
    cleanup_duplicate "Nice View (2022)" "奇迹·笨小孩 Nice View (2022)"
    cleanup_duplicate "No Man's Land (2013)" "无人区 No Man's Land (2013)"
    cleanup_duplicate "North by Northwest (1959)" "西北偏北 North by Northwest (1959)"
    cleanup_duplicate "Oldboy (2003)" "老男孩 Oldboy (2003)"
    cleanup_duplicate "Operation Red Sea (2018)" "红海行动 Operation Red Sea (2018)"
    cleanup_duplicate "Oppenheimer (2023)" "奥本海默 Oppenheimer (2023)"
    cleanup_duplicate "Pegasus (2019)" "飞驰人生 Pegasus (2019)"
    cleanup_duplicate "Princess Mononoke (1997)" "幽灵公主 Princess Mononoke (1997)"
    cleanup_duplicate "Psycho (1960)" "惊魂记 Psycho (1960)"
    cleanup_duplicate "Railway Heroes (2021)" "铁道英雄 Railway Heroes (2021)"
    cleanup_duplicate "Rear Window (1954)" "后窗 Rear Window (1954)"
    cleanup_duplicate "Rush Hour (1998)" "尖峰时刻 Rush Hour (1998)"
    cleanup_duplicate "Scarface (1983)" "疤面煞星 Scarface (1983)"
    cleanup_duplicate "Se7en (1995)" "七宗罪 Se7en (1995)"
    cleanup_duplicate "Seven Samurai (1954)" "七武士 Seven Samurai (1954)"
    cleanup_duplicate "Shaolin Soccer (2001)" "少林足球 Shaolin Soccer (2001)"
    cleanup_duplicate "Snatch (2000)" "偷拐抢骗 Snatch (2000)"
    cleanup_duplicate "Soul (2020)" "心灵奇旅 Soul (2020)"
    cleanup_duplicate "Space Sweepers (2021)" "胜利号 Space Sweepers (2021)"
    cleanup_duplicate "Sully (2016)" "萨利机长 Sully (2016)"
    cleanup_duplicate "The Intouchables (2011)" "触不可及 The Intouchables (2011)"
    cleanup_duplicate "The Invisible Man (2020)" "隐形人 The Invisible Man (2020)"
    cleanup_duplicate "The Kid (1921)" "寻子遇仙记 The Kid (1921)"
    cleanup_duplicate "The Lives of Others (2006)" "窃听风暴 The Lives of Others (2006)"
    cleanup_duplicate "The Lucky Guy (1998)" "行运一条龙 The Lucky Guy (1998)"
    cleanup_duplicate "The Mermaid (2016)" "美人鱼 The Mermaid (2016)"
    cleanup_duplicate "The Old Guard (2020)" "永生守卫 The Old Guard (2020)"
    cleanup_duplicate "The Piano (1993)" "钢琴课 The Piano (1993)"
    cleanup_duplicate "The Piano Teacher (2001)" "钢琴教师 The Piano Teacher (2001)"
    cleanup_duplicate "The Sting (1973)" "骗中骗 The Sting (1973)"
    cleanup_duplicate "The Wandering Earth II (2023)" "流浪地球2 The Wandering Earth II (2023)"
    cleanup_duplicate "The Wolf of Wall Street (2013)" "华尔街之狼 The Wolf of Wall Street (2013)"
    cleanup_duplicate "Togo (2019)" "多哥 Togo (2019)"
    cleanup_duplicate "Tomorrowland (2015)" "明日世界 Tomorrowland (2015)"
    cleanup_duplicate "Up (2009)" "飞屋环游记 Up (2009)"
    cleanup_duplicate "Whiplash (2014)" "爆裂鼓手 Whiplash (2014)"
    cleanup_duplicate "Wild Bill (2011)" "狂野比尔 Wild Bill (2011)"
    cleanup_duplicate "Your Name. (2016)" "你的名字 Your Name (2016)"
}

# 执行清理
process_cleanup

echo
echo "="*50
echo "清理完成统计:"
echo "🗑️  删除目录: $DELETED_COUNT 个"
echo "⏭️  跳过处理: $SKIP_COUNT 个"
echo "❌ 处理错误: $ERROR_COUNT 个"
echo "总计处理: $((DELETED_COUNT + SKIP_COUNT + ERROR_COUNT)) 个"
echo "完成时间: $(date)"
echo "="*50

# 显示剩余英文目录
echo
echo "检查剩余英文目录..."
REMAINING=$(ls | grep -E "^[A-Z]" | grep -v "HEVC编码\|CMCT\|RARBG" | wc -l)
echo "剩余英文目录数量: $REMAINING"

if [ $REMAINING -gt 0 ]; then
    echo "剩余英文目录列表:"
    ls | grep -E "^[A-Z]" | grep -v "HEVC编码\|CMCT\|RARBG" | head -10
    if [ $REMAINING -gt 10 ]; then
        echo "... 还有 $((REMAINING - 10)) 个目录"
    fi
fi

echo
echo "脚本执行完成！"