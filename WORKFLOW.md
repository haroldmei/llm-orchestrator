# Feature Engineering Workflow

## Detailed Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Initiates                            │
│                   python main.py --data-spec                      │
│                      data/data_spec.md                            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Load Configuration  │
                  │  • API credentials   │
                  │  • Model settings    │
                  │  • Thresholds        │
                  └──────────┬───────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  Initialize Orchestrator     │
              │  • Create agent instances    │
              │  • Setup logging             │
              │  • Validate inputs           │
              └──────────┬───────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                       STEP 1: DESIGN                           │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │             FE Designer Agent                          │   │
│  │                                                        │   │
│  │  Input:  data/data_spec.md                            │   │
│  │  Prompt: prompts/dl_fe_designer.md                    │   │
│  │                                                        │   │
│  │  Actions:                                             │   │
│  │  1. Read data specification                           │   │
│  │  2. Apply BiLSTM best practices                       │   │
│  │  3. Design feature transformations                    │   │
│  │  4. Create normalization strategy                     │   │
│  │  5. Define sequence parameters                        │   │
│  │                                                        │   │
│  │  Output: specs/fe_spec.md                             │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
╔══════════════════════════════════════════════════════════════════╗
║                 ITERATIVE REFINEMENT LOOP                        ║
║                   (Max 5 iterations)                             ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐  ║
║  │                  STEP 2: REVIEW                          │  ║
║  │                                                          │  ║
║  │  ┌────────────────────────────────────────────────┐     │  ║
║  │  │         FE Reviewer Agent                      │     │  ║
║  │  │                                                │     │  ║
║  │  │  Input:  specs/fe_spec.md                     │     │  ║
║  │  │          data/data_spec.md                     │     │  ║
║  │  │  Prompt: prompts/dl_fe_reviewer.md            │     │  ║
║  │  │                                                │     │  ║
║  │  │  Actions:                                     │     │  ║
║  │  │  1. Validate completeness                     │     │  ║
║  │  │  2. Check technical correctness               │     │  ║
║  │  │  3. Assess BiLSTM suitability                 │     │  ║
║  │  │  4. Evaluate best practices                   │     │  ║
║  │  │  5. Calculate confidence score                │     │  ║
║  │  │                                                │     │  ║
║  │  │  Output: specs/fe_spec_review.md              │     │  ║
║  │  │          confidence_score (float)             │     │  ║
║  │  └────────────────────────────────────────────────┘     │  ║
║  └──────────────────────────┬───────────────────────────────┘  ║
║                             │                                  ║
║                             ▼                                  ║
║                  ┌──────────────────────┐                      ║
║                  │  Evaluate Score      │                      ║
║                  │  Threshold: 90%      │                      ║
║                  └──────┬───────┬───────┘                      ║
║                         │       │                              ║
║        ┌────────────────┘       └──────────────────┐           ║
║        │ Score ≥ 90%                    Score < 90%│           ║
║        ▼                                           ▼           ║
║  ┌──────────────┐                    ┌────────────────────┐   ║
║  │ SUCCESS!     │                    │  STEP 3: FIX       │   ║
║  │ Create final │                    │                    │   ║
║  │ spec file    │                    │  ┌──────────────┐  │   ║
║  │              │                    │  │  FE Fixer    │  │   ║
║  └──────┬───────┘                    │  │  Agent       │  │   ║
║         │                            │  │              │  │   ║
║         │                            │  │  Input:      │  │   ║
║         │                            │  │  • fe_spec   │  │   ║
║         │                            │  │  • review    │  │   ║
║         │                            │  │  • data_spec │  │   ║
║         │                            │  │              │  │   ║
║         │                            │  │  Actions:    │  │   ║
║         │                            │  │  1. Parse    │  │   ║
║         │                            │  │  2. Fix      │  │   ║
║         │                            │  │  3. Update   │  │   ║
║         │                            │  │              │  │   ║
║         │                            │  │  Output:     │  │   ║
║         │                            │  │  Updated     │  │   ║
║         │                            │  │  fe_spec.md  │  │   ║
║         │                            │  └──────┬───────┘  │   ║
║         │                            └─────────┼──────────┘   ║
║         │                                      │              ║
║         │                                      │              ║
║         │                 ┌────────────────────┘              ║
║         │                 │ Increment iteration               ║
║         │                 │ Check max iterations              ║
║         │                 │                                   ║
║         │                 └──► LOOP BACK TO STEP 2            ║
║         │                                                     ║
╚═════════┼═════════════════════════════════════════════════════╝
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Final Output                             │
│                                                             │
│  IF confidence ≥ 90%:                                       │
│    ✓ specs/fe_spec_final.md                                │
│    ✓ Status: SUCCESS                                       │
│                                                             │
│  IF max iterations reached:                                │
│    ⚠ specs/fe_spec.md (best attempt)                       │
│    ⚠ Status: INCOMPLETE                                    │
│                                                             │
│  Metadata:                                                 │
│    • Total iterations                                      │
│    • Final confidence score                                │
│    • Execution logs                                        │
└─────────────────────────────────────────────────────────────┘
```

## State Transitions

```
[START] ──► [DESIGN] ──► [REVIEW] ──┬──► [SUCCESS] ──► [END]
                           │         │
                           └──► [FIX]┘
                                ▲  │
                                └──┘
                          (iterate max 5×)
```

## Convergence Criteria

1. **Success Case**: `confidence_score >= 0.9`
   - Final spec written to `fe_spec_final.md`
   - Pipeline terminates successfully

2. **Max Iterations**: `iteration >= 5`
   - Best attempt in `fe_spec.md`
   - Pipeline terminates with warning

## File Lifecycle

```
data_spec.md (immutable)
    │
    ├──► fe_spec.md (v1) ──► fe_spec.md (v2) ──► ... ──► fe_spec.md (vN)
    │                                                          │
    │                                                          ▼
    └──────────────────────────────────────────────► fe_spec_final.md

Reviews: fe_spec_review.md (updated each iteration)
```

## Error Handling

- **API Failures**: Logged and raised with context
- **Missing Files**: Validated before execution
- **Invalid Config**: Defaults applied with warnings
- **Parsing Errors**: Logged, confidence defaults to 0.5

## Logging Strategy

Each component logs to separate files:
- `orchestrator.log`: Workflow control
- `fedesigner.log`: Design operations
- `fereviewer.log`: Review operations  
- `fefixer.log`: Fix operations
- `main.log`: Top-level execution

All logs include:
- Timestamp
- Component name
- Log level
- Message with context

