// 飞书API客户端 - 使用直接HTTP调用
require('dotenv').config();

const FEISHU_BASE_URL = 'https://open.feishu.cn/open-apis';

class LarkClient {
  constructor() {
    this.appAccessToken = null;
    this.tokenExpireTime = 0;
  }

  // 获取app access token
  async getAppAccessToken() {
    // 检查token是否过期
    if (this.appAccessToken && Date.now() < this.tokenExpireTime) {
      return this.appAccessToken;
    }

    try {
      const response = await fetch(`${FEISHU_BASE_URL}/auth/v3/app_access_token/internal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          app_id: process.env.LARK_APP_ID,
          app_secret: process.env.LARK_APP_SECRET,
        }),
      });

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`获取飞书token失败: ${data.msg}`);
      }

      this.appAccessToken = data.app_access_token;
      this.tokenExpireTime = Date.now() + (data.expire_in - 300) * 1000; // 提前5分钟过期
      return this.appAccessToken;
    } catch (error) {
      console.error('获取飞书token失败:', error);
      throw error;
    }
  }

  // 获取多维表格数据
  async getBitableData(appToken, tableId, options = {}) {
    try {
      const { page_size = 100, page_token = '' } = options;
      const token = await this.getAppAccessToken();
      const url = `${FEISHU_BASE_URL}/bitable/v1/apps/${appToken}/tables/${tableId}/records?page_size=${page_size}&page_token=${page_token}`;

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`获取多维表格数据失败: ${data.msg}`);
      }

      return data.data.items;
    } catch (error) {
      console.error('获取多维表格数据失败:', error);
      throw error;
    }
  }

  // 添加多维表格记录
  async addBitableRecord(appToken, tableId, fields) {
    try {
      const token = await this.getAppAccessToken();
      const url = `${FEISHU_BASE_URL}/bitable/v1/apps/${appToken}/tables/${tableId}/records`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fields }),
      });

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`添加多维表格记录失败: ${data.msg}`);
      }

      return data.data;
    } catch (error) {
      console.error('添加多维表格记录失败:', error);
      throw error;
    }
  }

  // 更新多维表格记录
  async updateBitableRecord(appToken, tableId, recordId, fields) {
    try {
      const token = await this.getAppAccessToken();
      const url = `${FEISHU_BASE_URL}/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`;

      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fields }),
      });

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`更新多维表格记录失败: ${data.msg}`);
      }

      return data.data;
    } catch (error) {
      console.error('更新多维表格记录失败:', error);
      throw error;
    }
  }

  // 查询多维表格记录
  async queryBitableRecords(appToken, tableId, filter = {}) {
    try {
      const token = await this.getAppAccessToken();
      const url = `${FEISHU_BASE_URL}/bitable/v1/apps/${appToken}/tables/${tableId}/records/search`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filter }),
      });

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`查询多维表格记录失败: ${data.msg}`);
      }

      return data.data.items || [];
    } catch (error) {
      console.error('查询多维表格记录失败:', error);
      throw error;
    }
  }
}

module.exports = LarkClient;
