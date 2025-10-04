# Quick Start: Confidence Score Extraction

## Current Setup

The system now supports **3 reviewer implementations**. You can switch between them in `config/config.yaml`:

```yaml
reviewer_type: robust  # Options: "default", "robust", "structured"
```

## Options

### 1. **Default** (Current - Simple)
```yaml
reviewer_type: default
```
- Single regex pattern
- Defaults to 50% on failure
- ⚠️ Least reliable

### 2. **Robust** (Recommended - Better)
```yaml
reviewer_type: robust
```
- Multiple regex patterns
- Retry mechanism if parsing fails
- Range validation
- ✅ **Currently configured** - Best balance of reliability and simplicity

### 3. **Structured** (Best - Production)
```yaml
reviewer_type: structured
```
- JSON schema output
- Type validation
- No silent failures
- ✅ Most reliable for production

## Testing Each Approach

```bash
# Test with robust (current config)
python main.py --data-spec data/data_spec_example.md

# Test with structured
# 1. Edit config/config.yaml: reviewer_type: structured
# 2. Run: python main.py --data-spec data/data_spec_example.md

# Test with default (original)
# 1. Edit config/config.yaml: reviewer_type: default
# 2. Run: python main.py --data-spec data/data_spec_example.md
```

## Comparison at a Glance

| Feature | Default | Robust | Structured |
|---------|---------|--------|------------|
| Reliability | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Complexity | Low | Medium | High |
| Debugging | Poor | Good | Excellent |
| Validation | None | Range | Type + Range |
| Retry Logic | No | Yes | No (not needed) |
| **Recommended For** | Testing only | **Production-ready** | **Enterprise** |

## Recommendation

- **Now**: Use `robust` (already configured)
- **Later**: Migrate to `structured` for maximum reliability

## See Also

- [CONFIDENCE_SCORE_APPROACHES.md](CONFIDENCE_SCORE_APPROACHES.md) - Detailed comparison
- `src/agents/fe_reviewer.py` - Default implementation
- `src/agents/fe_reviewer_robust.py` - Robust implementation  
- `src/agents/fe_reviewer_improved.py` - Structured implementation

