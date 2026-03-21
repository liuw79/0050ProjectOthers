-- Hammerspoon 诊断配置
print("🔍 开始诊断模式...")

-- 检查基本功能
print("📱 Hammerspoon版本: " .. hs.processInfo.version)
print("🔋 电池电量: " .. (hs.battery.percentage() or "未知") .. "%")
print("⚡ 充电状态: " .. (hs.battery.isCharging() and "充电中" or "未充电"))

-- 测试菜单栏创建
print("🔍 测试菜单栏创建...")
local testMenuBar = hs.menubar.new()

if testMenuBar then
    print("✅ 菜单栏对象创建成功")
    
    -- 设置简单的标题和菜单
    testMenuBar:setTitle("🔋" .. (hs.battery.percentage() or 0) .. "%")
    testMenuBar:setMenu({
        { title = "诊断模式", disabled = true },
        { title = "电池: " .. (hs.battery.percentage() or 0) .. "%", disabled = true },
        { title = "充电: " .. (hs.battery.isCharging() and "是" or "否"), disabled = true },
        { title = "---", disabled = true },
        { title = "重新加载配置", fn = function() hs.reload() end },
        { title = "退出诊断", fn = function() 
            testMenuBar:delete()
            print("🗑️ 诊断菜单已删除")
        end }
    })
    
    print("✅ 诊断菜单栏已创建，应该能在顶部看到电池图标")
    
    -- 设置定时器更新电池状态
    local updateTimer = hs.timer.doEvery(30, function()
        local battery = hs.battery.percentage() or 0
        local charging = hs.battery.isCharging()
        local title = (charging and "⚡" or "🔋") .. battery .. "%"
        testMenuBar:setTitle(title)
        print("🔄 更新菜单栏: " .. title)
    end)
    
    print("⏰ 定时器已启动，每30秒更新一次")
else
    print("❌ 菜单栏对象创建失败！")
end

-- 检查权限
print("🔍 检查系统权限...")
local hasAccessibility = hs.accessibilityState()
print("辅助功能权限: " .. (hasAccessibility and "✅ 已授权" or "❌ 未授权"))

-- 安装IPC
print("🔍 安装IPC...")
hs.ipc.cliInstall()
print("✅ IPC安装完成")

-- 设置重载快捷键
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "r", function()
    print("🔄 重新加载配置...")
    hs.reload()
end)

print("🎉 诊断模式加载完成！")
print("💡 快捷键 Cmd+Alt+Ctrl+R 重新加载配置")
print("💡 如果看到菜单栏图标，说明基本功能正常")