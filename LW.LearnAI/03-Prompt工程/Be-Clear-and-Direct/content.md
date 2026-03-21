# Be Clear, Direct, and Detailed | 清晰、直接、详细

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct

---

When interacting with Claude, think of it as a brilliant but very new employee (with amnesia) who needs explicit instructions. Like any new employee, Claude does not have context on your norms, styles, guidelines, or preferred ways of working.

**与 Claude 交互时，把它想象成一个聪明但非常新的员工（患有健忘症），需要明确的指令。** 就像任何新员工一样，Claude 不了解你的规范、风格、指南或偏好的工作方式。

**The more precisely you explain what you want, the better Claude's response will be.**

**你越精确地解释你想要什么，Claude 的回复就越好。**

---

## The Golden Rule of Clear Prompting | 清晰提示词的黄金法则

Show your prompt to a colleague, ideally someone who has minimal context on the task, and ask them to follow the instructions. If they're confused, Claude will likely be too.

**把你的提示词给一位同事看，最好是几乎没有任务背景的人，让他们按照指令执行。如果他们感到困惑，Claude 很可能也会困惑。**

---

## How to Be Clear, Contextual, and Specific | 如何做到清晰、有上下文、具体

### Give Claude Contextual Information | 给 Claude 上下文信息

Just like you might be able to better perform on a task if you knew more context, Claude will perform better if it has more contextual information.

**就像如果你了解更多上下文可能会在任务上表现得更好一样，如果 Claude 拥有更多上下文信息，它的表现也会更好。**

Some examples of contextual information:

**一些上下文信息的例子：**

- What the task results will be used for
- **任务结果将用于什么**
- What audience the output is meant for
- **输出的目标受众是谁**
- What workflow the task is a part of, and where this task belongs in that workflow
- **任务属于哪个工作流程，以及这个任务在工作流程中的位置**
- The end goal of the task, or what a successful task completion looks like
- **任务的最终目标，或成功的任务完成是什么样的**

### Be Specific About What You Want Claude to Do | 明确告诉 Claude 你想要它做什么

For example, if you want Claude to output only code and nothing else, say so.

**例如，如果你想让 Claude 只输出代码而不输出其他内容，就要说出来。**

### Provide Instructions as Sequential Steps | 以顺序步骤的形式提供指令

Use numbered lists or bullet points to better ensure that Claude carries out the task the exact way you want it to.

**使用编号列表或项目符号，更好地确保 Claude 完全按照你想要的方式执行任务。**

---

## Examples | 示例

### Example 1: Anonymizing Customer Feedback | 示例 1：匿名化客户反馈

Notice that Claude still makes mistakes in the unclear prompting example, such as leaving in a customer's name.

**注意在不清晰的提示词示例中，Claude 仍然会犯错，比如保留了客户姓名。**

#### Unclear Prompt | 不清晰的提示词

```
Please remove all personally identifiable information from these customer feedback messages: {{FEEDBACK_DATA}}
```

**请从这些客户反馈消息中删除所有个人身份信息：{{FEEDBACK_DATA}}**

#### Clear Prompt | 清晰的提示词

```
Your task is to anonymize customer feedback for our quarterly review.

你的任务是为我们的季度审查匿名化客户反馈。

Instructions:
1. Replace all customer names with "CUSTOMER_[ID]" (e.g., "Jane Doe" → "CUSTOMER_001")
2. Replace email addresses with "EMAIL_[ID]@example.com"
3. Redact phone numbers as "PHONE_[ID]"
4. If a message mentions a specific product (e.g., "AcmeCloud"), leave it intact
5. If no PII is found, copy the message verbatim
6. Output only the processed messages, separated by "---"

指令：
1. 将所有客户名称替换为"CUSTOMER_[ID]"（例如，"Jane Doe"→"CUSTOMER_001"）
2. 将电子邮件地址替换为"EMAIL_[ID]@example.com"
3. 将电话号码编校为"PHONE_[ID]"
4. 如果消息提到特定产品（例如"AcmeCloud"），保留它
5. 如果没有找到 PII，逐字复制消息
6. 只输出处理后的消息，用"---"分隔

Data to process: {{FEEDBACK_DATA}}
```

---

### Example 2: Crafting a Marketing Email | 示例 2：撰写营销邮件

Notice that Claude makes up details to fill in the gaps where it lacks context with the vague prompt.

**注意在模糊的提示词中，Claude 会编造细节来填补它缺乏上下文的空白。**

#### Vague Prompt | 模糊的提示词

```
Write a marketing email for our new AcmeCloud features.
```

**为我们的新 AcmeCloud 功能写一封营销邮件。**

#### Specific Prompt | 具体的提示词

```
Your task is to craft a targeted marketing email for our Q3 AcmeCloud feature release.

你的任务是为我们的 Q3 AcmeCloud 功能发布撰写一封针对性的营销邮件。

Instructions:
1. Write for this target audience: Mid-size tech companies (100-500 employees) upgrading from on-prem to cloud
2. Highlight 3 key new features: advanced data encryption, cross-platform sync, and real-time collaboration
3. Tone: Professional yet approachable. Emphasize security, efficiency, and teamwork
4. Include a clear CTA: Free 30-day trial with priority onboarding
5. Subject line: Under 50 chars, mention "security" and "collaboration"
6. Personalization: Use {{COMPANY_NAME}} and {{CONTACT_NAME}} variables

指令：
1. 目标受众：中型科技公司（100-500名员工），从本地部署升级到云端
2. 突出 3 个关键新功能：高级数据加密、跨平台同步和实时协作
3. 语气：专业但平易近人。强调安全性、效率和团队合作
4. 包含明确的 CTA：免费 30 天试用，优先入驻
5. 主题行：50 字符以内，提及"security"和"collaboration"
6. 个性化：使用 {{COMPANY_NAME}} 和 {{CONTACT_NAME}} 变量

Structure:
1. Subject line
2. Email body (150-200 words)
3. CTA button text

结构：
1. 主题行
2. 邮件正文（150-200 字）
3. CTA 按钮文本
```

---

### Example 3: Incident Response | 示例 3：事件响应

Notice that Claude outputs superfluous text and different formatting with the vague prompt.

**注意在模糊的提示词中，Claude 会输出多余的文字和不同的格式。**

#### Vague Prompt | 模糊的提示词

```
Analyze this AcmeCloud outage report and summarize the key points. {{REPORT}}
```

**分析这份 AcmeCloud 故障报告并总结要点。{{REPORT}}**

#### Detailed Prompt | 详细的提示词

```
Analyze this AcmeCloud outage report. Skip the preamble. Keep your response terse and write only the bare bones necessary information.

分析这份 AcmeCloud 故障报告。跳过前言。保持回复简洁，只写出必要的信息。

List only:
1) Cause
2) Duration
3) Impacted services
4) Number of affected users
5) Estimated revenue loss

只列出：
1) 原因
2) 持续时间
3) 受影响的服务
4) 受影响用户数量
5) 预计收入损失

Here's the report: {{REPORT}}
```

---

## Key Takeaways | 关键要点

1. **Context matters** - Provide background information Claude needs
2. **上下文很重要** - 提供 Claude 需要的背景信息

3. **Be explicit** - Don't assume Claude will infer your preferences
4. **要明确** - 不要假设 Claude 会推断你的偏好

5. **Use structure** - Numbered steps and bullet points help Claude follow instructions precisely
6. **使用结构** - 编号步骤和项目符号帮助 Claude 精确遵循指令

7. **Test with humans** - If a human would be confused, Claude will be too
8. **用人类测试** - 如果人类会感到困惑，Claude 也会

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [GitHub Prompting Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
