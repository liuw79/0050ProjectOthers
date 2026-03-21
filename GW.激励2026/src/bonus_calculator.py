"""
2026年激励方案测算工具 - 核心测算引擎
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# 导入配置
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.bonus_rules import (
    PUBLIC_CLASS_BONUS, MEMBER_CARD_BONUS, BACKEND_PROJECT_BONUS,
    CIRCLE_MANAGEMENT_BONUS, TOPIC_CIRCLE_BONUS, OTHER_BONUS_POOLS,
    FORECAST_VERSIONS, SCENARIOS
)


class CircleType(Enum):
    """经营圈类型"""
    HUANAN = "华南"
    HUADONG = "华东"
    HUABEI = "华北"
    KA = "KA"


@dataclass
class PublicClassData:
    """公开课数据"""
    classes_60plus: int = 0      # ≥60人班级数
    classes_42_59: int = 0       # 42-59人班级数
    classes_below_42: int = 0    # <42人班级数
    individual_signups: int = 0  # 散客报名人次
    total_revenue: float = 0     # 公开课总收入
    avg_revenue_per_class: float = 0  # 平均班级收入
    substitute_days: int = 0     # 非班主任带班天数


@dataclass
class MemberCardData:
    """企业会员卡数据"""
    new_cards: int = 0           # 新开卡数
    renewal_cards: int = 0       # 续卡数
    active_members: int = 0      # 季度消卡6次的企业数
    source_persons: int = 0      # 来源人数（假设每人来源相同数量）
    converter_persons: int = 0   # 转化人数


@dataclass
class BackendProjectData:
    """后端项目数据"""
    project_count: int = 0       # 项目数量
    total_revenue: float = 0     # 项目总收入
    total_profit: float = 0      # 项目总利润
    source_persons: int = 0      # 来源人数
    lead_persons: int = 0        # 线索人数
    conversion_persons: int = 0  # 转化维护人数
    pm_persons: int = 0          # 项目经理人数


@dataclass
class CircleData:
    """经营圈数据"""
    circle_type: CircleType
    total_revenue: float = 0           # 总收入
    operating_cost: float = 0          # 运营成本（不含人员）
    public_class: PublicClassData = field(default_factory=PublicClassData)
    member_card: MemberCardData = field(default_factory=MemberCardData)
    backend_project: BackendProjectData = field(default_factory=BackendProjectData)
    growth_rate: float = 0             # 增长率（用于预测）


@dataclass
class TopicCircleData:
    """课题圈数据"""
    revenue_2025: float = 0      # 25年公开课收入
    profit_2025: float = 0       # 25年公开课利润
    revenue_2026: float = 0      # 26年公开课收入（预测）
    profit_2026: float = 0       # 26年公开课利润（预测）
    planned_new_courses: int = 20  # 按计划上新数量
    surprise_new_courses: int = 0  # 超预期上新数量


@dataclass
class BonusResult:
    """奖金测算结果"""
    category: str                # 奖金类别
    sub_category: str = ""       # 子类别
    amount: float = 0            # 金额
    formula: str = ""            # 计算公式
    notes: str = ""              # 备注


class BonusCalculator:
    """奖金测算引擎"""

    def __init__(self):
        self.results: List[BonusResult] = []

    def calculate_public_class_bonus(self, data: PublicClassData) -> Dict:
        """计算公开课奖金"""
        results = {}

        # 满班A (≥60人)
        if data.classes_60plus > 0:
            avg_revenue = data.avg_revenue_per_class or (data.total_revenue / max(1, data.classes_60plus + data.classes_42_59 + data.classes_below_42))
            amount = data.classes_60plus * avg_revenue * PUBLIC_CLASS_BONUS["满班A"]["rate"]
            results["满班A(≥60人)"] = {
                "amount": amount,
                "formula": f"{data.classes_60plus}班 × {avg_revenue:.0f}元 × 1.5%",
                "classes": data.classes_60plus
            }

        # 满班B (42-59人)
        if data.classes_42_59 > 0:
            avg_revenue = data.avg_revenue_per_class or (data.total_revenue / max(1, data.classes_60plus + data.classes_42_59 + data.classes_below_42))
            amount = data.classes_42_59 * avg_revenue * PUBLIC_CLASS_BONUS["满班B"]["rate"]
            results["满班B(42-59人)"] = {
                "amount": amount,
                "formula": f"{data.classes_42_59}班 × {avg_revenue:.0f}元 × 1%",
                "classes": data.classes_42_59
            }

        # 不满班 (<42人)
        if data.classes_below_42 > 0:
            avg_revenue = data.avg_revenue_per_class or (data.total_revenue / max(1, data.classes_60plus + data.classes_42_59 + data.classes_below_42))
            amount = data.classes_below_42 * avg_revenue * PUBLIC_CLASS_BONUS["不满班"]["rate"]
            results["不满班(<42人)"] = {
                "amount": amount,
                "formula": f"{data.classes_below_42}班 × {avg_revenue:.0f}元 × 0.5%",
                "classes": data.classes_below_42
            }

        # 散客
        # 需要散客单价，这里简化处理
        # results["散客"] = ...

        # 带班补贴
        if data.substitute_days > 0:
            avg_subsidy = 450  # 平均300-600
            amount = data.substitute_days * avg_subsidy
            results["带班补贴"] = {
                "amount": amount,
                "formula": f"{data.substitute_days}天 × {avg_subsidy}元/天"
            }

        results["公开课奖金合计"] = {
            "amount": sum(r["amount"] for r in results.values() if isinstance(r, dict) and "amount" in r)
        }

        return results

    def calculate_member_card_bonus(self, data: MemberCardData) -> Dict:
        """计算企业会员卡奖金"""
        results = {}

        # 开卡-来源人
        if data.new_cards > 0 and data.source_persons > 0:
            # 假设平均分配
            cards_per_person = data.new_cards / data.source_persons
            amount = data.new_cards * MEMBER_CARD_BONUS["开卡_来源人"]["amount"]
            results["开卡-来源人"] = {
                "amount": amount,
                "formula": f"{data.new_cards}张 × {MEMBER_CARD_BONUS['开卡_来源人']['amount']}元"
            }

        # 开卡-转化人
        if data.new_cards > 0 and data.converter_persons > 0:
            amount = data.new_cards * MEMBER_CARD_BONUS["开卡_转化人"]["amount"]
            results["开卡-转化人"] = {
                "amount": amount,
                "formula": f"{data.new_cards}张 × {MEMBER_CARD_BONUS['开卡_转化人']['amount']}元"
            }

        # 消卡
        if data.active_members > 0:
            amount = data.active_members * MEMBER_CARD_BONUS["消卡"]["amount"]
            results["消卡"] = {
                "amount": amount,
                "formula": f"{data.active_members}家 × {MEMBER_CARD_BONUS['消卡']['amount']}元/季 × 4季"
            }
            # 年度化
            results["消卡"]["amount"] = amount * 4

        # 续卡
        if data.renewal_cards > 0:
            amount = data.renewal_cards * MEMBER_CARD_BONUS["续卡"]["amount"]
            results["续卡"] = {
                "amount": amount,
                "formula": f"{data.renewal_cards}张 × {MEMBER_CARD_BONUS['续卡']['amount']}元"
            }

        results["会员卡奖金合计"] = {
            "amount": sum(r["amount"] for r in results.values() if isinstance(r, dict) and "amount" in r)
        }

        return results

    def calculate_backend_project_bonus(self, data: BackendProjectData) -> Dict:
        """计算后端项目奖金"""
        results = {}

        if data.total_profit <= 0:
            return {"后端项目奖金合计": {"amount": 0, "note": "无项目利润"}}

        # 来源
        if data.source_persons > 0:
            amount = data.total_profit * BACKEND_PROJECT_BONUS["来源"]["rate"]
            results["来源"] = {
                "amount": amount,
                "formula": f"{data.total_profit:.0f}元 × {BACKEND_PROJECT_BONUS['来源']['rate']*100}%"
            }

        # 线索
        if data.lead_persons > 0:
            amount = data.total_profit * BACKEND_PROJECT_BONUS["线索"]["rate"]
            results["线索"] = {
                "amount": amount,
                "formula": f"{data.total_profit:.0f}元 × {BACKEND_PROJECT_BONUS['线索']['rate']*100}%"
            }

        # 转化维护
        if data.conversion_persons > 0:
            amount = data.total_profit * BACKEND_PROJECT_BONUS["转化维护"]["rate"]
            results["转化维护"] = {
                "amount": amount,
                "formula": f"{data.total_profit:.0f}元 × {BACKEND_PROJECT_BONUS['转化维护']['rate']*100}%"
            }

        # 项目管理
        if data.pm_persons > 0:
            amount = data.total_profit * BACKEND_PROJECT_BONUS["项目管理"]["rate"]
            results["项目管理"] = {
                "amount": amount,
                "formula": f"{data.total_profit:.0f}元 × {BACKEND_PROJECT_BONUS['项目管理']['rate']*100}%"
            }

        results["后端项目奖金合计"] = {
            "amount": sum(r["amount"] for r in results.values() if isinstance(r, dict) and "amount" in r)
        }

        return results

    def calculate_circle_management_bonus(self, circle_type: CircleType,
                                          circle_data: CircleData,
                                          scenario: str = "保守") -> Dict:
        """计算圈子经营奖金"""
        results = {}
        config = CIRCLE_MANAGEMENT_BONUS.get(circle_type.value, {})

        if not config:
            return {"圈子经营奖金": {"amount": 0, "note": "未配置"}}

        # 计算经营利润
        operating_profit = circle_data.total_revenue - circle_data.operating_cost

        if config["type"] == "profit_percentage":
            # 华南/华东/KA - 按利润百分比
            base_bonus = operating_profit * config["base_rate"]
            multiplier = 1.0

            # 检查叠加条件
            scenario_config = SCENARIOS.get(scenario, SCENARIOS["保守"])
            if scenario_config.get("叠加条件达成") == True:
                multiplier = 1.2 * 1.2  # 两个叠加条件都达成
            elif isinstance(scenario_config.get("叠加条件达成"), dict):
                for cond, achieved in scenario_config["叠加条件达成"].items():
                    if achieved:
                        multiplier *= 1.2

            final_bonus = base_bonus * multiplier

            results["圈子经营奖金"] = {
                "amount": final_bonus,
                "formula": f"({circle_data.total_revenue:.0f} - {circle_data.operating_cost:.0f}) × 3% × {multiplier:.2f}",
                "base_bonus": base_bonus,
                "multiplier": multiplier,
                "operating_profit": operating_profit
            }

        elif config["type"] == "tiered_gmv":
            # 华北 - 阶梯制
            scenario_config = SCENARIOS.get(scenario, SCENARIOS["保守"])
            gmv_growth = scenario_config.get("华北GMV增长", 0.30)

            bonus_amount = 0
            for tier in config["tiers"]:
                if gmv_growth >= tier["gmv_growth"]:
                    bonus_amount = tier["bonus"]
                else:
                    break

            results["圈子经营奖金"] = {
                "amount": bonus_amount,
                "formula": f"GMV增长{gmv_growth*100:.0f}% → {bonus_amount/10000:.0f}万",
                "gmv_growth": gmv_growth
            }

        return results

    def calculate_topic_circle_bonus(self, data: TopicCircleData, scenario: str = "保守") -> Dict:
        """计算课题圈奖金"""
        results = {}

        # AI训战课专项奖金
        scenario_config = SCENARIOS.get(scenario, SCENARIOS["保守"])
        surprise_courses = scenario_config.get("超预期上新", 0)

        planned_bonus = data.planned_new_courses * TOPIC_CIRCLE_BONUS["AI训战课专项"]["按计划上新"]["amount"]
        surprise_bonus = surprise_courses * TOPIC_CIRCLE_BONUS["AI训战课专项"]["超预期上新"]["amount"]

        results["AI训战课专项-按计划"] = {
            "amount": planned_bonus,
            "formula": f"{data.planned_new_courses}门 × 1万"
        }
        results["AI训战课专项-超预期"] = {
            "amount": surprise_bonus,
            "formula": f"{surprise_courses}门 × 3万"
        }

        # 课题经营奖金（增量）
        profit_increase = data.profit_2026 - data.profit_2025
        if profit_increase > 0:
            incremental_bonus = profit_increase * 0.10
            results["课题经营奖金(增量)"] = {
                "amount": incremental_bonus,
                "formula": f"({data.profit_2026:.0f} - {data.profit_2025:.0f}) × 10%"
            }
        else:
            results["课题经营奖金(增量)"] = {
                "amount": 0,
                "note": "无增量利润"
            }

        results["课题圈奖金合计"] = {
            "amount": planned_bonus + surprise_bonus + results["课题经营奖金(增量)"]["amount"]
        }

        return results

    def calculate_all_bonuses(self, circles: Dict[CircleType, CircleData],
                             topic_data: TopicCircleData,
                             scenario: str = "保守") -> Dict:
        """计算所有奖金"""
        all_results = {
            "场景": scenario,
            "经营圈": {},
            "课题圈": {},
            "其他": {},
            "汇总": {}
        }

        total_bonus = 0
        total_revenue = 0

        # 各经营圈奖金
        for circle_type, circle_data in circles.items():
            circle_results = {
                "收入": circle_data.total_revenue,
                "公开课": self.calculate_public_class_bonus(circle_data.public_class),
                "会员卡": self.calculate_member_card_bonus(circle_data.member_card),
                "后端项目": self.calculate_backend_project_bonus(circle_data.backend_project),
                "经营奖金": self.calculate_circle_management_bonus(circle_type, circle_data, scenario)
            }

            # 计算圈子奖金合计
            circle_total = (
                circle_results["公开课"].get("公开课奖金合计", {}).get("amount", 0) +
                circle_results["会员卡"].get("会员卡奖金合计", {}).get("amount", 0) +
                circle_results["后端项目"].get("后端项目奖金合计", {}).get("amount", 0) +
                circle_results["经营奖金"].get("圈子经营奖金", {}).get("amount", 0)
            )
            circle_results["圈子奖金合计"] = circle_total
            circle_results["奖金占收入比"] = circle_total / max(1, circle_data.total_revenue) * 100

            all_results["经营圈"][circle_type.value] = circle_results
            total_bonus += circle_total
            total_revenue += circle_data.total_revenue

        # 课题圈奖金
        topic_results = self.calculate_topic_circle_bonus(topic_data, scenario)
        all_results["课题圈"] = topic_results
        total_bonus += topic_results.get("课题圈奖金合计", {}).get("amount", 0)

        # 其他奖金
        scenario_config = SCENARIOS.get(scenario, SCENARIOS["保守"])
        key_battle_bonus = scenario_config.get("关键战役奖金", 800000)
        other_bonus = {
            "内容圈_破圈奖金": {"amount": OTHER_BONUS_POOLS["内容圈_破圈奖金"]["amount"]},
            "关键战役奖金": {"amount": key_battle_bonus}
        }
        all_results["其他"] = other_bonus
        total_bonus += 200000 + key_battle_bonus  # 破圈+关键战役

        # 汇总
        all_results["汇总"] = {
            "总奖金": total_bonus,
            "总收入": total_revenue,
            "奖金占收入比": total_bonus / max(1, total_revenue) * 100
        }

        return all_results


def create_sample_data() -> Dict:
    """创建示例数据（用于测试）"""
    circles = {}

    # 华南圈示例数据
    huanan = CircleData(
        circle_type=CircleType.HUANAN,
        total_revenue=10000000,  # 1000万
        operating_cost=2000000,  # 200万
        public_class=PublicClassData(
            classes_60plus=20,
            classes_42_59=10,
            classes_below_42=5,
            total_revenue=3000000,
            avg_revenue_per_class=85000
        ),
        member_card=MemberCardData(
            new_cards=50,
            renewal_cards=30,
            active_members=40,
            source_persons=10,
            converter_persons=5
        ),
        backend_project=BackendProjectData(
            project_count=10,
            total_revenue=3000000,
            total_profit=600000,
            source_persons=5,
            lead_persons=3,
            conversion_persons=3,
            pm_persons=2
        )
    )
    circles[CircleType.HUANAN] = huanan

    # 华东圈示例数据
    huadong = CircleData(
        circle_type=CircleType.HUADONG,
        total_revenue=8000000,
        operating_cost=1600000,
        public_class=PublicClassData(
            classes_60plus=15,
            classes_42_59=8,
            classes_below_42=4,
            total_revenue=2400000,
            avg_revenue_per_class=85000
        ),
        member_card=MemberCardData(
            new_cards=40,
            renewal_cards=25,
            active_members=30,
            source_persons=8,
            converter_persons=4
        ),
        backend_project=BackendProjectData(
            project_count=8,
            total_revenue=2400000,
            total_profit=480000,
            source_persons=4,
            lead_persons=2,
            conversion_persons=2,
            pm_persons=1
        )
    )
    circles[CircleType.HUADONG] = huadong

    # 华北圈示例数据
    huabei = CircleData(
        circle_type=CircleType.HUABEI,
        total_revenue=5000000,
        operating_cost=1000000,
        public_class=PublicClassData(
            classes_60plus=10,
            classes_42_59=5,
            classes_below_42=3,
            total_revenue=1500000,
            avg_revenue_per_class=85000
        ),
        member_card=MemberCardData(
            new_cards=20,
            renewal_cards=15,
            active_members=15,
            source_persons=4,
            converter_persons=2
        ),
        backend_project=BackendProjectData(
            project_count=5,
            total_revenue=1500000,
            total_profit=300000,
            source_persons=2,
            lead_persons=1,
            conversion_persons=1,
            pm_persons=1
        )
    )
    circles[CircleType.HUABEI] = huabei

    # KA圈示例数据
    ka = CircleData(
        circle_type=CircleType.KA,
        total_revenue=15000000,
        operating_cost=3000000,
        public_class=PublicClassData(),  # KA圈无公开课
        member_card=MemberCardData(
            new_cards=30,
            renewal_cards=50,
            active_members=60,
            source_persons=6,
            converter_persons=3
        ),
        backend_project=BackendProjectData(
            project_count=20,
            total_revenue=10000000,
            total_profit=2000000,
            source_persons=5,
            lead_persons=3,
            conversion_persons=5,
            pm_persons=3
        )
    )
    circles[CircleType.KA] = ka

    # 课题圈数据
    topic_data = TopicCircleData(
        revenue_2025=5000000,
        profit_2025=1000000,
        revenue_2026=5500000,
        profit_2026=1200000,
        planned_new_courses=20,
        surprise_new_courses=0
    )

    return circles, topic_data


if __name__ == "__main__":
    # 测试测算引擎
    calculator = BonusCalculator()

    # 创建示例数据
    circles, topic_data = create_sample_data()

    # 运行三种场景测算
    for scenario in ["保守", "中性", "乐观"]:
        print(f"\n{'='*60}")
        print(f"场景: {scenario}")
        print('='*60)

        results = calculator.calculate_all_bonuses(circles, topic_data, scenario)

        print(f"\n【各经营圈奖金占收入比】")
        for circle_name, circle_data in results["经营圈"].items():
            print(f"  {circle_name}: {circle_data['奖金占收入比']:.2f}%")

        print(f"\n【课题圈奖金】")
        print(f"  合计: {results['课题圈']['课题圈奖金合计']['amount']/10000:.2f}万")

        print(f"\n【全公司汇总】")
        print(f"  总奖金: {results['汇总']['总奖金']/10000:.2f}万")
        print(f"  总收入: {results['汇总']['总收入']/10000:.2f}万")
        print(f"  奖金占收入比: {results['汇总']['奖金占收入比']:.2f}%")
