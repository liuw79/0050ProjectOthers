-- 剪贴板管理模块
-- 提供剪贴板历史记录、搜索、持久化等功能

local clipboard = {}
local config = require("config.settings").clipboard
local json = require("hs.json")

-- 全局变量
clipboardHistory = {}
clipboardWatcher = nil
local maxHistory = config.maxHistory
local historyFile = config.historyFile

-- 清理剪贴板内容（移除多余空白字符）
local function cleanClipboardContent(content)
    if not content then return "" end
    return content:gsub("^%s+", ""):gsub("%s+$", ""):gsub("%s+", " ")
end

-- 检查内容是否已存在于历史记录中
local function isContentExists(content)
    for _, item in ipairs(clipboardHistory) do
        if item.content == content then
            return true
        end
    end
    return false
end

-- 添加内容到剪贴板历史
local function addToClipboardHistory(content)
    if not content or content == "" then return end
    
    local cleanContent = cleanClipboardContent(content)
    if cleanContent == "" or isContentExists(cleanContent) then return end
    
    -- 添加新记录到历史开头
    table.insert(clipboardHistory, 1, {
        content = cleanContent,
        timestamp = os.time(),
        length = string.len(cleanContent)
    })
    
    -- 保持历史记录数量限制
    while #clipboardHistory > maxHistory do
        table.remove(clipboardHistory)
    end
    
    -- 保存到文件
    clipboard.saveHistory()
end

-- 加载历史记录
function clipboard.loadHistory()
    local file = io.open(historyFile, "r")
    if file then
        local content = file:read("*all")
        file:close()
        
        local success, data = pcall(json.decode, content)
        if success and data then
            clipboardHistory = data
        end
    end
end

-- 保存历史记录
function clipboard.saveHistory()
    if not config.enablePersistence then return end
    
    local file = io.open(historyFile, "w")
    if file then
        local success, jsonStr = pcall(json.encode, clipboardHistory)
        if success then
            file:write(jsonStr)
        end
        file:close()
    end
end

-- 显示剪贴板历史选择器
local function showClipboardHistory()
    if #clipboardHistory == 0 then
        hs.alert.show("剪贴板历史为空")
        return
    end
    
    local choices = {}
    for i, item in ipairs(clipboardHistory) do
        local preview = item.content
        if string.len(preview) > 100 then
            preview = string.sub(preview, 1, 100) .. "..."
        end
        
        local timeStr = os.date("%H:%M:%S", item.timestamp)
        
        table.insert(choices, {
            text = preview,
            subText = string.format("时间: %s | 长度: %d 字符", timeStr, item.length),
            index = i
        })
    end
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            hs.pasteboard.setContents(clipboardHistory[choice.index].content)
            hs.alert.show("已复制到剪贴板")
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("搜索剪贴板历史...")
    chooser:searchSubText(true)
    chooser:show()
end

-- 清空剪贴板历史
local function clearClipboardHistory()
    clipboardHistory = {}
    clipboard.saveHistory()
    hs.alert.show("剪贴板历史已清空")
end

-- 初始化剪贴板监听器
function clipboard.init()
    -- 加载历史记录
    clipboard.loadHistory()
    
    -- 获取当前剪贴板内容并添加到历史
    local currentContent = hs.pasteboard.getContents()
    if currentContent then
        addToClipboardHistory(currentContent)
    end
    
    -- 启动剪贴板监听器
    clipboardWatcher = hs.pasteboard.watcher.new(function()
        local newContent = hs.pasteboard.getContents()
        if newContent then
            addToClipboardHistory(newContent)
        end
    end)
    
    clipboardWatcher:start()
    
    -- 绑定快捷键
    hs.hotkey.bind(config.showKeybind, "v", function()
        showClipboardHistory()
    end)
    
    print("✅ 剪贴板管理模块已加载")
end

-- 停止剪贴板监听器
function clipboard.stop()
    if clipboardWatcher then
        clipboardWatcher:stop()
        clipboardWatcher = nil
    end
end

-- 获取历史记录统计信息
function clipboard.getStats()
    return {
        count = #clipboardHistory,
        maxHistory = maxHistory,
        oldestTimestamp = clipboardHistory[#clipboardHistory] and clipboardHistory[#clipboardHistory].timestamp or nil,
        newestTimestamp = clipboardHistory[1] and clipboardHistory[1].timestamp or nil
    }
end

-- 导出显示历史函数供调试使用
function clipboard.showHistory()
    showClipboardHistory()
end

return clipboard