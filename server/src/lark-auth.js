// 飞书认证中间件
require('dotenv').config();

class LarkAuth {
  constructor() {
    this.appId = process.env.LARK_APP_ID;
    this.appSecret = process.env.LARK_APP_SECRET;
  }

  // 验证飞书回调请求
  verifyCallback(body) {
    // 这里需要实现签名验证
    // 临时实现：仅检查必要参数
    if (!body.code || !body.state) {
      throw new Error('Invalid callback request');
    }
    return true;
  }
}

module.exports = LarkAuth;
