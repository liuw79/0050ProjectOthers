-- 系统功能模块
-- 提供系统级别的实用功能

local systemUtils = {}
local config = require("config.settings").systemUtils

-- 音量控制
local function adjustVolume(delta)
    local currentVolume = hs.audiodevice.defaultOutputDevice():volume()
    local newVolume = math.max(0, math.min(100, currentVolume + delta))
    hs.audiodevice.defaultOutputDevice():setVolume(newVolume)
    hs.alert.show(string.format("音量: %d%%", newVolume))
end

-- 亮度控制
local function adjustBrightness(delta)
    local currentBrightness = hs.brightness.get()
    local newBrightness = math.max(0, math.min(100, currentBrightness + delta))
    hs.brightness.set(newBrightness)
    hs.alert.show(string.format("亮度: %d%%", newBrightness))
end

-- 切换勿扰模式
local function toggleDoNotDisturb()
    local script = [[
        tell application "System Events"
            tell process "Control Center"
                click menu bar item "Control Center" of menu bar 1
                delay 0.5
                click button "Do Not Disturb" of group 1 of window "Control Center"
            end tell
        end tell
    ]]
    
    hs.osascript.applescript(script)
    hs.alert.show("勿扰模式已切换")
end

-- 锁定屏幕
local function lockScreen()
    hs.caffeinate.lockScreen()
end

-- 睡眠系统
local function sleepSystem()
    hs.caffeinate.systemSleep()
end

-- 重启系统
local function restartSystem()
    local button = hs.dialog.blockAlert("确认重启", "确定要重启系统吗？", "重启", "取消")
    if button == "重启" then
        hs.caffeinate.restartSystem()
    end
end

-- 关机
local function shutdownSystem()
    local button = hs.dialog.blockAlert("确认关机", "确定要关闭系统吗？", "关机", "取消")
    if button == "关机" then
        hs.caffeinate.shutdownSystem()
    end
end

-- 清空废纸篓
local function emptyTrash()
    local script = [[
        tell application "Finder"
            empty trash
        end tell
    ]]
    
    hs.osascript.applescript(script)
    hs.alert.show("废纸篓已清空")
end

-- 获取系统信息
local function getSystemInfo()
    local battery = hs.battery.percentage()
    local isCharging = hs.battery.isCharging()
    local volume = hs.audiodevice.defaultOutputDevice():volume()
    local brightness = hs.brightness.get()
    local wifi = hs.wifi.currentNetwork()
    
    local info = string.format(
        "电池: %d%% %s\n音量: %d%%\n亮度: %d%%\nWiFi: %s",
        battery,
        isCharging and "(充电中)" or "",
        volume,
        brightness,
        wifi or "未连接"
    )
    
    hs.alert.show(info, 4)
end

-- 切换 WiFi
local function toggleWiFi()
    local script = [[
        tell application "System Events"
            tell process "Control Center"
                click menu bar item "Control Center" of menu bar 1
                delay 0.5
                click button "Wi-Fi" of group 1 of window "Control Center"
            end tell
        end tell
    ]]
    
    hs.osascript.applescript(script)
    hs.alert.show("WiFi 已切换")
end

-- 切换蓝牙
local function toggleBluetooth()
    local script = [[
        tell application "System Events"
            tell process "Control Center"
                click menu bar item "Control Center" of menu bar 1
                delay 0.5
                click button "Bluetooth" of group 1 of window "Control Center"
            end tell
        end tell
    ]]
    
    hs.osascript.applescript(script)
    hs.alert.show("蓝牙已切换")
end

-- 显示系统功能选择器
local function showSystemChooser()
    local choices = {
        {text = "系统信息", subText = "显示电池、音量、亮度等信息", action = "info"},
        {text = "锁定屏幕", subText = "立即锁定屏幕", action = "lock"},
        {text = "睡眠", subText = "让系统进入睡眠状态", action = "sleep"},
        {text = "重启", subText = "重启系统", action = "restart"},
        {text = "关机", subText = "关闭系统", action = "shutdown"},
        {text = "音量 +10", subText = "增加音量", action = "volumeUp"},
        {text = "音量 -10", subText = "减少音量", action = "volumeDown"},
        {text = "亮度 +10", subText = "增加亮度", action = "brightnessUp"},
        {text = "亮度 -10", subText = "减少亮度", action = "brightnessDown"},
        {text = "切换勿扰模式", subText = "开启/关闭勿扰模式", action = "dnd"},
        {text = "切换 WiFi", subText = "开启/关闭 WiFi", action = "wifi"},
        {text = "切换蓝牙", subText = "开启/关闭蓝牙", action = "bluetooth"},
        {text = "清空废纸篓", subText = "清空废纸篓中的所有文件", action = "trash"}
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        if choice.action == "info" then
            getSystemInfo()
        elseif choice.action == "lock" then
            lockScreen()
        elseif choice.action == "sleep" then
            sleepSystem()
        elseif choice.action == "restart" then
            restartSystem()
        elseif choice.action == "shutdown" then
            shutdownSystem()
        elseif choice.action == "volumeUp" then
            adjustVolume(10)
        elseif choice.action == "volumeDown" then
            adjustVolume(-10)
        elseif choice.action == "brightnessUp" then
            adjustBrightness(10)
        elseif choice.action == "brightnessDown" then
            adjustBrightness(-10)
        elseif choice.action == "dnd" then
            toggleDoNotDisturb()
        elseif choice.action == "wifi" then
            toggleWiFi()
        elseif choice.action == "bluetooth" then
            toggleBluetooth()
        elseif choice.action == "trash" then
            emptyTrash()
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择系统功能...")
    chooser:show()
end

-- 咖啡因模式（防止系统睡眠）
local caffeineEnabled = false
local function toggleCaffeine()
    caffeineEnabled = not caffeineEnabled
    if caffeineEnabled then
        hs.caffeinate.set("system", true)
        hs.alert.show("☕ 咖啡因模式已开启（防止睡眠）")
    else
        hs.caffeinate.set("system", false)
        hs.alert.show("😴 咖啡因模式已关闭")
    end
end

-- 初始化系统功能模块
function systemUtils.init()
    -- 系统功能选择器
    hs.hotkey.bind({"cmd", "shift"}, "s", function()
        showSystemChooser()
    end)
    
    -- 快速锁屏
    hs.hotkey.bind({"cmd", "ctrl"}, "l", function()
        lockScreen()
    end)
    
    -- 咖啡因模式切换
    hs.hotkey.bind({"cmd", "shift"}, "c", function()
        toggleCaffeine()
    end)
    
    -- 快速音量调节
    hs.hotkey.bind({"cmd", "shift"}, "=", function()
        adjustVolume(5)
    end)
    
    hs.hotkey.bind({"cmd", "shift"}, "-", function()
        adjustVolume(-5)
    end)
    
    -- 快速亮度调节
    hs.hotkey.bind({"cmd", "shift", "alt"}, "=", function()
        adjustBrightness(5)
    end)
    
    hs.hotkey.bind({"cmd", "shift", "alt"}, "-", function()
        adjustBrightness(-5)
    end)
    
    print("✅ 系统功能模块已加载")
end

-- 获取系统状态
function systemUtils.getSystemStatus()
    return {
        battery = hs.battery.percentage(),
        isCharging = hs.battery.isCharging(),
        volume = hs.audiodevice.defaultOutputDevice():volume(),
        brightness = hs.brightness.get(),
        wifi = hs.wifi.currentNetwork(),
        caffeineEnabled = caffeineEnabled
    }
end

return systemUtils