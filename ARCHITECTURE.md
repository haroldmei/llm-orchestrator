# LLM Orchestrator Architecture

## Overview
A multi-agent AI orchestration system for automated feature engineering in BiLSTM deep learning models. The system uses Claude AI agents in an iterative refinement loop to design, review, and fix feature specifications.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Main Entry Point                         │
│                          (main.py)                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator Layer                            │
│              (src/core/orchestrator.py)                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Workflow Control Loop                                   │   │
│  │  • Initialize agents                                     │   │
│  │  • Manage iteration cycles                               │   │
│  │  • Check convergence criteria                            │   │
│  │  • Coordinate agent execution                            │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────┬───────────────┬───────────────┬─────────────────────────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ FE Designer │ │ FE Reviewer │ │  FE Fixer   │
│   Agent     │ │   Agent     │ │   Agent     │
└─────────────┘ └─────────────┘ └─────────────┘
       │               │               │
       └───────────────┴───────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │   BaseAgent (ABC)     │
           │  • Claude API client  │
           │  • Logging            │
           │  • Prompt management  │
           └───────────────────────┘
```

## Component Architecture

### 1. Core Layer (`src/core/`)
**Orchestrator** (`orchestrator.py`)
- Manages the agent lifecycle
- Controls iteration loop (max 5 iterations)
- Evaluates confidence scores (threshold: 90%)
- Coordinates file I/O between agents
- Aggregates results and produces final output

### 2. Agent Layer (`src/agents/`)
All agents inherit from `BaseAgent` which provides:
- Claude API integration
- Logging capabilities
- Prompt template management

**FE Designer** (`fe_designer.py`)
- Input: `data_spec.md`
- Output: `fe_spec.md`
- Purpose: Design initial feature specification using BiLSTM best practices

**FE Reviewer** (`fe_reviewer.py`)
- Input: `fe_spec.md`, `data_spec.md`
- Output: `fe_spec_review.md`, confidence score
- Purpose: Evaluate feature specification quality and completeness
- Produces final spec if confidence ≥ 90%

**FE Fixer** (`fe_fixer.py`)
- Input: `fe_spec.md`, `fe_spec_review.md`, `data_spec.md`
- Output: Updated `fe_spec.md`
- Purpose: Fix issues identified in review

### 3. Utility Layer (`src/utils/`)
**ConfigLoader** (`config_loader.py`)
- Loads YAML configuration
- Merges environment variables
- Provides default configurations

**FileManager** (`file_manager.py`)
- Manages file I/O operations
- Ensures directory structure
- Handles file copying and validation

## Data Flow

```
Input: data_spec.md
      │
      ▼
┌──────────────────┐
│  FE Designer     │──► fe_spec.md (v1)
└──────────────────┘
      │
      ▼
╔═══════════════════════════════════════════╗
║         Iterative Refinement Loop         ║
║                                           ║
║  ┌─────────────────┐                     ║
║  │  FE Reviewer    │──► fe_spec_review.md║
║  │  (+ confidence) │                     ║
║  └─────────────────┘                     ║
║          │                               ║
║          │ [confidence < 90%]            ║
║          ▼                               ║
║  ┌─────────────────┐                     ║
║  │   FE Fixer      │──► fe_spec.md (v2) ║
║  └─────────────────┘                     ║
║          │                               ║
║          └─► (repeat)                    ║
║                                           ║
║  [confidence ≥ 90% OR max iterations]    ║
╚═══════════════════════════════════════════╝
      │
      ▼
Output: fe_spec_final.md
```

## Configuration

### Config File (`config/config.yaml`)
```yaml
anthropic_api_key: ${ANTHROPIC_API_KEY}
model: claude-sonnet-4-20250514
max_iterations: 5
confidence_threshold: 0.9
```

### Prompt Templates (`prompts/`)
- `dl_fe_designer.md`: Feature design instructions
- `dl_fe_reviewer.md`: Review criteria and scoring
- `dl_fe_review_fixer.md`: Fix strategy guidelines

## Directory Structure

```
llm-orchestrator/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── config/
│   └── config.yaml           # Configuration
├── prompts/                  # Agent prompts
│   ├── dl_fe_designer.md
│   ├── dl_fe_reviewer.md
│   └── dl_fe_review_fixer.md
├── src/
│   ├── core/                 # Orchestration logic
│   │   └── orchestrator.py
│   ├── agents/               # AI agents
│   │   ├── base_agent.py
│   │   ├── fe_designer.py
│   │   ├── fe_reviewer.py
│   │   └── fe_fixer.py
│   └── utils/                # Utilities
│       ├── config_loader.py
│       └── file_manager.py
├── data/                     # Input data specs
├── specs/                    # Generated specs
├── logs/                     # Execution logs
└── tests/                    # Unit tests
```

## Design Patterns

### 1. Strategy Pattern
Each agent implements a specific strategy (design/review/fix) through the `BaseAgent` interface.

### 2. Template Method Pattern
`BaseAgent` defines the skeleton of agent operations, with concrete implementations in subclasses.

### 3. Iterator Pattern
Orchestrator implements an iterative refinement loop with convergence criteria.

### 4. Factory Pattern
ConfigLoader provides configuration objects with default values and environment merging.

## Scalability & Extension

### Adding New Agents
1. Inherit from `BaseAgent`
2. Implement `get_prompt_template()` and `execute()`
3. Register in orchestrator workflow

### Modifying Workflow
- Adjust `max_iterations` and `confidence_threshold` in config
- Modify orchestrator loop logic
- Add pre/post-processing steps

### Supporting Other Models
- Create new prompt templates for different architectures
- Update agent logic for model-specific requirements
- Extend configuration schema

## Monitoring & Logging

### Log Files
- `logs/orchestrator.log`: Workflow execution
- `logs/fedesigner.log`: Design agent activity
- `logs/fereviewer.log`: Review agent activity
- `logs/fefixer.log`: Fix agent activity
- `logs/main.log`: Top-level execution

### Metrics
- Iteration count
- Confidence score progression
- API call count
- Execution time

## Best Practices Applied

1. **Separation of Concerns**: Clear boundaries between orchestration, agents, and utilities
2. **Configuration Management**: Externalized configuration with environment variable support
3. **Error Handling**: Structured logging and exception handling
4. **Testability**: Abstract base classes and dependency injection
5. **Extensibility**: Plugin-style agent architecture
6. **Documentation**: Inline comments and architectural documentation
7. **Version Control**: .gitignore for sensitive and generated files
8. **Dependency Management**: Explicit version pinning in requirements.txt

