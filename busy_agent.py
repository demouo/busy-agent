#!/usr/bin/env python3
"""
Busy Agent - 模拟 ReAct Agent 工作过程
从 react-llama 数据集读取 trajectory 并以真实的方式打印
"""

import pandas as pd
import re
import time
import sys
import random
import json
import os
from typing import List, Dict


# ANSI 颜色代码
class Colors:
    """终端颜色代码"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class BusyAgent:
    """模拟忙碌的 ReAct Agent"""

    def __init__(self, dataset_path: str = 'datasets/react-llama.parquet', config_path: str = 'config.json', model: str = None):
        """初始化 Agent"""
        self.df = pd.read_parquet(dataset_path)
        print(f"✓ 加载了 {len(self.df)} 条 trajectory 数据")

        # 加载配置文件
        self.config = self._load_config(config_path)
        print(f"✓ 加载配置文件: {config_path}")

        # 设置模型
        self.model = model or self.config.get('model', {}).get('default', 'qwen-plus')
        self._display_model_info()

    def _load_config(self, config_path: str) -> dict:
        """
        加载配置文件

        Args:
            config_path: 配置文件路径

        Returns:
            配置字典
        """
        # 默认配置
        default_config = {
            "model": {
                "default": "qwen-plus",
                "available_models": {
                    "qwen-flash": {"display_name": "Qwen-Flash", "tier": "flash"},
                    "qwen-plus": {"display_name": "Qwen-Plus", "tier": "plus"},
                    "qwen-max": {"display_name": "Qwen-Max", "tier": "max"}
                }
            },
            "delays": {
                "thinking": {"min": 2.0, "max": 5.0},
                "executing": {"min": 3.0, "max": 6.0}
            },
            "typewriter": {
                "thought_speed": 0.02,
                "action_speed": 0.015,
                "observation_speed": 0.005
            },
            "display": {
                "observation_max_length": 500
            }
        }

        # 尝试加载配置文件
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
            except Exception as e:
                print(f"⚠️  配置文件加载失败，使用默认配置: {e}")
                return default_config
        else:
            print(f"⚠️  配置文件不存在，使用默认配置")
            return default_config

    def _display_model_info(self):
        """显示当前使用的模型信息"""
        models = self.config.get('model', {}).get('available_models', {})
        model_info = models.get(self.model, {})

        if model_info:
            display_name = model_info.get('display_name', self.model)
            tier = model_info.get('tier', 'unknown')

            # 根据模型档位选择颜色
            if tier == 'flash':
                color = Colors.BRIGHT_CYAN
            elif tier == 'plus':
                color = Colors.BRIGHT_GREEN
            elif tier == 'max':
                color = Colors.BRIGHT_MAGENTA
            else:
                color = Colors.WHITE

            print(f"{color}🤖 使用模型: {display_name}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}🤖 使用模型: {self.model}{Colors.RESET}")

    def parse_trajectory(self, trajectory: str) -> List[Dict[str, str]]:
        """
        解析 trajectory 文本，提取 Thought、Action、Observation

        返回格式：[
            {'type': 'thought', 'number': 1, 'content': '...'},
            {'type': 'action', 'number': 1, 'content': '...'},
            {'type': 'observation', 'number': 1, 'content': '...'},
            ...
        ]
        """
        steps = []

        # 使用正则表达式匹配 Thought、Action、Observation
        pattern = r'(Thought|Action|Observation)\s+(\d+):\s*([^\n]+(?:\n(?!(?:Thought|Action|Observation)\s+\d+:)[^\n]+)*)'

        matches = re.finditer(pattern, trajectory, re.MULTILINE)

        for match in matches:
            step_type = match.group(1).lower()
            step_number = int(match.group(2))
            content = match.group(3).strip()

            steps.append({
                'type': step_type,
                'number': step_number,
                'content': content
            })

        return steps

    def typewriter_print(self, text: str, delay: float = 0.03, end: str = '\n'):
        """
        打字机效果打印文本

        Args:
            text: 要打印的文本
            delay: 每个字符的延迟时间（秒）
            end: 结束字符
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(end)
        sys.stdout.flush()

    def loading_animation(self, message: str, duration: float = 2.0):
        """
        显示加载动画

        Args:
            message: 加载消息
            duration: 动画持续时间（秒）
        """
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                sys.stdout.write(f'\r{frame} {message}')
                sys.stdout.flush()
                time.sleep(0.1)
                if time.time() >= end_time:
                    break

        sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r')
        sys.stdout.flush()

    def print_step(self, step: Dict[str, str], fast_mode: bool = False):
        """
        打印单个步骤

        Args:
            step: 步骤字典 {'type': 'thought/action/observation', 'number': 1, 'content': '...'}
            fast_mode: 是否快速模式（跳过动画）
        """
        step_type = step['type']
        step_number = step['number']
        content = step['content']

        if step_type == 'thought':
            # 思考步骤
            if not fast_mode:
                thinking_min = self.config['delays']['thinking']['min']
                thinking_max = self.config['delays']['thinking']['max']
                self.loading_animation('思考中...', duration=random.uniform(thinking_min, thinking_max))

            prefix = f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}💭 Thought {step_number}:{Colors.RESET} "
            print(prefix, end='')

            if not fast_mode:
                thought_speed = self.config['typewriter']['thought_speed']
                self.typewriter_print(content, delay=thought_speed)
            else:
                print(content)

        elif step_type == 'action':
            # 动作步骤
            prefix = f"{Colors.BOLD}{Colors.BRIGHT_GREEN}⚡ Action {step_number}:{Colors.RESET} "
            print(prefix, end='')

            if not fast_mode:
                action_speed = self.config['typewriter']['action_speed']
                self.typewriter_print(content, delay=action_speed)
            else:
                print(content)

            # 执行动作后的延迟
            if not fast_mode:
                executing_min = self.config['delays']['executing']['min']
                executing_max = self.config['delays']['executing']['max']
                self.loading_animation('执行中...', duration=random.uniform(executing_min, executing_max))

        elif step_type == 'observation':
            # 观察步骤
            prefix = f"{Colors.BRIGHT_CYAN}📊 Observation {step_number}:{Colors.RESET} "
            print(prefix, end='')

            # Observation 通常很长，截断显示
            max_length = self.config['display']['observation_max_length']
            if len(content) > max_length and not fast_mode:
                display_content = content[:max_length] + '...'
            else:
                display_content = content

            if not fast_mode:
                observation_speed = self.config['typewriter']['observation_speed']
                self.typewriter_print(display_content, delay=observation_speed)
            else:
                print(display_content)

            print()  # 空行分隔

    def run(self, index: int = None, fast_mode: bool = False):
        """
        运行 Agent，显示一个 trajectory

        Args:
            index: 指定要显示的 trajectory 索引，None 表示随机选择
            fast_mode: 是否快速模式（跳过动画）
        """
        # 选择一个 trajectory
        if index is None:
            index = random.randint(0, len(self.df) - 1)

        row = self.df.iloc[index]
        question = row['question']
        correct_answer = row['correct_answer']
        trajectory = row['trajectory']

        # 显示标题
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{'=' * 80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🤖 ReAct Agent 工作中...{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{'=' * 80}{Colors.RESET}\n")

        # 显示问题
        print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}❓ 问题:{Colors.RESET}")
        print(f"{Colors.WHITE}{question}{Colors.RESET}\n")

        # 解析 trajectory
        steps = self.parse_trajectory(trajectory)

        if not steps:
            print(f"{Colors.RED}错误: 无法解析 trajectory{Colors.RESET}")
            return

        # 逐步打印
        print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}🔄 开始推理过程...{Colors.RESET}\n")

        for step in steps:
            self.print_step(step, fast_mode=fast_mode)

        # 显示最终答案
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_GREEN}{'=' * 80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}✅ 最终答案: {correct_answer}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}{'=' * 80}{Colors.RESET}\n")


def main():
    """主程序入口"""
    import argparse

    parser = argparse.ArgumentParser(description='Busy Agent - 模拟 ReAct Agent 工作过程')
    parser.add_argument('--index', type=int, default=None, help='指定要显示的 trajectory 索引')
    parser.add_argument('--fast', action='store_true', help='快速模式（跳过动画）')
    parser.add_argument('--loop', action='store_true', help='循环模式（持续显示随机 trajectory）')
    parser.add_argument('--delay', type=float, default=3.0, help='循环模式下每次之间的延迟（秒）')
    parser.add_argument('--model', type=str, default=None,
                        choices=['qwen-flash', 'qwen-plus', 'qwen-max'],
                        help='选择模型：qwen-flash（快速）、qwen-plus（平衡）、qwen-max（最强）')

    args = parser.parse_args()

    # 创建 Agent
    agent = BusyAgent(model=args.model)

    if args.loop:
        # 循环模式
        print(f"{Colors.BRIGHT_CYAN}🔄 循环模式已启动，按 Ctrl+C 退出{Colors.RESET}\n")
        try:
            while True:
                agent.run(fast_mode=args.fast)
                time.sleep(args.delay)
        except KeyboardInterrupt:
            print(f"\n{Colors.BRIGHT_YELLOW}👋 已退出{Colors.RESET}")
    else:
        # 单次运行
        agent.run(index=args.index, fast_mode=args.fast)


if __name__ == '__main__':
    main()
