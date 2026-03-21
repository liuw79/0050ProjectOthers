"""
2026年激励方案测算工具 - 报告生成器
生成Markdown格式的测算报告
"""

from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """测算报告生成器"""

    def __init__(self):
        self.report_lines = []

    def add_title(self, title: str, level: int = 1):
        """添加标题"""
        self.report_lines.append(f"{'#' * level} {title}\n")

    def add_text(self, text: str):
        """添加文本"""
        self.report_lines.append(f"{text}\n")

    def add_table(self, headers: List[str], rows: List[List]):
        """添加表格"""
        # 表头
        self.report_lines.append("| " + " | ".join(headers) + " |")
        # 分隔线
        self.report_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        # 数据行
        for row in rows:
            self.report_lines.append("| " + " | ".join([str(cell) for cell in row]) + " |")
        self.report_lines.append("")

    def add_section_divider(self):
        """添加分隔线"""
        self.report_lines.append("\n---\n")

    def generate_full_report(self, results: Dict) -> str:
        """生成完整测算报告"""

        # 标题
        self.add_title("2026年激励方案测算报告", 1)
        self.add_text(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.add_text(f"> 测算场景: {results.get('场景', '未知')}")
        self.add_section_divider()

        # 一、经营圈测算结果
        self.add_title("一、分经营圈奖金测算", 2)

        # 1.1 各经营圈奖金汇总
        self.add_title("1.1 各经营圈奖金占收入占比", 3)

        headers = ["经营圈", "总收入(万)", "总奖金(万)", "奖金占收入比"]
        rows = []
        for circle_name, circle_data in results["经营圈"].items():
            rows.append([
                circle_name,
                f"{circle_data['收入']/10000:.2f}",
                f"{circle_data['圈子奖金合计']/10000:.2f}",
                f"{circle_data['奖金占收入比']:.2f}%"
            ])

        # 添加合计行
        total_revenue = sum(c['收入'] for c in results["经营圈"].values())
        total_bonus = sum(c['圈子奖金合计'] for c in results["经营圈"].values())
        rows.append([
            "**合计**",
            f"**{total_revenue/10000:.2f}**",
            f"**{total_bonus/10000:.2f}**",
            f"**{total_bonus/total_revenue*100:.2f}%**"
        ])
        self.add_table(headers, rows)

        # 1.2 各经营圈奖金明细
        self.add_title("1.2 各经营圈奖金明细", 3)

        for circle_name, circle_data in results["经营圈"].items():
            self.add_text(f"**{circle_name}圈**")

            detail_headers = ["奖金类型", "金额(万)", "计算公式"]
            detail_rows = []

            # 公开课
            pc = circle_data.get("公开课", {})
            for key, val in pc.items():
                if isinstance(val, dict) and "amount" in val and key != "公开课奖金合计":
                    detail_rows.append([
                        f"公开课-{key}",
                        f"{val['amount']/10000:.2f}",
                        val.get("formula", "-")
                    ])

            # 会员卡
            mc = circle_data.get("会员卡", {})
            for key, val in mc.items():
                if isinstance(val, dict) and "amount" in val and key != "会员卡奖金合计":
                    detail_rows.append([
                        f"会员卡-{key}",
                        f"{val['amount']/10000:.2f}",
                        val.get("formula", "-")
                    ])

            # 后端项目
            bp = circle_data.get("后端项目", {})
            for key, val in bp.items():
                if isinstance(val, dict) and "amount" in val and key != "后端项目奖金合计":
                    detail_rows.append([
                        f"后端项目-{key}",
                        f"{val['amount']/10000:.2f}",
                        val.get("formula", "-")
                    ])

            # 经营奖金
            cm = circle_data.get("经营奖金", {}).get("圈子经营奖金", {})
            if cm:
                detail_rows.append([
                    "圈子经营奖金",
                    f"{cm['amount']/10000:.2f}",
                    cm.get("formula", "-")
                ])

            self.add_table(detail_headers, detail_rows)

        self.add_section_divider()

        # 二、课题圈测算结果
        self.add_title("二、三大课题圈奖金测算", 2)

        topic_headers = ["奖金类型", "金额(万)", "计算公式/说明"]
        topic_rows = []

        tc = results.get("课题圈", {})
        for key, val in tc.items():
            if isinstance(val, dict) and "amount" in val:
                topic_rows.append([
                    key,
                    f"{val['amount']/10000:.2f}",
                    val.get("formula", val.get("note", "-"))
                ])

        self.add_table(topic_headers, topic_rows)

        self.add_section_divider()

        # 三、其他奖金
        self.add_title("三、其他奖金", 2)

        other_headers = ["奖金类型", "金额(万)", "说明"]
        other_rows = []

        for key, val in results.get("其他", {}).items():
            if isinstance(val, dict) and "amount" in val:
                other_rows.append([
                    key,
                    f"{val['amount']/10000:.2f}",
                    val.get("note", "-")
                ])

        self.add_table(other_headers, other_rows)

        self.add_section_divider()

        # 四、全公司汇总
        self.add_title("四、全公司汇总", 2)

        summary = results.get("汇总", {})
        self.add_text(f"- **总奖金包**: {summary.get('总奖金', 0)/10000:.2f}万元")
        self.add_text(f"- **总收入**: {summary.get('总收入', 0)/10000:.2f}万元")
        self.add_text(f"- **奖金占收入比**: {summary.get('奖金占收入比', 0):.2f}%")

        self.add_section_divider()

        # 五、测算假设
        self.add_title("五、测算假设说明", 2)
        self.add_text("本次测算基于以下假设:")
        self.add_text("1. 各叠加条件达成情况按场景设定")
        self.add_text("2. 华北圈GMV增长按场景设定对应不同阶梯")
        self.add_text("3. 三大课题圈按计划上新20门，超预期上新按场景设定")
        self.add_text("4. 关键战役奖金包按场景设定")
        self.add_text("5. 未考虑啄木鸟奖、超额利润奖等不确定奖金")

        return "\n".join(self.report_lines)

    def generate_comparison_report(self, results_list: List[Dict]) -> str:
        """生成多场景对比报告"""

        self.add_title("2026年激励方案测算 - 多场景对比", 1)
        self.add_text(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.add_section_divider()

        # 场景对比表
        self.add_title("一、各场景奖金占比对比", 2)

        headers = ["经营圈"] + [r["场景"] for r in results_list]
        rows = []

        # 各经营圈对比
        circle_names = list(results_list[0]["经营圈"].keys())
        for circle_name in circle_names:
            row = [circle_name]
            for result in results_list:
                ratio = result["经营圈"][circle_name]["奖金占收入比"]
                row.append(f"{ratio:.2f}%")
            rows.append(row)

        # 全公司对比
        row = ["**全公司**"]
        for result in results_list:
            row.append(f"**{result['汇总']['奖金占收入比']:.2f}%**")
        rows.append(row)

        self.add_table(headers, rows)

        # 总奖金对比
        self.add_title("二、各场景总奖金包对比", 2)

        bonus_headers = ["场景", "总奖金(万)", "总收入(万)", "奖金占比"]
        bonus_rows = []
        for result in results_list:
            bonus_rows.append([
                result["场景"],
                f"{result['汇总']['总奖金']/10000:.2f}",
                f"{result['汇总']['总收入']/10000:.2f}",
                f"{result['汇总']['奖金占收入比']:.2f}%"
            ])

        self.add_table(bonus_headers, bonus_rows)

        return "\n".join(self.report_lines)

    def save_report(self, filepath: str, content: str = None):
        """保存报告到文件"""
        if content is None:
            content = "\n".join(self.report_lines)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"报告已保存到: {filepath}")


if __name__ == "__main__":
    # 测试报告生成器
    import sys
    sys.path.insert(0, '/Users/liuwei/SynologyDrive/0050Project/AI.long-running-agents')

    from src.bonus_calculator import BonusCalculator, create_sample_data

    calculator = BonusCalculator()
    circles, topic_data = create_sample_data()

    # 生成多个场景的结果
    results_list = []
    for scenario in ["保守", "中性", "乐观"]:
        result = calculator.calculate_all_bonuses(circles, topic_data, scenario)
        results_list.append(result)

    # 生成对比报告
    generator = ReportGenerator()
    report = generator.generate_comparison_report(results_list)

    print(report)

    # 保存报告
    generator.save_report('/Users/liuwei/SynologyDrive/0050Project/AI.long-running-agents/docs/测算报告-示例.md', report)
