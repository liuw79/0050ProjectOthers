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

-- 自动安装 Swipe.spoon（如缺失）
local function autoInstallSwipe()
    local spoonsPath = os.getenv("HOME") .. "/.hammerspoon/Spoons"
    local swipeDir = spoonsPath .. "/Swipe.spoon"
    local coreFile = swipeDir .. "/init.lua"

    -- 检查是否已安装且完整
    if hs.fs.attributes(coreFile) then
        return true
    end

    print("🔧 Swipe.spoon 未安装或不完整，开始自动安装...")

    -- 如果目录存在但不完整，先删除
    if hs.fs.attributes(swipeDir) then
        hs.execute(string.format("/bin/rm -rf '%s'", swipeDir))
    end

    -- 确保目标目录存在
    hs.fs.mkdir(spoonsPath)

    -- 使用国内镜像下载
    local tmpZip = os.getenv("HOME") .. "/.hammerspoon/Swipe.spoon.zip"
    local url = "https://cdn.jsdelivr.net/gh/Hammerspoon/Spoons@master/Spoons/Swipe.spoon.zip"

    print("⏬ 从国内镜像下载: " .. url)
    local cmd = string.format("/usr/bin/curl -L --connect-timeout 10 -m 120 -o '%s' '%s'", tmpZip, url)
    local _, _, _, rc = hs.execute(cmd)

    if rc == 0 and hs.fs.attributes(tmpZip) then
        print("📦 解压 Swipe.spoon...")
        hs.execute(string.format("/usr/bin/unzip -q -o '%s' -d '%s'", tmpZip, spoonsPath))
        hs.execute(string.format("/bin/rm -f '%s'", tmpZip))

        -- 验证安装
        if hs.fs.attributes(coreFile) then
            print("✅ Swipe.spoon 安装成功")
            return true
        end
    end

    print("❌ 自动安装失败，请手动安装 Swipe.spoon")
    return false
end

autoInstallSwipe()


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

-- 使用 Swipe.spoon 实现四指下滑关闭窗口功能
local function initSwipeGesture()
    -- 尝试加载 Swipe.spoon（需要提前安装）
    local ok, err = pcall(function()
        hs.loadSpoon("Swipe")
    end)
    if not ok then
        print("⚠️ 无法加载 Swipe.spoon: " .. tostring(err))
        return nil
    end
    
    -- 检查 spoon.Swipe 是否成功加载
    if not spoon.Swipe then
        print("⚠️ Swipe.spoon 加载失败: spoon.Swipe 为 nil")
        return nil
    end

    -- 启动四指下滑手势监听
    spoon.Swipe:start(4, function(direction, distance, id)
        -- direction: "left", "right", "up", "down"
        -- distance: 0~1 之间的浮点数，表示滑动距离占触控板宽/高的比例
        if direction == "down" and distance > 0.2 then -- 滑动超过 20% 视为有效
            local frontmostApp    = hs.application.frontmostApplication()
            local frontmostWindow = hs.window.focusedWindow()
            if not frontmostWindow then return end

            local appName = frontmostApp:name() or ""
            print("🔄 四指下滑检测到，尝试关闭窗口: " .. appName)

            -- 针对浏览器优先关闭当前标签页（Cmd+W）；若已无标签，浏览器自身会关闭窗口/退出
            local browserApps = {
                ["Google Chrome"] = true,
                ["Google Chrome Canary"] = true,
                ["Brave Browser"] = true,
                ["Microsoft Edge"] = true,
                ["Safari"] = true,
                ["Arc"] = true,
                -- 新增支持的应用：Trae、Cursor、Ghostty
                ["Trae"] = true,
                ["Cursor"] = true,
                ["Ghostty"] = true,
                ["Ghostty Terminal"] = true
            }

            if browserApps[appName] then
                -- 发送 Cmd+W 关闭标签页（更符合浏览器的交互）
                hs.eventtap.keyStroke({"cmd"}, "w")
                return
            end

            -- Finder 及系统设置直接关闭窗口
            if appName == "Finder" or appName == "System Preferences" or appName == "系统偏好设置" then
                frontmostWindow:close()
            else
                local success = frontmostWindow:close()
                if not success then
                    frontmostApp:hide()
                end
            end
        end
    end)

    print("✅ 四指下滑手势（Swipe.spoon）监听已启动")
    return spoon.Swipe
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