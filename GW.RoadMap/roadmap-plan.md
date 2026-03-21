# 科学创业路线图 - 改版设计计划

## 改版方向

- **载体**：H5 网页（纯 HTML/CSS/JS）
- **风格**：马里奥大陆节点式 — 保留手绘地图背景，叠加可点击的课程节点 + 路径线
- **受众**：潜在学员（招生展示）+ 已报名学员（学习导航）

---

## Step 1: 信息架构

### 顶层：创业系统总纲
- 《战略设计总纲课》
- 《组织设计总纲课》

### 左区：创业验证期（8 个模块）

| 序号 | 模块 | 包含课程 |
|------|------|--------|
| 1 | 定方向 | 《升级定位与品牌战略》《业务领先战略》《战略解码到绩效承接》 |
| 2 | 创模式 | 《商业模式创新》《超级门店:1店5开新模型》 |
| 3 | 搭班子 | 《战略人才规划》《卓越经营者》《超级面试官》 |
| 4 | 做产品 | 《从用户研究到产品创新》 |
| 5 | 树品牌 | 《战略视觉锤》《跨境爆品打造》 |
| 6 | 促增长 | 《B2B策略销售》《高效客户拜访》《微信生态私域布局》《小红书高效种草》《超级转化率》 |
| 7 | 带团队 | 《人人都是自己的CEO》《OGSM业务规划与执行》《经营分析会》《极简项目管理》《教练式领导力》《做实企业文化》 |
| - | 验证期选修 | 《创始人的极简法律》《直击经营的人才布阵》《结构化思考力》《从目标设定到成果落地》 |

### 右区：创业扩张期（8 个模块）

| 序号 | 模块 | 包含课程 |
|------|------|--------|
| 1 | 备粮草 | 《跨境财税合规》《创始人财务进阶》《财务BP能力提升》《业务优化与利润提升》 |
| 2 | 扩市场 | 《卓越经营者》《品牌增长与全域营销》《全域流量布局与经营》《B2B销售业绩管理》《超级转化率》《创始人的营销全景课》 |
| 3 | 保供给 | 《产品战略》《GTM产品市场协同作战》《轻量化实战IPD》《供应链管理》《需求预测&库存管控》《跨境全链路提效降本》 |
| 4 | 建组织 | 《流程型组织》 |
| 5 | 塑文化 | 《做实企业文化》 |
| 6 | 强激励 | 《科学分钱》《做对股权激励》 |
| 7 | 育人才 | 《直击经营的人才布阵》《业务管理者养成》《超级面试官》《战略人才规划》《高管团队的进化力》《干部管理》 |
| - | 扩张期选修 | 《经营分析会》《高质量复盘》《组织知识管理》《跨部门协作》 |

---

## Step 2: 地图分区 + 节点布局

### 地图整体构想

```
整体为一张横向/纵向的大陆地图，分为两个大陆板块：

┌─────────────────────────────────────────────┐
│                 创业系统总纲                    │
│          (地图顶部/中央 - 灯塔或城堡)           │
├──────────────────┬──────────────────────────┤
│   创业验证期大陆    │     创业扩张期大陆          │
│   (左侧/下方)      │     (右侧/上方)           │
│                    │                          │
│  起步小镇 → 平原    │   山腰要塞 → 王城         │
│  温暖色调           │   进阶色调                │
│                    │                          │
│  节点1: 定方向 🧭   │   节点1: 备粮草 💰        │
│  节点2: 创模式 ⚙️   │   节点2: 扩市场 🌍        │
│  节点3: 搭班子 🏴   │   节点3: 保供给 📦        │
│  节点4: 做产品 🔨   │   节点4: 建组织 🏛️        │
│  节点5: 树品牌 🎯   │   节点5: 塑文化 🎭        │
│  节点6: 促增长 📈   │   节点6: 强激励 🏆        │
│  节点7: 带团队 👥   │   节点7: 育人才 🎓        │
│  选修: 补给站 📚    │   选修: 补给站 📚         │
└──────────────────┴──────────────────────────┘
```

### 节点路径关系

**创业验证期路径（建议顺序，非强制线性）：**
```
定方向 ──→ 创模式 ──→ 搭班子 ──→ 做产品
                                    │
树品牌 ←── 促增长 ←── 带团队 ←──────┘
                       │
                    选修(补给站)
```

**创业扩张期路径：**
```
备粮草 ──→ 扩市场 ──→ 保供给
                        │
建组织 ←── 塑文化 ←────┘
  │
强激励 ──→ 育人才
              │
           选修(补给站)
```

**两大陆之间：**
- 验证期大陆最终节点 → 桥梁/传送门 → 扩张期大陆入口
- 视觉上表现为跨海大桥或星门

### 节点交互设计

- **默认状态**：显示模块图标 + 模块名称（如"定方向"）
- **Hover 状态**：节点放大，显示课程数量提示
- **点击展开**：弹出浮层/侧边栏，列出该模块所有课程名称
- **学员模式（可选）**：已完成节点亮起，未完成节点灰显

---

## Step 3: 视觉风格 + 地图背景生成

### 已确定的风格特征
- 淡蓝色水彩手绘底色
- 现代商业元素（非古代/中世纪）
- 深蓝色路径线连接各个节点
- 节点用深蓝色胶囊标签标注名称
- 人物场景表现团队协作
- 整体通透、留白充足

### 元素设计逻辑

**核心原则：**
- 验证期 = 小、简陋、手工、几个人、试错、草根
- 扩张期 = 大、专业、系统化、很多人、规模化

### 完整地图元素清单

#### 顶层：创业系统总纲（地图最高点）

| 节点 | 视觉元素 | 设计逻辑 |
|------|---------|---------|
| 总纲（战略+组织设计） | **灯塔/指挥塔** — 现代玻璃观景塔，顶部有光芒发散 | 灯塔=战略方向指引，位于地图最高点，俯瞰全局 |

#### 下区：创业验证期（从0到1，小而美，草根起步）

| 序号 | 模块 | 视觉元素 | 设计逻辑 |
|------|------|---------|---------|
| 1 | 定方向 | **咖啡馆讨论** — 几个人在咖啡馆小桌旁看地图、讨论方向 | 早期=咖啡馆创业，小范围探讨 |
| 2 | 创模式 | **车库白板** — 车库里摆着白板，上面画着商业模式草图，几个人站着讨论 | 车库创业=硅谷经典意象 |
| 3 | 搭班子 | **小桌面试** — 简易办公桌，三五个人围坐面试，墙上贴着简历 | 早期团队=小而精 |
| 4 | 做产品 | **手工工作台** — 简易工作台，有人在手工制作产品原型，旁边有草图 | 手工打磨=MVP阶段 |
| 5 | 树品牌 | **街边小店挂招牌** — 一个小店铺门面，有人在挂上新招牌 | 从一家小店开始=品牌起点 |
| 6 | 促增长 | **小黑板写目标** — 墙上小黑板写着销售数字，几个人在打电话、发传单 | 地推=早期增长方式 |
| 7 | 带团队 | **篝火会议** — 几个人围着篝火开会，队长站着讲话 | 篝火=早期团队凝聚 |
| - | 验证期选修 | **路边小书摊** — 简易书架、几本书、一把椅子 | 随时补充=轻量学习 |

#### 中间过渡区

| 元素 | 描述 | 设计逻辑 |
|------|------|---------|
| 山脉 | 横跨地图中部的山脉 | 跨越困难、进阶的门槛 |
| 跨河大桥 | 一座现代大桥跨越河流/峡谷 | 从验证到扩张的关键跨越 |

#### 上区：创业扩张期（从1到N，大而强，规模化）

| 序号 | 模块 | 视觉元素 | 设计逻辑 |
|------|------|---------|---------|
| 1 | 备粮草 | **银行大楼** — 现代玻璃银行建筑，有投资人在会议室签约 | 融资=专业金融机构 |
| 2 | 扩市场 | **全球贸易港** — 集装箱码头、货轮、飞机、地球仪 | 出海=全球化扩张 |
| 3 | 保供给 | **自动化工厂** — 流水线、机械臂、堆叠的包裹、运输卡车 | 供应链=规模化生产 |
| 4 | 建组织 | **企业总部大厦** — 现代玻璃幕墙写字楼，门口有公司Logo旗帜 | 总部=正规组织架构 |
| 5 | 塑文化 | **企业广场** — 雕塑、文化标语墙、很多员工在广场交流活动 | 广场=文化外显 |
| 6 | 强激励 | **上市敲钟/颁奖大会** — 舞台上敲钟或颁发奖杯，台下很多人鼓掌，背景有股权图表 | 上市/股权=终极激励 |
| 7 | 育人才 | **企业大学** — 现代培训中心，阶梯教室，很多学员，毕业帽元素 | 企业大学=系统化培养 |
| - | 扩张期选修 | **大型图书馆** — 宏伟的图书馆建筑，大量藏书 | 深度学习=高阶资源 |

#### 装饰元素

| 元素 | 位置 | 设计逻辑 |
|------|------|---------|
| 深蓝色路径线 | 从下往上连接所有节点 | 学习路径，蜿蜒向上 |
| 热气球 | 天空点缀，2-3个 | 象征上升、探索 |
| 小飞机 | 天空点缀，1-2架 | 象征速度、扩张 |
| 树木、云朵 | 散布各处 | 自然装饰，增加手绘感 |

### Nano Banana Pro 提示词 - 完整地图

```
A complete startup journey map in soft blue watercolor hand-drawn style, bird's eye view,
portrait orientation (3:4 ratio for mobile scrolling), showing a vertical journey from bottom to top.

OVERALL LAYOUT (bottom to top progression):
- Bottom region: "Validation Stage" - small scale, grassroots startup atmosphere, humble beginnings
- Middle: Mountains and a grand bridge crossing a river/valley (the leap from validation to expansion)
- Top region: "Expansion Stage" - large scale, professional enterprise atmosphere, sophisticated
- Very top: A modern glass observation tower/lighthouse with light rays (Strategic Overview, the ultimate goal)
- Dark blue path lines wind upward through all locations
- Decorations: 2-3 hot air balloons, 1-2 small airplanes in sky, scattered trees and clouds

BOTTOM REGION - VALIDATION STAGE (small, humble, handmade, few people, grassroots):
1. Coffee shop discussion - few people at a small cafe table looking at maps, discussing direction
2. Garage whiteboard - inside a garage, whiteboard with business model sketches, people standing around
3. Small table interview - simple desk, 3-5 people sitting for interview, resumes on wall
4. Handcraft workbench - simple workbench, someone handmaking a product prototype, sketches nearby
5. Small shop hanging signboard - a tiny storefront, someone hanging up a new shop sign
6. Small blackboard with goals - wall blackboard with sales numbers, people making phone calls, handing out flyers
7. Campfire meeting - few people gathered around campfire, team leader standing and speaking
8. Roadside book stand - simple bookshelf, few books, a chair (Electives)

MIDDLE TRANSITION:
- Mountain range marking the transition
- A grand modern bridge crossing a river/valley
- This represents the leap from startup to scale-up

TOP REGION - EXPANSION STAGE (large, professional, systematic, many people, enterprise scale):
1. Bank building - modern glass bank, investors signing contracts in meeting room
2. Global trade port - container terminal, cargo ships, airplanes, globe
3. Automated factory - assembly lines, robotic arms, stacked packages, delivery trucks
4. Corporate HQ tower - modern glass skyscraper with company flag at entrance
5. Corporate plaza - sculpture, culture wall, many employees gathering and interacting
6. IPO bell ceremony - stage with bell ringing or trophy presentation, large applauding crowd, equity charts in background
7. Corporate university - modern training center, tiered lecture hall, many students, graduation caps
8. Grand library - magnificent library building with vast book collections (Electives)

VERY TOP:
- The lighthouse/observation tower as the pinnacle, with light rays shining down over the entire map

STYLE REQUIREMENTS:
- Soft translucent blue watercolor wash as base
- Thin ink outlines, hand-drawn charm
- Modern business elements (laptops, smartphones, glass buildings, delivery trucks) - NOT medieval/ancient
- Dark blue path lines connecting all nodes flowing from bottom to top
- Clear visual contrast: bottom elements are SMALL and SIMPLE, top elements are LARGE and SOPHISTICATED
- Plenty of white space, airy and breathable
- No text labels, just visual elements

This should feel like a vertical "startup growth journey" - starting humble at bottom, scaling up magnificently toward the top.
```

---

## Step 4: 生成定制节点图标

### 需要的图标清单

**通用图标（2个）：**
1. 总纲 - 灯塔/战略指挥塔
2. 选修/补给站 - 背包/书架

**创业验证期图标（7个）：**
1. 定方向 - 望远镜/指南针
2. 创模式 - 蓝图/齿轮组合
3. 搭班子 - 旗帜与人群
4. 做产品 - 锤子与工作台
5. 树品牌 - 盾徽/旗帜
6. 促增长 - 上升箭头/火箭
7. 带团队 - 队长带领队伍行军

**创业扩张期图标（7个）：**
1. 备粮草 - 金币箱/粮仓
2. 扩市场 - 地球仪/商船
3. 保供给 - 运输车队/仓库
4. 建组织 - 城堡蓝图/建筑
5. 塑文化 - 旗帜飘扬/图腾
6. 强激励 - 奖杯/勋章
7. 育人才 - 学院/毕业帽

### Nano Banana Pro 提示词 - 节点图标

#### 提示词：批量生成验证期图标
```
Generate a set of 7 RPG-style game map location icons for an entrepreneurship
learning roadmap. Each icon represents a different business skill module.
Style: hand-drawn watercolor with slight 3D depth, warm Ghibli-inspired palette,
consistent size and framing, transparent background.

The 7 icons in a 4x2 grid:
1. "Set Direction" - A golden compass on a wooden stand with a small flag
2. "Create Model" - A glowing blueprint scroll with interlocking gears
3. "Build Team" - A banner planted on a hill with 3 small figures gathering
4. "Make Product" - A craftsman's workbench with hammer and glowing item
5. "Build Brand" - A heraldic shield with a shining emblem
6. "Drive Growth" - A small rocket launching from a market stall
7. "Lead Team" - A captain figure leading a marching group with torch

All icons should feel like locations on a fantasy RPG world map.
Consistent style, warm colors, no text.
```

#### 提示词：批量生成扩张期图标
```
Generate a set of 7 RPG-style game map location icons for an entrepreneurship
learning roadmap (advanced stage). Each icon represents a business scaling module.
Style: hand-drawn watercolor with slight 3D depth, slightly cooler and more
majestic palette than the first set, consistent size and framing,
transparent background.

The 7 icons in a 4x2 grid:
1. "Secure Funding" - A treasure chest overflowing with gold coins near a granary
2. "Expand Market" - A globe with trade ships sailing around it
3. "Secure Supply" - A caravan of supply wagons on a mountain road
4. "Build Organization" - A castle blueprint with construction scaffolding
5. "Shape Culture" - A grand totem pole with colorful banners flying
6. "Strengthen Incentives" - A trophy podium with medals and stars
7. "Develop Talent" - An academy building with graduation caps floating above

All icons should feel like advanced locations on a fantasy RPG world map.
Consistent style, slightly more grand/majestic than starter icons, no text.
```

---

## Step 5: 搭建 H5 页面

### 技术方案
- 单个 `index.html` 文件，内联 CSS + JS
- 地图背景用 `<img>` 或 CSS background
- 节点用绝对定位的 `<div>`，放在地图对应位置
- 路径线用 SVG `<path>` 或 CSS border
- 点击交互用原生 JS（无框架依赖）
- 响应式：优先适配手机竖屏

### 页面结构草案
```
<div class="map-container">
  <!-- 地图背景 -->
  <img class="map-bg" src="map-background.png" />

  <!-- SVG 路径层 -->
  <svg class="paths-layer">...</svg>

  <!-- 节点层 -->
  <div class="node" data-module="定方向" style="top:60%; left:15%">
    <img src="icons/direction.png" />
    <span>定方向</span>
  </div>
  <!-- ...更多节点 -->

  <!-- 课程详情浮层 -->
  <div class="detail-panel" id="detail-panel">
    <h3 class="module-name"></h3>
    <ul class="course-list"></ul>
  </div>
</div>
```

---

## Step 6: 迭代打磨清单

- [ ] 移动端节点点击区域 >= 44px
- [ ] 文字在地图背景上可读（加底色/阴影）
- [ ] 路径线在背景上清晰可见
- [ ] 两个大陆的色调区分明显
- [ ] 高维学堂 logo + 二维码位置合理
- [ ] 加载速度可接受（图片压缩）
- [ ] hover/点击动效流畅不卡顿

---

## 当前进度

- [x] Step 1: 信息架构梳理
- [x] Step 2: 地图分区 + 节点布局
- [x] Step 3: 视觉风格确定 + 元素清单设计
  - 风格已确定：淡蓝色水彩手绘，现代商业元素
  - 参考图已生成：效果风格1.png
  - 元素逻辑已确定：验证期=小而美草根，扩张期=大而强规模化
  - 完整提示词已准备好
- [ ] **下一步：用提示词 + 垫图生成完整地图背景**
- [ ] Step 4: 生成定制图标
- [ ] Step 5: 搭建 H5 页面
- [ ] Step 6: 迭代打磨

## 待办事项

1. 用 Nano Banana Pro 生成完整地图（用效果风格1.png作为垫图 + 上面的完整提示词）
2. 如果一次生成效果不好，可分两次生成（验证期 + 扩张期）再拼接
