import pyautogui
import time
import os
import numpy as np
from rapidocr_onnxruntime import RapidOCR

def find_and_click(image_path, confidence=0.8, is_retina=True):
    """
    通过截图匹配找图并点击
    """
    print(f"正在屏幕上寻找: {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"错误: 找不到截图文件 {image_path}，请先截图并放到当前目录！")
        return False

    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location is not None:
            x, y = location.x, location.y
            if is_retina:
                x, y = x / 2, y / 2
            
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print("=> 点击完成，微信已激活！")
            return True
        else:
            print("未找到图标，可能是被遮挡或截图不准确。")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

def get_wechat_names():
    print("====== 微信会话名字抓取 ======")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_image = os.path.join(current_dir, 'wechat_icon.png')
    
    # 1. 自动激活微信窗口
    success = find_and_click(target_image, confidence=0.8, is_retina=True)
    if not success:
        print("无法激活微信，程序退出。")
        return
        
    time.sleep(1) # 等待微信窗口完全置前
    
    all_names = set()
    ocr = RapidOCR()
    ignore_texts = ['微信', '通讯录', '收藏', '聊天文件', '朋友圈', '搜一搜', '订阅号']
    screen_width, screen_height = pyautogui.size()
    region_width = min(600, screen_width // 3)

    # 循环滚动截取 2 屏
    for screen_idx in range(2):
        print(f"正在截取第 {screen_idx + 1} 屏并识别...")
        
        img = pyautogui.screenshot(region=(0, 0, region_width, screen_height))
        img_cv = np.array(img)[:, :, ::-1]
        
        result, _ = ocr(img_cv)
        
        if result is not None:
            for box, text, score in result:
                if score < 0.6: continue
                if len(text) < 2 or len(text) > 15: continue
                if ':' in text or '昨天' in text or '星期' in text or '/' in text: continue
                if any(ignore in text for ignore in ignore_texts): continue
                all_names.add(text)
                
        # 2. 滚动一屏 (这里模拟鼠标滚轮向下滚动，数值可能需要根据 Mac 实际情况微调)
        if screen_idx < 1:  # 如果不是最后一屏，则滚动
            print("向下滚动列表...")
            # 鼠标移动到列表区域中心
            pyautogui.moveTo(region_width // 2, screen_height // 2)
            # 在 Mac 上，pyautogui.scroll 的数值如果是负数表示向下滚动
            pyautogui.scroll(-20) 
            time.sleep(2) # 等待滚动完成和界面刷新

    print("\n✅ 抓取完成。汇总的文本如下：")
    print("-" * 30)
    for name in all_names:
        print(name)
    print("-" * 30)

if __name__ == "__main__":
    get_wechat_names()
