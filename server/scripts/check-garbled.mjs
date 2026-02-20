/**
 * 检测乱码课程并列出本地文件
 */
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const COURSES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), '../../01_课程知识库');

const authRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ app_id: process.env.LARK_APP_ID, app_secret: process.env.LARK_APP_SECRET }),
});
const authData = await authRes.json();
const token = authData.tenant_access_token;

// 获取课程列表
const coursesRes = await fetch(
  `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_COURSES_APP_TOKEN}/tables/${process.env.LARK_COURSES_TABLE_ID}/records?page_size=100`,
  { headers: { 'Authorization': `Bearer ${token}` } }
);
const coursesData = await coursesRes.json();
const courses = (coursesData.data?.items || []).map(r => ({
  id: r.record_id,
  name: r.fields.course_name?.[0]?.text || r.fields.course_name,
}));

// 获取所有段落
let allSegments = [];
let pageToken = '';
for (let i = 0; i < 10; i++) {
  const res = await fetch(
    `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_SEGMENTS_APP_TOKEN}/tables/${process.env.LARK_SEGMENTS_TABLE_ID}/records/search`,
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ page_size: 500, page_token: pageToken })
    }
  );
  const data = await res.json();
  if (data.data?.items) allSegments.push(...data.data.items);
  pageToken = data.data?.page_token || '';
  if (!data.data?.has_more) break;
}

// 检测乱码
const garbledPattern = /[\uFFFD\u0000-\u001F]{3,}|ā|ē|ī|ō|ū|ǖ|ǘ|ǚ|ǜ|�{2,}/;
const garbledCourses = new Set();

for (const seg of allSegments) {
  let content = seg.fields.content || '';
  if (Array.isArray(content)) content = content.map(c => c.text || '').join('');
  if (garbledPattern.test(content)) {
    const courseId = seg.fields.course?.link_record_ids?.[0];
    if (courseId) garbledCourses.add(courseId);
  }
}

console.log('=== 乱码课程分析 ===\n');
console.log(`总段落数: ${allSegments.length}`);
console.log(`有乱码的课程: ${garbledCourses.size}\n`);

// 列出本地课程目录
const localDirs = fs.readdirSync(COURSES_DIR, { withFileTypes: true })
  .filter(d => d.isDirectory() && !d.name.startsWith('.'))
  .map(d => d.name);

console.log('=== 需要重新处理的课程 ===\n');

for (const courseId of garbledCourses) {
  const course = courses.find(c => c.id === courseId);
  const courseName = course?.name || courseId;

  // 尝试匹配本地文件
  const localMatch = localDirs.find(d =>
    d.includes(courseName) || courseName.includes(d) ||
    d.replace(/[^u4e00-\u9fa5a-zA-Z0-9]/g, '') === courseName.replace(/[^u4e00-\u9fa5a-zA-Z0-9]/g, '')
  );

  console.log(`课程: ${courseName}`);
  console.log(`  飞书ID: ${courseId}`);
  console.log(`  本地匹配: ${localMatch || '❌ 未找到'}`);

  if (localMatch) {
    const coursePath = path.join(COURSES_DIR, localMatch);
    const files = fs.readdirSync(coursePath).filter(f => f.endsWith('.txt'));
    console.log(`  文件数: ${files.length}`);
    for (const f of files) {
      const filePath = path.join(coursePath, f);
      const stat = fs.statSync(filePath);
      console.log(`    - ${f} (${Math.round(stat.size / 1024)}KB)`);
    }
  }
  console.log('');
}
