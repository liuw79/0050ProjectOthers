-- 媒体处理模块
-- 提供音视频文件的简单处理功能
-- 依赖: ffmpeg (需要通过 brew install ffmpeg 安装)

local mediaProcessor = {}

-- 全局函数声明
local cutVideo, convertVideo, extractAudio, convertAudio

-- 检查ffmpeg是否安装
local function checkFFmpeg()
    local task = hs.task.new("/usr/bin/which", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            return true
        else
            hs.alert.show("请先安装 ffmpeg: brew install ffmpeg", 5)
            return false
        end
    end, {"ffmpeg"})
    task:start()
    task:waitUntilExit()
    return task:terminationStatus() == 0
end

-- 选择文件对话框
local function selectFile(title, fileTypes)
    local chooser = hs.chooser.new(function(choice)
        if choice then
            return choice.path
        end
        return nil
    end)
    
    -- 使用系统文件选择器
    local script = string.format([[
        tell application "System Events"
            set theFile to choose file with prompt "%s"
            return POSIX path of theFile
        end tell
    ]], title or "选择文件")
    
    local success, result = hs.osascript.applescript(script)
    if success then
        return result:gsub("\n$", "") -- 移除末尾换行符
    end
    return nil
end

-- 选择保存位置
local function selectSaveLocation(defaultName)
    local script = string.format([[
        tell application "System Events"
            set theFile to choose file name with prompt "保存到" default name "%s"
            return POSIX path of theFile
        end tell
    ]], defaultName or "output")
    
    local success, result = hs.osascript.applescript(script)
    if success then
        return result:gsub("\n$", "")
    end
    return nil
end

-- 视频切割功能
local function cutVideo()
    if not checkFFmpeg() then return end
    
    local inputFile = selectFile("选择要切割的视频文件")
    if not inputFile then return end
    
    -- 获取切割参数
    local button, startTime = hs.dialog.textPrompt("开始时间", "请输入开始时间 (格式: HH:MM:SS 或 秒数)", "00:00:00", "确定", "取消")
    if button ~= "确定" then return end
    
    local button, duration = hs.dialog.textPrompt("持续时间", "请输入持续时间 (格式: HH:MM:SS 或 秒数)", "00:01:00", "确定", "取消")
    if button ~= "确定" then return end
    
    local outputFile = selectSaveLocation("cut_video.mp4")
    if not outputFile then return end
    
    -- 构建ffmpeg命令
    local cmd = string.format('ffmpeg -i "%s" -ss %s -t %s -c copy "%s"', 
        inputFile, startTime, duration, outputFile)
    
    hs.alert.show("正在切割视频...")
    
    -- 执行命令
    local task = hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            hs.alert.show("视频切割完成!")
            -- 在Finder中显示文件
            hs.execute(string.format('open -R "%s"', outputFile))
        else
            hs.alert.show("视频切割失败: " .. (stdErr or "未知错误"))
        end
    end, {"-c", cmd})
    
    task:start()
end

-- 视频格式转换
local function convertVideo()
    if not checkFFmpeg() then return end
    
    local inputFile = selectFile("选择要转换的视频文件")
    if not inputFile then return end
    
    -- 选择输出格式
    local formats = {
        {text = "MP4 (H.264)", format = "mp4", codec = "-c:v libx264 -c:a aac"},
        {text = "MOV (QuickTime)", format = "mov", codec = "-c:v libx264 -c:a aac"},
        {text = "AVI", format = "avi", codec = "-c:v libx264 -c:a mp3"},
        {text = "MKV", format = "mkv", codec = "-c:v libx264 -c:a aac"},
        {text = "WebM", format = "webm", codec = "-c:v libvpx-vp9 -c:a libopus"}
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        local outputFile = selectSaveLocation("converted_video." .. choice.format)
        if not outputFile then return end
        
        local cmd = string.format('ffmpeg -i "%s" %s "%s"', 
            inputFile, choice.codec, outputFile)
        
        hs.alert.show("正在转换视频格式...")
        
        local task = hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
            if exitCode == 0 then
                hs.alert.show("视频转换完成!")
                hs.execute(string.format('open -R "%s"', outputFile))
            else
                hs.alert.show("视频转换失败: " .. (stdErr or "未知错误"))
            end
        end, {"-c", cmd})
        
        task:start()
    end)
    
    chooser:choices(formats)
    chooser:show()
end

-- 音频提取
local function extractAudio()
    if not checkFFmpeg() then return end
    
    local inputFile = selectFile("选择视频文件")
    if not inputFile then return end
    
    local outputFile = selectSaveLocation("extracted_audio.mp3")
    if not outputFile then return end
    
    local cmd = string.format('ffmpeg -i "%s" -vn -acodec mp3 "%s"', 
        inputFile, outputFile)
    
    hs.alert.show("正在提取音频...")
    
    local task = hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
        if exitCode == 0 then
            hs.alert.show("音频提取完成!")
            hs.execute(string.format('open -R "%s"', outputFile))
        else
            hs.alert.show("音频提取失败: " .. (stdErr or "未知错误"))
        end
    end, {"-c", cmd})
    
    task:start()
end

-- 音频格式转换
local function convertAudio()
    if not checkFFmpeg() then return end
    
    local inputFile = selectFile("选择音频文件")
    if not inputFile then return end
    
    local formats = {
        {text = "MP3", format = "mp3", codec = "-acodec mp3"},
        {text = "AAC", format = "aac", codec = "-acodec aac"},
        {text = "WAV", format = "wav", codec = "-acodec pcm_s16le"},
        {text = "FLAC", format = "flac", codec = "-acodec flac"},
        {text = "OGG", format = "ogg", codec = "-acodec libvorbis"}
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        local outputFile = selectSaveLocation("converted_audio." .. choice.format)
        if not outputFile then return end
        
        local cmd = string.format('ffmpeg -i "%s" %s "%s"', 
            inputFile, choice.codec, outputFile)
        
        hs.alert.show("正在转换音频格式...")
        
        local task = hs.task.new("/bin/bash", function(exitCode, stdOut, stdErr)
            if exitCode == 0 then
                hs.alert.show("音频转换完成!")
                hs.execute(string.format('open -R "%s"', outputFile))
            else
                hs.alert.show("音频转换失败: " .. (stdErr or "未知错误"))
            end
        end, {"-c", cmd})
        
        task:start()
    end)
    
    chooser:choices(formats)
    chooser:show()
end

-- 显示媒体处理菜单
local function showMediaMenu()
    local menuItems = {
        {
            text = "🎬 切割视频",
            subText = "将视频切成两部分或提取片段",
            action = cutVideo
        },
        {
            text = "🔄 转换视频格式",
            subText = "转换视频到不同格式 (MP4, MOV, AVI等)",
            action = convertVideo
        },
        {
            text = "🎵 提取音频",
            subText = "从视频中提取音频文件",
            action = extractAudio
        },
        {
            text = "🎶 转换音频格式",
            subText = "转换音频到不同格式 (MP3, AAC, WAV等)",
            action = convertAudio
        }
    }
    
    local chooser = hs.chooser.new(function(choice)
        if choice and choice.action then
            choice.action()
        end
    end)
    
    chooser:choices(menuItems)
    chooser:placeholderText("选择媒体处理功能...")
    chooser:searchSubText(true)
    chooser:show()
end

-- 初始化模块
function mediaProcessor.init()
    -- 绑定快捷键 Opt+Cmd+M
    hs.hotkey.bind({"alt", "cmd"}, "m", function()
        showMediaMenu()
    end)
    
    print("✅ 媒体处理模块初始化成功 (Opt+Cmd+M)")
end

return mediaProcessor