/**
 * 导入课程原文到飞书多维表格
 *
 * 使用方法: node scripts/import-courses.js
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const COURSES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), '../../01_课程知识库');
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const APP_TOKEN = process.env.LARK_COURSES_APP_TOKEN;
const TABLE_ID = process.env.LARK_COURSES_TABLE_ID;
const APP_ID = process.env.LARK_APP_ID;
const APP_SECRET = process.env.LARK_APP_SECRET;

let appAccessToken = null;

async function getAppAccessToken() {
  if (appAccessToken) return appAccessToken;

  const res = await fetch(`${FEISHU_BASE}/auth/v3/app_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`认证失败: ${data.msg}`);
  appAccessToken = data.app_access_token;
  return appAccessToken;
}

async function addRecord(fields) {
  const token = await getAppAccessToken();
  const res = await fetch(`${FEISHU_BASE}/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ fields }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`添加记录失败: ${data.msg}`);
  return data.data;
}

async function main() {
  console.log('开始导入课程原文...\n');

  // 获取所有课程目录
  const dirs = fs.readdirSync(COURSES_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.'))
    .map(d => d.name);

  console.log(`发现 ${dirs.length} 个课程目录\n`);

  let imported = 0;
  let skipped = 0;

  for (const courseName of dirs) {
    const coursePath = path.join(COURSES_DIR, courseName);

    // 读取该课程下所有 .txt 文件
    const files = fs.readdirSync(coursePath)
      .filter(f => f.endsWith('.txt'));

    if (files.length === 0) {
      console.log(`⏭️  ${courseName} - 没有 txt 文件，跳过`);
      skipped++;
      continue;
    }

    // 合并所有文件内容
    let content = '';
    for (const file of files) {
      const filePath = path.join(coursePath, file);
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      content += `\n\n=== ${file} ===\n\n${fileContent}`;
    }

    // 提取老师名称（从目录名或文件名中）
    let teacher = '';
    const teacherMatch = courseName.match(/[^\s]+老师|[\u4e00-\u9fa5]{2,3}(?=\s|$)/);
    if (teacherMatch) teacher = teacherMatch[0];

    // 添加到多维表格
    try {
      await addRecord({
        course_name: courseName,
        teacher: teacher,
        content: content.trim(),
        status: '待提取',
      });
      console.log(`✅ ${courseName} - 已导入 (${content.length} 字)`);
      imported++;
    } catch (err) {
      console.log(`❌ ${courseName} - 导入失败: ${err.message}`);
    }
  }

  console.log(`\n导入完成！成功: ${imported}, 跳过: ${skipped}`);
}

main().catch(console.error);
