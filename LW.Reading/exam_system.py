#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考试系统 - 基于《管理的实践》第23章内容
支持单选题、多选题、填空题等题目类型
使用SQLite数据库存储
按目录结构展示题目
自动评分功能
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ExamDatabase:
    """考试系统数据库管理类"""
    
    def __init__(self, db_path: str = "exam_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建题目分类表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                parent_id INTEGER,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        """)
        
        # 创建题目表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                question_type TEXT NOT NULL CHECK (question_type IN ('single', 'multiple', 'fill')),
                question_text TEXT NOT NULL,
                options TEXT, -- JSON格式存储选项
                correct_answer TEXT NOT NULL, -- JSON格式存储正确答案
                explanation TEXT,
                difficulty INTEGER DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        
        # 创建考试记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                score REAL NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                answers TEXT, -- JSON格式存储答案详情
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_category(self, name: str, parent_id: Optional[int] = None, description: str = ""):
        """添加题目分类"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO categories (name, parent_id, description) VALUES (?, ?, ?)",
            (name, parent_id, description)
        )
        
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return category_id
    
    def add_question(self, category_id: int, question_type: str, question_text: str,
                    options: List[str] = None, correct_answer: Any = None,
                    explanation: str = "", difficulty: int = 1):
        """添加题目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        options_json = json.dumps(options, ensure_ascii=False) if options else None
        answer_json = json.dumps(correct_answer, ensure_ascii=False)
        
        cursor.execute("""
            INSERT INTO questions (category_id, question_type, question_text, options, 
                                 correct_answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category_id, question_type, question_text, options_json, 
               answer_json, explanation, difficulty))
        
        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return question_id
    
    def get_categories(self) -> List[Dict]:
        """获取所有分类"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, parent_id, description 
            FROM categories 
            ORDER BY parent_id, name
        """)
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                'id': row[0],
                'name': row[1],
                'parent_id': row[2],
                'description': row[3]
            })
        
        conn.close()
        return categories
    
    def get_questions_by_category(self, category_id: int) -> List[Dict]:
        """根据分类获取题目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, question_type, question_text, options, correct_answer, 
                   explanation, difficulty
            FROM questions 
            WHERE category_id = ?
            ORDER BY id
        """, (category_id,))
        
        questions = []
        for row in cursor.fetchall():
            questions.append({
                'id': row[0],
                'question_type': row[1],
                'question_text': row[2],
                'options': json.loads(row[3]) if row[3] else None,
                'correct_answer': json.loads(row[4]),
                'explanation': row[5],
                'difficulty': row[6]
            })
        
        conn.close()
        return questions
    
    def save_exam_record(self, student_name: str, category_id: int, 
                        total_questions: int, correct_answers: int, 
                        score: float, start_time: datetime, end_time: datetime,
                        answers: Dict):
        """保存考试记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        answers_json = json.dumps(answers, ensure_ascii=False)
        
        cursor.execute("""
            INSERT INTO exam_records (student_name, category_id, total_questions, 
                                    correct_answers, score, start_time, end_time, answers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_name, category_id, total_questions, correct_answers, 
               score, start_time, end_time, answers_json))
        
        conn.commit()
        conn.close()

class ExamSystem:
    """考试系统主类"""
    
    def __init__(self):
        self.db = ExamDatabase()
        self.current_questions = []
        self.current_answers = {}
        self.start_time = None
        self.student_name = ""
        self.current_category_id = None
        
        # 初始化示例数据
        self.init_sample_data()
    
    def init_sample_data(self):
        """初始化示例题目数据"""
        # 检查是否已有数据
        categories = self.db.get_categories()
        if categories:
            return
        
        # 创建分类
        management_cat = self.db.add_category("管理的实践", description="德鲁克管理学经典")
        motivation_cat = self.db.add_category("员工激励", management_cat, "第23章：需要怎样的激励")
        responsibility_cat = self.db.add_category("员工责任", management_cat, "负责任的员工培养")
        performance_cat = self.db.add_category("绩效管理", management_cat, "高标准绩效要求")
        
        # 添加员工激励相关题目
        self.db.add_question(
            motivation_cat, "single",
            "根据德鲁克的观点，企业应该关注员工的什么，而不是员工满意度？",
            ["A. 员工的薪资水平", "B. 员工的责任感", "C. 员工的工作环境", "D. 员工的社交关系"],
            "B",
            "德鲁克认为企业需要以追求绩效的内在自我动机取代外部施加的恐惧，唯一有效的方法是加强员工的责任感。",
            2
        )
        
        self.db.add_question(
            motivation_cat, "single",
            "为什么说'满意'不是充分的工作动机？",
            ["A. 满意的员工会要求更高薪资", "B. 满意只能算消极默许，企业需要员工心甘情愿投入工作", 
             "C. 满意的员工容易跳槽", "D. 满意度无法准确衡量"],
            "B",
            "满意并不是充分的工作动机，只能算消极默许。企业必须要求员工心甘情愿地投入工作，展现绩效。",
            2
        )
        
        self.db.add_question(
            motivation_cat, "multiple",
            "德鲁克提到的员工满意度问题包括哪些方面？（多选）",
            ["A. 无法分辨满意是出于工作满足感还是漠不关心", 
             "B. 没有固定的衡量标准", 
             "C. 传统数据对员工毫无意义", 
             "D. 满意度调查问题设计不当"],
            ["A", "B", "C"],
            "德鲁克指出了员工满意度概念的多个问题：无法分辨满意的真实原因、缺乏衡量标准、传统数据缺乏意义等。",
            3
        )
        
        # 添加员工责任相关题目
        self.db.add_question(
            responsibility_cat, "single",
            "造就负责任员工的四种方式不包括以下哪项？",
            ["A. 慎重安排员工职务", "B. 设定高绩效标准", "C. 提高员工薪资待遇", "D. 提供员工参与机会"],
            "C",
            "四种方式包括：慎重安排员工职务、设定高绩效标准、提供员工自我控制所需信息、提供参与机会培养管理者愿景。",
            2
        )
        
        self.db.add_question(
            responsibility_cat, "single",
            "IBM取消通行标准让员工决定自己工作标准的做法说明了什么？",
            ["A. 员工比管理者更了解工作要求", "B. 最低标准会误导员工", 
             "C. 标准化管理已经过时", "D. 员工自主管理更有效"],
            "B",
            "一般员工的产出标准通常都是最低标准，会误导员工。IBM的成功显示应该为员工设定真正的工作目标。",
            3
        )
        
        # 添加绩效管理相关题目
        self.db.add_question(
            performance_cat, "single",
            "最能激励员工改善工作绩效的方式是什么？",
            ["A. 提供丰厚的奖金", "B. 分派高要求的职务", "C. 改善工作环境", "D. 增加休假时间"],
            "B",
            "最能有效刺激员工改善工作绩效、带给他工作上自豪感与成就感的，莫过于分派他高要求的职务。",
            2
        )
        
        self.db.add_question(
            performance_cat, "multiple",
            "管理者为了激励员工达成最高绩效，应该做到哪些？（多选）",
            ["A. 对自己的工作绩效提出高标准", "B. 妥善拟订进度让员工随时有事可做", 
             "C. 保持设备一流状态", "D. 减少对员工的工作要求"],
            ["A", "B", "C"],
            "管理者必须对自己工作提出高标准，妥善安排工作进度，维护设备状态，这些都直接影响员工绩效。",
            3
        )
        
        self.db.add_question(
            performance_cat, "fill",
            "切萨皮克俄亥俄铁路公司员工重建工厂的例子说明了______的重要性。",
            None,
            "员工参与",
            "这个例子展现了员工参与决策和规划的重要性，当员工能参与工作规划时，计划会更完善，绩效更高。",
            2
        )

class ExamGUI:
    """考试系统图形界面"""
    
    def __init__(self):
        self.exam_system = ExamSystem()
        self.root = tk.Tk()
        self.root.title("考试系统 - 管理的实践")
        self.root.geometry("800x600")
        
        self.current_question_index = 0
        self.question_widgets = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="管理的实践 - 考试系统", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 学生姓名输入
        ttk.Label(main_frame, text="学生姓名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=20)
        self.name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 分类选择
        ttk.Label(main_frame, text="选择考试分类:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, 
                                          width=30, state="readonly")
        self.category_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 加载分类数据
        self.load_categories()
        
        # 开始考试按钮
        self.start_button = ttk.Button(main_frame, text="开始考试", 
                                      command=self.start_exam)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # 考试区域（初始隐藏）
        self.exam_frame = ttk.Frame(main_frame)
        self.exam_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.exam_frame.grid_remove()
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def load_categories(self):
        """加载分类数据"""
        categories = self.exam_system.db.get_categories()
        category_options = []
        
        for cat in categories:
            if cat['parent_id'] is not None:  # 只显示子分类
                category_options.append(f"{cat['name']} (ID: {cat['id']})")
        
        self.category_combo['values'] = category_options
        if category_options:
            self.category_combo.set(category_options[0])
    
    def start_exam(self):
        """开始考试"""
        student_name = self.name_entry.get().strip()
        if not student_name:
            messagebox.showerror("错误", "请输入学生姓名")
            return
        
        category_text = self.category_var.get()
        if not category_text:
            messagebox.showerror("错误", "请选择考试分类")
            return
        
        # 提取分类ID
        category_id = int(category_text.split("ID: ")[1].split(")")[0])
        
        # 获取题目
        questions = self.exam_system.db.get_questions_by_category(category_id)
        if not questions:
            messagebox.showerror("错误", "该分类下没有题目")
            return
        
        # 初始化考试
        self.exam_system.student_name = student_name
        self.exam_system.current_category_id = category_id
        self.exam_system.current_questions = questions
        self.exam_system.current_answers = {}
        self.exam_system.start_time = datetime.now()
        
        # 显示考试界面
        self.show_exam_interface()
    
    def show_exam_interface(self):
        """显示考试界面"""
        # 隐藏开始界面元素
        for widget in self.root.winfo_children()[0].winfo_children()[:4]:
            widget.grid_remove()
        
        # 显示考试框架
        self.exam_frame.grid()
        
        # 创建考试界面
        self.create_exam_widgets()
    
    def create_exam_widgets(self):
        """创建考试界面组件"""
        # 清除现有组件
        for widget in self.exam_frame.winfo_children():
            widget.destroy()
        
        # 进度信息
        progress_frame = ttk.Frame(self.exam_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        total_questions = len(self.exam_system.current_questions)
        progress_text = f"题目进度: {self.current_question_index + 1} / {total_questions}"
        ttk.Label(progress_frame, text=progress_text, font=('Arial', 12)).pack(side=tk.LEFT)
        
        # 当前题目
        if self.current_question_index < total_questions:
            self.show_current_question()
        
        # 导航按钮
        nav_frame = ttk.Frame(self.exam_frame)
        nav_frame.pack(fill=tk.X, pady=(20, 0))
        
        if self.current_question_index > 0:
            ttk.Button(nav_frame, text="上一题", 
                      command=self.prev_question).pack(side=tk.LEFT, padx=(0, 10))
        
        if self.current_question_index < total_questions - 1:
            ttk.Button(nav_frame, text="下一题", 
                      command=self.next_question).pack(side=tk.LEFT)
        else:
            ttk.Button(nav_frame, text="提交考试", 
                      command=self.submit_exam).pack(side=tk.LEFT)
    
    def show_current_question(self):
        """显示当前题目"""
        question = self.exam_system.current_questions[self.current_question_index]
        
        # 题目框架
        question_frame = ttk.LabelFrame(self.exam_frame, text=f"第 {self.current_question_index + 1} 题", 
                                       padding="10")
        question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 题目文本
        question_text = scrolledtext.ScrolledText(question_frame, height=3, wrap=tk.WORD)
        question_text.pack(fill=tk.X, pady=(0, 10))
        question_text.insert(tk.END, question['question_text'])
        question_text.config(state=tk.DISABLED)
        
        # 答案区域
        answer_frame = ttk.Frame(question_frame)
        answer_frame.pack(fill=tk.BOTH, expand=True)
        
        question_id = question['id']
        
        if question['question_type'] == 'single':
            # 单选题
            self.answer_var = tk.StringVar()
            if question_id in self.exam_system.current_answers:
                self.answer_var.set(self.exam_system.current_answers[question_id])
            
            for option in question['options']:
                option_value = option.split('.')[0].strip()
                ttk.Radiobutton(answer_frame, text=option, variable=self.answer_var, 
                               value=option_value).pack(anchor=tk.W, pady=2)
        
        elif question['question_type'] == 'multiple':
            # 多选题
            self.answer_vars = {}
            saved_answers = self.exam_system.current_answers.get(question_id, [])
            
            for option in question['options']:
                option_value = option.split('.')[0].strip()
                var = tk.BooleanVar()
                if option_value in saved_answers:
                    var.set(True)
                self.answer_vars[option_value] = var
                ttk.Checkbutton(answer_frame, text=option, variable=var).pack(anchor=tk.W, pady=2)
        
        elif question['question_type'] == 'fill':
            # 填空题
            ttk.Label(answer_frame, text="请填写答案:").pack(anchor=tk.W, pady=(0, 5))
            self.answer_entry = ttk.Entry(answer_frame, width=50)
            self.answer_entry.pack(anchor=tk.W)
            if question_id in self.exam_system.current_answers:
                self.answer_entry.insert(0, self.exam_system.current_answers[question_id])
    
    def save_current_answer(self):
        """保存当前题目答案"""
        question = self.exam_system.current_questions[self.current_question_index]
        question_id = question['id']
        
        if question['question_type'] == 'single':
            answer = self.answer_var.get()
            if answer:
                self.exam_system.current_answers[question_id] = answer
        
        elif question['question_type'] == 'multiple':
            selected = [key for key, var in self.answer_vars.items() if var.get()]
            if selected:
                self.exam_system.current_answers[question_id] = selected
        
        elif question['question_type'] == 'fill':
            answer = self.answer_entry.get().strip()
            if answer:
                self.exam_system.current_answers[question_id] = answer
    
    def next_question(self):
        """下一题"""
        self.save_current_answer()
        self.current_question_index += 1
        self.create_exam_widgets()
    
    def prev_question(self):
        """上一题"""
        self.save_current_answer()
        self.current_question_index -= 1
        self.create_exam_widgets()
    
    def submit_exam(self):
        """提交考试"""
        self.save_current_answer()
        
        # 检查是否所有题目都已回答
        total_questions = len(self.exam_system.current_questions)
        answered_questions = len(self.exam_system.current_answers)
        
        if answered_questions < total_questions:
            result = messagebox.askyesno("确认提交", 
                                       f"您还有 {total_questions - answered_questions} 道题未回答，确定要提交吗？")
            if not result:
                return
        
        # 计算分数
        self.calculate_and_show_results()
    
    def calculate_and_show_results(self):
        """计算并显示考试结果"""
        correct_count = 0
        total_count = len(self.exam_system.current_questions)
        detailed_results = []
        
        for question in self.exam_system.current_questions:
            question_id = question['id']
            user_answer = self.exam_system.current_answers.get(question_id)
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
            
            detailed_results.append({
                'question': question['question_text'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        score = (correct_count / total_count) * 100
        end_time = datetime.now()
        
        # 保存考试记录
        self.exam_system.db.save_exam_record(
            self.exam_system.student_name,
            self.exam_system.current_category_id,
            total_count,
            correct_count,
            score,
            self.exam_system.start_time,
            end_time,
            {
                'answers': self.exam_system.current_answers,
                'detailed_results': detailed_results
            }
        )
        
        # 显示结果
        self.show_results(score, correct_count, total_count, detailed_results)
    
    def show_results(self, score, correct_count, total_count, detailed_results):
        """显示考试结果"""
        # 清除考试界面
        for widget in self.exam_frame.winfo_children():
            widget.destroy()
        
        # 结果标题
        title_label = ttk.Label(self.exam_frame, text="考试结果", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 基本信息
        info_frame = ttk.Frame(self.exam_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(info_frame, text=f"学生: {self.exam_system.student_name}", 
                 font=('Arial', 12)).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"得分: {score:.1f}分", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"正确题数: {correct_count}/{total_count}", 
                 font=('Arial', 12)).pack(anchor=tk.W)
        
        # 详细结果
        results_frame = ttk.LabelFrame(self.exam_frame, text="详细结果", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        results_text = scrolledtext.ScrolledText(results_frame, height=15)
        results_text.pack(fill=tk.BOTH, expand=True)
        
        for i, result in enumerate(detailed_results, 1):
            status = "✓" if result['is_correct'] else "✗"
            results_text.insert(tk.END, f"{i}. {status} {result['question']}\n")
            results_text.insert(tk.END, f"   您的答案: {result['user_answer']}\n")
            results_text.insert(tk.END, f"   正确答案: {result['correct_answer']}\n")
            if result['explanation']:
                results_text.insert(tk.END, f"   解析: {result['explanation']}\n")
            results_text.insert(tk.END, "\n")
        
        results_text.config(state=tk.DISABLED)
        
        # 重新开始按钮
        ttk.Button(self.exam_frame, text="重新开始", 
                  command=self.restart_exam).pack(pady=10)
    
    def restart_exam(self):
        """重新开始考试"""
        # 重置状态
        self.current_question_index = 0
        self.exam_system.current_answers = {}
        
        # 隐藏考试框架
        self.exam_frame.grid_remove()
        
        # 显示开始界面
        for widget in self.root.winfo_children()[0].winfo_children()[:4]:
            widget.grid()
        
        # 清空输入
        self.name_entry.delete(0, tk.END)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ExamGUI()
    app.run()