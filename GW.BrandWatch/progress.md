# GW.BrandWatch 进展

## 项目简介
高维学堂学友企业品牌监控系统，监测媒体平台动态。

## 当前状态
Phase 1 完成，百度新闻已接入

## 已完成
- [x] RSS 源监控（36氪、虎嗅、钛媒体、界面、IT之家、爱范儿等 10 个）
- [x] 百度新闻搜索（Playwright 突破反爬）
- [x] 本地文件存储（data/目录，文件名：日期_媒体_标题.md）
- [x] 全局 SMTP 邮件工具（~/.config/mailer.py）
- [x] 定时任务（每天 9:00 执行，launchd）
- [x] 日报：有匹配时发送
- [x] 周报：周日发送本周汇总
- [x] 邮件末尾显示搜索信息源和品牌列表
- [x] 多收件人支持（liuwei@gaowei.com, zqj@gaowei.com）

## 待办
- [ ] 优化关键词匹配（"DR" 误匹配问题）
- [ ] 添加竞品关键词
- [ ] 全文匹配
- [ ] 飞书多维表对接
- [ ] 修复无效 RSS 源（创业邦、亿邦动力、澎湃、每经）

## 配置文件
- `config/monitor.yaml` - 品牌关键词、RSS源、开关配置
- `~/.config/smtp.yaml` - 邮件 SMTP 配置

## 使用
```bash
# 手动运行
cd /Users/liuwei/SynologyDrive/0050Project/GW.BrandWatch
python src/monitor.py

# 查看定时任务状态
launchctl list | grep brandwatch

# 手动触发
launchctl start com.gaowei.brandwatch
```

## 监控品牌
北方华创、名创优品/MINISO、霸王茶姬、小熊电器、电小二、DR钻戒、由莱/YOLAI、韶音/Shokz、盈富斯/INFOTHINK、倍思/Baseus、布童
