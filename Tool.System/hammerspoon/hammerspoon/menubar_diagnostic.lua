-- Hammerspoon菜单栏诊断脚本
print("🔍 开始Hammerspoon菜单栏诊断...")

-- 检查Hammerspoon版本
print("📋 Hammerspoon版本: " .. hs.processInfo.version)

-- 检查菜单栏模块是否可用
if hs.menubar then
    print("✅ hs.menubar 模块可用")
else
    print("❌ hs.menubar 模块不可用")
    return
end

-- 检查通知模块
if hs.notify then
    print("✅ hs.notify 模块可用")
else
    print("❌ hs.notify 模块不可用")
end

-- 检查电池模块
if hs.battery then
    print("✅ hs.battery 模块可用")
    print("🔋 当前电池电量: " .. (hs.battery.percentage() or "未知") .. "%")
else
    print("❌ hs.battery 模块不可用")
end

-- 尝试创建菜单栏
print("\n🔧 尝试创建菜单栏...")
local menubar = hs.menubar.new()

if menubar then
    print("✅ 菜单栏对象创建成功")
    
    -- 检查菜单栏方法
    local methods = {"setTitle", "setMenu", "setIcon", "delete", "isInMenuBar"}
    for _, method in ipairs(methods) do
        if menubar[method] then
            print("✅ 方法 " .. method .. " 可用")
        else
            print("❌ 方法 " .. method .. " 不可用")
        end
    end
    
    -- 尝试设置标题
    print("\n🏷️ 尝试设置菜单栏标题...")
    local success, error = pcall(function()
        menubar:setTitle("DIAG")
    end)
    
    if success then
        print("✅ 菜单栏标题设置成功")
        
        -- 检查是否在菜单栏中
        if menubar.isInMenuBar and menubar:isInMenuBar() then
            print("✅ 菜单栏项目已显示在菜单栏中")
        else
            print("❌ 菜单栏项目未显示在菜单栏中")
        end
        
        -- 等待3秒后删除
        hs.timer.doAfter(3, function()
            menubar:delete()
            print("🗑️ 诊断菜单栏已删除")
        end)
        
    else
        print("❌ 菜单栏标题设置失败: " .. tostring(error))
    end
    
else
    print("❌ 菜单栏对象创建失败")
end

-- 检查系统权限
print("\n🔐 检查系统权限...")
local hasAccessibility = hs.accessibilityState()
print("🔓 辅助功能权限: " .. (hasAccessibility and "已授权" or "未授权"))

-- 发送诊断完成通知
if hs.notify then
    hs.notify.new({
        title = "Hammerspoon诊断",
        informativeText = "菜单栏诊断完成，请查看控制台日志",
        autoWithdraw = false
    }):send()
end

print("\n✅ 诊断完成！请检查上述输出以确定问题所在。")