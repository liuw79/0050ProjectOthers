#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钢琴教程重构演示工具
展示钢琴教程细分分类方案
"""

import json
from datetime import datetime
from pathlib import Path

class PianoTutorialDemo:
    def __init__(self):
        # 钢琴教程细分分类方案
        self.piano_categories = {
            "🎹 小汤系列": {
                "keywords": ["小汤", "汤普森", "thompson", "小汤姆森"],
                "description": "汤普森简易钢琴教程系列",
                "priority": 1
            },
            "🎼 车尔尼系列": {
                "keywords": ["车尔尼", "599", "849", "299", "740", "czerny"],
                "description": "车尔尼钢琴练习曲系列",
                "priority": 2
            },
            "📚 拜厄教程": {
                "keywords": ["拜厄", "beyer", "基础", "入门", "初学"],
                "description": "拜厄钢琴基本教程",
                "priority": 3
            },
            "🤲 哈农练指法": {
                "keywords": ["哈农", "hanon", "指法", "手指", "练指", "基本功"],
                "description": "哈农钢琴练指法",
                "priority": 4
            },
            "🎵 布格缪勒作品": {
                "keywords": ["布格缪勒", "布格穆勒", "burgmuller", "25首", "18首"],
                "description": "布格缪勒钢琴进阶练习曲",
                "priority": 5
            },
            "🎼 巴赫作品": {
                "keywords": ["巴赫", "bach", "创意曲", "小前奏曲", "平均律"],
                "description": "巴赫钢琴作品集",
                "priority": 6
            },
            "🎤 流行曲目": {
                "keywords": ["流行", "现代", "爵士", "pop", "jazz", "动漫", "影视", "好歌"],
                "description": "流行音乐和现代钢琴曲目",
                "priority": 7
            },
            "📦 其他教材": {
                "keywords": ["piano", "钢琴", "教程", "教材", "练习"],
                "description": "其他钢琴教材和内容",
                "priority": 8
            }
        }
        
        # 模拟现有教程（基于实际扫描结果）
        self.existing_tutorials = [
            {
                'name': 'Piano.tutorial.collection',
                'type': 'piano',
                'size_gb': 15.2,
                'description': '钢琴教程合集，包含多套完整教程'
            },
            {
                'name': 'V叔的钢琴基础入门课',
                'type': 'piano',
                'size_gb': 3.8,
                'description': '钢琴基础入门课程'
            },
            {
                'name': '学钢琴必备的认知提升课 五维高效学习法 【成人、琴童家长】',
                'type': 'piano',
                'size_gb': 2.1,
                'description': '钢琴学习方法和认知提升'
            },
            {
                'name': 'L优质好歌轻松弹 打造你的拿手曲目 钢琴演奏好听歌曲 丫妮钢琴',
                'type': 'piano',
                'size_gb': 4.5,
                'description': '流行歌曲钢琴演奏教程'
            },
            {
                'name': '音乐奥秘解码——轻松学乐理',
                'type': 'non-piano',
                'size_gb': 1.8,
                'description': '通用乐理知识（非钢琴专用）'
            },
            {
                'name': '方百里 哈农(34个视频 共925M)',
                'type': 'non-piano',
                'size_gb': 0.9,
                'description': '哈农练习（可能包含其他乐器）'
            },
            {
                'name': '鲍释贤',
                'type': 'non-piano',
                'size_gb': 2.3,
                'description': '未明确的音乐教程'
            },
            {
                'name': 'AI',
                'type': 'non-piano',
                'size_gb': 1.2,
                'description': 'AI相关教程（非音乐）'
            },
            {
                'name': '高维学堂-专业课程',
                'type': 'keep',
                'size_gb': 25.6,
                'description': '高维学堂专业课程（保持不变）'
            }
        ]
        
    def categorize_piano_tutorials(self):
        """对钢琴教程进行分类"""
        print("🎯 钢琴教程细分分类方案")
        print("=" * 60)
        
        categorization_result = {}
        piano_tutorials = [t for t in self.existing_tutorials if t['type'] == 'piano']
        non_piano_tutorials = [t for t in self.existing_tutorials if t['type'] == 'non-piano']
        keep_tutorials = [t for t in self.existing_tutorials if t['type'] == 'keep']
        
        print(f"\n🔍 分析现有教程结构...")
        print(f"   钢琴教程: {len(piano_tutorials)} 个")
        print(f"   非钢琴教程: {len(non_piano_tutorials)} 个")
        print(f"   保持不变: {len(keep_tutorials)} 个")
        
        print("\n📋 钢琴教程分类结果:")
        
        for tutorial in piano_tutorials:
            folder_name = tutorial['name'].lower()
            categorized = False
            
            # 按优先级进行分类
            for category, config in sorted(self.piano_categories.items(), 
                                         key=lambda x: x[1].get('priority', 9)):
                if category == '📦 其他钢琴内容':  # 跳过兜底分类
                    continue
                    
                for keyword in config['keywords']:
                    if keyword in folder_name:
                        if category not in categorization_result:
                            categorization_result[category] = []
                        categorization_result[category].append(tutorial)
                        print(f"✅ {tutorial['name'][:50]}... → {category} (匹配: {keyword})")
                        categorized = True
                        break
                        
                if categorized:
                    break
                    
            if not categorized:
                if '📦 其他钢琴内容' not in categorization_result:
                    categorization_result['📦 其他钢琴内容'] = []
                categorization_result['📦 其他钢琴内容'].append(tutorial)
                print(f"❓ {tutorial['name'][:50]}... → 📦 其他钢琴内容")
                
        return categorization_result, non_piano_tutorials, keep_tutorials
        
    def show_new_structure(self, categorization_result, non_piano_tutorials, keep_tutorials):
        """展示新的目录结构"""
        print("\n🏗️  新的钢琴教程目录结构:")
        print("教程/")
        print("├── 钢琴教程专区/")
        
        total_piano_size = 0
        total_piano_count = 0
        
        for category, tutorials in categorization_result.items():
            category_size = sum(t['size_gb'] for t in tutorials)
            total_piano_size += category_size
            total_piano_count += len(tutorials)
            
            print(f"│   ├── {category}/  ({len(tutorials)}个教程, {category_size:.1f}GB)")
            
            for tutorial in tutorials:
                print(f"│   │   ├── {tutorial['name'][:60]}...")
                print(f"│   │   │   └── 大小: {tutorial['size_gb']}GB")
                
        # 显示保持不变的目录
        for tutorial in keep_tutorials:
            print(f"├── {tutorial['name']}/  (保持原有结构不变, {tutorial['size_gb']}GB)")
            
        print(f"\n📊 统计信息:")
        print(f"   钢琴教程总数: {total_piano_count} 个")
        print(f"   钢琴教程总大小: {total_piano_size:.1f}GB")
        print(f"   分类数量: {len(categorization_result)} 个")
        
        return total_piano_count, total_piano_size
        
    def show_deletion_plan(self, non_piano_tutorials):
        """展示删除计划"""
        print(f"\n🗑️  删除计划 - 非钢琴教程 ({len(non_piano_tutorials)}个):")
        
        total_delete_size = 0
        for tutorial in non_piano_tutorials:
            total_delete_size += tutorial['size_gb']
            print(f"   ❌ {tutorial['name']} ({tutorial['size_gb']}GB)")
            print(f"      理由: {tutorial['description']}")
            
        print(f"\n💾 释放空间: {total_delete_size:.1f}GB")
        return total_delete_size
        
    def show_category_details(self):
        """展示分类详情"""
        print("\n📚 钢琴教程分类详情:")
        print("=" * 60)
        
        for category, config in self.piano_categories.items():
            print(f"\n{category}")
            print(f"   📝 描述: {config['description']}")
            if config['keywords']:
                print(f"   🔍 关键词: {', '.join(config['keywords'])}")
            print(f"   📊 优先级: {config.get('priority', 9)}")
            
    def show_benefits(self):
        """展示重构优势"""
        print("\n💡 钢琴教程重构优势:")
        print("=" * 40)
        
        benefits = [
            ("🎯 专业聚焦", "专门针对钢琴学习，内容更加专业和聚焦"),
            ("📁 细分清晰", "按学习阶段和内容类型细分，查找更精准"),
            ("🚀 学习效率", "从入门到进阶的完整学习路径"),
            ("💾 空间优化", "删除非钢琴内容，释放存储空间"),
            ("🎨 视觉友好", "使用专业emoji图标，目录更直观"),
            ("📈 易于扩展", "支持新增钢琴教程的快速分类")
        ]
        
        for title, desc in benefits:
            print(f"   {title}: {desc}")
            
    def generate_implementation_plan(self):
        """生成实施计划"""
        print("\n🚀 实施计划:")
        print("=" * 40)
        
        steps = [
            "1️⃣ 备份现有教程目录",
            "2️⃣ 运行钢琴重构工具模拟",
            "3️⃣ 确认分类结果和删除列表",
            "4️⃣ 执行钢琴教程重新分类",
            "5️⃣ 删除非钢琴教程内容",
            "6️⃣ 验证新目录结构",
            "7️⃣ 更新相关文档和索引"
        ]
        
        for step in steps:
            print(f"   {step}")
            
        print("\n⚠️  重要提醒:")
        warnings = [
            "• 高维学堂目录完全保持不变",
            "• 重构前务必备份重要数据",
            "• 首次使用建议先模拟运行",
            "• 删除操作不可逆，请谨慎确认",
            "• 可根据实际需要调整分类规则"
        ]
        
        for warning in warnings:
            print(f"   {warning}")
            
    def save_plan_to_file(self, categorization_result, non_piano_tutorials, keep_tutorials):
        """保存计划到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_file = Path(f"piano_reorganization_plan_{timestamp}.json")
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'reorganization_type': 'piano_specialized',
            'summary': {
                'piano_tutorials': sum(len(tutorials) for tutorials in categorization_result.values()),
                'categories': len(categorization_result),
                'deletions': len(non_piano_tutorials),
                'preserved': len(keep_tutorials)
            },
            'piano_categories': {},
            'deletion_list': [],
            'preserved_directories': []
        }
        
        # 钢琴分类详情
        for category, tutorials in categorization_result.items():
            plan['piano_categories'][category] = {
                'count': len(tutorials),
                'total_size_gb': round(sum(t['size_gb'] for t in tutorials), 1),
                'tutorials': [{
                    'name': t['name'],
                    'size_gb': t['size_gb'],
                    'description': t['description']
                } for t in tutorials],
                'description': self.piano_categories.get(category, {}).get('description', '')
            }
            
        # 删除列表
        plan['deletion_list'] = [{
            'name': t['name'],
            'size_gb': t['size_gb'],
            'reason': t['description']
        } for t in non_piano_tutorials]
        
        # 保持不变的目录
        plan['preserved_directories'] = [{
            'name': t['name'],
            'size_gb': t['size_gb'],
            'description': t['description']
        } for t in keep_tutorials]
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
            
        print(f"\n📄 钢琴重构计划已保存: {plan_file}")
        return plan_file
        
    def run_demo(self):
        """运行完整演示"""
        # 1. 展示分类详情
        self.show_category_details()
        
        # 2. 分析和分类
        categorization_result, non_piano_tutorials, keep_tutorials = self.categorize_piano_tutorials()
        
        # 3. 展示新结构
        total_piano_count, total_piano_size = self.show_new_structure(
            categorization_result, non_piano_tutorials, keep_tutorials)
        
        # 4. 展示删除计划
        total_delete_size = self.show_deletion_plan(non_piano_tutorials)
        
        # 5. 展示优势
        self.show_benefits()
        
        # 6. 实施计划
        self.generate_implementation_plan()
        
        # 7. 保存计划
        plan_file = self.save_plan_to_file(categorization_result, non_piano_tutorials, keep_tutorials)
        
        print("\n🎉 钢琴教程重构方案演示完成！")
        print(f"\n📋 重构效果预览:")
        print(f"   🎹 保留钢琴教程: {total_piano_count} 个 ({total_piano_size:.1f}GB)")
        print(f"   🗑️  删除非钢琴教程: {len(non_piano_tutorials)} 个 ({total_delete_size:.1f}GB)")
        print(f"   📁 新增分类目录: {len(categorization_result)} 个")
        print(f"   💾 释放存储空间: {total_delete_size:.1f}GB")
        
        print(f"\n📋 下一步操作:")
        print(f"   1. 查看详细计划: {plan_file}")
        print(f"   2. 执行重构: python3 piano_tutorial_reorganizer.py --execute")
        print(f"   3. 确认效果后更新文档")
        
def main():
    demo = PianoTutorialDemo()
    demo.run_demo()
    
if __name__ == '__main__':
    main()