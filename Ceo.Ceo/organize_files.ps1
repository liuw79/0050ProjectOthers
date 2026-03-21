$ErrorActionPreference = 'Stop'

$basePath = "c:\Users\28919\SynologyDrive\0050 Project\Ceo.Ceo"
$filesSourceDir = Join-Path $basePath "files"

Write-Host "Starting file organization process..."
Write-Host "Base path: $basePath"
Write-Host "Source directory for files: $filesSourceDir"

$targetDirs = @{
    "01_战略与规划" = @(
        "高维学堂2025年OGSM.md",
        "高维学堂2025年OGSM - 2025年OGSM.csv",
        "CEO战略仪表盘指南.md",
        "CEO管理工具套装说明.md",
        "文档保密与协同标准.md" // 新增
    );
    "02_产品与运营" = @(
        "CEO产品开发管理文档.md",
        "CEO运营流程文档.md"
    );
    "03_组织与团队" = @(
        "CEO团队管理文档.md",
        "智邑组织设计工坊（2天1晚简化版) v2.txt",
        "高维学堂组织设计工作坊准备材料.md",
        "股权激励总体情况.md",
        "股权激励记录_范思洁.md",
        "股权激励记录_丹纯.md",
        "德鲁克读书会_卓有成效的管理者_学习资料.md", // 新增 - 示例文件名
        "德鲁克读书会_管理的实践_学习资料.md"    // 新增 - 示例文件名
    );
    "04_客户与市场" = @(
        "CEO客户分析工具.md"
    );
    "05_财务与监控" = @(
        "CEO财务监控工具指南.md"
    );
    "06_管理驾驶舱与工具集" = @(
        "CEO管理仪表盘.xlsx",
        "CEO管理仪表盘实施工作表.md",
        "CEO管理仪表盘实施计划.md",
        "CEO管理仪表盘数据采集模板.md",
        "CEO管理仪表盘模板结构.md",
        "CEO决策支持工具.md"
    );
    "07_改进与记录" = @(
        "CEO工具包改进建议与问题记录.md"
    )
}

foreach ($dirName in $targetDirs.Keys) {
    $fullDirPath = Join-Path $basePath $dirName
    if (-not (Test-Path $fullDirPath -PathType Container)) {
        try {
            New-Item -ItemType Directory -Path $fullDirPath -Force | Out-Null
            Write-Host "Successfully created directory: $fullDirPath"
        } catch {
            Write-Error "Failed to create directory: $fullDirPath. Error: $($_.Exception.Message)"
            # Exit 1 # Stop script if directory creation fails
        }
    } else {
        Write-Host "Directory already exists: $fullDirPath"
    }

    foreach ($fileName in $targetDirs[$dirName]) {
        $sourceFilePath = Join-Path $filesSourceDir $fileName
        $destinationFilePath = Join-Path $fullDirPath $fileName

        if (Test-Path $sourceFilePath -PathType Leaf) {
            try {
                Move-Item -Path $sourceFilePath -Destination $destinationFilePath -Force
                Write-Host "Successfully moved '$fileName' to '$dirName' directory."
            } catch {
                Write-Error "Failed to move '$sourceFilePath' to '$destinationFilePath'. Error: $($_.Exception.Message)"
            }
        } else {
            Write-Warning "Source file not found or is not a file: $sourceFilePath"
        }
    }
}

Write-Host "File organization process completed."

# Optional: Check if the original 'files' directory is empty and suggest removal or remove
# if ((Get-ChildItem -Path $filesSourceDir).Count -eq 0) {
#    Write-Host "The original 'files' directory is now empty."
#    # Remove-Item -Path $filesSourceDir -Recurse -Force
#    # Write-Host "Removed empty source directory: $filesSourceDir"
# } else {
#    Write-Warning "The original 'files' directory is not empty. Please check its contents: $filesSourceDir"
# }
