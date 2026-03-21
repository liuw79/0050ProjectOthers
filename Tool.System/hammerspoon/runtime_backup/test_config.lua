-- 测试配置加载脚本
print("🔍 开始测试 Hammerspoon 配置...")

-- 测试设置加载
local success, settings = pcall(require, "config.settings")
if success then
    print("✅ 设置文件加载成功")
else
    print("❌ 设置文件加载失败: " .. tostring(settings))
end

-- 测试个人信息模块
local success, personalInfo = pcall(require, "modules.personal-info")
if success then
    print("✅ 个人信息模块加载成功")
    if personalInfo.showChooser then
        print("✅ showChooser 函数存在")
    else
        print("❌ showChooser 函数不存在")
    end
else
    print("❌ 个人信息模块加载失败: " .. tostring(personalInfo))
end

-- 测试剪贴板模块
local success, clipboard = pcall(require, "modules.clipboard")
if success then
    print("✅ 剪贴板模块加载成功")
else
    print("❌ 剪贴板模块加载失败: " .. tostring(clipboard))
end

-- 测试快速记笔记模块
local success, quickNote = pcall(require, "modules.quick-note")
if success then
    print("✅ 快速记笔记模块加载成功")
else
    print("❌ 快速记笔记模块加载失败: " .. tostring(quickNote))
end

-- 测试窗口管理模块
local success, windowManager = pcall(require, "modules.window-management")
if success then
    print("✅ 窗口管理模块加载成功")
else
    print("❌ 窗口管理模块加载失败: " .. tostring(windowManager))
end

print("🎉 配置测试完成！")

-- 测试快捷键绑定
hs.hotkey.bind({"cmd", "alt"}, "T", function()
    hs.alert.show("测试快捷键工作正常！", 2)
end)

print("📋 测试快捷键已绑定: Cmd+Alt+T")
hs.alert.show("配置测试完成，按 Cmd+Alt+T 测试快捷键", 3)