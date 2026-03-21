-- Finder 新建 Markdown 文件模块
-- 快捷键: ⌘⇧M

local obj = {}
obj.__index = obj

-- Metadata
obj.name = "NewMarkdownFile"
obj.version = "1.0"
obj.author = "Tool.System"
obj.license = "MIT"

-- 脚本路径
local script_path = "/Users/comdir/SynologyDrive/0050Project/Tool.System/finder-new-md/create_new_md_simple.sh"

-- 创建 Markdown 文件
function obj:createMarkdownFile()
    -- 获取当前 Finder 路径
    local script = [[
        tell application "Finder"
            try
                set currentPath to POSIX path of (insertion location as alias)
                return currentPath
            on error
                return "~/Desktop"
            end try
        end tell
    ]]
    
    local ok, result = hs.osascript.applescript(script)
    local targetPath = ok and result or os.getenv("HOME") .. "/Desktop"
    
    -- 执行脚本创建文件
    local command = string.format('"%s" "%s"', script_path, targetPath)
    hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            -- 成功通知
            hs.notify.new({
                title = "新建 Markdown 文件",
                informativeText = "文件已创建",
                withdrawAfter = 2
            }):send()
        else
            -- 失败通知
            hs.notify.new({
                title = "新建 Markdown 文件",
                informativeText = "创建失败: " .. stdErr,
                withdrawAfter = 3
            }):send()
        end
    end, {"-c", command}):start()
end

-- 绑定快捷键
function obj:bindHotkeys(mapping)
    local def = {
        createMarkdown = hs.fnutils.partial(self.createMarkdownFile, self)
    }
    hs.spoons.bindHotkeysToSpec(def, mapping)
end

return obj
