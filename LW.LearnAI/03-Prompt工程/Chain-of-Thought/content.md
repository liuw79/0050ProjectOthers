# Let Claude Think (Chain of Thought Prompting) | 让 Claude 思考（链式思考提示）

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought

---

When faced with complex tasks like research, analysis, or problem-solving, giving Claude space to think can dramatically improve its performance. This technique, known as **chain of thought (CoT) prompting**, encourages Claude to break down problems step-by-step, leading to more accurate and nuanced outputs.

**面对研究、分析或问题解决等复杂任务时，给 Claude 留出思考空间可以显著提高其性能。** 这种技术被称为**链式思考（CoT）提示**，鼓励 Claude 逐步分解问题，从而产生更准确、更细致的输出。

---

## Before Implementing CoT | 在实施 CoT 之前

### Why Let Claude Think? | 为什么让 Claude 思考？

- **Accuracy**: Stepping through problems reduces errors, especially in math, logic, analysis, or generally complex tasks
- **准确性**：逐步解决问题可以减少错误，特别是在数学、逻辑、分析或通常复杂的任务中

- **Coherence**: Structured thinking leads to more cohesive, well-organized responses
- **连贯性**：结构化思考带来更连贯、更有组织的响应

- **Debugging**: Seeing Claude's thought process helps you pinpoint where prompts may be unclear
- **调试**：看到 Claude 的思考过程帮助你确定提示词可能不清楚的地方

### Why Not Let Claude Think? | 为什么不让 Claude 思考？

- Increased output length may impact latency
- **输出长度增加可能会影响延迟**

- Not all tasks require in-depth thinking
- **并非所有任务都需要深入思考**

Use CoT for tasks that a human would need to think through, like complex math, multi-step analysis, writing complex documents, or decisions with many factors.

**对人类需要思考的任务使用 CoT，比如复杂计算、多步分析、撰写复杂文档或有多种因素的决策。**

---

## How to Prompt for Thinking | 如何提示思考

The chain of thought techniques below are **ordered from least to most complex**. Less complex methods take up less space in the context window, but are also generally less powerful.

**下面的链式思考技术按从最简单到最复杂的顺序排列。** 较简单的方法占用上下文窗口的空间较少，但通常也较弱。

**CoT tip**: Always have Claude output its thinking. Without outputting its thought process, no thinking occurs!

**CoT 提示**：始终让 Claude 输出其思考。如果不输出思考过程，就不会发生思考！

---

### 1. Basic Prompt | 1. 基础提示

Include "Think step-by-step" in your prompt.

**在提示词中包含"逐步思考"。**

- Lacks guidance on *how* to think (which is especially not ideal if a task is very specific to your app, use case, or organization)
- **缺乏关于*如何*思考的指导**（不适合特定于你的应用、用例或组织的任务）

```
Draft personalized emails to donors asking for contributions to this year's Care for Kids program.
为今年的"关爱儿童"项目撰写个性化捐款请求邮件。

Program information: <program>{{PROGRAM_DETAILS}}</program>
项目信息：<program>{{PROGRAM_DETAILS}}</program>

Donor information: <donor>{{DONOR_DETAILS}}</donor>
捐款人信息：<donor>{{DONOR_DETAILS}}</donor>

Think step-by-step before you write the email.
在写邮件之前逐步思考。
```

---

### 2. Guided Prompt | 2. 引导式提示

Outline specific steps for Claude to follow in its thinking process.

**概述 Claude 在思考过程中应遵循的具体步骤。**

- Lacks structuring to make it easy to strip out and separate the answer from the thinking
- **缺乏结构化**，难以将答案与思考分离

```
Draft personalized emails to donors asking for contributions to this year's Care for Kids program.
为今年的"关爱儿童"项目撰写个性化捐款请求邮件。

Program information: <program>{{PROGRAM_DETAILS}}</program>
项目信息：<program>{{PROGRAM_DETAILS}}</program>

Donor information: <donor>{{DONOR_DETAILS}}</donor>
捐款人信息：<donor>{{DONOR_DETAILS}}</donor>

Think before you write the email. First, think through what messaging might appeal to this donor given their donation history and which campaigns they've supported in the past. Then, think through what aspects of the Care for Kids program would appeal to them, given their history. Finally, write the personalized donor email using your analysis.

在写邮件之前思考。首先，考虑这位捐款人的捐款历史和过去支持的活动，思考什么样的信息可能会吸引他们。然后，根据他们的历史，思考"关爱儿童"项目的哪些方面会吸引他们。最后，利用你的分析撰写个性化捐款邮件。
```

---

### 3. Structured Prompt | 3. 结构化提示

Use XML tags like `<thinking>` and `<answer>` to separate reasoning from the final answer.

**使用 XML 标签如 `<thinking>` 和 `<answer>` 将推理与最终答案分离。**

```
Draft personalized emails to donors asking for contributions to this year's Care for Kids program.
为今年的"关爱儿童"项目撰写个性化捐款请求邮件。

Program information: <program>{{PROGRAM_DETAILS}}</program>
项目信息：<program>{{PROGRAM_DETAILS}}</program>

Donor information: <donor>{{DONOR_DETAILS}}</donor>
捐款人信息：<donor>{{DONOR_DETAILS}}</donor>

Think before you write the email in <thinking> tags. First, think through what messaging might appeal to this donor given their donation history and which campaigns they've supported in the past. Then, think through what aspects of the Care for Kids program would appeal to them, given their history. Finally, write the personalized donor email in <email> tags, using your analysis.

在 <thinking> 标签中写邮件之前思考。首先，考虑这位捐款人的捐款历史和过去支持的活动，思考什么样的信息可能会吸引他们。然后，根据他们的历史，思考"关爱儿童"项目的哪些方面会吸引他们。最后，在 <email> 标签中撰写个性化捐款邮件，利用你的分析。
```

---

## Example: Financial Analysis | 示例：财务分析

### Without Thinking | 不使用思考

Without step-by-step thinking, Claude gives a recommendation that seems reasonable but lacks depth. It doesn't quantify the potential outcomes or consider historical market performance.

**不使用逐步思考，Claude 给出的建议看起来合理但缺乏深度。它没有量化潜在结果或考虑历史市场表现。**

```
You're a financial advisor. A client wants to invest $10,000. They can choose between two options:
A) A stock that historically returns 12% annually but is volatile
B) A bond that guarantees 6% annually
The client needs the money in 5 years for a down payment on a house.
Which option do you recommend?

你是一位财务顾问。客户想投资10,000美元。他们可以在两个选项中选择：
A) 一只历史年回报率12%但波动较大的股票
B) 一只保证年回报率6%的债券
客户需要在5年后用这笔钱作为购房首付。
你推荐哪个选项？
```

### With Thinking | 使用思考

With step-by-step thinking, the advisor provides a much richer analysis. It calculates exact figures for both scenarios, considers historical market volatility, and deeply analyzes the client's risk tolerance.

**使用逐步思考，顾问提供了更丰富的分析。它计算了两种情况的精确数字，考虑了历史市场波动性，并深入分析了客户的风险承受能力。**

```
To determine the best investment option for our client, I'll consider several factors step-by-step:

<thinking>
1. Understand the client's goal and timeline:
   理解客户的目标和时间线：
   - Goal: Down payment for a house
   - 目标：购房首付
   - Timeline: 5 years
   - 时间线：5年
   - Implication: This is a short-term, high-priority financial goal. The client likely cannot afford significant risk or volatility.
   - 影响：这是一个短期、高优先级的财务目标。客户可能无法承受重大风险或波动。

2. Analyze Option A (Stock):
   分析选项A（股票）：
   - Pro: Higher historical return (12% annually)
   - 优点：历史回报率较高（年12%）
   - Con: Volatile (implying potential for significant gains or losses)
   - 缺点：波动大（意味着可能有显著收益或损失）
   - Calculate potential 5-year return:
   - 计算5年潜在回报：
   - Best case (12% annually): $10,000 * (1.12)^5 ≈ $17,623.42
   - 最佳情况（年12%）：$10,000 * (1.12)^5 ≈ $17,623.42
   - Worst case (market crash): Could lose a substantial portion, e.g., 50% crash = $5,000
   - 最差情况（市场崩盘）：可能损失大部分，例如50%崩盘 = $5,000

3. Analyze Option B (Bond):
   分析选项B（债券）：
   - Pro: Guaranteed return (6% annually)
   - 优点：保证回报（年6%）
   - Con: Lower return compared to historical stock performance
   - 缺点：比历史股票表现回报率低
   - Calculate 5-year return:
   - 计算5年回报：
   - Guaranteed: $10,000 * (1.06)^5 ≈ $13,382.25
   - 保证：$10,000 * (1.06)^5 ≈ $13,382.25

4. Consider risk tolerance:
   考虑风险承受能力：
   - Goal is a house down payment (essential, not discretionary)
   - 目标是购房首付（必要，非可选）
   - Short timeline (5 years) limits ability to recover from market downturns
   - 短时间线（5年）限制了从市场下跌中恢复的能力
   - Conclusion: Client likely has low risk tolerance
   - 结论：客户可能有低风险承受能力

5. Final analysis:
   最终分析：
   - Option A (Stock): Higher potential return but unacceptable risk of not meeting the down payment goal
   - 选项A（股票）：更高潜在回报但不满足首付目标的风险不可接受
   - Option B (Bond): Guaranteed to meet ~80% of best-case stock scenario, 100% certainty of having funds
   - 选项B（债券）：保证达到最佳股票情况的~80%，100%确定有资金
</thinking>

<answer>
I recommend Option B, the bond with a guaranteed 6% annual return. While the stock's historical 12% return is tempting, the bond ensures you'll have $13,382.25 in 5 years for your house down payment. Given the importance and short timeline of your goal, the stock's volatility poses an unacceptable risk.

我推荐选项B，即保证6%年回报率的债券。虽然股票历史12%的回报率很诱人，但债券确保你在5年后有$13,382.25用于购房首付。鉴于你目标的重要性和短时间线，股票的波动性构成不可接受的风险。
</answer>
```

---

## Key Takeaways | 关键要点

1. **Use CoT for complex tasks** - Math, analysis, multi-step reasoning
2. **对复杂任务使用 CoT** - 数学、分析、多步推理

3. **Always output the thinking** - Claude must express its reasoning
4. **始终输出思考** - Claude 必须表达其推理

5. **Structure with XML tags** - Makes it easy to parse thinking from answer
6. **用 XML 标签结构化** - 便于解析思考和答案

7. **Guide the thinking process** - Specify what Claude should consider
8. **引导思考过程** - 指定 Claude 应该考虑什么

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [Extended Thinking](../06-高级功能/Extended-Thinking/content.md)
