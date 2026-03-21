/**
 * 验证段落质量 - 抽查几门课程确认内容正常
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
console.log('✅ 认证成功\n');

// 1. 获取课程列表
console.log('1. 获取课程列表...');
const coursesRes = await fetch(
  `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_COURSES_APP_TOKEN}/tables/${process.env.LARK_COURSES_TABLE_ID}/records?page_size=100`,
  { headers: { 'Authorization': `Bearer ${token}` } }
);
const coursesData = await coursesRes.json();
const courses = (coursesData.data?.items || []).map(r => ({
  id: r.record_id,
  name: r.fields.course_name?.[0]?.text || r.fields.course_name,
}));
console.log(`   课程数: ${courses.length}\n`);

// 2. 获取所有段落（分页）
console.log('2. 获取段落...');
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
  if (data.data?.items) {
    allSegments.push(...data.data.items);
  }
  pageToken = data.data?.page_token || '';
  if (!data.data?.has_more) break;
}
console.log(`   段落数: ${allSegments.length}\n`);

// 3. 按课程分组统计
console.log('3. 按课程统计...');
const segmentsByCourse = {};
for (const seg of allSegments) {
  const courseId = seg.fields.course?.link_record_ids?.[0];
  if (!courseId) continue;
  if (!segmentsByCourse[courseId]) segmentsByCourse[courseId] = [];
  segmentsByCourse[courseId].push(seg);
}
console.log(`   有段落的课程: ${Object.keys(segmentsByCourse).length}\n`);

// 4. 检测乱码
console.log('4. 检测乱码...');
const garbledPattern = /[\uFFFD\u0000-\u001F]{3,}|ā|ē|ī|ō|ū|ǖ|ǘ|ǚ|ǜ|�{2,}/;
const coursesWithGarbled = [];

for (const [courseId, segments] of Object.entries(segmentsByCourse)) {
  const course = courses.find(c => c.id === courseId);
  const courseName = course?.name || courseId;

  let garbledCount = 0;
  for (const seg of segments) {
    let content = seg.fields.content || '';
    // 处理富文本格式
    if (Array.isArray(content)) {
      content = content.map(c => c.text || '').join('');
    }
    if (garbledPattern.test(content)) {
      garbledCount++;
    }
  }

  if (garbledCount > 0) {
    coursesWithGarbled.push({ name: courseName, garbled: garbledCount, total: segments.length });
  }
}

if (coursesWithGarbled.length === 0) {
  console.log('   ✅ 未检测到乱码课程\n');
} else {
  console.log(`   ⚠️  有乱码的课程: ${coursesWithGarbled.length}`);
  for (const c of coursesWithGarbled) {
    console.log(`      - ${c.name}: ${c.garbled}/${c.total} 段落有乱码`);
  }
  console.log('');
}

// 5. 抽查 5 门课程的段落内容
console.log('5. 抽查 5 门课程...\n');
const toCheck = Object.entries(segmentsByCourse).slice(0, 5);

for (const [courseId, segments] of toCheck) {
  const course = courses.find(c => c.id === courseId);
  const courseName = course?.name || courseId;

  console.log(`\n=== ${courseName} (${segments.length} 段) ===`);

  // 显示第一段和最后一段的内容预览
  for (const seg of [segments[0], segments[segments.length - 1]]) {
    const idx = seg.fields.segment_index;
    let title = seg.fields.title || '(无标题)';
    // 处理富文本格式
    if (Array.isArray(title)) {
      title = title.map(t => t.text || '').join('');
    }
    let content = seg.fields.content || '';
    // 处理富文本格式
    if (Array.isArray(content)) {
      content = content.map(c => c.text || '').join('');
    }
    const preview = String(content).slice(0, 300).replace(/\n/g, ' ');
    const hasGarbled = garbledPattern.test(content);

    console.log(`  段落 ${idx}: ${title}`);
    console.log(`  预览: ${preview}...`);
    console.log(`  字数: ${content.length} | 乱码: ${hasGarbled ? '⚠️ 是' : '✅ 否'}`);
    console.log('');
  }
}

console.log('\n=== 验证完成 ===');
