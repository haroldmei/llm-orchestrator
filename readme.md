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

## GitHub Workflows

Automated CI/CD pipelines for spec generation and review:

### 1. Monitor Data Spec
**Trigger:** Changes to `data/data_spec.md`
- Runs full pipeline (Designer → Reviewer → Fixer)
- Creates PR with generated specs

### 2. Monitor FE Spec
**Trigger:** Changes to `specs/fe_spec.md`
- Runs reviewer pipeline
- Creates PR with review results

### 3. Compare and Merge
**Trigger:** Manual workflow dispatch
- Compare `fe_spec_review.md` and `fe_spec.md`
- Option to auto-merge or create PR

**Setup:**
1. Add `ANTHROPIC_API_KEY` secret to GitHub repository
2. Enable Actions with write permissions

See [scripts/README.md](scripts/README.md) for detailed workflow documentation.

## Helper Scripts

```bash
# Run reviewer only
python scripts/run_reviewer.py --fe-spec specs/fe_spec.md --data-spec data/data_spec.md

# Compare specs
python scripts/compare_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md

# Merge specs (with backup and confirmation)
python scripts/merge_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md
```

## Development

```bash
# Run tests
pytest tests/

# Format code
black src/ tests/

# Type check
mypy src/
```
