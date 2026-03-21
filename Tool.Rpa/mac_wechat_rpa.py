import pyautogui
import time
import os
import pyperclip

# 全局设置
# 鼠标移到屏幕四角时可以触发防故障中断
pyautogui.FAILSAFE = True
# 每个动作之间的停顿时间
pyautogui.PAUSE = 0.5

def find_and_click(image_path, confidence=0.8, is_retina=True):
    """
    通过截图匹配找图并点击
    :param image_path: 目标截图的路径 (比如微信图标的小图)
    :param confidence: 匹配置信度 (0-1)，越高越精确，需要安装 opencv-python
    :param is_retina: 如果你的 Mac 是视网膜屏幕，找到的坐标需要减半才能正确点击
    """
    print(f"正在屏幕上寻找: {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"错误: 找不到截图文件 {image_path}，请先截图并放到当前目录！")
        return False

    try:
        # 在屏幕上寻找中心点坐标
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        
        if location is not None:
            x, y = location.x, location.y
            print(f"成功找到图标，原始屏幕坐标: ({x}, {y})")
            
            # Mac Retina 屏幕的坐标映射问题：实际物理像素是逻辑像素的2倍
            if is_retina:
                x, y = x / 2, y / 2
                print(f"Retina 屏幕调整后坐标: ({x}, {y})")
            
            # 移动鼠标并点击
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print("=> 点击完成！")
            return True
        else:
            print("未找到图标，可能是被遮挡或截图不准确。")
            return False
            
    except Exception as e:
        print(f"发生错误: {e}")
        return False

def paste_text(text):
    """【处方】仅粘贴文本，不自动回车，分离动作以精确控制节奏"""
    pyperclip.copy(text)
    time.sleep(0.5)
    pyautogui.hotkey('command', 'v')  # Mac 的粘贴快捷键
    time.sleep(0.5)

def search_and_send(name, msg):
    print(f"准备唤出搜索框并查找: {name}...")
    pyautogui.hotkey('command', 'f')
    time.sleep(1)
    
    # 1. 粘贴名字，等待微信搜索结果出来
    paste_text(name)
    print("等待微信搜索结果加载...")
    time.sleep(2)  # 【关键调整】给微信充足的时间搜索并高亮第一个联系人
    
    # 2. 回车，进入聊天界面
    pyautogui.press('enter')
    print("进入聊天窗口...")
    time.sleep(1.5)  # 等待聊天窗口加载并自动聚焦输入框
    
    # 3. 粘贴消息并发送
    print(f"准备发送消息: {msg}...")
    paste_text(msg)
    pyautogui.press('enter')
    print("=> 消息发送完毕！")

if __name__ == "__main__":
    print("====== 极简 Mac RPA 测试 ======")
    print("请准备好包含【微信图标】的界面。3秒后开始扫描...")
    time.sleep(3)
    
    # 动态获取当前脚本所在目录，防止在别的路径运行找不到图
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_image = os.path.join(current_dir, 'wechat_icon.png')
    
    # 开始执行查找和点击
    success = find_and_click(target_image, confidence=0.8, is_retina=True)
    
    if success:
        print("微信已激活，1秒后开始执行搜索和发送...")
        time.sleep(1)
        search_and_send("刘燕", "燕我明天中午不吃。")
    else:
        print("提示: 请确认 wechat_icon.png 是否与屏幕上显示的微信图标完全一致。")
