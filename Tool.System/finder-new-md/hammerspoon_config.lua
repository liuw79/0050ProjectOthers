-- 新建 Markdown 文件快捷键配置
-- 将此代码添加到 init.lua 中

-- 加载 NewMarkdownFile 模块
hs.loadSpoon("NewMarkdownFile")

-- 绑定快捷键 ⌘⇧M
spoon.NewMarkdownFile:bindHotkeys({
    createMarkdown = {{"cmd", "shift"}, "M"}
})

hs.alert.show("新建 MD 快捷键已启用: ⌘⇧M", 2)
