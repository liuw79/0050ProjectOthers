#!/bin/bash

# 批量电影中文化重命名脚本
# 格式：中文名 英文名 (年份)

cd "/Volumes/video/电影/"

echo "开始批量重命名电影..."

# 定义重命名映射
declare -A movie_map=(
    ["A Scene at the Sea (1991)"]="那年夏天宁静的海 A Scene at the Sea (1991)"
    ["All for the Winner (1990)"]="赌圣 All for the Winner (1990)"
    ["American Made (2017)"]="美国制造 American Made (2017)"
    ["American Woman (2018)"]="美国女人 American Woman (2018)"
    ["Angels & Demons (2009)"]="天使与魔鬼 Angels & Demons (2009)"
    ["Ao.Der.letzte.Neandertaler (2010)"]="最后的尼安德特人 Ao.Der.letzte.Neandertaler (2010)"
    ["ARABIAN NIGHTS (1974)"]="天方夜谭 ARABIAN NIGHTS (1974)"
    ["Babyteeth (2020)"]="小牙齿 Babyteeth (2020)"
    ["Blade Runner (1982)"]="银翼杀手 Blade Runner (1982)"
    ["Blade Runner 2049 (2017)"]="银翼杀手2049 Blade Runner 2049 (2017)"
    ["Casablanca (1942)"]="卡萨布兰卡 Casablanca (1942)"
    ["Casino (1995)"]="赌场风云 Casino (1995)"
    ["Chicago (2002)"]="芝加哥 Chicago (2002)"
    ["Citizen Kane (1941)"]="公民凯恩 Citizen Kane (1941)"
    ["Crash (2004)"]="撞车 Crash (2004)"
    ["Django Unchained (2012)"]="被解救的姜戈 Django Unchained (2012)"
    ["Forrest Gump (1994)"]="阿甘正传 Forrest Gump (1994)"
    ["Green Book (2018)"]="绿皮书 Green Book (2018)"
    ["Hunter Killer (2018)"]="猎杀潜航 Hunter Killer (2018)"
    ["Jaws (1975)"]="大白鲨 Jaws (1975)"
    ["Kill Bill: Vol. 1 (2003)"]="杀死比尔 Kill Bill: Vol. 1 (2003)"
    ["Kill Bill: Vol. 2 (2004)"]="杀死比尔2 Kill Bill: Vol. 2 (2004)"
    ["Leon: The Professional (1994)"]="这个杀手不太冷 Leon: The Professional (1994)"
    ["Matrix (1999)"]="黑客帝国 Matrix (1999)"
    ["Matrix Reloaded (2003)"]="黑客帝国2重装上阵 Matrix Reloaded (2003)"
    ["Matrix Revolutions (2003)"]="黑客帝国3矩阵革命 Matrix Revolutions (2003)"
    ["Pulp Fiction (1994)"]="低俗小说 Pulp Fiction (1994)"
    ["Silence of the Lambs (1991)"]="沉默的羔羊 Silence of the Lambs (1991)"
    ["Taxi Driver (1976)"]="出租车司机 Taxi Driver (1976)"
    ["Terminator (1984)"]="终结者 Terminator (1984)"
    ["Terminator 2: Judgment Day (1991)"]="终结者2审判日 Terminator 2: Judgment Day (1991)"
    ["Titanic (1997)"]="泰坦尼克号 Titanic (1997)"
    ["To Kill a Mockingbird (1962)"]="杀死一只知更鸟 To Kill a Mockingbird (1962)"
    ["Too Cool to Kill (2022)"]="这个杀手不太冷静 Too Cool to Kill (2022)"
    ["Vertigo (1958)"]="迷魂记 Vertigo (1958)"
    ["Avatar (2009)"]="阿凡达 Avatar (2009)"
    ["Batman Begins (2005)"]="蝙蝠侠侠影之谜 Batman Begins (2005)"
    ["The Dark Knight (2008)"]="蝙蝠侠黑暗骑士 The Dark Knight (2008)"
    ["The Dark Knight Rises (2012)"]="蝙蝠侠黑暗骑士崛起 The Dark Knight Rises (2012)"
    ["100 YEN LOVE (2014)"]="百元之恋 100 YEN LOVE (2014)"
    ["22 Bullets 2010 (2010)"]="22颗子弹 22 Bullets 2010 (2010)"
)

# 执行重命名
count=0
for old_name in "${!movie_map[@]}"; do
    new_name="${movie_map[$old_name]}"
    if [ -d "$old_name" ]; then
        echo "重命名: $old_name -> $new_name"
        mv "$old_name" "$new_name"
        ((count++))
    else
        echo "跳过（不存在）: $old_name"
    fi
done

echo "批量重命名完成，共处理 $count 部电影"
echo "正在统计当前目录状态..."
echo "总目录数: $(find . -maxdepth 1 -type d | wc -l)"
echo "中文名目录数: $(find . -maxdepth 1 -type d -name '*[\u4e00-\u9fff]*' | wc -l)"