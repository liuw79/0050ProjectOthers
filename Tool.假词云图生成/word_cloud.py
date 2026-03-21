from PIL import Image, ImageDraw, ImageFont
import random
import math

import tkinter as tk
from tkinter import scrolledtext

def get_input_from_gui():
    """通过GUI窗口获取用户输入的关键词和图片尺寸"""
    words = []
    root = tk.Tk()
    root.title("词云图生成器")
    width = tk.IntVar(value=500)
    height = tk.IntVar(value=500)
    
    def submit():
        nonlocal words
        text = text_area.get("1.0", tk.END).strip()
        # 去除序号(如1. 2.)和括号及其内容
        import re
        text = re.sub(r'\d+\.\s*', '', text)  # 去除序号
        text = re.sub(r'\([^)]*\)', '', text)  # 去除半角括号内容
        text = re.sub(r'\（[^）]*\）', '', text)  # 去除全角括号内容
        words.extend([word.strip() for word in text.split('\n') if word.strip()])
        root.destroy()
    

    
    tk.Label(root, text="请输入关键词，每行一个:").pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    text_area.pack(pady=5, padx=10)
    
    # 添加尺寸设置
    size_frame = tk.Frame(root)
    size_frame.pack(pady=5)
    
    tk.Label(size_frame, text="宽度:").pack(side=tk.LEFT)
    tk.Entry(size_frame, textvariable=width, width=5).pack(side=tk.LEFT, padx=5)
    tk.Label(size_frame, text="高度:").pack(side=tk.LEFT)
    tk.Entry(size_frame, textvariable=height, width=5).pack(side=tk.LEFT, padx=5)
    
    tk.Button(root, text="生成词云图", command=submit).pack(pady=5)
    
    root.mainloop()
    return words, width.get(), height.get()

def generate_word_cloud():
    # 通过GUI获取用户输入的关键词和尺寸
    words, width, height = get_input_from_gui()
    
    if not words:
        print("未输入任何关键词！")
        return
    
    # 创建指定尺寸的画布
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 可用颜色列表
    colors = [
        (102, 153, 204),  # 柔和蓝
        (204, 153, 204),  # 淡紫
        (153, 204, 153),  # 薄荷绿
        (255, 204, 153),  # 浅橙
        (204, 204, 204),  # 浅灰
        (255, 153, 153),  # 粉红
        (153, 204, 204),  # 蓝绿
        (204, 153, 153)   # 玫瑰粉
    ]
    
    # 字体大小范围
    min_font_size = 20
    max_font_size = 60
    
    # 尝试加载字体（优先中文字体）
    font = None
    chinese_fonts = ['msyh.ttc', 'simsun.ttc', 'AlibabaPuHuiTi-3-55-Regular.ttf', 'arial.ttf']
    for font_name in chinese_fonts:
        try:
            font = ImageFont.truetype(font_name, 20)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()
    
    # 记录已放置文字的位置和大小
    placed_words = []
    
    # 放置每个词
    for word in words:
        # 随机选择字体大小
        font_size = random.randint(min_font_size, max_font_size)
        font = None
        for font_name in chinese_fonts:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
        if font is None:
            font = ImageFont.load_default()
        
        # 随机选择颜色
        color = random.choice(colors)
        
        # 计算文本大小
        text_bbox = draw.textbbox((0, 0), word, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 尝试放置文字，最多尝试100次
        placed = False
        for _ in range(100):
            # 随机位置（确保文本不会超出画布）
            max_x = max(0, width - text_width)
            max_y = max(0, height - text_height)
            x = random.randint(0, int(max_x)) if max_x > 0 else 0
            y = random.randint(0, int(max_y)) if max_y > 0 else 0
            
            # 检查是否与已放置文字重叠
            overlap = False
            for (px, py, p_width, p_height) in placed_words:
                if not (x + text_width < px or px + p_width < x or 
                        y + text_height < py or py + p_height < y):
                    overlap = True
                    break
            
            if not overlap:
                # 记录新文字的位置和大小
                placed_words.append((x, y, text_width, text_height))
                # 绘制文本到主图像
                draw.text((x, y), word, font=font, fill=color)
                placed = True
                break
        
        if not placed:
            print(f"无法放置文字: {word}")
    
    # 生成文件名：随机10个字符+时间戳+随机数
    import time
    import datetime
    all_chars = ''.join(words)
    random_chars = ''.join(random.sample(all_chars, min(10, len(all_chars)))) if all_chars else 'wordcloud'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(1000, 9999)
    filename = f"{random_chars}_{timestamp}_{random_num}.png"
    
    # 保存图片
    img.save(filename)
    print(f"词云图已生成，保存为{filename}")

if __name__ == "__main__":
    generate_word_cloud()