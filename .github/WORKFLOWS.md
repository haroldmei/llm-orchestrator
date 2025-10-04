# GitHub Workflows Guide

## Overview

Three automated workflows for orchestrating feature engineering spec generation and review.

## Workflows

### 1. Monitor Data Spec

**File:** `.github/workflows/monitor-data-spec.yml`

**Purpose:** Automatically run the full pipeline when data specifications change.

**Triggers:**
- Push to `data/data_spec.md`
- PR modifying `data/data_spec.md`
- Manual dispatch

**Process:**
1. Detects changes to `data/data_spec.md`
2. Runs full pipeline: Designer → Reviewer → Fixer
3. Generates:
   - `specs/fe_spec.md` (initial design)
   - `specs/fe_spec_review.md` (review feedback)
   - `specs/fe_spec_final.md` (fixed version)
4. Creates PR with generated specs

**Usage:**
```bash
git add data/data_spec.md
git commit -m "Update data specification"
git push
```

### 2. Monitor FE Spec

**File:** `.github/workflows/monitor-fe-spec.yml`

**Purpose:** Review and improve feature specs when manually edited.

**Triggers:**
- Push to `specs/fe_spec.md`
- PR modifying `specs/fe_spec.md`
- Manual dispatch

**Process:**
1. Detects changes to `specs/fe_spec.md`
2. Runs reviewer pipeline: Reviewer → Fixer
3. Generates:
   - `specs/fe_spec_review.md` (review)
   - `specs/fe_spec_final.md` (improved version)
4. Creates PR with review results

**Usage:**
```bash
# Manually edit specs/fe_spec.md
git add specs/fe_spec.md
git commit -m "Manual improvements to FE spec"
git push
```

### 3. Compare and Merge

**File:** `.github/workflows/compare-and-merge.yml`

**Purpose:** Review differences and merge reviewed specs back into main spec.

**Triggers:**
- Manual workflow dispatch only

**Process:**
1. Compare selected source and target files
2. Generate detailed comparison report
3. Either:
   - Auto-merge (if `auto_merge: true`)
   - Create PR for manual review

**Usage:**

Via GitHub UI:
1. Go to Actions → "Compare and Merge Specs"
2. Click "Run workflow"
3. Configure:
   - **Source file:** `specs/fe_spec_final.md` or `specs/fe_spec_review.md`
   - **Target file:** `specs/fe_spec.md`
   - **Auto merge:** `true` (direct merge) or `false` (create PR)
4. Click "Run workflow"

Via GitHub CLI:
```bash
gh workflow run compare-and-merge.yml \
  -f source_file=specs/fe_spec_final.md \
  -f target_file=specs/fe_spec.md \
  -f auto_merge=false
```

## Workflow Outputs

### Artifacts

All workflows produce downloadable artifacts:
- Generated specification files
- Review results
- Comparison reports
- Execution logs

**Access artifacts:**
1. Go to Actions tab
2. Select workflow run
3. Scroll to Artifacts section
4. Download ZIP files

### Pull Requests

Workflows automatically create PRs with:
- Descriptive titles and bodies
- Links to artifacts
- Pipeline execution details
- Automatic labels

## Setup

### Prerequisites

1. **GitHub Secrets:**
   ```
   Repository Settings → Secrets and variables → Actions → New repository secret
   ```
   Add: `ANTHROPIC_API_KEY` with your Anthropic API key

2. **Workflow Permissions:**
   ```
   Repository Settings → Actions → General → Workflow permissions
   ```
   Enable: "Read and write permissions"

3. **Required Files:**
   - `data/data_spec.md` - Must exist for designer workflow
   - `config/config.yaml` - Configuration file
   - `requirements.txt` - Python dependencies

### First-Time Setup

```bash
mkdir -p .github/workflows data specs logs scripts
touch data/data_spec.md

git add .github/ scripts/
git commit -m "Add GitHub workflows and scripts"
git push
```

## Common Workflows

### Scenario 1: New Data Spec

```bash
vi data/data_spec.md
git add data/data_spec.md
git commit -m "Add initial data specification"
git push
```

Result:
- Workflow "Monitor Data Spec" triggers
- Full pipeline runs
- PR created with all generated specs
- Review PR and merge when ready

### Scenario 2: Manual FE Spec Edit

```bash
vi specs/fe_spec.md
git add specs/fe_spec.md
git commit -m "Add custom features"
git push
```

Result:
- Workflow "Monitor FE Spec" triggers
- Reviewer evaluates your changes
- PR created with review feedback
- Review suggestions and merge fixes

### Scenario 3: Accept Reviewed Spec

1. Previous workflows completed, `fe_spec_final.md` exists
2. Go to Actions → "Compare and Merge Specs"
3. Run workflow:
   - Source: `specs/fe_spec_final.md`
   - Target: `specs/fe_spec.md`
   - Auto merge: `false`
4. Review comparison report in artifacts
5. Review PR and merge to accept changes

## Local Development

Test workflows locally using `act`:

```bash
# Install act
brew install act  # macOS
# or: https://github.com/nektos/act

# Test monitor-data-spec workflow
act push -W .github/workflows/monitor-data-spec.yml

# Test with secrets
act push -W .github/workflows/monitor-data-spec.yml -s ANTHROPIC_API_KEY=<key>
```

Or run scripts directly:

```bash
# Run full pipeline locally
python main.py --data-spec data/data_spec.md

# Run reviewer only
python scripts/run_reviewer.py --fe-spec specs/fe_spec.md --data-spec data/data_spec.md

# Compare and merge locally
python scripts/compare_specs.py --source specs/fe_spec_final.md --target specs/fe_spec.md
python scripts/merge_specs.py --source specs/fe_spec_final.md --target specs/fe_spec.md
```

## Troubleshooting

### Workflow Fails

1. Check Actions tab for error logs
2. Verify secrets are set correctly
3. Ensure required files exist
4. Check Python dependencies in requirements.txt

### API Rate Limits

- Anthropic: Monitor usage in console
- Add retries in config if needed
- Consider using workflow scheduling to avoid bursts

### Merge Conflicts

If PRs have conflicts:
1. Download artifacts from workflow
2. Resolve conflicts locally
3. Push resolved version

### Permission Errors

Ensure workflow has write permissions:
```
Settings → Actions → General → Workflow permissions
→ Read and write permissions ✓
```

## Best Practices

1. **Review PRs carefully** - Automated doesn't mean blindly merge
2. **Use compare workflow** - Always review diffs before accepting changes
3. **Keep backups** - Scripts create `.backup` files automatically
4. **Monitor logs** - Check logs in artifacts for debugging
5. **Iterate gradually** - Make small changes to data specs
6. **Version control** - Tag important spec versions

## Advanced Usage

### Custom Triggers

Add custom triggers to workflows:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  issues:
    types: [labeled]
```

### Environment-Specific Configs

Use different configs for different branches:

```yaml
- name: Select config
  run: |
    if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
      CONFIG="config/config.prod.yaml"
    else
      CONFIG="config/config.dev.yaml"
    fi
    echo "CONFIG=$CONFIG" >> $GITHUB_ENV
```

### Notifications

Add Slack/Email notifications:

```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

