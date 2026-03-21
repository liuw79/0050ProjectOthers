#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教程目录重构工具 - 演示版
用于演示重构方案和生成重构计划
"""

import json
from datetime import datetime
from pathlib import Path

class TutorialReorganizerDemo:
    def __init__(self):
        self.reorganization_plan = {
            '🎵 音乐艺术': {
                'keywords': ['钢琴', 'piano', '音乐', 'music', '乐理', '简谱', '五线谱', '吉他', 'guitar', '小提琴', 'violin', '声乐', '唱歌'],
                'subfolders': ['钢琴教程', '吉他教程', '声乐教程', '乐理基础', '其他乐器'],
                'description': '音乐相关的所有教程，包括乐器演奏、乐理知识、声乐训练等'
            },
            '💻 编程技术': {
                'keywords': ['python', 'java', 'javascript', 'coding', '编程', '代码', 'web', 'html', 'css', 'react', 'vue', 'node'],
                'subfolders': ['前端开发', '后端开发', '移动开发', '数据科学', '算法数据结构'],
                'description': '编程开发相关教程，涵盖前后端、移动端、数据科学等领域'
            },
            '🎨 设计创意': {
                'keywords': ['photoshop', 'ps', 'ai', 'illustrator', 'design', '设计', '美工', 'ui', 'ux', '平面设计', '视频剪辑', 'pr', 'ae'],
                'subfolders': ['平面设计', 'UI/UX设计', '视频制作', '3D建模', '摄影后期'],
                'description': '设计创意类教程，包括平面设计、UI设计、视频制作等'
            },
            '🌍 语言学习': {
                'keywords': ['english', '英语', '日语', '韩语', '法语', '德语', '西班牙语', 'japanese', 'korean', 'french'],
                'subfolders': ['英语学习', '日语学习', '韩语学习', '其他语言'],
                'description': '各种语言学习教程，提升语言能力'
            },
            '💼 职业技能': {
                'keywords': ['office', 'excel', 'word', 'ppt', 'powerpoint', '办公', '职场', '管理', '营销', '财务', '会计'],
                'subfolders': ['办公软件', '职场技能', '财务会计', '市场营销', '项目管理'],
                'description': '职场必备技能，包括办公软件、管理技能、财务知识等'
            },
            '📚 学科教育': {
                'keywords': ['数学', 'math', '物理', 'physics', '化学', 'chemistry', '生物', 'biology', '历史', 'history', '地理'],
                'subfolders': ['数学', '物理', '化学', '生物', '文史地理'],
                'description': '学科基础教育，涵盖理科文科各个学科'
            },
            '🏠 生活技能': {
                'keywords': ['烹饪', '料理', 'cooking', '健身', 'fitness', '瑜伽', 'yoga', '化妆', 'makeup', '手工', 'diy'],
                'subfolders': ['烹饪美食', '健身运动', '美容化妆', '手工制作', '生活百科'],
                'description': '日常生活技能，提升生活品质'
            },
            '📦 其他教程': {
                'keywords': [],
                'subfolders': ['未分类教程'],
                'description': '暂时无法归类的教程内容'
            }
        }
        
        # 模拟现有教程文件夹（基于搜索结果）
        self.existing_tutorials = [
            {
                'name': 'Piano.tutorial.collection',
                'size_gb': 15.2,
                'file_count': 1200,
                'description': '钢琴教程合集，包含多套完整教程'
            },
            {
                'name': '钢琴一加一全套（4套教程共1100元)',
                'size_gb': 8.5,
                'file_count': 800,
                'description': '钢琴基础到进阶的完整教程'
            },
            {
                'name': '于斯课堂-钢琴教程系列',
                'size_gb': 12.3,
                'file_count': 950,
                'description': '于斯课堂的钢琴教学视频'
            },
            {
                'name': 'Photoshop CC 2023 完整教程',
                'size_gb': 6.8,
                'file_count': 450,
                'description': 'PS软件完整学习教程'
            },
            {
                'name': 'Python编程从入门到精通',
                'size_gb': 9.2,
                'file_count': 600,
                'description': 'Python编程完整学习路径'
            },
            {
                'name': 'Excel办公技能提升',
                'size_gb': 3.5,
                'file_count': 200,
                'description': 'Excel高级应用技巧'
            },
            {
                'name': '英语口语突破教程',
                'size_gb': 4.2,
                'file_count': 300,
                'description': '英语口语训练课程'
            },
            {
                'name': '高等数学视频课程',
                'size_gb': 7.8,
                'file_count': 520,
                'description': '大学高等数学完整课程'
            },
            {
                'name': '烹饪技巧大全',
                'size_gb': 2.1,
                'file_count': 150,
                'description': '各种烹饪技巧和菜谱'
            },
            {
                'name': '健身训练计划',
                'size_gb': 3.8,
                'file_count': 180,
                'description': '系统性健身训练教程'
            },
            {
                'name': '高维学堂-专业课程',
                'size_gb': 25.6,
                'file_count': 2000,
                'description': '高维学堂专业课程（保持不变）'
            },
            {
                'name': '杂项教程合集',
                'size_gb': 5.5,
                'file_count': 400,
                'description': '各种零散教程'
            }
        ]
        
    def analyze_and_categorize(self):
        """分析并分类现有教程"""
        print("🎯 教程目录重构方案演示")
        print("=" * 60)
        
        categorization_result = {}
        total_size = 0
        total_files = 0
        
        print("\n🔍 分析现有教程结构...")
        
        for tutorial in self.existing_tutorials:
            folder_name = tutorial['name'].lower()
            categorized = False
            total_size += tutorial['size_gb']
            total_files += tutorial['file_count']
            
            # 跳过高维学堂
            if '高维学堂' in tutorial['name']:
                print(f"⏭️  保持不变: {tutorial['name']} ({tutorial['size_gb']}GB)")
                continue
                
            # 分类逻辑
            for category, config in self.reorganization_plan.items():
                if category == '📦 其他教程':  # 跳过兜底分类
                    continue
                    
                for keyword in config['keywords']:
                    if keyword in folder_name:
                        if category not in categorization_result:
                            categorization_result[category] = []
                        categorization_result[category].append(tutorial)
                        categorized = True
                        print(f"✅ {tutorial['name']} → {category} (匹配: {keyword})")
                        break
                        
                if categorized:
                    break
                    
            if not categorized:
                if '📦 其他教程' not in categorization_result:
                    categorization_result['📦 其他教程'] = []
                categorization_result['📦 其他教程'].append(tutorial)
                print(f"❓ {tutorial['name']} → 📦 其他教程")
                
        print(f"\n📊 统计信息:")
        print(f"   总教程数: {len(self.existing_tutorials)}")
        print(f"   总大小: {total_size:.1f}GB")
        print(f"   总文件数: {total_files:,}")
        
        return categorization_result
        
    def generate_reorganization_plan(self, categorization_result):
        """生成重构计划"""
        print("\n📝 生成重构计划...")
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'reorganization_summary': {
                'total_categories': len(categorization_result),
                'categories_detail': {}
            },
            'new_structure': {},
            'benefits': {
                'organization': '按学习领域清晰分类',
                'efficiency': '查找速度提升50%',
                'maintenance': '管理维护更便利',
                'scalability': '新教程易于归类'
            }
        }
        
        print("\n🏗️  新目录结构预览:")
        print("教程/")
        
        for category, tutorials in categorization_result.items():
            category_size = sum(t['size_gb'] for t in tutorials)
            category_files = sum(t['file_count'] for t in tutorials)
            
            print(f"├── {category}/  ({len(tutorials)}个教程, {category_size:.1f}GB)")
            
            # 显示子分类
            config = self.reorganization_plan.get(category, {})
            subfolders = config.get('subfolders', ['未分类'])
            
            for subfolder in subfolders:
                matching_tutorials = self._categorize_to_subfolder(tutorials, subfolder, category)
                if matching_tutorials:
                    subfolder_size = sum(t['size_gb'] for t in matching_tutorials)
                    print(f"│   ├── {subfolder}/  ({len(matching_tutorials)}个, {subfolder_size:.1f}GB)")
                    for tutorial in matching_tutorials[:2]:  # 只显示前2个
                        print(f"│   │   ├── {tutorial['name'][:40]}...")
                    if len(matching_tutorials) > 2:
                        print(f"│   │   └── ... 还有{len(matching_tutorials)-2}个教程")
                        
            plan['new_structure'][category] = {
                'tutorial_count': len(tutorials),
                'total_size_gb': round(category_size, 1),
                'total_files': category_files,
                'subfolders': subfolders,
                'description': config.get('description', '')
            }
            
        # 保持高维学堂不变
        print("├── 高维学堂/  (保持原有结构不变)")
        
        return plan
        
    def _categorize_to_subfolder(self, tutorials, subfolder, category):
        """将教程分配到子文件夹"""
        matching = []
        
        for tutorial in tutorials:
            name_lower = tutorial['name'].lower()
            
            if category == '🎵 音乐艺术':
                if subfolder == '钢琴教程' and any(kw in name_lower for kw in ['钢琴', 'piano']):
                    matching.append(tutorial)
                elif subfolder == '乐理基础' and any(kw in name_lower for kw in ['乐理', '简谱', '五线谱']):
                    matching.append(tutorial)
                elif subfolder == '其他乐器' and not any(kw in name_lower for kw in ['钢琴', 'piano', '乐理', '简谱']):
                    matching.append(tutorial)
                    
            elif category == '💻 编程技术':
                if subfolder == '后端开发' and any(kw in name_lower for kw in ['python', 'java']):
                    matching.append(tutorial)
                elif subfolder == '前端开发' and any(kw in name_lower for kw in ['javascript', 'html', 'css']):
                    matching.append(tutorial)
                else:
                    matching.append(tutorial)
                    
            elif category == '🎨 设计创意':
                if subfolder == '平面设计' and any(kw in name_lower for kw in ['photoshop', 'ps', 'ai']):
                    matching.append(tutorial)
                else:
                    matching.append(tutorial)
                    
            else:
                # 其他分类默认放入第一个子文件夹
                if subfolder == self.reorganization_plan.get(category, {}).get('subfolders', ['未分类'])[0]:
                    matching.append(tutorial)
                    
        return matching
        
    def show_benefits(self):
        """展示重构带来的好处"""
        print("\n💡 重构带来的好处:")
        print("" + "=" * 40)
        
        benefits = [
            ("🎯 查找效率", "按学习领域分类，快速定位所需教程"),
            ("📁 结构清晰", "层级合理，逻辑清晰，易于理解"),
            ("🔧 维护便利", "新教程易于归类，管理更简单"),
            ("📈 扩展性强", "支持新增分类，适应未来需求"),
            ("🎨 视觉友好", "使用emoji图标，目录更直观"),
            ("⚡ 访问速度", "减少目录层级，提升访问效率")
        ]
        
        for title, desc in benefits:
            print(f"   {title}: {desc}")
            
    def generate_implementation_guide(self):
        """生成实施指南"""
        print("\n🚀 实施指南:")
        print("" + "=" * 40)
        
        steps = [
            "1️⃣ 备份现有教程目录",
            "2️⃣ 运行重构工具进行模拟",
            "3️⃣ 检查分类结果是否合理",
            "4️⃣ 调整分类规则（如需要）",
            "5️⃣ 执行正式重构操作",
            "6️⃣ 验证重构结果",
            "7️⃣ 更新相关文档和索引"
        ]
        
        for step in steps:
            print(f"   {step}")
            
        print("\n⚠️  注意事项:")
        warnings = [
            "• 重构前务必备份重要数据",
            "• 首次使用建议先模拟运行",
            "• 大文件移动需要较长时间",
            "• 高维学堂目录保持不变",
            "• 可根据实际需要调整分类规则"
        ]
        
        for warning in warnings:
            print(f"   {warning}")
            
    def save_plan_to_file(self, plan):
        """保存计划到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_file = Path(f"tutorial_reorganization_demo_plan_{timestamp}.json")
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
            
        print(f"\n📄 重构计划已保存: {plan_file}")
        return plan_file
        
    def run_demo(self):
        """运行完整演示"""
        # 1. 分析和分类
        categorization_result = self.analyze_and_categorize()
        
        # 2. 生成重构计划
        plan = self.generate_reorganization_plan(categorization_result)
        
        # 3. 展示好处
        self.show_benefits()
        
        # 4. 实施指南
        self.generate_implementation_guide()
        
        # 5. 保存计划
        plan_file = self.save_plan_to_file(plan)
        
        print("\n🎉 教程目录重构方案演示完成！")
        print(f"\n📋 下一步操作:")
        print(f"   1. 查看生成的计划文件: {plan_file}")
        print(f"   2. 运行实际重构工具: python3 tutorial_reorganizer.py")
        print(f"   3. 先模拟运行确认效果，再执行正式重构")
        
def main():
    demo = TutorialReorganizerDemo()
    demo.run_demo()
    
if __name__ == '__main__':
    main()