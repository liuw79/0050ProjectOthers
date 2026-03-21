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
        "❓ 帮助系统: %s",
        "Cmd+Shift+V",
        "Opt+Cmd+P",
        "Cmd+Shift+N",
        "Cmd+Shift+W",
        "Cmd+Shift+S",
        "Cmd+Shift+T",
        "Opt+Cmd+M",
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

-- 加载Swipe.spoon实现四指手势
local function initSwipeGesture()
    local Swipe = hs.loadSpoon("Swipe")
    
    if Swipe then
        -- 配置四指下滑关闭窗口
        local current_id, threshold
        Swipe:start(4, function(direction, distance, id)
            if id == current_id then
                if distance > threshold then
                    threshold = math.huge -- 只触发一次
                    
                    if direction == "down" then
                        -- 静默关闭窗口，不显示提示
                        hs.eventtap.keyStroke({"cmd"}, "w")
                    end
                end
            else
                current_id = id
                threshold = 0.05 -- 降低阈值，提高响应速度
            end
        end)
        print("✅ 四指下滑关闭窗口功能已启用")
    else
        print("❌ Swipe.spoon加载失败，请检查安装")
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