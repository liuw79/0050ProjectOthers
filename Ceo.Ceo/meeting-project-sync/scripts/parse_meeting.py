#!/usr/bin/env python3
"""
会议纪要解析器 - 提取决策、任务和建议
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class MeetingParser:
    """解析会议纪要并提取关键信息"""
    
    def __init__(self):
        self.decision_keywords = ['决定', '决策', '批准', '同意', '确定', '定为', '决议']
        self.task_keywords = ['任务', '待办', '需要', '负责', '完成', '交付', 'TODO', 'Action Item']
        self.suggestion_keywords = ['建议', '提议', '下次', '后续', '跟进', '下周', '下一步']
    
    def parse(self, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        解析会议纪要内容
        
        Args:
            content: 会议纪要文本
            metadata: 可选的元数据（会议时间、参与者等）
        
        Returns:
            包含决策、任务、建议的结构化数据
        """
        if metadata is None:
            metadata = {}
        
        # 提取会议基本信息
        meeting_info = self._extract_meeting_info(content, metadata)
        
        # 提取决策事项
        decisions = self._extract_decisions(content)
        
        # 提取待办任务
        tasks = self._extract_tasks(content)
        
        # 提取下次会议建议
        next_meeting_suggestions = self._extract_suggestions(content)
        
        # 提取讨论主题
        topics = self._extract_topics(content)
        
        return {
            'meeting_info': meeting_info,
            'decisions': decisions,
            'tasks': tasks,
            'next_meeting_suggestions': next_meeting_suggestions,
            'topics': topics,
            'parsed_at': datetime.now().isoformat()
        }
    
    def _extract_meeting_info(self, content: str, metadata: Dict) -> Dict[str, Any]:
        """提取会议基本信息"""
        info = {
            'title': metadata.get('title', ''),
            'date': metadata.get('date', ''),
            'participants': metadata.get('participants', []),
            'location': metadata.get('location', ''),
            'duration': metadata.get('duration', '')
        }
        
        # 尝试从内容中提取
        if not info['title']:
            title_match = re.search(r'(?:会议主题|标题|主题)[:：]\s*(.+)', content)
            if title_match:
                info['title'] = title_match.group(1).strip()
        
        if not info['date']:
            date_match = re.search(r'(?:日期|时间|召开时间)[:：]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)', content)
            if date_match:
                info['date'] = date_match.group(1)
        
        if not info['participants']:
            participants_match = re.search(r'(?:参会人员|参与者|出席)[:：]\s*(.+)', content)
            if participants_match:
                participants_text = participants_match.group(1)
                info['participants'] = [p.strip() for p in re.split(r'[,，、]', participants_text)]
        
        return info
    
    def _extract_decisions(self, content: str) -> List[Dict[str, Any]]:
        """提取决策事项"""
        decisions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 检查是否包含决策关键词
            is_decision = any(keyword in line for keyword in self.decision_keywords)
            
            if is_decision:
                decision = {
                    'content': line,
                    'line_number': i + 1,
                    'priority': self._determine_priority(line),
                    'category': self._categorize_decision(line)
                }
                decisions.append(decision)
        
        return decisions
    
    def _extract_tasks(self, content: str) -> List[Dict[str, Any]]:
        """提取待办任务"""
        tasks = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 检查任务标记
            is_task = (
                line.startswith(('- [ ]', '* [ ]', '□', '☐')) or
                any(keyword in line for keyword in self.task_keywords) or
                re.match(r'^\d+[.、]', line)
            )
            
            if is_task:
                task = self._parse_task(line, i + 1)
                tasks.append(task)
        
        return tasks
    
    def _parse_task(self, line: str, line_number: int) -> Dict[str, Any]:
        """解析单个任务"""
        # 移除任务标记
        clean_line = re.sub(r'^[-*]\s*\[[ x]\]\s*|^[□☐]\s*|^\d+[.、]\s*', '', line)
        
        # 提取负责人
        assignee_match = re.search(r'[@【]([^】@]+)[】]?', clean_line)
        assignee = assignee_match.group(1) if assignee_match else None
        
        # 提取截止日期
        deadline_match = re.search(r'(\d{1,2}[-/月]\d{1,2}[日]?|\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?|本周|下周|本月底)', clean_line)
        deadline = deadline_match.group(1) if deadline_match else None
        
        # 移除已提取的信息，得到任务描述
        description = clean_line
        if assignee_match:
            description = description.replace(assignee_match.group(0), '').strip()
        if deadline_match:
            description = description.replace(deadline_match.group(0), '').strip()
        
        return {
            'description': description,
            'assignee': assignee,
            'deadline': deadline,
            'priority': self._determine_priority(line),
            'status': 'pending',
            'line_number': line_number
        }
    
    def _extract_suggestions(self, content: str) -> List[Dict[str, Any]]:
        """提取下次会议建议"""
        suggestions = []
        lines = content.split('\n')
        
        in_suggestion_section = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 检查是否进入建议部分
            if re.match(r'(?:下次会议|后续|跟进|下一步|建议)', line, re.IGNORECASE):
                in_suggestion_section = True
                continue
            
            # 在建议部分内提取内容
            if in_suggestion_section:
                if line and not line.startswith('#'):
                    suggestion = {
                        'content': line,
                        'line_number': i + 1,
                        'type': self._categorize_suggestion(line)
                    }
                    suggestions.append(suggestion)
                elif line.startswith('#'):
                    in_suggestion_section = False
        
        # 如果没有专门的建议部分，查找包含建议关键词的行
        if not suggestions:
            for i, line in enumerate(lines):
                line = line.strip()
                if any(keyword in line for keyword in self.suggestion_keywords):
                    suggestion = {
                        'content': line,
                        'line_number': i + 1,
                        'type': self._categorize_suggestion(line)
                    }
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _extract_topics(self, content: str) -> List[str]:
        """提取讨论主题"""
        topics = []
        
        # 查找标题
        for match in re.finditer(r'^#+\s+(.+)$', content, re.MULTILINE):
            topic = match.group(1).strip()
            if topic and topic not in topics:
                topics.append(topic)
        
        # 查找编号主题
        for match in re.finditer(r'^\d+[.、]\s+(.+?)[:：]', content, re.MULTILINE):
            topic = match.group(1).strip()
            if topic and topic not in topics:
                topics.append(topic)
        
        return topics
    
    def _determine_priority(self, text: str) -> str:
        """判断优先级"""
        high_priority_keywords = ['紧急', '重要', '优先', '立即', 'urgent', 'critical']
        medium_priority_keywords = ['尽快', '本周', '重点']
        
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in high_priority_keywords):
            return 'high'
        elif any(keyword in text_lower for keyword in medium_priority_keywords):
            return 'medium'
        else:
            return 'normal'
    
    def _categorize_decision(self, text: str) -> str:
        """分类决策"""
        if any(word in text for word in ['预算', '资金', '费用', '成本']):
            return 'financial'
        elif any(word in text for word in ['人员', '招聘', '调动', '团队']):
            return 'personnel'
        elif any(word in text for word in ['技术', '方案', '架构', '开发']):
            return 'technical'
        elif any(word in text for word in ['战略', '方向', '目标', '计划']):
            return 'strategic'
        else:
            return 'general'
    
    def _categorize_suggestion(self, text: str) -> str:
        """分类建议"""
        if any(word in text for word in ['议程', '时间', '地点']):
            return 'meeting_logistics'
        elif any(word in text for word in ['准备', '材料', '数据']):
            return 'preparation'
        elif any(word in text for word in ['邀请', '参与者']):
            return 'participants'
        else:
            return 'general'
    
    def export_to_json(self, parsed_data: Dict, output_path: str):
        """导出为JSON格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    
    def export_to_markdown(self, parsed_data: Dict, output_path: str):
        """导出为Markdown格式的项目任务清单"""
        with open(output_path, 'w', encoding='utf-8') as f:
            info = parsed_data['meeting_info']
            
            f.write(f"# 会议跟进任务清单\n\n")
            f.write(f"## 会议信息\n\n")
            f.write(f"- **标题**: {info['title']}\n")
            f.write(f"- **日期**: {info['date']}\n")
            f.write(f"- **参与者**: {', '.join(info['participants'])}\n\n")
            
            if parsed_data['decisions']:
                f.write(f"## 决策事项 ({len(parsed_data['decisions'])})\n\n")
                for i, decision in enumerate(parsed_data['decisions'], 1):
                    priority_icon = '🔴' if decision['priority'] == 'high' else '🟡' if decision['priority'] == 'medium' else '🟢'
                    f.write(f"{i}. {priority_icon} [{decision['category']}] {decision['content']}\n")
                f.write("\n")
            
            if parsed_data['tasks']:
                f.write(f"## 待办任务 ({len(parsed_data['tasks'])})\n\n")
                for i, task in enumerate(parsed_data['tasks'], 1):
                    priority_icon = '🔴' if task['priority'] == 'high' else '🟡' if task['priority'] == 'medium' else '🟢'
                    assignee = f"@{task['assignee']}" if task['assignee'] else "待分配"
                    deadline = f"⏰ {task['deadline']}" if task['deadline'] else ""
                    f.write(f"{i}. [ ] {priority_icon} {task['description']} - {assignee} {deadline}\n")
                f.write("\n")
            
            if parsed_data['next_meeting_suggestions']:
                f.write(f"## 下次会议建议\n\n")
                for suggestion in parsed_data['next_meeting_suggestions']:
                    f.write(f"- {suggestion['content']}\n")
                f.write("\n")
            
            if parsed_data['topics']:
                f.write(f"## 讨论主题\n\n")
                for topic in parsed_data['topics']:
                    f.write(f"- {topic}\n")


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python parse_meeting.py <会议纪要文件> [输出格式: json|markdown]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    
    # 读取会议纪要
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析
    parser = MeetingParser()
    parsed_data = parser.parse(content)
    
    # 输出
    output_base = Path(input_file).stem
    if output_format == 'json':
        output_file = f"{output_base}_parsed.json"
        parser.export_to_json(parsed_data, output_file)
        print(f"✅ 已导出JSON: {output_file}")
    else:
        output_file = f"{output_base}_tasks.md"
        parser.export_to_markdown(parsed_data, output_file)
        print(f"✅ 已导出Markdown任务清单: {output_file}")
    
    # 打印摘要
    print(f"\n📊 解析结果:")
    print(f"  - 决策事项: {len(parsed_data['decisions'])} 项")
    print(f"  - 待办任务: {len(parsed_data['tasks'])} 项")
    print(f"  - 下次会议建议: {len(parsed_data['next_meeting_suggestions'])} 项")
    print(f"  - 讨论主题: {len(parsed_data['topics'])} 项")


if __name__ == '__main__':
    main()
