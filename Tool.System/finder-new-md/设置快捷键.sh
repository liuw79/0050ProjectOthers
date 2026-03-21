#!/bin/bash

echo "========================================="
echo "  设置「新建md」快捷键"
echo "========================================="
echo ""

echo "请按照以下步骤设置快捷键："
echo ""
echo "1️⃣  打开「系统设置」（System Settings）"
echo ""
echo "2️⃣  点击「键盘」（Keyboard）"
echo ""
echo "3️⃣  点击「键盘快捷键...」按钮"
echo ""
echo "4️⃣  左侧选择「服务」（Services）"
echo ""
echo "5️⃣  在右侧找到「新建md」"
echo "    （可能在「文件和文件夹」或「通用」分类下）"
echo ""
echo "6️⃣  双击右侧的快捷键区域"
echo ""
echo "7️⃣  按下你想要的快捷键组合"
echo ""
echo "推荐的快捷键："
echo "  • ⌘⇧M  (Command + Shift + M)"
echo "  • ⌘⌃N  (Command + Control + N)"
echo "  • ⌘⌥M  (Command + Option + M)"
echo ""
echo "========================================="
echo ""

read -p "是否现在打开系统设置？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在打开系统设置..."
    open "x-apple.systempreferences:com.apple.preference.keyboard?Shortcuts"
    echo ""
    echo "✅ 已打开！请按照上述步骤操作"
else
    echo "稍后可以手动打开系统设置进行配置"
fi

echo ""
echo "设置完成后，在 Finder 中按下快捷键即可创建 MD 文件！"
echo ""
