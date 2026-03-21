-- 测试菜单栏功能
print("🔍 开始测试菜单栏功能...")

-- 创建一个简单的菜单栏项目
local testMenuBar = hs.menubar.new()

if testMenuBar then
    print("✅ 菜单栏对象创建成功")
    
    -- 设置标题
    testMenuBar:setTitle("🔋测试")
    
    -- 设置菜单
    testMenuBar:setMenu(function()
        return {
            { title = "测试菜单项", disabled = true },
            { title = "电池状态: " .. (hs.battery.percentage() or 0) .. "%", disabled = true },
            { title = "删除测试图标", fn = function()
                testMenuBar:delete()
                print("🗑️ 测试菜单栏已删除")
            end }
        }
    end)
    
    print("✅ 测试菜单栏已创建，应该能在顶部看到🔋测试图标")
    print("💡 点击图标可以看到菜单，选择'删除测试图标'可以移除")
else
    print("❌ 菜单栏对象创建失败")
end

-- 检查系统权限
print("🔍 检查系统权限...")
local hasAccessibility = hs.accessibilityState()
print("辅助功能权限: " .. (hasAccessibility and "✅ 已授权" or "❌ 未授权"))

-- 检查电池监控模块
print("🔍 检查电池监控模块...")
local batteryMonitor = require("modules.battery-monitor")
if batteryMonitor then
    print("✅ 电池监控模块加载成功")
    
    -- 尝试获取电池信息
    local battery = hs.battery.percentage()
    print("当前电池电量: " .. (battery or "未知") .. "%")
else
    print("❌ 电池监控模块加载失败")
end