-- Hammerspoon 全局配置文件
-- 这里存放所有可配置的参数，便于统一管理

local config = {}

-- 剪贴板管理配置
config.clipboard = {
    maxHistory = 20,  -- 最大历史记录数
    showKeybind = {"cmd", "shift", "v"},  -- 显示剪贴板历史快捷键
    enablePersistence = true,  -- 是否启用持久化存储
    historyFile = os.getenv("HOME") .. "/.hammerspoon/clipboard_history.json"
}

-- 个人信息配置
-- 默认示例数据，真实信息请在 personal-info-private.lua 中配置
config.personalInfo = {
    phone = "13800138000",
    email = "example@example.com",
    address = "示例地址",
    companyName = "示例公司",
    taxId = "000000000000000000",
    companyEmail = "company@example.com",
    idCard = "000000000000000000"
}

-- 尝试加载私有个人信息配置（如果存在）
local success, privateInfo = pcall(require, "config.personal-info-private")
if success and privateInfo then
    -- 用私有配置覆盖默认配置
    for key, value in pairs(privateInfo) do
        config.personalInfo[key] = value
    end
end

-- 快速记笔记配置
config.quickNote = {
    notesPath = os.getenv("HOME") .. "/Documents/Notes/",
    defaultCategory = "日常",
    keybind = {{"cmd", "shift"}, "n"},
    categories = {"工作", "学习", "生活", "想法", "日常", "数据字典"}
}

-- 窗口管理配置
config.windowManagement = {
    closeKeybind = {"cmd", "w"},
    swipeGesture = true,  -- 是否启用四指下滑关闭窗口
    animationDuration = 0.2
}

-- 电池监控配置
config.batteryMonitor = {
<<<<<<< HEAD:hammerspoon/config/settings.lua
    chargeLimit = 80,           -- 充电限制百分比（建议80%）
=======
    chargeLimit = 90,           -- 充电限制百分比（建议80%）
>>>>>>> 1724227 (fix: change clipboard history shortcut to Cmd+Shift+V):config/settings.lua
    lowBatteryThreshold = 20,   -- 低电量警告阈值
    enableNotifications = true,  -- 是否启用通知
    checkInterval = 60,         -- 检查间隔（秒）
    showMenuBar = true,         -- 是否显示菜单栏图标
    useBatt = true,             -- 是否使用batt命令行工具
    battPath = "/usr/local/bin/batt" -- batt命令行工具路径
}

-- 系统功能配置
config.system = {
    screenRecordKeybind = {"cmd", "shift", "5"},
    enableIPC = true,
    showLoadMessage = true
}

-- 番茄时钟配置
config.pomodoro = {
    duration = 25,  -- 番茄时钟时长（分钟）
    keybind = {"cmd", "shift", "t"},  -- 启动番茄时钟快捷键
    alwaysShow = true,  -- 是否总是显示菜单栏图标
    alertDuration = 5,  -- 提醒持续时间（秒）
    alertTextSize = 80,  -- 提醒文字大小
    enableNotification = true,  -- 是否启用系统通知
    enableSound = false  -- 是否启用提醒音效
}

-- 界面配置
config.ui = {
    theme = "dark",
    fontSize = 14,
    transparency = 0.9,
    cornerRadius = 8
}

return config