# RustDesk 部署状态

## 部署信息
- **服务器**: op.gaowei.com
- **部署时间**: 2024年6月15日
- **部署状态**: ✅ 成功
- **使用脚本**: quick_deploy.sh

## 服务状态
所有端口正常监听：
- 21115 (TCP) - hbbs 信令服务器 ✅
- 21116 (TCP/UDP) - hbbs NAT类型测试 ✅
- 21117 (TCP) - hbbr 中继服务器 ✅
- 21119 (TCP) - hbbr 中继服务器 ✅

## 客户端配置
- **ID服务器**: op.gaowei.com:21115
- **中继服务器**: op.gaowei.com:21117
- **公钥**: LtfD+68UsylW2fOqeW6bf4UyeCR14GgmE76U+xmfl0w=

## 验证结果
- SSH连接: ✅ 正常
- 端口连通性: ✅ 21115、21117端口测试通过
- Docker容器: ✅ 运行正常

## 管理命令
```bash
# 连接服务器
ssh root@op.gaowei.com

# 查看服务状态
netstat -tlnp | grep -E ':(21115|21116|21117|21119)'

# 查看Docker进程
ps aux | grep docker
```