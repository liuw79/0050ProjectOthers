-- 手势功能测试脚本
-- 用于验证四指下滑手势是否正常工作

print("🧪 开始测试手势功能...")

-- 检查Swipe.spoon是否可用
local Swipe = hs.loadSpoon("Swipe")
if Swipe then
    print("✅ Swipe.spoon 加载成功")
    
    -- 测试手势监听
    local testGesture = function()
        print("🖐️ 测试手势监听器...")
        
        -- 创建一个临时的手势监听器
        local testWatcher = hs.eventtap.new({hs.eventtap.event.types.gesture}, function(event)
            local touches = event:getTouches()
            if touches and #touches == 4 then
                print("🎯 检测到四指触摸事件")
                return false -- 不拦截事件
            end
        end)
        
        testWatcher:start()
        print("👆 请在触控板上使用四指下滑手势...")
        print("⏰ 测试将在10秒后自动停止")
        
        -- 10秒后停止测试
        hs.timer.doAfter(10, function()
            testWatcher:stop()
            print("⏹️ 手势测试结束")
        end)
    end
    
    testGesture()
else
    print("❌ Swipe.spoon 加载失败")
end

print("📋 手势功能状态检查完成")