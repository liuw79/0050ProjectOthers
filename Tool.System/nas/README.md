# NAS 文件清理工具套件

这是一套专为 NAS 存储设备设计的文件管理和清理工具，帮助您高效地整理文件、清理空间、优化存储结构。

## 🛠️ 工具概览

### 1. `quick_cleanup.sh` - 快速清理工具
**推荐首选工具** - 简单易用的交互式清理工具

**特点：**
- 🚀 即开即用，无需复杂配置
- 🎯 针对常见清理需求优化
- 🖥️ 友好的交互式界面
- ⚡ 快速扫描和清理

**主要功能：**
- 快速扫描存储空间
- 清理临时文件（.tmp, .cache, .DS_Store 等）
- 删除空目录
- 查找大文件（>100MB）
- 简单重复文件检测
- 目录大小排行
- 系统文件清理
- 一键清理模式

### 2. `nas_cleanup.sh` - 高级清理工具
功能全面的专业清理工具

**特点：**
- 🔧 高度可配置
- 📊 详细的分析报告
- 🔍 精确的重复文件检测
- 📈 HTML 报告生成
- 🛡️ 安全的清理机制

### 3. `music_organizer.sh` - 音乐文件分析工具
专业的音乐收藏分析和管理工具

**特点：**
- 🎵 专门针对音乐文件优化
- 📊 详细的格式分布分析
- 🔍 智能重复文件检测
- 📁 目录结构优化建议
- 📝 文件命名规范检查
- 🎼 古典音乐特殊支持

### 4. `music_organizer_auto.sh` - 自动音乐整理工具
基于元数据的智能音乐文件整理工具

**特点：**
- 🤖 基于音乐元数据自动分类
- 🗂️ 多种整理模式（艺术家/专辑、流派/艺术家等）
- 🔒 安全模式预览功能
- 💾 自动备份机制
- 📄 详细的整理报告

### 5. `music_config.conf` - 音乐工具配置文件
音乐分析和整理工具的专用配置文件

### 6. `nas_config.conf` - 配置文件
用于自定义清理参数和规则

## 🚀 快速开始

### 方法一：本地清理工具（推荐用于本地挂载的 NAS）

```bash
# 1. 进入工具目录
cd nas

# 2. 给脚本执行权限
chmod +x quick_cleanup.sh

# 3. 运行快速清理工具
./quick_cleanup.sh
```

### 方法二：远程 SSH 清理工具（推荐用于远程 NAS）

a```bash
# 1. 配置 NAS 连接信息（已配置：192.168.3.50:30220）
# 连接信息存储在 nas_connection.conf 中

# 2. 测试 NAS 连接
./test_nas_connection.sh

# 3. 运行远程清理工具
./remote_nas_cleanup.sh
```

### 方法三：高级清理工具

```bash
# 1. 配置 NAS 路径（编辑 nas_config.conf）
vim nas_config.conf

# 2. 给脚本执行权限
chmod +x nas_cleanup.sh

# 3. 运行高级清理工具
./nas_cleanup.sh
```

### 方法四：音乐文件分析和整理

```bash
# 1. 音乐文件分析
chmod +x music_organizer.sh
./music_organizer.sh

# 2. 自动音乐整理（可选）
chmod +x music_organizer_auto.sh
./music_organizer_auto.sh

# 3. 配置音乐工具（可选）
vim music_config.conf
```

### 方法五：视频文件分析和整理

使用视频分析工具对NAS中的视频文件进行全面分析：

```bash
# 基本分析（推荐先使用）
./video_organizer.sh --dry-run

# 使用自定义配置
./video_organizer.sh -c custom_video_config.conf --dry-run

# 详细输出模式
./video_organizer.sh --dry-run --verbose

# 支持命令行注释
./video_organizer.sh --dry-run # 先分析
```

**工具特点：**
- ✅ 已修复参数解析问题，支持命令行注释
- ✅ 已安装必要依赖：ffmpeg、mediainfo
- ✅ 兼容macOS系统，使用自定义文件大小格式化函数
- ✅ 成功分析10,761个视频文件
- ✅ 生成详细的HTML分析报告
- 🤖 **智能删除建议** - 基于文件大小、时长、分辨率、编码格式等维度分析
- 💾 **数据缓存** - 避免重复分析，节省时间
- 🎯 **交互式删除** - 在报告中标记文件并生成删除脚本

**智能删除建议功能：**
工具会自动分析以下维度并给出删除建议：
- **文件大小**: 过小的文件 (<10MB) 可能是预览或损坏文件
- **视频时长**: 过短的视频 (<1分钟) 可能是片段或预览
- **分辨率**: 低分辨率文件 (<480p) 画质较差
- **编码格式**: 过时的格式 (wmv, flv, 3gp)
- **文件名模式**: 包含 test, temp, backup, copy, duplicate 等关键词

**数据缓存：**
- 分析结果会缓存在 `cache/` 目录中
- 只有文件修改时间变化才会重新分析
- 大幅提升重复运行的速度

```bash
# 1. 视频文件分析
chmod +x video_organizer.sh
./video_organizer.sh

# 2. 自动视频整理（可选）
chmod +x video_organizer_auto.sh
./video_organizer_auto.sh

# 3. 配置视频工具（可选）
vim video_config.conf

# 4. 分析完成后，打开生成的HTML报告
# 在报告中可以:
# - 查看智能删除建议
# - 标记要删除的文件
# - 生成删除脚本
# - 手动执行删除操作
```

## 📋 使用指南

### 首次使用

1. **设置 NAS 路径**
   - 快速清理工具：运行后选择 "配置设置" 修改路径
   - 高级清理工具：编辑 `nas_config.conf` 文件中的 `NAS_PATH`

2. **权限设置**
   ```bash
   chmod +x *.sh
   ```

3. **开始清理**
   - 建议先运行 "快速扫描" 了解存储状况
   - 根据扫描结果选择合适的清理操作

### 常见清理流程

#### 🧹 日常维护清理
```bash
./quick_cleanup.sh
# 选择：8) 一键清理
```

#### 🔍 深度空间分析
```bash
./quick_cleanup.sh
# 依次选择：
# 1) 快速扫描
# 4) 查找大文件
# 6) 目录大小排行
```

#### 🗂️ 重复文件清理
```bash
./nas_cleanup.sh
# 使用高级工具的精确重复文件检测
```

#### 🎵 音乐收藏分析
```bash
./music_organizer.sh
# 依次选择：
# 1) 分析音乐格式分布
# 2) 分析目录结构
# 3) 查找重复文件
# 6) 完整分析（推荐）
```

#### 🎼 音乐文件自动整理
```bash
./music_organizer_auto.sh
# 建议流程：
# 1) 预览整理计划（安全模式）
# 5) 配置整理选项
# 7) 完整整理流程
```

## 🎯 清理建议

### 安全清理顺序
1. **临时文件** - 最安全，可以放心删除
2. **空目录** - 相对安全，删除前确认
3. **系统文件** - 清理 .DS_Store 等系统生成文件
4. **大文件** - 需要手动检查，谨慎删除
5. **重复文件** - 需要仔细比较，保留一份即可

### 文件类型说明

#### 🗑️ 可安全删除的临时文件
- `.tmp`, `.temp` - 临时文件
- `.cache` - 缓存文件
- `.bak`, `.old` - 备份文件
- `.DS_Store` - macOS 系统文件
- `Thumbs.db` - Windows 缩略图文件
- `@eaDir` - Synology 系统目录

#### ⚠️ 需要谨慎处理的文件
- 大文件（>100MB）- 可能是重要的媒体文件
- 重复文件 - 确认内容相同后再删除
- 空目录 - 可能有特殊用途

## ⚙️ 配置说明

### 快速清理工具配置
- 运行时选择 "配置设置" 进行配置
- 主要配置项：NAS 路径

### 高级清理工具配置
编辑 `nas_config.conf` 文件：

```bash
# 基本配置
NAS_PATH="/volume1"              # NAS 根路径
MIN_FILE_SIZE_MB=100            # 大文件阈值
MAX_SCAN_DEPTH=10               # 扫描深度

# 清理规则
CLEAN_TEMP_FILES=true           # 清理临时文件
CLEAN_EMPTY_DIRS=true           # 清理空目录
CLEAN_DUPLICATES=false          # 清理重复文件（谨慎）
```

### 音乐工具配置
编辑 `music_config.conf` 文件：

```bash
# 音乐文件路径配置
MUSIC_ROOT_PATH="/volume1/music"     # 音乐根目录
ORGANIZED_PATH="/volume1/music_organized"  # 整理后目录

# 支持的音乐格式
SUPPORTED_AUDIO_FORMATS=("flac" "mp3" "wav" "aac" "m4a" "ogg")

# 整理模式配置
ORGANIZATION_PATTERN="artist/album"  # 整理模式
SAFE_MODE=true                      # 安全模式
CREATE_BACKUP_BEFORE_CHANGES=true   # 操作前备份

# 古典音乐特殊配置
ENABLE_COMPOSER_GROUPING=true       # 启用作曲家分组
CLASSICAL_NAMING_PATTERN="{composer}/{work}/{movement}"
```

### 视频工具配置
编辑 `video_config.conf` 文件：

```bash
# 视频文件路径配置（SMB挂载点）
VIDEO_ROOT_PATH="/Volumes/video"     # 视频根目录
ORGANIZED_PATH="/Volumes/video_organized"  # 整理后目录

# 支持的视频格式
SUPPORTED_VIDEO_FORMATS=("mp4" "mkv" "avi" "mov" "wmv" "flv" "webm" "m4v" "ts")

# 文件大小阈值
MIN_FILE_SIZE="10M"    # 小文件标记
MAX_FILE_SIZE="50G"    # 大文件关注
HUGE_FILE_SIZE="10G"   # 超大文件特殊处理

# 整理设置
AUTO_ORGANIZE="false"  # 自动整理开关
DRY_RUN="true"         # 测试模式
DETECT_DUPLICATES="true"  # 重复检测

# 目录映射（基于实际11TB视频库）
# 电影: 4.3TB, 5616文件
# 电视: 2.7TB, 8460文件  
# 动画: 1.3TB, 3862文件
# 演出: 1.5TB
# 记录片: 363G, 540文件
# 教程: 739G, 5540文件
```

## 📊 报告功能

### 快速清理工具
- 实时显示清理进度
- 统计删除文件数量和释放空间

### 高级清理工具
- 生成详细的 HTML 报告
- 包含文件分布图表
- 清理前后对比

### 音乐分析工具
- 音乐格式分布统计
- 目录结构分析报告
- 重复文件检测结果
- 文件大小分布图表
- 命名规范检查报告
- 美观的 HTML 可视化报告

### 音乐整理工具
- 整理操作详细日志
- 文件移动统计报告
- 整理前后对比
- 错误和警告汇总
- 整理建议和优化提示

### 视频分析工具
- 视频格式分布（mp4, mkv, avi等）
- 分辨率质量分析（4K, 1080p, 720p等）
- 目录大小统计（11TB总量分析）
- 大文件识别（>5GB文件）
- 重复文件检测
- 比特率和编码分析
- 交互式HTML报告

### 视频整理工具
- 文件移动统计
- 空间优化建议
- 重复文件处理结果
- 目录结构重组日志
- 错误处理汇总

## 🛡️ 安全特性

- **确认机制** - 删除前需要用户确认
- **备份建议** - 重要文件建议先备份
- **日志记录** - 记录所有操作
- **分步执行** - 可以逐步进行清理
- **路径验证** - 防止误操作

## 🔧 故障排除

### 常见问题

1. **权限不足**
   ```bash
   chmod +x *.sh
   # 或者使用 sudo 运行
   ```

2. **路径不存在**
   - 检查 NAS 是否正确挂载
   - 确认路径配置正确

3. **扫描速度慢**
   - 大容量存储扫描需要时间
   - 可以限制扫描深度

4. **音乐元数据读取失败**
   ```bash
   # 安装 ffmpeg（包含 ffprobe）
   # macOS: brew install ffmpeg
   # Ubuntu: sudo apt install ffmpeg
   ```

5. **音乐文件整理权限问题**
   - 确保对音乐目录有读写权限
   - 建议先使用安全模式预览

### 视频工具特定问题

6. **参数解析错误**
   - 问题：`未知选项: #` 或 `未知选项: 先分析`
   - 原因：脚本无法正确处理命令行注释
   - 解决：已修复参数解析逻辑，支持忽略注释和中文描述

7. **依赖工具缺失**
   - 问题：`缺少以下工具: ffprobe (ffmpeg) mediainfo`
   - 解决：`brew install ffmpeg mediainfo`

8. **numfmt命令不存在**
   - 问题：`numfmt: command not found`
   - 原因：macOS默认不包含numfmt工具
   - 解决：已实现自定义文件大小格式化函数

9. **bash语法兼容性**
   - 问题：`${ext,,}: bad substitution`
   - 原因：某些bash版本不支持新语法
   - 解决：使用`tr '[:upper:]' '[:lower:]'`替代

## 🎵 音乐工具特殊说明

### 支持的音乐格式
- **无损格式**: FLAC, APE, WAV, AIFF, DSD
- **有损格式**: MP3, AAC, M4A, OGG, WMA
- **特殊格式**: MKA, MPC, TTA, WV

### 整理模式说明
1. **artist_album** - 艺术家/专辑 (推荐)
2. **genre_artist** - 流派/艺术家/专辑
3. **year_artist** - 年份/艺术家/专辑
4. **composer_work** - 作曲家/作品 (古典音乐专用)

### 古典音乐特殊处理
- 自动识别古典音乐关键词
- 支持作曲家分组
- 特殊的命名规则
- 作品和乐章结构化整理

### 安全建议
1. **首次使用必须启用安全模式**
2. **重要音乐收藏请先备份**
3. **建议分批次整理大型音乐库**
4. **定期检查整理结果和报告**

### 性能优化
- 大型音乐库（>10000文件）建议分目录处理
- 可调整并发处理数量
- 内存使用限制可配置
- 支持断点续传功能

## 电视目录标准化完整流程

### 标准化目标
- 所有文件夹必须包含中文名称
- 格式：`中文名.英文名.季数.年份 [评分]`
- 消除重复文件夹
- 统一命名规范

### 处理步骤

#### 1. 初步分析
```bash
# 检查目录状态
ls -la | head -20

# 统计文件夹数量
ls -1 | wc -l
```

#### 2. 识别问题文件夹
```python
# 检查缺少中文名称的文件夹
import re
from pathlib import Path

for folder in Path('.').iterdir():
    if folder.is_dir() and not re.search(r'[\u4e00-\u9fff]', folder.name):
        print(folder.name)
```

#### 3. 批量重命名处理
创建批量重命名脚本，包含常见影视剧的中英文对照：
- 《权力的游戏》Game of Thrones
- 《基地》Foundation  
- 《金装律师》Suits
- 《东京爱情故事》Tokyo Love Story
- 等等...

#### 4. 最终验证
确保所有72个文件夹都包含中文名称，达到100%标准化率。

### 常见问题解决

#### 重复文件夹处理
- 保留质量更好的版本
- 删除命名不规范的重复项

#### 特殊情况
- CCTV开头的文件夹已包含中文，无需额外处理
- 季数格式统一为"Season X"或"SXX"
- 评分统一为"[无评分]"格式

## 电视剧智能评分系统

### 评分标准
- **9.0-9.5分**: 经典神剧，必看佳作
- **8.5-8.9分**: 优秀佳作，强烈推荐
- **8.0-8.4分**: 值得一看，质量不错
- **7.5-7.9分**: 还不错，可以考虑
- **7.0-7.4分**: 一般般，时间充裕可看

### 评分结果统计
- **文件夹总数**: 72部
- **已评分**: 42部
- **评分分布**:
  - 经典神剧 (9.0+): 8部
  - 优秀佳作 (8.5+): 8部
  - 值得一看 (8.0+): 10部
  - 还不错 (7.5+): 12部
  - 一般般 (7.0+): 4部

### 推荐观看清单

#### 🏆 经典神剧 (9.0+分)
- 《大秦帝国·联盟》(9.3分) - 历史正剧巅峰
- 《我的团长我的团》(9.4分) - 抗战题材经典
- 《CCTV航拍中国》(9.2分) - 纪录片精品
- 《三国》(9.1分) - 古装历史剧
- 《权力的游戏》(9.2分) - 奇幻史诗
- 《苍穹浩瀚》(9.0分) - 科幻太空剧
- 《东京爱情故事》(9.0分) - 日剧经典

#### ⭐ 优秀佳作 (8.5+分)
- 《风味人间》(8.9分) - 美食纪录片
- 《爱死亡和机器人》(8.9分) - 科幻动画
- 《大江大河》(8.8分) - 改革开放题材
- 《基地》(8.8分) - 科幻史诗
- 《机智的医生生活》(8.7分) - 韩国医疗剧
- 《心灵奇旅》(8.7分) - 动画电影
- 《山河令》(8.6分) - 古装武侠
- 《金装律师》(8.5分) - 律政职场剧

### 使用方法
```bash
# 运行评分系统
python3 tv_rating_system.py
```

评分系统会自动:
1. 识别文件夹中的中文剧名
2. 匹配内置的评分数据库
3. 将"[无评分]"替换为具体分数
4. 生成评分统计报告

## 智能删除建议系统

### 删除策略分类

#### 🗑️ 自动删除（安全）
- **元数据文件**: .nfo、.xml、-thumb.jpg、-poster.jpg、.DS_Store
- **空文件夹**: 完全空的目录
- **过小文件夹**: 总大小<100MB且无有效视频内容
- **临时文件**: .tmp、.temp、.cache等临时文件
- **重复后缀**: 同名文件夹的多个版本（保留最大）

#### ⚠️ 建议删除（需确认）
- **低质量版本**: 同一内容的多个分辨率版本（保留最高质量）
- **不完整下载**: 文件名包含"part"、"incomplete"等
- **样本文件**: Sample、Preview等预览文件
- **字幕包**: 独立的字幕文件夹（如果视频已内嵌字幕）
- **发布说明**: ReadMe、NFO说明文件夹

#### 🔍 人工审核（谨慎处理）
- **异常大小**: 明显超出正常范围的文件夹
- **命名异常**: 包含乱码或特殊字符的文件夹
- **格式过时**: VCD、RMVB等过时格式
- **语言版本**: 非中文且无字幕的外语版本

### 删除建议工具

#### 智能分析脚本
```bash
# 1. 运行智能删除分析器（生成删除建议报告）
python3 smart_deletion_analyzer.py

# 2. 运行安全删除执行器（模拟模式）
python3 safe_deletion_executor.py

# 3. 执行实际删除操作
python3 safe_deletion_executor.py --execute
```

#### 工具功能说明

**smart_deletion_analyzer.py** - 智能删除建议分析器
- 🔍 全面分析目录中可删除的内容
- 📊 生成详细的删除建议报告
- 🏷️ 按安全级别分类（自动删除/建议删除/人工审核）
- 💾 保存JSON格式的详细分析结果

**safe_deletion_executor.py** - 安全删除执行器
- 🧪 支持模拟模式，安全预览删除项目
- 🗑️ 只删除100%安全的项目（空文件夹、元数据文件、过小无视频文件夹）
- 📝 生成详细的删除日志
- 🔒 内置安全保障机制

#### 安全删除流程
1. **生成删除建议报告**
2. **人工审核确认**
3. **分批次执行删除**
4. **验证删除结果**

### 删除统计示例

#### 电视目录智能删除成果
- 📁 处理前文件夹: 72个
- 📁 处理后文件夹: 70个
- 🗑️ 删除过小文件夹: 5个（无视频内容）
- 📄 删除元数据文件: 4个（.nfo和-thumb.jpg文件）
- 💾 释放空间: 223.8KB
- ✅ 删除成功率: 100%（9/9项目）

#### 删除项目详情
**自动删除的过小文件夹:**
- 龙之家族S01.House.of.the.Dragon.2022. [无评分] (69.0KB)
- CCTV航拍中国.第一季第二集.海南.Aerial.China.S01E02.Hainan.MP2 [9.2分] (413B)
- 苍穹浩瀚S01.Season 2.The.Expanse. [9.0分] (67.6KB)
- 傲骨之战S01.Season 3.The.Good.Fight. [8.3分] (63.4KB)
- 基地.Foundation.S01E06.Death.and.the.Maiden [8.8分] (16.9KB)

**自动删除的元数据文件:**
- 人体内旅行和地球内部之旅的.nfo和-thumb.jpg文件

#### 需人工审核项目（未删除）
- 爱死亡和机器人.Love.Death.&.Robots.Season.1 [8.9分] (22.1GB)
- 电影.The.Movies.Season.1.GUACAMOLE [7.5分] (46.4GB)
- 三国.Three.Kingdoms.2010.WiKi [9.1分] (224.9GB)
- 金装律师.Suits.Season.1.4.DTG [8.5分] (37.3GB)

#### 动画目录清理成果
- 📁 处理前文件夹: 42个
- 📁 处理后文件夹: 40个
- 🗑️ 删除重复文件夹: 2个
- 📄 删除无用文件: 15个
- 💾 释放空间: ~1.8GB

### 安全保障措施

#### 删除前备份
```bash
# 创建删除清单
echo "删除时间: $(date)" > deletion_log.txt
echo "删除项目:" >> deletion_log.txt
```

#### 回滚机制
- 保留删除日志
- 重要内容移至回收站而非直接删除
- 分阶段删除，便于中途停止

#### 验证检查
- 删除后重新扫描目录
- 确认重要内容未误删
- 生成删除后状态报告

## 电影目录全面排查

### 当前剩余英文目录列表 (118个)

截至批量重命名完成后，以下是剩余的英文电影目录：

```
Extended Collector's Edition Disc 1 (2009)
Ikiru (1952)
In the Mood for Love (2000)
Incendies (2010)
Inception (2010)
Indiana Jones and the Last Crusade (1989)
Inglourious Basterds (2009)
Interstellar (2014)
It's a Wonderful Life (1946)
Joker (2019)
Journey.to.the.West.The.Demons.Strike.Back.2017.720p.BluRay.x264-WiKi (2017)
Just Heroes (1989)
Justice.My.Foot.1992.1080p.BluRay.x264-WiKi (1992)
King of Comedy (1999)
King.of.Beggars.1992.720p.BluRay.x264-WiKi (1992)
King.of.Comedy.1999.HDTV.720p.AC3.2Audio.x264-CHDTV (1999)
Kis.Uykusu (2014)
Klaus (2019)
Knockout - Blu-ray™ (2020)
Koe.no.katachi (2016)
L.A. Confidential (1997)
La.grande.bellezza (2013)
Ladies Market (2021)
Lawyer.Lawyer.1997.720p.HDTV.x264-XXFANS (1997)
Leap (2020)
Leap Year 2010 (2010)
Léon - The Professional - Extended Edition (1994)
Life of Pi (2012)
Like Stars on Earth (2007)
Look Out, Officer! (1990)
Love on Delivery (1994)
Love Will Tear Us Apart (2021)
Love, Rosie (2014)
Love.is.Love.1990.Blu-ray.720p.x264.DTS.DD51.DualAudio.MySilu (1990)
Loving Vincent (2017)
Luca (2021)
M (1931)
MADE IN HONG KONG (1997)
Made in Italy (2020)
Man in Love (2021)
Memento (2000)
Merry Christmas Mr. Lawrence (1983)
Metropolis (1927)
MNHD-FRDS (2019)
Moana (2016)
Modern Times (1936)
Monty Python and the Holy Grail (1975)
Moon Man (2022)
MPEG-4 AVC Video 26934 kbps 1080p 23,976 fps 16-9 High Profile 4.1 (2009)
MPEG-4 x264@High Profile L4.1, 24 fps @ 10800 kbps (2018)
MPEG-H,HEVC x265 Main 10@L5.1@High, 24 1.001 fps @ 12966 kbps (2014)
Mulan (2020)
My People, My Country (2019)
Netemo sametemo 2018 (2018)
New Police Story (2004)
News of the World 2020 (2020)
Nice View (2022)
Nightmare Alley (2021) 1080p HDR Encode (2021)
No Man's Land (2013)
North by Northwest (1959)
Oldboy (2003)
Oldboy.2003.1080p.TWN.Blu-ray.AVC.DTS-HD.MA.5.1-hc@PTHome (2003)
Once Upon a Time in America (1984)
Once Upon a Time in the West (1968)
Operation Red Sea (2018)
Oppenheimer (2023)
Osaka.Loan.Shark (2021)
Paths of Glory (1957)
Pegasus (2019)
Perfume - The Story of a Murderer (2006)
Police Story - Lockdown (2013)
Police.Story.I (1985)
Police.Story.II (1988)
Police.Story.III.Super.Cop (1992)
Police.Story.IV.First.Strike (1996)
Princess Mononoke (1997)
Psycho (1960)
Raiders of the Lost Ark (1981)
Raiders of the Lost Ark 1981 (1981)
Railway Heroes (2021)
Rear Window (1954)
Redeeming Love (2022)
Remuxed by KAWAiREMUX group @ACM (2006)
Royal.Tramp.1992.BluRay.720p.AC3.2Audio.x264-CHD (1992)
Royal.Tramp.2.1992.BluRay.720p.AC3.2Audio.x264-CHD (1992)
RTHK TV 31.Philharmonic.5.Beethoven.at.teamLab.Tokyo (2020)
Running.on.Empty (1988)
Rush Hour (1998)
Salyut-7 (2017)
Scarface (1983)
Scary Movie (2000)
Scary Movie 2 (2001)
Scary Movie 3 (2003)
Scent.of.a.Woman.1992.1080p.BluRay.x264.DTS-FiDELiO (1992)
Se7en (1995)
Seven Samurai (1954)
Shaolin Soccer (2001)
Shattered.2021 (2022)
Sicario - Blu-ray (2015)
Sin.City.A.Dame.to.Kill.For.2014.1080p.BluRay.x265.10bit.DTS-PTH
Sixty.Million.Dollar.Man.1995.720p.BluRay.x264-WiKi (1995)
Snatch (2000)
Song of the Sea (2014)
Soul (2020)
SoulMate 2016 (2016)
Space Sweepers (2021)
Spider-Man - Across The Spider-Verse (2023)
Spider-Man - Into the Spider-Verse (2018)
Spider-Man.3 (2007)
Star Trek (2009)
Star Trek Beyond (2016)
Star Trek II - The Wrath of Khan (1982)
Star Trek III - The Search for Spock (1984)
Star Trek Into Darkness (2013)
Star Trek IV - The Voyage Home (1986)
Star Trek VI - The Undiscovered Country (1991)
Star.Trek.I.The.Motion.Picture (1979)
Star.Trek.IX.Insurrection (1998)
Star.Trek.VII.Generations (1994)
Star.Trek.VIII.First.Contact (1996)
Star.Trek.X.Nemesis (2002)
Suk.Suk (2020)
Sully (2016)
Summer Detective 2019 (2019)
Sunset Blvd. (1950)
Systemsprenger 2019 (2019)
Talvisota elokuvan kuvaukset Keuruulla (1989)
The Intouchables (2011)
The Invisible Man (2020)
The Kid (1921)
The Lives of Others (2006)
The Lucky Guy (1998)
THE LUNCHBOX (2013)
The Mermaid (2016)
The Old Guard (2020)
The Piano (1993)
The Piano Teacher (2001)
The Sting (1973)
The Swordsman In Double Flag Town - Blu-ray™ (1991)
The Tourist (2010)
The Wandering Earth II (2023)
The Wolf of Wall Street (2013)
The Yellow Sea 2010 (2010)
The.Beach.2000.Open.Matte.1080p.WEB-DL.DD5.1.H.264-spartanec163 (2000)
The.God.of.Cookery.1996.720p.HDTV.x264.2Audio-HDCTV (1996)
The.Human.Centipede.2009.BluRay.1080p.DTS.x264-CHD (2009)
The.Kings.Man (2021)
Time of the Gypsies (1988)
Togo (2019)
Tomorrowland (2015)
Tropic.Thunder.Directors.Cut (2008)
Umibe.no.Etranger (2020)
Un.sac.de.billes (2017)
Under the Open Sky (2021)
Up (2009)
Vettai (2012)
Vive L'Amour (1995)
Vychislitel AKA The Calculator [2014] 1080p BluRay - HJ (2014)
WALL·E (2008)
Western Stars (2019)
What a Wonderful Family 2 2017 1080p BluRay DD5.1 x265-10bit-HDS (2017)
What a Wonderful Family 3 My Wife My Life 2018 1080p BluRay DTS x264-HDS (2018)
When.Fortune.Smiles.1990.BluRay.720p.DTS x264-CHD (1990)
Whiplash (2014)
Wild Bill (2011)
Witness for the Prosecution (1957)
Yi Yi (2000) (2000)
Your Name. (2016)
Your Place or Mine (1998)
```

### 批量重命名统计
- **成功重命名**: 87个电影目录
- **跳过处理**: 27个（目标已存在）
- **处理失败**: 0个
- **剩余英文目录**: 118个

### 英文电影中文译名对照表

| 英文原名 | 中文译名 | 年份 |
|---------|---------|------|
| Extended Collector's Edition Disc 1 | 指环王扩展收藏版光盘1 | (2009) |
| Ikiru | 生之欲 | (1952) |
| In the Mood for Love | 花样年华 | (2000) |
| Incendies | 烈火焚身 | (2010) |
| Inception | 盗梦空间 | (2010) |
| Indiana Jones and the Last Crusade | 夺宝奇兵3：圣战奇兵 | (1989) |
| Inglourious Basterds | 无耻混蛋 | (2009) |
| Interstellar | 星际穿越 | (2014) |
| It's a Wonderful Life | 生活多美好 | (1946) |
| Joker | 小丑 | (2019) |
| Journey.to.the.West.The.Demons.Strike.Back | 西游伏妖篇 | (2017) |
| Just Heroes | 义胆群英 | (1989) |
| Justice.My.Foot | 审死官 | (1992) |
| King of Comedy | 喜剧之王 | (1999) |
| King.of.Beggars | 武状元苏乞儿 | (1992) |
| King.of.Comedy | 喜剧之王 | (1999) |
| Kis.Uykusu | 冬眠 | (2014) |
| Klaus | 克劳斯：圣诞节的秘密 | (2019) |
| Knockout | 拳击手 | (2020) |
| Koe.no.katachi | 声之形 | (2016) |
| L.A. Confidential | 洛城机密 | (1997) |
| La.grande.bellezza | 绝美之城 | (2013) |
| Ladies Market | 女人街 | (2021) |
| Lawyer.Lawyer | 算死草 | (1997) |
| Leap | 飞奔去月球 | (2020) |
| Leap Year 2010 | 闰年 | (2010) |
| Léon - The Professional - Extended Edition | 这个杀手不太冷：导演剪辑版 | (1994) |
| Life of Pi | 少年派的奇幻漂流 | (2012) |
| Like Stars on Earth | 地球上的星星 | (2007) |
| Look Out, Officer! | 师兄撞鬼 | (1990) |
| Love on Delivery | 破坏之王 | (1994) |
| Love Will Tear Us Apart | 爱情神话 | (2021) |
| Love, Rosie | 爱你，罗茜 | (2014) |
| Love.is.Love | 阿飞正传 | (1990) |
| Loving Vincent | 至爱梵高·星空之谜 | (2017) |
| Luca | 夏日友晴天 | (2021) |
| M | M就是凶手 | (1931) |
| MADE IN HONG KONG | 香港制造 | (1997) |
| Made in Italy | 意大利制造 | (2020) |
| Man in Love | 恋爱中的男人 | (2021) |
| Memento | 记忆碎片 | (2000) |
| Merry Christmas Mr. Lawrence | 圣诞快乐劳伦斯先生 | (1983) |
| Metropolis | 大都会 | (1927) |
| MNHD-FRDS | 技术规格目录 | (2019) |
| Moana | 海洋奇缘 | (2016) |
| Modern Times | 摩登时代 | (1936) |
| Monty Python and the Holy Grail | 巨蟒与圣杯 | (1975) |
| Moon Man | 独行月球 | (2022) |
| MPEG-4 AVC Video | 技术规格目录 | (2009) |
| MPEG-4 x264 | 技术规格目录 | (2018) |
| MPEG-H,HEVC x265 | 技术规格目录 | (2014) |
| Mulan | 花木兰 | (2020) |
| My People, My Country | 我和我的祖国 | (2019) |
| Netemo sametemo | 昼颜 | (2018) |
| New Police Story | 新警察故事 | (2004) |
| News of the World | 世界新闻 | (2020) |
| Nice View | 奇迹·笨小孩 | (2022) |
| Nightmare Alley | 玉面情魔 | (2021) |
| No Man's Land | 无人区 | (2013) |
| North by Northwest | 西北偏北 | (1959) |
| Oldboy | 老男孩 | (2003) |
| Oldboy.2003 | 老男孩 | (2003) |
| Once Upon a Time in America | 美国往事 | (1984) |
| Once Upon a Time in the West | 西部往事 | (1968) |
| Operation Red Sea | 红海行动 | (2018) |
| Oppenheimer | 奥本海默 | (2023) |
| Osaka.Loan.Shark | 大阪放贷人 | (2021) |
| Paths of Glory | 光荣之路 | (1957) |
| Pegasus | 飞驰人生 | (2019) |
| Perfume - The Story of a Murderer | 香水：一个杀手的故事 | (2006) |
| Police Story - Lockdown | 警察故事2013 | (2013) |
| Police.Story.I | 警察故事 | (1985) |
| Police.Story.II | 警察故事续集 | (1988) |
| Police.Story.III.Super.Cop | 警察故事3：超级警察 | (1992) |
| Police.Story.IV.First.Strike | 警察故事4：简单任务 | (1996) |
| Princess Mononoke | 幽灵公主 | (1997) |
| Psycho | 惊魂记 | (1960) |
| Raiders of the Lost Ark | 夺宝奇兵 | (1981) |
| Raiders of the Lost Ark 1981 | 夺宝奇兵 | (1981) |
| Railway Heroes | 铁道英雄 | (2021) |
| Rear Window | 后窗 | (1954) |
| Redeeming Love | 救赎之爱 | (2022) |
| Remuxed by KAWAiREMUX group | 技术重制版本 | (2006) |
| Royal.Tramp | 鹿鼎记 | (1992) |
| Royal.Tramp.2 | 鹿鼎记2：神龙教 | (1992) |
| RTHK TV 31.Philharmonic | 港台电视音乐节目 | (2020) |
| Running.on.Empty | 不归路 | (1988) |
| Rush Hour | 尖峰时刻 | (1998) |
| Salyut-7 | 礼炮7号 | (2017) |
| Scarface | 疤面煞星 | (1983) |
| Scary Movie | 惊声尖笑 | (2000) |
| Scary Movie 2 | 惊声尖笑2 | (2001) |
| Scary Movie 3 | 惊声尖笑3 | (2003) |
| Scent.of.a.Woman | 闻香识女人 | (1992) |
| Se7en | 七宗罪 | (1995) |
| Seven Samurai | 七武士 | (1954) |
| Shaolin Soccer | 少林足球 | (2001) |
| Shattered.2021 | 破碎 | (2022) |
| Sicario - Blu-ray | 边境杀手 | (2015) |
| Sin.City.A.Dame.to.Kill.For | 罪恶之城2：红颜夺命 | (2014) |
| Sixty.Million.Dollar.Man | 百变星君 | (1995) |
| Snatch | 偷拐抢骗 | (2000) |
| Song of the Sea | 海洋之歌 | (2014) |
| Soul | 心灵奇旅 | (2020) |
| SoulMate 2016 | 七月与安生 | (2016) |
| Space Sweepers | 胜利号 | (2021) |
| Spider-Man - Across The Spider-Verse | 蜘蛛侠：纵横宇宙 | (2023) |
| Spider-Man - Into the Spider-Verse | 蜘蛛侠：平行宇宙 | (2018) |
| Spider-Man.3 | 蜘蛛侠3 | (2007) |
| Star Trek | 星际迷航 | (2009) |
| Star Trek Beyond | 星际迷航3：超越星辰 | (2016) |
| Star Trek II - The Wrath of Khan | 星际迷航2：可汗怒吼 | (1982) |
| Star Trek III - The Search for Spock | 星际迷航3：石破天惊 | (1984) |
| Star Trek Into Darkness | 星际迷航：暗黑无界 | (2013) |
| Star Trek IV - The Voyage Home | 星际迷航4：抢救未来 | (1986) |
| Star Trek VI - The Undiscovered Country | 星际迷航6：未来之城 | (1991) |
| Star.Trek.I.The.Motion.Picture | 星际迷航1：无限太空 | (1979) |
| Star.Trek.IX.Insurrection | 星际迷航9：起义 | (1998) |
| Star.Trek.VII.Generations | 星际迷航7：日换星移 | (1994) |
| Star.Trek.VIII.First.Contact | 星际迷航8：第一类接触 | (1996) |
| Star.Trek.X.Nemesis | 星际迷航10：复仇女神 | (2002) |
| Suk.Suk | 叔·叔 | (2020) |
| Sully | 萨利机长 | (2016) |
| Summer Detective 2019 | 夏日侦探 | (2019) |
| Sunset Blvd. | 日落大道 | (1950) |
| Systemsprenger 2019 | 系统破坏者 | (2019) |
| Talvisota elokuvan kuvaukset | 冬季战争拍摄花絮 | (1989) |
| The Intouchables | 触不可及 | (2011) |
| The Invisible Man | 隐形人 | (2020) |
| The Kid | 寻子遇仙记 | (1921) |
| The Lives of Others | 窃听风暴 | (2006) |
| The Lucky Guy | 行运一条龙 | (1998) |
| THE LUNCHBOX | 午餐盒 | (2013) |
| The Mermaid | 美人鱼 | (2016) |
| The Old Guard | 永生守卫 | (2020) |
| The Piano | 钢琴课 | (1993) |
| The Piano Teacher | 钢琴教师 | (2001) |
| The Sting | 骗中骗 | (1973) |
| The Swordsman In Double Flag Town | 双旗镇刀客 | (1991) |
| The Tourist | 游客 | (2010) |
| The Wandering Earth II | 流浪地球2 | (2023) |
| The Wolf of Wall Street | 华尔街之狼 | (2013) |
| The Yellow Sea | 黄海 | (2010) |
| The.Beach | 海滩 | (2000) |
| The.God.of.Cookery | 食神 | (1996) |
| The.Human.Centipede | 人体蜈蚣 | (2009) |
| The.Kings.Man | 王牌特工：源起 | (2021) |
| Time of the Gypsies | 流浪者之歌 | (1988) |
| Togo | 多哥 | (2019) |
| Tomorrowland | 明日世界 | (2015) |
| Tropic.Thunder.Directors.Cut | 热带惊雷：导演剪辑版 | (2008) |
| Umibe.no.Etranger | 海边的异邦人 | (2020) |
| Un.sac.de.billes | 一袋弹珠 | (2017) |
| Under the Open Sky | 在蓝天下 | (2021) |
| Up | 飞屋环游记 | (2009) |
| Vettai | 猎人 | (2012) |
| Vive L'Amour | 爱情万岁 | (1995) |
| Vychislitel AKA The Calculator | 计算器 | (2014) |
| WALL·E | 机器人总动员 | (2008) |
| Western Stars | 西部明星 | (2019) |
| What a Wonderful Family 2 | 家族之苦2 | (2017) |
| What a Wonderful Family 3 | 家族之苦3 | (2018) |
| When.Fortune.Smiles | 笑傲江湖 | (1990) |
| Whiplash | 爆裂鼓手 | (2014) |
| Wild Bill | 狂野比尔 | (2011) |
| Witness for the Prosecution | 控方证人 | (1957) |
| Yi Yi (2000) | 一一 | (2000) |
| Your Name. | 你的名字 | (2016) |
| Your Place or Mine | 你的地方还是我的地方 | (1998) |

### 备注
剩余的英文目录包括一些特殊情况：
1. 重复电影（如多个版本的《喜剧之王》、《夺宝奇兵》）
2. 技术规格目录（MPEG-4相关）
3. 特殊格式或版本（Extended Edition、Director's Cut等）
4. 已提供完整中文译名对照表，可用于后续批量重命名

### 排查结果概述
- **总规模**: 476个一级目录，258个多级子目录
- **主要问题**: 命名规范不统一、系列电影分散、存在空目录和临时文件
- **技术规格目录**: 65个包含详细技术信息的目录名
- **系列电影**: 发现战狼、这个男人来自地球、Star Trek等系列

### 发现的问题类型
1. **命名格式混乱**: 中文简洁、技术规格、英文、混合等多种格式并存
2. **系列电影分散**: 同系列电影分别存储，不便管理
3. **特殊目录**: 合集目录、技术分类目录、临时目录混杂
4. **空目录**: IMDB TOP250合集等空目录需要清理

### 整理计划
1. **阶段一**: 清理空目录和临时文件（高优先级）✅ **已完成**
   - 已删除2个空目录："IMDB.TOP250.2020.09 PART.I (001-125)"和"Someone.To.Talk.To.2016.4K&1080p.HEVC&AVC.4in1.WEB-DL.x264.AAC-HQC"
   - 已清理`.deletedByTMM`临时目录（两次清理，共计320个子目录，确认为重复文件）
2. **阶段二**: 命名标准化，制定统一规范（中优先级）✅ **已完成**
   - 标准化了4K分辨率标识：将"2160p"统一替换为"4K"
   - 重命名了7个目录，提升命名一致性
   - 创建了[合集]专用目录，整理了1个合集
3. **阶段三**: 系列电影整理，创建系列目录（中优先级）✅ **已完成**
   - 创建了13个系列目录：哈利波特、Marvel复仇者联盟、蜘蛛侠、战狼、唐人街探案等
   - 整理了47部系列电影，减少主目录散乱程度
   - 支持中英文系列识别，覆盖主流电影系列
4. **阶段四**: 中文名标准化（高优先级）✅ **已完成**
   - 创建了包含200+电影的英文名到中文名映射字典
   - 实现了智能匹配算法，支持多种标题变体识别
   - 批量重命名了49部英文电影为中文名（13.0%成功率）
   - 包括《肖申克的救赎》、《教父》、《阿甘正传》、《星球大战》等经典影片
   - 创建了`movie_chinese_name_organizer.py`工具
5. **阶段五**: 分类优化，按类型或质量分级（低优先级）

### 当前状态
- **NAS连接状态**: ✅ 已连接（IP: 192.168.3.50）
- **目录总数**: 466个（主目录374个 + [合集]1个 + [系列]13个 + 系列内47个 + 中文名31个）
- **已创建工具**: 
  - `movie_organizer.py` - 电影目录自动整理脚本
  - `movie_series_organizer.py` - 系列电影整理脚本
  - `movie_chinese_name_organizer.py` - 中文名标准化脚本
- **整理报告**: 
  - `movie_organization_report_20250724_121335.json`
  - `movie_series_organization_report_20250724_122251.json`
  - `movie_chinese_name_organization_report_20250724_142438.json`
- **下一步**: 考虑是否进行类型分级整理（阶段五）

### 风险控制
- 操作前完整备份
- 分批次执行
- 保留操作日志
- 测试媒体播放器兼容性

**详细报告**: `movie_directory_audit_report.md`

## 钢琴教程分级目录重新整理

### 处理结果
- **原分级教程目录**: 包含初级、中级、高级三个子目录，共22个教程
- **重新分类**: 21个教程按专业分类重新分配到对应目录
- **保留教程**: 仅保留"V叔的钢琴基础入门课"作为真正的分级教程
- **清理结果**: 自动删除了空的初级、中级、高级目录

### 分类分布
- 🎼 车尔尼系列: 8个教程（包括599、718、740、139、299、821、849等）
- 🎓 乐理基础: 4个教程（宋大叔教音乐、陈俊宇乐理等）
- 🎤 编曲伴奏: 3个教程（爵士钢琴、即兴伴奏等）
- 🎹 小汤系列: 2个教程
- 🎵 哈农练指法: 2个教程
- 其他专业分类: 各1个教程

### 重要结论
**分级教程目录应该只保留真正按难度分级的通用教程，专业教程应归类到对应的专业分类中。**

## 电视目录质量分析系统

### 质量问题分类

#### 📉 评分过低内容 (4个)
**7.0-7.4分档位:**
- 翡翠日本.Jade.Japan.45.Day.Itinerary.2022.NGB [7.3分] (7.3分, 8.9GB)
- 家园.Home.Season 1 [7.4分] (7.4分, 4.8GB)
- 究极.Kyūkyoku [7.2分] (7.2分, 1.1GB)
- 墨西哥.地球生命节.Mexico.Earths.Festival.of.Life.2017.GER.DIY.mulpsn [7.4分] (7.4分, 43.3GB)

#### 📦 异常大小内容 (1个)
- **三国.Three.Kingdoms.2010.WiKi [9.1分]** (224.9GB) - 虽然评分很高，但文件过大需要检查

#### 🔍 低质量标识内容 (4个)
- 爱死亡和机器人.Love.Death.&.Robots.Season.1 [8.9分] - 包含"ts"标识
- 电影.The.Movies.Season.1.GUACAMOLE [7.5分] - 包含"cam"标识
- 三国.Three.Kingdoms.2010.WiKi [9.1分] - 包含"wiki"标识
- 金装律师.Suits.Season.1.4.DTG [8.5分] - 包含"dtg"标识

#### ❓ 可疑命名内容 (6个)
- 第十二夜.Shakespeare's.Globe.Twelfth.Night.2013.PTerWEB [无评分]
- 【国家地理.有字幕A】 [无评分]
- 大英两千年.2013.内嵌中英字幕￡CMCT呆呆熊 [无评分]
- 请回答1988.응답하라 1988.2015 [无评分]
- 奇葩说Season [无评分]
- 究极.Kyūkyoku [7.2分]

#### 📋 无评分内容 (29个)
需要使用评分系统为这些内容添加评分

### 质量改进建议

#### 🗑️ 建议删除的内容
**评分过低且占用空间大:**
- 墨西哥.地球生命节 (7.4分, 43.3GB) - 评分一般且占用空间较大
- 究极.Kyūkyoku (7.2分) - 评分较低

#### ⚠️ 需要检查的内容
**异常大小:**
- 三国.Three.Kingdoms.2010.WiKi (224.9GB) - 检查是否包含不必要内容

**低质量标识:**
- 电影.The.Movies.Season.1.GUACAMOLE - "cam"通常表示摄像头录制
- 其他包含发布组标识的内容需要验证质量

#### 📈 优化建议
1. **空间优化**: 删除评分低于7.0的内容可释放约57GB空间
2. **质量提升**: 寻找低质量内容的高清替代版本
3. **评分完善**: 为29个无评分内容添加评分
4. **命名规范**: 修复包含特殊字符的文件夹名称

### 质量分析工具

#### tv_quality_analysis.py - 质量分析器
```bash
# 运行质量分析
python3 tv_quality_analysis.py
```

**功能特点:**
- 🔍 全面分析评分、大小、命名等质量指标
- 📊 生成详细的质量问题报告
- 💡 提供针对性的改进建议
- 📝 保存分析结果到文件

## 教程目录重构系统

### 重构目标
将现有的教程目录按照学习内容类型进行重新组织，提高查找效率和管理便利性。

### 新目录结构设计

#### 🎵 音乐艺术
- **包含内容**: 钢琴、吉他、声乐、乐理等音乐相关教程
- **子分类**: 钢琴教程、吉他教程、声乐教程、乐理基础、其他乐器
- **预计规模**: 3个教程，36.0GB，2950个文件

#### 💻 编程技术
- **包含内容**: Python、Java、Web开发等编程相关教程
- **子分类**: 前端开发、后端开发、移动开发、数据科学、算法数据结构
- **预计规模**: 1个教程，9.2GB，600个文件

#### 🎨 设计创意
- **包含内容**: Photoshop、UI设计、视频制作等设计类教程
- **子分类**: 平面设计、UI/UX设计、视频制作、3D建模、摄影后期
- **预计规模**: 1个教程，6.8GB，450个文件

#### 🌍 语言学习
- **包含内容**: 英语、日语、韩语等语言学习教程
- **子分类**: 英语学习、日语学习、韩语学习、其他语言
- **预计规模**: 1个教程，4.2GB，300个文件

#### 💼 职业技能
- **包含内容**: Office办公、职场技能、财务会计等
- **子分类**: 办公软件、职场技能、财务会计、市场营销、项目管理
- **预计规模**: 1个教程，3.5GB，200个文件

#### 📚 学科教育
- **包含内容**: 数学、物理、化学等学科基础教育
- **子分类**: 数学、物理、化学、生物、文史地理
- **预计规模**: 1个教程，7.8GB，520个文件

#### 🏠 生活技能
- **包含内容**: 烹饪、健身、美容等生活技能
- **子分类**: 烹饪美食、健身运动、美容化妆、手工制作、生活百科
- **预计规模**: 2个教程，5.9GB，330个文件

#### 📦 其他教程
- **包含内容**: 暂时无法归类的教程内容
- **子分类**: 未分类教程
- **预计规模**: 1个教程，5.5GB，400个文件

### 分类规则

#### 关键词匹配
- **音乐艺术**: 钢琴、piano、音乐、music、乐理、吉他、guitar等
- **编程技术**: python、java、javascript、coding、编程、代码、web等
- **设计创意**: photoshop、ps、ai、design、设计、美工、ui、ux等
- **语言学习**: english、英语、日语、韩语、french、german等
- **职业技能**: office、excel、word、ppt、办公、职场、管理等
- **学科教育**: 数学、math、物理、physics、化学、生物等
- **生活技能**: 烹饪、cooking、健身、fitness、瑜伽、化妆等

#### 特殊处理
- **高维学堂**: 保持原有结构不变
- **未匹配内容**: 归入"其他教程"分类

### 重构优势

#### 🎯 查找效率
- 按学习领域分类，快速定位所需教程
- 减少目录层级，提升访问效率
- 预计查找速度提升50%

#### 📁 结构清晰
- 层级合理，逻辑清晰，易于理解
- 使用emoji图标，目录更直观
- 统一的命名规范

#### 🔧 维护便利
- 新教程易于归类，管理更简单
- 支持新增分类，适应未来需求
- 便于批量操作和管理

### 重构工具

#### tutorial_reorganizer.py
- **功能**: 教程目录自动重构工具
- **特点**:
  - 智能分类识别
  - 支持模拟运行
  - 自动备份结构
  - 详细操作日志
- **使用方法**: `python3 tutorial_reorganizer.py`

#### tutorial_reorganizer_demo.py
- **功能**: 重构方案演示工具
- **特点**:
  - 模拟重构过程
  - 生成详细计划
  - 展示预期效果
  - 无实际文件操作
- **使用方法**: `python3 tutorial_reorganizer_demo.py`

### 实施步骤

1. **备份现有教程目录**
2. **运行重构工具进行模拟**
3. **检查分类结果是否合理**
4. **调整分类规则（如需要）**
5. **执行正式重构操作**
6. **验证重构结果**
7. **更新相关文档和索引**

### 注意事项

- ⚠️ 重构前务必备份重要数据
- ⚠️ 首次使用建议先模拟运行
- ⚠️ 大文件移动需要较长时间
- ⚠️ 高维学堂目录保持不变
- ⚠️ 可根据实际需要调整分类规则

## 钢琴教程专用重构系统

### 专业化重构目标
针对钢琴学习内容进行专业化细分，删除所有非钢琴教程，保留高维学堂，创建专门的钢琴学习目录体系。

### 重要更新 (2025-07-23)
**保留音乐教程策略调整**：
- ✅ 保留 "音乐奥秘解码——轻松学乐理" → 归入 🎓 乐理基础
- ✅ 保留 "方百里 哈农" → 归入 🎵 哈农练指法  
- ✅ 保留 "鲍释贤" 教程并智能拆分：
  - 巴赫相关内容 → 🎪 巴赫作品
  - 拜厄相关内容 → 📚 拜厄教程
  - 车尔尼相关内容 → 🎼 车尔尼系列
  - 其他内容 → 📦 其他教材
- 新增 🎓 乐理基础 分类，专门收纳音乐理论相关教程
- 智能拆分功能：对包含多种教材的综合教程进行自动拆分归类

### 钢琴教程细分分类

#### 🎹 小汤系列
- **教材体系**: 汤普森简易钢琴教程
- **适用对象**: 钢琴启蒙和初学者
- **包含内容**: 循序渐进的基础教程，图文并茂
- **关键词**: 小汤、汤普森、thompson、小汤姆森
- **学习特点**: 启蒙经典，趣味性强

#### 🎼 车尔尼系列
- **教材体系**: 车尔尼钢琴练习曲
- **适用对象**: 需要技巧训练的学习者
- **包含内容**: 599、849、299、740等经典练习曲
- **关键词**: 车尔尼、599、849、299、740、czerny
- **学习特点**: 手指独立性训练，技巧提升

#### 📚 拜厄教程
- **教材体系**: 拜厄钢琴基本教程
- **适用对象**: 传统基础教学路线学习者
- **包含内容**: 基础指法、音符认识、基本练习
- **关键词**: 拜厄、beyer、基础、入门、初学
- **学习特点**: 传统经典，基础扎实

#### 🎵 哈农练指法
- **教材体系**: 哈农钢琴练指法
- **适用对象**: 需要基本功训练的学习者
- **包含内容**: 手指独立性练习，基本功强化
- **关键词**: 哈农、hanon、指法、手指、练指、基本功、方百里
- **学习特点**: 专门的手指技巧训练

#### 👨‍🏫 布格缪勒作品
- **教材体系**: 布格缪勒钢琴练习曲
- **适用对象**: 进阶阶段学习者
- **包含内容**: 25首简易进阶练习曲、18首性格练习曲
- **关键词**: 布格缪勒、布格穆勒、burgmuller、25首、18首
- **学习特点**: 音乐性与技巧性并重

#### 🎪 巴赫作品
- **教材体系**: 巴赫钢琴作品集
- **适用对象**: 古典音乐学习者
- **包含内容**: 创意曲、小前奏曲、平均律等
- **关键词**: 巴赫、bach、创意曲、小前奏曲、平均律
- **学习特点**: 复调训练，古典风格

#### 🎨 流行曲目
- **教材体系**: 现代流行钢琴
- **适用对象**: 喜欢现代音乐的学习者
- **包含内容**: 流行歌曲、爵士、动漫影视音乐
- **关键词**: 流行、现代、爵士、pop、jazz、动漫、影视
- **学习特点**: 现代风格，兴趣导向

#### 🎓 乐理基础
- **教材体系**: 音乐理论和乐理基础
- **适用对象**: 需要理论基础的学习者
- **包含内容**: 音乐理论、乐理知识、基础音乐知识
- **关键词**: 乐理、音乐奥秘、理论、基础知识、音乐理论
- **学习特点**: 理论基础，知识体系化

#### 📦 其他教材
- **教材体系**: 补充性钢琴教材
- **适用对象**: 综合性学习需求
- **包含内容**: 其他钢琴教材和练习内容
- **关键词**: piano、钢琴、教程、教材、练习
- **学习特点**: 补充和特殊内容

### 删除策略

#### 删除范围
- ❌ **非钢琴音乐教程**: 吉他、小提琴、声乐等其他乐器
- ❌ **通用乐理教程**: 非钢琴专用的乐理知识
- ❌ **编程技术教程**: Python、Web开发等技术内容
- ❌ **设计创意教程**: Photoshop、UI设计等设计内容
- ❌ **语言学习教程**: 英语、日语等语言学习
- ❌ **职业技能教程**: Office办公、职场技能等
- ❌ **学科教育教程**: 数学、物理等学科内容
- ❌ **生活技能教程**: 烹饪、健身等生活技能
- ❌ **其他非相关教程**: AI、杂项等无关内容

#### 保留策略
- ✅ **高维学堂**: 完全保持原有结构不变
- ✅ **钢琴专用教程**: 所有明确标注钢琴的教程
- ✅ **钢琴相关内容**: 包含piano关键词的教程

### 重构效果预期

#### 📊 数据统计
- **保留钢琴教程**: 4个 (25.6GB)
- **删除非钢琴教程**: 4个 (6.2GB)
- **新增分类目录**: 3个专业分类
- **释放存储空间**: 6.2GB

#### 🎯 专业化优势
- **专业聚焦**: 专门针对钢琴学习，内容更加专业
- **细分清晰**: 按学习阶段和内容类型细分
- **学习效率**: 从入门到进阶的完整学习路径
- **空间优化**: 删除无关内容，释放存储空间
- **查找精准**: 快速定位所需的钢琴学习资源

### 钢琴重构工具

#### piano_tutorial_reorganizer.py
- **功能**: 钢琴教程专用重构工具
- **特点**:
  - 专门针对钢琴教程的智能分类
  - 自动识别并删除非钢琴内容
  - 保护高维学堂目录不变
  - 支持模拟运行和实际执行
- **使用方法**: 
  - 模拟运行: `python3 piano_tutorial_reorganizer.py`
  - 实际执行: `python3 piano_tutorial_reorganizer.py --execute`

#### piano_tutorial_demo.py
- **功能**: 钢琴重构方案演示工具
- **特点**:
  - 详细展示分类方案
  - 显示删除计划和释放空间
  - 生成完整的重构计划文件
  - 无实际文件操作，安全演示
- **使用方法**: `python3 piano_tutorial_demo.py`

### 实施步骤

1. **📋 查看演示方案**
   ```bash
   python3 piano_tutorial_demo.py
   ```

2. **🔍 模拟重构过程**
   ```bash
   python3 piano_tutorial_reorganizer.py
   ```

3. **✅ 确认重构计划**
   - 检查分类结果是否合理
   - 确认删除列表无误
   - 验证高维学堂保持不变

4. **🚀 执行实际重构**
   ```bash
   python3 piano_tutorial_reorganizer.py --execute
   ```

5. **🔍 验证重构结果**
   - 检查新目录结构
   - 确认文件移动正确
   - 验证删除操作完成

### 安全保障

#### 🛡️ 数据保护
- **自动备份**: 重构前自动创建结构备份
- **模拟运行**: 支持无风险的模拟预览
- **操作日志**: 详细记录所有操作过程
- **确认机制**: 实际执行需要明确确认

#### ⚠️ 重要提醒
- **不可逆操作**: 删除操作无法撤销，请谨慎确认
- **备份建议**: 重构前务必备份重要数据
- **高维学堂**: 该目录完全不受影响
- **分类调整**: 可根据实际需要调整分类规则

继续## 标准化影片目录处理流程

### 动画目录清理（已完成）

**清理工具**：
- `smart_animation_cleaner.py` - 智能文件夹名称清理
- `handle_duplicates.py` - 重复文件夹处理
- `clean_video_files.py` - 视频文件名清理

**清理成果**：
- ✅ 技术参数清理：完全移除BluRay、x264、x265、H264、H265、DTS、AAC、1080p等技术标识
- ✅ 发布组标识清理：移除FRDS、FLUX、PTHome、PTHOME、PTHweb、DYGC、mUHD、MNHD等
- ✅ 重复文件夹处理：清理哈利波特系列重复文件夹，保留最大版本
- ✅ IMDB评分标准化：统一格式为[IMDB: X.X]或[无评分]
- ✅ 文件夹名称简化：保留核心信息，移除冗余技术参数

**统计数据**：
- 处理文件夹：40个
- 处理视频文件：9个
- 删除重复文件夹：2个
- 错误数：0个

### 电视目录清理（已完成）

**清理工具**：
- `smart_tv_cleaner.py` - 智能电视剧文件夹名称清理
- `clean_tv_files.py` - 电视视频文件名清理
- `tv_auto_cleanup.py` - 自动化整理和中文改名
- `fix_tv_duplicates.py` - 修复重复季数标识
- `final_tv_cleanup.py` - 清理发布组标识和技术参数

**清理成果**：
- ✅ 技术参数清理：完全移除BluRay、x264、x265、H264、H265、DTS、AAC、1080p、2160p、HDTV等技术标识
- ✅ 发布组标识清理：移除DBTV、PTH、FLUX、TOMMY、ROCCaT、HHWEB、CHDWEB等发布组标识
- ✅ 季数标准化：统一格式为"Season X"（如S01 -> Season 1）
- ✅ 流媒体平台标识清理：移除Netflix、NF、ATVP等平台标识
- ✅ 中文字幕标识清理：移除"国粤双语中字"等标识
- ✅ 中文名称添加：为缺少中文名称的文件夹自动添加中文标识（如Clarksons.Farm -> 克拉克森的农场.Clarksons.Farm）
- ✅ 元数据文件清理：自动删除.nfo、-thumb.jpg、.DS_Store等元数据文件
- ✅ IMDB评分标准化：统一格式为[IMDB: X.X]或[无评分]
- ✅ 过小文件夹清理：自动删除空文件夹或过小的无用内容

**最终统计数据**：
- 📁 文件夹总数：76个
- 📄 散落文件：0个
- 🎯 标准化率：100%（76/76个文件夹完全符合标准）
- 🏆 完美达标：所有文件夹均符合"中文名.英文名 [评分]"格式
- 处理视频文件：5个
- 中文改名：1个
- 元数据清理：13个文件
- 季数格式修复：4个
- 评分信息添加：7个
- 过小文件夹删除：2个
- 总重命名次数：89次
- 错误数：0个

基于动画目录整理的实践经验，制定以下标准化流程用于影片目录的系统性整理和清理：

### 📋 处理流程概览

**阶段一：目录分析** → **阶段二：文件重命名** → **阶段三：内容分类** → **阶段四：质量清理**

### 🔍 阶段一：目录分析

**1.1 基础统计**
```bash
# 统计文件夹数量
find "/目标路径" -maxdepth 1 -type d | wc -l

# 查看总容量
du -sh "/目标路径"

# 列出所有文件夹
find "/目标路径" -maxdepth 1 -type d -name "*" | sort
```

**1.2 问题识别**
- 检查命名不规范的文件夹（缺少中文标识）
- 识别重复或相似内容
- 发现异常大小的文件夹
- 统计各类型内容分布

### 🏷️ 阶段二：文件重命名

**2.1 命名标准**
- 格式：`中文名.英文名.技术参数`
- 示例：`哈利波特.Harry.Potter.WEB-DL.1080p.H265.AAC-PTHweb`

**2.2 批量重命名**
```bash
# 重命名示例
mv "原文件夹名" "新文件夹名"
```

**2.3 验证检查**
```bash
# 检查是否还有未重命名的文件夹
find "/目标路径" -maxdepth 1 -type d -name "*" | grep -v "中文" | wc -l
```

### 📁 阶段三：内容分类

**3.1 分类维度**
- **按内容类型**：电影动画、电视动画、儿童动画、特殊类型
- **按制作地区**：日本动画、美国动画、中国动画、其他地区
- **按目标受众**：儿童向、青少年向、成人向、全年龄
- **按系列归档**：同系列作品集中管理

**3.2 分类建议**
- 优先按内容类型进行一级分类
- 根据收藏规模决定是否进行二级分类
- 保持分类层级简洁，避免过度细分

### 🗑️ 阶段四：质量清理

**4.1 评估标准**
- **优先删除**：非正式内容、作业文件、评价极差作品
- **考虑删除**：小众作品、过时内容、重复版本
- **必须保留**：经典作品、高评分内容、稀有资源

**4.2 删除原则**
1. 先删除明显的垃圾内容
2. 评估空间释放效益
3. 考虑家庭成员观看偏好
4. 保留具有收藏价值的作品

**4.3 执行删除**
```bash
# 批量删除示例
rm -rf "文件夹1" "文件夹2" "文件夹3"
```

### 📊 处理效果记录

**统计指标：**
- 处理前后文件夹数量对比
- 释放的存储空间大小
- 保留内容的质量提升
- 管理效率的改善程度

**文档更新：**
- 记录删除的具体文件列表
- 更新当前库存状态
- 总结处理经验和教训

### 🔄 后续维护

- 定期重复此流程（建议3-6个月一次）
- 根据新增内容调整分类策略
- 持续优化命名规范
- 建立内容质量评估机制

---

### 视频工具特殊说明

**依赖要求：**
- 需要安装 `ffmpeg` 用于视频信息分析
- 可选安装 `mediainfo` 作为备选工具
- 安装命令：`brew install ffmpeg mediainfo`

**文件权限：**
- 确保脚本有执行权限：`chmod +x video_organizer*.sh`
- 确保SMB挂载点可访问：`/Volumes/video`

**支持格式：**
- 高质量：MKV, MP4, M4V, WEBM
- 常用格式：AVI, MOV, WMV, FLV
- 流媒体：TS, M2TS, 3GP
- 传统格式：RM, RMVB, MPG, MPEG

**当前视频库状态（11TB）：**
- 电影：4.3TB (5,616文件) - 最大分类
- 电视：2.7TB (8,460文件) - 文件数最多
- 动画：1.3TB (3,862文件)
- 演出：1.5TB
- 记录片：363GB (540文件)
- 教程：739GB (5,540文件) - 需要整理
- 会议：1.4GB (18文件)
- 回收站：5.2MB (130文件) - 可清理

**整理策略：**
- 按类型分类：电影/电视/动画/纪录片
- 按地区细分：国产/欧美/日韩/其他
- 按质量分级：4K/1080p/720p/其他
- 按年代归档：2020s/2010s/2000s等

**动画文件分类建议：**

基于当前1.3TB动画库（49个文件夹）的分析，建议按以下方式重新组织：

1. **按内容类型分类**
   ```
   动画/
   ├── 01-电影动画/          # 单部动画电影
   │   ├── 宫崎骏系列/       # 吉卜力工作室作品
   │   ├── 迪士尼动画/       # 迪士尼、皮克斯作品
   │   ├── 国产动画电影/     # 大鱼海棠、哪吒等
   │   └── 其他动画电影/
   ├── 02-电视动画/          # 连续剧动画
   │   ├── 日本动画/         # 海贼王、新世纪福音战士等
   │   ├── 欧美动画/         # 瑞克和莫蒂、小马宝莉等
   │   └── 国产动画/         # 国产电视动画
   ├── 03-儿童动画/          # 专门的儿童内容
   │   ├── 学前教育/         # 巧虎等教育类
   │   ├── 卡通系列/         # 汪汪队、熊出没等
   │   └── 经典动画/         # 猫和老鼠、米老鼠等
   └── 04-特殊类型/
       ├── 音乐动画/         # 音乐相关动画
       ├── 实验动画/         # 艺术性动画
       └── 合集系列/         # 多部作品合集
   ```

2. **按制作地区细分**
   - **日本动画**: 宫崎骏作品、吉卜力动画、TV动画系列
   - **欧美动画**: 迪士尼、皮克斯、梦工厂、独立制作
   - **国产动画**: 大鱼海棠、哪吒、熊出没系列
   - **其他地区**: 韩国、法国等其他国家作品

3. **按目标受众分类**
   - **全年龄**: 宫崎骏、迪士尼经典
   - **青少年**: 热血动画、冒险类
   - **成人向**: 深度剧情、艺术动画
   - **儿童专用**: 教育动画、卡通系列

4. **按系列归档**
   - **长篇系列**: 海贼王、瑞克和莫蒂（按季分组）
   - **电影系列**: 哈利波特、怪诞小镇（保持合集）
   - **制作公司**: 吉卜力、迪士尼（按工作室分组）
   - **主题系列**: 超级英雄、科幻、奇幻

**当前需要重新分类的文件夹示例：**
- `吉卜力动画合集` → `01-电影动画/宫崎骏系列/`
- `哈利波特全集` → `01-电影动画/奇幻系列/`
- `海贼王` → `02-电视动画/日本动画/长篇系列/`
- `熊出没系列` → `03-儿童动画/卡通系列/`
- `瑞克和莫蒂` → `02-电视动画/欧美动画/`

**分类优势：**
- 便于按年龄段筛选内容
- 方便按制作风格查找
- 提高媒体库管理效率
- 支持家庭成员个性化浏览

**动画库清理建议：**

基于内容质量、观看价值和存储空间考虑，以下动画建议删除：

🗑️ **优先删除（低价值/质量较差）：**
1. **音乐作业** (66M) - 非正式动画内容，可能是作业文件
2. **小蜘蛛卢卡斯（中英字幕）** (237M) - 小众作品，观看价值有限
3. **巧虎 2020年11月 快乐版 不一样的尾巴** (2.2G) - 单集幼教内容，价值有限
4. **匹诺曹.Pinocchio.2019** (5.7G) - 2019年版本评价较差，非经典版本

⚠️ **考虑删除（根据个人喜好）：**
1. **欧布奥特曼-普通话版** (18G) - 特摄片非传统动画，占用空间大
2. **西游记美猴王传奇.1999** - 较老的国产动画，画质一般
3. **乔瓦尼的岛屿.2014** - 小众日本动画，观看群体有限
4. **云之彼端约定的地方.2004** - 新海诚早期作品，不如后期经典

✅ **建议保留（经典/高价值）：**
- 吉卜力动画合集 - 宫崎骏经典作品
- 哈利波特系列 - 经典奇幻动画
- 海贼王系列 - 长篇经典动画
- 瑞克和莫蒂 - 高质量成人动画
- 新世纪福音战士 - 动画史经典
- 猫和老鼠经典全集 - 永恒经典
- 驯龙高手3 - 高质量3D动画
- 魅力四射(Encanto) - 迪士尼新作

**✅ 已完成删除（已释放约200GB）：**
- ✓ 音乐作业 (66M) - 非正式动画内容
- ✓ 小蜘蛛卢卡斯 (237M) - 小众作品
- ✓ 巧虎单集 (2.2G) - 单集幼教内容
- ✓ 匹诺曹2019版 (5.7G) - 评价较差的重制版本
- ✓ 欧布奥特曼 (18G) - 特摄片非传统动画
- ✓ 西游记美猴王传奇 - 较老国产动画
- ✓ 乔瓦尼的岛屿 - 小众日本动画
- ✓ 云之彼端约定的地方 - 新海诚早期作品

**当前动画库状态：**
- 文件夹数量：从50个减少到42个
- 总容量：从1.3TB减少到1.1TB
- 释放空间：约200GB
- 清理完成时间：2025年1月23日

## 动画库IMDB评分添加和文件名清理

### 操作概述
使用Python脚本批量为动画文件夹添加IMDB评分并清理技术参数信息。

### 处理结果
- **重命名文件夹**: 41个
- **跳过文件夹**: 6个
- **错误文件夹**: 0个
- **总计文件夹**: 47个
- **成功率**: 87.2%

### 主要改进
1. **添加IMDB评分**
   - 瑞克和莫蒂 [9.3]
   - 海贼王 [9.0]
   - 怪诞小镇 [8.9]
   - 猫和老鼠经典全集 [8.6]
   - 吉卜力动画合集 [8.5]
   - 新世纪福音战士 [8.5]
   - 驯龙高手3 [8.1]
   - 哈利波特系列 [7.6]
   - 魅力四射(Encanto) [7.2]
   - 哥斯拉大战金刚 [6.3]

2. **清理技术参数**
   - 移除编码信息：BluRay.x264.DTS-WiKi
   - 移除分辨率标识：1080p, 720p
   - 移除音频格式：DTS-HD, AC3, AAC
   - 移除发布组标识：[组名]
   - 标准化空格和格式

### 脚本功能
- **IMDB评分数据库**: 包含50+经典动画作品评分
- **智能匹配**: 支持中英文名称匹配
- **技术参数清理**: 15+种常见编码格式识别
- **预览模式**: 执行前可预览更改
- **安全操作**: 检查重名冲突，提供详细日志

### 操作时间
2025年1月27日完成IMDB评分添加和文件名清理

**清理效果：**
- ✅ 释放了约200GB存储空间
- ✅ 减少了8个文件夹，提升管理效率
- ✅ 保留了高质量经典作品
- ✅ 优化了动画库的整体质量

**大文件处理：**
- 识别>5GB的大文件
- 建议压缩或转码节省空间
- 考虑使用H.265编码

**重复文件检测：**
- 基于文件大小初步筛选
- 可选内容哈希验证（较慢）
- 智能保留高质量版本

**安全建议：**
- **强烈建议**首次使用 `DRY_RUN="true"`
- 11TB数据量巨大，操作前务必备份
- 分批处理，避免一次性处理所有文件
- 定期清理回收站释放空间

**性能优化：**
- 大型视频库处理时间较长（可能数小时）
- 建议夜间或空闲时运行
- 网络存储注意带宽限制
- 启用缓存避免重复扫描

**网络连接：**
- 确保SMB连接稳定
- 设置合理的超时时间
- 网络中断时自动重试

4. **无法删除文件**
   - 检查文件权限
   - 确认文件未被占用

5. **SSH 连接状态**
   
   ✅ **当前状态**: SSH 连接成功
   - **连接方式**: 使用 sshpass 自动输入密码
   - **成功命令**: `sshpass -p 'zmkm9282jsLW' ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -o PasswordAuthentication=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null 644378664@192.168.3.50 -p 30220`
   - **登录位置**: `/var/services/homes/644378664`
   - **注意事项**: 密码已从配置文件 `nas_connection.conf` 中获取

## 防止SSH命令卡顿的优化方案

**问题**: SSH命令经常因为输出过多或网络延迟而卡住无响应

**解决方案**:

### 1. 使用超时控制
```bash
# 为命令添加超时限制
timeout 30s ls -la /volume1/
```

### 2. 限制输出长度
```bash
# 使用 head 限制输出行数
ls -la /volume1/ | head -20

# 使用 grep 过滤特定内容
ls -la /volume1/ | grep -E '^d' | head -10  # 只显示目录
```

### 3. 分页查看大量输出
```bash
# 使用 less 分页查看（在SSH中设置PAGER=cat避免交互）
PAGER=cat ls -la /volume1/ | head -50
```

### 4. 优化的目录查看命令
```bash
# 快速查看主要目录结构
find /volume1/ -maxdepth 2 -type d | head -20

# 查看目录大小（限制输出）
du -sh /volume1/*/ 2>/dev/null | head -10
```

### 5. 后台执行长时间命令
```bash
# 将长时间命令放到后台执行
nohup find /volume1/ -name "*.log" > /tmp/logfiles.txt 2>&1 &

# 检查后台任务状态
jobs
ps aux | grep find
```

### 6. 使用SSH连接保持
```bash
# 添加连接保持参数防止超时断开
sshpass -p 'zmkm9282jsLW' ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o PreferredAuthentications=password -o PubkeyAuthentication=no -o PasswordAuthentication=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null 644378664@192.168.3.50 -p 30220
```
   
   **如果遇到 SSH 连接问题，请检查：**
   - 运行 `./test_nas_connection.sh` 进行诊断
   - 检查 NAS SSH 服务是否启用：
     * 登录 NAS 管理界面
     * 进入 控制面板 > 终端机和 SNMP
     * 确保 "启用 SSH 服务" 已勾选
     * 检查 SSH 端口设置
   - 验证用户权限：
     * 确保用户存在且有 SSH 登录权限
     * 检查用户名和密码是否正确
   - 网络连通性：
     * 确保 NAS 和本机在同一网络
     * 检查防火墙设置
   
   **诊断结果分析（2025-07-22）：**
- ✅ 网络连通性正常（ping 和端口 30220 可达）
- ✅ DSM 登录正常（用户 644378664 可以成功登录管理界面）
- ✅ 端口 30220 和 22 都可以建立TCP连接
- ❌ SSH 连接失败：`Connection closed by 192.168.3.50 port 30220`

**详细测试结果：**
```bash
# 端口连通性测试 - 成功
nc -zv 192.168.3.50 30220
# Connection to 192.168.3.50 port 30220 [tcp/*] succeeded!

# SSH连接测试 - 失败
sshpass -p "zmkm9282jsLW" ssh -p 30220 644378664@192.168.3.50
# Connection closed by 192.168.3.50 port 30220
```

**问题分析：**
端口开放但SSH连接被立即关闭，根据NAS SSH配置截图分析：

**发现的配置问题：**
- ✅ SSH功能已启用，端口30220正确
- ⚠️ 安全级别设置为"低"
- ⚠️ 启用了"自定义加密模式"，可能导致兼容性问题
- ⚠️ 加密算法配置可能与SSH客户端不兼容

**最终诊断（2025-01-27）：**

通过详细调试模式（`-vvv`）确认，SSH连接失败的根本原因在于 **NAS的SSH服务与客户端的OpenSSH版本（macOS Sonoma自带的 OpenSSH 9.9）不兼容**。

**核心证据：**
调试日志显示，在客户端发送其版本字符串 `SSH-2.0-OpenSSH_9.9` 后，服务器立即关闭连接（`kex_exchange_identification: Connection closed by remote host`），整个过程甚至未进入加密算法协商阶段。这表明NAS的SSH守护进程检测到`OpenSSH 9.9`后便主动断开连接。

**结论：**
任何在客户端调整加密算法、密钥交换算法或MACs的尝试都无法解决此问题。问题根源在服务器端。

**解决方案：**
1.  **（推荐）使用第三方SSH客户端：** 在iMac上安装并使用其他SSH客户端，如 `Termius`, `iTerm2` (配合旧版ssh) 或 `SecureCRT`，它们可能使用不同的SSH库或版本，从而绕过此问题。
2.  **更新NAS固件/SSH服务：** 检查NAS是否有系统更新，特别是安全更新，其中可能包含新版的SSH服务。
3.  **（不推荐）降级macOS的OpenSSH：** 这是一个复杂且可能影响系统安全性的操作，不推荐普通用户尝试。

## 在 NAS 上运行脚本的标准流程

由于 NAS 的 DSM 操作系统默认不支持在文件管理器中通过右键菜单直接打开终端，您需要通过以下标准步骤来执行脚本：

1.  **打开终端应用：**
    *   在 NAS 的桌面环境中，点击左上角的主菜单。
    *   找到并打开“终端机”或 “Terminal” 应用。

2.  **切换到脚本所在目录：**
    *   打开终端后，使用 `cd` 命令进入脚本所在的目录。脚本通常位于 `SynologyDrive` 文件夹内。例如，要进入本项目的 `nas` 目录，请复制并粘贴以下命令：
      ```bash
      cd /volume1/homes/644378664/SynologyDrive/0050Project/Tool.System/nas/
      ```

3.  **授予脚本执行权限（如果需要）：**
    *   首次运行脚本或新创建的脚本可能没有执行权限。使用 `chmod +x` 命令来添加权限。例如，为 `nas_cleanup.sh` 添加权限：
      ```bash
      chmod +x nas_cleanup.sh
      ```

4.  **运行脚本：**
    *   使用 `./` 加上脚本名称来执行。例如：
      ```bash
      ./nas_cleanup.sh
      ```

## 警告：关于使用 Telnet 的说明

**强烈不推荐使用 Telnet！**

Telnet 是一个过时且极不安全的协议，因为它以**明文（未加密）**形式传输所有通信内容，包括您的用户名和密码。这意味着任何能够监听您网络流量的人都可以轻易窃取您的登录凭据，从而完全控制您的 NAS。

仅在 SSH 完全无法使用且您完全了解并接受相关风险的紧急情况下，才应临时启用 Telnet。完成操作后，请**务必立即从 NAS 的控制面板中禁用 Telnet 服务**。

**临时连接命令：**
```bash
telnet 192.168.3.50
```

**可能的原因：**
- SSH 服务的自定义加密设置与客户端不兼容
- 安全级别"低"可能启用了某些限制性配置
- SSH 服务配置了严格的访问控制（IP白名单、用户限制等）
- 用户账户可能没有SSH登录权限（即使有DSM登录权限）
- 可能启用了 fail2ban 等安全工具阻止连接
- **关键发现：SSH版本兼容性问题**

**最新诊断结果（2025-01-22）：**
- 使用正确密码（zmkm9282jsLW）和用户名（644378664）
- 连接在密钥交换阶段被远程主机关闭
- 调试信息显示：`Local version string SSH-2.0-OpenSSH_9.9`
- NAS SSH服务在看到OpenSSH 9.9版本后立即断开连接
- **根本原因：NAS SSH服务与macOS OpenSSH 9.9版本不兼容**

**建议解决方案：**
1. ⭐ **重点：禁用"自定义加密模式"，使用默认加密设置** - 这很可能是问题的根源
2. ~~尝试将安全级别从"低"改为"中"或"高"~~ - 已测试过中、低级别都不行
3. **考虑降级SSH客户端版本或使用第三方SSH客户端**
4. **在NAS上更新SSH服务到支持新版本OpenSSH的版本**
5. 检查用户权限设置，确保用户有SSH访问权限
6. 如果仍然不行，尝试完全重置SSH配置到默认状态

**重要提示：**
自定义加密模式通常会限制SSH客户端的兼容性，建议优先禁用此选项。SSH版本兼容性问题是导致连接失败的主要原因。
   
   - 在 NAS 上查看 SSH 连接日志：
     * 登录 NAS 管理界面
     * 进入 日志中心 > 系统
     * 查看 SSH 相关的错误日志
     * 或者通过 SSH 连接成功后查看：
       ```bash
       # 查看 SSH 服务日志
       sudo tail -f /var/log/messages | grep ssh
       
       # 查看认证日志
       sudo tail -f /var/log/auth.log
       
       # 查看系统日志中的 SSH 相关信息
       sudo journalctl -u ssh -f
       ```
   - 常见连接被拒绝的原因：
     * SSH 服务未启动或配置错误
     * 用户名或密码错误
     * 用户没有 SSH 登录权限
     * 防火墙阻止了 SSH 端口
     * SSH 配置文件中禁用了密码认证
     * 达到了最大连接数限制
     * SSH 服务配置了访问限制（IP 白名单等）

### 性能优化

- 定期运行清理（建议每周一次）
- 先清理临时文件，再处理大文件
- 使用快速清理工具进行日常维护
- 使用高级工具进行深度清理

## 📝 使用技巧

1. **定期维护**：建议每周运行一次快速清理
2. **分类清理**：先清理安全的临时文件，再处理其他类型
3. **备份重要文件**：清理前备份重要数据
4. **监控空间**：定期查看磁盘使用情况
5. **渐进式清理**：不要一次性删除太多文件

## 🆘 支持

如果遇到问题或需要帮助：
1. 检查本 README 的故障排除部分
2. 查看脚本生成的日志文件
3. 确认 NAS 路径和权限设置

---

**⚠️ 重要提醒**
- 清理前请备份重要文件
- 建议先在测试目录试用
- 删除操作不可恢复，请谨慎操作
- 定期检查清理结果，确保没有误删重要文件

**🎉 开始清理您的 NAS 存储空间吧！**

## 🎬 电影目录批量重命名统计

### 重命名目标
将英文电影目录重命名为"中文名 英文名 (年份)"格式，提升中文用户的浏览体验。

### 第一轮重命名（2025-01-24 上午）
- **成功处理**: 87个目录
- **跳过处理**: 27个目录（已存在相同中文名或特殊情况）
- **剩余待处理**: 118个英文目录

### 第二轮重命名（2025-01-24 下午）
- **成功重命名**: 97个目录
- **跳过处理**: 72个目录（目标已存在和技术规格目录）
- **处理失败**: 0个目录
- **总计处理**: 169个目录

### 最终统计结果
- **总目录数量**: 596个
- **中文开头目录**: 481个（80.7%）
- **剩余英文目录**: 95个（15.9%）
- **其他目录**: 20个（3.4%）

### 重命名效果示例
```
原名: Inception (2010)
新名: 盗梦空间 Inception (2010)

原名: Interstellar (2014)
新名: 星际穿越 Interstellar (2014)

原名: The Wolf of Wall Street (2013)
新名: 华尔街之狼 The Wolf of Wall Street (2013)
```

### 剩余英文目录说明
剩余的95个英文目录主要包含：
- **技术规格目录**: HEVC编码、MPEG-4等技术参数目录
- **团队标识目录**: CMCT团队等制作组标识
- **特殊格式目录**: 少量无法匹配中文译名的特殊格式电影
- **重复版本**: 同一电影的不同版本或格式

### 使用的重命名脚本
- `batch_rename_all_movies.sh`: 第一轮重命名脚本
- `batch_rename_chinese_first.sh`: 第二轮优化重命名脚本

**备注**: 重命名过程中保留了所有原始文件，仅修改目录名称，确保数据安全。