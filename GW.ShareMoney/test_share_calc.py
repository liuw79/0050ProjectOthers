#!/usr/bin/env python3
"""
单元测试：净利分配计算器
"""

import unittest
from share_calc import (
    calculate_distribution,
    calc_partner_bonus,
    CONFIG
)


class TestShareCalc(unittest.TestCase):
    """净利分配计算测试"""

    def setUp(self):
        """测试前准备"""
        self.result = calculate_distribution(CONFIG)

    def test_profit_split_4_3_3(self):
        """测试 4:3:3 分配"""
        net_profit = CONFIG["net_profit"]

        # 40% 股东分红
        expected_shareholder = net_profit * 0.4
        self.assertEqual(self.result["shareholder_total"], expected_shareholder)

        # 30% 管理合伙人激励
        expected_bonus = net_profit * 0.3
        self.assertEqual(self.result["partner_bonus_total"], expected_bonus)

        # 30% 储备金
        expected_reserve = net_profit * 0.3
        self.assertEqual(self.result["reserve_total"], expected_reserve)

        print(f"✓ 4:3:3 分配: 股东{expected_shareholder/10000:.2f}万 + 激励{expected_bonus/10000:.2f}万 + 储备{expected_reserve/10000:.2f}万")

    def test_three_parts_sum(self):
        """测试三部分总和 = 净利润"""
        total = (self.result["shareholder_total"] +
                 self.result["partner_bonus_total"] +
                 self.result["reserve_total"])

        self.assertAlmostEqual(total, CONFIG["net_profit"], places=2)
        print(f"✓ 三部分总和: {total/10000:.2f}万 = 净利润")

    def test_retained_pool_update(self):
        """测试留存资金池更新"""
        expected = CONFIG["retained_pool"] + self.result["reserve_total"]
        self.assertEqual(self.result["new_retained_pool"], expected)
        print(f"✓ 资金池更新: {CONFIG['retained_pool']/10000:.2f}万 + {self.result['reserve_total']/10000:.2f}万 = {expected/10000:.2f}万")

    def test_shareholder_pool_sum(self):
        """测试股东分红池分配总和"""
        total = sum(self.result["shareholder_result"].values())
        expected = self.result["shareholder_total"]

        self.assertAlmostEqual(total, expected, places=2)
        print(f"✓ 股东分红池总和: {total/10000:.2f}万")

    def test_partner_bonus_pool_sum(self):
        """测试管理合伙人激励总和"""
        total = sum(self.result["partner_bonus_result"].values())
        expected = self.result["partner_bonus_total"]

        self.assertAlmostEqual(total, expected, places=2)
        print(f"✓ 管理合伙人激励总和: {total/10000:.2f}万")

    def test_partner_share_ratio_1_5_1_1(self):
        """【核心测试】股东分红中管理合伙人按1.5:1:1比例分配"""
        kk_share = self.result["shareholder_result"]["管理合伙人-KK"]
        liujun_share = self.result["shareholder_result"]["管理合伙人-刘军"]
        liuwei_share = self.result["shareholder_result"]["管理合伙人-刘伟"]

        # KK : 刘军 = 1.5 : 1
        kk_liujun_ratio = kk_share / liujun_share
        self.assertAlmostEqual(kk_liujun_ratio, 1.5, places=2)

        # 刘军 : 刘伟 = 1 : 1
        liujun_liuwei_ratio = liujun_share / liuwei_share
        self.assertAlmostEqual(liujun_liuwei_ratio, 1.0, places=2)

        print(f"✓ KK/刘军比例: {kk_liujun_ratio:.2f} (应为1.5)")
        print(f"✓ 刘军/刘伟比例: {liujun_liuwei_ratio:.2f} (应为1.0)")

    def test_shareholders_get_correct_amount(self):
        """测试股东分红金额"""
        result = self.result["shareholder_result"]

        # 东哥: 778.8万 × 4.90% = 38.16万
        expected_dongge = 7788000 * 0.049
        self.assertAlmostEqual(result["股东-东哥"], expected_dongge, places=0)

        # 慧余: 778.8万 × 17.04% = 132.70万
        expected_huiyu = 7788000 * 0.1704
        self.assertAlmostEqual(result["股东-慧余"], expected_huiyu, places=0)

        print(f"✓ 东哥分红: {result['股东-东哥']/10000:.2f}万")
        print(f"✓ 慧余分红: {result['股东-慧余']/10000:.2f}万")

    def test_partner_bonus_by_score(self):
        """【核心测试】管理合伙人激励按年度评分分配"""
        kk_bonus = self.result["partner_bonus_result"]["KK"]
        liujun_bonus = self.result["partner_bonus_result"]["刘军"]
        liuwei_bonus = self.result["partner_bonus_result"]["刘伟"]

        # 按评分比例: 7.17 : 6.0 : 5.33
        expected_ratio_kk = 7.17 / 5.33
        expected_ratio_liujun = 6.0 / 5.33

        actual_ratio_kk = kk_bonus / liuwei_bonus
        actual_ratio_liujun = liujun_bonus / liuwei_bonus

        self.assertAlmostEqual(actual_ratio_kk, expected_ratio_kk, places=2)
        self.assertAlmostEqual(actual_ratio_liujun, expected_ratio_liujun, places=2)

        print(f"✓ KK激励/刘伟激励: {actual_ratio_kk:.2f} (应为{expected_ratio_kk:.2f})")
        print(f"✓ 刘军激励/刘伟激励: {actual_ratio_liujun:.2f} (应为{expected_ratio_liujun:.2f})")


class TestCalcPartnerBonus(unittest.TestCase):
    """测试 calc_partner_bonus 函数"""

    def test_equal_ratio(self):
        """等比例分配"""
        total = 300
        ratio = {"A": 1, "B": 1, "C": 1}
        result = calc_partner_bonus(total, ratio)

        self.assertEqual(result["A"], 100)
        self.assertEqual(result["B"], 100)
        self.assertEqual(result["C"], 100)
        print("✓ 等比例分配测试通过")

    def test_1_5_1_1_ratio(self):
        """1.5:1:1 比例分配"""
        total = 350
        ratio = {"KK": 1.5, "刘军": 1.0, "刘伟": 1.0}
        result = calc_partner_bonus(total, ratio)

        self.assertEqual(result["KK"], 150)
        self.assertEqual(result["刘军"], 100)
        self.assertEqual(result["刘伟"], 100)
        print("✓ 1.5:1:1 比例分配测试通过")


if __name__ == "__main__":
    print("=" * 60)
    print("净利分配计算器 - 单元测试")
    print("=" * 60)
    print()

    unittest.main(verbosity=2)
