/**
 * Claude Remote - 飞书长连接版本
 * 使用官方 @larksuiteoapi/node-sdk
 */

import * as Lark from '@larksuiteoapi/node-sdk';
import axios from 'axios';
import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

import { parseCommand, getHelpText } from './commands.js';
import {
  setCurrentProject,
  getCurrentProjectInfo,
  getAllProjects,
  getHistory
} from './session.js';
import { sendMessage, resetSession } from './claude.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载环境配置
const envPath = join(__dirname, '../config/.env');
if (existsSync(envPath)) {
  const envContent = readFileSync(envPath, 'utf-8');
  envContent.split('\n').forEach(line => {
    const [key, ...values] = line.split('=');
    if (key && values.length > 0) {
      process.env[key.trim()] = values.join('=').trim();
    }
  });
}

// 飞书应用配置
const LARK_APP_ID = process.env.LARK_APP_ID;
const LARK_APP_SECRET = process.env.LARK_APP_SECRET;

// 消息去重缓存
const processedMessages = new Set();
const MESSAGE_CACHE_SIZE = 100;

// 飞书 API 地址
const LARK_API = 'https://open.feishu.cn';

// 存储 access token
let larkAccessToken = null;
let tokenExpireTime = 0;

// 获取飞书 access token
async function getLarkAccessToken() {
  if (larkAccessToken && Date.now() < tokenExpireTime) {
    return larkAccessToken;
  }

  try {
    const response = await axios.post(
      `${LARK_API}/open-apis/auth/v3/tenant_access_token/internal`,
      {
        app_id: LARK_APP_ID,
        app_secret: LARK_APP_SECRET
      }
    );

    if (response.data.code === 0) {
      larkAccessToken = response.data.tenant_access_token;
      tokenExpireTime = Date.now() + (response.data.expire - 60) * 1000;
      console.log('[Lark] 获取 access token 成功');
      return larkAccessToken;
    } else {
      throw new Error(`获取 token 失败: ${response.data.msg}`);
    }
  } catch (error) {
    console.error('[Lark] 获取 access token 失败:', error.message);
    throw error;
  }
}

// 发送飞书消息
async function sendLarkMessage(openId, content) {
  const token = await getLarkAccessToken();

  try {
    // 分段发送长消息
    const maxLength = 30000;
    const chunks = [];

    if (content.length > maxLength) {
      for (let i = 0; i < content.length; i += maxLength) {
        chunks.push(content.slice(i, i + maxLength));
      }
    } else {
      chunks.push(content);
    }

    for (const chunk of chunks) {
      await axios.post(
        `${LARK_API}/open-apis/im/v1/messages?receive_id_type=open_id`,
        {
          receive_id: openId,
          msg_type: 'text',
          content: JSON.stringify({ text: chunk })
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (chunks.length > 1) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }

    console.log('[Lark] 消息发送成功');
  } catch (error) {
    console.error('[Lark] 发送消息失败:', error.response?.data || error.message);
  }
}

// 处理飞书事件
async function handleEvent(data) {
  const openId = data.sender?.sender_id?.open_id;
  const message = data.message;

  if (!message || !openId) {
    return;
  }

  // 消息去重
  const messageId = message.message_id;
  if (processedMessages.has(messageId)) {
    console.log(`[Event] 跳过重复消息: ${messageId}`);
    return;
  }

  // 添加到已处理缓存
  processedMessages.add(messageId);
  if (processedMessages.size > MESSAGE_CACHE_SIZE) {
    const first = processedMessages.values().next().value;
    processedMessages.delete(first);
  }

  console.log(`[Event] 处理消息: ${messageId}`);

  // 忽略机器人自己发送的消息
  if (data.sender?.sender_type === 'app') {
    return;
  }

  // 解析消息内容
  let userMessage = '';
  try {
    const content = JSON.parse(message.content);
    userMessage = content.text || '';
  } catch (e) {
    userMessage = message.content || '';
  }

  if (!userMessage.trim()) {
    return;
  }

  console.log(`[Event] 用户消息: ${userMessage}`);

  try {
    const command = parseCommand(userMessage);
    let reply = '';

    switch (command.type) {
      case 'status': {
        const project = getCurrentProjectInfo();
        reply = `📍 当前项目: ${project?.name || 'sys'}\n`;
        reply += `📁 路径: ${project?.path || '未知'}\n`;
        reply += `📝 描述: ${project?.description || '无'}`;
        break;
      }

      case 'projects': {
        const projects = getAllProjects();
        const lines = ['📚 可用项目列表:\n'];

        const groups = {};
        for (const [key, info] of Object.entries(projects)) {
          const prefix = key[0].toUpperCase();
          if (!groups[prefix]) groups[prefix] = [];
          groups[prefix].push({ key, ...info });
        }

        const seenPaths = new Set();
        for (const [prefix, items] of Object.entries(groups)) {
          const uniqueItems = items.filter(item => {
            if (seenPaths.has(item.path)) return false;
            seenPaths.add(item.path);
            return true;
          });

          if (uniqueItems.length > 0) {
            lines.push(`\n【${prefix}】`);
            for (const item of uniqueItems) {
              const aliases = items.filter(i => i.path === item.path).map(i => i.key);
              lines.push(`  /${aliases.join(' /')} - ${item.description}`);
            }
          }
        }

        reply = lines.join('\n');
        break;
      }

      case 'history': {
        const history = getHistory(command.count);
        if (history.length === 0) {
          reply = '📜 暂无历史记录';
        } else {
          const lines = ['📜 历史记录:\n'];
          for (const h of history) {
            const role = h.role === 'user' ? '👤' : '🤖';
            const preview = h.content.substring(0, 100) + (h.content.length > 100 ? '...' : '');
            lines.push(`${role} ${preview}`);
          }
          reply = lines.join('\n');
        }
        break;
      }

      case 'help':
        reply = getHelpText();
        break;

      case 'switch': {
        const result = setCurrentProject(command.project);
        if (result.success) {
          reply = `✅ 已切换到: ${result.project.name}\n`;
          reply += `📁 路径: ${result.project.path}\n`;
          reply += `📝 ${result.project.description}`;
        } else {
          reply = `❌ ${result.error}`;
          if (result.hint) {
            reply += `\n\n💡 ${result.hint}`;
          }
          if (result.matches) {
            reply += `\n\n使用完整目录名切换，例如: /${result.matches[0]}`;
          }
        }
        break;
      }

      case 'wake':
        reply = '💡 电脑已经在运行中';
        break;

      case 'reset': {
        const project = getCurrentProjectInfo();
        if (resetSession(project?.path)) {
          reply = `✅ 已重置 ${project?.name || '当前项目'} 的会话上下文\n发送消息将开启全新对话`;
        } else {
          reply = '❌ 重置失败，请检查日志';
        }
        break;
      }

      case 'new': {
        if (command.content) {
          reply = await sendMessage(command.content, null, true);
        } else {
          reply = '用法: /new 你的问题\n开启新会话发送消息（不继承历史上下文）';
        }
        break;
      }

      case 'message': {
        reply = await sendMessage(command.content);
        break;
      }

      default:
        reply = '未知命令。发送 /help 查看帮助。';
    }

    await sendLarkMessage(openId, reply);

  } catch (error) {
    console.error('[Event] 处理错误:', error);
    await sendLarkMessage(openId, `❌ 处理出错: ${error.message}`);
  }
}

// 基础配置
const baseConfig = {
  appId: LARK_APP_ID,
  appSecret: LARK_APP_SECRET,
  loggerLevel: Lark.LoggerLevel.info
};

// 创建 SDK 客户端
const client = new Lark.Client(baseConfig);

// 创建 WebSocket 客户端
const wsClient = new Lark.WSClient(baseConfig);

// 启动服务
async function start() {
  console.log('\n🚀 Claude Remote 服务启动中...\n');
  console.log(`📡 长连接模式（使用官方SDK）`);
  console.log(`🔑 App ID: ${LARK_APP_ID}\n`);

  try {
    // 启动 WebSocket 长连接
    wsClient.start({
      eventDispatcher: new Lark.EventDispatcher({}).register({
        'im.message.receive_v1': async (data) => {
          console.log('[SDK] 收到消息事件');
          await handleEvent(data);
        }
      })
    });
    console.log('[WebSocket] ✅ 长连接已启动，等待飞书消息...');
  } catch (error) {
    console.error('启动失败:', error);
    process.exit(1);
  }
}

// 优雅关闭
process.on('SIGINT', () => {
  console.log('\n正在关闭...');
  process.exit(0);
});

start();
