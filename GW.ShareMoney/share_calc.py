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
    "retained_pool": 10430000,      # 留存资金池（不参与本次分配）1043万
    "net_profit": 19470000,         # 25年净利润 1947万（本次分配金额）

    # 净利分配比例（股东分红:管理合伙人激励:储备金）
    "profit_split": {
        "shareholder": 0.4,      # 股东分红 40%
        "partner_bonus": 0.3,    # 管理合伙人激励 30%
        "reserve": 0.3           # 储备金 30%（进入资金池）
    },

    # ===== 股权结构 =====
    # 股东（非管理合伙人）
    "shareholders": {
        "东哥": 0.049,
        "慧余": 0.1704,
    },

    # 管理合伙人（股东分红用）
    "partner_shares": {
        "刘军": 0.13,
        "刘伟": 0.16,
        "KK": 0.395,
        "股权池": 0.0456,
    },

    # 员工股权
    "employee_share_total": 0.05,  # 约5%
    "employees_detail": {},  # 待填入明细

    # 股东分红中管理合伙人部分的分配比例（固定比例）
    "partner_share_ratio": {
        "KK": 1.5,
        "刘军": 1.0,
        "刘伟": 1.0
    },

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
    """计算管理合伙人分配（按比例）"""
    ratio_sum = sum(partner_ratio.values())
    return {
        name: total * (ratio / ratio_sum)
        for name, ratio in partner_ratio.items()
    }


def calculate_distribution(config: dict) -> dict:
    """计算完整的利润分配"""

    # 1. 资金来源
    net_profit = config["net_profit"]
    retained_pool = config["retained_pool"]

    # 2. 按 4:3:3 分配
    shareholder_total = net_profit * config["profit_split"]["shareholder"]
    partner_bonus_total = net_profit * config["profit_split"]["partner_bonus"]
    reserve_total = net_profit * config["profit_split"]["reserve"]

    # 3. 计算总股权
    total_equity = (
        sum(config["shareholders"].values()) +
        sum(config["partner_shares"].values()) +
        config["employee_share_total"]
    )

    # 4. 股东分红分配
    shareholder_result = {}

    # 4.1 股东按股权比例分
    for name, share in config["shareholders"].items():
        shareholder_result[f"股东-{name}"] = shareholder_total * (share / total_equity)

    # 4.2 员工按股权比例分
    shareholder_result["员工合伙人"] = shareholder_total * (config["employee_share_total"] / total_equity)

    # 4.3 管理合伙人（含股权池）按固定比例分配，不是按股权比例
    partner_pool = shareholder_total * (sum(config["partner_shares"].values()) / total_equity)
    partner_share_result = calc_partner_bonus(partner_pool, config["partner_share_ratio"])
    for name, amount in partner_share_result.items():
        shareholder_result[f"管理合伙人-{name}"] = amount

    # 5. 管理合伙人激励（仅KK、刘军、刘伟参与）
    partner_bonus_result = calc_partner_bonus(partner_bonus_total, config["partner_bonus_ratio"])

    # 6. 管理合伙人合计
    partner_total = {}
    for name in ["KK", "刘军", "刘伟"]:
        partner_total[name] = shareholder_result.get(f"管理合伙人-{name}", 0) + partner_bonus_result.get(name, 0)

    # 7. 更新后的留存资金池
    new_retained_pool = retained_pool + reserve_total

    return {
        "year": config["year"],
        "net_profit": net_profit,
        "retained_pool": retained_pool,
        "shareholder_total": shareholder_total,
        "partner_bonus_total": partner_bonus_total,
        "reserve_total": reserve_total,
        "total_equity": total_equity,
        "shareholder_result": shareholder_result,
        "partner_bonus_result": partner_bonus_result,
        "partner_total": partner_total,
        "new_retained_pool": new_retained_pool,
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
        f"| 留存资金池（不动） | {format_money(result['retained_pool'])} |",
        f"| 25年净利润（本次分配） | {format_money(result['net_profit'])} |",
        "",
        "## 二、分配比例（4:3:3）",
        "",
        "| 项目 | 比例 | 金额 |",
        "|------|------|------|",
        f"| 股东分红 | 40% | {format_money(result['shareholder_total'])} |",
        f"| 管理合伙人激励 | 30% | {format_money(result['partner_bonus_total'])} |",
        f"| 储备金（进入资金池） | 30% | {format_money(result['reserve_total'])} |",
        "",
        "## 三、股东分红明细",
        "",
        f"股东分红总额: **{format_money(result['shareholder_total'])}**",
        "",
        "### 3.1 股东分红（按股权比例）",
        "",
        "| 姓名 | 股权比例 | 分红金额 |",
        "|------|----------|----------|",
    ]

    for name, share in config["shareholders"].items():
        key = f"股东-{name}"
        amount = result["shareholder_result"][key]
        lines.append(f"| {name} | {share*100:.2f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "### 3.2 管理合伙人分红（1.5:1:1，含股权池）",
        "",
        "| 姓名 | 比例 | 分红金额 |",
        "|------|------|----------|",
    ])

    ratio_sum = sum(config["partner_share_ratio"].values())
    for name in ["KK", "刘军", "刘伟"]:
        key = f"管理合伙人-{name}"
        amount = result["shareholder_result"][key]
        ratio = config["partner_share_ratio"][name]
        lines.append(f"| {name} | {ratio/ratio_sum*100:.1f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "### 3.3 员工合伙人分红",
        "",
        "| 项目 | 股权比例 | 分红金额 | 备注 |",
        "|------|----------|----------|------|",
    ])

    emp_amount = result["shareholder_result"]["员工合伙人"]
    lines.append(f"| 员工持股池 | {config['employee_share_total']*100:.1f}% | {format_money(emp_amount)} | 明细待补充 |")

    lines.extend([
        "",
        "## 四、管理合伙人激励（按年度评分）",
        "",
        "| 姓名 | 评分 | 比例 | 激励金额 |",
        "|------|------|------|----------|",
    ])

    ratio_sum = sum(config["partner_bonus_ratio"].values())
    for name, amount in result["partner_bonus_result"].items():
        ratio = config["partner_bonus_ratio"][name]
        lines.append(f"| {name} | {ratio:.2f} | {ratio/ratio_sum*100:.1f}% | {format_money(amount)} |")

    lines.extend([
        "",
        "## 五、管理合伙人合计",
        "",
        "| 姓名 | 股东分红 | 激励 | **合计** |",
        "|------|----------|------|----------|",
    ])

    for name, total in result["partner_total"].items():
        share = result["shareholder_result"].get(f"管理合伙人-{name}", 0)
        bonus = result["partner_bonus_result"].get(name, 0)
        lines.append(f"| {name} | {format_money(share)} | {format_money(bonus)} | **{format_money(total)}** |")

    lines.extend([
        "",
        "## 六、储备金",
        "",
        "| 项目 | 金额 | 说明 |",
        "|------|------|------|",
        f"| 本年储备金（30%） | {format_money(result['reserve_total'])} | 进入资金池 |",
        f"| 原留存资金池 | {format_money(result['retained_pool'])} | |",
        f"| **更新后资金池** | **{format_money(result['new_retained_pool'])}** | |",
        "",
        "---",
        f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])

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
