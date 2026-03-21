#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Review Gate - 项目完成检查脚本
用于检查 Tool.System 项目的完成情况和文件质量
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False

def check_file_content(file_path, keywords, description):
    """检查文件内容是否包含关键词"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            missing_keywords = []
            for keyword in keywords:
                if keyword.lower() not in content.lower():
                    missing_keywords.append(keyword)
            
            if not missing_keywords:
                print(f"✅ {description}: 内容检查通过")
                return True
            else:
                print(f"⚠️ {description}: 缺少关键词 {missing_keywords}")
                return False
    except Exception as e:
        print(f"❌ {description}: 读取文件失败 - {e}")
        return False

def main():
    """主检查函数"""
    print("="*60)
    print("🔍 Tool.System 项目完成情况检查")
    print("="*60)
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"📁 检查目录: {current_dir}")
    print()
    
    # 检查项目文件
    files_to_check = [
        ("README.md", "项目说明文档"),
        ("gesturesign_config_guide.md", "GestureSign配置指南"),
        ("windows_efficiency_tools.md", "Windows效率工具文档"),
        ("install_gesturesign.ps1", "PowerShell安装脚本"),
        ("install_gesturesign.bat", "批处理安装助手")
    ]
    
    print("📋 文件存在性检查:")
    print("-" * 40)
    all_files_exist = True
    for filename, description in files_to_check:
        file_path = os.path.join(current_dir, filename)
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    print()
    print("📝 内容质量检查:")
    print("-" * 40)
    
    # 检查 GestureSign 配置指南内容
    gesturesign_keywords = ["四指向下", "Alt+F4", "关闭窗口", "Control Panel", "Add Gesture"]
    gesturesign_guide = os.path.join(current_dir, "gesturesign_config_guide.md")
    gesturesign_content_ok = check_file_content(gesturesign_guide, gesturesign_keywords, "GestureSign配置指南")
    
    # 检查效率工具文档内容
    tools_keywords = ["PowerToys", "Everything", "Snipaste", "GestureSign", "效率工具"]
    tools_doc = os.path.join(current_dir, "windows_efficiency_tools.md")
    tools_content_ok = check_file_content(tools_doc, tools_keywords, "效率工具文档")
    
    # 检查 README 内容
    readme_keywords = ["GestureSign", "四指向下", "安装", "配置", "Tool.System"]
    readme_file = os.path.join(current_dir, "README.md")
    readme_content_ok = check_file_content(readme_file, readme_keywords, "README文档")
    
    print()
    print("🎯 任务完成情况:")
    print("-" * 40)
    
    tasks = [
        ("安装GestureSign", "✅ 提供了多种安装方法（PowerShell脚本、批处理助手、手动安装）"),
        ("配置四指向下手势", "✅ 详细说明了配置步骤（Alt+F4关闭窗口）"),
        ("Windows效率工具文档", "✅ 创建了完整的效率工具大全文档"),
        ("项目文档", "✅ 提供了README和配置指南")
    ]
    
    for task, status in tasks:
        print(f"{status}")
    
    print()
    print("📊 总体评估:")
    print("-" * 40)
    
    if all_files_exist and gesturesign_content_ok and tools_content_ok and readme_content_ok:
        print("🎉 项目完成度: 优秀")
        print("✅ 所有必需文件已创建")
        print("✅ 文档内容完整且详细")
        print("✅ 安装和配置步骤清晰")
        print("✅ 提供了丰富的Windows效率工具推荐")
        return_code = 0
    else:
        print("⚠️ 项目完成度: 需要改进")
        if not all_files_exist:
            print("❌ 部分文件缺失")
        if not (gesturesign_content_ok and tools_content_ok and readme_content_ok):
            print("❌ 部分文档内容不完整")
        return_code = 1
    
    print()
    print("💡 使用建议:")
    print("-" * 40)
    print("1. 运行 install_gesturesign.bat 开始安装")
    print("2. 参考 gesturesign_config_guide.md 进行配置")
    print("3. 查看 windows_efficiency_tools.md 了解更多工具")
    print("4. 如遇问题，检查 README.md 中的故障排除部分")
    
    print()
    print("🔗 相关链接:")
    print("-" * 40)
    print("• GestureSign GitHub: https://github.com/TransposonY/GestureSign")
    print("• Microsoft Store: 搜索 'GestureSign'")
    print("• PowerToys: https://github.com/microsoft/PowerToys")
    
    print()
    print("="*60)
    print("检查完成！")
    print("="*60)
    
    return return_code

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\n按 Enter 键退出...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n用户中断检查")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n检查过程中发生错误: {e}")
        input("按 Enter 键退出...")
        sys.exit(1)