# LLM Orchestrator for Feature Engineering

An intelligent multi-agent orchestration system that automates feature engineering for BiLSTM deep learning models using LLM APIs (DeepSeek, Claude).

## Overview

This system uses three specialized AI agents in an iterative refinement loop to design, review, and perfect feature specifications:

1. **FE Designer**: Designs initial feature specifications from data specs
2. **FE Reviewer**: Reviews and scores feature quality (target: 90%+ confidence)
3. **FE Fixer**: Fixes issues identified in reviews

The agents iterate until achieving 90%+ confidence or max iterations (5).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (DeepSeek is default)
export DEEPSEEK_API_KEY=your_key_here

# Or for Claude
# export ANTHROPIC_API_KEY=your_key_here

# Run pipeline
python main.py --data-spec data/data_spec_example.md
```

## Project Structure

```
llm-orchestrator/
├── main.py                   # Entry point
├── config/                   # Configuration
├── prompts/                  # Agent prompts
├── src/
│   ├── core/                # Orchestration logic
│   ├── agents/              # AI agents
│   └── utils/               # Utilities
├── data/                    # Input specs
├── specs/                   # Generated specs
└── tests/                   # Unit tests
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design, component descriptions, and data flow diagrams.

## Configuration

Edit `config/config.yaml`:
```yaml
provider: deepseek              # "deepseek" or "anthropic"
model: deepseek-chat            # or "claude-sonnet-4-20250514"
max_iterations: 5
confidence_threshold: 0.9
reviewer_type: robust           # "default", "robust", or "structured"
```

### Supported Providers

- **DeepSeek** (default): Set `DEEPSEEK_API_KEY` environment variable
- **Anthropic Claude**: Set `ANTHROPIC_API_KEY` environment variable

Switch providers by updating the `provider` and `model` fields in `config.yaml`.

## Development

```bash
# Run tests
pytest tests/

# Format code
black src/ tests/

# Type check
mypy src/
```
