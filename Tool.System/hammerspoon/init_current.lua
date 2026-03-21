-- Hammerspoon 简化配置
-- 只保留核心功能，避免权限问题

-- 加载设置
require("config.settings")

-- 只加载安全的核心模块
local personalInfo = require("modules.personal-info")
local clipboard = require("modules.clipboard")
local quickNote = require("modules.quick-note")
local windowManager = require("modules.window-management")

-- 初始化模块
if personalInfo and personalInfo.init then personalInfo.init() end
if clipboard and clipboard.init then clipboard.init() end
if quickNote and quickNote.init then quickNote.init() end
if windowManager and windowManager.init then windowManager.init() end

-- 简化的系统功能（移除蓝牙相关）
local function showSimpleSystemChooser()
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
            local battery = hs.battery.percentage()
            local volume = hs.audiodevice.defaultOutputDevice():volume()
            local brightness = hs.brightness.get()
            hs.alert.show(string.format("电池: %d%% | 音量: %d%% | 亮度: %d%%", 
                battery, math.floor(volume), math.floor(brightness)))
        elseif choice.action == "lock" then
            hs.caffeinate.lockScreen()
        elseif choice.action == "sleep" then
            hs.caffeinate.systemSleep()
        elseif choice.action == "volumeUp" then
            local device = hs.audiodevice.defaultOutputDevice()
            if device then
                device:setVolume(math.min(100, device:volume() + 10))
                hs.alert.show("音量: " .. math.floor(device:volume()) .. "%")
            end
        elseif choice.action == "volumeDown" then
            local device = hs.audiodevice.defaultOutputDevice()
            if device then
                device:setVolume(math.max(0, device:volume() - 10))
                hs.alert.show("音量: " .. math.floor(device:volume()) .. "%")
            end
        elseif choice.action == "brightnessUp" then
            local current = hs.brightness.get()
            hs.brightness.set(math.min(100, current + 10))
            hs.alert.show("亮度: " .. math.floor(hs.brightness.get()) .. "%")
        elseif choice.action == "brightnessDown" then
            local current = hs.brightness.get()
            hs.brightness.set(math.max(0, current - 10))
            hs.alert.show("亮度: " .. math.floor(hs.brightness.get()) .. "%")
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择系统功能...")
    chooser:show()
end

-- 简化的电池状态显示
local function showBatteryStatus()
    local battery = hs.battery.percentage()
    local isCharging = hs.battery.isCharging()
    local powerSource = hs.battery.powerSource()
    
    local status = isCharging and "充电中" or "未充电"
    local message = string.format("电池: %d%% (%s)\n电源: %s", 
        battery, status, powerSource)
    
    hs.alert.show(message, 3)
end

-- 快捷键绑定
hs.hotkey.bind({"cmd", "alt"}, "P", function()
    -- 个人信息快速输入
    if personalInfo and personalInfo.showChooser then
        personalInfo.showChooser()
    else
        hs.alert.show("个人信息模块未正确加载")
    end
end)

hs.hotkey.bind({"cmd", "alt"}, "B", function()
    -- 显示电池状态
    showBatteryStatus()
end)

hs.hotkey.bind({"cmd", "alt"}, "S", function()
    -- 系统功能
    showSimpleSystemChooser()
end)

hs.hotkey.bind({"cmd", "alt", "ctrl"}, "R", function()
    -- 重新加载配置
    hs.reload()
    hs.alert.show("Hammerspoon 配置已重新加载")
end)

-- 显示启动消息
hs.alert.show("Hammerspoon 简化版已启动", 2)