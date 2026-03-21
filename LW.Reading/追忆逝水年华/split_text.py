#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本文件拆分工具
用于将《追忆似水年华.txt》大文件拆分成小文件，便于处理
"""

import os
import re

def find_novel_start(file_path):
    """找到小说正文开始的位置"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 寻找小说开头的标志性句子
    start_patterns = [
        r'有很长一段时间，我都是早早就躺下了',
        r'很长时间里，我都是早早就躺下了',
        r'在很长一段时间里，我都是早早就躺下了'
    ]
    
    for i, line in enumerate(lines):
        for pattern in start_patterns:
            if re.search(pattern, line):
                print(f"找到小说开头在第 {i+1} 行: {line.strip()}")
                return i, lines
    
    # 如果没找到标志性开头，寻找第一卷标题
    for i, line in enumerate(lines):
        if '第一卷' in line or '在斯万家那边' in line:
            print(f"找到第一卷标题在第 {i+1} 行: {line.strip()}")
            return i, lines
    
    print("未找到明确的小说开头，从第200行开始")
    return 200, lines

def split_by_chapters(lines, start_line):
    """按章节拆分文本"""
    chapters = []
    current_chapter = []
    chapter_count = 0
    
    # 章节标识模式
    chapter_patterns = [
        r'^\s*第[一二三四五六七八九十\d]+卷',
        r'^\s*第[一二三四五六七八九十\d]+章',
        r'^\s*[一二三四五六七八九十\d]+\s*$',
        r'^\s*\d+\s*$'
    ]
    
    for i in range(start_line, len(lines)):
        line = lines[i].strip()
        
        # 检查是否是章节标题
        is_chapter_title = False
        for pattern in chapter_patterns:
            if re.match(pattern, line) and len(line) < 50:
                is_chapter_title = True
                break
        
        if is_chapter_title and current_chapter:
            # 保存当前章节
            chapters.append({
                'title': f'第{chapter_count+1}部分',
                'content': current_chapter.copy()
            })
            current_chapter = []
            chapter_count += 1
        
        current_chapter.append(lines[i])
    
    # 添加最后一个章节
    if current_chapter:
        chapters.append({
            'title': f'第{chapter_count+1}部分',
            'content': current_chapter
        })
    
    return chapters

def split_by_paragraphs(lines, start_line, max_lines_per_file=30):
    """按段落数量拆分文本"""
    parts = []
    current_part = []
    part_count = 0
    line_count = 0
    
    for i in range(start_line, len(lines)):
        current_part.append(lines[i])
        line_count += 1
        
        # 如果达到最大行数或遇到明显的段落分隔
        if (line_count >= max_lines_per_file or 
            (lines[i].strip() == '' and line_count > 10)):
            
            if current_part:
                parts.append({
                    'title': f'第{part_count+1}部分',
                    'content': current_part.copy()
                })
                current_part = []
                part_count += 1
                line_count = 0
    
    # 添加最后一部分
    if current_part:
        parts.append({
            'title': f'第{part_count+1}部分',
            'content': current_part
        })
    
    return parts

def save_parts(parts, output_dir):
    """保存拆分后的文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, part in enumerate(parts):
        filename = f'part_{i+1:03d}.txt'
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(part['content'])
        
        print(f"已保存: {filename} ({len(part['content'])} 行)")

def main():
    input_file = '/Users/liuwei/SynologyDrive/0050Project/LW.Reading/追忆逝水年华/追忆似水年华.txt'
    output_dir = '/Users/liuwei/SynologyDrive/0050Project/LW.Reading/追忆逝水年华/parts'
    
    print("开始拆分《追忆似水年华.txt》...")
    
    # 找到小说开始位置
    start_line, lines = find_novel_start(input_file)
    print(f"文件总行数: {len(lines)}")
    print(f"从第 {start_line+1} 行开始处理")
    
    # 尝试按章节拆分
    chapters = split_by_chapters(lines, start_line)
    
    if len(chapters) > 1:
        print(f"\n按章节拆分成功，共 {len(chapters)} 个章节")
        save_parts(chapters, output_dir)
    else:
        print("\n未能按章节拆分，改为按段落拆分")
        # 按段落拆分
        parts = split_by_paragraphs(lines, start_line, max_lines_per_file=30)
        print(f"按段落拆分成功，共 {len(parts)} 个部分")
        save_parts(parts, output_dir)
    
    # 如果第一次拆分的文件还是太大，进一步细分
    large_files = []
    for i, part in enumerate((chapters if len(chapters) > 1 else parts)):
        if len(part['content']) > 100:
            large_files.append(i)
    
    if large_files:
        print(f"\n发现 {len(large_files)} 个大文件，进行进一步拆分...")
        # 重新按更小的块拆分
        all_parts = split_by_paragraphs(lines, start_line, max_lines_per_file=20)
        print(f"细分完成，共 {len(all_parts)} 个部分")
        # 清空目录重新保存
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        save_parts(all_parts, output_dir)
    
    print(f"\n拆分完成！文件保存在: {output_dir}")
    
    # 显示前几个文件的信息
    print("\n前5个文件预览:")
    for i in range(min(5, len(os.listdir(output_dir)))):
        part_file = os.path.join(output_dir, f'part_{i+1:03d}.txt')
        if os.path.exists(part_file):
            with open(part_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                print(f"part_{i+1:03d}.txt: {first_line[:50]}...")

if __name__ == '__main__':
    main()