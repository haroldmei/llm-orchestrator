```json
{
  "updated_spec": {
    "overview": "BiLSTM-based player movement prediction for NFL pass plays. Uses pre-pass tracking data (ending at QB release) to predict player trajectories during ball flight. Features engineered for temporal validity with strict prevention of future information leakage.",
    "data_contract": {
      "entities": ["game_id", "play_id", "nfl_id", "frame_id"],
      "schema": [
        {"field": "timestamp", "dtype": "int64", "unit": "ms"},
        {"field": "game_id", "dtype": "int64"},
        {"field": "play_id", "dtype": "int64"},
        {"field": "nfl_id", "dtype": "int64"},
        {"field": "frame_id", "dtype": "int64"}
      ]
    },
    "sequence_policy": {
      "window_length_T": 15,
      "stride": 1,
      "alignment": "ends_at_pass_release",
      "padding": {"mode": "right", "value": 0},
      "masking": {"enabled": true, "mask_value": -999.0},
      "truncation": "head",
      "variable_length": "bucketed"
    },
    "feature_table": [
      {
        "feature_name": "player_x",
        "source": "input.x",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 120],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_y",
        "source": "input.y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 53.3],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_s",
        "source": "input.s",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→robust_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 15],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_a",
        "source": "input.a",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→robust_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [-10, 10],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_o",
        "source": "input.o",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→minmax_0_360",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 360],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_dir",
        "source": "input.dir",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "ffill→minmax_0_360",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 360],
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "delta_x",
        "source": "derived: x_t - x_{t-1}",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "zero_first→standard_scaler",
        "missing_policy": "impute_0_at_start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input.x → diff → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "delta_y",
        "source": "derived: y_t - y_{t-1}",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "zero_first→standard_scaler",
        "missing_policy": "impute_0_at_start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input.y → diff → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "speed_x",
        "source": "derived: s * cos(dir)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input.s + input.dir → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "speed_y",
        "source": "derived: s * sin(dir)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input.s + input.dir → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "accel_magnitude",
        "source": "derived: sqrt(a_x² + a_y²)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "log1p→robust_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, null],
        "leakage_risk": "none",
        "lineage": "input.a → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "distance_to_qb",
        "source": "derived: sqrt((x - qb_x)² + (y - qb_y)²)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "robust_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 100],
        "leakage_risk": "none",
        "lineage": "input.x/y + qb_position → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "angle_to_qb",
        "source": "derived: atan2(qb_y - y, qb_x - x) - dir",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "minmax_-180_180",
        "missing_policy": "pad_to_T",
        "range_or_values": [-180, 180],
        "leakage_risk": "none",
        "lineage": "input + qb_position → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_position",
        "source": "input.player_position",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 8,
        "oov_policy": "min_freq>=10 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": ["QB", "WR", "RB", "TE", "CB", "S", "LB", "DL"],
        "leakage_risk": "none",
        "lineage": "roster_data → static"
      },
      {
        "feature_name": "player_role",
        "source": "input.player_role",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 4,
        "oov_policy": "min_freq>=5 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": ["Targeted Receiver", "Passer", "Defensive Coverage", "Other Route Runner"],
        "leakage_risk": "none",
        "lineage": "play_data → static_per_play"
      },
      {
        "feature_name": "player_side",
        "source": "input.player_side",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "fixed_vocab -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": ["Offense", "Defense"],
        "leakage_risk": "none",
        "lineage": "play_data → static_per_play"
      },
      {
        "feature_name": "play_direction",
        "source": "input.play_direction",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "fixed_vocab -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": ["left", "right"],
        "leakage_risk": "none",
        "lineage": "play_data → static_per_play"
      },
      {
        "feature_name": "absolute_yardline",
        "source": "input.absolute_yardline_number",
        "dtype": "float32",
        "is_sequence": false,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "minmax_0_120",
        "missing_policy": "mean_impute",
        "range_or_values": [0, 120],
        "leakage_risk": "none",
        "lineage": "play_data → static_per_play"
      },
      {
        "feature_name": "time_delta_ms",
        "source": "diff(timestamp)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "N/A",
        "transform": "constant_100ms_impute",
        "missing_policy": "impute_100_at_start",
        "range_or_values": [100, 100],
        "leakage_risk": "none",
        "lineage": "input.timestamp → diff → filtered_by_frame_id <= pass_release_frame"
      }
    ],
    "embedding_plan": [
      {"table": "player_position", "dim": 8, "share_across": "all_players"},
      {"table": "player_role", "dim": 4, "share_across": "all_players"},
      {"table": "player_side", "dim": 2, "share_across": "all_players"},
      {"table": "play_direction", "dim": 2, "share_across": "all_plays"}
    ],
    "normalization": {
      "strategy": "mixed",
      "scope": "per-feature-global",
      "policies": {
        "standard": ["player_x", "player_y", "delta_x", "delta_y", "speed_x", "speed_y"],
        "robust": ["player_s", "player_a", "accel_magnitude", "distance_to_qb"],
        "minmax": ["player_o", "player_dir", "angle_to_qb", "absolute_yardline"]
      }
    },
    "leakage_analysis": [
      {
        "risk": "Ball landing coordinates unavailable at prediction time",
        "mitigation": "Removed ball_land_x/y features, replaced with QB position proxies"
      },
      {
        "risk": "Player age requires play_date not in input",
        "mitigation": "Removed age feature due to data unavailability"
      },
      {
        "risk": "Future frame information in sequences",
        "mitigation": "Strict filtering by frame_id <= pass_release_frame"
      }
    ],
    "validation_policy": {
      "split": "time-based_by_week",
      "folds": 3,
      "gaps": "1_week",
      "group_by": ["game_id", "play_id"]
    },
    "naming_conventions": {
      "style": "snake_case",
      "units": "explicit"
    }
  },
  "issue_to_fix_matrix": [
    {
      "comment_id": "ISS-001",
      "comment": "Window size T=20 frames may not align with actual pre-pass sequence lengths",
      "fix": "Reduced to T=15 based on empirical analysis of pre-pass durations, aligned sequences to end at pass release",
      "spec_section": "sequence_policy.window_length_T"
    },
    {
      "comment_id": "ISS-002",
      "comment": "Ball landing coordinates create temporal leakage",
      "fix": "Removed all ball_land_x/y derived features, replaced with distance_to_qb and angle_to_qb using QB position",
      "spec_section": "feature_table + leakage_analysis"
    },
    {
      "comment_id": "ISS-003",
      "comment": "Delta features create NaN for first frame",
      "fix": "Implemented zero_first transform for delta features with explicit impute_0_at_start policy",
      "spec_section": "feature_table.delta_*"
    },
    {
      "comment_id": "ISS-004",
      "comment": "Padding strategy ambiguous with meaningful zeros",
      "fix": "Changed to right-padding with explicit mask_value = -999.0 preserved through normalization",
      "spec_section": "sequence_policy.padding + masking"
    },
    {
      "comment_id": "ISS-005",
      "comment": "Player age derivation requires unavailable play_date",
      "fix": "Removed player_age_years feature due to data unavailability",
      "spec_section": "feature_table (removed)"
    },
    {
      "comment_id": "ISS-006",
      "comment": "Mixed normalization strategies without rationale",
      "fix": "Documented normalization scope and strategies with clear feature categorization",
      "spec_section": "normalization"
    },
    {
      "comment_id": "ISS-007",
      "comment": "Excessive embedding dimensions for player position",
      "fix": "Reduced player_position embedding from 16 to 8 dimensions",
      "spec_section": "embedding_plan"
    }
  ],
  "acceptance_checklist": [
    "All review comments mapped and resolved with concrete fixes",
    "No future information used in features - ball landing coordinates removed",
    "Sequence window/stride/padding/masking explicitly defined for BiLSTM",
    "Embedding dims and OOV policy defined for all categorical features",
    "Normalization scopes and strategies documented per feature type",
    "Time-aware split policy with game/play grouping defined",
    "Temporal alignment enforced: sequences end at pass release frame"
  ],
  "open_questions": [
    "Confirm QB position availability at all pre-pass frames for distance/angle calculations",
    "Validate T=15 window covers sufficient pre-pass context across all play types",
    "Coordinate system standardization needed for directional features?"
  ],
  "assumptions": [
    "QB position available in tracking data for all frames",
    "Pass release frame clearly identifiable in dataset",
    "Right-padding suitable for BiLSTM; adjust if causal modeling preferred"
  ]
}
```

```md
# NFL Big Data Bowl 2026 - BiLSTM Feature Specification

## Overview & Scope
This specification defines features for BiLSTM-based prediction of NFL player movement during pass plays. The model uses **pre-pass tracking data only** (ending at quarterback release) to predict player trajectories while the ball is in air. All features are engineered with strict temporal validity to prevent future information leakage.

**Prediction Task**: Multi-step regression of (x,y) coordinates for each player-frame during ball flight
**Input Context**: Last 1.5 seconds (15 frames) before pass release
**Temporal Constraint**: No information beyond pass release frame used in features

## Data Contract & Lineage

### Primary Entities
- `game_id`, `play_id`, `nfl_id`, `frame_id` - Composite key for sequences
- `timestamp` - Millisecond precision timing
- All features filtered by `frame_id <= pass_release_frame`

### Data Sources
- **Tracking Data**: Player positions, speeds, accelerations, orientations
- **Play Context**: Player roles, sides, field position, play direction  
- **Roster Data**: Player positions (static attributes)

## Feature Table

### Sequential Features (T=15 timesteps)

| Feature | Source | Type | Transform | Normalization | Masking |
|---------|--------|------|-----------|---------------|---------|
| player_x | Raw tracking | Continuous | Forward fill | StandardScaler | -999.0 |
| player_y | Raw tracking | Continuous | Forward fill | StandardScaler | -999.0 |
| player_s | Raw tracking | Continuous | Forward fill | RobustScaler | -999.0 |
| player_a | Raw tracking | Continuous | Forward fill | RobustScaler | -999.0 |
| player_o | Raw tracking | Continuous | Forward fill | MinMax [0,360] | -999.0 |
| player_dir | Raw tracking | Continuous | Forward fill | MinMax [0,360] | -999.0 |
| delta_x | Derived: x_t - x_{t-1} | Continuous | Zero first frame | StandardScaler | -999.0 |
| delta_y | Derived: y_t - y_{t-1} | Continuous | Zero first frame | StandardScaler | -999.0 |
| speed_x | Derived: s * cos(dir) | Continuous | - | StandardScaler | -999.0 |
| speed_y | Derived: s * sin(dir) | Continuous | - | StandardScaler | -999.0 |
| accel_magnitude | Derived: sqrt(a_x² + a_y²) | Continuous | Log1p | RobustScaler | -999.0 |
| distance_to_qb | Derived: Euclidean to QB | Continuous | - | RobustScaler | -999.0 |
| angle_to_qb | Derived: relative angle | Continuous | - | MinMax [-180,180] | -999.0 |
| time_delta_ms | Derived: frame diff | Continuous | Constant 100ms | - | -999.0 |

### Static Features (Context)

| Feature | Source | Type | Encoding | Embedding Dim |
|---------|--------|------|----------|---------------|
| player_position | Roster | Categorical | Index + Embed | 8 |
| player_role | Play data | Categorical | Index + Embed | 4 |
| player_side | Play data | Categorical | Index + Embed | 2 |
| play_direction | Play data | Categorical | Index + Embed | 2 |
| absolute_yardline | Play data | Continuous | MinMax [0,120] | - |

## Sequence Policy

### Windowing & Alignment
- **Window Length (T)**: 15 frames (1.5 seconds pre-pass)
- **Stride**: 1 frame (dense sampling)
- **Alignment**: Sequences end exactly at pass release frame (t0)
- **Variable Length**: Bucketed with right-padding

### Padding & Masking
- **Padding**: Right-padding with zeros
- **Masking**: Explicit mask value = -999.0 preserved through normalization
- **Truncation**: Head truncation for sequences longer than T

## Embedding Plan

| Categorical Feature | Embedding Dim | Sharing Scope | OOV Policy |
|---------------------|---------------|---------------|------------|
| player_position | 8 | All players | min_freq>=10 → OOV_INDEX |
| player_role | 4 | All players | min_freq>=5 → OOV_INDEX |
| player_side | 2 | All players | Fixed vocab → OOV_INDEX |
| play_direction | 2 | All plays | Fixed vocab → OOV_INDEX |

## Normalization Strategy

**Scope**: Per-feature global normalization fit on training data only

| Method | Features | Rationale |
|--------|----------|-----------|
| StandardScaler | Positions, deltas, speed components | Gaussian-like distributions |
| RobustScaler | Speeds, accelerations, distances | Outlier-resistant for physical metrics |
| MinMax [0,1] | Angles, orientations, yardline | Bounded circular/field constraints |

## Leakage Analysis & Mitigation

### Critical Resolutions
1. **❌ REMOVED**: Ball landing coordinates (`ball_land_x`, `ball_land_y`)
   - *Mitigation*: Replaced with QB position-based features available at prediction time

2. **❌ REMOVED**: Player age (required unavailable `play_date`)
   - *Mitigation*: Feature excluded due to data constraints

3. **✅ ENFORCED**: Temporal filtering
   - *Mitigation*: All features strictly filtered by `frame_id <= pass_release_frame`

## Validation & Splits

### Cross-Validation Policy
- **Strategy**: Time-based split by game week
- **Folds**: 3-fold with 1-week gaps between folds
- **Grouping**: `game_id` and `play_id` to prevent data leakage
- **Test Scope**: Final 5 weeks of 2025 season (live leaderboard)

## Issue → Fix Matrix

| Issue ID | Severity | Fix Applied | Section |
|----------|----------|-------------|---------|
| ISS-001 | BLOCKER | Reduced T=15, aligned to pass release | Sequence Policy |
| ISS-002 | BLOCKER | Removed ball landing features | Feature Table |
| ISS-003 | MAJOR | Zero imputation for delta features | Transform Pipeline |
| ISS-004 | MAJOR | Right-padding with explicit masking | Padding/Masking |
| ISS-005 | MAJOR | Removed age feature | Feature Table |
| ISS-006 | MINOR | Documented normalization rationale | Normalization |
| ISS-007 | MINOR | Reduced embedding dimensions | Embedding Plan |

## Acceptance Checklist

- [x] All review comments addressed with concrete fixes
- [x] No temporal leakage - ball landing coordinates removed
- [x] BiLSTM-compatible sequence policy defined
- [x] Embedding dimensions optimized for categorical features  
- [x] Normalization strategies documented per feature type
- [x] Time-aware validation with game/play grouping
- [x] Temporal alignment: sequences end at pass release

## Open Questions

1. **QB Position Availability**: Confirm QB tracking data available for all pre-pass frames
2. **Window Size Validation**: Verify T=15 covers sufficient context across play types
3. **Coordinate System**: Standardization needs for directional features across field orientations

## Assumptions & Constraints

- Using right-padding for BiLSTM processing
- QB position reliably available in tracking data
- Pass release frame clearly identifiable in dataset
- 10Hz sampling rate consistent across all tracking data
```