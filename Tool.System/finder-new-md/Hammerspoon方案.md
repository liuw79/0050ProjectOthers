# Hammerspoon 方案 - Finder 新建 Markdown 文件

## 🎯 为什么选择 Hammerspoon？

如果 Automator 服务在系统设置中不显示，使用 Hammerspoon 是最佳替代方案：

✅ 更可靠 - 不依赖系统服务  
✅ 更灵活 - 完全自定义快捷键  
✅ 更强大 - 可以扩展更多功能  
✅ 已安装 - 你的系统已有 Hammerspoon  

---

## 📦 安装步骤

### 方式 1：自动配置（推荐）

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.System/finder-new-md
./install_to_hammerspoon.sh
```

### 方式 2：手动配置

#### 步骤 1：复制 Spoon

Spoon 已创建在：
```
hammerspoon/Spoons/NewMarkdownFile.spoon/init.lua
```

#### 步骤 2：修改 Hammerspoon 配置

编辑你的 `~/.hammerspoon/init.lua`，添加以下代码：

```lua
-- 新建 Markdown 文件快捷键
hs.loadSpoon("NewMarkdownFile")
spoon.NewMarkdownFile:bindHotkeys({
    createMarkdown = {{"cmd", "shift"}, "M"}
})
```

或者直接复制提供的配置：

```bash
# 查看配置示例
cat /Users/comdir/SynologyDrive/0050Project/Tool.System/finder-new-md/hammerspoon_config.lua

# 可以将内容复制到你的 init.lua 中
```

#### 步骤 3：重新加载 Hammerspoon

1. 点击菜单栏的 Hammerspoon 图标
2. 选择「Reload Config」
3. 看到提示：「新建 MD 快捷键已启用: ⌘⇧M」

---

## 🚀 使用方法

### 快捷键

在 Finder 中按 **⌘⇧M**：
1. 自动在当前目录创建 `未命名.md`
2. 文件在 Finder 中被选中
3. 按回车键重命名

### 自定义快捷键

编辑 `init.lua` 中的快捷键配置：

```lua
-- 改为其他快捷键
spoon.NewMarkdownFile:bindHotkeys({
    createMarkdown = {{"cmd", "ctrl"}, "N"}  -- ⌘⌃N
})

-- 或者
spoon.NewMarkdownFile:bindHotkeys({
    createMarkdown = {{"cmd", "alt"}, "M"}   -- ⌘⌥M
})
```

---

## 🔧 高级配置

### 修改脚本路径

如果脚本位置改变，编辑 Spoon 文件：

```lua
-- 在 NewMarkdownFile.spoon/init.lua 中
local script_path = "/你的/新路径/create_new_md_simple.sh"
```

### 添加更多功能

可以扩展 Spoon 支持：
- 不同类型的文件（.txt, .py, .js）
- 多种模板选择
- 自定义文件名
- 等等

---

## 📊 对比：Automator vs Hammerspoon

| 特性 | Automator 服务 | Hammerspoon |
|------|----------------|-------------|
| 系统集成 | ✅ 原生支持 | ⚠️  需要额外软件 |
| 快捷键设置 | ⚠️  系统设置（可能不显示） | ✅ 灵活自定义 |
| 稳定性 | ⚠️  macOS 版本依赖 | ✅ 非常稳定 |
| 扩展性 | ❌ 有限 | ✅ 非常强大 |
| 配置难度 | ✅ 简单 | ⭐⭐ 中等 |

---

## ✅ 验证安装

运行以下测试：

```bash
# 1. 检查 Spoon 是否存在
ls -la ~/SynologyDrive/0050Project/Tool.System/hammerspoon/Spoons/NewMarkdownFile.spoon/

# 2. 检查脚本是否可执行
ls -la ~/SynologyDrive/0050Project/Tool.System/finder-new-md/create_new_md_simple.sh

# 3. 手动测试脚本
~/SynologyDrive/0050Project/Tool.System/finder-new-md/create_new_md_simple.sh ~/Desktop
```

---

## 🆘 故障排除

### 问题：按快捷键没反应

**检查**：
1. Hammerspoon 是否在运行？（菜单栏有图标）
2. 配置是否已加载？（Reload Config）
3. 快捷键是否冲突？（尝试其他组合）

**解决**：
```lua
-- 在 init.lua 中添加调试信息
hs.hotkey.bind({"cmd", "shift"}, "M", function()
    hs.alert.show("快捷键触发了！")
    spoon.NewMarkdownFile:createMarkdownFile()
end)
```

### 问题：创建文件失败

**检查**：
1. 脚本路径是否正确？
2. 脚本是否有执行权限？
3. 查看 Hammerspoon Console 的错误信息

**解决**：
```bash
# 确保脚本可执行
chmod +x ~/SynologyDrive/0050Project/Tool.System/finder-new-md/create_new_md_simple.sh

# 测试脚本
~/SynologyDrive/0050Project/Tool.System/finder-new-md/create_new_md_simple.sh ~/Desktop
```

---

## 📖 相关文档

- Hammerspoon 官方文档: https://www.hammerspoon.org/docs/
- Spoon 开发指南: https://github.com/Hammerspoon/hammerspoon/blob/master/SPOONS.md
- 你的 Hammerspoon 配置: `/Users/comdir/SynologyDrive/0050Project/Tool.System/hammerspoon/`

---

## 🎉 优势

使用 Hammerspoon 方案的好处：

1. **不依赖系统服务** - 绕过 macOS 服务识别问题
2. **快捷键完全自定义** - 不受系统设置限制
3. **统一管理** - 所有自定义功能都在 Hammerspoon 中
4. **更强扩展性** - 可以添加更多自动化功能
5. **跨版本兼容** - 不受 macOS 版本更新影响

---

**推荐指数**: ⭐⭐⭐⭐⭐

如果你已经在使用 Hammerspoon，这是最佳方案！
