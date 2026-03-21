-- 安全的系统工具模块
-- 移除了蓝牙等可能导致权限问题的功能

local M = {}

-- 获取系统信息
local function getSystemInfo()
    local battery = hs.battery.percentage()
    local volume = hs.audiodevice.defaultOutputDevice():volume()
    local brightness = hs.brightness.get()
    
    local info = string.format([[
系统信息:
电池: %d%%
音量: %d%%
亮度: %d%%
]], battery, math.floor(volume), math.floor(brightness))
    
    hs.alert.show(info, 5)
end

-- 锁定屏幕
local function lockScreen()
    hs.caffeinate.lockScreen()
    hs.alert.show("屏幕已锁定")
end

-- 系统睡眠
local function sleepSystem()
    hs.caffeinate.systemSleep()
end

-- 调整音量
local function adjustVolume(delta)
    local device = hs.audiodevice.defaultOutputDevice()
    if device then
        local newVolume = math.max(0, math.min(100, device:volume() + delta))
        device:setVolume(newVolume)
        hs.alert.show("音量: " .. math.floor(newVolume) .. "%")
    end
end

-- 调整亮度
local function adjustBrightness(delta)
    local current = hs.brightness.get()
    local newBrightness = math.max(0, math.min(100, current + delta))
    hs.brightness.set(newBrightness)
    hs.alert.show("亮度: " .. math.floor(newBrightness) .. "%")
end

-- 显示系统功能选择器（安全版本）
local function showSystemChooser()
    local choices = {
        {text = "系统信息", subText = "显示电池、音量、亮度等信息", action = "info"},
        {text = "锁定屏幕", subText = "立即锁定屏幕", action = "lock"},
        {text = "睡眠", subText = "让系统进入睡眠状态", action = "sleep"},
        {text = "音量 +10", subText = "增加音量", action = "volumeUp"},
        {text = "音量 -10", subText = "减少音量", action = "volumeDown"},
        {text = "亮度 +10", subText = "增加亮度", action = "brightnessUp"},
        {text = "亮度 -10", subText = "减少亮度", action = "brightnessDown"}
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        if choice.action == "info" then
            getSystemInfo()
        elseif choice.action == "lock" then
            lockScreen()
        elseif choice.action == "sleep" then
            sleepSystem()
        elseif choice.action == "volumeUp" then
            adjustVolume(10)
        elseif choice.action == "volumeDown" then
            adjustVolume(-10)
        elseif choice.action == "brightnessUp" then
            adjustBrightness(10)
        elseif choice.action == "brightnessDown" then
            adjustBrightness(-10)
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择系统功能...")
    chooser:show()
end

-- 初始化函数
function M.init()
    -- 绑定快捷键
    hs.hotkey.bind({"cmd", "alt"}, "S", showSystemChooser)
    return true
end

-- 导出函数
M.showSystemChooser = showSystemChooser
M.getSystemInfo = getSystemInfo
M.lockScreen = lockScreen
M.sleepSystem = sleepSystem
M.adjustVolume = adjustVolume
M.adjustBrightness = adjustBrightness

return M