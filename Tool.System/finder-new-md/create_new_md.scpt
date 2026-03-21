#!/usr/bin/osascript

# AppleScript 版本的新建 Markdown 文件
# 可以直接通过快速操作或 Alfred 等工具调用

on run {input, parameters}
    -- 获取 Finder 当前目录
    tell application "Finder"
        try
            set currentFolder to (insertion location as alias)
        on error
            set currentFolder to (path to desktop folder)
        end try
        set targetPath to POSIX path of currentFolder
    end tell
    
    -- 生成唯一文件名
    set baseName to "未命名"
    set extension to ".md"
    set counter to 0
    set fileName to baseName & extension
    set filePath to targetPath & fileName
    
    repeat while fileExists(filePath)
        set counter to counter + 1
        set fileName to baseName & counter & extension
        set filePath to targetPath & fileName
    end repeat
    
    -- 创建文件并写入模板
    set fileContent to "# 标题

## 简介

内容...

## 详细信息

"
    
    try
        set fileRef to open for access POSIX file filePath with write permission
        set eof fileRef to 0
        write fileContent to fileRef as «class utf8»
        close access fileRef
    on error errMsg
        try
            close access POSIX file filePath
        end try
        display notification "创建失败: " & errMsg with title "新建 Markdown 文件"
        return
    end try
    
    -- 在 Finder 中显示并选中
    tell application "Finder"
        activate
        reveal POSIX file filePath
        select POSIX file filePath
    end tell
    
    -- 显示通知
    display notification "已创建: " & fileName with title "新建 Markdown 文件"
    
    -- 延迟后进入重命名模式
    delay 0.3
    tell application "System Events"
        keystroke return
    end tell
    
    return input
end run

-- 辅助函数：检查文件是否存在
on fileExists(filePath)
    try
        tell application "System Events"
            return exists disk item filePath
        end tell
    on error
        return false
    end try
end fileExists
