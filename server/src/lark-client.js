// 飞书API客户端
require('dotenv').config();
const { WebClient } = require('@larksuiteoapi/web');
const { Client as DocClient } = require('@larksuiteoapi/docx');

class LarkClient {
  constructor() {
    // 初始化WebClient（用于多维表格操作）
    this.webClient = new WebClient({
      appId: process.env.LARK_APP_ID,
      appSecret: process.env.LARK_APP_SECRET,
    });
  }

  // 获取access token
  async getAccessToken() {
    try {
      const response = await this.webClient.auth.appAccessToken.internalGet({});
      return response.app_access_token;
    } catch (error) {
      console.error('获取飞书token失败:', error);
      throw error;
    }
  }

  // 获取多维表格数据
  async getBitableData(appToken, tableId, options = {}) {
    try {
      const { page_size = 100, page_token = '' } = options;
      const response = await this.webClient.bitable.appTableRecord.list({
        app_token: appToken,
        table_id: tableId,
        page_size,
        page_token,
      });
      return response.data.items;
    } catch (error) {
      console.error('获取多维表格数据失败:', error);
      throw error;
    }
  }

  // 添加多维表格记录
  async addBitableRecord(appToken, tableId, fields) {
    try {
      const response = await this.webClient.bitable.appTableRecord.create({
        app_token: appToken,
        table_id: tableId,
        fields,
      });
      return response.data;
    } catch (error) {
      console.error('添加多维表格记录失败:', error);
      throw error;
    }
  }

  // 更新多维表格记录
  async updateBitableRecord(appToken, tableId, recordId, fields) {
    try {
      const response = await this.webClient.bitable.appTableRecord.update({
        app_token: appToken,
        table_id: tableId,
        record_id: recordId,
        fields,
      });
      return response.data;
    } catch (error) {
      console.error('更新多维表格记录失败:', error);
      throw error;
    }
  }

  // 查询多维表格记录
  async queryBitableRecords(appToken, tableId, filter = {}) {
    try {
      const response = await this.webClient.bitable.appTableRecord.search({
        app_token: appToken,
        table_id: tableId,
        filter,
      });
      return response.data.items;
    } catch (error) {
      console.error('查询多维表格记录失败:', error);
      throw error;
    }
  }
}

module.exports = LarkClient;
