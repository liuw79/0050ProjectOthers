#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动化 - 快速启动脚本
直接运行此脚本即可执行：激活微信 -> 搜索"面条" -> 发送"hello"
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from wechat_automation import WeChatAutomation
    import time
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请先运行安装脚本: install_wechat_automation.ps1")
    input("按回车键退出...")
    sys.exit(1)

def main():
    print("=" * 50)
    print("🤖 微信自动化脚本")
    print("功能：激活微信 -> 搜索联系人 -> 发送消息")
    print("=" * 50)
    
    # 获取用户输入
    print("\n📝 请输入发送信息：")
    contact_name = input("联系人名称 (默认: 面条): ").strip() or "面条"
    message = input("消息内容 (默认: hello): ").strip() or "hello"
    
    print(f"\n📋 操作配置:")
    print(f"   联系人: {contact_name}")
    print(f"   消息: {message}")
    
    # 确认执行
    confirm = input("\n确认执行吗？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes', '是', '确认']:
        print("操作已取消")
        return
    
    # 创建自动化实例
    try:
        wechat_bot = WeChatAutomation()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        input("按回车键退出...")
        return
    
    # 倒计时
    print("\n⏰ 5秒后开始执行，请确保微信已打开...")
    for i in range(5, 0, -1):
        print(f"   倒计时: {i}")
        time.sleep(1)
    
    print("\n🚀 开始执行自动化操作...")
    
    # 执行操作
    try:
        success = wechat_bot.auto_send_to_contact(contact_name, message)
        
        if success:
            print("\n✅ 操作成功完成！")
            print(f"已向 '{contact_name}' 发送消息: '{message}'")
        else:
            print("\n❌ 操作失败")
            print("请检查：")
            print("1. 微信是否已启动并登录")
            print("2. 联系人是否存在")
            print("3. 微信窗口是否可见")
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 执行过程中出错: {e}")
        print("\n🔧 故障排除建议：")
        print("1. 确保微信客户端已启动")
        print("2. 检查联系人名称是否正确")
        print("3. 尝试手动操作一次微信搜索功能")
        print("4. 重启微信客户端")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()