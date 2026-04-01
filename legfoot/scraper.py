#!/usr/bin/env python3
"""
Legfoot BBS Image Scraper
自动回复帖子并下载图片

Usage:
    python3 scraper.py --login            # 首次运行：打开浏览器登录
    python3 scraper.py --pages 1-5        # 抓取第1-5页所有帖子
    python3 scraper.py --post 12345       # 抓取指定帖子
    python3 scraper.py --url "http://..." # 抓取指定URL
    python3 scraper.py --pages 1 --dry-run  # 预览模式
"""

import argparse
import json
import logging
import os
import random
import re
import sys
import time
import urllib.parse
from pathlib import Path
import random

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
PROGRESS_FILE = BASE_DIR / "progress.json"
LOG_FILE = BASE_DIR / "scraper.log"
SESSION_DIR = Path("/tmp/legfoot_browser_session")

FORUM_BASE = "http://members.legfoot.net"
FORUM_URL = f"{FORUM_BASE}/showforum.cgi?forum=1"
LOGIN_URL = f"{FORUM_BASE}/login.cgi"
GOTO_TIMEOUT = 60_000
GOTO_WAIT = "domcontentloaded"

# ── 论坛账号 ─────────────────────────────────────────────────────────
FORUM_USER = "commy"
FORUM_PASS = "aaa111"

# ── logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── progress / helpers ───────────────────────────────────────────────
def load_progress():
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        # 兼容旧格式: completed=[id1,id2,...] -> completed={id: count,...}
        if isinstance(data.get("completed"), list):
            old_ids = data["completed"]
            data["completed"] = {pid: -1 for pid in old_ids}  # -1 = 未知数量
        if isinstance(data.get("failed"), list):
            data["failed"] = list(set(data["failed"]))
        return data
    return {"completed": {}, "failed": []}


def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2))


def scan_downloaded_images():
    """扫描 images/ 目录，统计每个帖子ID已下载的图片数。"""
    pid_count = {}
    for d in IMAGES_DIR.iterdir():
        if not d.is_dir():
            continue
        for f in d.iterdir():
            if f.is_file():
                # 文件名格式: {pid}_{NNN}.{ext}
                m = re.match(r"^(\d+)_", f.name)
                if m:
                    pid = m.group(1)
                    pid_count[pid] = pid_count.get(pid, 0) + 1
    return pid_count


def is_post_done(pid, progress, disk_images):
    """判断帖子是否已完整处理（有图片且记录在 progress 中）。"""
    if pid in progress.get("failed", []):
        return False
    if pid in progress.get("completed", {}):
        img_count = disk_images.get(pid, 0)
        # 已有图片才算真正完成
        return img_count > 0
    return False


def safe_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\n\r\t]', "_", name).strip()[:80]


def launch_browser(pw, headless=False):
    """启动 Playwright 浏览器，使用持久化 session 目录。"""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    return pw.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=headless,
        viewport={"width": 1280, "height": 900},
    )


def get_main_page(ctx):
    """获取浏览器的第一个页面（避免空白标签问题）。"""
    if ctx.pages:
        return ctx.pages[0]
    return ctx.new_page()


LOGIN_DONE_FILE = BASE_DIR / ".login_done"


def do_login(pw):
    """打开浏览器让用户手动登录。"""
    # 清除旧标记
    LOGIN_DONE_FILE.unlink(missing_ok=True)

    log.info("启动浏览器，请在弹出窗口中登录论坛…")
    ctx = launch_browser(pw, headless=False)
    page = ctx.new_page()
    page.goto(FORUM_URL, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)

    print("\n" + "=" * 50)
    print("  请在浏览器窗口中登录论坛")
    print("  登录成功后，在终端执行:")
    print(f"    touch {LOGIN_DONE_FILE}")
    print("  脚本会自动检测并继续…")
    print("=" * 50 + "\n")

    # 轮询等待标记文件
    while not LOGIN_DONE_FILE.exists():
        time.sleep(2)

    log.info("检测到登录完成信号，验证登录状态…")
    LOGIN_DONE_FILE.unlink(missing_ok=True)

    # 验证登录状态
    page.goto(FORUM_URL, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)
    is_guest = page.evaluate("() => document.body.innerText.includes('游客')")
    if is_guest:
        print("⚠ 未检测到登录状态，请重试")
        ctx.close()
        return False

    log.info("登录成功！Session 已保存。")
    ctx.close()
    return True


# ── forum listing ────────────────────────────────────────────────────
def get_thread_links(page, start=1, end=1):
    """从论坛列表页提取帖子链接。"""
    links = []
    for pn in range(start, end + 1):
        url = FORUM_URL if pn == 1 else f"{FORUM_BASE}/showforum.cgi?forum=1&page={pn}"
        log.info("列表页 %d: %s", pn, url)
        try:
            page.goto(url, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)
        except PlaywrightTimeout:
            log.warning("页面加载超时，继续解析已有内容")
        time.sleep(5)

        anchors = page.eval_on_selector_all(
            'a[href*="showtopic"]',
            """els => els.map(a => ({href: a.href, text: a.textContent.trim()}))
               .filter(x => x.text.length > 0 && !x.text.match(/^\\d+$/))""",
        )

        seen = set()
        for a in anchors:
            m = re.search(r"id=(\d+)", a["href"])
            if not m:
                continue
            pid = m.group(1)
            if pid in seen:
                continue
            seen.add(pid)
            links.append({"id": pid, "url": a["href"], "title": a["text"]})

        log.info("  找到 %d 个帖子", len(seen))
    return links


# ── single thread processing ────────────────────────────────────────
REPLY_POOL = [
    "感谢分享",
    "谢谢楼主分享",
    "好帖，感谢",
    "支持一下",
    "感谢分享，收藏了",
    "谢谢分享",
    "很不错，感谢楼主",
    "顶一下",
    "感谢楼主辛苦分享",
    "收藏了，谢谢",
]


def random_reply() -> str:
    return random.choice(REPLY_POOL)


def extract_model_name(title: str) -> str:
    """从帖子标题提取模特名字。如 'Model 杨晨晨Yome 26033116' -> '杨晨晨Yome'"""
    m = re.match(r"Model\s+(.+?)\s+\d{8,}", title)
    if m:
        return safe_name(m.group(1).strip())
    return safe_name(title)


def process_thread(context, info, *, delay=5, reply_text=None, dry_run=False):
    pid = info["id"]
    url = info["url"]
    title = safe_name(info["title"])
    model_name = extract_model_name(info["title"])
    save_dir = IMAGES_DIR / model_name

    if dry_run:
        log.info("[DRY-RUN] 会处理: %s  (%s)", title, url)
        return True

    save_dir.mkdir(parents=True, exist_ok=True)
    page = context.new_page()

    try:
        log.info("打开帖子: %s", title)
        try:
            page.goto(url, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)
        except PlaywrightTimeout:
            log.warning("帖子加载超时，继续操作")
        time.sleep(delay)

        # ── 检查是否已登录 ──────────────────────────────────────────
        has_login_link = page.evaluate(
            "() => { const links = [...document.querySelectorAll('a')]; "
            "return links.some(a => a.textContent.trim() === '登陆'); }"
        )
        if has_login_link:
            log.error("未登录！")
            return False

        # ── 检查附件是否需要回复 ───────────────────────────────────
        need_reply = page.evaluate(
            """() => {
                const text = document.body.innerText;
                return text.includes('需要回复') || text.includes('回复可见')
                    || text.includes('等级');
            }"""
        )

        if need_reply:
            # 寻找回复输入框
            textarea = page.query_selector(
                'textarea[name="inpost"], textarea[name="message"], '
                'textarea[name="body"], textarea[name="content"], '
                'textarea, #message, #inpost'
            )
            if textarea:
                actual_reply = reply_text or random_reply()
                log.info("需要回复，输入: %s", actual_reply)
                textarea.fill(actual_reply)
                time.sleep(2)

                btn = page.query_selector(
                    'input[type="submit"], button[type="submit"], '
                    'input[value*="回复"], input[value*="提交"], '
                    'input[value*="发表"]'
                )
                if btn:
                    btn.click()
                    log.info("回复已提交")
                else:
                    page.evaluate(
                        "() => { const f = document.querySelector('form'); "
                        "if (f) f.submit(); }"
                    )
                    log.info("通过 form.submit() 提交")
                time.sleep(delay)
            else:
                log.info("未找到回复框，尝试直接获取图片")
        else:
            log.info("无需回复，直接获取图片")

        # ── 收集图片 URL ────────────────────────────────────────────
        time.sleep(3)

        # 策略：从帖子内容区域查找大图
        image_urls = page.evaluate(
            """() => {
                const imgs = [...document.querySelectorAll('img')];
                return imgs
                    .filter(img => img.naturalWidth > 100 && img.naturalHeight > 100)
                    .filter(img => {
                        const s = img.src.toLowerCase();
                        // 内容图片特征
                        return s.includes('images.legfoot.net/uploads')
                            || s.includes('images.legfoot.net/attachments')
                            || s.includes('images.legfoot.net/photo')
                            || s.includes('upload') || s.includes('attachment')
                            || s.includes('photo');
                    })
                    .filter(img => {
                        const s = img.src.toLowerCase();
                        // 排除 UI 元素
                        return !s.includes('/avatars/') && !s.includes('/avatar')
                            && !s.includes('emoji') && !s.includes('smiley')
                            && !s.includes('/icon') && !s.includes('/logo')
                            && !s.includes('/banner') && !s.includes('images/star')
                            && !s.includes('images/lftitle') && !s.includes('images/vip')
                            && !s.includes('images/styles')
                            && !s.includes('members.legfoot.net/images/')
                            && !s.includes('signature.gif');
                    })
                    .map(img => img.src);
            }"""
        )

        # 如果精确匹配为空，宽松匹配
        if not image_urls:
            image_urls = page.evaluate(
                """() => {
                    const imgs = [...document.querySelectorAll('img')];
                    return imgs
                        .filter(img => img.naturalWidth > 200 && img.naturalHeight > 200)
                        .filter(img => {
                            const s = img.src.toLowerCase();
                            return s.includes('images.legfoot.net')
                                && !s.includes('/avatars/')
                                && !s.includes('members.legfoot.net/images/');
                        })
                        .map(img => img.src);
                }"""
            )

        # 去重
        image_urls = list(dict.fromkeys(image_urls))
        log.info("找到 %d 张图片", len(image_urls))

        # ── 下载图片 ────────────────────────────────────────────────
        for i, img_url in enumerate(image_urls, 1):
            parsed = urllib.parse.urlparse(img_url)
            ext = Path(parsed.path).suffix or ".jpg"
            fname = f"{pid}_{i:03d}{ext}"
            fpath = save_dir / fname

            if fpath.exists():
                log.info("  跳过已存在: %s", fname)
                continue

            try:
                resp = page.request.get(img_url)
                if resp.ok:
                    fpath.write_bytes(resp.body())
                    log.info("  下载: %s", fname)
                else:
                    log.warning("  HTTP %d: %s", resp.status, img_url)
            except Exception as e:
                log.error("  下载失败 %s: %s", img_url, e)

            time.sleep(2)

        return True

    except Exception as e:
        log.error("处理帖子 %s 出错: %s", pid, e)
        return False
    finally:
        page.close()


# ── main ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Legfoot BBS 图片抓取器")
    ap.add_argument("--pages", help="页码范围，如 1-5")
    ap.add_argument("--post", help="单个帖子 ID")
    ap.add_argument("--url", help="帖子直链")
    ap.add_argument("--delay", type=int, default=5, help="操作间隔秒数（默认 5）")
    ap.add_argument("--reply", default=None, help="回复内容（默认随机）")
    ap.add_argument("--skip-announcements", action="store_true", default=True,
                    help="跳过公告帖（默认开启）")
    ap.add_argument("--dry-run", action="store_true", help="仅预览，不执行")
    args = ap.parse_args()

    if not any([args.pages, args.post, args.url]):
        ap.print_help()
        sys.exit(1)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    progress = load_progress()

    # 扫描磁盘已有图片，构建去重依据
    disk_images = scan_downloaded_images()
    log.info("磁盘已有 %d 个帖子的图片（共 %d 张）",
             len(disk_images), sum(disk_images.values()))

    # 将磁盘数据同步到 progress（补漏）
    for pid, count in disk_images.items():
        if pid not in progress["completed"]:
            progress["completed"][pid] = count
            log.info("  补录磁盘帖子: %s (%d 张图片)", pid, count)
    save_progress(progress)

    # 清除登录标记
    LOGIN_DONE_FILE.unlink(missing_ok=True)

    with sync_playwright() as pw:
        # 启动浏览器（headless 模式即可，自动登录）
        ctx = launch_browser(pw, headless=True)
        try:
            # ── 先检查登录状态 ────────────────────────────────────
            pg = get_main_page(ctx)
            pg.goto(FORUM_URL, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)
            time.sleep(5)
            is_guest = pg.evaluate(
                "() => { const links = [...document.querySelectorAll('a')]; "
                "return links.some(a => a.textContent.trim() === '登陆'); }"
            )

            if is_guest:
                log.info("未登录，自动登录中…")
                pg.goto(LOGIN_URL, wait_until=GOTO_WAIT, timeout=GOTO_TIMEOUT)
                time.sleep(3)
                # 填写登录表单（字段名已确认：username, password）
                user_input = pg.query_selector('input[name="username"]')
                pass_input = pg.query_selector('input[name="password"]')
                submit_btn = pg.query_selector('input[type="submit"]')
                if user_input and pass_input:
                    user_input.fill(FORUM_USER)
                    pass_input.fill(FORUM_PASS)
                    time.sleep(1)
                    if submit_btn:
                        submit_btn.click()
                    else:
                        pg.evaluate("() => document.querySelector('form').submit()")
                    time.sleep(5)
                    log.info("自动登录完成")
                else:
                    log.error("未找到登录表单")
                    return
            else:
                log.info("已登录，开始抓取…")

            # ── 确定要处理的帖子列表 ────────────────────────────────
            threads = []

            if args.url:
                m = re.search(r"id=(\d+)", args.url)
                pid = m.group(1) if m else "unknown"
                threads = [{"id": pid, "url": args.url, "title": f"topic_{pid}"}]

            elif args.post:
                threads = [
                    {
                        "id": args.post,
                        "url": f"{FORUM_BASE}/showtopic.cgi?forum=1&id={args.post}",
                        "title": f"topic_{args.post}",
                    }
                ]

            elif args.pages:
                parts = args.pages.split("-")
                s = int(parts[0])
                e = int(parts[1]) if len(parts) > 1 else s
                pg = ctx.new_page()
                threads = get_thread_links(pg, s, e)
                pg.close()

            # 过滤公告帖
            if args.skip_announcements:
                ann_keywords = ["已封会员", "禁止传播", "净化网络", "禁止含有二维码",
                                "VIP 模特推介", "发帖量突破", "站庆", "全体会员"]
                before = len(threads)
                threads = [t for t in threads
                           if not any(kw in t["title"] for kw in ann_keywords)]
                log.info("过滤公告: %d → %d 个帖子", before, len(threads))

            log.info("共 %d 个帖子待处理", len(threads))

            # ── 逐帖处理 ────────────────────────────────────────────
            skipped = 0
            for t in threads:
                if not args.dry_run and is_post_done(t["id"], progress, disk_images):
                    skipped += 1
                    continue

                ok = process_thread(
                    ctx, t,
                    delay=args.delay,
                    reply_text=args.reply,
                    dry_run=args.dry_run,
                )
                if not args.dry_run:
                    if ok:
                        # 记录下载的图片数
                        new_count = len(list(
                            f for d in IMAGES_DIR.iterdir() if d.is_dir()
                            for f in d.iterdir()
                            if f.name.startswith(f"{t['id']}_")
                        ))
                        progress["completed"][t["id"]] = new_count
                    else:
                        if t["id"] not in progress["failed"]:
                            progress["failed"].append(t["id"])
                    save_progress(progress)
                time.sleep(args.delay)

            if skipped:
                log.info("跳过已下载: %d 个帖子", skipped)

        finally:
            ctx.close()

    log.info("全部完成！")


if __name__ == "__main__":
    main()
