# 获取 npm 全局模块路径
$npmPath = "$([Environment]::GetFolderPath('ApplicationData'))\npm"

# 获取当前用户的 PATH 环境变量
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# 检查 npm 路径是否已在 PATH 中
if (-not $userPath.Contains($npmPath)) {
    Write-Host "npm 全局路径 '$npmPath' 未在您的用户 PATH 环境变量中找到。"
    Write-Host "正在为您添加..."

    # 将 npm 路径添加到 PATH
    $newPath = "$userPath;$npmPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")

    Write-Host "成功！npm 路径已添加到您的用户 PATH 环境变量中。"
    Write-Host "请注意：您需要关闭并重新打开一个新的 PowerShell 窗口才能使更改生效。"
} else {
    Write-Host "npm 全局路径 '$npmPath' 已经存在于您的用户 PATH 环境变量中。"
    Write-Host "如果 'gemini' 命令仍然无法使用，请尝试重启您的计算机。"
}

Write-Host "脚本执行完毕。"