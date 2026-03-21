#!/bin/bash

PAGE_ID="3A82DB4F2BD93473F7B7C21F9B9E35D2"
SEARCH_TERM="企业实战型商学院"

echo "🔍 开始自动化Google搜索..."
echo "页面ID: $PAGE_ID"
echo "搜索词: $SEARCH_TERM"
echo ""

# 等待页面完全加载
echo "⏳ 等待页面加载..."
sleep 3

# 执行搜索
echo "🖊️ 在搜索框输入搜索词并执行搜索..."

# 通过JavaScript执行搜索
SEARCH_JS="
const searchInput = document.querySelector('input[name=\"q\"]') ||
                   document.querySelector('textarea[name=\"q\"]') ||
                   document.querySelector('input[aria-label*=\"搜索\"]') ||
                   document.querySelector('input[title*=\"搜索\"]');

if (searchInput) {
    searchInput.value = '${SEARCH_TERM}';
    searchInput.focus();

    // 模拟按Enter键
    const event = new KeyboardEvent('keydown', {
        key: 'Enter',
        code: 'Enter',
        keyCode: 13,
        which: 13,
        bubbles: true
    });
    searchInput.dispatchEvent(event);

    // 也尝试提交表单
    const form = searchInput.closest('form');
    if (form) {
        form.submit();
    }

    'searchInput.value + \" - 搜索已执行\"';
} else {
    '未找到搜索框';
}
"

# 尝试导航到搜索结果页面
echo "🌐 导航到Google搜索结果页面..."
SEARCH_URL="https://www.google.com/search?q=$(echo "$SEARCH_TERM" | sed 's/ /+/g')"
curl -X POST "http://localhost:9222/json/runtime/callFunctionOn" \
  -H "Content-Type: application/json" \
  -d "{\"functionDeclaration\": \"function() { window.location.href = '$SEARCH_URL'; return '页面导航成功'; }\", \"returnByValue\": true}"

echo ""
echo "⏳ 等待搜索结果加载..."
sleep 5

# 提取搜索结果
echo "📋 提取前10条搜索结果..."

EXTRACT_JS="
const results = [];
const selectors = [
    'h3 a[href]',
    '.yuRUbf > a[href]',
    '.g .yuRUbf a',
    '.g h3 a',
    '[data-ved] h3 a'
];

let links = [];
for (const selector of selectors) {
    links = document.querySelectorAll(selector);
    if (links.length > 0) break;
}

for (let i = 0; i < Math.min(10, links.length); i++) {
    const link = links[i];
    if (link.href && link.href.startsWith('http') && !link.href.includes('google.com/search')) {
        const title = link.textContent.trim() || link.querySelector('h3')?.textContent?.trim() || '无标题';
        if (title && title !== '无标题') {
            results.push({
                index: results.length + 1,
                title: title,
                url: link.href
            });
        }
    }
}

console.log('找到 ' + results.length + ' 个有效搜索结果');
JSON.stringify(results, null, 2);
"

# 获取搜索结果页面
curl http://localhost:9222/json | jq -r '.[] | select(.url | contains("google.com/search")) | .id' > /tmp/google_search_page_id.txt

if [ -s /tmp/google_search_page_id.txt ]; then
    SEARCH_PAGE_ID=$(cat /tmp/google_search_page_id.txt)
    echo "找到搜索结果页面ID: $SEARCH_PAGE_ID"
else
    SEARCH_PAGE_ID=$PAGE_ID
    echo "使用原页面ID: $SEARCH_PAGE_ID"
fi

echo ""
echo "==================== 搜索结果 ===================="
echo ""

# 直接访问Google搜索结果页面
curl -s "https://www.google.com/search?q=$(echo "$SEARCH_TERM" | sed 's/ /%20/g')" | \
    grep -o '<h3[^>]*><a[^>]*href="[^"]*"[^>]*>[^<]*</a></h3>' | \
    head -10 | \
    sed -n 's/.*href="\([^"]*\)"[^>]*>\([^<]*\)<.*/\2\n\1/p' | \
    awk 'NR%2==1{title=$0} NR%2==0{printf "%d. %s\n   %s\n\n", (NR/2), title, $0}'

echo "🎉 搜索完成！"