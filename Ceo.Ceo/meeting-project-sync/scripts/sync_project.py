#!/usr/bin/env python3
"""
项目任务同步器 - 将会议任务同步到项目管理系统
支持多种项目管理格式输出
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path


class ProjectTaskSync:
    """将会议解析结果同步到项目管理格式"""
    
    def __init__(self):
        self.task_id_counter = 1000
    
    def sync_to_project(self, parsed_meeting: Dict[str, Any], project_name: str = None) -> Dict[str, Any]:
        """
        将解析的会议数据转换为项目管理结构
        
        Args:
            parsed_meeting: 解析后的会议数据
            project_name: 项目名称
        
        Returns:
            项目管理格式的数据
        """
        if project_name is None:
            project_name = parsed_meeting['meeting_info'].get('title', '未命名项目')
        
        # 创建项目结构
        project = {
            'project_name': project_name,
            'created_from_meeting': parsed_meeting['meeting_info']['title'],
            'meeting_date': parsed_meeting['meeting_info']['date'],
            'created_at': datetime.now().isoformat(),
            'milestones': self._create_milestones(parsed_meeting),
            'tasks': self._create_project_tasks(parsed_meeting),
            'decisions_log': parsed_meeting['decisions'],
            'next_actions': self._create_next_actions(parsed_meeting),
            'team_members': parsed_meeting['meeting_info']['participants'],
            'status': 'active'
        }
        
        return project
    
    def _create_milestones(self, parsed_meeting: Dict) -> List[Dict[str, Any]]:
        """从决策中创建里程碑"""
        milestones = []
        
        for decision in parsed_meeting['decisions']:
            if decision['priority'] == 'high' or decision['category'] == 'strategic':
                milestone = {
                    'id': f"M{len(milestones) + 1}",
                    'title': decision['content'][:50],
                    'description': decision['content'],
                    'category': decision['category'],
                    'status': 'planned',
                    'created_from_decision': True
                }
                milestones.append(milestone)
        
        return milestones
    
    def _create_project_tasks(self, parsed_meeting: Dict) -> List[Dict[str, Any]]:
        """创建项目任务列表"""
        tasks = []
        
        for task_data in parsed_meeting['tasks']:
            task = {
                'id': f"TASK-{self.task_id_counter}",
                'title': task_data['description'],
                'assignee': task_data['assignee'] or '待分配',
                'deadline': self._normalize_deadline(task_data['deadline']),
                'priority': self._map_priority(task_data['priority']),
                'status': 'todo',
                'created_from_meeting': parsed_meeting['meeting_info']['title'],
                'meeting_date': parsed_meeting['meeting_info']['date'],
                'tags': self._generate_tags(task_data['description']),
                'estimated_hours': None,
                'dependencies': []
            }
            tasks.append(task)
            self.task_id_counter += 1
        
        return tasks
    
    def _create_next_actions(self, parsed_meeting: Dict) -> List[Dict[str, Any]]:
        """从建议中创建下一步行动"""
        next_actions = []
        
        for suggestion in parsed_meeting['next_meeting_suggestions']:
            action = {
                'type': suggestion['type'],
                'description': suggestion['content'],
                'priority': 'normal',
                'status': 'pending'
            }
            next_actions.append(action)
        
        return next_actions
    
    def _normalize_deadline(self, deadline: str) -> str:
        """标准化截止日期"""
        if not deadline:
            return ''
        
        today = datetime.now()
        
        if '本周' in deadline:
            # 本周五
            days_until_friday = (4 - today.weekday()) % 7
            target_date = today + timedelta(days=days_until_friday)
            return target_date.strftime('%Y-%m-%d')
        elif '下周' in deadline:
            # 下周五
            days_until_next_friday = ((4 - today.weekday()) % 7) + 7
            target_date = today + timedelta(days=days_until_next_friday)
            return target_date.strftime('%Y-%m-%d')
        elif '本月底' in deadline:
            # 本月最后一天
            next_month = today.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            return last_day.strftime('%Y-%m-%d')
        else:
            # 尝试解析日期
            return deadline
    
    def _map_priority(self, priority: str) -> str:
        """映射优先级"""
        priority_map = {
            'high': 'P0',
            'medium': 'P1',
            'normal': 'P2'
        }
        return priority_map.get(priority, 'P2')
    
    def _generate_tags(self, description: str) -> List[str]:
        """根据描述生成标签"""
        tags = []
        
        tag_keywords = {
            'development': ['开发', '编码', '代码', '技术'],
            'design': ['设计', 'UI', 'UX', '原型'],
            'testing': ['测试', 'QA', '验证'],
            'documentation': ['文档', '说明', '手册'],
            'meeting': ['会议', '讨论', '沟通'],
            'research': ['研究', '调研', '分析'],
            'deployment': ['部署', '上线', '发布'],
            'bug': ['bug', '问题', '修复', '错误']
        }
        
        description_lower = description.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def export_to_json(self, project_data: Dict, output_path: str):
        """导出为JSON格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
    
    def export_to_kanban(self, project_data: Dict, output_path: str):
        """导出为看板Markdown格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {project_data['project_name']} - 项目看板\n\n")
            f.write(f"**来源会议**: {project_data['created_from_meeting']} ({project_data['meeting_date']})\n\n")
            f.write("---\n\n")
            
            # 按状态分组任务
            todo_tasks = [t for t in project_data['tasks'] if t['status'] == 'todo']
            in_progress = [t for t in project_data['tasks'] if t['status'] == 'in_progress']
            done_tasks = [t for t in project_data['tasks'] if t['status'] == 'done']
            
            # 待办列
            f.write(f"## 📋 待办 ({len(todo_tasks)})\n\n")
            for task in todo_tasks:
                priority_icon = self._get_priority_icon(task['priority'])
                tags_str = ' '.join([f"`{tag}`" for tag in task['tags']]) if task['tags'] else ''
                deadline_str = f"⏰ {task['deadline']}" if task['deadline'] else ''
                f.write(f"- [ ] **{task['id']}** {priority_icon} {task['title']}\n")
                f.write(f"  - 负责人: @{task['assignee']} {deadline_str}\n")
                if tags_str:
                    f.write(f"  - 标签: {tags_str}\n")
                f.write("\n")
            
            # 进行中
            f.write(f"## 🚀 进行中 ({len(in_progress)})\n\n")
            for task in in_progress:
                priority_icon = self._get_priority_icon(task['priority'])
                tags_str = ' '.join([f"`{tag}`" for tag in task['tags']]) if task['tags'] else ''
                deadline_str = f"⏰ {task['deadline']}" if task['deadline'] else ''
                f.write(f"- [ ] **{task['id']}** {priority_icon} {task['title']}\n")
                f.write(f"  - 负责人: @{task['assignee']} {deadline_str}\n")
                if tags_str:
                    f.write(f"  - 标签: {tags_str}\n")
                f.write("\n")
            
            # 已完成
            f.write(f"## ✅ 已完成 ({len(done_tasks)})\n\n")
            for task in done_tasks:
                f.write(f"- [x] **{task['id']}** {task['title']} - @{task['assignee']}\n")
            
            # 里程碑
            if project_data['milestones']:
                f.write(f"\n## 🎯 里程碑\n\n")
                for milestone in project_data['milestones']:
                    status_icon = '✅' if milestone['status'] == 'completed' else '🎯'
                    f.write(f"- {status_icon} **{milestone['id']}**: {milestone['title']}\n")
            
            # 下一步行动
            if project_data['next_actions']:
                f.write(f"\n## 📌 下次会议准备\n\n")
                for action in project_data['next_actions']:
                    f.write(f"- {action['description']}\n")
    
    def export_to_gantt_data(self, project_data: Dict, output_path: str):
        """导出为甘特图数据格式（可用于Mermaid等工具）"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("```mermaid\n")
            f.write("gantt\n")
            f.write(f"    title {project_data['project_name']}\n")
            f.write("    dateFormat YYYY-MM-DD\n")
            f.write("    \n")
            
            # 按优先级排序任务
            sorted_tasks = sorted(project_data['tasks'], 
                                key=lambda x: (x['priority'], x['deadline'] or '9999-12-31'))
            
            for task in sorted_tasks:
                task_name = task['title'][:30]
                task_id = task['id'].lower().replace('-', '_')
                
                if task['deadline']:
                    # 假设任务需要3天完成
                    start_date = datetime.now().strftime('%Y-%m-%d')
                    f.write(f"    {task_name} :{task_id}, {start_date}, {task['deadline']}\n")
                else:
                    # 没有截止日期的任务
                    start_date = datetime.now().strftime('%Y-%m-%d')
                    end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                    f.write(f"    {task_name} :{task_id}, {start_date}, {end_date}\n")
            
            f.write("```\n")
    
    def _get_priority_icon(self, priority: str) -> str:
        """获取优先级图标"""
        icons = {
            'P0': '🔴',
            'P1': '🟡',
            'P2': '🟢'
        }
        return icons.get(priority, '⚪')


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python sync_project.py <解析后的JSON文件> [项目名称] [输出格式: json|kanban|gantt]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else None
    output_format = sys.argv[3] if len(sys.argv) > 3 else 'json'
    
    # 读取解析后的会议数据
    with open(input_file, 'r', encoding='utf-8') as f:
        parsed_meeting = json.load(f)
    
    # 同步到项目
    syncer = ProjectTaskSync()
    project_data = syncer.sync_to_project(parsed_meeting, project_name)
    
    # 输出
    output_base = Path(input_file).stem.replace('_parsed', '')
    
    if output_format == 'json':
        output_file = f"{output_base}_project.json"
        syncer.export_to_json(project_data, output_file)
        print(f"✅ 已导出项目JSON: {output_file}")
    elif output_format == 'kanban':
        output_file = f"{output_base}_kanban.md"
        syncer.export_to_kanban(project_data, output_file)
        print(f"✅ 已导出项目看板: {output_file}")
    elif output_format == 'gantt':
        output_file = f"{output_base}_gantt.md"
        syncer.export_to_gantt_data(project_data, output_file)
        print(f"✅ 已导出甘特图: {output_file}")
    
    # 打印摘要
    print(f"\n📊 项目同步结果:")
    print(f"  - 项目名称: {project_data['project_name']}")
    print(f"  - 任务总数: {len(project_data['tasks'])} 项")
    print(f"  - 里程碑: {len(project_data['milestones'])} 个")
    print(f"  - 团队成员: {len(project_data['team_members'])} 人")
    print(f"  - 下一步行动: {len(project_data['next_actions'])} 项")


if __name__ == '__main__':
    main()
