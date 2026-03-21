-- 增强窗口管理模块
-- 提供智能窗口布局和管理功能

local windowManager = {}
local config = require("config.settings").windowManager

-- 窗口布局预设
local layouts = {
    -- 左半屏
    leftHalf = hs.geometry.rect(0, 0, 0.5, 1),
    -- 右半屏
    rightHalf = hs.geometry.rect(0.5, 0, 0.5, 1),
    -- 上半屏
    topHalf = hs.geometry.rect(0, 0, 1, 0.5),
    -- 下半屏
    bottomHalf = hs.geometry.rect(0, 0.5, 1, 0.5),
    -- 左上角
    topLeft = hs.geometry.rect(0, 0, 0.5, 0.5),
    -- 右上角
    topRight = hs.geometry.rect(0.5, 0, 0.5, 0.5),
    -- 左下角
    bottomLeft = hs.geometry.rect(0, 0.5, 0.5, 0.5),
    -- 右下角
    bottomRight = hs.geometry.rect(0.5, 0.5, 0.5, 0.5),
    -- 中央 2/3
    center = hs.geometry.rect(1/6, 1/6, 2/3, 2/3),
    -- 最大化
    maximize = hs.geometry.rect(0, 0, 1, 1),
    -- 左 2/3
    leftTwoThirds = hs.geometry.rect(0, 0, 2/3, 1),
    -- 右 2/3
    rightTwoThirds = hs.geometry.rect(1/3, 0, 2/3, 1)
}

-- 获取当前聚焦窗口
local function getFocusedWindow()
    local win = hs.window.focusedWindow()
    if not win then
        hs.alert.show("没有聚焦的窗口")
        return nil
    end
    return win
end

-- 应用窗口布局
local function applyLayout(win, layout)
    if not win then return end
    
    local screen = win:screen()
    local frame = screen:frame()
    
    win:setFrame({
        x = frame.x + layout.x * frame.w,
        y = frame.y + layout.y * frame.h,
        w = layout.w * frame.w,
        h = layout.h * frame.h
    })
end

-- 智能窗口切换（循环不同大小）
local windowStates = {}
local function smartResize(win, layoutName)
    if not win then return end
    
    local winId = win:id()
    local currentState = windowStates[winId] or 0
    
    local cycles = {
        leftHalf = {"leftHalf", "leftTwoThirds", "leftHalf"},
        rightHalf = {"rightHalf", "rightTwoThirds", "rightHalf"},
        maximize = {"maximize", "center", "maximize"}
    }
    
    local cycle = cycles[layoutName] or {layoutName}
    currentState = (currentState % #cycle) + 1
    windowStates[winId] = currentState
    
    applyLayout(win, layouts[cycle[currentState]])
    hs.alert.show("窗口: " .. cycle[currentState])
end

-- 移动窗口到指定屏幕
local function moveToScreen(win, direction)
    if not win then return end
    
    local screen = win:screen()
    local nextScreen
    
    if direction == "next" then
        nextScreen = screen:next()
    elseif direction == "previous" then
        nextScreen = screen:previous()
    else
        return
    end
    
    if nextScreen then
        win:moveToScreen(nextScreen)
        hs.alert.show("窗口已移动到 " .. nextScreen:name())
    end
end

-- 显示窗口信息
local function showWindowInfo(win)
    if not win then return end
    
    local app = win:application()
    local screen = win:screen()
    local frame = win:frame()
    
    local info = string.format(
        "应用: %s\n标题: %s\n屏幕: %s\n位置: %.0f, %.0f\n大小: %.0f x %.0f",
        app:name(),
        win:title(),
        screen:name(),
        frame.x, frame.y,
        frame.w, frame.h
    )
    
    hs.alert.show(info, 3)
end

-- 显示窗口管理选择器
local function showWindowChooser()
    local choices = {
        {text = "左半屏", subText = "将窗口移动到左半屏", action = "leftHalf"},
        {text = "右半屏", subText = "将窗口移动到右半屏", action = "rightHalf"},
        {text = "上半屏", subText = "将窗口移动到上半屏", action = "topHalf"},
        {text = "下半屏", subText = "将窗口移动到下半屏", action = "bottomHalf"},
        {text = "左上角", subText = "将窗口移动到左上角", action = "topLeft"},
        {text = "右上角", subText = "将窗口移动到右上角", action = "topRight"},
        {text = "左下角", subText = "将窗口移动到左下角", action = "bottomLeft"},
        {text = "右下角", subText = "将窗口移动到右下角", action = "bottomRight"},
        {text = "居中", subText = "将窗口居中显示", action = "center"},
        {text = "最大化", subText = "最大化窗口", action = "maximize"},
        {text = "移动到下一屏幕", subText = "将窗口移动到下一个屏幕", action = "nextScreen"},
        {text = "移动到上一屏幕", subText = "将窗口移动到上一个屏幕", action = "prevScreen"},
        {text = "窗口信息", subText = "显示当前窗口详细信息", action = "info"}
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        local win = getFocusedWindow()
        if not win then return end
        
        if choice.action == "nextScreen" then
            moveToScreen(win, "next")
        elseif choice.action == "prevScreen" then
            moveToScreen(win, "previous")
        elseif choice.action == "info" then
            showWindowInfo(win)
        elseif layouts[choice.action] then
            applyLayout(win, layouts[choice.action])
            hs.alert.show("窗口: " .. choice.text)
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择窗口操作...")
    chooser:show()
end

-- 应用预设布局
local function applyPresetLayout(presetName)
    local preset = config.presets[presetName]
    if not preset then
        hs.alert.show("未找到预设: " .. presetName)
        return
    end
    
    for _, rule in ipairs(preset) do
        local app = hs.application.get(rule.app)
        if app then
            local windows = app:allWindows()
            for _, win in ipairs(windows) do
                if rule.title == nil or win:title():find(rule.title) then
                    applyLayout(win, layouts[rule.layout])
                end
            end
        end
    end
    
    hs.alert.show("已应用预设: " .. presetName)
end

-- 显示预设布局选择器
local function showPresetChooser()
    local choices = {}
    for name, _ in pairs(config.presets) do
        table.insert(choices, {
            text = name,
            subText = "应用 " .. name .. " 布局预设",
            preset = name
        })
    end
    
    if #choices == 0 then
        hs.alert.show("没有配置预设布局")
        return
    end
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            applyPresetLayout(choice.preset)
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择布局预设...")
    chooser:show()
end

-- 初始化窗口管理模块
function windowManager.init()
    -- 基本窗口操作快捷键
    hs.hotkey.bind({"cmd", "alt"}, "left", function()
        local win = getFocusedWindow()
        if win then smartResize(win, "leftHalf") end
    end)
    
    hs.hotkey.bind({"cmd", "alt"}, "right", function()
        local win = getFocusedWindow()
        if win then smartResize(win, "rightHalf") end
    end)
    
    hs.hotkey.bind({"cmd", "alt"}, "up", function()
        local win = getFocusedWindow()
        if win then applyLayout(win, layouts.topHalf) end
    end)
    
    hs.hotkey.bind({"cmd", "alt"}, "down", function()
        local win = getFocusedWindow()
        if win then applyLayout(win, layouts.bottomHalf) end
    end)
    
    hs.hotkey.bind({"cmd", "alt"}, "return", function()
        local win = getFocusedWindow()
        if win then smartResize(win, "maximize") end
    end)
    
    hs.hotkey.bind({"cmd", "alt"}, "c", function()
        local win = getFocusedWindow()
        if win then applyLayout(win, layouts.center) end
    end)
    
    -- 屏幕移动快捷键
    hs.hotkey.bind({"cmd", "alt", "shift"}, "right", function()
        local win = getFocusedWindow()
        if win then moveToScreen(win, "next") end
    end)
    
    hs.hotkey.bind({"cmd", "alt", "shift"}, "left", function()
        local win = getFocusedWindow()
        if win then moveToScreen(win, "previous") end
    end)
    
    -- 窗口管理选择器
    hs.hotkey.bind({"cmd", "shift"}, "w", function()
        showWindowChooser()
    end)
    
    -- 预设布局选择器
    hs.hotkey.bind({"cmd", "shift", "alt"}, "w", function()
        showPresetChooser()
    end)
    
    print("✅ 窗口管理模块已加载")
end

-- 获取窗口统计信息
function windowManager.getStats()
    local allWindows = hs.window.allWindows()
    local visibleWindows = hs.window.visibleWindows()
    local screens = hs.screen.allScreens()
    
    return {
        totalWindows = #allWindows,
        visibleWindows = #visibleWindows,
        screens = #screens,
        focusedWindow = hs.window.focusedWindow() and hs.window.focusedWindow():title() or "无"
    }
end

return windowManager