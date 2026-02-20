/**
 * 修复乱码课程 - 重新处理8门课程
 * 排除: 月度经营分析会(241019) 本地文件损坏
 */
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const COURSES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), '../../01_课程知识库');

// 需要重新处理的课程（排除月度经营分析会(241019)本地文件损坏）
const TO_FIX = [
  '创始人财务进阶(240921)',
  '创始人财务进阶(260117)',
  '升级定位(250315)',
  '月度经营分析会(260109)',
  '超级转化率 陈勇老师',
  '超级转化率(251220)',
  '超级面试官',
  '需求预测管理和库存管控(260117)',
];

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

// 1. 获取飞书课程和段落
const coursesRes = await fetch(
  `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_COURSES_APP_TOKEN}/tables/${process.env.LARK_COURSES_TABLE_ID}/records?page_size=100`,
  { headers: { 'Authorization': `Bearer ${token}` } }
);
const coursesData = await coursesRes.json();
const courses = (coursesData.data?.items || []).map(r => ({
  id: r.record_id,
  name: r.fields.course_name?.[0]?.text || r.fields.course_name,
}));

console.log(`飞书课程: ${courses.length} 门\n`);

// 2. 处理每门课程
let fixed = 0;
for (const courseName of TO_FIX) {
  console.log('='.repeat(50));
  console.log(`处理: ${courseName}`);

  // 匹配飞书课程
  const course = courses.find(c => c.name === courseName || c.name.includes(courseName) || courseName.includes(c.name));
  if (!course) {
    console.log('  ❌ 飞书中未找到对应课程\n');
    continue;
  }

  // 读取本地文件
  const localPath = path.join(COURSES_DIR, courseName);
  if (!fs.existsSync(localPath)) {
    console.log(`  ❌ 本地目录不存在: ${localPath}\n`);
    continue;
  }

  const files = fs.readdirSync(localPath).filter(f => f.endsWith('.txt'));
  let content = '';
  for (const file of files) {
    const filePath = path.join(localPath, file);
    content += `\n\n=== ${file} ===\n\n${readFileWithEncoding(filePath)}`;
  }
  console.log(`  本地内容: ${content.length} 字`);

  // 删除旧段落
  console.log('  删除旧段落...');
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

  const toDelete = allSegments.filter(r => {
    const courseId = r.fields.course?.link_record_ids?.[0];
    return courseId === course.id;
  }).map(r => r.record_id);

  if (toDelete.length > 0) {
    // 分批删除
    for (let i = 0; i < toDelete.length; i += 500) {
      const batch = toDelete.slice(i, i + 500);
      await fetch(
        `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_SEGMENTS_APP_TOKEN}/tables/${process.env.LARK_SEGMENTS_TABLE_ID}/records/batch_delete`,
        {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ records: batch }),
        }
      );
    }
    console.log(`  删除 ${toDelete.length} 个旧段落`);
  }

  // 清除课程状态
  await fetch(
    `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_COURSES_APP_TOKEN}/tables/${process.env.LARK_COURSES_TABLE_ID}/records/${course.id}`,
    {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ fields: { process_status: '待处理' } }),
    }
  );
  console.log('  ✅ 清除状态');

  // 调用 segmenter 处理
  const { segmenter } = await import('../src/lib/segmenter.js');
  const result = await segmenter.processCourse(content.trim(), courseName);

  console.log(`  划分: ${result.segments.length} 个段落`);

  // 保存段落
  let saved = 0;
  for (const seg of result.segments) {
    try {
      await fetch(
        `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_SEGMENTS_APP_TOKEN}/tables/${process.env.LARK_SEGMENTS_TABLE_ID}/records`,
        {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            fields: {
              title: seg.title,
              segment_index: seg.index,
              summary: seg.summary,
              content: seg.content,
              char_count: seg.charCount,
              course: [course.id],
            }
          }),
        }
      );
      saved++;
    } catch (e) {
      console.log(`  ⚠️ 段落 ${seg.index} 保存失败: ${e.message}`);
    }
  }

  // 更新课程状态
  await fetch(
    `https://open.feishu.cn/open-apis/bitable/v1/apps/${process.env.LARK_COURSES_APP_TOKEN}/tables/${process.env.LARK_COURSES_TABLE_ID}/records/${course.id}`,
    {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fields: {
          overview: result.overview,
          process_status: '已完成',
        }
      }),
    }
  );

  console.log(`  ✅ 课程处理完成，保存 ${saved} 个段落\n`);
  fixed++;
}

console.log('='.repeat(50));
console.log(`修复完成: ${fixed}/${TO_FIX.length} 门课程\n`);

// 编码转换函数
function readFileWithEncoding(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    if (!content.includes('�') && !hasGarbledText(content)) {
      return content;
    }
  } catch (e) {}

  try {
    const result = execFileSync('iconv', ['-f', 'GBK', '-t', 'UTF-8', filePath], {
      encoding: 'utf-8',
      maxBuffer: 50 * 1024 * 1024
    });
    console.log(`  编码转换: ${path.basename(filePath)} (GBK → UTF-8)`);
    return result;
  } catch (e) {
    console.log(`  编码转换失败: ${path.basename(filePath)}`);
    return fs.readFileSync(filePath, 'utf-8');
  }
}

function hasGarbledText(text) {
  const sample = text.slice(0, 2000);
  const garbledPatterns = [
    /[\x80-\x9F]{3,}/,
    /ā|ē|ī|ō|ū|ǖ|ǘ|ǚ|ǜ/,
  ];
  return garbledPatterns.some(p => p.test(sample));
}
