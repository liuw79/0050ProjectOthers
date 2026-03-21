# 高维学堂企业学习规划应用 UI设计规范

## 一、设计原则

1. **一致性原则**：全平台保持统一的视觉语言和交互模式


1. **清晰性原则**：信息层级分明，功能操作直观


1. **高效性原则**：减少用户认知负担，提高任务完成效率


1. **适应性原则**：响应式设计适配不同设备尺寸



## 二、色彩系统

### 1. 主色系

名称色值应用场景品牌蓝#00A0EBRGB(0,160,235)主要按钮、导航栏、关键操作、品牌标志浅蓝#C3E7F4次级按钮、图标填充中浅蓝#91D6F2进度条、标签背景### 2. 中性色

名称色值应用场景浅灰#EFEFEFRGB(239,239,239)背景色、卡片底色、分割线深黑#231815RGB(35,24,21)标题文字、正文、图标描述纯白#FFFFFF文字反色、卡片内容### 3. 辅助色

名称色值应用场景深蓝灰#004960深色模式背景、图表底色近黑色#002733页脚、分隔区块### 4. 强调色

名称色值应用场景浅米色#ECC2ADRGB(230,194,173)警告提示、高亮标签深蓝#2D459ARGB(45,69,154)加载动画、特殊状态指示### 配色比例

图表代码下载.kvfysmfp{overflow:hidden;touch-action:none}.ufhsfnkm{transform-origin: 0 0}#mermaid-svg-30{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#ccc;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-svg-30 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-svg-30 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-svg-30 .error-icon{fill:#a44141;}#mermaid-svg-30 .error-text{fill:#ddd;stroke:#ddd;}#mermaid-svg-30 .edge-thickness-normal{stroke-width:1px;}#mermaid-svg-30 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-30 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-30 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-svg-30 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-30 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-30 .marker{fill:lightgrey;stroke:lightgrey;}#mermaid-svg-30 .marker.cross{stroke:lightgrey;}#mermaid-svg-30 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-30 p{margin:0;}#mermaid-svg-30 .pieCircle{stroke:black;stroke-width:2px;opacity:0.7;}#mermaid-svg-30 .pieOuterCircle{stroke:black;stroke-width:2px;fill:none;}#mermaid-svg-30 .pieTitleText{text-anchor:middle;font-size:25px;fill:hsl(28.5714285714, 17.3553719008%, 86.2745098039%);font-family:"trebuchet ms",verdana,arial,sans-serif;}#mermaid-svg-30 .slice{font-family:"trebuchet ms",verdana,arial,sans-serif;fill:#ccc;font-size:17px;}#mermaid-svg-30 .legend text{fill:hsl(28.5714285714, 17.3553719008%, 86.2745098039%);font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:17px;}#mermaid-svg-30 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}50%40%8%2%色彩使用比例中性色 50%主色系 40%辅助色 8%强调色 2%## 三、字体系统

### 1. 中文字体

* **主要字体**：阿里巴巴普惠体

* Bold：导航标题、主要按钮文字


* Regular：正文内容、描述文字





### 2. 英文字体

* **主要字体**：Gotham

* Black：重要标题


* Medium：辅助信息





### 3. 字体使用规范

元素移动端PC端字重颜色主标题24px32pxBold#231815副标题18px24pxMedium#231815正文16px18pxRegular#231815辅助文字14px16pxRegular#666666按钮文字16px18pxMedium#FFFFFF标签文字12px14pxRegular#231815## 四、布局规范

### 1. 栅格系统

* **移动端**：4px基准网格


* **PC端**：8px基准网格


* 间距系统：4/8/12/16/24/32/48/64



### 2. 响应式断点

设备类型宽度范围列数间距手机<768px4列16px平板768-1024px8列24px桌面>1024px12列32px### 3. 页面边距

设备左右边距顶部边距手机16px12px平板24px16px桌面32px24px## 五、核心组件规范

### 1. 按钮系统

图表代码下载.kvfysmfp{overflow:hidden;touch-action:none}.ufhsfnkm{transform-origin: 0 0}#mermaid-svg-56{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#ccc;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-svg-56 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-svg-56 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-svg-56 .error-icon{fill:#a44141;}#mermaid-svg-56 .error-text{fill:#ddd;stroke:#ddd;}#mermaid-svg-56 .edge-thickness-normal{stroke-width:1px;}#mermaid-svg-56 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-56 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-56 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-svg-56 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-56 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-56 .marker{fill:lightgrey;stroke:lightgrey;}#mermaid-svg-56 .marker.cross{stroke:lightgrey;}#mermaid-svg-56 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-56 p{margin:0;}#mermaid-svg-56 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#ccc;}#mermaid-svg-56 .cluster-label text{fill:#F9FFFE;}#mermaid-svg-56 .cluster-label span{color:#F9FFFE;}#mermaid-svg-56 .cluster-label span p{background-color:transparent;}#mermaid-svg-56 .label text,#mermaid-svg-56 span{fill:#ccc;color:#ccc;}#mermaid-svg-56 .node rect,#mermaid-svg-56 .node circle,#mermaid-svg-56 .node ellipse,#mermaid-svg-56 .node polygon,#mermaid-svg-56 .node path{fill:#1f2020;stroke:#ccc;stroke-width:1px;}#mermaid-svg-56 .rough-node .label text,#mermaid-svg-56 .node .label text,#mermaid-svg-56 .image-shape .label,#mermaid-svg-56 .icon-shape .label{text-anchor:middle;}#mermaid-svg-56 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-svg-56 .rough-node .label,#mermaid-svg-56 .node .label,#mermaid-svg-56 .image-shape .label,#mermaid-svg-56 .icon-shape .label{text-align:center;}#mermaid-svg-56 .node.clickable{cursor:pointer;}#mermaid-svg-56 .root .anchor path{fill:lightgrey!important;stroke-width:0;stroke:lightgrey;}#mermaid-svg-56 .arrowheadPath{fill:lightgrey;}#mermaid-svg-56 .edgePath .path{stroke:lightgrey;stroke-width:2.0px;}#mermaid-svg-56 .flowchart-link{stroke:lightgrey;fill:none;}#mermaid-svg-56 .edgeLabel{background-color:hsl(0, 0%, 34.4117647059%);text-align:center;}#mermaid-svg-56 .edgeLabel p{background-color:hsl(0, 0%, 34.4117647059%);}#mermaid-svg-56 .edgeLabel rect{opacity:0.5;background-color:hsl(0, 0%, 34.4117647059%);fill:hsl(0, 0%, 34.4117647059%);}#mermaid-svg-56 .labelBkg{background-color:rgba(87.75, 87.75, 87.75, 0.5);}#mermaid-svg-56 .cluster rect{fill:hsl(180, 1.5873015873%, 28.3529411765%);stroke:rgba(255, 255, 255, 0.25);stroke-width:1px;}#mermaid-svg-56 .cluster text{fill:#F9FFFE;}#mermaid-svg-56 .cluster span{color:#F9FFFE;}#mermaid-svg-56 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(20, 1.5873015873%, 12.3529411765%);border:1px solid rgba(255, 255, 255, 0.25);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-svg-56 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#ccc;}#mermaid-svg-56 rect.text{fill:none;stroke-width:0;}#mermaid-svg-56 .icon-shape,#mermaid-svg-56 .image-shape{background-color:hsl(0, 0%, 34.4117647059%);text-align:center;}#mermaid-svg-56 .icon-shape p,#mermaid-svg-56 .image-shape p{background-color:hsl(0, 0%, 34.4117647059%);padding:2px;}#mermaid-svg-56 .icon-shape rect,#mermaid-svg-56 .image-shape rect{opacity:0.5;background-color:hsl(0, 0%, 34.4117647059%);fill:hsl(0, 0%, 34.4117647059%);}#mermaid-svg-56 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}按钮类型

主要按钮

次要按钮

文字按钮

图标按钮

禁用状态

背景： #00A0EB

文字： 白色

背景： #91D6F2

边框： 1px solid #00A0EB

背景： #EFEFEF

文字： #AAAAAA

#### 按钮规格

类型高度圆角内边距使用场景大按钮48px8px0 24px核心操作中按钮40px6px0 16px常规操作小按钮32px4px0 12px表格操作### 2. 导航系统

* **顶部导航（PC）**：

* 高度：64px


* 背景：#00A0EB


* 文字颜色：白色


* Logo尺寸：最小40px高度




* **底部导航（移动端）**：

* 高度：56px


* 图标尺寸：24x24px


* 激活状态：#00A0EB





### 3. 卡片设计

图表代码下载渲染失败### 4. 表单元素

元素高度边框圆角聚焦状态输入框48px1px solid #CCCCCC4px2px solid #00A0EB下拉框48px1px solid #CCCCCC4px2px solid #00A0EB复选框20x20px1px solid #CCCCCC4px-单选按钮20x20px1px solid #CCCCCC50%-## 六、深色模式适配

### 颜色转换

元素浅色模式深色模式背景#EFEFEF#002733卡片#FFFFFF#004960文字#231815#FFFFFF次要文字#666666#C3E7F4分割线#EFEFEF#004960## 七、品牌应用规范

### 1. Logo使用

* 最小尺寸：15mm（物理尺寸）


* 安全间距：≥Logo高度的1/2


* 禁用效果：变灰或透明度50%



### 2. 图标系统

* 线性图标：2px描边，#231815


* 填充图标：主色区域#00A0EB，辅助区域#91D6F2


* 尺寸系列：16px, 24px, 32px, 48px



### 3. 动效原则

* 持续时间：200-300ms


* 缓动曲线：ease-in-out


* 使用场景：

* 页面过渡：淡入淡出


* 操作反馈：微动效


* 加载状态：循环动画





## 八、设计交付规范

1. **设计文件**：

* 使用Figma/Sketch组件库


* 图层命名规范：类别/状态/尺寸


* 标注使用Auto Layout




1. **开发交付**：

* 提供CSS变量体系


* 图标导出SVG格式


* 动效提供Lottie文件




1. **设计验收**：

* 色彩对比度≥4.5:1


* 触摸目标≥44x44px


* 文字缩放测试（125%）





**备注**：所有设计决策应优先考虑用户体验目标和业务目标的一致性，在特殊情况下可适当调整规范，但需记录设计决策原因。

