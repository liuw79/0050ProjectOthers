# Windows CLI 工具使用指南

## 简介

本指南涵盖了 Windows 系统下常用的命令行界面（CLI）工具的安装、配置和使用方法。这些工具可以大大提升开发者和高级用户的工作效率。

## 快速安装

### 自动安装（推荐）

运行项目中的安装脚本：

```powershell
.\install_cli_tools.ps1
```

该脚本会自动检查和安装以下工具：
- Chocolatey 包管理器
- Node.js（如果未安装）
- Git（如果未安装）
- 其他可选 CLI 工具

## 核心工具

### 🍫 Chocolatey

**功能**：Windows 包管理器

**安装**：
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**常用命令**：
```powershell
choco install <package>     # 安装软件包
choco upgrade <package>     # 升级软件包
choco uninstall <package>   # 卸载软件包
choco list --local-only     # 查看已安装的包
choco search <keyword>      # 搜索软件包
```

### 🌐 Node.js & npm

**功能**：JavaScript 运行时和包管理器

**安装**：
```powershell
choco install nodejs
```

**常用命令**：
```powershell
node --version              # 查看 Node.js 版本
npm --version               # 查看 npm 版本
npm install -g <package>    # 全局安装包
npm list -g --depth=0       # 查看全局安装的包
npm config get prefix       # 查看全局安装路径
```

### 🔧 Git

**功能**：版本控制系统

**安装**：
```powershell
choco install git
```

**基本配置**：
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

**常用命令**：
```bash
git clone <url>             # 克隆仓库
git status                  # 查看状态
git add .                   # 添加所有更改
git commit -m "message"     # 提交更改
git push                    # 推送到远程
git pull                    # 拉取远程更改
```

## AI CLI 工具

### 🤖 Gemini CLI

**功能**：Google Gemini AI 命令行工具

**安装**：参考 `Gemini CLI/readme.md`

**使用**：
```bash
gemini                      # 启动交互模式
gemini "your question"      # 直接提问
```

### 🧠 Claude Code

**功能**：Anthropic Claude AI 编程助手

**安装**：参考 `Claude code/readme.md`

**使用**：
```bash
claude                      # 启动编程助手
/help                       # 查看帮助
/login                      # 重新登录
```

## 开发者工具

### 🐙 GitHub CLI

**功能**：GitHub 命令行工具

**安装**：
```powershell
choco install gh
```

**认证**：
```bash
gh auth login
```

**常用命令**：
```bash
gh repo create              # 创建仓库
gh repo clone <repo>        # 克隆仓库
gh issue list               # 查看 issues
gh pr create                # 创建 Pull Request
gh pr list                  # 查看 Pull Requests
```

### ☁️ Azure CLI

**功能**：Azure 云服务命令行工具

**安装**：
```powershell
choco install azure-cli
```

**登录**：
```bash
az login
```

**常用命令**：
```bash
az account list             # 查看账户
az group list               # 查看资源组
az vm list                  # 查看虚拟机
```

### 🐳 Docker CLI

**功能**：容器管理工具

**安装**：
```powershell
choco install docker-desktop
```

**常用命令**：
```bash
docker --version            # 查看版本
docker images               # 查看镜像
docker ps                   # 查看运行中的容器
docker run <image>          # 运行容器
docker build -t <name> .    # 构建镜像
```

### ⚓ Kubectl

**功能**：Kubernetes 集群管理工具

**安装**：
```powershell
choco install kubernetes-cli
```

**常用命令**：
```bash
kubectl version             # 查看版本
kubectl get pods            # 查看 Pods
kubectl get services        # 查看服务
kubectl apply -f <file>     # 应用配置
```

### 🏗️ Terraform

**功能**：基础设施即代码工具

**安装**：
```powershell
choco install terraform
```

**常用命令**：
```bash
terraform init              # 初始化
terraform plan              # 查看执行计划
terraform apply             # 应用更改
terraform destroy           # 销毁资源
```

## 系统工具

### 🗜️ 7-Zip CLI

**功能**：文件压缩解压工具

**安装**：
```powershell
choco install 7zip
```

**常用命令**：
```bash
7z a archive.zip file.txt   # 压缩文件
7z x archive.zip            # 解压文件
7z l archive.zip            # 列出压缩包内容
```

### 🔍 Everything CLI

**功能**：文件搜索工具命令行版本

**安装**：
```powershell
choco install everything
```

**使用**：
```bash
es <search_term>            # 搜索文件
```

## 疑难解答

### 命令无法识别问题

如果安装后命令无法识别，通常是 PATH 环境变量问题：

1. **检查 PATH**：
   ```powershell
   $env:PATH -split ';'
   ```

2. **添加路径到 PATH**：
   - 按 `Win + R`，输入 `sysdm.cpl`
   - 点击"高级" → "环境变量"
   - 编辑用户变量中的 `Path`
   - 添加相应的程序路径

3. **常见路径**：
   - npm 全局包：`%APPDATA%\npm`
   - Chocolatey：`C:\ProgramData\chocolatey\bin`
   - Git：`C:\Program Files\Git\cmd`

4. **重启终端**：
   修改 PATH 后必须重启 PowerShell 才能生效。

### PowerShell 执行策略

如果脚本无法执行，可能需要修改执行策略：

```powershell
# 查看当前策略
Get-ExecutionPolicy

# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或者临时绕过策略
Set-ExecutionPolicy Bypass -Scope Process -Force
```

### 网络问题

如果下载速度慢或失败：

1. **使用国内镜像**：
   ```powershell
   # npm 使用淘宝镜像
   npm config set registry https://registry.npmmirror.com
   
   # Chocolatey 使用代理（如果需要）
   choco config set proxy http://proxy-server:port
   ```

2. **检查防火墙和杀毒软件**：
   确保允许相关程序访问网络。

## 最佳实践

### 1. 定期更新

```powershell
# 更新 Chocolatey 包
choco upgrade all

# 更新 npm 全局包
npm update -g

# 更新 Git
git update-git-for-windows
```

### 2. 备份配置

重要的配置文件应该备份：
- Git 配置：`~\.gitconfig`
- npm 配置：`~\.npmrc`
- PowerShell 配置：`$PROFILE`

### 3. 使用别名

在 PowerShell 配置文件中添加常用别名：

```powershell
# 编辑配置文件
notepad $PROFILE

# 添加别名示例
Set-Alias ll Get-ChildItem
Set-Alias grep Select-String
function .. { Set-Location .. }
```

### 4. 安全注意事项

- 只从官方源安装软件
- 定期检查已安装的包
- 避免使用管理员权限运行不必要的命令
- 保持系统和工具更新

## 推荐学习资源

- [PowerShell 官方文档](https://docs.microsoft.com/powershell/)
- [Git 官方教程](https://git-scm.com/docs/gittutorial)
- [Docker 官方文档](https://docs.docker.com/)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)

---

**提示**：本指南涵盖了常用的 CLI 工具，根据实际需求选择安装。如有问题，请参考各工具的官方文档或在项目中提交 Issue。