#!/bin/bash

# 双击运行的安装脚本

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 确保脚本有执行权限
chmod +x install.sh
chmod +x create_new_md.sh

# 运行安装
./install.sh

# 等待用户按键
echo ""
read -p "按任意键关闭窗口..." -n 1 -r
