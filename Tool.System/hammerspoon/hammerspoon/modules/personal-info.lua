-- 个人信息快速粘贴模块
-- 提供快速输入个人信息的功能

local personalInfo = {}
local config = require("config.settings").personalInfo

-- 个人信息数据
local infoData = {
    phone = config.phone,
    email = config.email,
    address = config.address,
    companyName = config.companyName,
    taxId = config.taxId,
    companyEmail = config.companyEmail,
    idCard = config.idCard
}

-- 显示个人信息选择器
local function showPersonalInfoChooser()
    local choices = {
        {
            text = "手机号: " .. infoData.phone,
            subText = "点击直接输入电话号码到当前光标位置",
            type = "phone"
        },
        {
            text = "个人邮箱: " .. infoData.email,
            subText = "点击直接输入邮箱地址到当前光标位置",
            type = "email"
        },
        {
            text = "地址: " .. infoData.address,
            subText = "点击直接输入地址到当前光标位置",
            type = "address"
        },
        {
            text = "公司名称: " .. infoData.companyName,
            subText = "点击直接输入公司名称到当前光标位置",
            type = "companyName"
        },
        {
            text = "纳税人识别号: " .. infoData.taxId,
            subText = "点击直接输入纳税人识别号到当前光标位置",
            type = "taxId"
        },
        {
            text = "公司邮箱: " .. infoData.companyEmail,
            subText = "点击直接输入公司邮箱到当前光标位置",
            type = "companyEmail"
        },
        {
            text = "身份证: " .. infoData.idCard,
            subText = "点击直接输入身份证到当前光标位置",
            type = "idCard"
        },
        {
            text = "完整信息",
            subText = "直接输入所有个人信息到当前光标位置",
            type = "all"
        }
    }
    
    local chooser = hs.chooser.new(function(choice)
        if not choice then return end
        
        local content = ""
        if choice.type == "phone" then
            content = infoData.phone
        elseif choice.type == "email" then
            content = infoData.email
        elseif choice.type == "address" then
            content = infoData.address
        elseif choice.type == "companyName" then
            content = infoData.companyName
        elseif choice.type == "taxId" then
            content = infoData.taxId
        elseif choice.type == "companyEmail" then
            content = infoData.companyEmail
        elseif choice.type == "idCard" then
            content = infoData.idCard
        elseif choice.type == "all" then
            content = string.format("手机号: %s\n个人邮箱: %s\n地址: %s\n公司名称: %s\n纳税人识别号: %s\n公司邮箱: %s\n身份证: %s", 
                infoData.phone, infoData.email, infoData.address, infoData.companyName, infoData.taxId, infoData.companyEmail, infoData.idCard)
        end
        
        if content ~= "" then
            -- 直接输入文本到当前光标位置
            hs.eventtap.keyStrokes(content)
            hs.alert.show("已输入: " .. choice.text:match("^[^:]+"))
        end
    end)
    
    chooser:choices(choices)
    chooser:placeholderText("选择要输入的个人信息...")
    chooser:show()
end

-- 初始化个人信息模块
function personalInfo.init()
    -- 绑定快捷键
    hs.hotkey.bind({"alt", "cmd"}, "p", function()
        showPersonalInfoChooser()
    end)
    print("✅ 个人信息模块已加载，快捷键: Opt+Cmd+P")
end

-- 导出显示选择器函数供外部调用
function personalInfo.showChooser()
    showPersonalInfoChooser()
end

-- 更新个人信息
function personalInfo.updateInfo(newInfo)
    for key, value in pairs(newInfo) do
        if infoData[key] then
            infoData[key] = value
        end
    end
end

-- 获取个人信息
function personalInfo.getInfo()
    return infoData
end

-- 显示个人信息选择器（供外部调用）
function personalInfo.showChooser()
    showPersonalInfoChooser()
end

return personalInfo