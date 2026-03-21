# Git 仓库管理与重命名操作记录

> 本文档记录了 2025-09-25 对本仓库进行的历史整理、强制推送以及远程仓库重命名的完整操作流程，便于后续参考与复现。

---

## 1. 本地分支强制覆盖远程（以本地为准）

1. 确认工作区干净，确保 **无未提交文件**：

   ```bash
   git status -sb
   ```

2. 确认远程地址：

   ```bash
   git remote -v
   ```

3. 强制推送本地 `main` 分支到远程：

   ```bash
   git push -f origin main
   ```

   *说明：该命令会用本地提交历史覆盖远程分支历史，需谨慎使用。*

---

## 2. 远程仓库改名（`hammerspoon-config` → `Tool.System`）

### 2.1 GitHub 页面操作

1. 打开仓库主页 → `Settings` → `General` → **Repository name**。
2. 将仓库名从 `hammerspoon-config` 修改为 `Tool.System` 并确认。
3. GitHub 会自动创建旧地址到新地址的 **301 重定向**，旧链接依然可访问，但推荐各端更新为新地址。

### 2.2 本地仓库更新远程地址

```bash
git remote set-url origin https://github.com/liuw79/Tool.System.git

git remote -v   # 验证已指向新仓库名

git push -u origin main   # 如提示无上游分支，则设置并推送
```

执行结果示例：

```text
branch 'main' set up to track 'origin/main'.
Everything up-to-date
```

---

## 3. 其他注意事项

1. **通知协作者**：其他克隆了旧仓库的协作者需执行相同的 `git remote set-url`，或重新克隆新仓库。
2. **删除旧仓库**：确认新仓库运作正常后，可选择在 GitHub 上删除旧仓库（若 GitHub 未自动保留重定向）。
3. **处理 git stash**：本次操作前曾临时 `git stash` 了 `hammerspoon/clipboard_history.json`，如需恢复可执行：

   ```bash
   git stash list
   git stash pop stash@{<编号>}
   ```

4. **仓库瘦身**：若仍需删除大文件/子目录，可先本地清理后重复第 1 步强制推送。

---

> 以上步骤已在 macOS 环境验证通过，如需在 Windows / Linux 终端执行同样有效。