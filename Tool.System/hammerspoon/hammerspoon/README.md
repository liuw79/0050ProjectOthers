# 电池充电限制控制工具

## 功能说明

这个工具可以在 macOS 上控制电池充电限制，在 80% 和 100% 之间切换。

## 文件说明

- `battery_control_wrapper.sh` - 主要的控制脚本
- `battery_control.lua` - Hammerspoon 配置文件
- `test_battery_control.sh` - 测试脚本

## 使用方法

### 1. 命令行使用

```bash
# 切换电池充电限制（80% ↔ 100%）
./battery_control_wrapper.sh toggle

# 设置为 80% 限制
./battery_control_wrapper.sh set80

# 取消限制（设置为 100%）
./battery_control_wrapper.sh set100
```

### 2. Hammerspoon 快捷键

将 `battery_control.lua` 的内容添加到你的 `~/.hammerspoon/init.lua` 文件中，然后：

- 按 `Cmd + Shift + B` 切换电池充电限制

### 3. 状态说明

- **80% 限制**: 电池充电到 80% 后停止充电，保护电池寿命
- **100% 无限制**: 电池可以充电到 100%，系统默认行为

## 工作原理

1. 脚本使用状态文件 `/tmp/battery_limit_state` 来跟踪当前状态
2. 调用 `batt` 命令来实际控制充电限制
3. 提供用户友好的状态反馈

## 依赖要求

- macOS 系统
- 已安装 `batt` 工具 (https://github.com/charlie0129/batt)
- Hammerspoon (如果使用快捷键功能)
- sudo 权限

## 测试

运行测试脚本来验证功能：

```bash
./test_battery_control.sh
```

## 注意事项

1. 首次运行需要输入 sudo 密码
2. 状态切换可能需要 1-2 分钟才能在系统中生效
3. 当前电量高于设置的限制时，电池不会充电但会使用外接电源

# Hammerspoon 增强配置

这是一个模块化的 Hammerspoon 配置，提供了丰富的功能来提升 macOS 的使用体验。

## 功能特性

### 📋 剪贴板管理
- 自动保存剪贴板历史记录
- 支持搜索和过滤
- 持久化存储
- 支持文本、图片、文件等多种类型
- **快捷键**: `Cmd + Shift + V`

### 👤 个人信息管理
- 快速输入姓名、手机号、个人邮箱、地址到当前光标位置
- 支持公司信息：公司名称、纳税人识别号、公司邮箱、身份证
- 支持完整信息一键输入
- **隐私保护**：真实信息存储在本地私有文件中，不会提交到版本控制
- **快捷键**: `Opt + Cmd + P`

**配置说明：**
- 默认配置文件：`config/settings.lua`（包含示例数据）
- 私有配置文件：`config/personal-info-private.lua`（包含真实信息，已加入.gitignore）
- 系统会自动加载私有配置覆盖默认配置

### 📝 快速记笔记
- 支持分类记录（工作、学习、生活、想法、待办）
- 自动添加时间戳
- Markdown 格式
- 自动保存到文件
- 支持剪贴板内容预填充
- **查看功能**：浏览已保存笔记，支持内容搜索
- **快捷键**: `Cmd + Shift + N`
1. 确保已安装 [Hammerspoon](https://www.hammerspoon.org/)
2. 将配置文件复制到 `~/.hammerspoon/` 目录
3. 重新加载 Hammerspoon 配置（`Cmd + Alt + Ctrl + R`）
4. 按 `Cmd + Shift + H` 查看帮助
### 🍒 番茄时钟
- 25分钟标准番茄工作法计时
- 菜单栏显示倒计时
- 支持开始/暂停/恢复功能
- 时间到达时弹窗和通知提醒
- **快捷键**: `Cmd + Shift + T`

### ❓ 帮助系统
- 快捷键列表
- 功能模块说明
- 系统状态显示
- 配置信息查看
- **快捷键**: `Cmd + Shift + H`

### 🚀 Git 自动化脚本
- 全自动化Git推送脚本 `git_push`
- 自动添加所有变化到暂存区
- 智能生成提交信息或使用自定义信息
- 自动推送到远程仓库
- 彩色输出和详细状态信息
- **使用方法**: `./git_push` 或 `./git_push "自定义提交信息"`

## 文件结构

```
~/.hammerspoon/
├── init.lua                    # 主配置文件
├── git_push                    # 全自动化Git推送脚本
├── config/
│   └── settings.lua           # 全局设置和配置
├── modules/
│   ├── clipboard.lua          # 剪贴板管理模块
│   ├── personal-info.lua      # 个人信息模块
│   ├── quick-note.lua         # 快速记笔记模块
│   ├── window-manager.lua     # 窗口管理模块
│   ├── system-utils.lua       # 系统功能模块
│   └── help-system.lua        # 帮助系统模块
└── README.md                   # 说明文档
```

## 快速开始

### 安装

详细安装指南请参考 [INSTALL.md](INSTALL.md) 文件。

**快速安装：**
```bash
# 1. 安装 Hammerspoon
brew install --cask hammerspoon

# 2. 部署配置
cd /path/to/Tool.System
ln -s "$(pwd)/hammerspoon" ~/.hammerspoon

# 3. 启动应用
open -a Hammerspoon
```

### 首次使用

1. 配置系统权限（辅助功能）
2. 复制个人信息模板：`cp config/settings.lua config/personal-info-private.lua`
3. 编辑个人信息文件
4. 按 `Cmd + Shift + H` 查看帮助菜单

## 自定义配置

所有配置都在 `config/settings.lua` 文件中，你可以根据需要修改：

- 个人信息（姓名、电话、邮箱、地址）
- 笔记保存路径和分类
- 剪贴板历史数量限制
- 快捷键绑定
- 窗口布局预设

## 常用快捷键

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 剪贴板历史 | `Cmd + Shift + V` | 显示剪贴板历史选择器 |
| 个人信息 | `Opt + Cmd + P` | 快速输入个人信息到光标位置 |
| 快速记笔记 | `Cmd + Shift + N` | 打开笔记输入界面 |
| 窗口管理 | `Cmd + Shift + W` | 窗口管理选择器 |
| 系统功能 | `Cmd + Shift + S` | 系统功能选择器 |
| 帮助系统 | `Cmd + Shift + H` | 显示帮助菜单 |
| 重新加载 | `Cmd + Alt + Ctrl + R` | 重新加载配置 |

## 版本历史

### v2.0 (当前版本)
- 完全重构为模块化架构
- 新增窗口管理功能
- 新增系统功能模块
- 新增帮助系统
- 改进剪贴板管理
- 优化用户体验

### v1.0
- 基础剪贴板管理
- 个人信息快速粘贴
- 简单的快速记笔记功能

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个配置！

## 许可证

MIT License
