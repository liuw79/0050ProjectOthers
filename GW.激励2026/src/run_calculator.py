"""
2026年激励方案测算工具 - 主程序入口
运行方式: python src/run_calculator.py
"""

import sys
import os
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bonus_calculator import (
    BonusCalculator, CircleData, CircleType,
    PublicClassData, MemberCardData, BackendProjectData,
    TopicCircleData, create_sample_data
)
from src.report_generator import ReportGenerator


def load_data_from_csv(filepath: str) -> dict:
    """从CSV文件加载数据"""
    import csv

    circles = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            circle_type_str = row['circle_type'].strip()
            circle_type = CircleType(circle_type_str)

            circle_data = CircleData(
                circle_type=circle_type,
                total_revenue=float(row.get('total_revenue', 0) or 0),
                operating_cost=float(row.get('operating_cost', 0) or 0),
                public_class=PublicClassData(
                    classes_60plus=int(row.get('classes_60plus', 0) or 0),
                    classes_42_59=int(row.get('classes_42_59', 0) or 0),
                    classes_below_42=int(row.get('classes_below_42', 0) or 0),
                    individual_signups=int(row.get('individual_signups', 0) or 0),
                    total_revenue=float(row.get('public_class_revenue', 0) or 0),
                    avg_revenue_per_class=float(row.get('avg_revenue_per_class', 0) or 0),
                    substitute_days=int(row.get('substitute_days', 0) or 0)
                ),
                member_card=MemberCardData(
                    new_cards=int(row.get('new_cards', 0) or 0),
                    renewal_cards=int(row.get('renewal_cards', 0) or 0),
                    active_members=int(row.get('active_members', 0) or 0),
                    source_persons=int(row.get('source_persons', 0) or 0),
                    converter_persons=int(row.get('converter_persons', 0) or 0)
                ),
                backend_project=BackendProjectData(
                    project_count=int(row.get('project_count', 0) or 0),
                    total_revenue=float(row.get('project_revenue', 0) or 0),
                    total_profit=float(row.get('project_profit', 0) or 0),
                    source_persons=int(row.get('project_source_persons', 0) or 0),
                    lead_persons=int(row.get('project_lead_persons', 0) or 0),
                    conversion_persons=int(row.get('project_conversion_persons', 0) or 0),
                    pm_persons=int(row.get('project_pm_persons', 0) or 0)
                )
            )
            circles[circle_type] = circle_data

    return circles


def load_topic_data_from_json(filepath: str) -> TopicCircleData:
    """从JSON文件加载课题圈数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return TopicCircleData(
        revenue_2025=data.get('revenue_2025', 0),
        profit_2025=data.get('profit_2025', 0),
        revenue_2026=data.get('revenue_2026', 0),
        profit_2026=data.get('profit_2026', 0),
        planned_new_courses=data.get('planned_new_courses', 20),
        surprise_new_courses=data.get('surprise_new_courses', 0)
    )


def apply_growth_forecast(circles: dict, version: str = "版本二_增长") -> dict:
    """应用增长预测"""
    from config.bonus_rules import FORECAST_VERSIONS

    growth_rates = FORECAST_VERSIONS.get(version, FORECAST_VERSIONS["版本一_持平"])

    forecasted_circles = {}
    for circle_type, circle_data in circles.items():
        growth_rate = growth_rates.get(circle_type.value, 0)

        # 创建新的数据对象
        new_circle = CircleData(
            circle_type=circle_type,
            total_revenue=circle_data.total_revenue * (1 + growth_rate),
            operating_cost=circle_data.operating_cost * (1 + growth_rate * 0.5),  # 成本增长较慢
            public_class=PublicClassData(
                classes_60plus=int(circle_data.public_class.classes_60plus * (1 + growth_rate)),
                classes_42_59=int(circle_data.public_class.classes_42_59 * (1 + growth_rate)),
                classes_below_42=int(circle_data.public_class.classes_below_42 * (1 + growth_rate)),
                individual_signups=int(circle_data.public_class.individual_signups * (1 + growth_rate)),
                total_revenue=circle_data.public_class.total_revenue * (1 + growth_rate),
                avg_revenue_per_class=circle_data.public_class.avg_revenue_per_class,
                substitute_days=int(circle_data.public_class.substitute_days * (1 + growth_rate))
            ),
            member_card=MemberCardData(
                new_cards=int(circle_data.member_card.new_cards * (1 + growth_rate)),
                renewal_cards=int(circle_data.member_card.renewal_cards * (1 + growth_rate)),
                active_members=int(circle_data.member_card.active_members * (1 + growth_rate)),
                source_persons=circle_data.member_card.source_persons,
                converter_persons=circle_data.member_card.converter_persons
            ),
            backend_project=BackendProjectData(
                project_count=int(circle_data.backend_project.project_count * (1 + growth_rate)),
                total_revenue=circle_data.backend_project.total_revenue * (1 + growth_rate),
                total_profit=circle_data.backend_project.total_profit * (1 + growth_rate),
                source_persons=circle_data.backend_project.source_persons,
                lead_persons=circle_data.backend_project.lead_persons,
                conversion_persons=circle_data.backend_project.conversion_persons,
                pm_persons=circle_data.backend_project.pm_persons
            ),
            growth_rate=growth_rate
        )
        forecasted_circles[circle_type] = new_circle

    return forecasted_circles


def main():
    """主函数"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("="*60)
    print("2026年激励方案测算工具")
    print("="*60)

    # 初始化测算引擎
    calculator = BonusCalculator()

    # 数据输入方式选择
    print("\n请选择数据输入方式:")
    print("1. 使用示例数据（快速体验）")
    print("2. 从CSV文件加载")
    print("3. 手动输入")

    choice = input("\n请输入选项 (1/2/3): ").strip()

    if choice == "1":
        # 使用示例数据
        circles, topic_data = create_sample_data()
        print("\n已加载示例数据")

    elif choice == "2":
        # 从CSV加载
        csv_path = input("请输入CSV文件路径 (默认: data/input_data.csv): ").strip()
        if not csv_path:
            csv_path = os.path.join(project_root, "data", "input_data.csv")
        elif not os.path.isabs(csv_path):
            csv_path = os.path.join(project_root, csv_path)

        try:
            circles = load_data_from_csv(csv_path)
            print(f"\n已从 {csv_path} 加载数据")
        except FileNotFoundError:
            print(f"文件未找到: {csv_path}")
            print("将使用示例数据")
            circles, topic_data = create_sample_data()

        # 课题圈数据
        topic_json_path = input("请输入课题圈数据JSON路径 (默认: data/topic_data.json): ").strip()
        if not topic_json_path:
            topic_json_path = os.path.join(project_root, "data", "topic_data.json")
        elif not os.path.isabs(topic_json_path):
            topic_json_path = os.path.join(project_root, topic_json_path)

        try:
            topic_data = load_topic_data_from_json(topic_json_path)
        except FileNotFoundError:
            print(f"课题圈数据文件未找到，将使用默认值")
            topic_data = TopicCircleData()

    else:
        # 手动输入（简化版）
        print("\n手动输入模式 - 使用示例数据作为基础")
        circles, topic_data = create_sample_data()

    # 选择预测版本
    print("\n请选择收入预测版本:")
    print("1. 版本一：与25年持平")
    print("2. 版本二：KA+50%, 华南华东+10%, 华北+50%")

    version_choice = input("请输入选项 (1/2): ").strip()
    if version_choice == "2":
        circles = apply_growth_forecast(circles, "版本二_增长")
        print("\n已应用增长预测")
    else:
        circles = apply_growth_forecast(circles, "版本一_持平")
        print("\n使用持平版本")

    # 选择测算场景
    print("\n请选择测算场景:")
    print("1. 保守场景")
    print("2. 中性场景")
    print("3. 乐观场景")
    print("4. 全部场景（对比报告）")

    scenario_choice = input("请输入选项 (1/2/3/4): ").strip()

    # 生成报告
    report_gen = ReportGenerator()
    output_dir = os.path.join(project_root, "docs")

    if scenario_choice == "4":
        # 生成多场景对比报告
        results_list = []
        for scenario in ["保守", "中性", "乐观"]:
            result = calculator.calculate_all_bonuses(circles, topic_data, scenario)
            results_list.append(result)

        report = report_gen.generate_comparison_report(results_list)
        output_file = os.path.join(output_dir, "测算报告-多场景对比.md")
    else:
        # 单场景报告
        scenario_map = {"1": "保守", "2": "中性", "3": "乐观"}
        scenario = scenario_map.get(scenario_choice, "保守")

        result = calculator.calculate_all_bonuses(circles, topic_data, scenario)
        report = report_gen.generate_full_report(result)
        output_file = os.path.join(output_dir, f"测算报告-{scenario}场景.md")

    # 保存报告
    report_gen.save_report(output_file, report)

    # 打印摘要
    print("\n" + "="*60)
    print("测算完成！")
    print("="*60)

    if scenario_choice == "4":
        for result in results_list:
            print(f"\n【{result['场景']}场景】")
            print(f"  总奖金: {result['汇总']['总奖金']/10000:.2f}万")
            print(f"  奖金占收入比: {result['汇总']['奖金占收入比']:.2f}%")
    else:
        print(f"\n【{scenario}场景】")
        print(f"  总奖金: {result['汇总']['总奖金']/10000:.2f}万")
        print(f"  奖金占收入比: {result['汇总']['奖金占收入比']:.2f}%")

    print(f"\n详细报告已保存到: {output_file}")

    return result


if __name__ == "__main__":
    main()
