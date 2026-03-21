"""Playwright 浏览器操作封装"""
import asyncio
import re
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Page, BrowserContext


class DeepSeekBrowser:
    """Deepseek 网页操作封装"""

    BASE_URL = "https://chat.deepseek.com"

    # 选择器（基于 DOM 探索结果）
    SELECTORS = {
        "chat_link": "a[href^='/a/chat/s/']",  # 对话链接
        "message": "[class*='ds-message']",  # 消息容器
    }

    def __init__(self, user_data_dir: str = "./browser_data", headless: bool = False):
        self.user_data_dir = Path(user_data_dir)
        self.headless = headless
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        """启动浏览器"""
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self._playwright = await async_playwright().start()
        self.context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=self.headless
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

    async def close(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if hasattr(self, '_playwright'):
            await self._playwright.stop()

    async def goto_home(self):
        """导航到 Deepseek 首页"""
        await self.page.goto(self.BASE_URL)
        await self.page.wait_for_load_state("networkidle")

    async def wait_for_login(self) -> bool:
        """等待用户登录，返回是否登录成功"""
        try:
            # 等待对话链接出现（登录后的标志）
            await self.page.wait_for_selector(self.SELECTORS["chat_link"], timeout=300000)
            return True
        except Exception:
            return False

    async def get_chat_list(self) -> list[dict]:
        """获取对话列表"""
        # 先滚动加载所有对话
        await self._scroll_to_load_all_chats()

        chat_links = await self.page.query_selector_all(self.SELECTORS["chat_link"])
        chats = []
        seen_ids = set()

        for link in chat_links:
            href = await link.get_attribute("href")
            if not href:
                continue

            # 提取对话 ID: /a/chat/s/{uuid}
            match = re.search(r'/a/chat/s/([a-f0-9-]+)', href)
            if not match:
                continue

            chat_id = match.group(1)
            if chat_id in seen_ids:
                continue
            seen_ids.add(chat_id)

            # 获取标题
            title = await link.text_content()
            title = title.strip() if title else f"untitled-{chat_id[:8]}"

            chats.append({
                "id": chat_id,
                "title": title,
                "url": f"{self.BASE_URL}/a/chat/s/{chat_id}"
            })

        return chats

    async def _scroll_to_load_all_chats(self):
        """滚动加载所有对话列表"""
        # 使用 JavaScript 在页面上下文中完成所有滚动
        await self.page.evaluate('''() => {
            return new Promise((resolve) => {
                // 找到 scrollHeight 最大的滚动容器
                const scrollAreas = document.querySelectorAll('[class*="ds-scroll-area"]');
                let sidebar = null;
                let maxScrollHeight = 0;

                for (const area of scrollAreas) {
                    if (area.scrollHeight > maxScrollHeight) {
                        maxScrollHeight = area.scrollHeight;
                        sidebar = area;
                    }
                }

                if (!sidebar) {
                    resolve();
                    return;
                }

                let prevCount = 0;
                let noChangeCount = 0;
                let scrollCount = 0;

                const scroll = () => {
                    sidebar.scrollTop = sidebar.scrollHeight;
                    scrollCount++;

                    // 检查对话链接数量
                    const links = document.querySelectorAll('a[href^="/a/chat/s/"]');
                    const currentCount = links.length;

                    if (currentCount === prevCount) {
                        noChangeCount++;
                    } else {
                        noChangeCount = 0;
                    }

                    prevCount = currentCount;

                    // 连续 5 次没变化或滚动超过 100 次，停止
                    if (noChangeCount >= 5 || scrollCount >= 100) {
                        resolve();
                    } else {
                        setTimeout(scroll, 500);
                    }
                };

                scroll();
            });
        }''')

    async def open_chat(self, chat_id: str):
        """打开指定对话"""
        url = f"{self.BASE_URL}/a/chat/s/{chat_id}"
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
        # 等待消息加载
        await asyncio.sleep(1)

    async def get_chat_content(self) -> list[dict]:
        """获取当前对话内容，保留 Markdown 格式"""
        # 先滚动加载所有消息
        await self._scroll_to_load_all_messages()

        # 使用 JavaScript 提取格式化的消息内容
        messages = await self.page.evaluate('''() => {
            const msgElements = document.querySelectorAll('[class*="ds-message"]');
            const results = [];

            for (const msg of msgElements) {
                // 判断角色
                const parent = msg.parentElement;
                const parentStyle = parent?.getAttribute('style') || '';
                const isAssistant = parentStyle.includes('assistant');
                const role = isAssistant ? 'assistant' : 'user';

                // 提取格式化内容
                let content = '';

                // 查找消息内容区域（排除思考区域）
                const contentAreas = msg.querySelectorAll('p, h1, h2, h3, h4, li, pre code, blockquote');

                if (contentAreas.length > 0) {
                    const parts = [];
                    for (const el of contentAreas) {
                        // 跳过思考区域
                        if (el.closest('[class*="think"]')) continue;

                        let text = '';
                        const tagName = el.tagName.toLowerCase();

                        if (tagName === 'p') {
                            text = el.textContent.trim();
                        } else if (tagName.match(/^h[1-4]$/)) {
                            const level = tagName[1];
                            text = '#'.repeat(parseInt(level)) + ' ' + el.textContent.trim();
                        } else if (tagName === 'li') {
                            text = '- ' + el.textContent.trim();
                        } else if (tagName === 'pre' || el.closest('pre')) {
                            text = '``\\n' + el.textContent.trim() + '\\n``';
                        } else if (tagName === 'blockquote') {
                            text = '> ' + el.textContent.trim();
                        } else {
                            text = el.textContent.trim();
                        }

                        if (text) parts.push(text);
                    }
                    content = parts.join('\\n\\n');
                }

                // 如果没有找到结构化内容，使用全文
                if (!content) {
                    content = msg.textContent.trim();
                }

                if (content) {
                    results.push({ role, content });
                }
            }

            return results;
        }''')

        return messages

    async def _scroll_to_load_all_messages(self):
        """滚动加载所有消息"""
        # 获取消息区域滚动容器
        scroll_area = await self.page.query_selector('[class*="ds-scroll-area"]')
        if not scroll_area:
            return

        # 多次滚动到顶部（历史消息在上面）
        for _ in range(5):
            await scroll_area.evaluate('el => { el.scrollTop = 0; }')
            await asyncio.sleep(0.5)

        # 再滚动到底部确保所有消息加载
        for _ in range(3):
            await scroll_area.evaluate('el => { el.scrollTop = el.scrollHeight; }')
            await asyncio.sleep(0.3)
