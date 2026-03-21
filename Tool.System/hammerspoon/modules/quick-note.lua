-- 快速记笔记模块
-- 提供快速创建和保存笔记的功能

local quickNote = {}
local config = require("config.settings").quickNote

-- 确保笔记目录存在
local function ensureNotesDirectory()
    local cmd = string.format("mkdir -p '%s'", config.notesPath)
    os.execute(cmd)
end

-- 获取当前日期时间字符串
local function getCurrentDateTime()
    return os.date("%Y-%m-%d %H:%M:%S")
end

-- 获取当前日期字符串（用于文件名）
local function getCurrentDate()
    return os.date("%Y-%m-%d")
end

-- 显示分类选择器
local function showCategoryChooser(callback)
    local choices = {}
    for _, category in ipairs(config.categories) do
        table.insert(choices, {
            text = category,
            subText = "选择 " .. category .. " 分类",
            category = category
        })
    end
    
    local chooser = hs.chooser.new(function(choice)
        if choice and callback then
            callback(choice.category)
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择笔记分类...")
    chooser:show()
end

-- 显示笔记输入对话框
local function showNoteInput(category)
    local clipboardContent = hs.pasteboard.getContents() or ""
    local defaultText = clipboardContent ~= "" and clipboardContent or ""
    
    -- 创建用户内容控制器来处理 JavaScript 消息
    local userContentController = hs.webview.usercontent.new("noteHandler")
    
    -- 使用 webview 创建多行文本输入框
    local webview = hs.webview.new({x=0, y=0, w=600, h=400}, {}, userContentController)
    
    userContentController:setCallback(function(message)
        print("🔍 收到JavaScript消息:")
        print("消息类型: " .. tostring(message.action))
        if message.content then
            print("消息内容长度: " .. tostring(#message.content))
            print("消息内容预览: " .. tostring(message.content):sub(1, 50) .. "...")
        end
        
        if message.action == "save" then
            local content = message.content
            if content and content ~= "" then
                print("✅ 调用保存函数")
                quickNote.saveNote(category, content)
            else
                print("❌ 内容为空，不保存")
            end
        elseif message.action == "cancel" then
            print("✅ 用户取消操作")
        end
        
        -- 关闭 webview
        if webview then
            webview:delete()
        end
    end)
    webview:windowTitle("快速记笔记 - " .. category)
    webview:windowStyle("utility")
    webview:allowTextEntry(true)
    webview:closeOnEscape(true)
    
    local html = [[
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            color: #333;
        }
        textarea {
            width: 100%;
            height: 200px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            box-sizing: border-box;
        }
        .buttons {
            margin-top: 15px;
            text-align: right;
        }
        button {
            padding: 8px 16px;
            margin-left: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .save-btn {
            background-color: #007AFF;
            color: white;
        }
        .cancel-btn {
            background-color: #f0f0f0;
            color: #333;
        }
        button:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>请输入笔记内容</h2>
        <textarea id="noteContent" placeholder="在此输入笔记内容..." autofocus>]] .. defaultText .. [[</textarea>
        <div class="buttons">
            <button class="cancel-btn" onclick="cancel()">取消</button>
            <button class="save-btn" onclick="save()">保存</button>
        </div>
    </div>
    
    <script>
        function save() {
            var content = document.getElementById('noteContent').value;
            if (content.trim() !== '') {
                window.webkit.messageHandlers.noteHandler.postMessage({
                    action: 'save',
                    content: content
                });
            } else {
                alert('请输入笔记内容');
            }
        }
        
        function cancel() {
            window.webkit.messageHandlers.noteHandler.postMessage({
                action: 'cancel'
            });
        }
        
        // 支持 Cmd+Enter 快速保存
        document.addEventListener('keydown', function(e) {
            if (e.metaKey && e.key === 'Enter') {
                save();
            }
        });
        
        // 自动聚焦到文本框
        document.getElementById('noteContent').focus();
    </script>
</body>
</html>
    ]]
    
    webview:html(html)
    webview:show()
    webview:centerOnScreen()
end

-- 保存笔记到文件
function quickNote.saveNote(category, content)
    print("🔍 开始保存笔记...")
    print("分类: " .. tostring(category))
    print("内容长度: " .. tostring(content and #content or 0))
    
    ensureNotesDirectory()
    
    local currentDate = getCurrentDate()
    local currentDateTime = getCurrentDateTime()
    local fileName = string.format("%s_%s.md", currentDate, category)
    local filePath = config.notesPath .. fileName
    
    print("文件路径: " .. filePath)
    
    -- 准备笔记内容
    local noteContent = string.format("## %s\n\n%s\n\n---\n\n", currentDateTime, content)
    
    print("准备写入内容: " .. noteContent:sub(1, 100) .. "...")
    
    -- 检查文件是否存在，如果存在则追加内容
    local file = io.open(filePath, "a")
    if file then
        local success, err = pcall(function()
            file:write(noteContent)
            file:close()
        end)
        
        if success then
            hs.alert.show(string.format("笔记已保存到: %s", fileName))
            print(string.format("📝 笔记已保存: %s - %s", category, content:sub(1, 50) .. (content:len() > 50 and "..." or "")))
        else
            hs.alert.show("写入文件时出错: " .. tostring(err))
            print("❌ 写入文件时出错: " .. tostring(err))
        end
    else
        hs.alert.show("无法打开文件: " .. filePath)
        print("❌ 无法打开文件: " .. filePath)
    end
end

-- 快速记笔记（使用默认分类）
local function quickNoteWithDefaultCategory()
    showNoteInput(config.defaultCategory)
end

-- 打开笔记目录
local function openNotesDirectory()
    os.execute(string.format("open '%s'", config.notesPath))
end

-- 获取所有笔记文件
local function getAllNotes()
    local notes = {}
    local cmd = string.format("find '%s' -name '*.md' -type f | sort -r", config.notesPath)
    local handle = io.popen(cmd)
    
    if handle then
        for line in handle:lines() do
            local fileName = line:match(".*/(.+)$")
            if fileName then
                local date, category = fileName:match("(%d%d%d%d%-%d%d%-%d%d)_(.+)%.md$")
                if date and category then
                    table.insert(notes, {
                        fileName = fileName,
                        filePath = line,
                        date = date,
                        category = category,
                        displayText = string.format("%s - %s", date, category)
                    })
                end
            end
        end
        handle:close()
    end
    
    return notes
end

-- 显示笔记内容预览
local function previewNote(filePath)
    local file = io.open(filePath, "r")
    if file then
        local content = file:read("*a")
        file:close()
        
        -- 提取前200个字符作为预览
        local preview = content:sub(1, 200)
        if content:len() > 200 then
            preview = preview .. "..."
        end
        
        return preview
    end
    return "无法读取文件内容"
end

-- 显示笔记查看器
local function showNoteViewer()
    local notes = getAllNotes()
    
    if #notes == 0 then
        hs.alert.show("暂无笔记文件")
        return
    end
    
    local choices = {}
    for _, note in ipairs(notes) do
        local preview = previewNote(note.filePath)
        table.insert(choices, {
            text = note.displayText,
            subText = preview,
            filePath = note.filePath,
            fileName = note.fileName
        })
    end
    
    local chooser = hs.chooser.new(function(choice)
        if choice then
            -- 在默认编辑器中打开笔记文件
            os.execute(string.format("open '%s'", choice.filePath))
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("搜索或选择笔记文件...")
    chooser:searchSubText(true)  -- 允许搜索子文本（内容预览）
    chooser:show()
end

-- 显示笔记操作选择器
local function showNoteActions()
    local choices = {
        {
            text = "快速记笔记 (" .. config.defaultCategory .. ")",
            subText = "使用默认分类快速记录",
            action = "quick"
        },
        {
            text = "选择分类记笔记",
            subText = "选择分类后记录笔记",
            action = "category"
        },
        {
            text = "查看已保存的笔记",
            subText = "浏览和搜索已保存的笔记文件",
            action = "view"
        },
        {
            text = "打开笔记目录",
            subText = "在 Finder 中打开笔记文件夹",
            action = "open"
        }
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        if choice.action == "quick" then
            quickNoteWithDefaultCategory()
        elseif choice.action == "category" then
            showCategoryChooser(showNoteInput)
        elseif choice.action == "view" then
            showNoteViewer()
        elseif choice.action == "open" then
            openNotesDirectory()
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择笔记操作...")
    chooser:show()
end

-- 初始化快速记笔记模块
function quickNote.init()
    ensureNotesDirectory()
    
    -- 绑定快捷键
    hs.hotkey.bind(config.keybind[1], config.keybind[2], function()
        showNoteActions()
    end)
    
    print("✅ 快速记笔记模块已加载")
end

-- 获取笔记统计信息
function quickNote.getStats()
    local cmd = string.format("find '%s' -name '*.md' | wc -l", config.notesPath)
    local handle = io.popen(cmd)
    local result = handle:read("*a")
    handle:close()
    
    return {
        notesPath = config.notesPath,
        totalFiles = tonumber(result:match("%d+")) or 0,
        categories = config.categories
    }
end

return quickNote