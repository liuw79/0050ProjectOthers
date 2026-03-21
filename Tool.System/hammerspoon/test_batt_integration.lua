#!/usr/bin/env lua

-- 测试batt与Hammerspoon集成的脚本
-- 这个脚本模拟Hammerspoon环境来测试batt功能

print("🔋 测试batt与Hammerspoon集成")
print("=" .. string.rep("=", 40))

-- 模拟hs.execute函数
local function execute(cmd)
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    local success = handle:close()
    return result, success
end

-- 模拟hs.osascript.applescript函数
local function applescript(script)
    -- 将AppleScript保存到临时文件
    local tmpfile = "/tmp/test_applescript.scpt"
    local file = io.open(tmpfile, "w")
    file:write(script)
    file:close()
    
    -- 执行AppleScript
    local cmd = string.format("osascript %s", tmpfile)
    local output, success = execute(cmd)
    
    -- 清理临时文件
    os.remove(tmpfile)
    
    return success, output:gsub("\n$", ""), nil
end

-- 配置
local config = {
    useBatt = true,
    battPath = "/usr/local/bin/batt"
}

-- 检查batt命令是否可用
local function isBattAvailable()
    if not config.useBatt then return false end
    
    local output, status = execute(string.format("[ -x \"%s\" ] && echo 1 || echo 0", config.battPath))
    return output:match("1") ~= nil
end

-- 获取当前batt设置的充电限制
local function getBattLimit()
    if not isBattAvailable() then return nil end
    
    -- 使用osascript获取状态，因为需要sudo权限
    local script = string.format([[
        do shell script "sudo %s status" with administrator privileges
    ]], config.battPath)
    
    local success, output, descriptor = applescript(script)
    if success and output then
        -- 解析输出中的上限设置
        local limit = output:match("Upper limit: (%d+)%%")
        if limit then
            return tonumber(limit)
        end
    end
    
    return nil
end

-- 使用batt设置充电限制
local function setBattLimit(limit)
    if not isBattAvailable() then
        print("❌ 未找到batt命令行工具")
        return false
    end
    
    -- batt命令需要sudo权限，使用osascript来请求管理员权限
    local script = string.format([[
        do shell script "sudo %s limit %d" with administrator privileges
    ]], config.battPath, limit)
    
    local success, output, descriptor = applescript(script)
    
    if success then
        return true
    else
        print("❌ 设置充电限制失败: " .. (output or "权限被拒绝"))
        return false
    end
end

-- 开始测试
print("1. 检查batt工具是否可用...")
if isBattAvailable() then
    print("✅ batt工具可用")
else
    print("❌ batt工具不可用")
    os.exit(1)
end

print("\n2. 获取当前充电限制...")
local currentLimit = getBattLimit()
if currentLimit then
    print(string.format("✅ 当前充电限制: %d%%", currentLimit))
else
    print("❌ 无法获取当前充电限制")
end

print("\n3. 测试设置充电限制为75%...")
if setBattLimit(75) then
    print("✅ 充电限制设置成功")
    
    -- 验证设置是否生效
    print("\n4. 验证设置是否生效...")
    local newLimit = getBattLimit()
    if newLimit == 75 then
        print("✅ 验证成功，充电限制已设置为75%")
    else
        print(string.format("⚠️ 验证失败，当前限制为: %s", newLimit or "未知"))
    end
else
    print("❌ 充电限制设置失败")
end

print("\n5. 恢复原始设置...")
if currentLimit and setBattLimit(currentLimit) then
    print(string.format("✅ 已恢复原始充电限制: %d%%", currentLimit))
else
    print("⚠️ 无法恢复原始设置")
end

print("\n🎉 测试完成！")