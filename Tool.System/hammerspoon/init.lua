-- Hammerspoon 增强配置
-- 作者: 刘伟
-- 版本: 2.0
-- 功能: 模块化设计，包含剪贴板管理、个人信息、快速记笔记、窗口管理、系统功能等

-- 加载配置
print("🔍 开始加载配置...")
local success, settings = pcall(require, "config.settings")
if not success then
    print("❌ 配置加载失败: " .. tostring(settings))
    return
end
print("✅ 配置加载成功")

-- 加载所有功能模块
print("🔍 开始加载模块...")
local modules = {}

local moduleList = {
    {name = "clipboard", path = "modules.clipboard"},
    {name = "personalInfo", path = "modules.personal-info"},
    {name = "quickNote", path = "modules.quick-note"},
    {name = "windowManager", path = "modules.window-manager"},
    {name = "systemUtils", path = "modules.system-utils"},
    {name = "helpSystem", path = "modules.help-system"},
    {name = "pomodoro", path = "modules.pomodoro"},
    {name = "mediaProcessor", path = "modules.media-processor"},
    {name = "batteryMonitor", path = "modules.battery-monitor"},
    {name = "mediaKeys", path = "modules.media-keys"}
}

for _, moduleInfo in ipairs(moduleList) do
    local success, module = pcall(require, moduleInfo.path)
    if success then
        modules[moduleInfo.name] = module
        print("✅ " .. moduleInfo.name .. " 模块加载成功")
    else
        print("❌ " .. moduleInfo.name .. " 模块加载失败: " .. tostring(module))
    end
end

-- 初始化所有模块
local function initializeModules()
    print("🚀 正在初始化 Hammerspoon 模块...")
    
    for name, module in pairs(modules) do
        if module and module.init then
            local success, error = pcall(module.init)
            if success then
                print(string.format("✅ %s 模块初始化成功", name))
            else
                print(string.format("❌ %s 模块初始化失败: %s", name, error))
            end
        else
            print(string.format("⚠️  %s 模块没有 init 方法", name))
        end
    end
end

-- 显示启动信息
local function showStartupInfo()
    local info = string.format(
        "🎉 Hammerspoon 增强配置已加载\n\n" ..
        "📋 剪贴板管理: %s\n" ..
        "👤 个人信息: %s\n" ..
        "📝 快速记笔记: %s\n" ..
        "🪟 窗口管理: %s\n" ..
        "⚙️ 系统功能: %s\n" ..
        "🍒 番茄时钟: %s\n" ..
        "🎬 媒体处理: %s\n" ..
        "🔋 电池监控: %s\n" ..
        "🖐️ 手势功能: %s\n" ..
        "❓ 帮助系统: %s",
        "Cmd+Shift+V",
        "Opt+Cmd+P",
        "Cmd+Shift+N",
        "Cmd+Shift+W",
        "Cmd+Shift+S",
        "Cmd+Shift+T",
        "Opt+Cmd+M",
        "Cmd+Shift+B(状态) / Cmd+Opt+B(切换100%)",
        "四指下滑关闭窗口",
        "Cmd+Shift+H"
    )
    
    print(info)
    
    -- 显示欢迎信息
    if modules.helpSystem and modules.helpSystem.showWelcome then
        modules.helpSystem.showWelcome()
    end
end

-- 错误处理
local function handleError(error)
    print("❌ 配置加载出错: " .. tostring(error))
    hs.alert.show("配置加载出错，请检查日志", 3)
end

-- 主初始化函数
local function init()
    local success, error = pcall(function()
        -- 启用IPC模块
        hs.ipc.cliInstall()
        
        -- 初始化所有模块
        initializeModules()
        
        -- 显示启动信息
        showStartupInfo()
        
        print("🎉 Hammerspoon 增强配置加载完成!")
    end)
    
    if not success then
        handleError(error)
    end
end

-- 配置重载处理
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "r", function()
    hs.alert.show("重新加载配置...")
    hs.reload()
end)

-- 简单有效的四指下滑手势
local function initSwipeGesture()
    local Swipe = hs.loadSpoon("Swipe")
    
    if Swipe then
        local lastTriggerTime = 0
        local cooldownTime = 1.5 -- 1.5秒冷却时间
        
        Swipe:start(4, function(direction, distance, id)
            -- 只处理下滑手势，距离超过阈值
            if direction == "down" and distance > 0.1 then
                local currentTime = hs.timer.secondsSinceEpoch()
                
                -- 简单的冷却时间检查
                if currentTime - lastTriggerTime < cooldownTime then
                    return
                end
                
                lastTriggerTime = currentTime
                print("✅ 四指下滑触发")
                
                -- 直接发送 Cmd+W，简单有效
                hs.eventtap.keyStroke({"cmd"}, "w", 0)
            end
        end)
        
        print("✅ 四指下滑关闭功能已启用（简化版）")
    else
        print("❌ Swipe.spoon加载失败")
    end
end

-- 启动配置
init()

-- 初始化四指下滑手势
initSwipeGesture()

-- 导出模块供其他地方使用
return {
    modules = modules,
    settings = settings
}