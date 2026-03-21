#!/usr/bin/env python3
"""
DeepSeek问答数据深度分析脚本
分析维度：时间线、问题类型、知识主题、金句、决策模式、重复主题
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# 配置
BASE_DIR = Path("/Users/comdir/SynologyDrive/0050Project/Tool.DeepSeek/My Deepseek")
OUTPUT_DIR = BASE_DIR / "analysis_output"

# 问题类型分类关键词
QUESTION_TYPES = {
    "决策咨询": ["应该", "选择", "哪个", "还是", "建议", "决策", "怎么办", "如何选", "怎么选", "比较好", "值得"],
    "知识学习": ["是什么", "什么是", "为什么", "原理", "概念", "意思", "区别", "如何理解", "介绍"],
    "执行指导": ["怎么", "如何做", "步骤", "方法", "教程", "操作", "实现", "设置", "配置"],
    "创意生成": ["帮我写", "生成", "创作", "设计", "构思", "润色", "优化", "改写", "排版"],
    "问题诊断": ["问题", "错误", "报错", "原因", "为什么不行", "故障", "异常", "分析"],
    "数据分析": ["数据", "分析", "统计", "计算", "对比", "表格", "图表", "指标"],
    "信息查询": ["有没有", "哪里", "什么时候", "谁", "多少", "哪里可以", "推荐"],
}

# 决策相关关键词
DECISION_KEYWORDS = [
    "方案", "选择", "对比", "利弊", "优劣势", "建议", "决策", "确定",
    "A还是B", "两个", "哪个好", "值得买", "应该选", "怎么选"
]

# 金句特征（简洁有力、有洞察）
def is_golden_quote(text):
    """判断是否可能是金句"""
    if not text or len(text) < 10 or len(text) > 150:
        return False
    # 包含关键结构
    patterns = [
        r"^\d+\.",  # 数字开头
        r"[：:]\s*[^。]+$",  # 冒号后的短句
        r"。[^。]{5,30}$",  # 最后一句总结
        r"(核?心|关键|本质|底?层逻辑|原则|法则|定律)",
        r"(重要|必须|一定|永远|从来|真正)",
        r"(不是.*而是|与其.*不如|没有.*只有)",
    ]
    for p in patterns:
        if re.search(p, text):
            return True
    return False

def extract_frontmatter(content):
    """提取YAML前置信息"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        data = {}
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        return data
    return {}

def extract_user_questions(content):
    """提取用户问题"""
    questions = []
    # 移除frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # 提取User部分
    user_sections = re.findall(r'## User\s*\n(.*?)(?=## Assistant|\Z)', content, re.DOTALL)
    for section in user_sections:
        text = section.strip()
        if text:
            # 取第一句或前100字符
            first_line = text.split('\n')[0][:100]
            questions.append(first_line)
    return questions

def extract_assistant_content(content):
    """提取助手回复内容"""
    # 移除frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # 提取Assistant部分
    assistant_sections = re.findall(r'## Assistant\s*\n(.*?)(?=## User|\Z)', content, re.DOTALL)
    return '\n'.join(assistant_sections)

def classify_question_type(question):
    """分类问题类型"""
    scores = {}
    for qtype, keywords in QUESTION_TYPES.items():
        score = sum(1 for kw in keywords if kw in question)
        if score > 0:
            scores[qtype] = score
    if scores:
        return max(scores, key=scores.get)
    return "其他"

def extract_dates(text):
    """从文本中提取日期信息"""
    dates = []
    patterns = [
        r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
        r'(\d{4}[-/年]\d{1,2}[月]?)',
        r'(\d{1,2}月\d{1,2}[日]?)',
        r'(今天|昨天|前天|上周|本月|去年|今年)',
    ]
    for p in patterns:
        matches = re.findall(p, text)
        dates.extend(matches)
    return dates

def extract_golden_quotes(content):
    """提取金句"""
    quotes = []
    # 按句子分割
    sentences = re.split(r'[。\n]', content)
    for s in sentences:
        s = s.strip()
        if is_golden_quote(s):
            quotes.append(s)
    return quotes[:5]  # 每个文件最多5条

def analyze_file(filepath):
    """分析单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    result = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'category': filepath.parent.name,
    }

    # 提取frontmatter
    fm = extract_frontmatter(content)
    result['title'] = fm.get('title', filepath.stem)
    result['messages'] = int(fm.get('messages', 0)) if fm.get('messages', '').isdigit() else 0
    result['processed_date'] = fm.get('processed', '')

    # 提取用户问题
    questions = extract_user_questions(content)
    result['questions'] = questions
    result['question_preview'] = questions[0] if questions else result['title']

    # 问题类型分类
    if questions:
        result['question_type'] = classify_question_type(questions[0])
    else:
        result['question_type'] = '其他'

    # 提取助手内容
    assistant_content = extract_assistant_content(content)
    result['content_length'] = len(assistant_content)

    # 提取日期线索
    dates = extract_dates(content)
    result['date_hints'] = dates

    # 提取金句
    quotes = extract_golden_quotes(assistant_content)
    result['golden_quotes'] = quotes

    # 决策相关度
    decision_score = sum(1 for kw in DECISION_KEYWORDS if kw in content)
    result['decision_relevance'] = decision_score

    return result

def main():
    print("开始分析DeepSeek问答数据...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 收集所有md文件
    all_files = []
    for category_dir in BASE_DIR.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith('.'):
            for f in category_dir.glob("*.md"):
                if "兴趣分析" not in f.name and "精选有价值" not in f.name and "process_log" not in f.name:
                    all_files.append(f)

    print(f"找到 {len(all_files)} 个对话文件")

    # 分析所有文件
    results = []
    for i, f in enumerate(all_files):
        if (i + 1) % 100 == 0:
            print(f"处理进度: {i+1}/{len(all_files)}")
        result = analyze_file(f)
        if result:
            results.append(result)

    print(f"成功分析 {len(results)} 个文件")

    # 统计分析
    analysis = {
        'total_count': len(results),
        'categories': Counter(r['category'] for r in results),
        'question_types': Counter(r['question_type'] for r in results),
        'avg_messages': sum(r['messages'] for r in results) / len(results) if results else 0,
        'avg_content_length': sum(r['content_length'] for r in results) / len(results) if results else 0,
    }

    # 按分类统计问题类型
    category_question_types = defaultdict(Counter)
    for r in results:
        category_question_types[r['category']][r['question_type']] += 1
    analysis['category_question_types'] = {k: dict(v) for k, v in category_question_types.items()}

    # 收集所有金句
    all_quotes = []
    for r in results:
        for q in r['golden_quotes']:
            all_quotes.append({
                'quote': q,
                'category': r['category'],
                'source': r['title']
            })
    analysis['golden_quotes'] = all_quotes[:100]  # 取前100条

    # 决策相关对话
    decision_related = sorted(
        [r for r in results if r['decision_relevance'] > 0],
        key=lambda x: x['decision_relevance'],
        reverse=True
    )[:50]
    analysis['decision_related'] = decision_related

    # 按分类整理
    by_category = defaultdict(list)
    for r in results:
        by_category[r['category']].append(r)
    analysis['by_category'] = {k: len(v) for k, v in by_category.items()}

    # 问题类型详情
    question_type_details = defaultdict(list)
    for r in results:
        question_type_details[r['question_type']].append({
            'title': r['title'],
            'category': r['category'],
            'question': r['question_preview']
        })
    analysis['question_type_details'] = {k: v[:10] for k, v in question_type_details.items()}

    # 保存完整结果
    with open(OUTPUT_DIR / 'full_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"分析完成，结果保存到 {OUTPUT_DIR}")

    return analysis

if __name__ == "__main__":
    main()
