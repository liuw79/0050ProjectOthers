#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公开课产品分析 - 快速启动脚本
一键运行完整的公开课产品分析，生成所有图表和报告
"""

import sys
import os
from pathlib import Path
import subprocess
import time

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 公开课产品分析系统启动")
    print("=" * 60)
    
    # 检查项目目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"📁 项目目录: {project_root}")
    print(f"⏰ 开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 运行分析脚本
    print("🔍 步骤1: 运行数据分析...")
    try:
        result = subprocess.run([
            sys.executable, 
            "scripts/analysis/open_course_analyzer.py"
        ], capture_output=True, text=True, check=True)
        
        print("✅ 数据分析完成")
        if result.stdout:
            print("📊 分析结果:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据分析失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    # 运行可视化脚本
    print("📈 步骤2: 生成可视化图表...")
    try:
        result = subprocess.run([
            sys.executable, 
            "scripts/visualization/open_course_visualizer.py"
        ], capture_output=True, text=True, check=True)
        
        print("✅ 可视化图表生成完成")
        if result.stdout:
            print("🎨 可视化结果:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 可视化生成失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    # 显示生成的文件
    print("📋 生成的文件清单:")
    print()
    
    # 图表文件
    charts_dir = project_root / "reports" / "charts"
    if charts_dir.exists():
        print("📊 图表文件 (reports/charts/):")
        chart_files = [f for f in charts_dir.glob("open_course_*.png") if f.is_file()]
        for chart_file in sorted(chart_files):
            file_size = chart_file.stat().st_size / 1024  # KB
            print(f"   📈 {chart_file.name} ({file_size:.1f}KB)")
        print()
    
    # 数据文件
    exports_dir = project_root / "data" / "exports"
    if exports_dir.exists():
        print("📁 数据文件 (data/exports/):")
        data_files = [f for f in exports_dir.glob("*course*") if f.is_file()]
        for data_file in sorted(data_files):
            file_size = data_file.stat().st_size / 1024  # KB
            print(f"   📄 {data_file.name} ({file_size:.1f}KB)")
        print()
    
    # 报告文件
    reports_dir = project_root / "reports" / "summaries"
    if reports_dir.exists():
        print("📝 报告文件 (reports/summaries/):")
        report_files = [f for f in reports_dir.glob("*course*") if f.is_file()]
        for report_file in sorted(report_files):
            file_size = report_file.stat().st_size / 1024  # KB
            print(f"   📋 {report_file.name} ({file_size:.1f}KB)")
        print()
    
    # 显示关键指标
    print("🎯 关键业绩指标:")
    summary_file = exports_dir / "open_course_summary.json"
    if summary_file.exists():
        try:
            import json
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            
            print(f"   💰 总收入: {summary['总收入']:.1f}万元")
            print(f"   💵 总利润: {summary['总利润']:.1f}万元")
            print(f"   📦 总订单: {summary['总订单']:,}单")
            print(f"   📊 平均利润率: {summary['平均利润率']:.1f}%")
            print(f"   🎓 课程数量: {summary['课程数量']}门")
            print(f"   👨‍🏫 讲师数量: {summary['讲师数量']}人")
            print(f"   🏆 收入最高课程: {summary['收入最高课程']}")
            print(f"   💎 收入最高讲师: {summary['收入最高讲师']}")
            
        except Exception as e:
            print(f"   ⚠️ 读取摘要数据失败: {e}")
    
    print()
    print("=" * 60)
    print("🎉 公开课产品分析完成！")
    print("=" * 60)
    print()
    print("📖 使用说明:")
    print("   1. 查看图表: 打开 reports/charts/ 目录下的PNG文件")
    print("   2. 查看数据: 打开 data/exports/ 目录下的CSV文件")
    print("   3. 查看报告: 打开 reports/summaries/open_course_analysis_report.md")
    print("   4. 重新分析: 再次运行此脚本")
    print()
    print(f"⏰ 完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 