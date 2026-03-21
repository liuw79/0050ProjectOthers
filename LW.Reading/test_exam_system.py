#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考试系统测试脚本
测试数据库功能和基本逻辑
"""

import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from exam_system import ExamDatabase, ExamSystem

def test_database():
    """测试数据库功能"""
    print("=== 测试数据库功能 ===")
    
    # 创建数据库实例
    db = ExamDatabase("test_exam.db")
    
    # 测试添加分类
    print("1. 测试添加分类...")
    cat1 = db.add_category("测试分类1", description="这是一个测试分类")
    cat2 = db.add_category("测试子分类", cat1, "这是一个子分类")
    print(f"   添加分类成功，ID: {cat1}, {cat2}")
    
    # 测试获取分类
    print("2. 测试获取分类...")
    categories = db.get_categories()
    for cat in categories:
        print(f"   分类: {cat['name']} (ID: {cat['id']}, 父ID: {cat['parent_id']})")
    
    # 测试添加题目
    print("3. 测试添加题目...")
    
    # 单选题
    q1 = db.add_question(
        cat2, "single",
        "这是一道测试单选题？",
        ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
        "B",
        "这是解析内容",
        2
    )
    
    # 多选题
    q2 = db.add_question(
        cat2, "multiple",
        "这是一道测试多选题？（多选）",
        ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
        ["A", "C"],
        "多选题解析",
        3
    )
    
    # 填空题
    q3 = db.add_question(
        cat2, "fill",
        "这是一道______题。",
        None,
        "填空",
        "填空题解析",
        1
    )
    
    print(f"   添加题目成功，ID: {q1}, {q2}, {q3}")
    
    # 测试获取题目
    print("4. 测试获取题目...")
    questions = db.get_questions_by_category(cat2)
    for q in questions:
        print(f"   题目: {q['question_text'][:20]}... (类型: {q['question_type']})")
    
    # 测试保存考试记录
    print("5. 测试保存考试记录...")
    start_time = datetime.now()
    end_time = datetime.now()
    answers = {q1: "B", q2: ["A", "C"], q3: "填空"}
    
    db.save_exam_record(
        "测试学生", cat2, 3, 3, 100.0,
        start_time, end_time, answers
    )
    print("   考试记录保存成功")
    
    print("数据库测试完成！\n")
    return db, cat2

def test_exam_system():
    """测试考试系统逻辑"""
    print("=== 测试考试系统逻辑 ===")
    
    # 创建考试系统实例
    exam_system = ExamSystem()
    
    # 测试获取分类
    print("1. 测试获取预置分类...")
    categories = exam_system.db.get_categories()
    for cat in categories:
        if cat['parent_id'] is not None:  # 只显示子分类
            print(f"   分类: {cat['name']} (ID: {cat['id']})")
            
            # 获取该分类下的题目
            questions = exam_system.db.get_questions_by_category(cat['id'])
            print(f"   题目数量: {len(questions)}")
            
            # 显示前2道题目
            for i, q in enumerate(questions[:2]):
                print(f"   题目{i+1}: {q['question_text'][:30]}...")
                print(f"          类型: {q['question_type']}, 难度: {q['difficulty']}")
    
    print("考试系统测试完成！\n")

def test_scoring():
    """测试评分功能"""
    print("=== 测试评分功能 ===")
    
    # 模拟题目和答案
    questions = [
        {
            'id': 1,
            'question_type': 'single',
            'question_text': '单选题测试',
            'correct_answer': 'B'
        },
        {
            'id': 2,
            'question_type': 'multiple',
            'question_text': '多选题测试',
            'correct_answer': ['A', 'C']
        },
        {
            'id': 3,
            'question_type': 'fill',
            'question_text': '填空题测试',
            'correct_answer': '正确答案'
        }
    ]
    
    # 模拟用户答案
    user_answers = {
        1: 'B',      # 正确
        2: ['A', 'C'], # 正确
        3: '正确答案'   # 正确
    }
    
    # 计算得分
    correct_count = 0
    for question in questions:
        question_id = question['id']
        user_answer = user_answers.get(question_id)
        correct_answer = question['correct_answer']
        
        is_correct = False
        if question['question_type'] == 'single':
            is_correct = user_answer == correct_answer
        elif question['question_type'] == 'multiple':
            is_correct = set(user_answer or []) == set(correct_answer)
        elif question['question_type'] == 'fill':
            is_correct = (user_answer or "").strip().lower() == correct_answer.lower()
        
        if is_correct:
            correct_count += 1
        
        print(f"题目{question_id}: {'✓' if is_correct else '✗'} {question['question_text']}")
        print(f"   用户答案: {user_answer}")
        print(f"   正确答案: {correct_answer}")
    
    score = (correct_count / len(questions)) * 100
    print(f"\n总得分: {score:.1f}分 ({correct_count}/{len(questions)})")
    print("评分功能测试完成！\n")

def main():
    """主测试函数"""
    print("考试系统功能测试")
    print("=" * 50)
    
    try:
        # 测试数据库功能
        test_database()
        
        # 测试考试系统
        test_exam_system()
        
        # 测试评分功能
        test_scoring()
        
        print("=" * 50)
        print("所有测试完成！系统功能正常。")
        
        # 清理测试数据库
        if os.path.exists("test_exam.db"):
            os.remove("test_exam.db")
            print("测试数据库已清理。")
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()