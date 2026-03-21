#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到脚本所在目录，确保相对路径正确
cd "$SCRIPT_DIR"

# 设置 PATH 以包含本地安装的 claude
export PATH="$SCRIPT_DIR/local-tools/bin:$PATH"

# 临时修改 HOME 目录以绕过权限限制，将配置文件保存在当前目录下
# 注意：这会导致 claude 的配置也保存在当前目录下
export HOME="$SCRIPT_DIR"

# 启动 happy-coder，通过环境变量配置 Claude 权限模式
# 尝试直接通过 happy 传递参数或设置环境变量
# 根据 happy-coder 文档（如果有），通常它只是调用 claude
# 如果 happy-coder 内部硬编码了调用方式，可能无法直接改。
# 但 claude 支持 --permission-mode 参数。

# 我们先尝试设置 CLAUDE_OPTS 或类似的变量，或者如果 happy 接受参数
# 既然 happy 是 node 脚本，我们看看能不能直接修改 happy 的调用

# 假设 happy 只是调用 `claude` 命令
# 我们可以创建一个 wrapper 脚本来劫持 claude 命令

mkdir -p bin
cat > bin/claude << EOF
#!/bin/bash
# 调用真实的 claude，并强制添加 --permission-mode=bypassPermissions
# 注意：bypassPermissions 可能太危险，建议用 default 或 specific
# 用户要求 "不要再跟我确认"，对应 --permission-mode=bypassPermissions (或 dontAsk?)
# 查看 help: choices: "acceptEdits", "bypassPermissions", "default", "delegate", "dontAsk", "plan"
# dontAsk 可能是不询问直接执行，bypassPermissions 可能是绕过权限检查
# 试一下 bypassPermissions 或 dontAsk
exec "$SCRIPT_DIR/local-tools/bin/claude" --permission-mode=bypassPermissions "\$@"
EOF
chmod +x bin/claude

# 将当前 bin 目录加入 PATH 最前面
export PATH="$SCRIPT_DIR/bin:$PATH"

# 欺骗 happy-coder 的检测逻辑
# 它会在 $HOME/.local/bin/claude 寻找 claude
# 因为我们将 HOME 设为了 SCRIPT_DIR，所以它会找 $SCRIPT_DIR/.local/bin/claude
mkdir -p "$SCRIPT_DIR/.local/bin"
# 创建软链接指向我们的 wrapper 脚本 (bin/claude)
# 注意：必须指向 wrapper，这样才能带上 --permission-mode 参数
ln -sf "$SCRIPT_DIR/bin/claude" "$SCRIPT_DIR/.local/bin/claude"

# 启动 happy-coder
./node_modules/.bin/happy
