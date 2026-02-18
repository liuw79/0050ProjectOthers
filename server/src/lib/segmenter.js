// server/src/lib/segmenter.js

// 配置常量
const MIN_SEGMENT_SIZE = 8000; // 段落最小字数
const MAX_SEGMENT_SIZE = 15000; // 段落最大字数
const TARGET_SEGMENT_SIZE = 10000; // 目标段落字数

// GLM API 配置（延迟获取，确保 dotenv 已加载）
const getGLMConfig = () => ({
  apiKey: process.env.ZHIPUAI_API_KEY,
  baseUrl: 'https://open.bigmodel.cn/api/paas/v4',
});

/**
 * 调用 GLM API 生成文本
 */
async function callGLM(prompt) {
  const { apiKey, baseUrl } = getGLMConfig();

  if (!apiKey) {
    console.log('GLM API Key 未配置');
    return '';
  }

  try {
    console.log('GLM API 请求...');
    const res = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'glm-4-flash',  // 快速模型，效果稳定
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 200,
      }),
    });
    const data = await res.json();
    console.log('GLM API 响应:', JSON.stringify(data).slice(0, 200));
    return data.choices?.[0]?.message?.content || '';
  } catch (e) {
    console.error('GLM API 调用失败:', e.message);
    return '';
  }
}

/**
 * 语义切分器类
 * 策略：按语义段落（双换行）智能切分，确保每段 8000-15000 字
 */
export class Segmenter {
  constructor(options = {}) {
    this.minSegmentSize = options.minSegmentSize || MIN_SEGMENT_SIZE;
    this.maxSegmentSize = options.maxSegmentSize || MAX_SEGMENT_SIZE;
    this.targetSegmentSize = options.targetSegmentSize || TARGET_SEGMENT_SIZE;
  }

  /**
   * 按语义段落切分文本
   * 优先在双换行处切分，确保每段在目标范围内
   */
  createSegments(text) {
    const totalLength = text.length;
    const segments = [];

    // 按双换行分割成自然段落
    const paragraphs = text.split(/\n\n+/);
    const paragraphBoundaries = [0];
    let currentPos = 0;

    for (const para of paragraphs) {
      currentPos += para.length + 2; // +2 for \n\n
      paragraphBoundaries.push(Math.min(currentPos, totalLength));
    }

    // 基于自然段落边界，合并成目标大小的段
    let segmentStart = 0;
    let segmentLength = 0;

    for (let i = 0; i < paragraphs.length; i++) {
      const paraLength = paragraphs[i].length + 2;
      segmentLength += paraLength;

      // 如果达到目标大小，且不是最后一个段落
      if (segmentLength >= this.targetSegmentSize && i < paragraphs.length - 1) {
        const segmentEnd = paragraphBoundaries[i + 1];
        segments.push({ start: segmentStart, end: segmentEnd });
        segmentStart = segmentEnd;
        segmentLength = 0;
      }
    }

    // 添加最后一段
    if (segmentStart < totalLength) {
      const lastSegmentLength = totalLength - segmentStart;

      // 如果最后一段太短，合并到前一段
      if (lastSegmentLength < this.minSegmentSize / 2 && segments.length > 0) {
        segments[segments.length - 1].end = totalLength;
      } else {
        segments.push({ start: segmentStart, end: totalLength });
      }
    }

    // 处理过长的段落
    const finalSegments = [];
    for (const seg of segments) {
      const length = seg.end - seg.start;
      if (length > this.maxSegmentSize) {
        // 按固定大小切分
        const subSegments = this._splitBySize(seg.start, seg.end, this.targetSegmentSize);
        finalSegments.push(...subSegments);
      } else {
        finalSegments.push(seg);
      }
    }

    console.log(`划分为 ${finalSegments.length} 个段落`);
    return finalSegments;
  }

  /**
   * 按固定大小切分段落
   */
  _splitBySize(start, end, targetSize) {
    const segments = [];
    let current = start;

    while (current < end) {
      const segmentEnd = Math.min(current + targetSize, end);
      // 确保最后一段不要太短
      if (end - segmentEnd < this.minSegmentSize / 2 && segmentEnd < end) {
        segments.push({ start: current, end: end });
        break;
      }
      segments.push({ start: current, end: segmentEnd });
      current = segmentEnd;
    }

    return segments;
  }

  /**
   * 为段落生成标题和摘要
   */
  async generateSegmentMeta(text, courseName, index) {
    const analysisText = text.slice(0, 2000);

    // 使用 GLM 生成标题
    const titlePrompt = `给课程段落起标题，15-20字，概括主题。

课程：${courseName}
内容：${analysisText.slice(0, 1000)}

只输出标题，不要其他内容。`;

    let title = '';
    try {
      title = await callGLM(titlePrompt);
      title = title.trim().replace(/["\n]/g, '').slice(0, 25);
    } catch (e) {
      console.error(`生成标题失败:`, e.message);
    }

    // 如果 GLM 失败，使用备选方案
    if (!title || title.length < 5) {
      title = this._extractTitle(text, courseName, index);
    }

    // 使用 GLM 生成摘要
    const summaryPrompt = `用100字概括课程段落核心内容。

${analysisText}

只输出摘要。`;

    let summary = '';
    try {
      summary = await callGLM(summaryPrompt);
      summary = summary.trim().slice(0, 200);
    } catch (e) {
      console.error(`生成摘要失败:`, e.message);
    }

    if (!summary) {
      summary = text.slice(0, 150).replace(/\n/g, ' ').trim() + '...';
    }

    return { title, summary, keywords: [] };
  }

  /**
   * 从内容提取标题（备选方案）
   */
  _extractTitle(text, courseName, index) {
    const lines = text.split('\n')
      .map(l => l.trim())
      .filter(l => l.length >= 10 && l.length <= 50)
      .filter(l => !l.startsWith('**') && !l.startsWith('===') && !l.startsWith('###'));

    const keywords = ['核心', '关键', '方法', '策略', '原则', '实战', '案例', '体系', '流程'];

    for (const line of lines) {
      if (keywords.some(k => line.includes(k))) {
        return line.slice(0, 25);
      }
    }

    return lines[0]?.slice(0, 25) || `${courseName.slice(0, 10)} 第${index}段`;
  }

  /**
   * 生成默认的元数据
   */
  _getDefaultMeta(text, index) {
    const firstLine = text.split('\n').find(line => line.trim().length > 10) || '';
    const title = firstLine.slice(0, 25) || `第${index}段`;
    return {
      title: `${title}${title.length >= 25 ? '' : '...'}`,
      summary: text.slice(0, 300).replace(/\n/g, ' ') + '...',
      keywords: []
    };
  }

  /**
   * 生成课程概述
   */
  async generateCourseOverview(text, courseName) {
    const samples = [
      text.slice(0, 1500),
      text.slice(Math.floor(text.length * 0.5), Math.floor(text.length * 0.5) + 1500),
    ].join('\n\n---\n\n');

    const prompt = `根据课程内容采样，生成200字概述。

课程：${courseName}
字数：${text.length}

采样：
${samples}

要求：包含核心主题和主要框架。`;

    let overview = '';
    try {
      overview = await callGLM(prompt);
    } catch (e) {
      console.error('生成概述失败:', e.message);
    }

    if (!overview) {
      overview = `【${courseName}】\n\n本课程共 ${text.length} 字，划分为多个段落。`;
    }

    return overview;
  }

  /**
   * 完整处理一门课程
   */
  async processCourse(text, courseName) {
    console.log(`\n开始处理课程: ${courseName}`);
    console.log(`文本长度: ${text.length} 字`);

    // 1. 生成课程概述
    console.log('\n1. 生成课程概述...');
    const overview = await this.generateCourseOverview(text, courseName);
    console.log(`   概述长度: ${overview.length} 字`);

    // 2. 划分段落
    console.log('\n2. 划分段落...');
    const segmentRanges = this.createSegments(text);

    // 3. 为每个段落生成元数据
    console.log('\n3. 生成段落元数据...');
    const segments = [];
    let segmentIndex = 0;

    for (let i = 0; i < segmentRanges.length; i++) {
      const { start, end } = segmentRanges[i];
      const content = text.slice(start, end).trim();

      if (content.length < this.minSegmentSize / 2) {
        console.log(`  跳过段落 ${i + 1}（过短: ${content.length} 字）`);
        continue;
      }

      segmentIndex++;
      console.log(`  处理段落 ${segmentIndex}/${segmentRanges.length} (${content.length} 字)...`);

      const meta = await this.generateSegmentMeta(content, courseName, segmentIndex);

      segments.push({
        index: segmentIndex,
        title: meta.title,
        summary: meta.summary,
        content: content,
        charCount: content.length,
        keywords: meta.keywords
      });

      // 避免请求过快
      await this._sleep(300);
    }

    console.log(`\n处理完成！共 ${segments.length} 个段落`);

    return { overview, segments };
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export const segmenter = new Segmenter();
