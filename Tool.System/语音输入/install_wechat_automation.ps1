# 微信自动化依赖安装脚本
# 使用国内镜像源安装Python包

Write-Host "开始安装微信自动化所需依赖..." -ForegroundColor Green

# 设置Anaconda环境路径
$anacondaPath = "C:\Users\28919\anaconda3\Scripts"
$pipPath = "$anacondaPath\pip.exe"

# 检查pip是否存在
if (-not (Test-Path $pipPath)) {
    Write-Host "错误: 未找到pip，请检查Anaconda安装路径" -ForegroundColor Red
    exit 1
}

# 使用清华大学镜像源
$mirrorUrl = "https://pypi.tuna.tsinghua.edu.cn/simple"

# 安装所需包
$packages = @(
    "pyautogui",
    "pygetwindow",
    "pillow",
    "opencv-python"
)

foreach ($package in $packages) {
    Write-Host "正在安装 $package..." -ForegroundColor Yellow
    & $pipPath install $package -i $mirrorUrl --trusted-host pypi.tuna.tsinghua.edu.cn
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $package 安装成功" -ForegroundColor Green
    } else {
        Write-Host "❌ $package 安装失败" -ForegroundColor Red
    }
}

Write-Host "\n依赖安装完成！" -ForegroundColor Green
Write-Host "现在可以运行微信自动化脚本了" -ForegroundColor Cyan

# 暂停以查看结果
Read-Host "按任意键继续..."