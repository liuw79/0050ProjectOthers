#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动化脚本 - 使用影刀RPA
功能：激活微信窗口，搜索联系人，发送消息

依赖：
- 影刀RPA软件
- pyautogui (用于屏幕操作)
- pygetwindow (用于窗口管理)
"""

import time
import pyautogui
import pygetwindow as gw
from typing import Optional

class WeChatAutomation:
    """微信自动化操作类"""
    
    def __init__(self):
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True  # 鼠标移到左上角停止
        pyautogui.PAUSE = 0.5      # 每次操作间隔0.5秒
        
    def find_wechat_window(self) -> Optional[object]:
        """查找微信窗口"""
        try:
            # 常见的微信窗口标题
            wechat_titles = ['微信', 'WeChat', 'WeChat for Windows']
            
            for title in wechat_titles:
                windows = gw.getWindowsWithTitle(title)
                if windows:
                    return windows[0]
            
            # 如果没找到，尝试模糊匹配
            all_windows = gw.getAllWindows()
            for window in all_windows:
                if '微信' in window.title or 'WeChat' in window.title:
                    return window
                    
            return None
        except Exception as e:
            print(f"查找微信窗口时出错: {e}")
            return None
    
    def activate_wechat(self) -> bool:
        """激活微信窗口"""
        try:
            wechat_window = self.find_wechat_window()
            if not wechat_window:
                print("未找到微信窗口，请确保微信已启动")
                return False
            
            # 激活窗口
            wechat_window.activate()
            time.sleep(1)
            
            # 如果窗口最小化，先恢复
            if wechat_window.isMinimized:
                wechat_window.restore()
                time.sleep(1)
            
            print(f"已激活微信窗口: {wechat_window.title}")
            return True
            
        except Exception as e:
            print(f"激活微信窗口时出错: {e}")
            return False
    
    def search_contact(self, contact_name: str) -> bool:
        """搜索联系人"""
        try:
            # 使用Ctrl+F打开搜索框
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # 清空搜索框并输入联系人名称
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.typewrite(contact_name)
            time.sleep(1)
            
            # 按回车确认搜索
            pyautogui.press('enter')
            time.sleep(1)
            
            print(f"已搜索联系人: {contact_name}")
            return True
            
        except Exception as e:
            print(f"搜索联系人时出错: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """发送消息"""
        try:
            # 输入消息
            pyautogui.typewrite(message)
            time.sleep(0.5)
            
            # 按回车发送
            pyautogui.press('enter')
            time.sleep(0.5)
            
            print(f"已发送消息: {message}")
            return True
            
        except Exception as e:
            print(f"发送消息时出错: {e}")
            return False
    
    def auto_send_to_contact(self, contact_name: str, message: str) -> bool:
        """自动发送消息给指定联系人"""
        print("开始微信自动化操作...")
        
        # 1. 激活微信窗口
        if not self.activate_wechat():
            return False
        
        # 2. 搜索联系人
        if not self.search_contact(contact_name):
            return False
        
        # 3. 发送消息
        if not self.send_message(message):
            return False
        
        print("微信自动化操作完成！")
        return True

def main():
    """主函数 - 演示用法"""
    # 创建自动化实例
    wechat_bot = WeChatAutomation()
    
    # 执行自动化操作
    contact_name = "面条"  # 要搜索的联系人
    message = "hello"     # 要发送的消息
    
    # 给用户5秒时间准备
    print("5秒后开始执行微信自动化操作...")
    for i in range(5, 0, -1):
        print(f"倒计时: {i}")
        time.sleep(1)
    
    # 执行操作
    success = wechat_bot.auto_send_to_contact(contact_name, message)
    
    if success:
        print("\n✅ 操作成功完成！")
    else:
        print("\n❌ 操作失败，请检查微信是否正常运行")

if __name__ == "__main__":
    main()