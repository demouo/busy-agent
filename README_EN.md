# Busy Agent 🤖

Pretend to be busy in the LLM Agent era!

This is a fun project that reads trajectories from the react-llama dataset and prints the Agent's thinking and execution process in ReAct Agent style, making you look like you're running a real AI Agent.

## Features

- 🎨 **Colorful Output**: Uses ANSI color codes for beautiful terminal output
- ⌨️ **Typewriter Effect**: Character-by-character printing to simulate real thinking process
- ⏳ **Loading Animations**: Displays "Thinking...", "Executing..." and other animation effects
- 🔄 **ReAct Style**: Complete display of Thought → Action → Observation reasoning loop
- 🎲 **Random Selection**: Randomly selects from 3538 trajectories for display
- 🚀 **Multiple Modes**: Supports fast mode, loop mode, and more
- 🎯 **Smart Answer Generation**: Intelligently generates correct or incorrect answers based on configured success rate and incident events
- 🤖 **LLM as Judge**: Simulates LLM scoring system to evaluate answer quality
- 📊 **Observable Metrics**: Real-time display of success rate, time spent, step count, incidents, and other key metrics
- 🌍 **Multi-language Support**: Supports Chinese and English interface switching

## Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install busy-agent
```

After installation, you can directly use the `busy-agent` command.

### Method 2: Install from Source

```bash
git clone https://github.com/demouo/busy-agent.git
cd busy-agent
pip install -e .
```

### Method 3: Development Mode

If you want to modify the code or contribute:

```bash
git clone https://github.com/demouo/busy-agent.git
cd busy-agent
pip install -r requirements.txt
python busy_agent.py  # Run script directly
```

## Usage

### Basic Usage

Run the program to continuously display random trajectories (loop mode by default):

```bash
busy-agent
```

### Fast Mode

Skip animation effects for quick display (suitable for testing):

```bash
busy-agent --fast
```

### Single Run Mode

Display a single trajectory and exit:

```bash
busy-agent --once
```

### Specify Index

Display a specific trajectory by index (automatically enters single run mode):

```bash
busy-agent --index 0
```

### Loop Mode Settings

Customize the delay between loops (seconds):

```bash
busy-agent --delay 5.0
```

### Model Selection

Choose different AI models (similar to Claude's three-tier model system):

**qwen-flash** (Fast model):
```bash
busy-agent --model qwen-flash
```

**qwen-plus** (Balanced model, default):
```bash
busy-agent --model qwen-plus
```

**qwen-max** (Most powerful model):
```bash
busy-agent --model qwen-max
```

The program displays the current model at startup, with different models distinguished by different colors.

### Language Selection

Switch between Chinese and English interface:

```bash
busy-agent --language en  # English
busy-agent --language zh  # Chinese
```

## Configuration File

The program uses the `config.json` configuration file to manage delay times and display parameters. You can adjust these parameters to control the Agent's "busyness" level.

### Configuration Options

**Language Configuration** (`language`):
- `default`: Default language, options: `zh` (Chinese) or `en` (English)

**Model Configuration** (`model`):
- `default`: Default model, options: `qwen-flash`, `qwen-plus`, `qwen-max`
- `available_models`: List of available models and their configurations

**Delay Time Configuration** (`delays`):
- `thinking.min` / `thinking.max`: Thinking delay time range (seconds), default 4.0-10.0 seconds
- `executing.min` / `executing.max`: Action execution delay time range (seconds), default 6.0-12.0 seconds

**Typewriter Effect Configuration** (`typewriter`):
- `thought_speed`: Typing speed for thought content (delay per character), default 0.02 seconds
- `action_speed`: Typing speed for action content, default 0.015 seconds
- `observation_speed`: Typing speed for observation content, default 0.005 seconds

**Display Configuration** (`display`):
- `observation_max_length`: Maximum display length for observation content, default 500 characters

**Print Mode Configuration** (`print_modes`):
- `switch_interval`: Switch print mode every N steps, default 10 steps
- `modes`: Available print modes (smooth, chunky, slow, instant)

**Incident Configuration** (`incidents`):
- `model_disconnect`: Model disconnection configuration
  - `enabled`: Whether to enable, default true
  - `probability`: Trigger probability, default 0.03 (3%)
  - `max_retries`: Maximum retry count, default 8
- `action_timeout`: Action timeout configuration
  - `enabled`: Whether to enable, default true
  - `probability`: Trigger probability, default 0.02 (2%)
  - `max_retries`: Maximum retry count, default 8

**Success Rate Configuration** (`success_rate`):
- `target_rate`: Target success rate, default 0.60 (60%)
- `incident_penalty`: Incident penalty coefficient, default 0.3 (increases failure probability by 30% when incidents occur)
- `wrong_answer_strategies`: Wrong answer generation strategies
  - `unable_to_determine`: Unable to determine type answers (weight 0.4)
  - `reasoning_failed`: Reasoning failed type answers (weight 0.3)
  - `wrong_guess`: Random wrong answers (weight 0.3)

**LLM Scoring Configuration** (`llm_judge`):
- `enabled`: Whether to enable LLM as Judge scoring, default true
- `correct_answer_score`: Correct answer score range, default 8.5-10.0
- `wrong_answer_score`: Wrong answer score range, default 2.0-6.0

**Metrics Tracking Configuration** (`metrics`):
- `track_success_rate`: Whether to track success rate, default true
- `track_time`: Whether to track time spent, default true
- `track_steps`: Whether to track step count, default true
- `track_retries`: Whether to track retry count, default true
- `track_incidents`: Whether to track incident events, default true

## Output Example

The program outputs the Agent's reasoning process in ReAct style:

```
🤖 ReAct Agent Working...
================================================================================

❓ Question:
Since 2017 Nick Ayers has been Chief of Staff to a man that served as governor of what state?

🔄 Starting reasoning process...

💭 Thought 1: I need to search Nick Ayers, find who he is chief of staff to...
⚡ Action 1: Search[Nick Ayers]
📊 Observation 1: James Nicholas Ayers (born August 16, 1982) is an American...

💭 Thought 2: Nick Ayers is chief of staff to Mike Pence...
⚡ Action 2: Search[Mike Pence]
📊 Observation 2: Michael Richard Pence (born June 7, 1959) is an American...

💭 Thought 3: Mike Pence was governor of Indiana...
⚡ Action 3: Finish[Indiana]

✅ Final Answer: Indiana
================================================================================

📊 Observable Metrics:

🤖 LLM as Judge Score: 9.27/10.0
✅ Overall Success Rate: 100.0% (1/1)
⏱️  Time Spent: 45.32s
📝 Total Steps: 8
```

## Project Structure

```
busy-agent/
├── busy_agent/           # Package directory
│   ├── __init__.py      # Package initialization
│   ├── agent.py         # Core BusyAgent class
│   ├── cli.py           # CLI entry point
│   └── data/            # Data files
│       ├── config.json
│       └── datasets/
│           └── react-llama.parquet
├── setup.py             # Packaging configuration
├── MANIFEST.in          # Data file manifest
├── README.md            # Chinese documentation
├── README_EN.md         # English documentation
├── requirements.txt     # Python dependencies
└── LICENSE              # License file
```

## Dataset

The project uses the react-llama dataset, containing 3538 ReAct-style trajectories. Each data entry includes:
- **question**: Question
- **correct_answer**: Correct answer
- **trajectory**: Complete reasoning process (Thought → Action → Observation)

## Technical Implementation

- **Parsing**: Uses regular expressions to parse trajectory text
- **Typewriter Effect**: Character-by-character printing to simulate real input
- **Loading Animation**: Uses Unicode characters to create rotating animations
- **Color Output**: ANSI escape sequences for colorful terminal output
- **Smart Answer Generation**: Probabilistic determination based on success rate and incidents
- **LLM as Judge**: Simulated scoring system with realistic score ranges
- **Observable Metrics**: Real-time tracking and display of key performance indicators

## License

MIT License

---

**Note**: This project is for entertainment and demonstration purposes. It simulates an AI Agent's working process to make your terminal look busy and professional.

For more information, visit: https://github.com/demouo/busy-agent
