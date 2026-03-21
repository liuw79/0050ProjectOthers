// server/src/lib/lark.js
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

export class LarkClient {
  constructor() {
    this.token = null;
    this.tokenExpire = 0;
  }

  get appId() {
    return process.env.LARK_APP_ID;
  }

  get appSecret() {
    return process.env.LARK_APP_SECRET;
  }

  async getToken() {
    if (this.token && Date.now() < this.tokenExpire) {
      return this.token;
    }
    const res = await fetch(`${FEISHU_BASE}/auth/v3/app_access_token/internal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        app_id: this.appId,
        app_secret: this.appSecret,
      }),
    });
    const data = await res.json();
    if (data.code !== 0) throw new Error(`飞书认证失败: ${data.msg}`);
    this.token = data.app_access_token;
    this.tokenExpire = Date.now() + (data.expire - 300) * 1000;
    return this.token;
  }

  async getRecords(appToken, tableId) {
    const token = await this.getToken();
    const url = `${FEISHU_BASE}/bitable/v1/apps/${appToken}/tables/${tableId}/records?page_size=500`;
    console.log('Lark request:', url);
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    const text = await res.text();
    console.log('Lark response status:', res.status, 'body:', text.slice(0, 200));
    let data;
    try {
      data = JSON.parse(text);
    } catch (e) {
      console.error('Lark JSON parse error:', e.message);
      throw new Error(`飞书 API 返回非 JSON: ${text.slice(0, 100)}`);
    }
    if (data.code !== 0) throw new Error(`获取记录失败: ${data.msg}`);
    return this.normalize(data.data.items || []);
  }

  async searchRecords(appToken, tableId, filter) {
    const token = await this.getToken();
    const res = await fetch(
      `${FEISHU_BASE}/bitable/v1/apps/${appToken}/tables/${tableId}/records/search`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filter }),
      }
    );
    const data = await res.json();
    if (data.code !== 0) throw new Error(`搜索失败: ${data.msg}`);
    return this.normalize(data.data.items || []);
  }

  async addRecord(appToken, tableId, fields) {
    const token = await this.getToken();
    const res = await fetch(
      `${FEISHU_BASE}/bitable/v1/apps/${appToken}/tables/${tableId}/records`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fields }),
      }
    );
    const data = await res.json();
    if (data.code !== 0) throw new Error(`添加记录失败: ${data.msg}`);
    return data.data;
  }

  async updateRecord(appToken, tableId, recordId, fields) {
    const token = await this.getToken();
    const res = await fetch(
      `${FEISHU_BASE}/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ fields }),
      }
    );
    const data = await res.json();
    if (data.code !== 0) throw new Error(`更新记录失败: ${data.msg}`);
    return data.data;
  }

  async deleteRecords(appToken, tableId, recordIds) {
    if (!recordIds || recordIds.length === 0) return { deleted: 0 };

    const token = await this.getToken();
    const res = await fetch(
      `${FEISHU_BASE}/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_delete`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ records: recordIds }),
      }
    );
    const data = await res.json();
    if (data.code !== 0) throw new Error(`删除记录失败: ${data.msg}`);
    return { deleted: recordIds.length };
  }

  normalize(records) {
    return records.map(r => {
      const fields = {};
      for (const [k, v] of Object.entries(r.fields || {})) {
        if (Array.isArray(v) && v[0]?.text !== undefined) {
          fields[k] = v[0].text;
        } else {
          fields[k] = v;
        }
      }
      return { ...r, fields };
    });
  }
}

export const lark = new LarkClient();
