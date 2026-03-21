# 微信自动化教程

## 📋 功能说明

这个脚本可以自动化执行以下微信操作：
1. 激活微信窗口
2. 搜索指定联系人（如"面条"）
3. 发送指定消息（如"hello"）

## 🚀 快速开始

### 1. 安装依赖

**方法一：使用PowerShell脚本（推荐）**
```powershell
# 右键以管理员身份运行PowerShell，然后执行：
.\install_wechat_automation.ps1
```

**方法二：手动安装**
```bash
# 使用Anaconda环境安装
C:\Users\28919\anaconda3\Scripts\pip.exe install pyautogui pygetwindow pillow opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

### 2. 准备工作

1. **启动微信**：确保微信客户端已经启动并登录
2. **窗口可见**：微信窗口不要最小化
3. **联系人存在**：确保要搜索的联系人（如"面条"）在你的微信好友列表中

### 3. 运行脚本

```bash
# 使用Anaconda Python运行
C:\Users\28919\anaconda3\python.exe wechat_automation.py
```

## 📖 详细使用教程

### 基本用法

```python
from wechat_automation import WeChatAutomation

# 创建自动化实例
wechat_bot = WeChatAutomation()

# 发送消息给指定联系人
success = wechat_bot.auto_send_to_contact("面条", "hello")

if success:
    print("消息发送成功！")
else:
    print("消息发送失败！")
```

### 高级用法

```python
from wechat_automation import WeChatAutomation
import time

wechat_bot = WeChatAutomation()

# 分步执行操作
if wechat_bot.activate_wechat():
    time.sleep(1)
    
    if wechat_bot.search_contact("面条"):
        time.sleep(1)
        
        # 发送多条消息
        messages = ["hello", "你好", "最近怎么样？"]
        for msg in messages:
            wechat_bot.send_message(msg)
            time.sleep(2)  # 每条消息间隔2秒
```

## ⚙️ 配置说明

### 修改目标联系人和消息

编辑 `wechat_automation.py` 文件的 `main()` 函数：

```python
def main():
    wechat_bot = WeChatAutomation()
    
    # 修改这里的联系人和消息
    contact_name = "你的联系人名称"  # 改为你要发送的联系人
    message = "你的消息内容"       # 改为你要发送的消息
    
    # 其余代码保持不变...
```

### 调整操作间隔

如果你的电脑较慢，可以增加操作间隔：

```python
class WeChatAutomation:
    def __init__(self):
        pyautogui.PAUSE = 1.0  # 增加到1秒间隔
```

## 🛠️ 故障排除

### 常见问题

**1. 找不到微信窗口**
- 确保微信已启动
- 检查微信窗口标题是否为"微信"或"WeChat"
- 尝试重启微信

**2. 搜索功能不工作**
- 确保微信窗口处于活动状态
- 检查Ctrl+F快捷键是否被其他软件占用
- 手动测试Ctrl+F是否能打开微信搜索框

**3. 消息发送失败**
- 确保已选中正确的联系人
- 检查输入法状态（建议使用英文输入法）
- 确保聊天窗口已打开

**4. 脚本运行出错**
```bash
# 检查依赖是否正确安装
C:\Users\28919\anaconda3\Scripts\pip.exe list | findstr pyautogui
C:\Users\28919\anaconda3\Scripts\pip.exe list | findstr pygetwindow
```

### 调试模式

在脚本中添加调试信息：

```python
# 在操作前添加截图功能
import pyautogui

# 截图保存当前屏幕状态
pyautogui.screenshot('debug_screenshot.png')

# 打印窗口信息
import pygetwindow as gw
print("所有窗口:", [w.title for w in gw.getAllWindows()])
```

## 🔒 安全注意事项

1. **鼠标安全**：脚本设置了 `pyautogui.FAILSAFE = True`，将鼠标移到屏幕左上角可紧急停止

2. **操作间隔**：设置了适当的操作间隔，避免操作过快导致问题

3. **异常处理**：所有操作都包含异常处理，出错时会显示错误信息

4. **权限要求**：某些操作可能需要管理员权限

## 📝 自定义扩展

### 添加新功能

```python
class WeChatAutomation:
    def send_file(self, file_path: str) -> bool:
        """发送文件"""
        try:
            # 使用Ctrl+Shift+D打开文件发送对话框
            pyautogui.hotkey('ctrl', 'shift', 'd')
            time.sleep(1)
            
            # 输入文件路径
            pyautogui.typewrite(file_path)
            pyautogui.press('enter')
            
            return True
        except Exception as e:
            print(f"发送文件时出错: {e}")
            return False
    
    def send_emoji(self, emoji_name: str) -> bool:
        """发送表情"""
        try:
            # 打开表情面板
            pyautogui.hotkey('ctrl', 'shift', 'e')
            time.sleep(1)
            
            # 搜索表情
            pyautogui.typewrite(emoji_name)
            pyautogui.press('enter')
            
            return True
        except Exception as e:
            print(f"发送表情时出错: {e}")
            return False
```

### 批量操作

```python
def batch_send_messages():
    """批量发送消息给多个联系人"""
    wechat_bot = WeChatAutomation()
    
    contacts_and_messages = [
        ("面条", "hello"),
        ("朋友A", "你好"),
        ("朋友B", "最近怎么样？")
    ]
    
    for contact, message in contacts_and_messages:
        print(f"正在发送消息给 {contact}...")
        wechat_bot.auto_send_to_contact(contact, message)
        time.sleep(3)  # 每个联系人间隔3秒
```

## 📞 技术支持

如果遇到问题，请检查：
1. Python环境是否正确
2. 依赖包是否安装完整
3. 微信版本是否兼容
4. 系统权限是否足够

---

**注意**：此脚本仅用于学习和个人使用，请遵守微信使用条款，不要用于垃圾信息发送或其他违规行为。