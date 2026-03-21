-- 测试 Hammerspoon 快捷键功能
-- 这个脚本用于验证 Hammerspoon 是否能正确响应快捷键

print("🔍 开始测试 Hammerspoon 快捷键功能...")

-- 测试简单的快捷键
hs.hotkey.bind({"cmd", "shift"}, "T", function()
    hs.alert.show("✅ Hammerspoon 快捷键测试成功！", 2)
    print("✅ 测试快捷键 Cmd+Shift+T 被触发")
end)

-- 测试电池控制快捷键
hs.hotkey.bind({"cmd", "shift"}, "B", function()
    print("🔋 电池控制快捷键被触发")
    hs.alert.show("🔋 电池控制快捷键已触发", 2)
    
    -- 执行电池控制脚本
    local scriptPath = hs.configdir .. "/battery_control_wrapper.sh"
    print("📍 脚本路径: " .. scriptPath)
    
    -- 检查脚本是否存在
    local file = io.open(scriptPath, "r")
    if file then
        file:close()
        print("✅ 脚本文件存在")
        
        local task = hs.task.new(scriptPath, function(exitCode, stdOut, stdErr)
            print("📊 脚本执行结果:")
            print("   退出码: " .. tostring(exitCode))
            print("   输出: " .. (stdOut or "无"))
            print("   错误: " .. (stdErr or "无"))
            
            if exitCode == 0 then
                local message = stdOut:gsub("\n", "")
                hs.alert.show(message, 3)
            else
                hs.alert.show("❌ 电池控制失败: " .. (stdErr or "未知错误"), 3)
            end
        end, {"toggle"}):start()
    else
        print("❌ 脚本文件不存在: " .. scriptPath)
        hs.alert.show("❌ 电池控制脚本不存在", 2)
    end
end)

print("✅ 测试快捷键已设置:")
print("   Cmd+Shift+T: 测试快捷键")
print("   Cmd+Shift+B: 电池控制")
print("📝 请尝试按下这些快捷键来测试功能")