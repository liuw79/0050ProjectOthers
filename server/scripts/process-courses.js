/**
 * 处理本地课程文件，生成语义段落并存入飞书
 *
 * 使用方法:
 *   node scripts/process-courses.js              # 处理所有课程
 *   node scripts/process-courses.js --course "课程名"  # 处理指定课程
 *   node scripts/process-courses.js --limit 2    # 只处理前2门课程
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import dotenv from 'dotenv';
import { segmenter } from '../src/lib/segmenter.js';
import { lark } from '../src/lib/lark.js';

dotenv.config({ path: path.join(path.dirname(fileURLToPath(import.meta.url)), '../.env') });

const COURSES_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), '../../01_课程知识库');

const TABLES = {
  courses: {
    appToken: process.env.LARK_COURSES_APP_TOKEN,
    tableId: process.env.LARK_COURSES_TABLE_ID,
  },
  segments: {
    appToken: process.env.LARK_SEGMENTS_APP_TOKEN,
    tableId: process.env.LARK_SEGMENTS_TABLE_ID,
  },
};

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    course: null,
    limit: null,
    dryRun: false,
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--course' && args[i + 1]) {
      options.course = args[i + 1];
      i++;
    } else if (args[i] === '--limit' && args[i + 1]) {
      options.limit = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--dry-run') {
      options.dryRun = true;
    }
  }

  return options;
}

/**
 * 读取本地课程文件
 */
function readLocalCourses() {
  if (!fs.existsSync(COURSES_DIR)) {
    console.error(`课程目录不存在: ${COURSES_DIR}`);
    return [];
  }

  const dirs = fs.readdirSync(COURSES_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.'))
    .map(d => d.name);

  return dirs.map(courseName => {
    const coursePath = path.join(COURSES_DIR, courseName);
    const files = fs.readdirSync(coursePath).filter(f => f.endsWith('.txt'));

    if (files.length === 0) return null;

    // 合并所有文件内容
    let content = '';
    for (const file of files) {
      const filePath = path.join(coursePath, file);
      const fileContent = readFileWithEncoding(filePath);
      content += `\n\n=== ${file} ===\n\n${fileContent}`;
    }

    return {
      name: courseName,
      content: content.trim(),
      fileCount: files.length,
    };
  }).filter(Boolean);
}

/**
 * 检测并转换文件编码
 */
function readFileWithEncoding(filePath) {
  // 先尝试 UTF-8
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    // 检查是否有乱码特征
    if (!content.includes('�') && !hasGarbledText(content)) {
      return content;
    }
  } catch (e) {}

  // 尝试 GBK 转 UTF-8
  try {
    const result = execFileSync('iconv', ['-f', 'GBK', '-t', 'UTF-8', filePath], {
      encoding: 'utf-8',
      maxBuffer: 50 * 1024 * 1024
    });
    console.log(`  编码转换: ${path.basename(filePath)} (GBK → UTF-8)`);
    return result;
  } catch (e) {
    console.log(`  编码转换失败: ${path.basename(filePath)} - ${e.message}`);
    return fs.readFileSync(filePath, 'utf-8');
  }
}

/**
 * 检测是否有乱码
 */
function hasGarbledText(text) {
  // 检查常见的 GBK 乱码特征
  const sample = text.slice(0, 2000);
  const garbledPatterns = [
    /[\x80-\x9F]{3,}/,  // 连续高位字节
    /ā|ē|ī|ō|ū|ǖ|ǘ|ǚ|ǜ/, // 拼音符号乱码
  ];
  return garbledPatterns.some(p => p.test(sample));
}

/**
 * 获取飞书中的课程记录
 */
async function getFeishuCourses() {
  const records = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
  return records.map(r => ({
    id: r.record_id,
    name: r.fields.course_name,
    teacher: r.fields.teacher,
    content: r.fields.content,
    processStatus: r.fields.process_status,
  }));
}

/**
 * 匹配本地课程和飞书课程
 */
function matchCourses(localCourses, feishuCourses) {
  const matches = [];

  for (const local of localCourses) {
    // 尝试多种匹配方式
    let feishu = feishuCourses.find(f => f.name === local.name);

    // 如果精确匹配失败，尝试模糊匹配
    if (!feishu) {
      feishu = feishuCourses.find(f => {
        const localName = local.name.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
        const feishuName = f.name.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
        return localName.includes(feishuName) || feishuName.includes(localName);
      });
    }

    matches.push({
      local,
      feishu,
      matched: !!feishu,
    });
  }

  return matches;
}

/**
 * 将段落写入飞书
 */
async function saveSegmentsToFeishu(courseId, segments, dryRun = false) {
  if (dryRun) {
    console.log(`  [DRY RUN] 将保存 ${segments.length} 个段落到飞书`);
    return;
  }

  let savedCount = 0;
  for (const segment of segments) {
    try {
      // 关联字段：直接使用 record_id 数组
      const fields = {
        title: segment.title,
        segment_index: segment.index,
        summary: segment.summary,
        content: segment.content,
        char_count: segment.charCount,
      };

      // 添加关联字段
      fields.course = [courseId];

      // 添加关键词（如果有）
      if (segment.keywords && segment.keywords.length > 0) {
        fields.keywords = segment.keywords;
      }

      await lark.addRecord(TABLES.segments.appToken, TABLES.segments.tableId, fields);
      console.log(`  ✅ 段落 ${segment.index} 保存成功`);
      savedCount++;
    } catch (err) {
      console.error(`  ❌ 段落 ${segment.index} 保存失败: ${err.message}`);
    }
  }
  return savedCount;
}

/**
 * 更新课程处理状态
 * 注意：需要先在飞书课程表中添加以下字段：
 * - overview (多行文本)
 * - segment_index (多行文本)
 * - process_status (单选: 待处理/处理中/已完成)
 */
async function updateCourseStatus(courseId, overview, segmentIndex, dryRun = false) {
  if (dryRun) {
    console.log(`  [DRY RUN] 将更新课程状态和概述`);
    return;
  }

  try {
    // 尝试更新，如果字段不存在会失败，但不影响段落数据
    await lark.updateRecord(TABLES.courses.appToken, TABLES.courses.tableId, courseId, {
      overview: overview,
      segment_index: JSON.stringify(segmentIndex),
      process_status: '已完成',
    });
    console.log(`  ✅ 课程状态更新成功`);
  } catch (err) {
    // 字段不存在时不报错，只是提示
    if (err.message.includes('FieldNameNotFound')) {
      console.log(`  ⚠️ 课程表缺少字段(overview/segment_index/process_status)，跳过状态更新`);
      console.log(`     请在飞书课程表中添加这些字段后重新运行`);
    } else {
      console.error(`  ❌ 课程状态更新失败: ${err.message}`);
    }
  }
}

/**
 * 生成段落索引
 */
function generateSegmentIndex(segments) {
  return {
    segments: segments.map(s => ({
      index: s.index,
      title: s.title,
      summary: s.summary.slice(0, 100) + '...', // 索引中只保留摘要前100字
    }))
  };
}

/**
 * 处理单门课程
 */
async function processCourse(localCourse, feishuCourse, dryRun = false) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`处理课程: ${localCourse.name}`);
  console.log(`文件数: ${localCourse.fileCount}, 总字数: ${localCourse.content.length}`);
  console.log(`飞书ID: ${feishuCourse ? feishuCourse.id : '未匹配'}`);

  if (!feishuCourse) {
    console.log('⚠️ 未在飞书中找到对应课程，跳过');
    return { success: false, reason: '未匹配' };
  }

  if (feishuCourse.processStatus === '已完成') {
    console.log('⏭️ 课程已处理过，跳过（如需重新处理，请先清除状态）');
    return { success: false, reason: '已处理' };
  }

  try {
    // 使用本地文件内容（更完整）
    const content = localCourse.content;

    // 调用语义切分器处理
    const result = await segmenter.processCourse(content, localCourse.name);

    // 保存段落到飞书
    console.log('\n保存段落到飞书...');
    await saveSegmentsToFeishu(feishuCourse.id, result.segments, dryRun);

    // 更新课程状态
    console.log('\n更新课程状态...');
    const segmentIndex = generateSegmentIndex(result.segments);
    await updateCourseStatus(feishuCourse.id, result.overview, segmentIndex, dryRun);

    console.log(`\n✅ 课程处理完成！共 ${result.segments.length} 个段落`);
    return { success: true, segmentCount: result.segments.length };
  } catch (err) {
    console.error(`\n❌ 课程处理失败: ${err.message}`);
    return { success: false, reason: err.message };
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('课程段落处理脚本');
  console.log('================\n');

  const options = parseArgs();
  if (options.dryRun) {
    console.log('🔍 DRY RUN 模式 - 不会实际写入飞书\n');
  }

  // 读取本地课程
  console.log('1. 读取本地课程文件...');
  const localCourses = readLocalCourses();
  console.log(`   找到 ${localCourses.length} 门本地课程\n`);

  if (localCourses.length === 0) {
    console.log('没有找到本地课程文件');
    return;
  }

  // 获取飞书课程
  console.log('2. 获取飞书课程记录...');
  const feishuCourses = await getFeishuCourses();
  console.log(`   找到 ${feishuCourses.length} 门飞书课程\n`);

  // 匹配课程
  console.log('3. 匹配本地课程和飞书课程...');
  const matches = matchCourses(localCourses, feishuCourses);
  const matchedCount = matches.filter(m => m.matched).length;
  console.log(`   成功匹配 ${matchedCount}/${matches.length} 门课程\n`);

  // 筛选要处理的课程
  let toProcess = matches.filter(m => m.matched);

  if (options.course) {
    toProcess = toProcess.filter(m =>
      m.local.name.includes(options.course)
    );
    console.log(`   筛选包含 "${options.course}" 的课程: ${toProcess.length} 门\n`);
  }

  if (options.limit) {
    toProcess = toProcess.slice(0, options.limit);
    console.log(`   限制处理数量: ${toProcess.length} 门\n`);
  }

  // 处理课程
  console.log('4. 开始处理课程...\n');

  const results = {
    total: toProcess.length,
    success: 0,
    failed: 0,
    skipped: 0,
    details: [],
  };

  for (const match of toProcess) {
    const result = await processCourse(match.local, match.feishu, options.dryRun);
    results.details.push({
      name: match.local.name,
      ...result,
    });

    if (result.success) {
      results.success++;
    } else if (result.reason === '已处理') {
      results.skipped++;
    } else {
      results.failed++;
    }
  }

  // 输出统计
  console.log('\n' + '='.repeat(60));
  console.log('处理完成！');
  console.log(`总计: ${results.total} 门`);
  console.log(`成功: ${results.success} 门`);
  console.log(`跳过: ${results.skipped} 门`);
  console.log(`失败: ${results.failed} 门`);

  if (results.failed > 0) {
    console.log('\n失败详情:');
    results.details
      .filter(d => !d.success && d.reason !== '已处理')
      .forEach(d => console.log(`  - ${d.name}: ${d.reason}`));
  }
}

main().catch(err => {
  console.error('脚本执行失败:', err);
  process.exit(1);
});
