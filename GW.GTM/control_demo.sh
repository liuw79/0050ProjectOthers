#!/bin/bash

PAGE_ID="F86FF4AB11A81DD8824FC785E498333D"

echo "🎯 开始操控Chrome浏览器中的搜索结果页面..."
echo "页面ID: $PAGE_ID"
echo ""

# 1. 在页面上添加一个醒目的标记
echo "✏️ 1. 在页面上添加AI操控标记..."
curl -s "http://localhost:9222/json/runtime/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "const marker = document.createElement(\"div\"); marker.innerHTML = \"🤖 由Claude AI正在操控此页面 - \" + new Date().toLocaleString(); marker.style.cssText = \"position: fixed; top: 10px; right: 10px; background: rgba(255,0,0,0.9); color: white; padding: 15px; border-radius: 10px; z-index: 9999; font-size: 16px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); animation: pulse 2s infinite;\"; document.head.insertAdjacentHTML(\"beforeend\", \"<style>@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }</style>\"); document.body.appendChild(marker); \"AI标记已添加\"",
    "returnByValue": true
  }' | jq -r '.result.value'

echo ""

# 2. 高亮第一个搜索结果
echo "🎯 2. 高亮第一个搜索结果..."
curl -s "http://localhost:9222/json/runtime/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "const firstResult = document.querySelector(\"h3 a, .yuRUbf a, [data-ved] h3 a\"); if (firstResult) { firstResult.style.cssText = \"background: yellow !important; border: 3px solid red !important; padding: 5px !important; border-radius: 5px !important;\"; firstResult.scrollIntoView({behavior: \"smooth\"}); \"第一个结果已高亮: \" + firstResult.textContent.trim(); } else { \"未找到搜索结果\"; }",
    "returnByValue": true
  }' | jq -r '.result.value'

echo ""

# 3. 选择并"复制"前3个搜索结果
echo "📋 3. 选择前3个搜索结果并模拟复制..."
curl -s "http://localhost:9222/json/runtime/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "const results = []; const links = document.querySelectorAll(\"h3 a, .yuRUbf a, [data-ved] h3 a\"); for (let i = 0; i < Math.min(3, links.length); i++) { const link = links[i]; if (link.href && !link.href.includes(\"google.com/search\")) { results.push({ index: i+1, title: link.textContent.trim(), url: link.href }); link.style.cssText += \"background: lightgreen !important; animation: blink 1s 3;\"; } } document.head.insertAdjacentHTML(\"beforeend\", \"<style>@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }</style>\"); JSON.stringify(results, null, 2);",
    "returnByValue": true
  }' | jq -r '.result.value'

echo ""

# 4. 模拟点击操作（不实际跳转）
echo "🖱️ 4. 模拟鼠标悬停效果..."
curl -s "http://localhost:9222/json/runtime/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "const allLinks = document.querySelectorAll(\"h3 a, .yuRUbf a\"); allLinks.forEach((link, index) => { link.addEventListener(\"mouseover\", () => { link.style.cssText += \"transform: scale(1.05) !important; transition: all 0.2s !important;\"; }); link.addEventListener(\"mouseout\", () => { link.style.transform = \"scale(1)\"; }); }); \"已为 \" + allLinks.length + \" 个链接添加悬停效果\"",
    "returnByValue": true
  }' | jq -r '.result.value'

echo ""

# 5. 获取页面信息并"复制"到剪贴板
echo "📄 5. 获取页面信息并复制..."
PAGE_INFO=$(curl -s "http://localhost:9222/json/runtime/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "JSON.stringify({ title: document.title, url: window.location.href, resultsCount: document.querySelectorAll(\"h3 a, .yuRUbf a\").length, timestamp: new Date().toISOString() }, null, 2)",
    "returnByValue": true
  }' | jq -r '.result.value')

echo "已复制到'剪贴板'的页面信息:"
echo "$PAGE_INFO"

echo ""
echo "🎉 浏览器操控演示完成！"
echo ""
echo "你现在可以在Chrome浏览器中看到："
echo "- 右上角红色的AI操控标记（带动画效果）"
echo "- 第一个搜索结果被黄色高亮"
echo "- 前3个搜索结果闪烁绿色（模拟复制）"
echo "- 所有链接都有悬停放大效果"