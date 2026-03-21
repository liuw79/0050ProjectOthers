# GW.ShareMoney - 公司净利分配计算器

## 使用方法

```bash
python3 share_calc.py
```

生成报告：`净利分配_2025.md`

## 配置说明

修改 `share_calc.py` 中的 `CONFIG`：

### 可变参数

| 参数 | 说明 | 当前值 |
|------|------|--------|
| `profit_split` | 分配比例 | 4:3:3（以后可能变） |
| `partner_bonus_ratio` | 年度评分 | 7.17/6.0/5.33（下次一定变） |

### 固定参数

| 参数 | 说明 |
|------|------|
| `net_profit` | 当年净利润 |
| `retained_pool` | 留存资金池 |
| `shareholders` | 股东股权比例 |
| `partner_shares` | 管理合伙人股权比例 |
| `partner_share_ratio` | 股东分红比例 1.5:1:1 |
| `employee_share_total` | 员工持股比例 |

## 分配规则

1. 净利润按 **4:3:3** 分成：股东分红 / 管理合伙人激励 / 储备金
2. 股东分红中：
   - 股东（东哥、慧余）：按股权比例
   - 员工：按股权比例
   - 管理合伙人：按 **1.5:1:1** 固定比例
3. 管理合伙人激励：按**年度评分**分配
4. 储备金进入资金池

## 测试

```bash
python3 -m unittest test_share_calc -v
```
