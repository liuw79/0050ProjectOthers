# 全局配置

## 沟通规则

**始终使用中文与用户沟通。**

## 项目启动流程

1. 输入缩写 → 切换到对应目录（无需询问）
2. 不自动读取 progress，由用户决定是否查看

## 原则

**宁缺毋滥。** 新增文件或目录要谨慎看看有没有已经存在的"马甲"，冗余文件立即删除，一个用途只留一个位置。

## progress.md 规则

> **每个项目都需要一个 progress.md 文件，没有的话要创建。**

此文件仅记录最新有效信息，包括当前会话的工作进度。如有版本迭代，只保留最新版本，删除旧版本的相关描述以避免上下文混乱。

**触发方式：** 用户说 "progress" 时，更新这个文件。

## 快捷命令

| 缩写 | 动作 | 说明 |
|------|------|------|
| `cf` | `open` 当前文件所在目录 | 打开刚生成文件的文件夹 |

## SSH 配置

**腾讯工蜂**：`git.code.tencent.com`

密钥位置：`Tool.System/ssh_keys/`
- `id_rsa_gw` - 私钥
- `id_rsa_gw.pub` - 公钥

SSH config 配置：
```
Host git.code.tencent.com
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    IdentityFile ~/.ssh/id_rsa_gw
```

**新电脑配置步骤**：详见 `Tool.System/ssh_keys/README.md`

## 可用 Skills

| 命令 | 说明 |
|------|------|
| `/tencent-ssh` | 添加 SSH Key 到腾讯工蜂 |
| `/meeting` | 会议记录解析与项目任务同步 |

## 项目缩写映射

### 高维 (GW) 系列
| 缩写 | 目录 | 说明 |
|------|------|------|
| `gkb` | GW.KnowledgeBase | 知识库 |
| `gc` / `con` / `CON` | GW.Content | 内容 |
| `da` / `data` / `DATA` | GW.DataAnalysis | 数据分析 |
| `db` | GW.Database | 数据库 |
| `gtm` | GW.GTM | GTM |
| `html` | GW.Html | HTML |
| `ig` | GW.InfoGraphic | 信息图 |
| `invest` | GW.Invest | 投资 |
| `jf` | GW.JingyingFenxi | 经营分析 |
| `lm` | GW.LearnMap | 学习地图 |
| `lp` | GW.LessonPromotion | 课程推广 |
| `lessons` | GW.Lessons | 课程 |
| `project` | GW.Project | 项目 |
| `rm` | GW.RoadMap | 路线图 |
| `sqlbot` | GW.Sqlbot | SQL机器人 |
| `trackr` | GW.Trackr | 追踪器 |
| `ui` | GW.UI | UI |
| `bw` | GW.BrandWatch | 品牌监测 |
| `web` / `www` / `website` | GW.Website | 网站项目 |
| `csv` | GW.Csv | CSV |
| `classroom` | GW.Classroom | 课堂 |
| `ascend` | GW.AscendPlan | 攀升计划 |
| `sm` / `share` / `SHARE` | GW.ShareMoney | 净利分配 |

### 刘伟 (LW) 系列
| 缩写 | 目录 | 说明 |
|------|------|------|
| `lkb` / `LKB` | /Users/comdir/SynologyDrive/LW.KnowledgeBase | 知识库（项目外路径） |
| `ltf` / `LTF` | LW.LiuTongfei | 刘同飞 |
| `yy` / `YY` | LW.Yy | Yy |
| `br` | LW.BloomReader | Bloom阅读器 |
| `ebook` | LW.eBook | 电子书 |
| `fy` | LW.FeiYang | 飞扬 |
| `reading` | LW.Reading | 阅读 |
| `wp` | LW.wePark | wePark |
| `wxwm` | LW.wxWaterMark | 微信水印 |

### 工具 (Tool) 系列
| 缩写 | 目录 | 说明 |
|------|------|------|
| `ts` / `sys` / `SYS` | Tool.System | 系统工具 |
| `tas` | Tool.Agent-S | Agent-S |
| `td` | Tool.Docs | 文档工具 |
| `ds` / `deepseek` | Tool.DeepSeek | DeepSeek导出 |
| `rpa` | others/Test.RPA | RPA自动化 |

### 其他
| 缩写 | 目录 | 说明 |
|------|------|------|
| `ai` / `agt` | AI.long-running-agents | AI长运行代理 |
| `bu` | browser-use | 浏览器使用 |
| `kt` | KK.Time | KK时间 |
| `yf` | YY.Fangcheng | 方程 |
| `oc` | OpenClaw | OpenClaw - 开源 AI Agent 平台 |

---

## OpenClaw 信息

**OpenClaw** 是一个开源的个人 AI 助手项目（GitHub 6万+ star），类似 Claude Code。

- **官网**: https://openclaw.ai
- **GitHub**: https://github.com/openclaw/openclaw
- **本地安装**: `npm install -g openclaw@latest`
- **启动**: `openclaw gateway --port 18789`
- **状态**: `openclaw status`
- **Dashboard**: http://127.0.0.1:18789/
- **配置文件**: `~/.openclaw/openclaw.json`
- **工作目录**: `~/openclaw` (源码)
- **扩展目录**: `~/.openclaw/extensions/`

**本地配置**:
- 当前版本: 2026.2.26
- Gateway: http://127.0.0.1:18789/
- 飞书已配置 (appId: cli_a913c55ee839dcd2)

---
*此配置对所有项目生效*
