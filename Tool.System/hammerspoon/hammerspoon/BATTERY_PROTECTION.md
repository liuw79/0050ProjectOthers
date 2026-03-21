# 🔋 macOS电池保护完整解决方案

## 📋 概述

虽然Hammerspoon本身无法直接控制电池充电，但我们可以通过以下方案实现电池保护：

1. **Hammerspoon电池监控模块** - 监控电池状态，提供充电提醒
2. **外部充电控制工具** - 实际控制充电过程（推荐BatFi）

## 🔧 已配置的Hammerspoon功能

### 电池监控模块特性
- ✅ 实时监控电池电量和充电状态
- ✅ 达到80%充电限制时发送通知提醒
- ✅ 低电量（20%以下）警告
- ✅ 菜单栏显示电池状态
- ✅ 详细的电池健康信息
- ✅ 可自定义充电限制阈值

### 配置文件位置
- 模块文件：`modules/battery-monitor.lua`
- 配置文件：`config/settings.lua` 中的 `batteryMonitor` 部分

### 默认配置
```lua
config.batteryMonitor = {
    chargeLimit = 80,           -- 充电限制百分比
    lowBatteryThreshold = 20,   -- 低电量警告阈值
    enableNotifications = true,  -- 启用通知
    checkInterval = 60,         -- 检查间隔60秒
    showMenuBar = true          -- 显示菜单栏图标
}
```

## 🛠️ 推荐的充电控制工具

### 1. BatFi (强烈推荐)
**特点：**
- 🎯 精确控制充电限制（默认80%）
- 🔄 一键临时充满功能
- 📊 详细电池信息显示
- 🎨 美观的状态栏集成
- 💰 付费软件，质量有保障

**安装方式：**
```bash
# 方式1：从官网下载
open https://micropixels.software/apps/batfi

# 方式2：通过Homebrew安装
brew install --cask batfi
```

### 2. AlDente (备选)
**特点：**
- 🆓 有免费版本
- ⚙️ 功能丰富
- ⚠️ 部分用户反映精度问题

**安装方式：**
```bash
# 从App Store搜索"AlDente"
# 或访问：https://apphousekitchen.com/
```

### 3. batt (命令行工具)
**特点：**
- 🆓 完全免费开源
- 💻 命令行操作
- 🔧 需要一定技术基础

**安装方式：**
```bash
# 安装
brew install charlie0129/tap/batt

# 设置80%充电限制
sudo batt limit 80

# 查看状态
batt status
```

## 🚀 完整设置步骤

### 步骤1：重新加载Hammerspoon配置
1. 打开Hammerspoon
2. 点击菜单栏图标 → "Reload Config"
3. 确认电池监控模块已加载

### 步骤2：安装充电控制工具
推荐安装BatFi：
```bash
brew install --cask batfi
```

### 步骤3：配置BatFi
1. 启动BatFi
2. 设置充电限制为80%
3. 启用开机自启动
4. 根据需要调整通知设置

### 步骤4：验证设置
1. 连接充电器
2. 观察Hammerspoon菜单栏电池图标
3. 确认BatFi在80%时停止充电
4. 检查是否收到Hammerspoon的充电提醒

## ⚙️ 自定义配置

### 修改充电限制阈值
编辑 `config/settings.lua`：
```lua
config.batteryMonitor = {
    chargeLimit = 75,  -- 改为75%
    -- 其他配置...
}
```

### 禁用通知
```lua
config.batteryMonitor = {
    enableNotifications = false,
    -- 其他配置...
}
```

### 隐藏菜单栏图标
```lua
config.batteryMonitor = {
    showMenuBar = false,
    -- 其他配置...
}
```

## 🔍 故障排除

### 问题1：Hammerspoon电池模块未加载
**解决方案：**
1. 检查 `init.lua` 中是否包含 `batteryMonitor` 模块
2. 重新加载Hammerspoon配置
3. 查看控制台错误信息

### 问题2：BatFi无法控制充电
**解决方案：**
1. 确保BatFi有系统权限
2. 重启BatFi应用
3. 检查macOS系统完整性保护设置

### 问题3：通知过于频繁
**解决方案：**
1. 增加检查间隔：`checkInterval = 300` (5分钟)
2. 或禁用通知：`enableNotifications = false`

## 📚 相关资源

- [BatFi官网](https://micropixels.software/apps/batfi)
- [AlDente官网](https://apphousekitchen.com/)
- [batt开源项目](https://github.com/charlie0129/batt)
- [电池保护最佳实践](https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries)

## 💡 使用建议

1. **日常使用**：设置80%充电限制，保护电池健康
2. **出行前**：使用BatFi的"一键充满"功能临时充到100%
3. **定期检查**：通过Hammerspoon菜单查看电池健康状况
4. **长期存放**：电量保持在50%左右

---

**注意**：电池保护是一个长期过程，坚持使用80%充电限制可以显著延长电池寿命。