import pyautogui
import time
import os
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def find_and_click(image_path, confidence=0.8, is_retina=True):
    print(f"正在屏幕上寻找: {image_path}...")

    if not os.path.exists(image_path):
        print(f"错误: 找不到截图文件 {image_path}")
        return False

    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)

        if location is not None:
            x, y = location.x, location.y
            print(f"成功找到图标，原始屏幕坐标: ({x}, {y})")

            if is_retina:
                x, y = x / 2, y / 2
                print(f"Retina 屏幕调整后坐标: ({x}, {y})")

            # 调试：先移动，等待确认
            print(f"[调试] 准备移动鼠标到 ({x}, {y})...")
            pyautogui.moveTo(x, y, duration=1)
            print(f"[调试] 当前鼠标位置: {pyautogui.position()}")

            input("[调试] 鼠标已移动，按回车继续点击...")
            pyautogui.click()
            print("=> 点击完成！")
            return True
        else:
            print("未找到图标")
            return False

    except Exception as e:
        print(f"发生错误: {e}")
        return False

def paste_text(text):
    pyperclip.copy(text)
    time.sleep(0.5)
    pyautogui.hotkey('command', 'v')
    time.sleep(0.5)

def search_and_send(name, msg):
    print(f"准备唤出搜索框并查找: {name}...")
    input("[调试] 请确保微信在最前面，按回车继续...")
    pyautogui.hotkey('command', 'f')
    time.sleep(1)

    paste_text(name)
    print("等待微信搜索结果加载...")
    time.sleep(2)

    input("[调试] 搜索结果已加载，按回车进入聊天窗口...")
    pyautogui.press('enter')
    print("进入聊天窗口...")
    time.sleep(1.5)

    print(f"准备发送消息: {msg}...")
    paste_text(msg)
    input("[调试] 消息已输入，按回车发送...")
    pyautogui.press('enter')
    print("=> 消息发送完毕！")

if __name__ == "__main__":
    print("====== 调试版 Mac RPA ======")
    print("请准备好包含【微信图标】的界面。3秒后开始扫描...")
    time.sleep(3)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_image = os.path.join(current_dir, 'wechat_icon.png')

    success = find_and_click(target_image, confidence=0.8, is_retina=True)

    if success:
        print("微信已激活，1秒后开始执行搜索和发送...")
        time.sleep(1)
        search_and_send("刘燕", "燕我明天中午不吃。")
