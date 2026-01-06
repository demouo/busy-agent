# Busy Agent 🤖

在 LLM Agent 时代假装很忙！

这是一个有趣的项目，通过读取 react-llama 数据集的 trajectory，以 ReAct Agent 的风格逐步打印 Agent 的思考和执行过程，让你看起来像是在运行一个真实的 AI Agent。

## 特性

- 🎨 **彩色输出**: 使用 ANSI 颜色代码，让输出更加美观
- ⌨️ **打字机效果**: 逐字符打印，模拟真实的思考过程
- ⏳ **加载动画**: 显示"思考中..."、"执行中..."等动画效果
- 🔄 **ReAct 风格**: 完整展示 Thought → Action → Observation 的推理循环
- 🎲 **随机选择**: 从 3538 条 trajectory 中随机选择展示
- 🚀 **多种模式**: 支持快速模式、循环模式等

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

运行程序，随机显示一个 trajectory：

```bash
python busy_agent.py
```

### 快速模式

跳过动画效果，快速显示（适合测试）：

```bash
python busy_agent.py --fast
```

### 指定索引

显示特定索引的 trajectory：

```bash
python busy_agent.py --index 0
```

### 循环模式

持续显示随机 trajectory，假装一直在忙：

```bash
python busy_agent.py --loop
```

自定义循环间隔时间（秒）：

```bash
python busy_agent.py --loop --delay 5.0
```

## 配置文件

程序使用 `config.json` 配置文件来管理延迟时间和显示参数。你可以根据需要调整这些参数来控制 Agent 的"忙碌"程度。

### 配置项说明

**延迟时间配置** (`delays`):
- `thinking.min` / `thinking.max`: 思考延迟时间范围（秒），默认 2.0-5.0 秒
- `executing.min` / `executing.max`: 执行动作延迟时间范围（秒），默认 3.0-6.0 秒

**打字机效果配置** (`typewriter`):
- `thought_speed`: 思考内容的打字速度（每字符延迟），默认 0.02 秒
- `action_speed`: 动作内容的打字速度，默认 0.015 秒
- `observation_speed`: 观察内容的打字速度，默认 0.005 秒

**显示配置** (`display`):
- `observation_max_length`: 观察内容的最大显示长度，默认 500 字符

### 配置示例

```json
{
  "delays": {
    "thinking": {
      "min": 2.0,
      "max": 5.0
    },
    "executing": {
      "min": 3.0,
      "max": 6.0
    }
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
```

## 输出示例

程序会以 ReAct 风格输出 Agent 的推理过程：

```
🤖 ReAct Agent 工作中...
================================================================================

❓ 问题:
Since 2017 Nick Ayers has been Chief of Staff to a man that served as governor of what state?

🔄 开始推理过程...

💭 Thought 1: I need to search Nick Ayers, find who he is chief of staff to...
⚡ Action 1: Search[Nick Ayers]
📊 Observation 1: James Nicholas Ayers (born August 16, 1982) is an American...

💭 Thought 2: Nick Ayers is chief of staff to Mike Pence...
⚡ Action 2: Search[Mike Pence]
📊 Observation 2: Michael Richard Pence (born June 7, 1959) is an American...

💭 Thought 3: Mike Pence was governor of Indiana...
⚡ Action 3: Finish[Indiana]

✅ 最终答案: Indiana
```

## 项目结构

```
busy-agent/
├── busy_agent.py          # 主程序
├── config.json            # 配置文件（延迟时间、打字速度等）
├── datasets/
│   └── react-llama.parquet  # ReAct trajectory 数据集
├── explore_dataset.py     # 数据集探索脚本
├── view_trajectory.py     # 查看 trajectory 示例
├── requirements.txt       # Python 依赖
└── README.md             # 项目说明
```

## 数据集

项目使用 react-llama 数据集，包含 3538 条 ReAct 风格的 trajectory。每条数据包括：
- **question**: 问题
- **correct_answer**: 正确答案
- **trajectory**: 完整的推理过程（Thought → Action → Observation）

## 技术实现

- **解析**: 使用正则表达式解析 trajectory 文本
- **打字机效果**: 逐字符打印，模拟真实输入
- **加载动画**: 使用 Unicode 字符创建旋转动画
- **颜色输出**: ANSI 转义序列实现彩色终端输出

## 许可证

MIT License
