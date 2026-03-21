# Tool.System 目录清理整理计划

## 📋 当前目录分析

### 🎯 已整理的目录
- ✅ **chrome/** - 新建的Chrome相关工具目录
  - `bookmarks/` - Chrome书签清理工具

### 🔧 开发工具类目录
- **Claude code/** - Claude代码工具
- **Gemini CLI/** - Gemini命令行工具  
- **Ghostty Terminal/** - Ghostty终端工具
- **Windows CLI Tools/** - Windows命令行工具
- **语音输入/** - 语音输入自动化工具

### 🖥️ 系统工具类目录
- **hammerspoon/** - Hammerspoon配置和模块
- **iMac_sleep_troubleshooting/** - iMac睡眠问题诊断工具

### 📁 数据管理类目录
- **nas/** - NAS文件管理工具（内容过多，需要整理）

### 📚 文档和配置类
- **docs/** - 文档目录
- **scripts/** - 脚本工具
- **tests/** - 测试相关文件

### ❌ 需要清理的目录
- **Users/** - 似乎是误创建的用户目录
- **Volumes/** - 似乎是误创建的卷目录
- **software/** - 空目录

### 📄 根目录文件
- `README.md` - 主文档
- `system_enhancement.md` - 系统增强文档

## 🎯 清理整理计划

### 1. 删除无用目录
- [ ] 删除 `Users/` 目录（误创建）
- [ ] 删除 `Volumes/` 目录（误创建）
- [ ] 删除 `software/` 空目录

### 2. 整理开发工具
- [ ] 创建 `dev-tools/` 目录
- [ ] 移动相关工具到统一目录：
  - `Claude code/` → `dev-tools/claude/`
  - `Gemini CLI/` → `dev-tools/gemini/`
  - `Windows CLI Tools/` → `dev-tools/windows-cli/`
  - `语音输入/` → `dev-tools/voice-input/`

### 3. 整理系统工具
- [ ] 创建 `system-tools/` 目录
- [ ] 移动系统相关工具：
  - `hammerspoon/` → `system-tools/hammerspoon/`
  - `iMac_sleep_troubleshooting/` → `system-tools/imac-sleep/`
  - `Ghostty Terminal/` → `system-tools/ghostty/`

### 4. 整理NAS工具
- [ ] 重新组织 `nas/` 目录内容
- [ ] 按功能分类NAS工具

### 5. 保持现有结构
- [ ] `chrome/` - 保持
- [ ] `docs/` - 保持
- [ ] `scripts/` - 保持
- [ ] `tests/` - 保持

## 📊 预期结果

整理后的目录结构：
```
Tool.System/
├── chrome/                    # Chrome相关工具
├── dev-tools/                 # 开发工具集合
├── system-tools/              # 系统工具集合
├── nas/                       # NAS管理工具
├── docs/                      # 文档
├── scripts/                   # 脚本工具
├── tests/                     # 测试文件
├── README.md
└── system_enhancement.md
```

## ⚠️ 注意事项
1. 移动前先备份重要文件
2. 更新相关文档中的路径引用
3. 检查脚本中的硬编码路径
4. 测试移动后工具的正常运行