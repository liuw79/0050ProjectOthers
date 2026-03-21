# H5 课程详情页设计方案

## Context

用户希望重新设计课程详情 H5 页面，参考设计图的简洁现代风格，同时保持高维学堂品牌色。

**目标：**
1. 在 GW.Website 中新增 H5 课程详情页 (`/h5/course/:id`)
2. 输出 H5 设计规范供微信端参考

**参考设计特点：** 深蓝渐变背景、大标题白色粗体、黄色强调、圆角按钮、简洁现代

**品牌融合：** 使用品牌蓝 `#0099FF` 系渐变 + 橙色 `#F08519` 作为强调色

---

## 设计规范

### 色彩方案

| 用途 | 色值 |
|------|------|
| 主色 | `#0099FF` |
| 主色深 | `#007ACC` |
| 强调色 | `#F08519` |
| 文字 | `#333333` / `#666666` / `#999999` |
| 背景 | `#FFFFFF` / `#F5F5F5` |

### H5 Hero 渐变

```css
background: linear-gradient(135deg, #0099FF 0%, #007ACC 100%);
```

---

## 文件结构

### 新增文件

```
src/
├── views/h5/
│   └── CourseDetail.vue              # H5 课程详情页
│
├── components/h5/
│   ├── layout/
│   │   ├── H5Header.vue              # 简化头部 (返回+分享)
│   │   └── H5BottomBar.vue           # 底部固定操作栏
│   │
│   └── course/
│       ├── H5CourseHero.vue          # Hero 区域
│       ├── H5CourseMeta.vue          # 元信息条
│       ├── H5CourseTabs.vue          # Tab 导航
│       ├── H5CourseIntro.vue         # 课程介绍
│       ├── H5CourseModules.vue       # 核心模块
│       ├── H5CourseMentor.vue        # 导师介绍
│       ├── H5CourseFeedback.vue      # 学友反馈
│       └── H5CourseNotice.vue        # 报名须知
│
├── styles/
│   └── h5.css                        # H5 专用样式 (可导出)
│
├── types/
│   └── h5.ts                         # H5 类型定义
│
└── composables/
    └── useH5.ts                      # H5 工具函数

docs/
└── h5-design-spec.md                 # 设计规范文档
```

### 修改文件

| 文件 | 修改内容 |
|------|----------|
| `src/router/index.ts` | 添加 `/h5/course/:id` 路由 |
| `src/App.vue` | H5 页面隐藏 PC Header/Footer |

---

## 页面结构

```
CourseDetail.vue
├── H5Header (返回 + 分享)
├── H5CourseHero (渐变背景 + 课程标题 + 价格)
├── H5CourseMeta (时间/地点/人数)
├── H5CourseTabs (Tab 导航 - 吸顶)
├── H5CourseIntro (课程介绍)
├── H5CourseModules (核心实操模块)
├── H5CourseMentor (导师介绍)
├── H5CourseFeedback (学友反馈)
├── H5CourseNotice (报名须知)
└── H5BottomBar (固定底部: 首页/关注/立即报名)
```

---

## 实现步骤

### Phase 1: 基础架构
1. 创建 `src/styles/h5.css` - H5 样式基础
2. 创建 `src/types/h5.ts` - 类型定义
3. 修改 `src/router/index.ts` - 添加路由
4. 修改 `src/App.vue` - H5 布局处理

### Phase 2: 布局组件
5. 创建 `H5Header.vue` - 简化头部
6. 创建 `H5BottomBar.vue` - 底部操作栏

### Phase 3: 核心组件
7. 创建 `H5CourseHero.vue` - Hero 区域
8. 创建 `H5CourseMeta.vue` - 元信息条
9. 创建 `H5CourseTabs.vue` - Tab 导航

### Phase 4: 内容组件
10. 创建 `H5CourseIntro.vue` - 课程介绍
11. 创建 `H5CourseModules.vue` - 核心模块
12. 创建 `H5CourseMentor.vue` - 导师介绍
13. 创建 `H5CourseFeedback.vue` - 学友反馈
14. 创建 `H5CourseNotice.vue` - 报名须知

### Phase 5: 整合与输出
15. 创建 `CourseDetail.vue` - 整合所有组件
16. 创建 `docs/h5-design-spec.md` - 设计规范文档
17. 创建 `src/composables/useH5.ts` - 工具函数

---

## 验证方式

1. **开发服务器测试**
   ```bash
   cd /Users/comdir/SynologyDrive/0050Project/GW.Website
   npm run dev
   ```

2. **访问 H5 页面**
   - 打开浏览器开发者工具 → 切换到移动端视图
   - 访问 `http://localhost:5173/h5/course/303`

3. **检查项**
   - [ ] 渐变背景显示正常
   - [ ] 底部固定栏适配 iOS 安全区域
   - [ ] Tab 吸顶效果
   - [ ] 移动端滚动流畅

---

## 关键参考文件

- `src/style.css` - 现有样式系统
- `src/components/courses/CourseCard.vue` - 组件模式参考
- `src/composables/useApi.ts` - API 请求模式
