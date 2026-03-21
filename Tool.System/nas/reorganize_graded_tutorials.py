#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分级教程重新整理脚本
将分级教程目录下的教程重新分配到对应的专业分类中
"""

import os
import shutil
import logging
from datetime import datetime
import argparse

# 配置日志
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"graded_tutorials_reorganization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 基础路径
BASE_PATH = "/Volumes/video/教程/钢琴教程专区"
GRADED_PATH = os.path.join(BASE_PATH, "🎯 分级教程")

# 教程重新分类映射
TUTORIAL_MAPPING = {
    # 乐理基础类
    "宋大叔教音乐": "🎓 乐理基础",
    "陈俊宇《钢琴乐理的秘密》": "🎓 乐理基础",
    "音乐术语": "🎓 乐理基础",
    "音乐笔试专业知识": "🎓 乐理基础",
    
    # 小汤系列
    "小汤《钢琴入门基础教程全集》": "🎹 小汤系列",
    "汤普森现代钢琴视频教程": "🎹 小汤系列",
    
    # 车尔尼系列
    "车尔尼599": "🎼 车尔尼系列",
    "车尔尼718": "🎼 车尔尼系列",
    "车尔尼740": "🎼 车尔尼系列",
    "车尔尼139": "🎼 车尔尼系列",
    "车尔尼299": "🎼 车尔尼系列",
    "车尔尼821": "🎼 车尔尼系列",
    "车尔尼849": "🎼 车尔尼系列",
    "车尔尼钢琴高级练习版": "🎼 车尔尼系列",
    "车尔尼钢琴简易练习曲139": "🎼 车尔尼系列",
    
    # 哈农练指法
    "哈农钢琴全套教程": "🎵 哈农练指法",
    "手指快速跑动训练要领": "🎵 哈农练指法",
    
    # 拜厄教程
    "拜厄钢琴基本教程": "📚 拜厄教程",
    
    # 巴赫作品
    "巴赫钢琴教程全集": "🎪 巴赫作品",
    
    # 考级教程
    "乔睿钢琴考级要领": "🎭 考级教程",
    
    # 编曲伴奏
    "24小时学好爵士钢琴": "🎤 编曲伴奏",
    "钢琴即兴伴奏教程": "🎤 编曲伴奏",
    "通俗钢琴即兴伴奏入门一学通": "🎤 编曲伴奏",
    
    # 基础教程（保留在分级教程中的）
    "V叔的钢琴基础入门课": "🎯 分级教程",  # 保持不动
}

def find_matching_category(tutorial_name):
    """根据教程名称找到匹配的分类"""
    for keyword, category in TUTORIAL_MAPPING.items():
        if keyword in tutorial_name:
            return category, keyword
    return None, None

def move_tutorial(source_path, target_category, tutorial_name, keyword, dry_run=True):
    """移动教程到目标分类"""
    target_base = os.path.join(BASE_PATH, target_category)
    
    # 确保目标目录存在
    if not dry_run:
        os.makedirs(target_base, exist_ok=True)
    
    target_path = os.path.join(target_base, os.path.basename(source_path))
    
    if dry_run:
        logger.info(f"📋 计划移动: {tutorial_name} → {target_category} (匹配: {keyword})")
    else:
        try:
            shutil.move(source_path, target_path)
            logger.info(f"✅ 移动: {tutorial_name} → {target_category} (匹配: {keyword})")
            return True
        except Exception as e:
            logger.error(f"❌ 移动失败: {tutorial_name} - {str(e)}")
            return False
    return True

def process_graded_tutorials(dry_run=True):
    """处理分级教程目录"""
    logger.info(f"{'🔍 模拟运行' if dry_run else '🚀 开始执行'}: 分级教程重新整理")
    logger.info(f"📁 处理目录: {GRADED_PATH}")
    
    if not os.path.exists(GRADED_PATH):
        logger.error(f"❌ 目录不存在: {GRADED_PATH}")
        return
    
    moved_count = 0
    kept_count = 0
    total_count = 0
    category_stats = {}
    
    # 遍历所有子目录（初级、中级、高级等）
    for level_dir in os.listdir(GRADED_PATH):
        level_path = os.path.join(GRADED_PATH, level_dir)
        if not os.path.isdir(level_path) or level_dir.startswith('.'):
            continue
            
        logger.info(f"\n📂 处理 {level_dir} 目录:")
        
        # 遍历该级别下的所有教程
        for tutorial_dir in os.listdir(level_path):
            tutorial_path = os.path.join(level_path, tutorial_dir)
            if not os.path.isdir(tutorial_path) or tutorial_dir.startswith('.'):
                continue
                
            total_count += 1
            
            # 查找匹配的分类
            target_category, keyword = find_matching_category(tutorial_dir)
            
            if target_category and target_category != "🎯 分级教程":
                # 需要移动到其他分类
                if move_tutorial(tutorial_path, target_category, tutorial_dir, keyword, dry_run):
                    moved_count += 1
                    category_stats[target_category] = category_stats.get(target_category, 0) + 1
            else:
                # 保持在分级教程中
                kept_count += 1
                logger.info(f"📍 保持: {tutorial_dir} → 🎯 分级教程")
    
    # 统计信息
    logger.info(f"\n📊 处理统计:")
    logger.info(f"   总教程数: {total_count}")
    logger.info(f"   重新分类: {moved_count}个")
    logger.info(f"   保持原位: {kept_count}个")
    
    if category_stats:
        logger.info(f"\n📋 新分类分布:")
        for category, count in sorted(category_stats.items()):
            logger.info(f"   {category}: {count}个")
    
    # 检查是否需要删除空目录
    if not dry_run and moved_count > 0:
        cleanup_empty_directories()
    
    if dry_run:
        logger.info(f"\n⚠️ 这是模拟运行，没有实际修改文件")
        logger.info(f"如需实际执行，请运行: python3 reorganize_graded_tutorials.py --execute")
    else:
        logger.info(f"\n🎉 分级教程重新整理完成!")
        logger.info(f"教程已按专业分类重新分配，便于查找和学习")

def cleanup_empty_directories():
    """清理空目录"""
    logger.info(f"\n🧹 清理空目录:")
    
    for level_dir in os.listdir(GRADED_PATH):
        level_path = os.path.join(GRADED_PATH, level_dir)
        if not os.path.isdir(level_path) or level_dir.startswith('.'):
            continue
            
        try:
            # 检查目录是否为空（除了.DS_Store等隐藏文件）
            contents = [f for f in os.listdir(level_path) if not f.startswith('.')]
            if not contents:
                shutil.rmtree(level_path)
                logger.info(f"🗑️ 删除空目录: {level_dir}")
        except Exception as e:
            logger.error(f"❌ 删除目录失败 {level_dir}: {str(e)}")
    
    # 检查分级教程根目录是否为空
    try:
        contents = [f for f in os.listdir(GRADED_PATH) if not f.startswith('.') and os.path.isdir(os.path.join(GRADED_PATH, f))]
        if not contents:
            # 如果分级教程目录完全空了，可以考虑删除或重命名
            logger.info(f"📝 分级教程目录已清空，可考虑删除或重新规划")
    except Exception as e:
        logger.error(f"❌ 检查根目录失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='分级教程重新整理脚本')
    parser.add_argument('--execute', action='store_true', help='实际执行移动操作（默认为模拟运行）')
    
    args = parser.parse_args()
    
    process_graded_tutorials(dry_run=not args.execute)

if __name__ == "__main__":
    main()