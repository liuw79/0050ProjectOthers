#!/bin/bash

echo "🔍 从Google搜索结果页面提取前10条链接..."
echo ""

# 直接获取搜索结果页面的HTML内容并解析
SEARCH_URL="https://www.google.com/search?q=%E4%BC%81%E4%B8%9A%E5%AE%9E%E6%88%98%E5%9E%8B%E5%95%86%E5%AD%A6%E9%99%A2"

echo "==================== 企业实战型商学院 - 前10条搜索结果 ===================="
echo ""

# 使用curl获取搜索结果并解析
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
     "$SEARCH_URL" | \
     grep -o '<h3[^>]*class="[^"]*"[^>]*><a[^>]*href="[^"]*"[^>]*data-ved="[^"]*"[^>]*>[^<]*</a></h3>\|<h3[^>]*><a[^>]*href="[^"]*"[^>]*>[^<]*</a></h3>' | \
     sed 's/<h3[^>]*><a[^>]*href="\([^"]*\)"[^>]*>\([^<]*\)<\/a><\/h3>/\2|\1/g' | \
     grep -v 'google.com' | \
     head -10 | \
     awk -F'|' '{printf "%d. %s\n   %s\n\n", NR, $1, $2}'

echo ""
echo "🎉 链接提取完成！"
echo ""
echo "💡 你现在可以在Chrome浏览器中看到："
echo "   1. 原始Google主页"
echo "   2. 搜索结果页面：企业实战型商学院"
echo "   3. 调试信息页面"