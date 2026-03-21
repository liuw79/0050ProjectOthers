#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
营收分析模块
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import DATA_CONFIG, ANALYSIS_CONFIG
from scripts.utils.data_loader import data_loader

class RevenueAnalyzer:
    """营收分析器类"""
    
    def __init__(self):
        self.currency_unit = ANALYSIS_CONFIG["currency_unit"]
        self.decimal_places = ANALYSIS_CONFIG["decimal_places"]
        self.months = DATA_CONFIG["months"]
        self.regions = DATA_CONFIG["regions"]
        self.business_lines = DATA_CONFIG["business_lines"]
    
    def calculate_summary_stats(self, data: Dict) -> Dict:
        """
        计算汇总统计数据
        
        Args:
            data: 营收数据字典
        
        Returns:
            汇总统计结果
        """
        df = pd.DataFrame(data)
        
        # 计算总计和平均值
        summary = {}
        
        # 数值列（排除月份列）
        numeric_columns = [col for col in df.columns if col != '月份']
        
        # 总计
        summary['总计'] = df[numeric_columns].sum().to_dict()
        
        # 平均值
        summary['平均值'] = df[numeric_columns].mean().to_dict()
        
        # 最大值和对应月份
        summary['最大值'] = {}
        summary['最大值月份'] = {}
        for col in numeric_columns:
            max_idx = df[col].idxmax()
            summary['最大值'][col] = df[col].max()
            summary['最大值月份'][col] = df.loc[max_idx, '月份']
        
        # 最小值和对应月份
        summary['最小值'] = {}
        summary['最小值月份'] = {}
        for col in numeric_columns:
            min_idx = df[col].idxmin()
            summary['最小值'][col] = df[col].min()
            summary['最小值月份'][col] = df.loc[min_idx, '月份']
        
        # 增长率分析
        summary['增长率'] = self.calculate_growth_rate(df, numeric_columns)
        
        return summary
    
    def calculate_growth_rate(self, df: pd.DataFrame, columns: List[str]) -> Dict:
        """
        计算增长率
        
        Args:
            df: 数据DataFrame
            columns: 要计算的列名列表
        
        Returns:
            增长率字典
        """
        growth_rates = {}
        
        for col in columns:
            values = df[col].values
            rates = []
            
            for i in range(1, len(values)):
                if values[i-1] != 0:
                    rate = (values[i] - values[i-1]) / values[i-1] * 100
                    rates.append(rate)
                else:
                    rates.append(0)
            
            growth_rates[col] = {
                '月度增长率': rates,
                '平均增长率': np.mean(rates) if rates else 0,
                '最大增长率': max(rates) if rates else 0,
                '最小增长率': min(rates) if rates else 0
            }
        
        return growth_rates
    
    def compare_regions(self, region_data: Dict[str, Dict]) -> Dict:
        """
        比较不同区域的营收数据
        
        Args:
            region_data: 区域数据字典 {'region_name': data_dict}
        
        Returns:
            比较分析结果
        """
        comparison = {}
        
        # 计算每个区域的汇总数据
        region_summaries = {}
        for region, data in region_data.items():
            region_summaries[region] = self.calculate_summary_stats(data)
        
        # 总营收排名
        total_revenues = {}
        for region, summary in region_summaries.items():
            # 假设第一个业务线是主要营收指标
            main_business = list(summary['总计'].keys())[0]
            total_revenues[region] = summary['总计'][main_business]
        
        # 按总营收排序
        sorted_regions = sorted(total_revenues.items(), key=lambda x: x[1], reverse=True)
        
        comparison['营收排名'] = sorted_regions
        comparison['区域汇总'] = region_summaries
        
        # 计算占比
        total_all_regions = sum(total_revenues.values())
        comparison['营收占比'] = {
            region: (revenue / total_all_regions * 100) 
            for region, revenue in total_revenues.items()
        }
        
        return comparison
    
    def analyze_business_lines(self, data: Dict) -> Dict:
        """
        分析各业务线表现
        
        Args:
            data: 营收数据字典
        
        Returns:
            业务线分析结果
        """
        df = pd.DataFrame(data)
        business_analysis = {}
        
        # 排除月份列
        business_columns = [col for col in df.columns if col != '月份']
        
        for business in business_columns:
            business_analysis[business] = {
                '总营收': df[business].sum(),
                '平均营收': df[business].mean(),
                '营收占比': df[business].sum() / df[business_columns].sum().sum() * 100,
                '稳定性': df[business].std(),  # 标准差，越小越稳定
                '趋势': self.analyze_trend(df[business].values)
            }
        
        return business_analysis
    
    def analyze_trend(self, values: np.ndarray) -> str:
        """
        分析趋势
        
        Args:
            values: 数值数组
        
        Returns:
            趋势描述
        """
        if len(values) < 2:
            return "数据不足"
        
        # 计算线性回归斜率
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "上升趋势"
        elif slope < -0.1:
            return "下降趋势"
        else:
            return "平稳趋势"
    
    def generate_insights(self, analysis_results: Dict) -> List[str]:
        """
        生成分析洞察
        
        Args:
            analysis_results: 分析结果字典
        
        Returns:
            洞察列表
        """
        insights = []
        
        # 基于分析结果生成洞察
        if '营收排名' in analysis_results:
            top_region = analysis_results['营收排名'][0]
            insights.append(f"营收最高的区域是{top_region[0]}，营收为{top_region[1]:.2f}{self.currency_unit}")
        
        if '营收占比' in analysis_results:
            for region, ratio in analysis_results['营收占比'].items():
                if ratio > 50:
                    insights.append(f"{region}占据主导地位，营收占比达{ratio:.1f}%")
        
        return insights
    
    def export_analysis_report(self, analysis_results: Dict, filename: str = "analysis_report.json"):
        """
        导出分析报告
        
        Args:
            analysis_results: 分析结果
            filename: 文件名
        """
        # 转换numpy类型为Python原生类型，便于JSON序列化
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            else:
                return obj
        
        converted_results = convert_numpy_types(analysis_results)
        data_loader.save_json(converted_results, filename, "processed")

# 创建全局分析器实例
revenue_analyzer = RevenueAnalyzer()

if __name__ == "__main__":
    # 测试营收分析器
    print("营收分析器测试:")
    
    # 示例数据
    sample_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元': [100, 120, 150, 180, 160, 140],
        '公开课': [50, 60, 80, 90, 70, 65]
    }
    
    summary = revenue_analyzer.calculate_summary_stats(sample_data)
    print("汇总统计:", summary)
    
    business_analysis = revenue_analyzer.analyze_business_lines(sample_data)
    print("业务线分析:", business_analysis) 