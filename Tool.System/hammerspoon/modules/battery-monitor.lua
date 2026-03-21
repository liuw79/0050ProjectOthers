-- 电池监控增强模块
-- 提供电池状态监控、充电提醒等功能
-- 集成batt命令行工具实现充电限制控制

local batteryMonitor = {}
local config = require("config.settings").batteryMonitor or {}

-- 默认配置
local defaultConfig = {
    chargeLimit = 80,           -- 充电限制百分比
    lowBatteryThreshold = 20,   -- 低电量警告阈值
    enableNotifications = true,  -- 是否启用通知
    checkInterval = 60,         -- 检查间隔（秒）
    showMenuBar = true,         -- 是否显示菜单栏图标
    useBatt = true,             -- 是否使用batt命令行工具
    battPath = "/usr/local/bin/batt" -- batt命令行工具路径
}

-- 合并配置
for key, value in pairs(defaultConfig) do
    if config[key] == nil then
        config[key] = value
    end
end

local menuBar = nil
local timer = nil
local lastBatteryLevel = nil
local lastChargingState = nil

-- 临时充电状态管理（使用全局变量保持状态）
if not _G.batteryMonitorState then
    _G.batteryMonitorState = {
        isTemporaryCharge = false,
        previousChargeLimit = nil
    }
end
local isTemporaryCharge = _G.batteryMonitorState.isTemporaryCharge
local previousChargeLimit = _G.batteryMonitorState.previousChargeLimit

-- 获取电池信息
local function getBatteryInfo()
    return {
        percentage = hs.battery.percentage(),
        isCharging = hs.battery.isCharging(),
        isCharged = hs.battery.isCharged(),
        amperage = hs.battery.amperage(),
        watts = hs.battery.watts(),
        cycles = hs.battery.cycles(),
        health = hs.battery.health(),
        timeRemaining = hs.battery.timeRemaining()
    }
end

-- 格式化时间
local function formatTime(minutes)
    if not minutes or minutes < 0 then
        return "计算中..."
    end
    
    local hours = math.floor(minutes / 60)
    local mins = minutes % 60
    
    if hours > 0 then
        return string.format("%d小时%d分钟", hours, mins)
    else
        return string.format("%d分钟", mins)
    end
end

-- 更新菜单栏
local function updateMenuBar()
    -- 如果菜单栏对象丢失且需要显示，则尝试重新创建
    if (not menuBar) and config.showMenuBar then
        menuBar = hs.menubar.new()
        if menuBar then
            menuBar:setMenu(createMenu)
        else
            return -- 创建失败直接退出，避免后续错误
        end
    end

    if not menuBar then return end
    
    local battery = getBatteryInfo()
    -- 使用更紧凑的显示格式，减少占用空间
    local percentage = battery.percentage or 0
    local title
    
    if battery.isCharging then
        title = string.format("⚡%d", percentage)
    elseif percentage <= config.lowBatteryThreshold then
        title = string.format("🪫%d", percentage)
    else
        title = string.format("🔋%d", percentage)
    end
    
    menuBar:setTitle(title)
    -- 设置菜单内容
    menuBar:setMenu(createMenu)
end

-- 创建菜单
local function createMenu()
    local battery = getBatteryInfo()
    local menu = {}
    
    -- 基本信息
    table.insert(menu, {
        title = string.format("电池电量: %d%%", battery.percentage or 0),
        disabled = true
    })
    
    table.insert(menu, {
        title = string.format("充电状态: %s", 
            battery.isCharging and "充电中" or 
            battery.isCharged and "已充满" or "使用电池"),
        disabled = true
    })
    
    if battery.timeRemaining and battery.timeRemaining > 0 then
        local timeText = battery.isCharging and "充满时间" or "剩余时间"
        table.insert(menu, {
            title = string.format("%s: %s", timeText, formatTime(battery.timeRemaining)),
            disabled = true
        })
    end
    
    table.insert(menu, { title = "-" })
    
    -- 详细信息
    table.insert(menu, {
        title = string.format("电池健康度: %s", battery.health or "未知"),
        disabled = true
    })
    
    table.insert(menu, {
        title = string.format("充电周期: %d", battery.cycles or 0),
        disabled = true
    })
    
    if battery.watts then
        table.insert(menu, {
            title = string.format("功率: %.1fW", battery.watts),
            disabled = true
        })
    end
    
    -- batt状态信息
    if config.useBatt and isBattAvailable() then
        local battLimit = getBattLimit()
        if battLimit then
            table.insert(menu, {
                title = string.format("系统充电限制: %d%%", battLimit),
                disabled = true
            })
        end
    end
    
    table.insert(menu, { title = "-" })
    
    -- 充电限制提醒
    if battery.isCharging and battery.percentage and battery.percentage >= config.chargeLimit then
        table.insert(menu, {
            title = string.format("⚠️ 已达到%d%%充电限制", config.chargeLimit),
            disabled = true
        })
        table.insert(menu, { title = "-" })
    end
    
    -- batt充电限制控制
    if config.useBatt and isBattAvailable() then
        -- 充电限制控制子菜单
        local limitSubmenu = {
            { title = "设置充电限制", disabled = true },
            { title = "60%", fn = function() batteryMonitor.setChargeLimit(60) end },
            { title = "70%", fn = function() batteryMonitor.setChargeLimit(70) end },
            { title = "80%", fn = function() batteryMonitor.setChargeLimit(80) end },
            { title = "90%", fn = function() batteryMonitor.setChargeLimit(90) end },
            { title = "100%", fn = function() batteryMonitor.setChargeLimit(100) end }
        }
        
        table.insert(menu, {
            title = "充电限制控制",
            menu = limitSubmenu
        })
        
        table.insert(menu, { title = "-" })
    end
    
    -- 操作选项
    table.insert(menu, {
        title = "打开活动监视器",
        fn = function()
            hs.application.launchOrFocus("Activity Monitor")
        end
    })
    
    table.insert(menu, {
        title = "打开系统信息",
        fn = function()
            hs.execute("open /Applications/Utilities/System\\ Information.app")
        end
    })
    
    table.insert(menu, { title = "-" })
    
    table.insert(menu, {
        title = "刷新",
        fn = function()
            -- 刷新电池状态，避免直接调用 updateMenuBar 造成循环
            checkBatteryStatus()
        end
    })
    
    return menu
end

-- 检查电池状态
local function checkBatteryStatus()
    local battery = getBatteryInfo()
    
    if not battery.percentage then return end
    
    -- 检查充电限制
    if config.enableNotifications and battery.isCharging then
        if battery.percentage >= config.chargeLimit and 
           (not lastBatteryLevel or lastBatteryLevel < config.chargeLimit) then
            hs.notify.new({
                title = "电池充电提醒",
                informativeText = string.format("电池已达到%d%%，建议停止充电以保护电池健康", config.chargeLimit),
                soundName = "Glass"
            }):send()
        end
    end
    
    -- 检查低电量
    if config.enableNotifications and not battery.isCharging then
        if battery.percentage <= config.lowBatteryThreshold and 
           (not lastBatteryLevel or lastBatteryLevel > config.lowBatteryThreshold) then
            hs.notify.new({
                title = "低电量警告",
                informativeText = string.format("电池电量仅剩%d%%，请及时充电", battery.percentage),
                soundName = "Sosumi"
            }):send()
        end
    end
    
    -- 更新状态
    lastBatteryLevel = battery.percentage
    lastChargingState = battery.isCharging
    
    -- 更新菜单栏
    updateMenuBar()
end

-- 初始化
function batteryMonitor.init()
    -- 清理现有资源
    if menuBar then
        menuBar:delete()
        menuBar = nil
    end
    
    if timer then
        timer:stop()
        timer = nil
    end
    
    if config.showMenuBar then
        menuBar = hs.menubar.new()
        if menuBar then
            -- 设置初始标题
            menuBar:setTitle("🔋--")
            
            -- 设置菜单生成函数
            menuBar:setMenu(createMenu)
        else
            return batteryMonitor
        end
    end
    
    -- 启动定时器
    timer = hs.timer.doEvery(config.checkInterval, checkBatteryStatus)
    
    -- 立即检查一次并更新显示
    checkBatteryStatus()
    
    -- 绑定快捷键
    batteryMonitor.bindHotkeys()
    
    return batteryMonitor
end

-- 停止监控
function batteryMonitor.stop()
    if timer then
        timer:stop()
        timer = nil
    end
    
    if menuBar then
        menuBar:delete()
        menuBar = nil
    end
end

-- 获取当前电池状态
function batteryMonitor.getStatus()
    return getBatteryInfo()
end

-- 检查batt命令是否可用
local function isBattAvailable()
    if not config.useBatt then return false end
    
    local output, status = hs.execute(string.format("[ -x \"%s\" ] && echo 1 || echo 0", config.battPath))
    return output:match("1") ~= nil
end

-- 使用batt设置充电限制
local function setBattLimit(limit)
    if not isBattAvailable() then
        hs.alert.show("未找到batt命令行工具")
        return false
    end
    
    -- batt命令需要sudo权限，使用osascript来请求管理员权限
    local script = string.format([[
        do shell script "sudo %s limit %d" with administrator privileges
    ]], config.battPath, limit)
    
    local success, output, descriptor = hs.osascript.applescript(script)
    
    if success then
        return true
    else
        hs.alert.show("设置充电限制失败: " .. (output or "权限被拒绝"))
        return false
    end
end

-- 获取当前batt设置的充电限制
local function getBattLimit()
    if not isBattAvailable() then return nil end
    
    -- 使用osascript获取状态，因为需要sudo权限
    local script = string.format([[
        do shell script "sudo %s status" with administrator privileges
    ]], config.battPath)
    
    local success, output, descriptor = hs.osascript.applescript(script)
    if success and output then
        -- 解析输出中的上限设置
        local limit = output:match("Upper limit: (%d+)%%")
        if limit then
            return tonumber(limit)
        end
    end
    
    return nil
end

-- 设置充电限制
function batteryMonitor.setChargeLimit(limit)
    if limit and limit > 0 and limit <= 100 then
        config.chargeLimit = limit
        
        -- 如果batt可用，则使用batt设置系统充电限制
        if config.useBatt and isBattAvailable() then
            if setBattLimit(limit) then
                hs.alert.show(string.format("充电限制已设置为%d%%（已应用到系统）", limit))
            else
                hs.alert.show(string.format("充电限制已设置为%d%%（仅监控提醒）", limit))
            end
        else
            hs.alert.show(string.format("充电限制已设置为%d%%（仅监控提醒）", limit))
        end
    else
        hs.alert.show("无效的充电限制值")
    end
end

-- 切换临时充电到100%
function batteryMonitor.toggleTemporaryCharge()
    if _G.batteryMonitorState.isTemporaryCharge then
        -- 恢复到之前的充电限制
        local restoreLimit = _G.batteryMonitorState.previousChargeLimit or 80
        batteryMonitor.setChargeLimit(restoreLimit)
        _G.batteryMonitorState.isTemporaryCharge = false
        _G.batteryMonitorState.previousChargeLimit = nil
        hs.alert.show(string.format("已恢复充电限制到%d%%", restoreLimit), 2)
    else
        -- 保存当前充电限制并设置为100%
        _G.batteryMonitorState.previousChargeLimit = config.chargeLimit
        batteryMonitor.setChargeLimit(100)
        _G.batteryMonitorState.isTemporaryCharge = true
        hs.alert.show("已临时设置充电到100%", 2)
    end
end

-- 切换通知
function batteryMonitor.toggleNotifications()
    config.enableNotifications = not config.enableNotifications
    hs.alert.show(string.format("电池通知已%s", config.enableNotifications and "启用" or "禁用"))
end

-- 显示电池状态
function batteryMonitor.showStatus()
    local battery = getBatteryInfo()
    local status = string.format(
        "🔋 电池状态\n" ..
        "电量: %d%%\n" ..
        "状态: %s\n" ..
        "健康度: %s\n" ..
        "充电周期: %d",
        battery.percentage or 0,
        battery.isCharging and "充电中" or (battery.isCharged and "已充满" or "使用电池"),
        battery.health or "未知",
        battery.cycles or 0
    )
    
    if battery.timeRemaining and battery.timeRemaining > 0 then
        local timeText = battery.isCharging and "充满时间" or "剩余时间"
        status = status .. "\n" .. timeText .. ": " .. formatTime(battery.timeRemaining)
    end
    
    hs.alert.show(status, 3)
end

-- 绑定快捷键
function batteryMonitor.bindHotkeys()
    -- Cmd+Shift+B 显示电池状态
    hs.hotkey.bind({"cmd", "shift"}, "b", function()
        batteryMonitor.showStatus()
    end)
    
    -- Cmd+Option+B 切换临时充电到100%
    hs.hotkey.bind({"cmd", "option"}, "b", function()
        batteryMonitor.toggleTemporaryCharge()
    end)
    
    print("✅ 电池监控快捷键已绑定:")
    print("   Cmd+Shift+B - 显示电池状态")
    print("   Cmd+Option+B - 切换临时充电到100%（开关）")
end

return batteryMonitor