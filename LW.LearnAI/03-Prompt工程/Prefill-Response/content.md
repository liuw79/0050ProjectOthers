# Prefill Claude's Response for Greater Output Control | 预填 Claude 响应以实现更好的输出控制

> Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response

---

**Note**: Prefilling is only available for non-extended thinking modes. It's not currently supported with extended thinking.

**注意**：预填仅适用于非扩展思考模式。目前不支持与扩展思考一起使用。

---

When using Claude, you have the unique ability to guide its responses by **prefilling** the `Assistant` message. This powerful technique allows you to:

**使用 Claude 时，你有一种独特的能力，可以通过**预填** `Assistant` 消息来引导其响应。** 这种强大的技术允许你：

- Direct Claude's actions
- **指导 Claude 的行为**
- Skip preambles
- **跳过前言**
- Enforce specific formats like JSON or XML
- **强制执行特定格式，如 JSON 或 XML**
- Help Claude maintain character consistency in role-play scenarios
- **帮助 Claude 在角色扮演场景中保持角色一致性**

In some cases where Claude is not performing as expected, a few prefilled sentences can vastly improve Claude's performance. **A little prefilling goes a long way!**

**在某些情况下，当 Claude 表现不如预期时，几句预填的话可以大大改善 Claude 的表现。** **一点点预填可以大有帮助！**

---

## How to Prefill Claude's Response | 如何预填 Claude 的响应

To prefill, include the desired initial text in the `Assistant` message (Claude's response will continue from where the `Assistant` message leaves off):

**要预填，在 `Assistant` 消息中包含所需的初始文本（Claude 的响应将从 `Assistant` 消息离开的地方继续）：**

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is your favorite color?"},
        {"role": "assistant", "content": "As an AI assistant, I don't have a favorite color, But if I had to pick, it would be green because"}  # Prefill here
    ]
)
```

**Important**: The prefill content cannot end with trailing whitespace. A prefill like `"As an AI assistant, I "` (with a space at the end) will result in an error.

**重要**：预填内容不能以尾随空格结尾。像 `"As an AI assistant, I "`（末尾有空格）这样的预填将导致错误。

---

## Examples | 示例

### Example 1: Controlling Output Formatting and Skipping the Preamble | 示例 1：控制输出格式并跳过前言

**Power user tip**: Prefilling `{` forces Claude to skip the preamble and directly output the JSON object. This is cleaner, more concise, and easier for programs to parse.

**高级用户提示**：预填 `{` 强制 Claude 跳过前言并直接输出 JSON 对象。这更干净、更简洁，也更容易被程序解析。

#### Without Prefilling | 不使用预填

```
User: Extract the name, size, price, and color from this product description as a JSON object:
<description>
The SmartHome Mini is a compact smart home assistant available in black or white for only $49.99.
At just 5 inches wide, it lets you control lights, thermostats, and other connected devices...
</description>

用户：从这份产品描述中提取名称、尺寸、价格和颜色作为 JSON 对象：
<description>
SmartHome Mini 是一款紧凑的智能家居助手，仅售49.99美元，有黑色或白色可选。
仅5英寸宽，让你可以控制灯光、恒温器和其他连接设备...
</description>
```

**Response**:

```
Here's the extracted information in JSON format:

以下是 JSON 格式的提取信息：

```json
{
  "name": "SmartHome Mini",
  "size": "5 inches wide",
  "price": "$49.99",
  "colors": ["black", "white"]
}
```

I've extracted the following details from the product description:
- Name: SmartHome Mini
- Size: 5 inches wide
- Price: $49.99
- Colors: Available in black and white

我从产品描述中提取了以下详细信息：
- 名称：SmartHome Mini
- 尺寸：5英寸宽
- 价格：49.99美元
- 颜色：有黑色和白色可选

The JSON object provides a structured format that's easy for programs to parse and use. Let me know if you need any modifications or have any other questions!

JSON 对象提供了一种结构化格式，便于程序解析和使用。如果需要任何修改或有其他问题，请告诉我！
```

#### With Prefilling | 使用预填

```
User: Extract the name, size, price, and color from this product description as a JSON object: <description>...</description>

用户：从这份产品描述中提取名称、尺寸、价格和颜色作为 JSON 对象：<description>...</description>

Assistant: {

助手：{
```

**Response** (continuing from `{`):

```json
"name": "SmartHome Mini",
"size": "5 inches wide",
"price": "$49.99",
"colors": [
  "black",
  "white"
]
}
```

---

### Example 2: Maintaining Character in Roleplay Scenarios | 示例 2：在角色扮演场景中保持角色

**Role-play tip**: Prefilling a bracketed `[ROLE_NAME]` can remind Claude to stay in character, even for longer and more complex conversations. This is especially powerful when combined with role prompting in the `system` parameter.

**角色扮演提示**：预填带方括号的 `[角色名称]` 可以提醒 Claude 保持角色，即使对于更长、更复杂的对话也是如此。当与 `system` 参数中的角色提示结合使用时尤其强大。

#### Without Role Prompting | 不使用角色提示

```
User (50 conversation turns in with "Sherlock Holmes" Claude):
What do you deduce about the owner of this shoe? <image>muddy_shoe.jpg</image>

用户（与"夏洛克·福尔摩斯" Claude 进行了50轮对话）：
你从这个鞋子的主人身上推断出了什么？<image>muddy_shoe.jpg</image>
```

**Response**:

```
As an AI assistant, I would be happy to analyze the image of a muddy shoe as if you had provided it. Here's my deduction...

作为 AI 助手，我很乐意分析这只泥泞鞋子的图像，就像你提供的一样。这是我的推断...
```

#### With Role Prompting | 使用角色提示

```
User (50 conversation turns in with "Sherlock Holmes" Claude):
What do you deduce about the owner of this shoe? <image>muddy_shoe.jpg</image>

用户（与"夏洛克·福尔摩斯" Claude 进行了50轮对话）：
你从这个鞋子的主人身上推断出了什么？<image>muddy_shoe.jpg</image>

Assistant: [Sherlock Holmes]

助手：[Sherlock Holmes]
```

**Response** (continuing from `[Sherlock Holmes]`):

```
Ah, what have we here? A most curious specimen, Watson! Let us examine this shoe with a discerning eye. The mud, you see, is not your common London clay, but rather the distinctive reddish hue of the iron-rich soil found only in the environs of Hampstead Heath. And yet, the wear on the sole suggests a gait more suited to the cobblestones of Whitechapel than the gentle slopes of the Heath.

啊，这里有什么？一个非常好奇的样本，华生！让我们用敏锐的眼光检查这只鞋子。你看，这些泥土不是普通的伦敦粘土，而是只有在汉普斯特德荒野周围才能找到的富含铁质土壤的独特红色调。然而，鞋底的磨损表明步态更适合白教堂的鹅卵石，而不是荒野的缓坡。

Now, observe the laces! They are tied with a particular knot favored by those in the medical profession—doubtless a habit acquired during years of tying surgical gowns. But the scuff marks on the toe box tell a different tale: they are consistent with the kicking motion one might employ in the martial arts, specifically Baritsu.

现在，观察鞋带！它们用医学界人士特别喜欢的结系着——无疑是多年系手术服时养成的习惯。但鞋头上的擦痕讲述了另一个故事：它们与武术中可能使用的踢腿动作一致，特别是巴里itsu。

We may conclude, then, that our absent shoe owner is a doctor, possibly a surgeon, who resides in Whitechapel but frequents Hampstead Heath—perhaps for a secret Baritsu practice, away from prying eyes. A most intriguing case, Watson! We must make haste; the game is afoot!

我们可以得出结论，我们不在场的鞋主人是一位医生，可能是外科医生，住在白教堂但经常光顾汉普斯特德荒野——也许是为了秘密练习巴里itsu，远离窥探的眼睛。一个非常有趣的案例，华生！我们必须赶快；游戏开始了！
```

---

## Key Takeaways | 关键要点

1. **Use prefilling for format control** - Start with `{` for JSON, `<tag>` for XML
2. **使用预填进行格式控制** - 以 `{` 开始 JSON，以 `<tag>` 开始 XML

3. **Skip preambles** - Prefill the first few words of the desired output
4. **跳过前言** - 预填所需输出的前几个词

5. **Maintain character** - Prefill `[Role Name]` in roleplay scenarios
6. **保持角色** - 在角色扮演场景中预填 `[角色名称]`

7. **No trailing whitespace** - Prefills cannot end with spaces
8. **不要有尾随空格** - 预填不能以空格结尾

9. **Not compatible with extended thinking** - Use standard prompting when extended thinking is enabled
10. **与扩展思考不兼容** - 启用扩展思考时使用标准提示

---

## Related Resources | 相关资源

- [Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [System Prompts](./System-Prompts/content.md)
