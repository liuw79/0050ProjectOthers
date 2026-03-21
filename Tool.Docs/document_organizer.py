#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档整理工具
自动整理WPS云文档备份目录中的文档，按类型和内容进行分类
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('document_organizer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DocumentOrganizer:
    def __init__(self, source_dir, target_dir):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        
        # 文档分类规则
        self.categories = {
            '01_个人证件': {
                'keywords': ['护照', '身份证', '出生医学证明', '户口', '驾驶证'],
                'patterns': [r'.*护照.*', r'.*身份证.*', r'.*出生.*证明.*']
            },
            '02_合同协议': {
                'keywords': ['合同', '协议', '协议书', '委托书', '授权'],
                'patterns': [r'.*合同.*', r'.*协议.*', r'.*委托.*', r'.*授权.*']
            },
            '03_财务文档': {
                'keywords': ['发票', '收据', '报销', '工资', '薪酬', '财务', '税务', '纳税', '开户证明', '银行'],
                'patterns': [r'.*发票.*', r'.*工资.*', r'.*财务.*', r'.*税.*', r'.*银行.*']
            },
            '04_项目文档': {
                'keywords': ['项目', '立项', '验收', '结项', '任务书', 'OKR'],
                'patterns': [r'.*项目.*', r'.*立项.*', r'.*验收.*', r'.*结项.*', r'.*OKR.*']
            },
            '05_教育学习': {
                'keywords': ['作业', '练习', '课程', '课表', '教学', '学习', '考试', '年级', '班级', '暑假', '寒假'],
                'patterns': [r'.*作业.*', r'.*练习.*', r'.*课程.*', r'.*年级.*', r'.*班.*']
            },
            '06_高维学堂': {
                'keywords': ['高维', '学堂', '创始人', '学友', '导师', '企业'],
                'patterns': [r'.*高维.*', r'.*学堂.*', r'.*创始人.*', r'.*学友.*']
            },
            '07_人事档案': {
                'keywords': ['简历', '在职证明', '收入证明', '离职', '入职', '员工'],
                'patterns': [r'.*简历.*', r'.*在职.*证明.*', r'.*收入.*证明.*', r'.*离职.*', r'.*入职.*']
            },
            '08_扫描文件': {
                'keywords': ['scan'],
                'patterns': [r'.*scan.*', r'\d{8}scan.*']
            },
            '09_数据统计': {
                'keywords': ['统计', '数据', '报表', '分析', '排行'],
                'patterns': [r'.*统计.*', r'.*数据.*', r'.*报表.*']
            },
            '10_生活文档': {
                'keywords': ['旅游', '攻略', '房产', '装修', '医疗', '体检'],
                'patterns': [r'.*旅游.*', r'.*攻略.*', r'.*房产.*', r'.*装修.*', r'.*体检.*']
            }
        }
        
        # 按文件扩展名分类
        self.file_types = {
            'PDF文档': ['.pdf'],
            'Word文档': ['.docx', '.doc'],
            'Excel文档': ['.xlsx', '.xls', '.csv'],
            'PPT文档': ['.pptx', '.ppt'],
            '图片文件': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            '文本文件': ['.txt'],
            '其他文件': []
        }
        
    def create_directories(self):
        """创建目标目录结构"""
        self.target_dir.mkdir(exist_ok=True)
        
        # 按内容分类的目录
        content_dir = self.target_dir / '按内容分类'
        content_dir.mkdir(exist_ok=True)
        
        for category in self.categories.keys():
            (content_dir / category).mkdir(exist_ok=True)
            
        # 按文件类型分类的目录
        type_dir = self.target_dir / '按文件类型分类'
        type_dir.mkdir(exist_ok=True)
        
        for file_type in self.file_types.keys():
            (type_dir / file_type).mkdir(exist_ok=True)
            
        # 按年份分类的目录
        year_dir = self.target_dir / '按年份分类'
        year_dir.mkdir(exist_ok=True)
        
        # 未分类目录
        (self.target_dir / '未分类').mkdir(exist_ok=True)
        
        logger.info("目录结构创建完成")
        
    def extract_year_from_filename(self, filename):
        """从文件名中提取年份"""
        # 匹配4位数字年份
        year_patterns = [
            r'(20\d{2})',  # 2000-2099
            r'(19\d{2})'   # 1900-1999
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, filename)
            if match:
                year = int(match.group(1))
                if 1990 <= year <= 2030:  # 合理的年份范围
                    return str(year)
        return None
        
    def categorize_by_content(self, filename):
        """根据文件名内容分类"""
        filename_lower = filename.lower()
        
        for category, rules in self.categories.items():
            # 检查关键词
            for keyword in rules['keywords']:
                if keyword.lower() in filename_lower:
                    return category
                    
            # 检查正则表达式
            for pattern in rules['patterns']:
                if re.search(pattern, filename, re.IGNORECASE):
                    return category
                    
        return None
        
    def categorize_by_type(self, filename):
        """根据文件扩展名分类"""
        ext = Path(filename).suffix.lower()
        
        for file_type, extensions in self.file_types.items():
            if ext in extensions:
                return file_type
                
        return '其他文件'
        
    def organize_files(self, dry_run=True):
        """整理文件"""
        if not self.source_dir.exists():
            logger.error(f"源目录不存在: {self.source_dir}")
            return
            
        self.create_directories()
        
        files_processed = 0
        files_categorized = 0
        
        # 统计信息
        stats = {
            'content_categories': {},
            'file_types': {},
            'years': {},
            'uncategorized': 0
        }
        
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                files_processed += 1
                filename = file_path.name
                
                logger.info(f"处理文件: {filename}")
                
                # 按内容分类
                content_category = self.categorize_by_content(filename)
                if content_category:
                    target_path = self.target_dir / '按内容分类' / content_category / filename
                    stats['content_categories'][content_category] = stats['content_categories'].get(content_category, 0) + 1
                    files_categorized += 1
                else:
                    target_path = self.target_dir / '未分类' / filename
                    stats['uncategorized'] += 1
                    
                # 按文件类型分类
                file_type = self.categorize_by_type(filename)
                type_target_path = self.target_dir / '按文件类型分类' / file_type / filename
                stats['file_types'][file_type] = stats['file_types'].get(file_type, 0) + 1
                
                # 按年份分类
                year = self.extract_year_from_filename(filename)
                if year:
                    year_dir = self.target_dir / '按年份分类' / year
                    year_dir.mkdir(exist_ok=True)
                    year_target_path = year_dir / filename
                    stats['years'][year] = stats['years'].get(year, 0) + 1
                    
                    if not dry_run:
                        try:
                            shutil.copy2(file_path, year_target_path)
                        except Exception as e:
                            logger.error(f"复制文件到年份目录失败 {filename}: {e}")
                
                # 执行文件复制（如果不是试运行）
                if not dry_run:
                    try:
                        # 复制到内容分类目录
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, target_path)
                        
                        # 复制到文件类型目录
                        type_target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, type_target_path)
                        
                        logger.info(f"文件已复制: {filename} -> {content_category or '未分类'}")
                        
                    except Exception as e:
                        logger.error(f"复制文件失败 {filename}: {e}")
                        
        # 输出统计信息
        logger.info(f"\n=== 整理统计 ===")
        logger.info(f"总文件数: {files_processed}")
        logger.info(f"已分类文件数: {files_categorized}")
        logger.info(f"未分类文件数: {stats['uncategorized']}")
        
        logger.info(f"\n=== 内容分类统计 ===")
        for category, count in sorted(stats['content_categories'].items()):
            logger.info(f"{category}: {count} 个文件")
            
        logger.info(f"\n=== 文件类型统计 ===")
        for file_type, count in sorted(stats['file_types'].items()):
            logger.info(f"{file_type}: {count} 个文件")
            
        logger.info(f"\n=== 年份统计 ===")
        for year, count in sorted(stats['years'].items()):
            logger.info(f"{year}年: {count} 个文件")
            
        return stats
        
    def generate_index(self):
        """生成文档索引"""
        index_file = self.target_dir / '文档索引.md'
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("# 文档整理索引\n\n")
            f.write(f"整理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 按内容分类索引
            f.write("## 按内容分类\n\n")
            content_dir = self.target_dir / '按内容分类'
            if content_dir.exists():
                for category_dir in sorted(content_dir.iterdir()):
                    if category_dir.is_dir():
                        files = list(category_dir.glob('*'))
                        f.write(f"### {category_dir.name} ({len(files)} 个文件)\n\n")
                        for file_path in sorted(files):
                            f.write(f"- {file_path.name}\n")
                        f.write("\n")
                        
            # 按文件类型索引
            f.write("## 按文件类型分类\n\n")
            type_dir = self.target_dir / '按文件类型分类'
            if type_dir.exists():
                for type_dir_path in sorted(type_dir.iterdir()):
                    if type_dir_path.is_dir():
                        files = list(type_dir_path.glob('*'))
                        f.write(f"### {type_dir_path.name} ({len(files)} 个文件)\n\n")
                        
            # 按年份索引
            f.write("## 按年份分类\n\n")
            year_dir = self.target_dir / '按年份分类'
            if year_dir.exists():
                for year_dir_path in sorted(year_dir.iterdir()):
                    if year_dir_path.is_dir():
                        files = list(year_dir_path.glob('*'))
                        f.write(f"### {year_dir_path.name}年 ({len(files)} 个文件)\n\n")
                        
        logger.info(f"文档索引已生成: {index_file}")

def main():
    # 配置路径
    source_dir = r"c:\Users\28919\SynologyDrive\0050Project\Tool.Docs\WPS云文档备份2025年5月14日"
    target_dir = r"c:\Users\28919\SynologyDrive\0050Project\Tool.Docs\整理后的文档"
    
    organizer = DocumentOrganizer(source_dir, target_dir)
    
    print("=== 文档整理工具 ===")
    print(f"源目录: {source_dir}")
    print(f"目标目录: {target_dir}")
    print()
    
    # 先进行试运行
    print("正在进行试运行分析...")
    stats = organizer.organize_files(dry_run=True)
    
    print("\n试运行完成！")
    print("\n是否执行实际整理？(y/n): ", end="")
    
    choice = input().strip().lower()
    if choice == 'y':
        print("\n开始实际整理...")
        organizer.organize_files(dry_run=False)
        organizer.generate_index()
        print("\n整理完成！")
    else:
        print("\n已取消整理操作")

if __name__ == "__main__":
    main()