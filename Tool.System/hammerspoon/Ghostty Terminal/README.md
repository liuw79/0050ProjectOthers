# Ghostty Terminal 安装指南

## 📋 安装信息

**安装日期**: 2025年1月23日  
**版本**: Ghostty 1.2.0  
**安装方式**: Homebrew Cask  

## ✅ 安装状态

- ✅ **应用安装**: `/Applications/Ghostty.app`
- ✅ **命令行工具**: `/Applications/Ghostty.app/Contents/MacOS/ghostty`
- ✅ **手册页面**: `/opt/homebrew/share/man/man1/ghostty.1`
- ✅ **Shell补全**: Bash, Fish, Zsh

## 🚀 使用方式

### 图形界面启动
1. 在 Launchpad 中找到 Ghostty
2. 或在 Applications 文件夹中双击 Ghostty.app

### 命令行启动
```bash
# 直接启动应用
open -a Ghostty

# 使用命令行工具
/Applications/Ghostty.app/Contents/MacOS/ghostty

# 查看版本信息
/Applications/Ghostty.app/Contents/MacOS/ghostty --version
```

## 🔧 技术信息

- **Zig版本**: 0.14.1
- **构建模式**: ReleaseFast
- **字体引擎**: CoreText
- **渲染器**: Metal
- **事件循环**: kqueue

## 📚 相关资源

- **官方网站**: https://ghostty.org/
- **文档**: `man ghostty`
- **配置**: `man ghostty.5`

## 🛠 安装命令记录

```bash
# 使用Homebrew安装（已配置国内镜像）
brew install --cask ghostty
```

## 💡 提示

- Ghostty是一个现代化的终端模拟器，专为性能和功能而设计
- 支持GPU加速渲染，提供流畅的使用体验
- 完全兼容现有的终端工作流程