# Giving Claude a Role with a System Prompt | 通过系统提示词赋予 Claude 角色

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts

---

When using Claude, you can dramatically improve its performance by using the `system` parameter to give it a role. This technique, known as **role prompting**, is the most powerful way to use system prompts with Claude.

**使用 Claude 时，你可以通过 `system` 参数给它一个角色，从而显著提高其性能。** 这种技术被称为**角色提示**，是在 Claude 中使用系统提示词最强大的方式。

The right role can turn Claude from a general assistant into your virtual domain expert!

**正确的角色可以将 Claude 从通用助手变成你的虚拟领域专家！**

**System prompt tips**: Use the `system` parameter to set Claude's role. Put everything else, like task-specific instructions, in the `user` turn instead.

**系统提示词提示**：使用 `system` 参数设置 Claude 的角色。将其他所有内容（如特定任务指令）放在 `user` 轮次中。

---

## Why Use Role Prompting? | 为什么使用角色提示？

| Benefit | Description |
|---------|-------------|
| **Enhanced accuracy** | In complex scenarios like legal analysis or financial modeling, role prompting can significantly boost Claude's performance |
| **提高准确性** | 在法律分析或财务建模等复杂场景中，角色提示可以显著提升 Claude 的表现 |

| **Tailored tone** | Whether you need a CFO's brevity or a copywriter's flair, role prompting adjusts Claude's communication style |
| **定制语气** | 无论你需要 CFO 的简洁还是文案的文采，角色提示都能调整 Claude 的沟通风格 |

| **Improved focus** | By setting the role context, Claude stays more within the bounds of your task's specific requirements |
| **提高专注度** | 通过设置角色上下文，Claude 更能保持在任务特定要求的范围内 |

---

## How to Give Claude a Role | 如何赋予 Claude 角色

Use the `system` parameter in the Messages API to set Claude's role:

**在 Messages API 中使用 `system` 参数设置 Claude 的角色：**

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=2048,
    system="You are a seasoned data scientist at a Fortune 500 company.",  # <-- role prompt
    messages=[
        {"role": "user", "content": "Analyze this dataset for anomalies: <dataset>{{DATASET}}</dataset>"}
    ]
)

print(response.content)
```

**Role prompting tip**: Experiment with roles! A `data scientist` might see different insights than a `marketing strategist` for the same data. A `data scientist specializing in customer insight analysis for Fortune 500 companies` might yield different results still!

**角色提示提示**：尝试不同的角色！对于同样的数据，`数据科学家`可能会看到与`营销策略师`不同的洞察。一位`专门为财富500强公司进行客户洞察分析的数据科学家`可能又会产生不同的结果！

---

## Examples | 示例

### Example 1: Legal Contract Analysis | 示例 1：法律合同分析

**Without a role**, Claude might miss critical issues:

**不使用角色**，Claude 可能会遗漏关键问题：

```
User: Analyze this software licensing agreement for potential risks: <contract>{{CONTRACT}}</contract>
Focus on indemnification, liability, and IP ownership.

用户：分析这份软件许可协议的潜在风险：<contract>{{CONTRACT}}</contract>
关注赔偿、责任和知识产权所有权。
```

**Response**: "Here's a summary... The agreement seems standard..."

**响应**："这是一个摘要...协议看起来是标准的..."

---

**With a role**, Claude catches critical issues that could cost millions:

**使用角色**，Claude 会发现可能造成数百万损失的关键问题：

```
User: You are the General Counsel of a Fortune 500 tech company. We're considering this software licensing agreement for our core data infrastructure: <contract>{{CONTRACT}}</contract>

Analyze it for potential risks, focusing on indemnification, liability, and IP ownership. Give your professional opinion.

用户：你是一家财富500强科技公司的总法律顾问。我们正在考虑将这份软件许可协议用于我们的核心数据基础设施：<contract>{{CONTRACT}}</contract>

分析其潜在风险，关注赔偿、责任和知识产权所有权。给出你的专业意见。
```

**Response**:

```
I've reviewed the software licensing agreement, and I have serious concerns that could expose our company to significant risks:

我已经审查了软件许可协议，我有严重的担忧，可能会使我们的公司面临重大风险：

1. Indemnification (Section 8):
   - Critical Issue: We indemnify the vendor against "any and all claims" arising from our use.
   - Risk: This could hold us liable even for the vendor's negligence or product defects.
   - Recommendation: Reject. Limit our indemnity to claims arising from our violation of the agreement.

1. 赔偿（第8条）：
   - 关键问题：我们对供应商的"任何和所有索赔"进行赔偿，这些索赔源于我们的使用。
   - 风险：即使由于供应商的疏忽或产品缺陷，这也可能使我们承担责任。
   - 建议：拒绝。将我们的赔偿限制在因我们违反协议而产生的索赔。

2. Limitation of Liability (Section 9):
   - Critical Issue: Damages capped at $500, including direct damages.
   - Risk: Grossly inadequate. A critical failure in our data infrastructure could cost us millions in lost revenue and reputational damage.
   - Recommendation: Reject. Negotiate for cap at 12 months of fees for direct damages, and carve-outs for data breaches.

2. 责任限制（第9条）：
   - 关键问题：损害赔偿上限为500美元，包括直接损害。
   - 风险：严重不足。数据基础设施的关键故障可能使我们损失数百万的收入和声誉损害。
   - 建议：拒绝。谈判将直接损害的上限设为12个月的费用，并为数据泄露设置例外。

3. IP Ownership (Section 12):
   - Critical Issue: Vendor gains joint ownership of our modifications and integrations.
   - Risk: They could use or sell our proprietary algorithms or data insights to competitors.
   - Recommendation: Reject. We must retain full ownership of our work.

3. 知识产权所有权（第12条）：
   - 关键问题：供应商获得我们修改和集成的联合所有权。
   - 风险：他们可以将我们的专有算法或数据洞察出售给竞争对手。
   - 建议：拒绝。我们必须保留对我们工作的完全所有权。

Professional Opinion: Do not sign this agreement. It is grossly unfavorable and exposes us to unacceptable levels of risk.

专业意见：不要签署这份协议。它严重不利，使我们面临不可接受的风险水平。
```

---

### Example 2: Financial Analysis | 示例 2：财务分析

**Without a role**, Claude's analysis lacks depth:

**不使用角色**，Claude 的分析缺乏深度：

```
User: Analyze this dataset of our Q2 financials: <data>{{FINANCIALS}}</data>
Highlight key trends and recommend actions.

用户：分析我们的 Q2 财务数据集：<data>{{FINANCIALS}}</data>
突出关键趋势并建议行动。
```

**Response**: Basic summary with generic recommendations...

**响应**：基本摘要和通用建议...

---

**With a role**, Claude delivers actionable insights:

**使用角色**，Claude 提供可操作的洞察：

```
User: You are the CFO of a high-growth B2B SaaS company. We're in a board meeting discussing our Q2 financials: <data>{{FINANCIALS}}</data>

Analyze key trends, flag concerns, and recommend strategic actions. Our investors want aggressive growth but are wary of our burn rate.

用户：你是一家高增长 B2B SaaS 公司的 CFO。我们正在董事会会议上讨论 Q2 财务：<data>{{FINANCIALS}}</data>

分析关键趋势，标记问题，并建议战略行动。我们的投资者希望积极增长，但对我们消耗率持谨慎态度。
```

**Response**:

```
Board members, here's my analysis of our Q2 financials:

董事会成员，这是我对我们 Q2 财务的分析：

1. Revenue ($15.2M, +22% YoY):
   - Insight: Enterprise growth (+30%) is outpacing overall growth.
   - Flag: SMB segment declined 5%.
   - Action: Reallocate 20% of SMB marketing budget to enterprise sales. Task product to simplify SMB onboarding.

1. 收入（1520万美元，同比+22%）：
   - 洞察：企业增长（+30%）超过整体增长。
   - 标记：SMB细分市场下降5%。
   - 行动：将20%的SMB营销预算重新分配给企业销售。让产品团队简化SMB入门。

2. Margins (Gross: 72%, +3% QoQ; EBITDA: 18%, -2% QoQ):
   - Insight: Infrastructure optimizations boosted gross margins.
   - Flag: R&D spend on AI features dented EBITDA.
   - Action: No change. Our AI roadmap is critical for enterprise stickiness.

2. 利润率（毛利率：72%，环比+3%；EBITDA：18%，环比-2%）：
   - 洞察：基础设施优化提高了毛利率。
   - 标记：AI功能的研发支出影响了EBITDA。
   - 行动：不变。我们的AI路线图对企业粘性至关重要。

3. Cash ($4.1M OCF, $28M reserves):
   - Insight: 15-month runway at current burn.
   - Flag: CAC up 20%, eroding LTV/CAC.
   - Action: Freeze non-essential hires. Implement sales funnel analytics to cut CAC by 15% in Q3.

3. 现金（经营现金流410万美元，储备2800万美元）：
   - 洞察：按当前消耗率可维持15个月。
   - 标记：CAC上升20%，侵蚀LTV/CAC。
   - 行动：冻结非必要招聘。实施销售漏斗分析，在Q3将CAC降低15%。

Strategic Stance: We're threading the needle between growth and burn. Enterprise focus is our growth engine—invest there. But watch SMB churn; it could bleed into enterprise. Our AI bet is sound, but we must convert it to ARR by Q4, or we cut R&D by 30%.

战略立场：我们在增长和消耗之间穿针引线。企业聚焦是我们的增长引擎——在那里投资。但要关注SMB流失；它可能蔓延到企业。我们的AI赌注是合理的，但我们必须在Q4将其转化为ARR，否则我们将研发削减30%。

In sum: Double down on enterprise, streamline SMB, optimize sales, and monetize AI. Questions?

总之：加倍投入企业市场，精简SMB，优化销售，并实现AI货币化。有问题吗？
```

---

## Key Takeaways | 关键要点

1. **Use the system parameter** - Set roles through the `system` parameter, not in user messages
2. **使用 system 参数** - 通过 `system` 参数设置角色，而不是在用户消息中

3. **Be specific with roles** - "CFO of a high-growth B2B SaaS company" > "financial analyst"
4. **角色要具体** - "高增长 B2B SaaS 公司的 CFO" > "财务分析师"

5. **Match expertise to task** - Choose roles with relevant domain knowledge
6. **专业知识匹配任务** - 选择具有相关领域知识的角色

7. **Keep task instructions in user turn** - The system prompt is for role, user message is for task
8. **任务指令放在用户轮次** - 系统提示词用于角色，用户消息用于任务

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [Prefill Response](./Prefill-Response/content.md)
