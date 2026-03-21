#!/usr/bin/env python3
"""
分析 DeepSeek 对话的兴趣分布
- 从内容中提取日期线索
- 按季度分析热门话题
- 生成报告
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

EXPORTS_DIR = Path(__file__).parent.parent / "exports"
OUTPUT_DIR = Path(__file__).parent.parent / "My Deepseek"

# 话题关键词映射
TOPIC_KEYWORDS = {
    "AI与技术": ["AI", "人工智能", "GPT", "Claude", "DeepSeek", "ChatGPT", "机器学习", "编程", "代码", "Python", "开发"],
    "健康医疗": ["健康", "医疗", "病症", "药物", "治疗", "医院", "症状", "医生", "疫苗", "体检"],
    "商业创业": ["创业", "公司", "企业", "运营", "营销", "品牌", "战略", "投资", "融资", "OGSM"],
    "学习教育": ["学习", "教育", "课程", "知识", "阅读", "书", "培训", "考试", "写作"],
    "生活日常": ["美食", "旅游", "购物", "交通", "餐厅", "酒店", "生活", "日常"],
    "亲子家庭": ["孩子", "儿子", "女儿", "父母", "家庭", "亲子", "教育", "学校"],
    "数码设备": ["手机", "电脑", "Mac", "iPhone", "iPad", "华为", "小米", "苹果", "耳机"],
    "金融理财": ["股票", "基金", "理财", "投资", "银行", "财务", "保险"],
    "运动健身": ["健身", "运动", "跑步", "游泳", "滑雪", "锻炼", "减肥"],
}


def extract_date_from_content(content: str) -> str:
    """从内容中提取日期线索"""
    # 常见日期模式
    patterns = [
        r'(\d{4})年(\d{1,2})月(\d{1,2})日?',  # 2025年1月15日
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # 2025-01-15 或 2025/01/15
        r'(\d{1,2})月(\d{1,2})日',  # 1月15日
        r'(今天|昨天|前天|上周|下周|上个月|下个月)',
        r'(春节|元旦|五一|十一|中秋|端午)',
        r'(\d{4})年(\d{1,2})月',  # 2025年1月
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(0)

    return None


def guess_quarter_from_content(content: str) -> str:
    """根据内容猜测季度"""
    content_lower = content.lower()

    # 季度特征词
    q1_words = ["春节", "过年", "元旦", "一月", "二月", "三月", "1月", "2月", "3月", "寒假"]
    q2_words = ["五一", "劳动节", "四月", "五月", "六月", "4月", "5月", "6月", "暑假前"]
    q3_words = ["暑假", "中秋", "七月", "八月", "九月", "7月", "8月", "9月", "开学"]
    q4_words = ["十一", "国庆", "双十一", "双11", "十月", "十一月", "十二月", "10月", "11月", "12月"]

    for word in q1_words:
        if word in content:
            return "Q1"
    for word in q2_words:
        if word in content:
            return "Q2"
    for word in q3_words:
        if word in content:
            return "Q3"
    for word in q4_words:
        if word in content:
            return "Q4"

    return "未知"


def classify_topic(title: str, content: str) -> str:
    """分类话题"""
    text = (title + " " + content[:500]).lower()

    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        scores[topic] = score

    max_score = max(scores.values()) if scores else 0
    if max_score > 0:
        return max(scores, key=scores.get)
    return "其他"


def analyze_all_files():
    """分析所有文件"""
    results = {
        "total": 0,
        "by_quarter": defaultdict(lambda: {"count": 0, "topics": Counter(), "titles": []}),
        "by_topic": Counter(),
        "by_quarter_topic": defaultdict(lambda: Counter()),
        "date_hints": [],
    }

    md_files = list(EXPORTS_DIR.glob("*.md"))

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 获取标题
            title = ""
            for line in content.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            # 提取日期线索
            date_hint = extract_date_from_content(content)

            # 猜测季度
            quarter = guess_quarter_from_content(content)

            # 分类话题
            topic = classify_topic(title, content)

            # 统计
            results["total"] += 1
            results["by_topic"][topic] += 1
            results["by_quarter"][quarter]["count"] += 1
            results["by_quarter"][quarter]["topics"][topic] += 1
            if len(results["by_quarter"][quarter]["titles"]) < 10:
                results["by_quarter"][quarter]["titles"].append(title)
            results["by_quarter_topic"][quarter][topic] += 1

            if date_hint:
                results["date_hints"].append({
                    "title": title[:30],
                    "date": date_hint,
                    "quarter": quarter
                })

        except Exception as e:
            pass

    return results


def generate_report(results: dict) -> str:
    """生成分析报告"""
    lines = []
    lines.append("# DeepSeek 对话兴趣分析报告")
    lines.append(f"\n> 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 总对话数: {results['total']}")

    # 话题分布
    lines.append("\n## 📊 话题分布\n")
    lines.append("| 话题 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    for topic, count in results["by_topic"].most_common():
        pct = count / results["total"] * 100
        bar = "█" * int(pct / 5)
        lines.append(f"| {topic} | {count} | {pct:.1f}% {bar} |")

    # 季度分析
    lines.append("\n## 📅 季度兴趣分析\n")
    lines.append("*（根据对话内容中的日期线索推测）*\n")

    for quarter in ["Q1", "Q2", "Q3", "Q4", "未知"]:
        if quarter not in results["by_quarter"]:
            continue
        q_data = results["by_quarter"][quarter]
        lines.append(f"### {quarter} ({q_data['count']} 条)\n")

        if q_data["topics"]:
            lines.append("**热门话题:**\n")
            for topic, count in q_data["topics"].most_common(5):
                lines.append(f"- {topic}: {count} 条")

        if q_data["titles"]:
            lines.append(f"\n**示例对话:**\n")
            for title in q_data["titles"][:5]:
                lines.append(f"- {title[:40]}...")
        lines.append("")

    # 日期线索
    if results["date_hints"]:
        lines.append("\n## 🗓️ 日期线索示例\n")
        lines.append("```")
        for hint in results["date_hints"][:20]:
            lines.append(f"[{hint['quarter']}] {hint['date'][:15]:15} | {hint['title'][:25]}")
        lines.append("```")

    # 兴趣画像
    lines.append("\n## 🎯 兴趣画像总结\n")

    top_topics = results["by_topic"].most_common(3)
    if top_topics:
        lines.append(f"**你最关注的话题:** {', '.join([t[0] for t in top_topics])}")

    # 找出各季度最热话题
    lines.append("\n**各季度关注重点:**")
    for quarter in ["Q1", "Q2", "Q3", "Q4"]:
        if quarter in results["by_quarter"] and results["by_quarter"][quarter]["topics"]:
            top = results["by_quarter"][quarter]["topics"].most_common(1)[0]
            lines.append(f"- {quarter}: {top[0]} ({top[1]}条)")

    return "\n".join(lines)


def main():
    print("分析 DeepSeek 对话...")

    results = analyze_all_files()

    # 生成报告
    report = generate_report(results)

    # 保存报告
    report_path = OUTPUT_DIR / "兴趣分析报告.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n报告已保存: {report_path}")

    # 也保存 JSON 数据
    json_path = OUTPUT_DIR / "兴趣分析数据.json"

    # 转换 defaultdict 为普通 dict
    serializable_results = {
        "total": results["total"],
        "by_topic": dict(results["by_topic"]),
        "by_quarter": {k: {
            "count": v["count"],
            "topics": dict(v["topics"]),
            "titles": v["titles"]
        } for k, v in results["by_quarter"].items()},
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)

    print(f"数据已保存: {json_path}")

    # 打印报告
    print("\n" + "=" * 60)
    print(report)


if __name__ == "__main__":
    main()
