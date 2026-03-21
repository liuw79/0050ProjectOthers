-- 媒体键控制模块
-- 简单可靠的媒体键实现

local M = {}

-- 初始化媒体键功能
function M.init()
    -- 启用 AppleScript 支持
    hs.allowAppleScript(true)
    
    -- 绑定媒体键
    M.bindMediaKeys()
    
    print("✅ 媒体键模块初始化成功")
end

-- 绑定媒体键
function M.bindMediaKeys()
    -- F7: 上一首
    hs.hotkey.bind({}, "f7", function()
        M.previousTrack()
    end)
    
    -- F8: 播放/暂停
    hs.hotkey.bind({}, "f8", function()
        M.playPause()
    end)
    
    -- F9: 下一首
    hs.hotkey.bind({}, "f9", function()
        M.nextTrack()
    end)
    
    -- 为兼容「将 F1、F2 等键用作标准功能键」未开启的情况，再额外绑定带 Fn 修饰键
    local fn = {"fn"}

    -- F7: 上一首 (Fn+F7 情况)
    hs.hotkey.bind(fn, "f7", function()
        M.previousTrack()
    end)

    -- F8: 播放/暂停 (Fn+F8 情况)
    hs.hotkey.bind(fn, "f8", function()
        M.playPause()
    end)

    -- F9: 下一首 (Fn+F9 情况)
    hs.hotkey.bind(fn, "f9", function()
        M.nextTrack()
    end)
    
    print("✅ 媒体键绑定完成 (F7=上一首, F8=播放/暂停, F9=下一首)")
end

-- 上一首
function M.previousTrack()
    local success, result = hs.applescript.applescript([[
        tell application "Music"
            if it is running then
                previous track
                return "success"
            else
                return "not_running"
            end if
        end tell
    ]])
    
    if success and result == "success" then
        hs.alert.show("⏮ 上一首", 0.5)
    elseif result == "not_running" then
        hs.alert.show("Music 应用未运行", 1)
    else
        hs.alert.show("操作失败", 0.5)
    end
end

-- 播放/暂停
function M.playPause()
    local success, result = hs.applescript.applescript([[
        tell application "Music"
            if it is running then
                playpause
                return "success"
            else
                return "not_running"
            end if
        end tell
    ]])
    
    if success and result == "success" then
        hs.alert.show("⏯ 播放/暂停", 0.5)
    elseif result == "not_running" then
        hs.alert.show("Music 应用未运行", 1)
    else
        hs.alert.show("操作失败", 0.5)
    end
end

-- 下一首
function M.nextTrack()
    local success, result = hs.applescript.applescript([[
        tell application "Music"
            if it is running then
                next track
                return "success"
            else
                return "not_running"
            end if
        end tell
    ]])
    
    if success and result == "success" then
        hs.alert.show("⏭ 下一首", 0.5)
    elseif result == "not_running" then
        hs.alert.show("Music 应用未运行", 1)
    else
        hs.alert.show("操作失败", 0.5)
    end
end

return M