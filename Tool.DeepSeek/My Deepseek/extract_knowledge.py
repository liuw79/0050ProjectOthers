#!/usr/bin/env python3
"""
深度知识提取脚本
从商业管理类对话中提取：方法论、框架、模型、洞察
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter

BASE_DIR = Path("/Users/comdir/SynologyDrive/0050Project/Tool.DeepSeek/My Deepseek")
OUTPUT_DIR = BASE_DIR / "analysis_output"

# 商业方法论关键词
METHODOLOGY_PATTERNS = {
    "分析框架": ["RFM", "SWOT", "PEST", "波特五力", "商业模式画布", "价值链", "平衡计分卡", "OGSM", "OKR", "KPI"],
    "管理模型": ["漏斗", "矩阵", "金字塔", "闭环", "飞轮", "双因素", "马斯洛", "PDCA", "SMART"],
    "商业概念": ["护城河", "壁垒", "差异化", "核心竞争力", "飞轮效应", "网络效应", "规模效应", "边际成本"],
    "决策工具": ["决策树", "概率", "期望值", "ROI", "盈亏平衡", "成本效益", "敏感性分析"],
}

# 高价值金句模式（更严格）
GOLDEN_PATTERNS = [
    r"(核?心|关键|本质|底?层逻辑|原则)是[：:]",  # 核心是...
    r"(不是|不要|千万别).{3,}(而是|要|应该)",  # 不是...而是...
    r"(与其|与其说).{3,}(不如|不如说)",  # 与其...不如...
    r"(最重要|最关键|最核心|最本质).{0,10}(是|在于)",  # 最重要的是...
    r"(永远|从来|总是|一定).{3,}(因为|由于|只有)",  # 因果关系
    r"(真正的|真正的成功|真正的领导|真正的管理)",  # 深度洞察
    r"(第一性|底层|本质|元认知)",  # 认知升级
    r"(只有|只要|除非|如果).{3,}(才|就|能|会)",  # 条件关系
]

def extract_methodology(content, title):
    """提取方法论和框架"""
    found = defaultdict(list)
    for category, patterns in METHODOLOGY_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in content.lower():
                # 提取包含该模式的句子
                sentences = re.split(r'[。\n]', content)
                for s in sentences:
                    if pattern.lower() in s.lower() and len(s) > 20:
                        found[category].append({
                            'pattern': pattern,
                            'sentence': s.strip()[:200],
                            'source': title
                        })
                        break  # 每个模式只取一个
    return dict(found)

def extract_golden_insights(content, title):
    """提取高质量金句"""
    insights = []
    sentences = re.split(r'[。\n]', content)

    for s in sentences:
        s = s.strip()
        if len(s) < 20 or len(s) > 150:
            continue

        # 检查是否匹配高价值模式
        for pattern in GOLDEN_PATTERNS:
            if re.search(pattern, s):
                insights.append({
                    'text': s,
                    'source': title,
                    'pattern': pattern
                })
                break

    return insights[:3]  # 每个文件最多3条

def analyze_category(category_name, category_dir):
    """分析一个分类目录"""
    results = {
        'methodologies': defaultdict(list),
        'insights': [],
        'topics': Counter(),
        'high_value_files': []
    }

    for f in category_dir.glob("*.md"):
        if "兴趣分析" in f.name or "精选有价值" in f.name or "process_log" in f.name:
            continue

        try:
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
        except:
            continue

        title = f.stem

        # 提取方法论
        methods = extract_methodology(content, title)
        for cat, items in methods.items():
            results['methodologies'][cat].extend(items)

        # 提取金句
        insights = extract_golden_insights(content, title)
        results['insights'].extend(insights)

        # 统计主题词
        # 从标题提取关键词
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', title)
        results['topics'].update(keywords)

    return results

def main():
    print("="*60)
    print("深度知识提取")
    print("="*60)

    all_results = {}
    all_insights = []
    all_methodologies = defaultdict(list)

    for category_dir in BASE_DIR.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        print(f"分析: {category_dir.name}")
        results = analyze_category(category_dir.name, category_dir)
        all_results[category_dir.name] = results
        all_insights.extend(results['insights'])

        for cat, items in results['methodologies'].items():
            all_methodologies[cat].extend(items)

    # 去重金句
    unique_insights = []
    seen = set()
    for insight in all_insights:
        if insight['text'] not in seen:
            seen.add(insight['text'])
            unique_insights.append(insight)

    print(f"\n提取结果:")
    print(f"  - 高质量金句: {len(unique_insights)}")
    print(f"  - 方法论框架: {sum(len(v) for v in all_methodologies.values())}")

    # 保存结果
    output = {
        'insights': sorted(unique_insights, key=lambda x: len(x['text']))[:100],
        'methodologies': {k: v[:20] for k, v in all_methodologies.items()},
        'by_category': {k: {
            'topics': dict(v['topics'].most_common(10)),
            'insight_count': len(v['insights'])
        } for k, v in all_results.items()}
    }

    with open(OUTPUT_DIR / 'knowledge_extraction.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 生成Markdown
    md = generate_knowledge_md(output)
    with open(OUTPUT_DIR / 'knowledge_extraction.md', 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"\n结果已保存到 {OUTPUT_DIR}")

def generate_knowledge_md(data):
    """生成知识提取Markdown"""
    md = """# 深度知识提取报告

> 从982条对话中提取的高价值内容

---

## 一、高质量金句精选

"""
    for i, insight in enumerate(data['insights'][:50], 1):
        md += f"### {i}. {insight['text']}\n"
        md += f"*来源: {insight['source']}*\n\n"

    md += """---

## 二、方法论与框架汇总

"""
    for category, items in data['methodologies'].items():
        if items:
            md += f"### {category}\n\n"
            for item in items[:10]:
                md += f"**{item['pattern']}** - {item['source']}\n"
                md += f"> {item['sentence'][:100]}...\n\n"

    md += """---

## 三、各分类主题分布

"""
    for cat, info in sorted(data['by_category'].items(), key=lambda x: -x[1]['insight_count']):
        if info['insight_count'] > 0:
            md += f"### {cat}\n"
            md += f"金句数: {info['insight_count']}\n"
            md += f"高频词: {', '.join([f'{k}({v})' for k,v in list(info['topics'].items())[:5]])}\n\n"

    return md

if __name__ == "__main__":
    main()
