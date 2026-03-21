#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理重复的钢琴教程
删除重复的陈俊宇和宋大叔教程，保留编号较小的版本
"""

import os
import shutil
from pathlib import Path

# 基础路径
BASE_PATH = "/Volumes/video/教程/钢琴教程专区"
THEORY_PATH = os.path.join(BASE_PATH, "🎓 乐理基础")

# 需要删除的重复教程（保留编号较小的版本）
DUPLICATE_TUTORIALS = [
    # 陈俊宇重复教程 - 删除无编号版本，保留【02】版本
    "23 陈俊宇《钢琴乐理的秘密》",
    
    # 宋大叔重复教程 - 删除无编号版本，保留【01】版本  
    "宋大叔教音乐最新全集"
]

def simulate_cleanup():
    """模拟清理重复教程"""
    print("=== 清理重复钢琴教程 - 模拟模式 ===")
    print(f"检查目录: {THEORY_PATH}")
    print()
    
    deleted_count = 0
    
    for tutorial_name in DUPLICATE_TUTORIALS:
        tutorial_path = os.path.join(THEORY_PATH, tutorial_name)
        
        if os.path.exists(tutorial_path):
            print(f"[模拟] 删除重复教程: {tutorial_name}")
            deleted_count += 1
        else:
            print(f"[跳过] 未找到: {tutorial_name}")
        print()
    
    print(f"模拟结果: 将删除 {deleted_count} 个重复教程")
    print()
    
    # 显示保留的教程
    print("保留的教程:")
    kept_tutorials = [
        "【01】.《宋大叔教音乐最新全集》←【第一最先看！！基础乐理、音基非常重要！】",
        "【02】.陈俊宇《钢琴乐理的秘密》"
    ]
    
    for tutorial in kept_tutorials:
        tutorial_path = os.path.join(THEORY_PATH, tutorial)
        if os.path.exists(tutorial_path):
            print(f"  ✓ {tutorial}")
        else:
            print(f"  ✗ {tutorial} (未找到)")
    print()

def execute_cleanup():
    """执行实际的清理"""
    print("=== 清理重复钢琴教程 - 执行模式 ===")
    print(f"检查目录: {THEORY_PATH}")
    print()
    
    deleted_count = 0
    
    for tutorial_name in DUPLICATE_TUTORIALS:
        tutorial_path = os.path.join(THEORY_PATH, tutorial_name)
        
        if os.path.exists(tutorial_path):
            print(f"[执行] 删除重复教程: {tutorial_name}")
            
            # 删除目录及其内容
            shutil.rmtree(tutorial_path)
            deleted_count += 1
            print(f"  已删除: {tutorial_path}")
        else:
            print(f"[跳过] 未找到: {tutorial_name}")
        print()
    
    print(f"执行结果: 成功删除 {deleted_count} 个重复教程")
    print()
    
    # 验证保留的教程
    print("验证保留的教程:")
    kept_tutorials = [
        "【01】.《宋大叔教音乐最新全集》←【第一最先看！！基础乐理、音基非常重要！】",
        "【02】.陈俊宇《钢琴乐理的秘密》"
    ]
    
    for tutorial in kept_tutorials:
        tutorial_path = os.path.join(THEORY_PATH, tutorial)
        if os.path.exists(tutorial_path):
            print(f"  ✓ {tutorial}")
        else:
            print(f"  ✗ {tutorial} (未找到)")
    print()

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        execute_cleanup()
    else:
        simulate_cleanup()
        print("要执行实际删除，请运行: python remove_duplicate_tutorials.py --execute")
        print("警告: 删除操作不可逆，请确认后再执行！")

if __name__ == "__main__":
    main()