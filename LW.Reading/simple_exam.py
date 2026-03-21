#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版考试系统 - 命令行版本
基于《管理的实践》第23章内容
"""

import sqlite3
import json
import os
from datetime import datetime

class SimpleExamSystem:
    """简化版考试系统"""
    
    def __init__(self):
        self.db_path = "simple_exam.db"
        self.init_database()
        self.init_sample_data()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建题目表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question_type TEXT NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT,
                correct_answer TEXT NOT NULL,
                explanation TEXT
            )
        """)
        
        # 创建考试记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                category TEXT NOT NULL,
                score REAL NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                exam_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def init_sample_data(self):
        """初始化示例数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM questions")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # 添加示例题目
        questions = [
            # 员工激励分类题目
            {
                'category': '员工激励',
                'question_type': 'single',
                'question_text': '根据德鲁克的观点，企业应该关注员工的什么，而不是员工满意度？',
                'options': json.dumps(['A. 员工的薪资水平', 'B. 员工的责任感', 'C. 员工的工作环境', 'D. 员工的社交关系']),
                'correct_answer': 'B',
                'explanation': '德鲁克认为企业需要以追求绩效的内在自我动机取代外部施加的恐惧，唯一有效的方法是加强员工的责任感。'
            },
            {
                'category': '员工激励',
                'question_type': 'single',
                'question_text': '为什么说"满意"不是充分的工作动机？',
                'options': json.dumps(['A. 满意的员工会要求更高薪资', 'B. 满意只能算消极默许，企业需要员工心甘情愿投入工作', 'C. 满意的员工容易跳槽', 'D. 满意度无法准确衡量']),
                'correct_answer': 'B',
                'explanation': '满意并不是充分的工作动机，只能算消极默许。企业必须要求员工心甘情愿地投入工作，展现绩效。'
            },
            {
                'category': '员工激励',
                'question_type': 'multiple',
                'question_text': '德鲁克提到的员工满意度问题包括哪些方面？（多选）',
                'options': json.dumps(['A. 无法分辨满意是出于工作满足感还是漠不关心', 'B. 没有固定的衡量标准', 'C. 传统数据对员工毫无意义', 'D. 满意度调查问题设计不当']),
                'correct_answer': json.dumps(['A', 'B', 'C']),
                'explanation': '德鲁克指出了员工满意度概念的多个问题：无法分辨满意的真实原因、缺乏衡量标准、传统数据缺乏意义等。'
            },
            {
                'category': '员工激励',
                'question_type': 'single',
                'question_text': '企业关心满意度问题的根本原因是什么？',
                'options': json.dumps(['A. 提高员工福利待遇', 'B. 领悟到恐惧不再是员工的工作动机', 'C. 改善劳资关系', 'D. 符合现代管理理念']),
                'correct_answer': 'B',
                'explanation': '企业之所以关心满意度问题，是因为领悟到在工业社会中，恐惧不再是员工的工作动机。'
            },
            {
                'category': '员工激励',
                'question_type': 'fill',
                'question_text': '德鲁克认为，我们无法用______买到责任感。',
                'options': None,
                'correct_answer': '金钱',
                'explanation': '德鲁克明确指出：我们无法用金钱买到责任感。金钱上的奖赏和诱因当然很重要，但大半只会带来反效果。'
            },
            
            # 员工责任分类题目
            {
                'category': '员工责任',
                'question_type': 'single',
                'question_text': '造就负责任员工的四种方式不包括以下哪项？',
                'options': json.dumps(['A. 慎重安排员工职务', 'B. 设定高绩效标准', 'C. 提高员工薪资待遇', 'D. 提供员工参与机会']),
                'correct_answer': 'C',
                'explanation': '四种方式包括：慎重安排员工职务、设定高绩效标准、提供员工自我控制所需信息、提供参与机会培养管理者愿景。'
            },
            {
                'category': '员工责任',
                'question_type': 'multiple',
                'question_text': '德鲁克提到的培养负责任员工的方法包括哪些？（多选）',
                'options': json.dumps(['A. 职务安排要求员工承担更大责任', 'B. 设定高标准的绩效要求', 'C. 提供充分的信息', 'D. 让员工参与影响其工作的决策']),
                'correct_answer': json.dumps(['A', 'B', 'C', 'D']),
                'explanation': '四种方式都非常必要：慎重安排员工职务、设定高绩效标准、提供员工自我控制所需信息、提供参与机会培养管理者愿景。'
            },
            {
                'category': '员工责任',
                'question_type': 'single',
                'question_text': '关于员工想不想承担责任的问题，德鲁克的观点是什么？',
                'options': json.dumps(['A. 人们天生害怕承担责任', 'B. 人们都想承担责任', 'C. 员工想不想承担责任根本无关紧要', 'D. 需要通过培训改变员工态度']),
                'correct_answer': 'C',
                'explanation': '德鲁克认为员工想不想承担责任根本无关紧要，重要的是企业必须要求员工负起责任。'
            },
            {
                'category': '员工责任',
                'question_type': 'fill',
                'question_text': '德鲁克认为，只求过关就好，往往消磨员工的干劲；通过努力不懈和发挥能力，专注于达到______，总是能激发员工的干劲。',
                'options': None,
                'correct_answer': '最高要求',
                'explanation': '德鲁克强调要设定高要求的职务来激发员工干劲，而不是仅仅设定最低标准。'
            },
            {
                'category': '员工责任',
                'question_type': 'single',
                'question_text': '为什么企业不应该公布最低产出标准？',
                'options': json.dumps(['A. 会增加管理成本', 'B. 员工会认为这个标准代表常态', 'C. 容易泄露商业机密', 'D. 不利于绩效考核']),
                'correct_answer': 'B',
                'explanation': '企业甚至不应该公布最低标准，以免员工会认为这个标准代表常态，这样会误导员工。'
            },
            
            # 绩效管理分类题目
            {
                'category': '绩效管理',
                'question_type': 'single',
                'question_text': '最能激励员工改善工作绩效的方式是什么？',
                'options': json.dumps(['A. 提供丰厚的奖金', 'B. 分派高要求的职务', 'C. 改善工作环境', 'D. 增加休假时间']),
                'correct_answer': 'B',
                'explanation': '最能有效刺激员工改善工作绩效、带给他工作上自豪感与成就感的，莫过于分派他高要求的职务。'
            },
            {
                'category': '绩效管理',
                'question_type': 'multiple',
                'question_text': '管理者为了激励员工达成最高绩效，应该做到哪些？（多选）',
                'options': json.dumps(['A. 对自己工作提出高标准', 'B. 妥善安排工作进度', 'C. 维护设备状态', 'D. 增加员工福利']),
                'correct_answer': json.dumps(['A', 'B', 'C']),
                'explanation': '管理者必须对自己工作提出高标准，妥善安排工作进度，维护设备状态，这些都直接影响员工绩效。'
            },
            {
                'category': '绩效管理',
                'question_type': 'single',
                'question_text': '管理能力的第一个考验是什么？',
                'options': json.dumps(['A. 制定完善的规章制度', 'B. 让员工在干扰最小的情况下发挥最大效益', 'C. 建立良好的人际关系', 'D. 掌握先进的管理技术']),
                'correct_answer': 'B',
                'explanation': '管理能力的第一个考验，就是管理者是否有能力让员工在干扰最小的情况下，发挥工作最大的效益。'
            },
            {
                'category': '绩效管理',
                'question_type': 'fill',
                'question_text': '切萨皮克俄亥俄铁路公司员工重建工厂的例子说明了______的重要性。',
                'options': None,
                'correct_answer': '员工参与',
                'explanation': '这个例子展现了员工参与决策和规划的重要性，当员工能参与工作规划时，计划会更完善，绩效更高。'
            },
            {
                'category': '绩效管理',
                'question_type': 'single',
                'question_text': '最打击员工士气的情况是什么？',
                'options': json.dumps(['A. 工作任务过重', 'B. 薪资待遇偏低', 'C. 管理者瞎忙时让员工闲着无所事事', 'D. 工作环境恶劣']),
                'correct_answer': 'C',
                'explanation': '最打击员工士气的事情莫过于，管理者像无头苍蝇般瞎忙时，却让员工闲在那儿无所事事。'
            },
            {
                'category': '绩效管理',
                'question_type': 'multiple',
                'question_text': '员工要承担达到最高绩效的责任，需要具备哪些条件？（多选）',
                'options': json.dumps(['A. 拥有管理者的愿景', 'B. 获得充足的工作信息', 'C. 参与工作规划决策', 'D. 接受专业技能培训']),
                'correct_answer': json.dumps(['A', 'B', 'C']),
                'explanation': '只有当员工拥有管理者的愿景，获得充足信息，并能参与相关决策时，才会承担起达到最高绩效的责任。'
            }
        ]
        
        for q in questions:
            cursor.execute("""
                INSERT INTO questions (category, question_type, question_text, options, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (q['category'], q['question_type'], q['question_text'], 
                   q['options'], q['correct_answer'], q['explanation']))
        
        conn.commit()
        conn.close()
    
    def get_categories(self):
        """获取所有分类"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM questions ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def get_questions_by_category(self, category):
        """根据分类获取题目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question_type, question_text, options, correct_answer, explanation
            FROM questions WHERE category = ? ORDER BY id
        """, (category,))
        
        questions = []
        for row in cursor.fetchall():
            questions.append({
                'id': row[0],
                'question_type': row[1],
                'question_text': row[2],
                'options': json.loads(row[3]) if row[3] else None,
                'correct_answer': json.loads(row[4]) if row[1] == 'multiple' else row[4],
                'explanation': row[5]
            })
        
        conn.close()
        return questions
    
    def save_exam_record(self, student_name, category, score, total_questions, correct_answers):
        """保存考试记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exam_records (student_name, category, score, total_questions, correct_answers)
            VALUES (?, ?, ?, ?, ?)
        """, (student_name, category, score, total_questions, correct_answers))
        conn.commit()
        conn.close()
    
    def start_exam(self):
        """开始考试"""
        print("\n" + "="*50)
        print("欢迎使用考试系统 - 管理的实践")
        print("="*50)
        
        # 输入学生姓名
        student_name = input("\n请输入您的姓名: ").strip()
        if not student_name:
            print("姓名不能为空！")
            return
        
        # 选择分类
        categories = self.get_categories()
        print("\n可选择的考试分类:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        try:
            choice = int(input("\n请选择分类编号: ")) - 1
            if choice < 0 or choice >= len(categories):
                print("无效的选择！")
                return
            selected_category = categories[choice]
        except ValueError:
            print("请输入有效的数字！")
            return
        
        # 获取题目
        questions = self.get_questions_by_category(selected_category)
        if not questions:
            print("该分类下没有题目！")
            return
        
        print(f"\n开始考试: {selected_category}")
        print(f"总题数: {len(questions)}")
        print("-" * 50)
        
        # 开始答题
        user_answers = {}
        for i, question in enumerate(questions, 1):
            print(f"\n第 {i} 题:")
            print(question['question_text'])
            
            if question['question_type'] == 'single':
                # 单选题
                for option in question['options']:
                    print(f"  {option}")
                answer = input("请选择答案 (A/B/C/D): ").strip().upper()
                user_answers[question['id']] = answer
                
            elif question['question_type'] == 'multiple':
                # 多选题
                for option in question['options']:
                    print(f"  {option}")
                answer = input("请选择答案 (如: A,C): ").strip().upper()
                user_answers[question['id']] = [x.strip() for x in answer.split(',') if x.strip()]
                
            elif question['question_type'] == 'fill':
                # 填空题
                answer = input("请填写答案: ").strip()
                user_answers[question['id']] = answer
        
        # 计算得分
        self.calculate_score(questions, user_answers, student_name, selected_category)
    
    def calculate_score(self, questions, user_answers, student_name, category):
        """计算得分并显示结果"""
        correct_count = 0
        total_count = len(questions)
        
        print("\n" + "="*50)
        print("考试结果")
        print("="*50)
        
        for i, question in enumerate(questions, 1):
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
            
            status = "✓" if is_correct else "✗"
            print(f"\n第 {i} 题: {status}")
            print(f"题目: {question['question_text']}")
            print(f"您的答案: {user_answer}")
            print(f"正确答案: {correct_answer}")
            if question['explanation']:
                print(f"解析: {question['explanation']}")
        
        score = (correct_count / total_count) * 100
        
        print("\n" + "-"*50)
        print(f"学生: {student_name}")
        print(f"分类: {category}")
        print(f"得分: {score:.1f}分")
        print(f"正确题数: {correct_count}/{total_count}")
        
        # 保存记录
        self.save_exam_record(student_name, category, score, total_count, correct_count)
        print("\n考试记录已保存！")
    
    def show_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "="*30)
            print("考试系统主菜单")
            print("="*30)
            print("1. 开始考试")
            print("2. 查看题目统计")
            print("3. 退出系统")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == '1':
                self.start_exam()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                print("感谢使用考试系统！")
                break
            else:
                print("无效的选择，请重新输入！")
    
    def show_statistics(self):
        """显示题目统计"""
        categories = self.get_categories()
        print("\n题目统计:")
        print("-" * 30)
        
        for category in categories:
            questions = self.get_questions_by_category(category)
            single_count = sum(1 for q in questions if q['question_type'] == 'single')
            multiple_count = sum(1 for q in questions if q['question_type'] == 'multiple')
            fill_count = sum(1 for q in questions if q['question_type'] == 'fill')
            
            print(f"\n{category}:")
            print(f"  总题数: {len(questions)}")
            print(f"  单选题: {single_count}")
            print(f"  多选题: {multiple_count}")
            print(f"  填空题: {fill_count}")

def main():
    """主函数"""
    try:
        exam_system = SimpleExamSystem()
        exam_system.show_menu()
    except KeyboardInterrupt:
        print("\n\n程序已退出！")
    except Exception as e:
        print(f"\n程序运行出错: {e}")

if __name__ == "__main__":
    main()