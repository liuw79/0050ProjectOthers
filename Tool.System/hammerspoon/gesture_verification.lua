-- 手势功能验证脚本
print("🔍 验证手势功能修复...")

-- 检查当前窗口
local win = hs.window.focusedWindow()
if win then
    local app = win:application()
    print(string.format("✅ 当前窗口: %s (%s)", win:title() or "无标题", app:name() or "未知应用"))
    
    -- 测试直接关闭方法
    print("🧪 测试窗口关闭方法...")
    
    -- 先尝试直接关闭
    local success = win:close()
    if success then
        print("✅ 直接关闭窗口成功")
    else
        print("⚠️ 直接关闭失败，这可能是某些应用的正常行为")
        
        -- 测试快捷键方法
        print("🔑 测试快捷键方法...")
        hs.eventtap.keyStroke({"cmd"}, "w", 0)
        
        -- 检查是否成功
        hs.timer.doAfter(0.5, function()
            local currentWin = hs.window.focusedWindow()
            if not currentWin or currentWin:id() ~= win:id() then
                print("✅ 快捷键关闭成功")
            else
                print("⚠️ 快捷键关闭可能失败，窗口仍然存在")
            end
        end)
    end
else
    print("❌ 没有找到活动窗口")
end

print("\n📝 现在可以尝试四指下滑手势，应该能看到详细的调试信息并成功关闭窗口")