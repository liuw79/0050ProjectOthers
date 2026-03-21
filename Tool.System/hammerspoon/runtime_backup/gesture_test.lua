-- 手势测试脚本
print("🔍 开始手势功能诊断...")

-- 检查Swipe.spoon是否存在
local swipeSpoonPath = hs.spoons.resourcePath("Swipe")
if swipeSpoonPath then
    print("✅ Swipe.spoon 路径存在: " .. swipeSpoonPath)
else
    print("❌ Swipe.spoon 路径不存在")
    return
end

-- 尝试加载Swipe.spoon
local Swipe = hs.loadSpoon("Swipe")
if Swipe then
    print("✅ Swipe.spoon 加载成功")
else
    print("❌ Swipe.spoon 加载失败")
    return
end

-- 检查手势事件监听
local gestureWatcher = hs.eventtap.new({hs.eventtap.event.types.gesture}, function(event)
    local touches = event:getTouches()
    if touches and #touches > 0 then
        print(string.format("🖐️ 检测到 %d 指触摸", #touches))
        for i, touch in ipairs(touches) do
            print(string.format("   手指 %d: 阶段=%s, 位置=(%.2f, %.2f)", 
                i, touch.phase, touch.normalizedPosition.x, touch.normalizedPosition.y))
        end
        return false -- 不拦截事件
    end
end)

if gestureWatcher then
    gestureWatcher:start()
    print("✅ 手势监听器已启动")
    print("📝 请在触控板上进行四指手势，观察输出...")
    
    -- 10秒后停止监听
    hs.timer.doAfter(10, function()
        gestureWatcher:stop()
        print("⏹️ 手势监听器已停止")
    end)
else
    print("❌ 无法创建手势监听器")
end