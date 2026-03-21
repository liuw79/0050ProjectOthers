#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整理拜厄教程目录中的非拜厄教程
将错误分类的教程移动到正确的专业分类目录
"""

import os
import shutil
from pathlib import Path

# 基础路径
BASE_PATH = "/Volumes/video/教程/钢琴教程专区"
BEYER_PATH = os.path.join(BASE_PATH, "📚 拜厄教程")

# 需要重新分类的教程映射
MISPLACED_TUTORIALS = {
    # 基础教程类
    "10 钢琴基础教程全套1-4 高清 价值888元--25.77GB": "🎓 乐理基础",
    "25 教你巧学钢琴-陆佳": "🎓 乐理基础", 
    "小贝零基础钢琴教学": "🎓 乐理基础"
}

def simulate_reorganization():
    """模拟重新整理过程"""
    print("=== 拜厄教程目录错误分类整理 - 模拟模式 ===")
    print(f"源目录: {BEYER_PATH}")
    print()
    
    moved_count = 0
    
    for tutorial_name, target_category in MISPLACED_TUTORIALS.items():
        source_path = os.path.join(BEYER_PATH, tutorial_name)
        target_path = os.path.join(BASE_PATH, target_category, tutorial_name)
        
        if os.path.exists(source_path):
            print(f"[模拟] 移动: {tutorial_name}")
            print(f"  从: {target_category}")
            print(f"  到: {target_category}")
            moved_count += 1
        else:
            print(f"[跳过] 未找到: {tutorial_name}")
        print()
    
    print(f"模拟结果: 将移动 {moved_count} 个教程")
    print()

def execute_reorganization():
    """执行实际的重新整理"""
    print("=== 拜厄教程目录错误分类整理 - 执行模式 ===")
    print(f"源目录: {BEYER_PATH}")
    print()
    
    moved_count = 0
    
    for tutorial_name, target_category in MISPLACED_TUTORIALS.items():
        source_path = os.path.join(BEYER_PATH, tutorial_name)
        target_dir = os.path.join(BASE_PATH, target_category)
        target_path = os.path.join(target_dir, tutorial_name)
        
        if os.path.exists(source_path):
            # 确保目标目录存在
            os.makedirs(target_dir, exist_ok=True)
            
            # 移动教程
            print(f"[执行] 移动: {tutorial_name}")
            print(f"  从: 📚 拜厄教程")
            print(f"  到: {target_category}")
            
            shutil.move(source_path, target_path)
            moved_count += 1
        else:
            print(f"[跳过] 未找到: {tutorial_name}")
        print()
    
    print(f"执行结果: 成功移动 {moved_count} 个教程")
    print()

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        execute_reorganization()
    else:
        simulate_reorganization()
        print("要执行实际移动，请运行: python reorganize_beyer_misplaced.py --execute")

if __name__ == "__main__":
    main()