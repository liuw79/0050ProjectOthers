/**
 * 清理飞书段落表中的重复记录
 * 保留每组重复中最新的一条
 */
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';
dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const authRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ app_id: process.env.LARK_APP_ID, app_secret: process.env.LARK_APP_SECRET }),
});
const authData = await authRes.json();
if (authData.code !== 0) {
  console.error('认证失败:', authData.msg);
  process.exit(1);
}
const token = authData.tenant_access_token;

console.log('=== 清理重复段落 ===\n');

// 1. 获取所有段落
console.log('1. 获取所有段落...');
let all = [], pageToken = '';
for (let i = 0; i < 60; i++) {
  const res = await fetch(
    'https://open.feishu.cn/open-apis/bitable/v1/apps/' + process.env.LARK_SEGMENTS_APP_TOKEN + '/tables/' + process.env.LARK_SEGMENTS_TABLE_ID + '/records/search',
    { method: 'POST', headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }, body: JSON.stringify({ page_size: 500, page_token: pageToken }) }
  );
  const data = await res.json();
  if (!data.data || !data.data.items) {
    console.log('API 响应异常:', JSON.stringify(data).slice(0, 200));
    break;
  }
  all.push(...data.data.items);
  pageToken = data.data.page_token || '';
  if (!data.data.has_more) break;
}
console.log('   总数:', all.length);

// 2. 按课程+段落索引分组
console.log('\n2. 分析重复情况...');
const groups = {};
for (const r of all) {
  const courseId = r.fields.course?.link_record_ids?.[0];
  const idx = r.fields.segment_index;
  if (courseId && idx !== undefined) {
    const key = courseId + '-' + idx;
    if (!groups[key]) groups[key] = [];
    groups[key].push(r);
  }
}

// 3. 找出要删除的记录ID（保留每组中最新的一个）
const toDelete = [];
for (const [key, records] of Object.entries(groups)) {
  if (records.length > 1) {
    // 按创建时间排序，保留最新的
    records.sort((a, b) => (b.created_time || 0) - (a.created_time || 0));
    // 删除除第一个外的所有记录
    for (let i = 1; i < records.length; i++) {
      toDelete.push(records[i].record_id);
    }
  }
}

console.log('   重复组:', Object.entries(groups).filter(([k, v]) => v.length > 1).length);
console.log('   需删除:', toDelete.length);

// 4. 分批删除
console.log('\n3. 删除重复记录...');
let deleted = 0;
const batchSize = 500;

for (let i = 0; i < toDelete.length; i += batchSize) {
  const batch = toDelete.slice(i, i + batchSize);

  const res = await fetch(
    'https://open.feishu.cn/open-apis/bitable/v1/apps/' + process.env.LARK_SEGMENTS_APP_TOKEN + '/tables/' + process.env.LARK_SEGMENTS_TABLE_ID + '/records/batch_delete',
    {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ records: batch }),
    }
  );
  const data = await res.json();

  if (data.code === 0) {
    deleted += batch.length;
    console.log('   已删除:', deleted, '/', toDelete.length);
  } else {
    console.log('   删除失败:', data.msg);
  }

  // 避免请求过快
  await new Promise(r => setTimeout(r, 100));
}

console.log('\n=== 完成 ===');
console.log('删除:', deleted, '条');
console.log('保留:', all.length - deleted, '条');
