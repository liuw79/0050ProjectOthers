-- 番茄时钟模块
-- 基于Cherry.spoon实现，提供简化的番茄工作法计时功能

local M = {}
local config = require("config.settings").pomodoro
local cherry = nil

-- 初始化番茄时钟
function M.init()
    -- 加载Cherry.spoon
    cherry = hs.loadSpoon("Cherry")
    
    if not cherry then
        print("❌ Cherry.spoon加载失败，请检查Spoons目录")
        return false
    end
    
    -- 配置Cherry参数
    cherry.duration = config.duration
    cherry.alwaysShow = config.alwaysShow
    cherry.alertDuration = config.alertDuration
    cherry.alertTextSize = config.alertTextSize
    
    -- 配置通知
    if config.enableNotification then
        cherry.notification = hs.notify.new({
            title = "番茄时钟完成! 🍒",
            informativeText = "休息一下吧～",
            withdrawAfter = 0
        })
    else
        cherry.notification = nil
    end
    
    -- 配置声音
    if config.enableSound then
        cherry.sound = hs.sound.getByName("Glass")
    else
        cherry.sound = nil
    end
    
    -- 绑定快捷键
    local success, error = pcall(function()
        hs.hotkey.bind(config.keybind[1], config.keybind[2], function()
            M.toggle()
        end)
    end)
    
    if success then
        print("✅ 番茄时钟模块初始化成功 - 快捷键: " .. table.concat(config.keybind, "+"))
        return true
    else
        print("❌ 番茄时钟快捷键绑定失败: " .. tostring(error))
        return false
    end
end

-- 切换番茄时钟状态
function M.toggle()
    if not cherry then
        hs.alert.show("番茄时钟未初始化")
        return
    end
    
    if cherry.timerRunning then
        -- 如果正在运行，则暂停
        cherry:pause()
        hs.alert.show("番茄时钟已暂停 ⏸️", 1)
    else
        -- 如果未运行或已暂停，则开始/恢复
        if cherry.timeLeft and cherry.timeLeft > 0 and cherry.timeLeft < cherry.duration * 60 then
            -- 恢复暂停的计时
            cherry:start(true)
            hs.alert.show("番茄时钟已恢复 ▶️", 1)
        else
            -- 开始新的番茄时钟
            cherry:start()
            hs.alert.show("番茄时钟已开始 🍒", 1)
        end
    end
end

-- 停止番茄时钟
function M.stop()
    if cherry then
        cherry:reset()
        hs.alert.show("番茄时钟已停止 ⏹️", 1)
    end
end

-- 获取当前状态
function M.getStatus()
    if not cherry then
        return "未初始化"
    end
    
    if cherry.timerRunning then
        return "运行中"
    elseif cherry.timeLeft and cherry.timeLeft > 0 then
        return "已暂停"
    else
        return "已停止"
    end
end

-- 获取剩余时间
function M.getTimeLeft()
    if cherry and cherry.timeLeft then
        local minutes = math.floor(cherry.timeLeft / 60)
        local seconds = cherry.timeLeft % 60
        return string.format("%02d:%02d", minutes, seconds)
    end
    return "00:00"
end

return M