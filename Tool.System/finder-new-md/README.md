# Finder 右键新建 Markdown 文件

在 macOS Finder 中添加右键快速创建 Markdown 文件的功能。

## 功能特点

✅ 在 Finder 任意位置右键快速创建 MD 文件  
✅ 自动处理重名文件（添加数字后缀）  
✅ 创建后自动选中并进入重命名模式  
✅ 包含基础 Markdown 模板  
✅ 显示系统通知反馈  
✅ 支持设置全局快捷键  

## 快速安装

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.System/finder-new-md
chmod +x install.sh
./install.sh
```

安装程序会自动：
1. 创建 Automator 快速操作
2. 配置系统服务
3. 刷新 Finder

## 使用方法

### 方法 1：右键菜单

1. 在 Finder 中打开任意文件夹
2. 在空白处右键点击（或选中文件夹后右键）
3. 选择「快速操作」→「新建 Markdown 文件」
4. 输入文件名并回车

### 方法 2：快捷键（可选）

1. 打开「系统偏好设置」→「键盘」→「快捷键」
2. 左侧选择「服务」
3. 右侧找到「新建 Markdown 文件」
4. 点击右侧设置快捷键（例如：⌘⇧N）

### 方法 3：使用 Finder 工具栏（可选）

1. 在 Finder 中按住 `⌘` 键
2. 将「新建 Markdown 文件」从「快速操作」拖到工具栏
3. 以后可以直接点击工具栏按钮

## 文件说明

- `create_new_md.sh` - 创建 Markdown 文件的核心脚本
- `install.sh` - 自动安装脚本
- `README.md` - 本说明文档
- `uninstall.sh` - 卸载脚本（可选）

## 自定义

### 修改文件模板

编辑 `create_new_md.sh` 中的模板内容：

```bash
cat > "$file_path" << 'EOF'
# 你的自定义模板
EOF
```

### 修改默认文件名

编辑 `create_new_md.sh`：

```bash
base_name="未命名"  # 改为你喜欢的名称
```

## 故障排除

### 看不到「新建 Markdown 文件」选项

1. 确认安装成功
2. 重启 Finder：`killall Finder`
3. 刷新服务缓存：`/System/Library/CoreServices/pbs -flush_cache`
4. 检查文件路径：`ls -la ~/Library/Services/`

### 权限问题

```bash
chmod +x create_new_md.sh
chmod +x install.sh
```

### 重新安装

```bash
./uninstall.sh
./install.sh
```

## 卸载

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.System/finder-new-md
./uninstall.sh
```

或手动删除：

```bash
rm -rf ~/Library/Services/新建\ Markdown\ 文件.workflow
/System/Library/CoreServices/pbs -flush_cache
```

## 兼容性

- macOS 10.15 (Catalina) 及以上
- 支持 Intel 和 Apple Silicon (M1/M2/M3) 架构

## 技术实现

- 使用 Automator 快速操作
- Shell 脚本处理文件创建
- AppleScript 控制 Finder 交互
- 系统通知提供反馈

## 更新日志

### v1.0 (2026-02-01)
- ✨ 初始版本
- ✅ 基础创建功能
- ✅ 自动重命名支持
- ✅ 系统通知集成

## 许可证

MIT License

## 作者

Tool.System Project
