# Hammerspoon 简化版使用指南

## 概述

由于 Hammerspoon 在 macOS 15.6.1 上访问蓝牙功能时会因权限问题导致崩溃，我们创建了这个简化版配置，移除了所有可能导致权限问题的功能，只保留核心的、稳定的功能。

## 崩溃原因

原始崩溃错误：
```
Termination Reason: Namespace TCC, Code 0
This app has crashed because it attempted to access privacy-sensitive data without a usage description. 
The app's Info.plist must contain an NSBluetoothAlwaysUsageDescription key with a string value explaining to the user how the app uses this data.
```

问题出现在 `system-utils.lua` 模块中的蓝牙切换功能，该功能尝试访问蓝牙但没有相应的权限描述。

## 简化版功能

### 保留的核心功能

1. **个人信息快速输入** - `Cmd + Alt + P`
   - 快速输入预设的个人信息
   - 包括姓名、邮箱、电话、地址等

2. **剪贴板管理** - `Cmd + Shift + V`
   - 剪贴板历史记录
   - 快速粘贴之前复制的内容

3. **快速记笔记** - `Cmd + Shift + N`
   - 快速创建和保存笔记
   - 支持时间戳

4. **窗口管理**
   - 窗口排列和调整
   - 多显示器支持

5. **电池状态显示** - `Cmd + Alt + B`
   - 显示电池电量、充电状态和电源信息
   - 简化版，无复杂监控功能

6. **系统功能** - `Cmd + Alt + S`
   - 系统信息显示（电池、音量、亮度）
   - 锁定屏幕
   - 系统睡眠
   - 音量调节（+10/-10）
   - 亮度调节（+10/-10）

### 移除的功能

为了避免权限问题，以下功能已被移除：

- ❌ 蓝牙切换功能
- ❌ WiFi 切换功能（可能涉及网络权限）
- ❌ 复杂的电池监控和保护功能
- ❌ 系统重启/关机功能
- ❌ 勿扰模式切换
- ❌ 清空废纸篓功能
- ❌ 番茄钟功能
- ❌ 媒体处理器功能
- ❌ 帮助系统

## 快捷键列表

| 快捷键 | 功能 |
|--------|------|
| `Cmd + Alt + P` | 个人信息快速输入 |
| `Cmd + Alt + B` | 显示电池状态 |
| `Cmd + Alt + S` | 系统功能选择器 |
| `Cmd + Shift + V` | 剪贴板历史 |
| `Cmd + Shift + N` | 快速记笔记 |
| `Cmd + Alt + Ctrl + R` | 重新加载配置 |

## 系统功能详情

通过 `Cmd + Alt + S` 可以访问以下系统功能：

1. **系统信息** - 显示电池、音量、亮度百分比
2. **锁定屏幕** - 立即锁定屏幕
3. **睡眠** - 让系统进入睡眠状态
4. **音量 +10** - 增加音量 10%
5. **音量 -10** - 减少音量 10%
6. **亮度 +10** - 增加亮度 10%
7. **亮度 -10** - 减少亮度 10%

## 配置文件结构

```
hammerspoon/
├── init.lua                    # 简化版主配置文件
├── settings.lua               # 基本设置
├── modules/
│   ├── personal-info.lua      # 个人信息模块
│   ├── clipboard.lua          # 剪贴板模块
│   ├── quick-note.lua         # 快速记笔记模块
│   ├── window-management.lua  # 窗口管理模块
│   └── system-utils-safe.lua  # 安全的系统工具模块
└── SIMPLE_VERSION_GUIDE.md   # 本文档
```

## 故障排除

### 如果 Hammerspoon 仍然崩溃

1. 检查 Hammerspoon 控制台是否有错误信息
2. 确保所有模块文件都存在
3. 尝试重新启动 Hammerspoon
4. 检查 macOS 系统权限设置

### 如果快捷键不工作

1. 确保 Hammerspoon 有辅助功能权限
2. 检查快捷键是否与其他应用冲突
3. 重新加载配置：`Cmd + Alt + Ctrl + R`

### 恢复完整功能

如果需要恢复完整功能，可以：

1. 备份当前简化版配置
2. 恢复 `init_backup.lua` 为 `init.lua`
3. 但需要解决蓝牙权限问题

## 注意事项

- 这个简化版本优先考虑稳定性而非功能完整性
- 所有保留的功能都经过测试，不会导致权限问题
- 如果需要蓝牙控制功能，建议使用系统自带的控制中心
- 定期检查 Hammerspoon 更新，新版本可能解决权限问题

## 更新日志

- **v1.0** (2024-01-23): 创建简化版配置，移除蓝牙等权限敏感功能
- 解决了 macOS 15.6.1 上的崩溃问题
- 保留了核心的个人信息、剪贴板、笔记和窗口管理功能