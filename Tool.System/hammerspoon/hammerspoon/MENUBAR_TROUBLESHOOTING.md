# Hammerspoon菜单栏图标问题综合解决方案

## 问题诊断结果

经过详细测试，发现在macOS 15.6.1系统上使用Hammerspoon 1.0.0时，菜单栏图标无法正常显示。

### 系统环境
- **macOS版本**: 15.6.1 (24G90)
- **Hammerspoon版本**: 1.0.0
- **辅助功能权限**: 已授权 ✅
- **Hammerspoon进程**: 正常运行 ✅

### 问题分析

1. **版本兼容性问题**: Hammerspoon 1.0.0可能与macOS 15.6.1存在兼容性问题
2. **系统安全限制**: macOS 15.6.1引入了新的安全限制，可能影响菜单栏访问
3. **菜单栏空间限制**: 系统菜单栏空间可能被其他应用占用

## 解决方案

### 方案1: 升级Hammerspoon（推荐）

```bash
# 下载最新版本的Hammerspoon
# 访问 https://github.com/Hammerspoon/hammerspoon/releases
# 下载最新的稳定版本（建议0.9.100或更高版本）

# 或使用Homebrew安装
brew install --cask hammerspoon
```

### 方案2: 使用替代方案

如果升级后仍有问题，可以考虑以下替代方案：

#### A. 使用BitBar/SwiftBar
```bash
# 安装SwiftBar（BitBar的现代替代品）
brew install --cask swiftbar

# 创建电池监控脚本
mkdir -p ~/SwiftBar
```

#### B. 使用系统原生通知
创建一个基于通知的电池监控系统：

```lua
-- 仅使用通知的电池监控
local function checkBattery()
    local percentage = hs.battery.percentage()
    local isCharging = hs.battery.isCharging()
    
    if percentage <= 20 and not isCharging then
        hs.notify.new({
            title = "电池电量低",
            informativeText = "当前电量: " .. percentage .. "%",
            autoWithdraw = false
        }):send()
    end
    
    if percentage >= 80 and isCharging then
        hs.notify.new({
            title = "电池充电完成",
            informativeText = "当前电量: " .. percentage .. "%",
            autoWithdraw = false
        }):send()
    end
end

-- 每5分钟检查一次
hs.timer.doEvery(300, checkBattery)
```

### 方案3: 手动权限配置

1. **打开系统设置**
2. **隐私与安全性** → **辅助功能**
3. **确保Hammerspoon已被授权**
4. **重启Hammerspoon**

### 方案4: 重新安装Hammerspoon

```bash
# 完全卸载Hammerspoon
rm -rf ~/.hammerspoon
rm -rf /Applications/Hammerspoon.app

# 重新下载安装最新版本
# 从官网下载: https://www.hammerspoon.org/
```

## 临时解决方案

在问题解决之前，可以使用以下配置：

```lua
-- 临时配置：使用通知代替菜单栏
local batteryMonitor = {}

function batteryMonitor.init()
    -- 显示启动通知
    hs.notify.new({
        title = "电池监控已启动",
        informativeText = "将通过通知显示电池状态",
        autoWithdraw = true
    }):send()
    
    -- 定时检查电池状态
    hs.timer.doEvery(1800, function() -- 每30分钟
        local percentage = hs.battery.percentage()
        local isCharging = hs.battery.isCharging()
        
        hs.notify.new({
            title = "电池状态",
            informativeText = string.format("电量: %d%% %s", 
                percentage, 
                isCharging and "(充电中)" or "(未充电)"),
            autoWithdraw = true
        }):send()
    end)
end

-- 启动监控
batteryMonitor.init()

-- 快捷键查看电池状态
hs.hotkey.bind({"cmd", "alt"}, "B", function()
    local percentage = hs.battery.percentage()
    local isCharging = hs.battery.isCharging()
    
    hs.alert.show(string.format("电池: %d%% %s", 
        percentage, 
        isCharging and "⚡充电中" or "🔋未充电"))
end)
```

## 验证步骤

1. **重新加载配置**: `Cmd+Alt+Ctrl+R`
2. **检查通知**: 应该看到"电池监控已启动"通知
3. **测试快捷键**: 按`Cmd+Alt+B`查看电池状态
4. **等待定时通知**: 30分钟后会自动显示电池状态

## 进一步调试

如果问题持续存在：

1. **查看系统日志**:
   ```bash
   log show --predicate 'process == "Hammerspoon"' --last 1h
   ```

2. **检查权限**:
   ```bash
   tccutil reset Accessibility com.hammerspoon.Hammerspoon
   ```

3. **重置Hammerspoon配置**:
   ```bash
   mv ~/.hammerspoon ~/.hammerspoon.backup
   mkdir ~/.hammerspoon
   ```

## 联系支持

如果以上方案都无法解决问题：

1. **Hammerspoon GitHub Issues**: https://github.com/Hammerspoon/hammerspoon/issues
2. **Hammerspoon论坛**: https://github.com/Hammerspoon/hammerspoon/discussions
3. **提供系统信息**: macOS版本、Hammerspoon版本、错误日志

---

**最后更新**: 2025年9月23日  
**适用版本**: macOS 15.6.1, Hammerspoon 1.0.0