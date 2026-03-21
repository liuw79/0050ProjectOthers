"""Obsidian 增强处理模块"""
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# 预定义分类关键词
CATEGORIES = {
    "AI": ["AI", "人工智能", "GPT", "Claude", "Deepseek", "LLM", "大模型", "ChatGPT", "机器学习", "深度学习"],
    "编程": ["代码", "编程", "Python", "JavaScript", "API", "函数", "bug", "调试", "开发", "Git", "GitHub"],
    "效率工具": ["工具", "效率", "Obsidian", "Notion", "快捷键", "自动化", "工作流", "插件"],
    "投资理财": ["股票", "投资", "基金", "理财", "财务", "分红", "收益", "市值"],
    "健康生活": ["健康", "运动", "饮食", "睡眠", "医疗", "医院", "药品", "锻炼", "健身"],
    "旅行出行": ["旅行", "旅游", "酒店", "机票", "景点", "签证", "出行", "交通"],
    "美食": ["美食", "餐厅", "菜谱", "烹饪", "食材", "饮品", "红酒", "咖啡"],
    "汽车": ["汽车", "特斯拉", "电动车", "驾驶", "车牌", "保养", "充电"],
    "教育学习": ["学习", "教育", "课程", "培训", "孩子", "学校", "考试", "读书"],
    "商业管理": ["管理", "创业", "企业", "团队", "员工", "客户", "营销", "战略", "品牌"],
    "房产家居": ["房子", "装修", "家具", "家电", "租房", "买房", "物业"],
    "法律": ["法律", "合同", "维权", "赔偿", "纠纷", "诉讼"],
    "科技数码": ["手机", "电脑", "Mac", "iPhone", "数码", "硬件", "设备", "购买"],
    "其他": []
}


def classify_content(content: str) -> str:
    """根据内容分类"""
    content_lower = content.lower()

    scores = {}
    for category, keywords in CATEGORIES.items():
        if category == "其他":
            continue
        score = sum(1 for kw in keywords if kw.lower() in content_lower)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)
    return "其他"


def extract_tags(content: str, title: str, max_tags: int = 3) -> list:
    """提取标签"""
    tags = []

    # 从标题提取关键实体
    title_keywords = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)
    for kw in title_keywords[:2]:
        if len(kw) >= 2 and kw not in ["什么", "怎么", "如何", "可以", "能否", "是否"]:
            tags.append(kw)

    # 根据内容添加分类标签
    category = classify_content(content)
    if category != "其他":
        tags.append(category)

    # 去重并限制数量
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)

    return unique_tags[:max_tags]


def find_related_topics(content: str, all_titles: list, current_title: str, max_links: int = 3) -> list:
    """查找相关话题"""
    related = []

    for title in all_titles:
        if title == current_title:
            continue

        # 简单的关键词匹配
        title_keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,4}', title))
        content_keywords = set(re.findall(r'[\u4e00-\u9fa5]{2,4}', content))

        common = title_keywords & content_keywords
        # 排除常见无意义词
        common -= {"什么", "怎么", "如何", "可以", "能否", "是否", "这个", "那个", "问题"}

        if len(common) >= 1:
            related.append((title, len(common)))

    # 按相关度排序
    related.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in related[:max_links]]


def add_frontmatter(content: str, tags: list, category: str, created: str, related: list) -> str:
    """添加 Obsidian frontmatter"""
    lines = ["---"]
    lines.append(f"tags: {tags}")
    lines.append(f"category: {category}")
    lines.append(f"created: {created}")
    if related:
        lines.append(f"related: {related}")
    lines.append("---")
    lines.append("")

    return "\n".join(lines) + content


def process_markdown_file(
    filepath: Path,
    all_titles: list,
    output_dir: Path,
    organized: bool = True
) -> dict:
    """处理单个 MD 文件"""
    content = filepath.read_text(encoding="utf-8")

    # 提取标题（第一个 # 行）
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem

    # 如果已经有 frontmatter，跳过
    if content.startswith("---"):
        return {"status": "skipped", "title": title, "reason": "已有 frontmatter"}

    # 提取标签和分类
    tags = extract_tags(content, title)
    category = classify_content(content)

    # 查找相关话题
    related = find_related_topics(content, all_titles, title)

    # 添加 frontmatter
    created = datetime.fromtimestamp(filepath.stat().st_ctime).strftime("%Y-%m-%d")
    new_content = add_frontmatter(content, tags, category, created, related)

    # 确定输出路径
    if organized:
        category_dir = output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        new_filepath = category_dir / filepath.name
    else:
        new_filepath = output_dir / filepath.name

    # 处理重名
    if new_filepath.exists():
        counter = 1
        while new_filepath.exists():
            new_filepath = new_filepath.parent / f"{filepath.stem}-{counter}.md"
            counter += 1

    new_filepath.write_text(new_content, encoding="utf-8")

    return {
        "status": "processed",
        "title": title,
        "category": category,
        "tags": tags,
        "related_count": len(related)
    }


def generate_moc(output_dir: Path, stats: dict) -> Path:
    """生成 MOC (Map of Content)"""
    moc_path = output_dir / "MOC.md"

    lines = ["# DeepSeek 对话索引", ""]
    lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 总计: {len(stats)} 条对话")
    lines.append("")

    # 按分类分组
    by_category = defaultdict(list)
    for item in stats:
        by_category[item.get("category", "其他")].append(item)

    for category in sorted(by_category.keys()):
        items = by_category[category]
        lines.append(f"## {category} ({len(items)})")
        lines.append("")

        for item in items:
            title = item["title"]
            # 创建相对路径链接
            lines.append(f"- [[{title}]]")

        lines.append("")

    moc_path.write_text("\n".join(lines), encoding="utf-8")
    return moc_path


def process_all_files(
    input_dir: str = "./exports",
    output_dir: str = "./exports_obsidian",
    organized: bool = True
):
    """处理所有 MD 文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 收集所有标题
    md_files = list(input_path.glob("*.md"))
    all_titles = []
    for f in md_files:
        content = f.read_text(encoding="utf-8")
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            all_titles.append(title_match.group(1))

    print(f"找到 {len(md_files)} 个 MD 文件")

    # 处理每个文件
    stats = []
    for i, filepath in enumerate(md_files):
        result = process_markdown_file(filepath, all_titles, output_path, organized)
        stats.append(result)

        if (i + 1) % 100 == 0:
            print(f"已处理 {i + 1}/{len(md_files)} 个文件")

    # 生成 MOC
    moc_path = generate_moc(output_path, stats)

    # 统计
    processed = sum(1 for s in stats if s["status"] == "processed")
    skipped = sum(1 for s in stats if s["status"] == "skipped")

    print(f"\n处理完成！")
    print(f"已处理: {processed} | 跳过: {skipped}")
    print(f"输出目录: {output_path.absolute()}")
    print(f"MOC: {moc_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Obsidian 增强处理")
    parser.add_argument("-i", "--input", default="./exports", help="输入目录")
    parser.add_argument("-o", "--output", default="./exports_obsidian", help="输出目录")
    parser.add_argument("--flat", action="store_true", help="不按分类组织（扁平结构）")

    args = parser.parse_args()

    process_all_files(
        input_dir=args.input,
        output_dir=args.output,
        organized=not args.flat
    )
