#!/usr/bin/env python3
"""
公司净利分配计算器
GW.ShareMoney
"""

import json
from datetime import datetime
from pathlib import Path

# ============ 配置区 ============
CONFIG = {
    "year": 2025,

    # ===== 资金来源 =====
    "retained_earnings": 10430000,   # 账上未分配利润（不含25年利润）1043万
    "net_profit_2025": 19470000,     # 25年净利润 1947万

    # ===== 25年利润分配比例 =====
    "profit_split": {
        "shareholder": 0.4,      # 股东分红 40%
        "partner_bonus": 0.3,    # 管理合伙人激励 30%
        "reserve": 0.3           # 预留 30%
    },

    # ===== 预留目标 =====
    "target_reserve": 18390000,       # 预留目标：1839万
    # 明细（供参考）
    "salary_reserve": 12100000,       # 员工资险金 1210万
    "service_fee_reserve": 1290000,   # 外挂服务费 129万
    "ai_invest_reserve": 5000000,     # AI战略投入 500万

    # ===== 股权结构 =====
    # 股东
    "investors": {
        "东哥": 0.049,
        "慧余": 0.1704,
    },

    # 管理合伙人（股东分红用）
    "partner_shares": {
        "刘军": 0.13,
        "刘伟": 0.16,
        "KK": 0.395,  # 37.3% + 2.2%
        "股权池": 0.0456,  # 9.56% - 5%（划给员工后）
    },

    # 员工股权（总股本2亿股，员工约800-1000万股 ≈ 4-5%）
    "employee_share_total": 0.05,  # 约5%
    "employees_detail": {},  # 待填入明细

    # 管理合伙人激励分配（按年度评分）
    "partner_bonus_ratio": {
        "KK": 7.17,
        "刘军": 6.0,
        "刘伟": 5.33
    },

    # 年化定存利率
    "deposit_rate": 0.025  # 2.5%
}


def calc_partner_bonus(total: float, partner_ratio: dict) -> dict:
    """按比例/评分分配"""
    ratio_sum = sum(partner_ratio.values())
    return {
        name: total * (ratio / ratio_sum)
        for name, ratio in partner_ratio.items()
    }


def calculate_distribution(config: dict) -> dict:
    """计算完整的利润分配"""
    profit_split = config["profit_split"]

    # ===== 1. 25年净利润分配 =====
    net_profit = config["net_profit_2025"]
    shareholder_pool = net_profit * profit_split["shareholder"]      # 40% 股东分红
    partner_bonus_pool = net_profit * profit_split["partner_bonus"]  # 30% 管理合伙人激励
    reserve_from_2025 = net_profit * profit_split["reserve"]         # 30% 预留

    # ===== 2. 资金储备池 =====
    reserve_pool = config["retained_earnings"] + reserve_from_2025  # 历史可分配 + 25年预留30%
    target_reserve = config["target_reserve"]
    reserve_gap = target_reserve - reserve_pool

    # ===== 3. 股东分红分配 =====
    total_equity = (
        sum(config["investors"].values()) +
        sum(config["partner_shares"].values()) +
        config["employee_share_total"]
    )

    shareholder_result = {}

    # 3.1 股东按股权比例分
    for name, share in config["investors"].items():
        shareholder_result[f"股东-{name}"] = shareholder_pool * (share / total_equity)

    # 3.2 员工按股权比例分
    shareholder_result["员工合伙人"] = shareholder_pool * (config["employee_share_total"] / total_equity)

    # 3.3 管理合伙人（含股权池）按 1.5:1:1 分配
    partner_pool = shareholder_pool * (sum(config["partner_shares"].values()) / total_equity)
    partner_share_result = calc_partner_bonus(partner_pool, config["partner_bonus_ratio"])
    for name, amount in partner_share_result.items():
        shareholder_result[f"管理合伙人-{name}"] = amount

    # ===== 4. 管理合伙人激励（按评分分配） =====
    partner_bonus_result = calc_partner_bonus(partner_bonus_pool, config["partner_bonus_ratio"])

    # ===== 5. 管理合伙人合计 =====
    partner_total = {}
    for name in ["KK", "刘军", "刘伟"]:
        partner_total[name] = shareholder_result.get(f"管理合伙人-{name}", 0) + partner_bonus_result.get(name, 0)

    return {
        "year": config["year"],
        "retained_earnings": config["retained_earnings"],
        "net_profit_2025": net_profit,
        # 25年利润分配
        "shareholder_pool": shareholder_pool,
        "partner_bonus_pool": partner_bonus_pool,
        "reserve_from_2025": reserve_from_2025,
        # 资金储备池
        "reserve_pool": reserve_pool,
        "target_reserve": target_reserve,
        "reserve_gap": reserve_gap,
        # 预留明细
        "salary_reserve": config["salary_reserve"],
        "service_fee_reserve": config["service_fee_reserve"],
        "ai_invest_reserve": config["ai_invest_reserve"],
        # 分配结果
        "total_equity": total_equity,
        "shareholder_result": shareholder_result,
        "partner_bonus_result": partner_bonus_result,
        "partner_total": partner_total,
        "profit_split": profit_split,
    }


def format_money(amount: float) -> str:
    """格式化金额"""
    if amount >= 10000:
        return f"{amount/10000:.2f}万"
    return f"{amount:.2f}"


def generate_markdown(result: dict, config: dict) -> str:
    """生成Markdown报告"""
    lines = [
        f"# {result['year']}年度净利分配报告",
        "",
        "## 一、资金来源",
        "",
        "| 项目 | 金额 |",
        "|------|------|",
        f"| 账上未分配利润（不含25年） | {format_money(result['retained_earnings'])} |",
        f"| 25年净利润 | {format_money(result['net_profit_2025'])} |",
        "",
        "## 二、25年净利润分配",
        "",
        f"25年净利润 **{format_money(result['net_profit_2025'])}** 分为三部分：",
        "",
        "| 项目 | 比例 | 金额 |",
        "|------|------|------|",
        f"| 股东分红 (A) | 40% | {format_money(result['shareholder_pool'])} |",
        f"| 管理合伙人激励 (B) | 30% | {format_money(result['partner_bonus_pool'])} |",
        f"| 预留 (C) | 30% | {format_money(result['reserve_from_2025'])} |",
        "",
        "## 三、资金储备池",
        "",
        "| 项目 | 金额 | 说明 |",
        "|------|------|------|",
        f"| 历史可分配利润 | {format_money(result['retained_earnings'])} | 账上未分配利润 |",
        f"| 25年预留30% | {format_money(result['reserve_from_2025'])} | 1947万 × 30% |",
        f"| **储备池合计** | **{format_money(result['reserve_pool'])}** | |",
        f"| **预留目标** | **{format_money(result['target_reserve'])}** | 员工资险金+外挂服务费+AI战略投入 |",
        f"| **差额** | **{format_money(result['reserve_gap'])}** | 需补足 |",
        "",
        "### 预留目标构成",
        "",
        "| 项目 | 金额 |",
        "|------|------|",
        f"| 员工资险金 | {format_money(result['salary_reserve'])} |",
        f"| 外挂服务费 | {format_money(result['service_fee_reserve'])} |",
        f"| AI战略投入 | {format_money(result['ai_invest_reserve'])} |",
        f"| **合计** | **{format_money(result['target_reserve'])}** |",
        "",
        "## 四、股东分红明细（A池）",
        "",
        f"股东分红总额: **{format_money(result['shareholder_pool'])}**",
        "",
        "### 4.1 股东分红（按股权比例）",
        "",
        "| 姓名 | 股权比例 | 分红金额 |",
        "|------|----------|----------|",
    ]

    for name, share in config["investors"].items():
        key = f"股东-{name}"
        amount = result["shareholder_result"][key]
        lines.append(f"| {name} | {share*100:.2f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "### 4.2 管理合伙人分红（按1.5:1:1）",
        "",
        "| 姓名 | 比例 | 分红金额 |",
        "|------|------|----------|",
    ])

    ratio_sum = sum(config["partner_bonus_ratio"].values())
    for name in ["KK", "刘军", "刘伟"]:
        key = f"管理合伙人-{name}"
        amount = result["shareholder_result"][key]
        ratio = config["partner_bonus_ratio"][name]
        lines.append(f"| {name} | {ratio/ratio_sum*100:.1f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "### 4.3 员工合伙人分红（按股权比例）",
        "",
        "| 项目 | 股权比例 | 分红金额 | 备注 |",
        "|------|----------|----------|------|",
    ])

    emp_amount = result["shareholder_result"]["员工合伙人"]
    lines.append(f"| 员工持股池 | {config['employee_share_total']*100:.1f}% | {format_money(emp_amount)} | 明细待补充 |")

    lines.extend([
        "",
        "## 五、管理合伙人激励（B池，按评分分配）",
        "",
        f"激励总额: **{format_money(result['partner_bonus_pool'])}**",
        "",
        "| 姓名 | 评分 | 占比 | 激励金额 |",
        "|------|------|------|----------|",
    ])

    ratio_sum = sum(config["partner_bonus_ratio"].values())
    for name, amount in result["partner_bonus_result"].items():
        ratio = config["partner_bonus_ratio"][name]
        lines.append(f"| {name} | {ratio:.2f} | {ratio/ratio_sum*100:.1f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "## 六、管理合伙人合计",
        "",
        "| 姓名 | 股东分红(1.5:1:1) | 激励(按评分) | **合计** |",
        "|------|-------------------|--------------|----------|",
    ])

    for name, total in result["partner_total"].items():
        share = result["shareholder_result"].get(f"管理合伙人-{name}", 0)
        bonus = result["partner_bonus_result"].get(name, 0)
        lines.append(f"| {name} | {format_money(share)} | {format_money(bonus)} | **{format_money(total)}** |")

    lines.extend([
        "",
        "## 七、资金储备池汇总",
        "",
        "| 项目 | 金额 | 说明 |",
        "|------|------|------|",
        f"| 历史可分配利润 | {format_money(result['retained_earnings'])} | |",
        f"| 25年预留30% | {format_money(result['reserve_from_2025'])} | |",
        f"| **储备池合计** | **{format_money(result['reserve_pool'])}** | |",
        f"| 预留目标 | {format_money(result['target_reserve'])} | 员工资险金+外挂服务费+AI战略投入 |",
        f"| **差额** | **{format_money(result['reserve_gap'])}** | 需补足 |",
        "",
        "---",
        f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## 附：股权结构",
        "",
        "| 类别 | 姓名/项目 | 股权比例 |",
        "|------|-----------|----------|",
    ])

    for name, share in config["investors"].items():
        lines.append(f"| 股东 | {name} | {share*100:.2f}% |")
    lines.append(f"| 管理合伙人 | KK+刘军+刘伟+股权池 | {sum(config['partner_shares'].values())*100:.2f}% |")
    lines.append(f"| _（分红按1.5:1:1）_ | | |")
    lines.append(f"| 员工 | 员工持股池 | {config['employee_share_total']*100:.1f}% |")

    total_eq = sum(config["investors"].values()) + sum(config["partner_shares"].values()) + config["employee_share_total"]
    lines.append(f"| **合计** | | **{total_eq*100:.2f}%** |")

    return "\n".join(lines)


def main():
    """主函数"""
    result = calculate_distribution(CONFIG)
    md_content = generate_markdown(result, CONFIG)

    # 保存Markdown
    output_path = Path(__file__).parent / f"净利分配_{CONFIG['year']}.md"
    output_path.write_text(md_content, encoding="utf-8")
    print(f"报告已生成: {output_path}")

    # 同时打印到控制台
    print("\n" + md_content)


if __name__ == "__main__":
    main()
