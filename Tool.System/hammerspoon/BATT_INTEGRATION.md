# batt与Hammerspoon集成使用说明

## 概述

本文档介绍如何使用Hammerspoon与batt命令行工具的集成，实现Mac电池充电限制的智能控制。

## 功能特性

- ✅ **智能充电限制**：通过菜单栏直接设置和控制电池充电上限
- ✅ **实时状态显示**：显示当前电池状态和batt设置的充电限制
- ✅ **无缝集成**：通过AppleScript自动处理sudo权限请求
- ✅ **多种限制选项**：支持60%、70%、75%、80%、85%、90%、95%、100%等预设值
- ✅ **电池保护**：延长电池寿命，减少电池老化

## 安装要求

### 1. batt工具安装

batt工具已成功安装在 `/usr/local/bin/batt`，支持以下功能：
- 设置电池充电上限和下限
- 实时监控电池状态
- 防止过度充电保护电池健康

### 2. Hammerspoon配置

battery-monitor模块已集成batt支持，配置如下：

```lua
-- 默认配置
local defaultConfig = {
    chargeLimit = 80,           -- 充电限制百分比
    lowBatteryThreshold = 20,   -- 低电量警告阈值
    enableNotifications = true,  -- 是否启用通知
    checkInterval = 60,         -- 检查间隔（秒）
    showMenuBar = true,         -- 是否显示菜单栏图标
    useBatt = true,             -- 是否使用batt命令行工具
    battPath = "/usr/local/bin/batt" -- batt命令行工具路径
}
```

## 使用方法

### 1. 通过菜单栏控制

1. 在macOS菜单栏中找到电池监控图标
2. 点击图标打开菜单
3. 在"batt充电限制控制"子菜单中选择所需的充电限制
4. 系统会自动请求管理员权限并应用设置

### 2. 支持的充电限制选项

- **60%** - 极度保护模式，适合长期插电使用
- **70%** - 高度保护模式
- **75%** - 平衡保护模式
- **80%** - 推荐日常使用（默认）
- **85%** - 轻度保护模式
- **90%** - 最小保护模式
- **95%** - 接近满电
- **100%** - 完全充电（禁用限制）

### 3. 状态显示

菜单栏会显示：
- 当前电池电量百分比
- 充电状态（充电中/放电中/已充满）
- 系统充电限制设置
- 电池健康度和充电周期
- 当前功率消耗

## 工作原理

### 1. 权限处理

由于batt命令需要sudo权限来控制硬件，集成使用AppleScript的`with administrator privileges`来处理权限请求：

```lua
local script = string.format([[
    do shell script "sudo %s limit %d" with administrator privileges
]], config.battPath, limit)

local success, output, descriptor = hs.osascript.applescript(script)
```

### 2. 状态监控

系统会定期检查：
- batt工具的可用性
- 当前充电限制设置
- 电池状态变化
- 充电限制达到时的通知

### 3. 自动化流程

1. 用户通过菜单选择充电限制
2. Hammerspoon调用AppleScript
3. AppleScript请求管理员权限
4. 执行batt命令设置充电限制
5. 系统应用新的充电策略
6. 菜单栏更新显示状态

## 故障排除

### 1. batt工具不可用

如果提示"未找到batt命令行工具"：
```bash
# 检查batt是否安装
which batt

# 检查权限
ls -la /usr/local/bin/batt

# 重新安装（如需要）
sudo batt install
```

### 2. 权限被拒绝

如果设置充电限制时权限被拒绝：
- 确保在弹出的权限对话框中输入正确的管理员密码
- 检查用户是否有管理员权限
- 尝试在终端中手动运行：`sudo batt status`

### 3. 设置不生效

如果充电限制设置后不生效：
- 等待2分钟让系统刷新充电状态
- 检查batt守护进程是否运行：`sudo batt status`
- 重启batt服务：`sudo batt install`

## 高级配置

### 1. 自定义充电限制

可以通过修改配置文件添加自定义充电限制选项：

```lua
-- 在battery-monitor.lua中添加自定义选项
{ title = "自定义值%", fn = function() 
    -- 实现自定义输入对话框
end }
```

### 2. 禁用macOS优化充电

为了获得最佳效果，建议禁用macOS内置的优化充电功能：
1. 打开"系统设置" > "电池"
2. 点击"电池健康度"旁的"i"图标
3. 关闭"优化电池充电"

### 3. 定时任务

可以设置定时任务在特定时间自动调整充电限制：

```lua
-- 工作时间设置为80%，睡眠时间设置为60%
hs.timer.doAt("09:00", "1d", function()
    batteryMonitor.setChargeLimit(80)
end)

hs.timer.doAt("22:00", "1d", function()
    batteryMonitor.setChargeLimit(60)
end)
```

## 电池保护建议

1. **日常使用**：建议设置80%充电限制
2. **长期插电**：建议设置60-70%充电限制
3. **出行前**：临时设置100%获得最大续航
4. **定期校准**：每月至少一次完整充放电循环

## 技术支持

- **batt项目**：https://github.com/charlie0129/batt
- **Hammerspoon文档**：https://www.hammerspoon.org/docs/
- **问题反馈**：请在相应的GitHub项目中提交issue

---

*最后更新：2025年9月23日*