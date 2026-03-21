# 🔋 无菜单栏图标的电池管理使用指南

当 Hammerspoon 菜单栏图标无法显示时，你仍然可以通过以下方式完全控制电池管理功能。

## 🎯 解决方案概览

我们提供了三种替代方案来控制电池功能：

1. **快捷键控制** - 最便捷的方式
2. **命令行控制** - 适合高级用户
3. **通知显示** - 实时状态反馈

## ⌨️ 快捷键控制

### 主要快捷键

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Cmd+Alt+B` | 显示电池状态 | 弹出通知显示详细电池信息 |
| `Cmd+Alt+P` | 切换充电保护 | 启用/禁用充电保护功能 |
| `Cmd+Alt+1` | 设置充电限制60% | 快速设置保守充电限制 |
| `Cmd+Alt+2` | 设置充电限制80% | 推荐的日常充电限制 |
| `Cmd+Alt+3` | 设置充电限制90% | 较高的充电限制 |
| `Cmd+Alt+H` | 显示帮助 | 查看所有可用快捷键 |
| `Cmd+Alt+Ctrl+R` | 重新加载配置 | 重启 Hammerspoon 配置 |

### 使用示例

1. **查看电池状态**: 按 `Cmd+Alt+B`
2. **启用电池保护**: 按 `Cmd+Alt+P`
3. **设置充电限制**: 按 `Cmd+Alt+2` (设置为80%)
4. **获取帮助**: 按 `Cmd+Alt+H`

## 💻 命令行控制

### 基本用法

```bash
# 进入 hammerspoon 目录
cd /Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon

# 显示电池状态
./battery_control.sh status

# 启用充电保护
./battery_control.sh protect on

# 禁用充电保护
./battery_control.sh protect off

# 设置充电限制
./battery_control.sh limit 80

# 设置放电限制
./battery_control.sh discharge 20

# 实时监控电池
./battery_control.sh monitor

# 显示帮助
./battery_control.sh help
```

### 创建别名 (可选)

为了更方便使用，可以在 `~/.zshrc` 中添加别名：

```bash
# 添加到 ~/.zshrc
alias battery='/Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon/battery_control.sh'

# 重新加载配置
source ~/.zshrc

# 现在可以直接使用
battery status
battery protect on
battery limit 80
```

## 🔔 通知系统

### 自动通知

系统会在以下情况自动发送通知：

- **启动时**: 显示欢迎信息和快捷键提示
- **充电保护触发**: 当电量达到设定限制时
- **低电量警告**: 当电量低于设定下限时
- **设置更改**: 当修改充电/放电限制时

### 通知内容

通知包含以下信息：
- 当前电量百分比
- 充电状态 (充电中/已充满/使用电池)
- 充电保护状态 (启用/禁用)
- 当前充电和放电限制

## 🔧 配置说明

### 默认设置

- **充电限制**: 80%
- **放电限制**: 20%
- **充电保护**: 默认启用
- **监控频率**: 每30秒检查一次

### 自定义设置

你可以通过以下方式修改设置：

1. **使用快捷键**: `Cmd+Alt+1/2/3` 快速设置常用充电限制
2. **使用命令行**: `./battery_control.sh limit <数值>`
3. **编辑配置文件**: 修改 `init.lua` 中的默认值

## 🚀 快速开始

1. **重新加载配置**:
   ```bash
   # 按快捷键
   Cmd+Alt+Ctrl+R
   
   # 或使用命令行
   osascript -e 'tell application "System Events" to keystroke "r" using {command down, option down, control down}'
   ```

2. **查看当前状态**:
   ```bash
   # 按快捷键
   Cmd+Alt+B
   
   # 或使用命令行
   ./battery_control.sh status
   ```

3. **启用电池保护**:
   ```bash
   # 按快捷键
   Cmd+Alt+P
   
   # 或使用命令行
   ./battery_control.sh protect on
   ```

## 🔍 故障排除

### 快捷键不工作

1. 确认 Hammerspoon 正在运行
2. 检查辅助功能权限
3. 重新加载配置: `Cmd+Alt+Ctrl+R`

### 命令行工具不工作

1. 确认脚本有执行权限: `chmod +x battery_control.sh`
2. 检查 Hammerspoon IPC 是否安装
3. 确认 Hammerspoon 正在运行

### 通知不显示

1. 检查系统通知设置
2. 确认 Hammerspoon 有通知权限
3. 重启 Hammerspoon 应用

## 📋 功能对比

| 功能 | 快捷键 | 命令行 | 菜单栏图标 |
|------|--------|--------|------------|
| 显示电池状态 | ✅ | ✅ | ❌ (不可用) |
| 切换充电保护 | ✅ | ✅ | ❌ (不可用) |
| 设置充电限制 | ✅ | ✅ | ❌ (不可用) |
| 实时监控 | ✅ | ✅ | ❌ (不可用) |
| 便捷性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 功能完整性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 💡 使用建议

1. **日常使用**: 主要使用快捷键 `Cmd+Alt+B` 和 `Cmd+Alt+P`
2. **详细监控**: 使用命令行 `./battery_control.sh monitor`
3. **自动化**: 可以将命令行脚本集成到其他自动化工具中
4. **学习**: 按 `Cmd+Alt+H` 随时查看快捷键帮助

## 🎉 总结

虽然菜单栏图标无法显示，但通过快捷键和命令行，你仍然可以完全控制电池管理的所有功能。这些替代方案甚至在某些方面比菜单栏图标更加强大和灵活！