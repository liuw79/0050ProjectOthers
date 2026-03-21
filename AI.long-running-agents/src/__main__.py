#!/usr/bin/env python3
"""
简化的命令入口 - 支持自然语言
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.commands.ask import ask
from src.cli import main
from click.testing import CliRunner


def is_natural_language(arg: str) -> bool:
    """判断是否是自然语言描述（而不是命令）"""
    commands = ['init', 'status', 'coder', 'initializer', 'dashboard', 'ask', '--help', '-h', '--version']

    # 如果是已知命令
    if arg in commands or arg.startswith('-'):
        return False

    # 包含中文或空格，很可能是自然语言
    if any('\u4e00' <= c <= '\u9fff' for c in arg) or ' ' in arg:
        return True

    # 以字母开头但包含描述性词语
    descriptive_words = ['create', 'build', 'make', 'help', 'api', 'app', 'project', 'system']
    if any(word in arg.lower() for word in descriptive_words):
        return True

    return False


def run():
    """主入口"""
    args = sys.argv[1:]

    if not args:
        # 无参数，显示帮助
        main(['--help'])
    elif len(args) == 1 and is_natural_language(args[0]):
        # 单个自然语言参数，直接当作请求处理
        runner = CliRunner()
        result = runner.invoke(ask, [args[0]])
        print(result.output)
    else:
        # 否则走正常命令流程
        main()


if __name__ == '__main__':
    run()
