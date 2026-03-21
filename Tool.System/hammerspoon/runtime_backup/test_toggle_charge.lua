-- 测试切换临时充电功能
print("=== 测试切换临时充电功能 ===")

-- 加载电池监控模块
local batteryMonitor = require('modules.battery-monitor')

-- 检查模块是否正确加载
if batteryMonitor then
    print("✅ 电池监控模块加载成功")
    
    -- 检查切换函数是否存在
    if batteryMonitor.toggleTemporaryCharge then
        print("✅ toggleTemporaryCharge 函数存在")
        
        -- 测试切换功能
        print("\n--- 第一次调用切换函数 ---")
        batteryMonitor.toggleTemporaryCharge()
        
        hs.timer.doAfter(2, function()
            print("\n--- 第二次调用切换函数 ---")
            batteryMonitor.toggleTemporaryCharge()
        end)
        
    else
        print("❌ toggleTemporaryCharge 函数不存在")
    end
    
    -- 检查其他相关函数
    if batteryMonitor.setChargeLimit then
        print("✅ setChargeLimit 函数存在")
    else
        print("❌ setChargeLimit 函数不存在")
    end
    
else
    print("❌ 电池监控模块加载失败")
end

print("\n=== 测试完成 ===")