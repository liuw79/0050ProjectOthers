/**
 * 命令解析模块
 */

export function parseCommand(text) {
  const trimmed = text.trim();

  // 检查是否是命令（以 / 开头）
  if (!trimmed.startsWith('/')) {
    return { type: 'message', content: trimmed };
  }

  const parts = trimmed.slice(1).split(/\s+/);
  const cmd = parts[0].toLowerCase();
  const args = parts.slice(1);

  switch (cmd) {
    case 'status':
      return { type: 'status' };

    case 'projects':
    case 'list':
      return { type: 'projects' };

    case 'history':
      return { type: 'history', count: parseInt(args[0]) || 20 };

    case 'help':
    case '?':
      return { type: 'help' };

    case 'wake':
      return { type: 'wake' };

    case 'reset':
      return { type: 'reset' };

    case 'new':
      return { type: 'new', content: args.join(' ') };

    default:
      // 检查是否是项目缩写
      return { type: 'switch', project: cmd };
  }
}

export function getHelpText() {
  return `🤖 Claude Remote 帮助

📚 命令列表:
• /kb, /gc, /ts 等 - 切换到对应项目
• /目录名 - 直接切换到任意目录
• /status - 查看当前项目状态
• /projects - 列出所有可用项目
• /reset - 重置当前项目会话（清除历史上下文）
• /new 问题 - 开启新会话提问（不继承历史）
• /history [数量] - 查看历史记录
• /help - 显示此帮助

💬 使用方式:
直接发送文字即可与 Claude 对话

📝 示例:
• /kb              → 切换到知识库项目
• /Tool.DeepSeek   → 直接切换到该目录
• /reset           → 清除当前项目的历史上下文
• /new 你好        → 开启新会话对话
• 你好 Claude      → 继续当前会话对话`;
}
