"""
高维学堂品牌监控系统 - RSS 监控模块
"""
import os
import re
import sys
import yaml
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from urllib.parse import quote

# 添加全局工具路径
sys.path.insert(0, os.path.expanduser("~/.config"))
from mailer import send_email


def load_config(config_path: str = "config/monitor.yaml") -> Dict:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """清理文件名，移除非法字符"""
    text = re.sub(r'[<>:"/\\|?*\n\r\t]', '', text)
    text = re.sub(r'\s+', '_', text)
    if len(text) > max_length:
        text = text[:max_length]
    return text.strip()


def match_brands(title: str, content: str, brands: List[str]) -> List[str]:
    """匹配标题和内容中的品牌关键词（全词匹配）"""
    text = f"{title} {content}"
    matched = []
    for brand in brands:
        # 使用词边界匹配，避免 "DRAM" 匹配到 "DR"
        pattern = r'(?<![a-zA-Z])' + re.escape(brand) + r'(?![a-zA-Z])'
        if re.search(pattern, text, re.IGNORECASE):
            matched.append(brand)
    return matched


def fetch_rss(source: Dict) -> List[Dict]:
    """抓取 RSS 源"""
    entries = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "source": source["name"],
                "category": source.get("category", "未分类"),
            })
    except Exception as e:
        print(f"抓取 {source['name']} 失败: {e}")
    return entries


def fetch_baidu_news(keyword: str, max_results: int = 20) -> List[Dict]:
    """使用 Playwright 抓取百度新闻搜索结果"""
    entries = []
    try:
        from playwright.sync_api import sync_playwright

        url = f"https://www.baidu.com/s?wd={quote(keyword)}&tn=news&rtt=1&bsst=1&cl=2"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle")

            news_items = page.query_selector_all(".result-op")[:max_results]
            for item in news_items:
                title_elem = item.query_selector("h3 a, .t a")
                if not title_elem:
                    continue
                title = title_elem.inner_text().strip()
                if not title or len(title) < 3:
                    continue

                link = title_elem.get_attribute("href") or ""

                # 获取摘要
                summary_elem = item.query_selector(".c-abstract, .c-font-normal")
                summary = summary_elem.inner_text() if summary_elem else ""

                # 获取来源和时间
                source_elem = item.query_selector(".c-color-gray, .newTimeFactor")
                source_text = source_elem.inner_text() if source_elem else ""

                entries.append({
                    "title": title,
                    "link": link,
                    "published": source_text,
                    "summary": summary,
                    "source": "百度新闻",
                    "category": "搜索引擎",
                    "keyword": keyword,
                })

            browser.close()
    except Exception as e:
        print(f"抓取百度新闻 '{keyword}' 失败: {e}")
    return entries


def save_article(article: Dict, matched_brands: List[str], data_dir: str) -> str:
    """保存文章到本地文件"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    source = sanitize_filename(article["source"])
    title = sanitize_filename(article["title"])
    filename = f"{date_str}_{source}_{title}.md"

    Path(data_dir).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(data_dir, filename)

    content = f"""# {article['title']}

## 基本信息
- **来源**: {article['source']}
- **分类**: {article['category']}
- **发布时间**: {article['published']}
- **链接**: {article['link']}
- **匹配品牌**: {', '.join(matched_brands)}
- **抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 摘要
{article['summary']}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def notify_email(results: Dict, config: Dict) -> bool:
    """发送日报（仅当有匹配时）"""
    # 无匹配不发送日报
    if results['matched_articles'] == 0:
        print("今日无匹配，不发送日报")
        return False

    brands = config.get("brands", [])
    sources = config.get("rss_sources", [])

    subject = f"品牌监控日报 {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""品牌监控日报

执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

结果统计:
- 抓取文章: {results['total_fetched']} 条
- 匹配文章: {results['matched_articles']} 条

匹配文章列表:
"""
    for f in results['saved_files']:
        body += f"- {os.path.basename(f)}\n"

    # 添加搜索信息
    body += f"""
---
## 本次搜索信息

**信息源** ({len(sources)} 个):
{', '.join([s['name'] for s in sources])}

**品牌关键词** ({len(brands)} 个):
{', '.join(brands)}
"""

    return send_email(subject, body)


def get_weekly_files(data_dir: str) -> List[str]:
    """获取本周的匹配文件"""
    today = datetime.now()
    # 均以周一为一周开始
    monday = today - timedelta(days=today.weekday())
    week_start = monday.strftime("%Y-%m-%d")

    files = []
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith('.md') and f >= week_start:
                files.append(os.path.join(data_dir, f))
    return sorted(files)


def send_weekly_report(data_dir: str, config: Dict) -> bool:
    """发送周报"""
    files = get_weekly_files(data_dir)
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    brands = config.get("brands", [])
    sources = config.get("rss_sources", [])

    subject = f"品牌监控周报 {monday.strftime('%Y-%m-%d')} ~ {sunday.strftime('%Y-%m-%d')}"
    body = f"""品牌监控周报

时间范围: {monday.strftime('%Y-%m-%d')} ~ {sunday.strftime('%Y-%m-%d')}
发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

本周匹配文章: {len(files)} 篇

"""

    if files:
        for f in files:
            body += f"- {os.path.basename(f)}\n"
    else:
        body += "(本周无匹配文章)\n"

    # 添加搜索信息
    body += f"""
---
## 本次搜索信息

**信息源** ({len(sources)} 个):
{', '.join([s['name'] for s in sources])}

**品牌关键词** ({len(brands)} 个):
{', '.join(brands)}
"""

    return send_email(subject, body)


def run_monitor(config_path: str = "config/monitor.yaml") -> Dict:
    """运行监控"""
    config = load_config(config_path)
    brands = config["brands"]
    rss_sources = config["rss_sources"]
    data_dir = config.get("data_dir", "data")
    enable_baidu = config.get("enable_baidu_news", True)

    results = {
        "total_fetched": 0,
        "matched_articles": 0,
        "saved_files": [],
    }

    print(f"开始监控，共 {len(rss_sources)} 个 RSS 源")
    print(f"监控品牌: {len(brands)} 个")
    if enable_baidu:
        print(f"百度新闻: 已启用")
    print("-" * 50)

    # 1. 抓取 RSS 源
    for source in rss_sources:
        print(f"抓取: {source['name']} ...")
        entries = fetch_rss(source)
        results["total_fetched"] += len(entries)
        print(f"  获取 {len(entries)} 条")

        for entry in entries:
            matched = match_brands(entry["title"], entry["summary"], brands)
            if matched:
                filepath = save_article(entry, matched, data_dir)
                results["matched_articles"] += 1
                results["saved_files"].append(filepath)
                print(f"  ✓ 匹配: {entry['title'][:30]}... -> {matched}")

    # 2. 抓取百度新闻（按品牌关键词搜索）
    if enable_baidu:
        print("-" * 50)
        print("抓取百度新闻...")
        for brand in brands:
            print(f"  搜索: {brand}")
            entries = fetch_baidu_news(brand)
            results["total_fetched"] += len(entries)

            for entry in entries:
                # 百度新闻已经是按关键词搜索的，直接保存
                filepath = save_article(entry, [brand], data_dir)
                results["matched_articles"] += 1
                results["saved_files"].append(filepath)
                print(f"    ✓ {entry['title'][:30]}...")

    print("-" * 50)
    print(f"监控完成: 抓取 {results['total_fetched']} 条, 匹配 {results['matched_articles']} 条")

    # 周日发送周报，否则发送日报（仅当有匹配时）
    today = datetime.now()
    if today.weekday() == 6:  # 周日
        print("今日为周日，发送周报")
        send_weekly_report(data_dir, config)
    else:
        notify_email(results, config)

    return results


if __name__ == "__main__":
    run_monitor()
