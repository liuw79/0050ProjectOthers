# Skills 描述诊断报告

**生成时间**: 2026-03-11
**评估数量**: 19 个 skills

---

## 诊断标准

根据 Anthropic 官方 skill-creator 最佳实践，好的描述应该：

1. **明确功能** - 清楚说明 skill 做什么
2. **明确触发** - 具体说明什么时候应该触发
3. **避免 Undertrigger** - 描述要"pushy"，主动引导触发
4. **语言一致** - 与用户主要语言匹配（中文用户用中文描述）

---

## 诊断结果总览

| Skill | 评分 | 主要问题 |
|-------|------|----------|
| 文章蓝军 | ⭐⭐⭐⭐ | 良好，有完整触发方式 |
| 3w-decode | ⭐⭐⭐ | 英文描述，缺少 pushy 触发词 |
| asset-produce | ⭐⭐⭐ | 英文描述，触发条件不够具体 |
| coaching-interview | ⭐⭐⭐⭐ | 良好，有中文触发方式 |
| customer-profile | ⭐⭐ | 英文描述，缺少中文触发词 |
| deepseek-to-obsidian | ⭐⭐⭐⭐ | 良好 |
| desensitize | ⭐⭐ | 英文描述，缺少中文触发词 |
| extracting-golden-quotes | ⭐⭐ | 描述太简短 |
| gemini-api | ⭐⭐⭐⭐ | 良好，有完整触发方式 |
| glossary-extract | ⭐⭐ | 英文描述，缺少中文触发词 |
| knowledge-extractor | ⭐⭐⭐ | 与 3w-decode 可能冲突 |
| naming-convention | ⭐⭐ | 描述太简短，缺少触发指导 |
| publish-feishu | ⭐⭐ | 英文描述，缺少中文触发词 |
| send-email | ⭐⭐⭐⭐ | 良好，有完整触发方式 |
| strategic-questioning | ⭐⭐⭐ | 英文描述 |
| trust-storyteller | ⭐⭐⭐ | 英文描述 |
| txt-preprocess | ⭐⭐⭐ | 英文描述 |
| update-wiki-homepage | ⭐⭐ | 描述太简短 |
| wechat-article | ⭐⭐ | 描述为空或缺失 |

---

## 详细诊断与改进建议

### 🔴 高优先级（需要大幅改进）

#### 1. wechat-article
**当前描述**: (缺失或为空)
**问题**: 无法触发
**建议描述**:
```
公众号写作技能。用于撰写高维学堂公众号文章。当用户说"写文章"、"公众号"、"推文"、"发公众号"或要求写任何微信公众号内容时，必须使用此技能。包括选题讨论、大纲设计、正文撰写、标题优化等全流程。
```

#### 2. extracting-golden-quotes
**当前描述**: `Use when extracting 金句 from course transcripts or lectures - must use raw transcript files, not processed notes`
**问题**: 太简短，缺少完整触发场景
**建议描述**:
```
金句提取技能。从课程逐字稿中提取精彩金句。当用户说"提取金句"、"找金句"、"课程金句"或需要从长文本中找出可直接引用的精彩句子时调用。必须使用原始逐字稿文件，不能使用已处理过的笔记。
```

#### 3. naming-convention
**当前描述**: `知识资产命名规范。创建、重命名、发布文件前必须遵守。统一命名格式，便于检索和管理。`
**问题**: 缺少具体触发场景和 pushy 指导
**建议描述**:
```
知识资产命名规范。创建、重命名、发布任何知识资产文件前必须遵守此规范。当用户创建新文件、保存文档、发布内容或提到"命名"、"文件名"时，必须先检查此技能确保命名符合规范。统一格式：[主题]-[类型]-by-[模型名].md
```

#### 4. update-wiki-homepage
**当前描述**: `更新飞书知识库首页的更新日志。每次发布文档后调用，记录最新动态。`
**问题**: 太简短，缺少触发词
**建议描述**:
```
飞书知识库更新日志。每次向飞书发布文档后，必须调用此技能更新首页的更新日志。当用户说"更新日志"、"发布到飞书后"、"记录更新"或完成任何飞书文档发布时自动触发。
```

---

### 🟡 中优先级（需要优化）

#### 5. 3w-decode
**当前描述**: (英文)
**问题**: 中文用户可能触发不准确
**建议**: 添加中文触发词如"3W解码"、"解码知识"、"深度分析逐字稿"

#### 6. knowledge-extractor
**问题**: 与 3w-decode 功能重叠，可能造成触发冲突
**建议**: 明确区分两者的使用场景，或在描述中说明优先级

#### 7-12. 英文描述的 skills
以下 skills 使用英文描述，建议改为中文或中英双语：
- customer-profile
- desensitize
- glossary-extract
- publish-feishu
- strategic-questioning
- trust-storyteller
- txt-preprocess

---

### 🟢 低优先级（基本合格）

#### 13-19. 已有中文触发方式的 skills
- 文章蓝军 ✓
- coaching-interview ✓
- deepseek-to-obsidian ✓
- gemini-api ✓
- send-email ✓

这些 skills 的描述基本完整，可以考虑进一步优化使其更"pushy"。

---

## 通用改进建议

### 1. 统一语言
建议所有面向中文用户的 skills 使用中文描述，或使用中英双语格式。

### 2. 增加触发词
每个 skill 描述应包含 3-5 个具体的触发词/短语。

### 3. 避免冲突
检查以下 skill 组是否存在功能重叠：
- `3w-decode` vs `knowledge-extractor`
- `extracting-golden-quotes` vs `glossary-extract`
- `asset-produce` vs 其他输出类 skills

### 4. Pushy 描述模板
```
[技能名称]。[一句话功能说明]。当用户说"[触发词1]"、"[触发词2]"或[场景描述]时，必须/应该使用此技能。[额外说明]
```

---

## 下一步建议

1. **立即修复**: wechat-article（缺失描述）
2. **优先优化**: extracting-golden-quotes, naming-convention, update-wiki-homepage
3. **批量改进**: 将所有英文描述改为中文
4. **冲突解决**: 梳理 3w-decode 和 knowledge-extractor 的关系

---

*报告生成模型: Claude (当前会话)*
