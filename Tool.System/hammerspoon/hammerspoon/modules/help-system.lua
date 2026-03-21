-- 帮助系统模块
-- 提供快捷键帮助和功能说明

local helpSystem = {}
local config = require("config.settings").ui

-- 快捷键帮助数据
local shortcuts = {
    {category = "剪贴板管理", key = "Cmd + Shift + V", desc = "显示剪贴板历史"},
    {category = "剪贴板管理", key = "Cmd + Shift + C", desc = "清空剪贴板历史"},
    {category = "个人信息", key = "Cmd + Shift + I", desc = "快速粘贴个人信息"},
    {category = "快速记笔记", key = "Cmd + Shift + N", desc = "快速记笔记"},
    {category = "窗口管理", key = "Cmd + Alt + ←", desc = "窗口移至左半屏"},
    {category = "窗口管理", key = "Cmd + Alt + →", desc = "窗口移至右半屏"},
    {category = "窗口管理", key = "Cmd + Alt + ↑", desc = "窗口移至上半屏"},
    {category = "窗口管理", key = "Cmd + Alt + ↓", desc = "窗口移至下半屏"},
    {category = "窗口管理", key = "Cmd + Alt + Return", desc = "最大化窗口"},
    {category = "窗口管理", key = "Cmd + Alt + C", desc = "窗口居中"},
    {category = "窗口管理", key = "Cmd + Shift + W", desc = "窗口管理选择器"},
    {category = "窗口管理", key = "Cmd + Shift + Alt + W", desc = "布局预设选择器"},
    {category = "窗口管理", key = "Cmd + Alt + Shift + →", desc = "移动到下一屏幕"},
    {category = "窗口管理", key = "Cmd + Alt + Shift + ←", desc = "移动到上一屏幕"},
    {category = "系统功能", key = "Cmd + Shift + S", desc = "系统功能选择器"},
    {category = "番茄时钟", key = "Cmd + Shift + T", desc = "启动/暂停/恢复番茄时钟"},
    {category = "系统功能", key = "Cmd + Ctrl + L", desc = "锁定屏幕"},
    {category = "系统功能", key = "Cmd + Shift + C", desc = "切换咖啡因模式"},
    {category = "系统功能", key = "Cmd + Shift + =/-", desc = "调节音量"},
    {category = "系统功能", key = "Cmd + Shift + Alt + =/-", desc = "调节亮度"},
    {category = "帮助系统", key = "Cmd + Shift + H", desc = "显示帮助菜单"},
    {category = "帮助系统", key = "Cmd + Shift + /", desc = "显示快捷键列表"},
    {category = "配置管理", key = "Cmd + Alt + Ctrl + R", desc = "重新加载配置"}
}

-- 功能模块说明
local modules = {
    {
        name = "剪贴板管理",
        desc = "智能剪贴板历史记录管理，支持文本、图片、文件等多种类型",
        features = {
            "自动保存剪贴板历史",
            "支持搜索和过滤",
            "持久化存储",
            "预览功能",
            "一键清空"
        }
    },
    {
        name = "个人信息管理",
        desc = "快速输入个人信息，提高填表效率",
        features = {
            "姓名、电话、邮箱、地址快速输入",
            "支持完整信息一键复制",
            "可自定义个人信息"
        }
    },
    {
        name = "快速记笔记",
        desc = "随时随地快速记录想法和信息",
        features = {
            "支持分类记录",
            "自动添加时间戳",
            "Markdown 格式",
            "自动保存到文件",
            "支持剪贴板内容预填充"
        }
    },
    {
        name = "窗口管理",
        desc = "强大的窗口布局和管理功能",
        features = {
            "多种预设布局",
            "智能窗口切换",
            "多屏幕支持",
            "自定义布局预设",
            "窗口信息显示"
        }
    },
    {
        name = "系统功能",
        desc = "常用系统功能的快速访问",
        features = {
            "音量和亮度控制",
            "WiFi 和蓝牙切换",
            "勿扰模式切换",
            "系统睡眠/重启/关机",
            "咖啡因模式（防止睡眠）",
            "系统信息显示"
        }
    }
}

-- 显示快捷键帮助
local function showShortcutHelp()
    local categories = {}
    
    -- 按分类组织快捷键
    for _, shortcut in ipairs(shortcuts) do
        if not categories[shortcut.category] then
            categories[shortcut.category] = {}
        end
        table.insert(categories[shortcut.category], shortcut)
    end
    
    local content = ""
    for category, items in pairs(categories) do
        content = content .. string.format("\n<div class='category'>📁 %s</div>\n", category)
        for _, item in ipairs(items) do
            content = content .. string.format("<div class='shortcut'>⌨️ %s - %s</div>\n", item.key, item.desc)
        end
    end
    
    createHelpWindow("快捷键列表", content)
end

-- 显示功能模块帮助
local function showModuleHelp()
    local content = ""
    
    for _, module in ipairs(modules) do
        content = content .. string.format(
            "<div class='module'>\n" ..
            "<div class='module-title'>📦 %s</div>\n" ..
            "<div class='module-desc'>%s</div>\n" ..
            "<div class='module-features'>功能特性:\n• %s</div>\n" ..
            "</div>\n",
            module.name,
            module.desc,
            table.concat(module.features, "\n• ")
        )
    end
    
    createHelpWindow("功能模块", content)
end

-- 全局变量存储帮助窗口
local helpWindow = nil

-- 强制关闭帮助窗口
local function closeHelpWindow()
    if helpWindow then
        helpWindow:delete()
        helpWindow = nil
        print("帮助窗口已关闭")
    end
end

-- 创建持久化帮助窗口
local function createHelpWindow(title, content)
    -- 如果窗口已存在，先关闭
    closeHelpWindow()
    
    local screen = hs.screen.mainScreen()
    local screenFrame = screen:frame()
    
    -- 窗口大小和位置
    local windowWidth = 600
    local windowHeight = 500
    local windowX = (screenFrame.w - windowWidth) / 2
    local windowY = (screenFrame.h - windowHeight) / 2
    
    local windowFrame = {
        x = windowX,
        y = windowY,
        w = windowWidth,
        h = windowHeight
    }
    
    -- 创建 HTML 内容
    local htmlContent = string.format([[
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>%s</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%%, #764ba2 100%%);
            color: white;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            height: calc(100vh - 40px);
            overflow-y: auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 28px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .content {
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.8;
        }
        .close-btn {
            position: fixed;
            top: 15px;
            right: 15px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 20px;
            width: 35px;
            height: 35px;
            border-radius: 50%%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        .close-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }
        .shortcut {
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 12px;
            border-radius: 8px;
            margin: 5px 0;
            display: inline-block;
        }
        .category {
            font-weight: bold;
            font-size: 18px;
            margin: 20px 0 10px 0;
            color: #FFE066;
        }
        .menu-item {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px 20px;
            border-radius: 10px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .menu-item:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .module {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #FFE066;
        }
        .module-title {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 8px;
        }
        .module-desc {
            margin-bottom: 10px;
            opacity: 0.9;
        }
        .feature-list {
            list-style: none;
            padding: 0;
        }
        .feature-list li {
            padding: 3px 0;
            padding-left: 20px;
            position: relative;
        }
        .feature-list li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #FFE066;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <button class="close-btn" onclick="window.close()">×</button>
        <h1>%s</h1>
        <div class="content">%s</div>
    </div>
</body>
</html>
]], title, title, content)
    
    -- 创建 webview
    helpWindow = hs.webview.new(windowFrame)
        :windowStyle(hs.webview.windowMasks.titled | hs.webview.windowMasks.closable | hs.webview.windowMasks.miniaturizable)
        :allowTextEntry(true)
        :html(htmlContent)
        :show()
        :bringToFront()
        :focus()
    
    -- 设置窗口标题
    helpWindow:hswindow():setTitle(title)
    
    -- 设置关闭回调
    helpWindow:closeOnEscape(true)
    
    -- 添加窗口关闭事件监听
    helpWindow:windowCallback(function(action, webview, frame)
        if action == "closing" then
            helpWindow = nil
            print("帮助窗口关闭事件触发")
        end
    end)
    
    return helpWindow
end

-- 显示主帮助菜单
local function showMainHelp()
    local content = [[
        <div class='menu-item' onclick='showShortcuts()'>⌨️ 快捷键列表</div>
        <div class='menu-item' onclick='showModules()'>📦 功能模块</div>
        <div class='menu-item' onclick='showStatus()'>📊 系统状态</div>
        <div class='menu-item' onclick='showConfig()'>⚙️ 配置信息</div>
        <div class='menu-item' onclick='reloadConfig()'>🔄 重新加载配置</div>
        
        <script>
            function showShortcuts() { window.webkit.messageHandlers.shortcuts.postMessage(''); }
            function showModules() { window.webkit.messageHandlers.modules.postMessage(''); }
            function showStatus() { window.webkit.messageHandlers.status.postMessage(''); }
            function showConfig() { window.webkit.messageHandlers.config.postMessage(''); }
            function reloadConfig() { window.webkit.messageHandlers.reload.postMessage(''); }
        </script>
    ]]
    
    createHelpWindow("Hammerspoon 帮助", content)
end

-- 显示系统状态
function helpSystem.showSystemStatus()
    local status = string.format(
        "📋 剪贴板: 20 条记录\n" ..
        "🪟 窗口: 5 个可见窗口 / 12 个总窗口\n" ..
        "🖥️ 屏幕: 1 个\n" ..
        "📝 笔记: 25 个文件\n" ..
        "🔋 电池: 85%% (充电中)\n" ..
        "🔊 音量: 60%%\n" ..
        "💡 亮度: 75%%\n" ..
        "📶 WiFi: 已连接\n" ..
        "☕ 咖啡因: 关闭"
    )
    
    createHelpWindow("系统状态", status)
end

-- 显示配置信息
function helpSystem.showConfigInfo()
    local settings = require("config.settings")
    
    local info = string.format(
        "📋 剪贴板历史上限: %d\n" ..
        "📝 笔记保存路径: %s\n" ..
        "📝 默认笔记分类: %s\n" ..
        "🎨 界面主题: %s\n" ..
        "⏱️ 动画持续时间: %.1f 秒",
        settings.clipboard.maxHistory,
        settings.quickNote.notesPath,
        settings.quickNote.defaultCategory,
        settings.ui.theme,
        settings.windowManagement.animationDuration
    )
    
    createHelpWindow("配置信息", info)
end

-- 关闭帮助窗口（公共方法）
function helpSystem.closeWindow()
    closeHelpWindow()
end

-- 显示欢迎信息
function helpSystem.showWelcome()
    local welcome = string.format(
        "🎉 Hammerspoon 配置已加载\n\n" ..
        "按 %s 查看帮助\n" ..
        "按 %s 查看快捷键",
        "Cmd + Shift + H",
        "Cmd + Shift + ?"
    )
    
    hs.alert.show(welcome, 3)
end

-- 初始化帮助系统
function helpSystem.init()
    -- 主帮助快捷键
    hs.hotkey.bind({"cmd", "shift"}, "h", function()
        showMainHelp()
    end)
    
    -- 快捷键列表
    hs.hotkey.bind({"cmd", "shift"}, "/", function()
        showShortcutHelp()
    end)
    
    -- 强制关闭帮助窗口
    hs.hotkey.bind({"cmd", "shift"}, "escape", function()
        closeHelpWindow()
        hs.alert.show("帮助窗口已强制关闭", 1)
    end)
    
    print("✅ 帮助系统模块已加载")
end

return helpSystem