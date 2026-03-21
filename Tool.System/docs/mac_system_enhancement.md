# 系统增强功能指南

## 桌面日历背景设置

### 方法一：WallCal（推荐）
**WallCal** 是一款专业的桌面日历应用，可以在桌面壁纸上显示半透明的日历覆盖层。

**功能特点：**
- 在桌面显示半透明日历
- 与macOS/iCloud日历同步
- 显示当前月份的日历事件和提醒
- 支持快捷键切换显示/隐藏
- 点击桌面任意位置可切换显示状态

**价格：** 免费基础功能，专业插件需付费

**下载方式：** App Store搜索"WallCal"

### 方法二：Plash + 网页日历（免费方案）
**Plash** 是一款开源应用，可以将任何网页设为Mac桌面壁纸。

**功能特点：**
- 将网页设为桌面壁纸
- 支持Google Calendar、Outlook 365等网页日历
- 低内存占用（约40MB）
- 支持多网站切换
- 可自定义CSS/JavaScript注入
- URL占位符适配屏幕尺寸

**使用步骤：**
1. 从App Store下载Plash
2. 打开Google Calendar或其他网页日历
3. 在Plash中添加日历网页URL
4. 设置为桌面壁纸

**价格：** 完全免费

**下载方式：** App Store搜索"Plash"

### 方法三：DejaDesktop（专业方案）
**DejaDesktop** 是一款专业的桌面信息工具。

**功能特点：**
- 支持Google/Outlook日历作为壁纸
- 可显示多天视图和任务
- 与多种日历服务同步
- 提供丰富的自定义选项

**价格：** 付费应用

**安装建议：**
- 对于简单需求，推荐使用WallCal
- 需要免费方案，选择Plash + 网页日历
- 专业用户可考虑DejaDesktop

## 微信铃声更换指南

### 微信铃声文件位置
微信的通知铃声文件位于：
```
/Applications/WeChat.app/Contents/Resources/notify.caf
```

### 文件信息
- **文件名：** notify.caf
- **格式：** CoreAudio Format (CAF)
- **大小：** 约159KB
- **用途：** 微信消息通知铃声

### 更换方法

#### 方法一：直接替换（需要管理员权限）

**步骤：**
1. **备份原文件**
   ```bash
   sudo cp "/Applications/WeChat.app/Contents/Resources/notify.caf" "/Applications/WeChat.app/Contents/Resources/notify_backup.caf"
   ```

2. **准备新铃声文件**
   - 格式要求：CAF格式（推荐）或WAV/AIFF格式
   - 时长建议：1-3秒
   - 文件大小：建议不超过200KB

3. **转换音频格式**（如果需要）
   ```bash
   # 将MP3转换为CAF格式
   afconvert input.mp3 output.caf -f caff
   ```

4. **替换铃声文件**
   ```bash
   sudo cp "your_new_ringtone.caf" "/Applications/WeChat.app/Contents/Resources/notify.caf"
   ```

5. **重启微信**
   - 完全退出微信应用
   - 重新启动微信

#### 方法二：使用音频编辑工具

**推荐工具：**
- **Audacity**（免费）
- **GarageBand**（系统自带）
- **Logic Pro**（专业版）

**制作步骤：**
1. 打开音频编辑软件
2. 导入或录制新铃声
3. 编辑音频（裁剪、调整音量等）
4. 导出为CAF格式
5. 按照方法一进行替换

### 注意事项

⚠️ **重要提醒：**
- 修改系统应用文件需要管理员权限
- 微信更新后可能会恢复原铃声
- 建议先备份原文件
- 修改前请确保微信已完全退出

**系统完整性保护：**
如果遇到权限问题，可能需要：
1. 关闭SIP（系统完整性保护）
2. 重启到恢复模式
3. 在终端中执行：`csrutil disable`
4. 重启系统后进行修改
5. 完成后重新启用SIP：`csrutil enable`

**测试铃声：**
```bash
# 播放当前微信铃声
afplay "/Applications/WeChat.app/Contents/Resources/notify.caf"
```

### 恢复原铃声
如果需要恢复原铃声：
```bash
sudo cp "/Applications/WeChat.app/Contents/Resources/notify_backup.caf" "/Applications/WeChat.app/Contents/Resources/notify.caf"
```

### 替代方案

如果直接修改应用文件遇到困难，可以考虑：

1. **使用第三方微信客户端**
   - 一些第三方客户端支持自定义铃声
   - 注意安全性和隐私保护

2. **系统通知声音**
   - 在系统偏好设置 → 声音中更改通知声音
   - 这会影响所有应用的通知声音

3. **使用Automator创建快捷方式**
   - 创建自动化脚本来快速切换铃声
   - 适合经常更换铃声的用户

## 微信图片文件存储位置

### 主要存储路径
微信传输和接收的图片文件存储在以下位置：

```
~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/[版本号]/[用户ID]/Message/MessageTemp/[聊天会话ID]/Image/
```

### 具体路径结构

**完整路径示例：**
```
/Users/[用户名]/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/23edee7174a6bafd2efb6265a4fa98e5/Message/MessageTemp/077584660634876d403b3b899a2f304d/Image/
```

**路径组成说明：**
- `2.0b4.0.9` - 微信版本号
- `23edee7174a6bafd2efb6265a4fa98e5` - 用户账号ID（MD5哈希值）
- `077584660634876d403b3b899a2f304d` - 聊天会话ID（每个联系人或群聊对应一个）

### 图片文件类型

**文件命名规则：**
- `[数字]_.pic.jpg` - 原图文件
- `[数字]_.pic_thumb.jpg` - 缩略图文件

**示例文件：**
```
531749458820_.pic.jpg        # 原图 (47KB)
531749458820_.pic_thumb.jpg  # 缩略图 (10KB)
651749618467_.pic.jpg        # 原图 (501KB)
651749618467_.pic_thumb.jpg  # 缩略图 (17KB)
```

### 其他媒体文件位置

**同级目录下还包含：**
- `Audio/` - 语音消息文件
- `Video/` - 视频文件
- `File/` - 其他文件类型

### 收藏图片位置

**收藏的图片存储在：**
```
~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/[版本号]/[用户ID]/Favorites/data/[收藏项ID]/
```

### 快速查找命令

**查找所有图片目录：**
```bash
find ~/Library/Containers/com.tencent.xinWeChat -name "Image" -type d
```

**查找特定聊天的图片：**
```bash
ls -la "~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/*/Message/MessageTemp/*/Image/"
```

**统计图片文件数量：**
```bash
find ~/Library/Containers/com.tencent.xinWeChat -name "*.pic.jpg" | wc -l
```

### 注意事项

⚠️ **重要提醒：**
- 图片文件按聊天会话分别存储在不同目录中
- 每个联系人/群聊对应一个唯一的哈希值目录
- 图片文件名为时间戳格式，不包含原始文件名
- 微信更新可能会改变版本号目录
- 用户切换账号会产生新的用户ID目录

**隐私保护：**
- 这些文件包含个人聊天记录，请妥善保护
- 备份或迁移时注意数据安全
- 不建议直接修改这些文件，可能导致微信异常

## Hammerspoon 配置管理

### 全新安装指南（适用于新Mac）

**1. 安装Hammerspoon应用**
```bash
# 使用Homebrew安装（推荐）
brew install --cask hammerspoon

# 或从官网下载安装包
# https://www.hammerspoon.org/
```

**2. 配置权限**
- 首次启动Hammerspoon时，系统会要求授予辅助功能权限
- 前往 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能
- 勾选Hammerspoon应用

**3. 部署配置文件**
```bash
# 进入项目目录
cd /path/to/Tool.System

# 创建符号链接（如果~/.hammerspoon目录不存在）
ln -s "$(pwd)/hammerspoon" ~/.hammerspoon

# 如果~/.hammerspoon目录已存在，需要先备份再删除
cp -r ~/.hammerspoon ~/.hammerspoon_backup_$(date +%Y%m%d_%H%M%S)
rm -rf ~/.hammerspoon
ln -s "$(pwd)/hammerspoon" ~/.hammerspoon
```

**4. 个人信息配置**
```bash
# 复制个人信息模板
cd hammerspoon/config
cp settings.lua personal-info-private.lua

# 编辑个人信息（替换示例数据为真实信息）
# personal-info-private.lua文件已加入.gitignore，不会被版本控制
```

**5. 启动和测试**
```bash
# 启动Hammerspoon
open -a Hammerspoon

# 重新加载配置
# 快捷键：Cmd + Alt + Ctrl + R
# 或在Hammerspoon菜单中选择"Reload Config"
```

**6. 验证功能**
- 按 `Cmd + Shift + H` 查看帮助菜单
- 按 `Cmd + Shift + V` 测试剪贴板历史
- 按 `Cmd + Shift + N` 测试快速记笔记
- 按 `Cmd + Shift + W` 测试窗口管理

### 配置文件迁移方案（适用于已有配置）
- **问题**: 如何将系统中的Hammerspoon配置文件迁移到项目目录进行版本控制
- **解决方案**: 使用符号链接方式，保持Hammerspoon安装目录不变，只将配置文件放在项目目录
- **实施步骤**:
  1. 备份原系统配置: `cp -r ~/.hammerspoon ~/.hammerspoon_backup_$(date +%Y%m%d_%H%M%S)`
  2. 同步配置到项目目录: `rsync -av --delete ~/.hammerspoon/ ./hammerspoon/`
  3. 删除系统配置目录: `rm -rf ~/.hammerspoon`
  4. 创建符号链接: `ln -s "$(pwd)/hammerspoon" ~/.hammerspoon`
- **优势**: 
  - Hammerspoon程序本身保持在系统默认位置
  - 配置文件在项目目录中便于版本控制和同步
  - 系统正常读取配置，无需修改任何代码

### 配置目录清理
为保持项目目录整洁，已清理hammerspoon目录中的冗余文件：

**删除的文件类型：**
- 备份文件：`init.lua.backup.*`
- 测试文件：`test_config.lua`, `test-chooser.lua`, `test-gesture.lua`
- 临时文件：`.DS_Store`, `clipboard_history.json`, `debug_log.md`
- 脚本文件：`git_push`, `init_complex.lua`, `init_simple.lua`
- 错误目录：`Users/`（误创建的目录）
- 重复内容：`Spoons/Spoons/`, `TouchEvents.spoon/`

**保留的核心文件：**
- 配置文件：`init.lua`, `config/`, `modules/`
- 文档文件：`README.md`, `四指手势使用说明.md`, `docs/`
- 插件文件：`Spoons/Swipe.spoon/`
- 版本控制：`.git/`, `.gitignore`

清理后的目录结构更加简洁，只保留必要的配置文件和文档，便于维护和版本控制。

## 总结

本文档记录了各种系统增强工具的安装和配置过程，为提升工作效率提供了全面的解决方案。通过这些工具的组合使用，可以显著改善日常的计算机使用体验。