# Windows CLI 工具安装脚本
# 作者: AI Assistant
# 版本: 1.0
# 描述: 自动安装常用的 Windows CLI 工具

Write-Host "=== Windows CLI 工具安装脚本 ===" -ForegroundColor Green
Write-Host ""

# 检查管理员权限
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Administrator)) {
    Write-Host "警告: 建议以管理员权限运行此脚本以获得最佳体验" -ForegroundColor Yellow
    Write-Host ""
}

# 检查 PowerShell 版本
$psVersion = $PSVersionTable.PSVersion.Major
if ($psVersion -lt 5) {
    Write-Host "错误: 需要 PowerShell 5.0 或更高版本" -ForegroundColor Red
    exit 1
}

Write-Host "PowerShell 版本: $($PSVersionTable.PSVersion)" -ForegroundColor Green
Write-Host ""

# 检查并安装 Chocolatey
Write-Host "检查 Chocolatey 包管理器..." -ForegroundColor Yellow
try {
    choco --version | Out-Null
    Write-Host "Chocolatey 已安装" -ForegroundColor Green
} catch {
    Write-Host "正在安装 Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Chocolatey 安装成功!" -ForegroundColor Green
    } else {
        Write-Host "Chocolatey 安装失败，将使用其他方式安装工具" -ForegroundColor Yellow
    }
}

Write-Host ""

# 检查 Node.js
Write-Host "检查 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Node.js 版本: $nodeVersion" -ForegroundColor Green
    
    # 检查版本是否 >= 18
    $versionNumber = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($versionNumber -lt 18) {
        Write-Host "警告: 建议升级到 Node.js 18+ 版本" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Node.js 未安装，正在安装..." -ForegroundColor Yellow
    try {
        choco install nodejs -y
        Write-Host "Node.js 安装成功!" -ForegroundColor Green
    } catch {
        Write-Host "请手动安装 Node.js: https://nodejs.org" -ForegroundColor Red
    }
}

Write-Host ""

# 安装 Git（如果未安装）
Write-Host "检查 Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "Git 版本: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git 未安装，正在安装..." -ForegroundColor Yellow
    try {
        choco install git -y
        Write-Host "Git 安装成功!" -ForegroundColor Green
    } catch {
        Write-Host "请手动安装 Git: https://git-scm.com" -ForegroundColor Red
    }
}

Write-Host ""

# 安装 Windows Terminal（如果未安装）
Write-Host "检查 Windows Terminal..." -ForegroundColor Yellow
$wtInstalled = Get-AppxPackage -Name "Microsoft.WindowsTerminal" -ErrorAction SilentlyContinue
if ($wtInstalled) {
    Write-Host "Windows Terminal 已安装" -ForegroundColor Green
} else {
    Write-Host "Windows Terminal 未安装，建议从 Microsoft Store 安装" -ForegroundColor Yellow
    Write-Host "下载链接: https://aka.ms/terminal" -ForegroundColor Cyan
}

Write-Host ""

# 安装常用 CLI 工具
$cliTools = @(
    @{Name="GitHub CLI"; Command="gh"; Package="gh"; Description="GitHub 命令行工具"},
    @{Name="Azure CLI"; Command="az"; Package="azure-cli"; Description="Azure 云服务命令行工具"},
    @{Name="Docker CLI"; Command="docker"; Package="docker-desktop"; Description="Docker 容器管理工具"},
    @{Name="Kubectl"; Command="kubectl"; Package="kubernetes-cli"; Description="Kubernetes 集群管理工具"},
    @{Name="Terraform"; Command="terraform"; Package="terraform"; Description="基础设施即代码工具"},
    @{Name="7-Zip CLI"; Command="7z"; Package="7zip"; Description="文件压缩解压工具"}
)

Write-Host "=== 可选 CLI 工具安装 ===" -ForegroundColor Green
Write-Host "以下工具可根据需要选择安装:" -ForegroundColor White
Write-Host ""

foreach ($tool in $cliTools) {
    Write-Host "检查 $($tool.Name)..." -ForegroundColor Yellow
    try {
        $null = & $tool.Command --version 2>$null
        Write-Host "$($tool.Name) 已安装" -ForegroundColor Green
    } catch {
        Write-Host "$($tool.Name) 未安装" -ForegroundColor Red
        Write-Host "描述: $($tool.Description)" -ForegroundColor Gray
        $install = Read-Host "是否安装 $($tool.Name)? (y/N)"
        if ($install -eq 'y' -or $install -eq 'Y') {
            try {
                choco install $tool.Package -y
                Write-Host "$($tool.Name) 安装成功!" -ForegroundColor Green
            } catch {
                Write-Host "$($tool.Name) 安装失败" -ForegroundColor Red
            }
        }
    }
    Write-Host ""
}

# 检查 PATH 环境变量
Write-Host "=== 环境变量检查 ===" -ForegroundColor Green
$npmPath = "$env:APPDATA\npm"
$currentPath = $env:PATH

if ($currentPath -like "*$npmPath*") {
    Write-Host "npm 全局路径已在 PATH 中" -ForegroundColor Green
} else {
    Write-Host "警告: npm 全局路径不在 PATH 中" -ForegroundColor Yellow
    Write-Host "这可能导致全局安装的 npm 包无法直接运行" -ForegroundColor Yellow
    Write-Host "请参考项目中的疑难解答文档修复 PATH 环境变量" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host "建议操作:" -ForegroundColor White
Write-Host "1. 重启 PowerShell 终端以刷新环境变量" -ForegroundColor Yellow
Write-Host "2. 如遇到命令无法识别，请检查 PATH 环境变量" -ForegroundColor Yellow
Write-Host "3. 参考各工具的 readme.md 文件进行详细配置" -ForegroundColor Yellow
Write-Host ""
Write-Host "已安装的 AI CLI 工具:" -ForegroundColor Cyan
Write-Host "- Gemini CLI: 运行 'gemini' 命令" -ForegroundColor White
Write-Host "- Claude Code: 运行 'claude' 命令" -ForegroundColor White
Write-Host ""
Write-Host "如需帮助，请查看项目文档或运行 'toolname --help'" -ForegroundColor Gray