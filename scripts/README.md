# Orchestrator Scripts

Helper scripts for the LLM orchestrator system.

## Scripts

### `run_reviewer.py`
Run only the reviewer agent on an existing feature specification.

```bash
python scripts/run_reviewer.py --fe-spec specs/fe_spec.md --data-spec data/data_spec.md
```

### `compare_specs.py`
Generate a comparison report between two specification files.

```bash
python scripts/compare_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md --output comparison_report.md
```

### `merge_specs.py`
Merge specifications with backup and confirmation.

```bash
python scripts/merge_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md
```

Add `--force` to skip confirmation prompts (use in automation).

## GitHub Workflows

### Monitor Data Spec (`monitor-data-spec.yml`)
- **Trigger:** Changes to `data/data_spec.md`
- **Action:** Run full pipeline (Designer → Reviewer → Fixer)
- **Output:** Creates PR with generated specs

### Monitor FE Spec (`monitor-fe-spec.yml`)
- **Trigger:** Changes to `specs/fe_spec.md`
- **Action:** Run reviewer pipeline (Reviewer → Fixer)
- **Output:** Creates PR with review results

### Compare and Merge (`compare-and-merge.yml`)
- **Trigger:** Manual workflow dispatch
- **Action:** Compare specs and optionally merge
- **Options:**
  - Source file selection
  - Target file selection
  - Auto-merge or create PR

## Usage Examples

### Local Development

1. **Run full pipeline:**
```bash
python main.py --data-spec data/data_spec.md
```

2. **Run only reviewer:**
```bash
python scripts/run_reviewer.py --fe-spec specs/fe_spec.md --data-spec data/data_spec.md
```

3. **Compare and merge manually:**
```bash
python scripts/compare_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md
python scripts/merge_specs.py --source specs/fe_spec_review.md --target specs/fe_spec.md
```

### GitHub Actions

1. **Auto-trigger on push:**
   - Push changes to `data/data_spec.md` → Runs designer pipeline
   - Push changes to `specs/fe_spec.md` → Runs reviewer pipeline

2. **Manual merge workflow:**
   - Go to Actions → "Compare and Merge Specs"
   - Click "Run workflow"
   - Select source and target files
   - Choose auto-merge or create PR

## Setup

### Required Secrets

Add these secrets to your GitHub repository:

- `ANTHROPIC_API_KEY` - Your Anthropic API key for Claude

### Repository Setup

1. Enable GitHub Actions in your repository settings
2. Ensure workflows have write permissions:
   - Settings → Actions → General → Workflow permissions → "Read and write permissions"

## Workflow Outputs

All workflows generate artifacts you can download:
- Generated specifications
- Review results
- Comparison reports
- Logs

Access artifacts from the Actions tab → Select workflow run → Artifacts section.

