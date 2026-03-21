---
title: (setq hr-recruitment
category: 商业管理
tags: [商业管理, 教程, 对比]
source: DeepSeek
messages: unknown
processed: 2026-02-20
---
'(

---
messages: 4
---

## User

(setq hr-recruitment-prompt
  '(:role "You are a seasoned HR Director, particularly skilled in recruiting suitable talent for businesses."
    :context "The user will provide a brief overview of the company's background, including its industry, size, products/services, annual revenue, the position to be filled, and expectations for the position."
    :task (
      (:step-1 "Deeply understand the company's background provided by the user and search the internet for relevant industry trends, company news, and reports.")
      (:step-2 "Analyze, infer, and supplement the following key information:"
        :industry-characteristics "Industry characteristics and current development trends."
        :company-size "Company size and market position."
        :product-advantage "Whether the company’s products/services have a competitive advantage."
        :position-role "The role of the position in the company's development and its impact.")
      (:step-3 "Based on the gathered, learned, or inferred information, first consider:"
        :objective "What should this position bring to the company?"
        :goals "Quantify the Objective into measurable Goals."
        :strategies "How will this position achieve the Goals and Objective?"
        :measures "How can the achievement of Goals and Objective be measured using KPIs or OKRs?"
        :challenges "What challenges might this position face?"
        :obstacles "What potential obstacles could hinder this position’s effectiveness in the organization?")
      (:step-4 "Generate a comprehensive and detailed Job Description, including:"
        :job-title "The title should be modern, forward-thinking, easy to understand, and professional."
        :company-overview "Based on the user’s input and all the knowledge and information you have gathered or inferred, derive the company’s culture, mission, vision, and values."
        :job-summary "A comprehensive and detailed job description."
        :responsibilities "List five major responsibilities, each including both daily and long-term duties."
        :qualifications (
          :education-background (
            :level "The required education level to qualify for the position."
            :degree "The required degree(s) to qualify for the position."
            :certifications "Any necessary professional certifications."
          )
          :skills (
            :technical-skills (
              :competencies "Relevant professional competencies."
              :methodologies "Methodologies applicable to the role."
              :tools "Tools required for daily work."
              :language-proficiency "Language proficiency needed for the job."
            )
            :soft-skills (
              :communication "Communication skills."
              :collaboration "Collaboration abilities."
              :leadership "Leadership skills."
              :adaptability "Adaptability."
              :problem-solving "Problem-solving abilities."
              :time-management "Time management."
              :empathy "Empathy, self-awareness, and interpersonal relationship management."
              :user-thinking "User-centric and customer-oriented thinking."
              :ethics "Professional ethics."
            )
          )
          :work-experience (
            :years "The minimum years of experience required for this position."
            :competitive-experience "Whether the candidate should have prior experience in competitive or industry-leading companies."
          )
          :preferred-qualifications "Any conditions that would give candidates an advantage, such as working for certain benchmark companies or obtaining specific certifications."
        )
        :work-environment "Describe the company’s work environment and team atmosphere."
        :career-development "Emphasize the career growth path and professional development opportunities."
        :compensation (
          :salary-benchmark "Research relevant salary data online and deduce the average salary benchmarks for this position in China, Japan, and the United States."
          :compensation-package (
            :equity "Equity and stock options."
            :stock "Stock grants or performance-based shares."
            :benefits "Travel allowances and vacation benefits."
            :subsidies "Daily expense subsidies, travel allowances, overtime pay, and transportation allowances."
          )
        )
      )
    )
    :language "Ensure the output language matches the input language of the user."
    :tone-and-format (
      :inclusive-language "Use inclusive language and avoid terminology or phrases that might alienate candidates."
      :active-verbs "Use active verbs such as 'lead,' 'develop,' 'create,' or 'implement' to describe responsibilities."
      :clarity "Ensure clarity and logical structure, using headings to separate sections."
      :readability "Use tables or bullet points where necessary to present data and perform

这个提示词是别人写的，请告诉我怎么能看明白，以及学会这种写法

## Assistant

这个提示词的写法体现了结构化思维和系统化设计的特点，属于一种专业级的任务分解框架。要理解并掌握这种写法，可以从以下几个层次逐步分析：

### 一、结构拆解

- 顶层框架（基于Lisp语法）:role：定义AI扮演的角色:context：设定对话场景:task：核心任务分解（含嵌套步骤）:language：语言要求:tone-and-format：行文规范

顶层框架（基于Lisp语法）

- :role：定义AI扮演的角色

:role：定义AI扮演的角色

- :context：设定对话场景

:context：设定对话场景

- :task：核心任务分解（含嵌套步骤）

:task：核心任务分解（含嵌套步骤）

- :language：语言要求

:language：语言要求

- :tone-and-format：行文规范

:tone-and-format：行文规范

- 任务分解结构lisp复制下载(step 
  (子步骤 
    (:参数 说明)
    (:参数 (嵌套参数 说明))
  )
)典型特征：层级嵌套、参数命名规范、逻辑关联

任务分解结构

典型特征：层级嵌套、参数命名规范、逻辑关联

- 知识维度设计行业分析（趋势/规模/产品优势）岗位分析（目标/KPI/挑战）任职资格（硬技能/软技能/经验）薪酬体系（国际基准/福利组合）

知识维度设计

- 行业分析（趋势/规模/产品优势）

行业分析（趋势/规模/产品优势）

- 岗位分析（目标/KPI/挑战）

岗位分析（目标/KPI/挑战）

- 任职资格（硬技能/软技能/经验）

任职资格（硬技能/软技能/经验）

- 薪酬体系（国际基准/福利组合）

薪酬体系（国际基准/福利组合）

### 二、核心设计逻辑

- MECE原则（Mutually Exclusive, Collectively Exhaustive）每个层级的要素相互独立且完全穷尽例如技能分解为技术技能（硬技能）和软技能

MECE原则（Mutually Exclusive, Collectively Exhaustive）

- 每个层级的要素相互独立且完全穷尽

每个层级的要素相互独立且完全穷尽

- 例如技能分解为技术技能（硬技能）和软技能

例如技能分解为技术技能（硬技能）和软技能

- 系统思维框架图表代码下载全屏.kvfysmfp{overflow:hidden;touch-action:none}.ufhsfnkm{transform-origin: 0 0}#mermaid-svg-0{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-svg-0 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-svg-0 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-svg-0 .error-icon{fill:#552222;}#mermaid-svg-0 .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-0 .edge-thickness-normal{stroke-width:1px;}#mermaid-svg-0 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-0 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-0 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-svg-0 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-0 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-0 .marker{fill:#333333;stroke:#333333;}#mermaid-svg-0 .marker.cross{stroke:#333333;}#mermaid-svg-0 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-0 p{margin:0;}#mermaid-svg-0 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#mermaid-svg-0 .cluster-label text{fill:#333;}#mermaid-svg-0 .cluster-label span{color:#333;}#mermaid-svg-0 .cluster-label span p{background-color:transparent;}#mermaid-svg-0 .label text,#mermaid-svg-0 span{fill:#333;color:#333;}#mermaid-svg-0 .node rect,#mermaid-svg-0 .node circle,#mermaid-svg-0 .node ellipse,#mermaid-svg-0 .node polygon,#mermaid-svg-0 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-svg-0 .rough-node .label text,#mermaid-svg-0 .node .label text,#mermaid-svg-0 .image-shape .label,#mermaid-svg-0 .icon-shape .label{text-anchor:middle;}#mermaid-svg-0 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-svg-0 .rough-node .label,#mermaid-svg-0 .node .label,#mermaid-svg-0 .image-shape .label,#mermaid-svg-0 .icon-shape .label{text-align:center;}#mermaid-svg-0 .node.clickable{cursor:pointer;}#mermaid-svg-0 .root .anchor path{fill:#333333!important;stroke-width:0;stroke:#333333;}#mermaid-svg-0 .arrowheadPath{fill:#333333;}#mermaid-svg-0 .edgePath .path{stroke:#333333;stroke-width:2.0px;}#mermaid-svg-0 .flowchart-link{stroke:#333333;fill:none;}#mermaid-svg-0 .edgeLabel{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-svg-0 .edgeLabel p{background-color:rgba(232,232,232, 0.8);}#mermaid-svg-0 .edgeLabel rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-svg-0 .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#mermaid-svg-0 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-svg-0 .cluster text{fill:#333;}#mermaid-svg-0 .cluster span{color:#333;}#mermaid-svg-0 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-svg-0 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-svg-0 rect.text{fill:none;stroke-width:0;}#mermaid-svg-0 .icon-shape,#mermaid-svg-0 .image-shape{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-svg-0 .icon-shape p,#mermaid-svg-0 .image-shape p{background-color:rgba(232,232,232, 0.8);padding:2px;}#mermaid-svg-0 .icon-shape rect,#mermaid-svg-0 .image-shape rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-svg-0 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-svg-0 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-svg-0 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}公司背景行业分析岗位定位目标设定任职要求薪酬设计

系统思维框架

公司背景

行业分析

岗位定位

目标设定

任职要求

薪酬设计

- 量化思维渗透目标必须可量化（如"Quantify the Objective into measurable Goals"）薪酬部分要求数据调研（salary-benchmark）

量化思维渗透

- 目标必须可量化（如"Quantify the Objective into measurable Goals"）

目标必须可量化（如"Quantify the Objective into measurable Goals"）

- 薪酬部分要求数据调研（salary-benchmark）

薪酬部分要求数据调研（salary-benchmark）

### 三、学习路径建议

- 基础要素训练角色定义：精准描述期望的AI人格场景限定：构建具体业务上下文任务拆解：从宏观到微观的层级展开

基础要素训练

- 角色定义：精准描述期望的AI人格

角色定义：精准描述期望的AI人格

- 场景限定：构建具体业务上下文

场景限定：构建具体业务上下文

- 任务拆解：从宏观到微观的层级展开

任务拆解：从宏观到微观的层级展开

- 结构化表达训练markdown复制下载1. 学习嵌套列表的表达方式
  - 层级缩进规范
  - 参数命名体系（如:technical-skills）
2. 掌握语义关联技巧
  - 每个子项必须支撑父级目标
  - 避免信息孤岛

结构化表达训练

- 行业知识沉淀建立岗位分析矩阵：| 维度         | 分析要点                  | 数据来源          ||--------------|---------------------------|-------------------|| 行业趋势     | CAGR/竞争格局/技术革新    | 行业白皮书        || 岗位价值     | ROI/战略贡献度/替代成本   | 岗位评估模型      || 薪酬基准     | 分位值/地域系数/福利组合  | 薪酬调研报告      |

行业知识沉淀

- 建立岗位分析矩阵：| 维度         | 分析要点                  | 数据来源          ||--------------|---------------------------|-------------------|| 行业趋势     | CAGR/竞争格局/技术革新    | 行业白皮书        || 岗位价值     | ROI/战略贡献度/替代成本   | 岗位评估模型      || 薪酬基准     | 分位值/地域系数/福利组合  | 薪酬调研报告      |

建立岗位分析矩阵：| 维度         | 分析要点                  | 数据来源          ||--------------|---------------------------|-------------------|| 行业趋势     | CAGR/竞争格局/技术革新    | 行业白皮书        || 岗位价值     | ROI/战略贡献度/替代成本   | 岗位评估模型      || 薪酬基准     | 分位值/地域系数/福利组合  | 薪酬调研报告      |

### 四、高级技巧解析

- 动态平衡设计硬性要求（如:years）与软性要求（如:empathy）的比例控制标准化（:certifications）与差异化（:preferred-qualifications）的配比

动态平衡设计

- 硬性要求（如:years）与软性要求（如:empathy）的比例控制

硬性要求（如:years）与软性要求（如:empathy）的比例控制

- 标准化（:certifications）与差异化（:preferred-qualifications）的配比

标准化（:certifications）与差异化（:preferred-qualifications）的配比

- 国际化视角图表代码下载全屏.kvfysmfp{overflow:hidden;touch-action:none}.ufhsfnkm{transform-origin: 0 0}#mermaid-svg-2{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-svg-2 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-svg-2 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-svg-2 .error-icon{fill:#552222;}#mermaid-svg-2 .error-text{fill:#552222;stroke:#552222;}#mermaid-svg-2 .edge-thickness-normal{stroke-width:1px;}#mermaid-svg-2 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-2 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-2 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-svg-2 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-2 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-2 .marker{fill:#333333;stroke:#333333;}#mermaid-svg-2 .marker.cross{stroke:#333333;}#mermaid-svg-2 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-2 p{margin:0;}#mermaid-svg-2 .pieCircle{stroke:black;stroke-width:2px;opacity:0.7;}#mermaid-svg-2 .pieOuterCircle{stroke:black;stroke-width:2px;fill:none;}#mermaid-svg-2 .pieTitleText{text-anchor:middle;font-size:25px;fill:black;font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-2 .slice{font-family:"trebuchet ms",verdana,arial,sans-serif;fill:#333;font-size:17px;}#mermaid-svg-2 .legend text{fill:black;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:17px;}#mermaid-svg-2 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}40%35%25%薪酬基准国家中国日本美国

国际化视角

- 合规性设计包含:inclusive-language（避免歧视性表述）设置:ethics（职业道德规范）

合规性设计

- 包含:inclusive-language（避免歧视性表述）

包含:inclusive-language（避免歧视性表述）

- 设置:ethics（职业道德规范）

设置:ethics（职业道德规范）

### 五、实践应用建议

- 模板迭代方法每次使用后记录缺失项建立参数权重评分表定期更新行业关键词库

模板迭代方法

- 每次使用后记录缺失项

每次使用后记录缺失项

- 建立参数权重评分表

建立参数权重评分表

- 定期更新行业关键词库

定期更新行业关键词库

- 效果评估指标excel复制下载| 评估维度       | 衡量标准                     | 目标值 |
|----------------|------------------------------|--------|
| 岗位匹配度     | 候选人筛选通过率             | ≥80%   |
| 市场竞争力     | 岗位发布后7天申请量          | ≥50    |
| 组织适配性     | 试用期通过率                 | ≥90%   |

效果评估指标

- 自动化扩展思路将参数转化为数据库字段开发智能提示词生成器集成薪酬数据API

自动化扩展思路

- 将参数转化为数据库字段

将参数转化为数据库字段

- 开发智能提示词生成器

开发智能提示词生成器

- 集成薪酬数据API

集成薪酬数据API

这种写法本质上是在构建一个"可执行的思考框架"，需要结合领域知识、逻辑思维和工程化设计能力。建议从模仿现有框架开始，逐步加入自己的行业认知，最终形成个性化的专业模板。

## User

请合理拆分并解释代码，带我阅读

## Assistant

我们将采用分层解析的方式逐步拆解该提示词的架构设计，并通过「功能模块+设计意图+代码示例」的三段式结构进行解读。以下是详细拆解：

### 一、顶层架构设计

#### 功能模块解析

### 二、任务流程分解（:task模块）

#### 阶段流程图解

Step1: 理解公司背景

Step2: 行业/产品/岗位分析

Step3: 目标/KPI/挑战推导

Step4: 生成完整JD

### 三、关键子步骤详解

#### 1. 信息收集阶段（Step-1）

设计重点：

- 深度理解：要求AI先消化用户提供的原始信息

深度理解：要求AI先消化用户提供的原始信息

- 主动扩展：通过"search the internet"指令激活联网检索能力

主动扩展：通过"search the internet"指令激活联网检索能力

- 示例场景：当用户说"我们是一家新能源电池初创企业"，AI会自动补充：markdown复制下载- 行业趋势：固态电池技术突破（引用2023年行业报告）
- 竞争格局：CATL/BYD市场占有率数据

示例场景：当用户说"我们是一家新能源电池初创企业"，AI会自动补充：

#### 2. 分析推理阶段（Step-2）

结构化分析框架：

#### 3. 战略规划阶段（Step-3）

目标推导逻辑：

#### 4. 输出生成阶段（Step-4）

JD生成矩阵：

### 四、高级设计特征

#### 1. 动态参数体系

实现逻辑：

- 通过自然语言指令触发数据检索

通过自然语言指令触发数据检索

- 按国家维度建立基准参数

按国家维度建立基准参数

- 组合固定薪酬与浮动激励

组合固定薪酬与浮动激励

#### 2. 合规性设计

关键检查点：

- ✅ 移除年龄/性别暗示（如不写"90后优先"）

✅ 移除年龄/性别暗示（如不写"90后优先"）

- ✅ 避免学历歧视（如"统招本科"改为"本科及以上"）

✅ 避免学历歧视（如"统招本科"改为"本科及以上"）

- ✅ 使用中性化职位名称（如"销售经理"而非"销售小哥"）

✅ 使用中性化职位名称（如"销售经理"而非"销售小哥"）

### 五、学习实践建议

#### 临摹训练步骤

- 结构复现：先用注释符号标记各模块功能lisp复制下载;; [角色定义] 限定AI的专业领域
(:role "You are...")

;; [任务分解] 使用step-n进行流程控制
(:task ( (:step-1 "...") ))

结构复现：先用注释符号标记各模块功能

- 参数替换：保持结构不变，修改具体内容diff复制下载- :role "HR Director"
+ :role "Marketing Consultant"

参数替换：保持结构不变，修改具体内容

- 扩展训练：添加新的分析维度lisp复制下载(:step-2 (... 
  :new-dimension "新增分析维度说明"
))

扩展训练：添加新的分析维度

#### 调试技巧

- 测试用例：用不同行业/规模的公司输入，观察JD变化

测试用例：用不同行业/规模的公司输入，观察JD变化

- 质量评估：检查是否包含：战略级目标（如"3年实现市占率提升"）具体方法论要求（如"熟悉OKR实施流程"）可量化指标（如"管理10人以上团队经验"）

质量评估：检查是否包含：

- 战略级目标（如"3年实现市占率提升"）

战略级目标（如"3年实现市占率提升"）

- 具体方法论要求（如"熟悉OKR实施流程"）

具体方法论要求（如"熟悉OKR实施流程"）

- 可量化指标（如"管理10人以上团队经验"）

可量化指标（如"管理10人以上团队经验"）

这种结构化提示词设计本质上是在构建「可执行的决策树」，需要持续迭代优化各节点的参数权重。建议从模仿行业标杆企业的JD开始，逐步加入个性化分析维度。