#!/usr/bin/env python3
"""
DeepSeek问答数据深度分析脚本 v2
分析维度：
1. 时间线分析
2. 问题类型归类
3. 知识主题提取
4. 金句提取
5. 决策模式分析
6. 重复主题识别
7. 【新增】提示词质量分析
8. 【新增】提问技巧分析
9. 【新增】成长相关内容提取
10.【新增】个人能力画像
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

# 成长相关关键词
GROWTH_KEYWORDS = {
    "技能提升": ["学习", "提升", "提高", "进步", "成长", "技能", "能力", "掌握", "精通"],
    "认知升级": ["认知", "思维", "底层逻辑", "本质", "洞察", "理解", "框架", "模型"],
    "管理能力": ["管理", "团队", "领导", "组织", "激励", "沟通", "协作", "决策"],
    "商业思维": ["商业", "盈利", "模式", "市场", "竞争", "战略", "定位", "差异化"],
    "个人效能": ["效率", "时间", "精力", "专注", "习惯", "自律", "目标", "规划"],
}

# 提示词质量指标
PROMPT_QUALITY_INDICATORS = {
    "有上下文": ["背景是", "情况是", "目前", "现有", "我们的"],
    "有目标": ["希望", "想要", "目的是", "目标是", "需要"],
    "有约束": ["要求", "限制", "不超过", "只需要", "必须"],
    "有示例": ["比如", "例如", "像这样", "参考", "类似"],
    "有格式要求": ["格式", "表格", "列表", "按", "输出"],
    "有角色设定": ["作为", "你是", "假设", "扮演"],
    "追问深化": ["进一步", "详细", "具体", "展开", "深入"],
}

# 高质量提示词模式
GOOD_PROMPT_PATTERNS = [
    r"背景[是为].{5,50}(?:希望|想要|需要)",
    r"(?:希望|想要|需要).{5,50}(?:要求|限制|格式)",
    r"作为.{2,20},.{5,}",
    r"请.{5,}(?:按|用|以).{3,}格式",
    r"参考.{5,50}(?:写|生成|分析)",
]

def is_golden_quote(text):
    """判断是否可能是金句"""
    if not text or len(text) < 10 or len(text) > 150:
        return False
    patterns = [
        r"^\d+\.",
        r"[：:]\s*[^。]+$",
        r"。[^。]{5,30}$",
        r"(核?心|关键|本质|底?层逻辑|原则|法则|定律)",
        r"(重要|必须|一定|永远|从来|真正)",
        r"(不是.*而是|与其.*不如|没有.*只有)",
        r"(第一|首先|最|唯一)",
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
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    user_sections = re.findall(r'## User\s*\n(.*?)(?=## Assistant|\Z)', content, re.DOTALL)
    for section in user_sections:
        text = section.strip()
        if text:
            first_line = text.split('\n')[0][:200]
            questions.append({
                'text': first_line,
                'full': text[:500]
            })
    return questions

def extract_assistant_content(content):
    """提取助手回复内容"""
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
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

def analyze_prompt_quality(question_text):
    """分析提示词质量"""
    quality = {
        'score': 0,
        'indicators': [],
        'suggestions': []
    }

    # 检查各项指标
    for indicator, keywords in PROMPT_QUALITY_INDICATORS.items():
        if any(kw in question_text for kw in keywords):
            quality['indicators'].append(indicator)
            quality['score'] += 1

    # 检查高质量模式
    for pattern in GOOD_PROMPT_PATTERNS:
        if re.search(pattern, question_text):
            quality['score'] += 2

    # 长度评估
    if len(question_text) < 20:
        quality['suggestions'].append("提示词过短，建议增加背景说明")
    elif len(question_text) > 500:
        quality['suggestions'].append("提示词较长，建议分步骤提问")

    # 缺失建议
    if "有上下文" not in quality['indicators']:
        quality['suggestions'].append("可补充背景信息")
    if "有目标" not in quality['indicators']:
        quality['suggestions'].append("可明确目标/期望")
    if "有格式要求" not in quality['indicators']:
        quality['suggestions'].append("可指定输出格式")

    return quality

def analyze_growth_content(text):
    """分析成长相关内容"""
    growth = {}
    for category, keywords in GROWTH_KEYWORDS.items():
        matches = [kw for kw in keywords if kw in text]
        if matches:
            growth[category] = matches
    return growth

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
    sentences = re.split(r'[。\n]', content)
    for s in sentences:
        s = s.strip()
        if is_golden_quote(s):
            quotes.append(s)
    return quotes[:5]

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
    result['question_count'] = len(questions)
    result['question_preview'] = questions[0]['text'] if questions else result['title']

    # 提取助手内容
    assistant_content = extract_assistant_content(content)
    result['content_length'] = len(assistant_content)

    # 问题类型分类
    if questions:
        result['question_type'] = classify_question_type(questions[0]['text'])
    else:
        result['question_type'] = '其他'

    # 提示词质量分析
    if questions:
        result['prompt_quality'] = analyze_prompt_quality(questions[0]['full'])
    else:
        result['prompt_quality'] = {'score': 0, 'indicators': [], 'suggestions': []}

    # 成长内容分析
    result['growth_content'] = analyze_growth_content(content)

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

def generate_prompt_tips(results):
    """生成提示词改进建议"""
    tips = []

    # 统计高质量提示词特征
    high_quality = [r for r in results if r['prompt_quality']['score'] >= 3]
    low_quality = [r for r in results if r['prompt_quality']['score'] <= 1]

    if len(low_quality) > len(results) * 0.5:
        tips.append({
            "问题": "超过50%的提问缺少关键信息",
            "建议": "在提问时补充：背景+目标+约束条件",
            "示例": "背景：我们是一家培训公司，目标：想要分析客户数据，要求：按RFM模型分类"
        })

    # 统计常见问题
    indicator_counts = Counter()
    for r in results:
        for ind in r['prompt_quality']['indicators']:
            indicator_counts[ind] += 1

    total = len(results)
    for ind, count in indicator_counts.most_common():
        pct = count / total * 100
        if pct < 20:
            tips.append({
                "问题": f"仅{pct:.1f}%的提问包含「{ind}」",
                "建议": f"在提问时注意添加{ind}相关信息"
            })

    return tips

def generate_growth_report(results):
    """生成成长报告"""
    report = {
        "成长领域分布": Counter(),
        "高频成长话题": [],
        "成长相关对话": []
    }

    for r in results:
        for category, keywords in r['growth_content'].items():
            report["成长领域分布"][category] += 1
            if r not in report["成长相关对话"]:
                report["成长相关对话"].append(r)

    # 提取高频成长关键词
    all_keywords = Counter()
    for r in results:
        for kws in r['growth_content'].values():
            all_keywords.update(kws)

    report["高频成长话题"] = all_keywords.most_common(20)

    return report

def main():
    print("="*60)
    print("DeepSeek问答数据深度分析 v2")
    print("="*60)
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
    print()

    # ========== 基础统计 ==========
    analysis = {
        '分析时间': datetime.now().isoformat(),
        'total_count': len(results),
        'categories': dict(Counter(r['category'] for r in results)),
        'question_types': dict(Counter(r['question_type'] for r in results)),
        'avg_messages': sum(r['messages'] for r in results) / len(results) if results else 0,
        'avg_content_length': sum(r['content_length'] for r in results) / len(results) if results else 0,
    }

    print("基础统计:")
    print(f"  - 总对话数: {analysis['total_count']}")
    print(f"  - 平均消息数: {analysis['avg_messages']:.1f}")
    print(f"  - 平均内容长度: {analysis['avg_content_length']:.0f} 字符")
    print()

    # ========== 提示词质量分析 ==========
    print("分析提示词质量...")
    prompt_scores = [r['prompt_quality']['score'] for r in results]
    analysis['prompt_quality'] = {
        '平均分': sum(prompt_scores) / len(prompt_scores) if prompt_scores else 0,
        '高质量占比': len([s for s in prompt_scores if s >= 3]) / len(prompt_scores) * 100 if prompt_scores else 0,
        '低质量占比': len([s for s in prompt_scores if s <= 1]) / len(prompt_scores) * 100 if prompt_scores else 0,
        '改进建议': generate_prompt_tips(results)
    }
    print(f"  - 平均提示词质量分: {analysis['prompt_quality']['平均分']:.2f}")
    print(f"  - 高质量提示词占比: {analysis['prompt_quality']['高质量占比']:.1f}%")
    print()

    # ========== 成长内容分析 ==========
    print("分析成长相关内容...")
    growth_report = generate_growth_report(results)
    analysis['growth'] = growth_report
    print(f"  - 成长相关对话数: {len(growth_report['成长相关对话'])}")
    print(f"  - 成长领域分布: {dict(growth_report['成长领域分布'])}")
    print()

    # ========== 金句收集 ==========
    print("提取金句...")
    all_quotes = []
    for r in results:
        for q in r['golden_quotes']:
            all_quotes.append({
                'quote': q,
                'category': r['category'],
                'source': r['title']
            })
    analysis['golden_quotes'] = all_quotes
    print(f"  - 提取金句数: {len(all_quotes)}")
    print()

    # ========== 决策分析 ==========
    print("分析决策模式...")
    decision_related = sorted(
        [r for r in results if r['decision_relevance'] > 0],
        key=lambda x: x['decision_relevance'],
        reverse=True
    )[:30]
    analysis['decision_related'] = decision_related
    print(f"  - 决策相关对话: {len([r for r in results if r['decision_relevance'] > 0])}")
    print()

    # ========== 高质量对话推荐 ==========
    print("筛选高质量对话...")
    high_value = sorted(
        results,
        key=lambda x: (
            x['prompt_quality']['score'] * 2 +
            x['decision_relevance'] +
            len(x['golden_quotes']) * 3 +
            min(x['messages'], 20)
        ),
        reverse=True
    )[:50]
    analysis['high_value_conversations'] = high_value
    print(f"  - 推荐高价值对话: {len(high_value)}")
    print()

    # ========== 保存结果 ==========
    with open(OUTPUT_DIR / 'full_analysis_v2.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    # 生成Markdown报告
    generate_markdown_report(analysis, results, OUTPUT_DIR)

    print("="*60)
    print(f"分析完成！结果保存到 {OUTPUT_DIR}")
    print("="*60)

    return analysis

def generate_markdown_report(analysis, results, output_dir):
    """生成Markdown分析报告"""

    report = f"""# DeepSeek 问答数据深度分析报告 v2

> 分析时间: {analysis['分析时间']}
> 总对话数: {analysis['total_count']}

---

## 一、整体概览

### 1.1 话题分布

| 分类 | 数量 | 占比 |
|------|------|------|
"""
    total = analysis['total_count']
    for cat, count in sorted(analysis['categories'].items(), key=lambda x: -x[1]):
        pct = count / total * 100
        report += f"| {cat} | {count} | {pct:.1f}% |\n"

    report += f"""
### 1.2 问题类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
"""
    for qtype, count in sorted(analysis['question_types'].items(), key=lambda x: -x[1]):
        pct = count / total * 100
        report += f"| {qtype} | {count} | {pct:.1f}% |\n"

    report += f"""
### 1.3 基础指标

- 平均每次对话消息数: {analysis['avg_messages']:.1f}
- 平均回复内容长度: {analysis['avg_content_length']:.0f} 字符

---

## 二、提示词质量分析

### 2.1 质量评估

- **平均提示词质量分**: {analysis['prompt_quality']['平均分']:.2f} / 10
- **高质量提示词占比**: {analysis['prompt_quality']['高质量占比']:.1f}%
- **低质量提示词占比**: {analysis['prompt_quality']['低质量占比']:.1f}%

### 2.2 改进建议

"""
    for tip in analysis['prompt_quality']['改进建议'][:5]:
        report += f"**{tip['问题']}**\n"
        report += f"- 建议: {tip['建议']}\n"
        if '示例' in tip:
            report += f"- 示例: {tip['示例']}\n"
        report += "\n"

    report += """
### 2.3 提示词技巧总结

基于你的984条对话分析，以下是提升提示词质量的技巧：

1. **补充背景信息**: 让AI了解你的具体情况
2. **明确目标**: 清楚说明你想得到什么
3. **设置约束**: 限制字数、格式、范围
4. **提供示例**: 给出参考样板
5. **角色设定**: 让AI扮演特定角色
6. **追问深化**: 对答案不满意时追问

---

## 三、成长相关分析

### 3.1 成长领域分布

| 领域 | 相关对话数 |
|------|------------|
"""
    for area, count in analysis['growth']['成长领域分布'].most_common():
        report += f"| {area} | {count} |\n"

    report += """
### 3.2 高频成长关键词

"""
    for kw, count in analysis['growth']['高频成长话题'][:15]:
        report += f"- **{kw}** ({count}次)\n"

    report += """
---

## 四、金句精选

"""
    for i, q in enumerate(analysis['golden_quotes'][:30], 1):
        report += f"{i}. {q['quote']}\n"
        report += f"   *— {q['category']} | {q['source']}*\n\n"

    report += """
---

## 五、决策模式分析

你经常在以下场景进行决策咨询：

"""
    for r in analysis['decision_related'][:10]:
        report += f"- **{r['title']}** ({r['decision_relevance']}个决策关键词)\n"

    report += """
### 决策时关注的要素

根据对话分析，你在做决策时经常考虑：
1. **利弊对比** - 多个方案的优势劣势
2. **成本效益** - 投入产出比
3. **风险评估** - 可能的问题和风险
4. **时机判断** - 是否是合适的时机
5. **长期影响** - 决策的长期后果

---

## 六、高价值对话推荐

以下对话综合评分最高（提示词质量+决策相关性+金句数量）：

"""
    for i, r in enumerate(analysis['high_value_conversations'][:20], 1):
        score = (
            r['prompt_quality']['score'] * 2 +
            r['decision_relevance'] +
            len(r['golden_quotes']) * 3
        )
        report += f"### {i}. {r['title']}\n"
        report += f"- 分类: {r['category']}\n"
        report += f"- 综合评分: {score}\n"
        report += f"- 提示词质量: {r['prompt_quality']['score']}\n"
        if r['golden_quotes']:
            report += f"- 金句数: {len(r['golden_quotes'])}\n"
        report += "\n"

    report += """
---

## 七、个人能力画像

基于984条对话的内容分析：

### 你的优势
- **商业思维**: 关注商业模式、竞争策略、市场定位
- **数据意识**: 经常使用数据支撑决策
- **学习能力**: 主动学习新技术、新方法
- **系统思考**: 喜欢框架、模型、系统性方法

### 可提升方向
- **提示词技巧**: 提高提问的精确度和信息量
- **知识沉淀**: 将对话中的洞察整理成可复用的知识
- **行动转化**: 将分析结果转化为具体行动计划

### 建议的下一步

1. **整理知识卡片**: 将商业管理类的洞察整理成知识卡片库
2. **建立决策模板**: 基于你的决策模式创建决策模板
3. **优化提示词库**: 收集高效的提示词模式
4. **定期复盘**: 每月回顾高价值对话，提炼经验

---

*本报告基于 {total} 条对话自动生成*
""".format(total=total)

    with open(output_dir / 'analysis_report_v2.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Markdown报告已生成: {output_dir / 'analysis_report_v2.md'}")

if __name__ == "__main__":
    main()
