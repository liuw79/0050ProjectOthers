---
title: Odoo14的皮肤开发规范
category: 科技AI
tags: [科技AI, 教程, 推荐, 对比]
source: DeepSeek
messages: 6
processed: 2026-02-20
---
## User

Odoo14的皮肤开发规范

## Assistant

### Odoo 14 主题开发规范指南

#### 1. 主题目录结构

#### 2. manifest.py 配置

#### 3. SCSS 开发规范

文件组织：

- variables.scss: 定义颜色/字体等变量scss复制下载$primary: #3498db;
$font-heading: 'Roboto', sans-serif;

variables.scss: 定义颜色/字体等变量

- styles.scss: 主样式文件scss复制下载@import 'variables';

body {
  font-family: $font-heading;
  background: #f8f9fa;
}

.btn-primary {
  background-color: $primary;
}

styles.scss: 主样式文件

编译说明：Odoo 14 使用 libsass 自动编译 SCSS，无需手动编译。

#### 4. XML 视图开发

a. 布局覆盖 (layouts.xml):

b. 片段开发 (snippets.xml):

#### 5. JavaScript 交互

a. 基础 JS (theme.js):

b. 片段选项扩展 (snippet_options.js):

#### 6. 响应式设计

使用 Bootstrap 4 栅格系统：

#### 7. 图标与图像

- 位置：static/src/images/

位置：static/src/images/

- 引用方式：xml复制下载运行<img src="/my_theme/static/src/images/logo.png" class="logo"/>

引用方式：

- 推荐使用 SVG 格式保证清晰度。

推荐使用 SVG 格式保证清晰度。

#### 8. 主题继承机制

覆盖其他主题/模块：

#### 9. 多语言支持

在主题目录添加 i18n/ 文件夹：

在 XML 中使用可翻译文本：

#### 10. 测试与优化

- 浏览器兼容性： Chrome, Firefox, Safari, Edge

浏览器兼容性： Chrome, Firefox, Safari, Edge

- 移动端测试： 使用 Chrome 设备模拟器

移动端测试： 使用 Chrome 设备模拟器

- 性能优化：压缩图片（工具：TinyPNG）启用 Odoo 的缓存和压缩（web.base.url /assets）

性能优化：

- 压缩图片（工具：TinyPNG）

压缩图片（工具：TinyPNG）

- 启用 Odoo 的缓存和压缩（web.base.url /assets）

启用 Odoo 的缓存和压缩（web.base.url /assets）

### 最佳实践

- 模块化开发： 将功能拆分成独立片段

模块化开发： 将功能拆分成独立片段

- 避免硬编码： 使用 SCSS 变量和 XML 字段

避免硬编码： 使用 SCSS 变量和 XML 字段

- 版本控制： 使用 Git 管理代码变更

版本控制： 使用 Git 管理代码变更

- 遵循 OCA 标准： 参考 Odoo Community Association 指南

遵循 OCA 标准： 参考 Odoo Community Association 指南

> 官方文档参考：Odoo Website DocumentationSCSS Customization Guide

官方文档参考：

- Odoo Website Documentation

Odoo Website Documentation

- SCSS Customization Guide

SCSS Customization Guide

## User

odoo 14到最新版本，在前端技术上有什么变化吗

## Assistant

Odoo 从前端技术架构到开发范式经历了显著演进，以下是Odoo 14到最新版本（Odoo 16）在前端技术上的主要变化及关键特性对比：

### 🦉 一、核心框架：从传统Widget到OWL的全面重构

- Odoo 14：OWL框架初步引入定位：作为React/Vue的替代方案，强调动态应用场景下的XML模板兼容性、无工具链依赖-1-4。特点：基于TypeScript，支持钩子（Hooks）和响应式状态管理（如useState）-1。组件通过ES6类定义，模板采用QWeb（XML格式）-1。未全面覆盖，仅部分新模块使用，旧模块仍依赖传统Widget系统-3-4。

Odoo 14：OWL框架初步引入

- 定位：作为React/Vue的替代方案，强调动态应用场景下的XML模板兼容性、无工具链依赖-1-4。

定位：作为React/Vue的替代方案，强调动态应用场景下的XML模板兼容性、无工具链依赖-1-4。

- 特点：基于TypeScript，支持钩子（Hooks）和响应式状态管理（如useState）-1。组件通过ES6类定义，模板采用QWeb（XML格式）-1。未全面覆盖，仅部分新模块使用，旧模块仍依赖传统Widget系统-3-4。

特点：

- 基于TypeScript，支持钩子（Hooks）和响应式状态管理（如useState）-1。

基于TypeScript，支持钩子（Hooks）和响应式状态管理（如useState）-1。

- 组件通过ES6类定义，模板采用QWeb（XML格式）-1。

组件通过ES6类定义，模板采用QWeb（XML格式）-1。

- 未全面覆盖，仅部分新模块使用，旧模块仍依赖传统Widget系统-3-4。

未全面覆盖，仅部分新模块使用，旧模块仍依赖传统Widget系统-3-4。

- Odoo 15~16：OWL 2.x成为主流覆盖率：Odoo 16中99%的前端组件重构为OWL 2（仅Studio保留少量Widget）-3。性能提升：代码量减少30%，渲染速度提升2~20倍-3。引入 BlockDOM：以“块”为单位管理虚拟DOM，优化diff算法，大幅减少动态更新开销-3。

Odoo 15~16：OWL 2.x成为主流

- 覆盖率：Odoo 16中99%的前端组件重构为OWL 2（仅Studio保留少量Widget）-3。

覆盖率：Odoo 16中99%的前端组件重构为OWL 2（仅Studio保留少量Widget）-3。

- 性能提升：代码量减少30%，渲染速度提升2~20倍-3。引入 BlockDOM：以“块”为单位管理虚拟DOM，优化diff算法，大幅减少动态更新开销-3。

性能提升：

- 代码量减少30%，渲染速度提升2~20倍-3。

代码量减少30%，渲染速度提升2~20倍-3。

- 引入 BlockDOM：以“块”为单位管理虚拟DOM，优化diff算法，大幅减少动态更新开销-3。

引入 BlockDOM：以“块”为单位管理虚拟DOM，优化diff算法，大幅减少动态更新开销-3。

### ⚙️ 二、开发范式与工具链升级

- 资源引入方式变化Odoo 14及之前：通过XML视图注入静态资源（JS/CSS）-2。xml复制下载运行<template id="assets_backend">
    <script src="/module/static/src/js/file.js"/>
</template>Odoo 15+：统一在__manifest__.py中声明assets键管理资源-2：python复制下载'assets': {
    'web.assets_backend': ['module/static/src/js/file.js'],
}

资源引入方式变化

- Odoo 14及之前：通过XML视图注入静态资源（JS/CSS）-2。xml复制下载运行<template id="assets_backend">
    <script src="/module/static/src/js/file.js"/>
</template>

Odoo 14及之前：通过XML视图注入静态资源（JS/CSS）-2。

- Odoo 15+：统一在__manifest__.py中声明assets键管理资源-2：python复制下载'assets': {
    'web.assets_backend': ['module/static/src/js/file.js'],
}

Odoo 15+：统一在__manifest__.py中声明assets键管理资源-2：

- 性能优化技术片段缓存（Odoo 16）：通过t-cache指令缓存静态区块（如页头/页脚），动态区块依赖指定模型（如t-cache="products"），显著降低重复渲染成本-3。CSS清理：删除冗余SCSS代码，合并压缩CSS/JS文件，减少资源体积-3。请求合并：如视图加载（load_views）时精简字段数据，减少RPC请求量-3。

性能优化技术

- 片段缓存（Odoo 16）：通过t-cache指令缓存静态区块（如页头/页脚），动态区块依赖指定模型（如t-cache="products"），显著降低重复渲染成本-3。

片段缓存（Odoo 16）：通过t-cache指令缓存静态区块（如页头/页脚），动态区块依赖指定模型（如t-cache="products"），显著降低重复渲染成本-3。

- CSS清理：删除冗余SCSS代码，合并压缩CSS/JS文件，减少资源体积-3。

CSS清理：删除冗余SCSS代码，合并压缩CSS/JS文件，减少资源体积-3。

- 请求合并：如视图加载（load_views）时精简字段数据，减少RPC请求量-3。

请求合并：如视图加载（load_views）时精简字段数据，减少RPC请求量-3。

- 响应式与工具增强Bootstrap 4：全面采用Bootstrap 4栅格系统，强化移动端适配-6-8。开发者工具：调试模式（?debug=assets）支持非压缩资源加载，便于前端调试-9。Odoo Studio提供可视化审批流、低代码表单设计-7-10。

响应式与工具增强

- Bootstrap 4：全面采用Bootstrap 4栅格系统，强化移动端适配-6-8。

Bootstrap 4：全面采用Bootstrap 4栅格系统，强化移动端适配-6-8。

- 开发者工具：调试模式（?debug=assets）支持非压缩资源加载，便于前端调试-9。Odoo Studio提供可视化审批流、低代码表单设计-7-10。

开发者工具：

- 调试模式（?debug=assets）支持非压缩资源加载，便于前端调试-9。

调试模式（?debug=assets）支持非压缩资源加载，便于前端调试-9。

- Odoo Studio提供可视化审批流、低代码表单设计-7-10。

Odoo Studio提供可视化审批流、低代码表单设计-7-10。

### 🚀 三、用户体验与交互改进

- 界面操作效率提升高频操作外置（如CRM线索页一键发邮件），减少跳转步骤-8-10。嵌入Excel式视图（Spreadsheets），支持跨模块数据公式计算-8-10。

界面操作效率提升

- 高频操作外置（如CRM线索页一键发邮件），减少跳转步骤-8-10。

高频操作外置（如CRM线索页一键发邮件），减少跳转步骤-8-10。

- 嵌入Excel式视图（Spreadsheets），支持跨模块数据公式计算-8-10。

嵌入Excel式视图（Spreadsheets），支持跨模块数据公式计算-8-10。

- 多端适配与组件库PC/移动端共用业务模型，通过解耦设计实现多终端适配-7。丰富预制组件库（如28个业务模型、624种元素），提升开发复用率-7。

多端适配与组件库

- PC/移动端共用业务模型，通过解耦设计实现多终端适配-7。

PC/移动端共用业务模型，通过解耦设计实现多终端适配-7。

- 丰富预制组件库（如28个业务模型、624种元素），提升开发复用率-7。

丰富预制组件库（如28个业务模型、624种元素），提升开发复用率-7。

### 🔧 四、升级兼容性注意事项

- 迁移成本：OWL 2组件语法与1.x存在差异（如生命周期钩子变更），需重写部分组件-3。资源声明方式需从XML迁移至__manifest__.py-2。

迁移成本：

- OWL 2组件语法与1.x存在差异（如生命周期钩子变更），需重写部分组件-3。

OWL 2组件语法与1.x存在差异（如生命周期钩子变更），需重写部分组件-3。

- 资源声明方式需从XML迁移至__manifest__.py-2。

资源声明方式需从XML迁移至__manifest__.py-2。

- 性能权衡：片段缓存需谨慎设计依赖项，避免数据更新失效-3。旧版Widget需逐步替换为OWL组件，以利用BlockDOM优化-3。

性能权衡：

- 片段缓存需谨慎设计依赖项，避免数据更新失效-3。

片段缓存需谨慎设计依赖项，避免数据更新失效-3。

- 旧版Widget需逐步替换为OWL组件，以利用BlockDOM优化-3。

旧版Widget需逐步替换为OWL组件，以利用BlockDOM优化-3。

### 💎 版本间核心变化对比

### 💎 总结

- 技术栈迭代：Widget → OWL 1.x → OWL 2.x + BlockDOM，实现性能与开发体验跃迁。

技术栈迭代：Widget → OWL 1.x → OWL 2.x + BlockDOM，实现性能与开发体验跃迁。

- 工具链统一：资源管理、调试工具标准化，降低协作成本。

工具链统一：资源管理、调试工具标准化，降低协作成本。

- 设计范式：从操作冗余到交互精简，从响应式缺失到多端协同。

设计范式：从操作冗余到交互精简，从响应式缺失到多端协同。

💡 建议升级时优先重构高频交互模块（如表单/看板），并利用OWL 2的异步渲染与缓存机制最大化性能收益。如需深入BlockDOM或OWL 2语法，可参考官方Playground及社区教程-1-3。

## User

odoo最新是19吧？前端技术架构有什么演变

## Assistant

Odoo 从早期版本到最新版本（当前为 Odoo 19）的前端技术架构经历了显著演变，核心是从传统后端渲染模式转向现代化组件化架构。以下是关键阶段的演进分析：

### ⏳ 1. 传统架构阶段（Odoo 7-11）

- 技术栈：后端主导渲染：基于 Python 的 QWeb 模板引擎生成 HTML，前端通过 jQuery 操作 DOM 实现交互-7-8。模块化不足：业务逻辑与视图高度耦合，复用性低。

技术栈：

- 后端主导渲染：基于 Python 的 QWeb 模板引擎生成 HTML，前端通过 jQuery 操作 DOM 实现交互-7-8。

后端主导渲染：基于 Python 的 QWeb 模板引擎生成 HTML，前端通过 jQuery 操作 DOM 实现交互-7-8。

- 模块化不足：业务逻辑与视图高度耦合，复用性低。

模块化不足：业务逻辑与视图高度耦合，复用性低。

- 痛点：性能瓶颈：全页面刷新导致响应慢，复杂交互需大量手动 DOM 操作-2。开发效率低：缺乏组件化支持，维护成本高。

痛点：

- 性能瓶颈：全页面刷新导致响应慢，复杂交互需大量手动 DOM 操作-2。

性能瓶颈：全页面刷新导致响应慢，复杂交互需大量手动 DOM 操作-2。

- 开发效率低：缺乏组件化支持，维护成本高。

开发效率低：缺乏组件化支持，维护成本高。

### 🦉 2. OWL 框架引入阶段（Odoo 12-14）

- 技术变革：OWL（Odoo Web Library）：自研类 React/Vue 的组件化框架，支持虚拟 DOM、响应式数据和生命周期钩子-1-2。渐进式迁移：新模块使用 OWL，旧模块保留 jQuery Widgets。

技术变革：

- OWL（Odoo Web Library）：自研类 React/Vue 的组件化框架，支持虚拟 DOM、响应式数据和生命周期钩子-1-2。

OWL（Odoo Web Library）：自研类 React/Vue 的组件化框架，支持虚拟 DOM、响应式数据和生命周期钩子-1-2。

- 渐进式迁移：新模块使用 OWL，旧模块保留 jQuery Widgets。

渐进式迁移：新模块使用 OWL，旧模块保留 jQuery Widgets。

- 优势：组件化开发：提升代码复用率，例如表单、看板可封装为独立组件。性能优化：虚拟 DOM 减少全页面渲染，局部更新更高效-2。

优势：

- 组件化开发：提升代码复用率，例如表单、看板可封装为独立组件。

组件化开发：提升代码复用率，例如表单、看板可封装为独立组件。

- 性能优化：虚拟 DOM 减少全页面渲染，局部更新更高效-2。

性能优化：虚拟 DOM 减少全页面渲染，局部更新更高效-2。

### ⚡ 3. OWL 成熟与性能提升阶段（Odoo 15-16）

- 全面拥抱 OWL：废弃传统 Widgets：官方模块 99% 重构为 OWL 组件，仅 Studio 等少数功能保留旧实现-1。引入 BlockDOM：优化虚拟 DOM Diff 算法，渲染性能提升 2-20 倍-1。

全面拥抱 OWL：

- 废弃传统 Widgets：官方模块 99% 重构为 OWL 组件，仅 Studio 等少数功能保留旧实现-1。

废弃传统 Widgets：官方模块 99% 重构为 OWL 组件，仅 Studio 等少数功能保留旧实现-1。

- 引入 BlockDOM：优化虚拟 DOM Diff 算法，渲染性能提升 2-20 倍-1。

引入 BlockDOM：优化虚拟 DOM Diff 算法，渲染性能提升 2-20 倍-1。

- 工具链升级：资源声明标准化：静态资源（JS/SCSS）统一在 __manifest__.py 的 assets 键中声明，替代分散的 XML 注入-4。响应式设计强化：深度集成 Bootstrap 4，支持多端自适应布局-1。

工具链升级：

- 资源声明标准化：静态资源（JS/SCSS）统一在 __manifest__.py 的 assets 键中声明，替代分散的 XML 注入-4。

资源声明标准化：静态资源（JS/SCSS）统一在 __manifest__.py 的 assets 键中声明，替代分散的 XML 注入-4。

- 响应式设计强化：深度集成 Bootstrap 4，支持多端自适应布局-1。

响应式设计强化：深度集成 Bootstrap 4，支持多端自适应布局-1。

### 🚀 4. 现代架构阶段（Odoo 17-19）

- 性能与开发体验优化：片段缓存（Odoo 16+）：通过 t-cache 指令缓存静态区块，动态区块依赖模型状态更新，降低重复渲染开销-1。TypeScript 支持：OWL 2.x 全面支持 TypeScript，增强类型安全和开发效率-1-2。

性能与开发体验优化：

- 片段缓存（Odoo 16+）：通过 t-cache 指令缓存静态区块，动态区块依赖模型状态更新，降低重复渲染开销-1。

片段缓存（Odoo 16+）：通过 t-cache 指令缓存静态区块，动态区块依赖模型状态更新，降低重复渲染开销-1。

- TypeScript 支持：OWL 2.x 全面支持 TypeScript，增强类型安全和开发效率-1-2。

TypeScript 支持：OWL 2.x 全面支持 TypeScript，增强类型安全和开发效率-1-2。

- 微前端与低代码整合：模块联邦化：支持微前端架构（如 qiankun），实现业务模块独立开发部署-5。无代码工具：集成 顿表 等可视化设计器，允许非技术人员配置表单、流程和报表-1。

微前端与低代码整合：

- 模块联邦化：支持微前端架构（如 qiankun），实现业务模块独立开发部署-5。

模块联邦化：支持微前端架构（如 qiankun），实现业务模块独立开发部署-5。

- 无代码工具：集成 顿表 等可视化设计器，允许非技术人员配置表单、流程和报表-1。

无代码工具：集成 顿表 等可视化设计器，允许非技术人员配置表单、流程和报表-1。

### 💎 核心架构对比

### ⚠️ 开发者注意事项

- 迁移成本：OWL 2.x 与 1.x 的组件生命周期钩子不兼容，旧版 Widget 需重写为 OWL 组件-1-4。

迁移成本：

- OWL 2.x 与 1.x 的组件生命周期钩子不兼容，旧版 Widget 需重写为 OWL 组件-1-4。

OWL 2.x 与 1.x 的组件生命周期钩子不兼容，旧版 Widget 需重写为 OWL 组件-1-4。

- 性能调优：避免过度使用 t-cache，需精确指定依赖模型防止数据更新失效-1。

性能调优：

- 避免过度使用 t-cache，需精确指定依赖模型防止数据更新失效-1。

避免过度使用 t-cache，需精确指定依赖模型防止数据更新失效-1。

- 生态兼容：第三方模块需适配 OWL 和 TypeScript 规范，否则可能引发冲突-2。

生态兼容：

- 第三方模块需适配 OWL 和 TypeScript 规范，否则可能引发冲突-2。

第三方模块需适配 OWL 和 TypeScript 规范，否则可能引发冲突-2。

### 💡 总结

Odoo 的前端演进本质是 从后端耦合到前端自治 的转型：

- 技术驱动：jQuery → OWL → BlockDOM + TypeScript。

技术驱动：jQuery → OWL → BlockDOM + TypeScript。

- 体验升级：全页面刷新 → 组件化局部更新 → 低代码可视化开发。

体验升级：全页面刷新 → 组件化局部更新 → 低代码可视化开发。

- 趋势：深度整合微前端、静态资源 CDN 加速（如 Cloudflare）-5，并向无代码配置演进。

趋势：深度整合微前端、静态资源 CDN 加速（如 Cloudflare）-5，并向无代码配置演进。

> 更多 OWL 框架细节可参考 Odoo 官方文档，或查阅开源实现案例-4-7。

更多 OWL 框架细节可参考 Odoo 官方文档，或查阅开源实现案例-4-7。