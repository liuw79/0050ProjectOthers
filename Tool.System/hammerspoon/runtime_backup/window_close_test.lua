-- 窗口关闭功能测试脚本
print("🔍 开始窗口关闭功能诊断...")

-- 获取当前活动窗口信息
local function getCurrentWindowInfo()
    local win = hs.window.focusedWindow()
    if win then
        local app = win:application()
        print(string.format("✅ 当前活动窗口: %s (%s)", win:title() or "无标题", app:name() or "未知应用"))
        print(string.format("   窗口ID: %s", win:id()))
        print(string.format("   应用PID: %s", app:pid()))
        print(string.format("   窗口可关闭: %s", win:isStandard() and "是" or "否"))
        return win, app
    else
        print("❌ 没有找到活动窗口")
        return nil, nil
    end
end

-- 测试不同的关闭方法
local function testCloseMethods()
    local win, app = getCurrentWindowInfo()
    if not win then return end
    
    print("\n🧪 测试不同的窗口关闭方法:")
    
    -- 方法1: 使用快捷键 Cmd+W
    print("1. 测试 Cmd+W 快捷键...")
    hs.timer.doAfter(1, function()
        hs.eventtap.keyStroke({"cmd"}, "w")
        print("   已发送 Cmd+W")
    end)
    
    -- 方法2: 直接关闭窗口对象
    hs.timer.doAfter(3, function()
        local currentWin = hs.window.focusedWindow()
        if currentWin and currentWin:id() == win:id() then
            print("2. 测试直接关闭窗口对象...")
            local success = currentWin:close()
            print(string.format("   直接关闭结果: %s", success and "成功" or "失败"))
        end
    end)
    
    -- 方法3: 使用应用菜单
    hs.timer.doAfter(5, function()
        local currentWin = hs.window.focusedWindow()
        if currentWin then
            print("3. 测试应用菜单关闭...")
            local app = currentWin:application()
            if app then
                local success = app:selectMenuItem({"File", "Close"}) or 
                               app:selectMenuItem({"文件", "关闭"}) or
                               app:selectMenuItem({"Window", "Close"}) or
                               app:selectMenuItem({"窗口", "关闭"})
                print(string.format("   菜单关闭结果: %s", success and "成功" or "失败"))
            end
        end
    end)
    
    -- 方法4: 使用系统事件
    hs.timer.doAfter(7, function()
        local currentWin = hs.window.focusedWindow()
        if currentWin then
            print("4. 测试系统事件关闭...")
            hs.timer.doAfter(0.1, function()
                hs.eventtap.keyStroke({"cmd"}, "w", 0)
            end)
        end
    end)
end

-- 开始测试
getCurrentWindowInfo()
testCloseMethods()

print("\n📝 测试将在7秒内完成，请观察窗口是否关闭...")