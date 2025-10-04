```json
{
  "updated_spec": {
    "overview": "BiLSTM-based player movement prediction using pre-pass tracking data only. Predicts (x,y) coordinates for all players during pass flight frames using sequence data ending at ball release moment (t0). Eliminates all future information leakage while preserving motion dynamics and contextual features.",
    "data_contract": {
      "entities": ["game_id", "play_id", "nfl_id", "frame_id"],
      "schema": [
        {"field": "timestamp", "dtype": "int64", "unit": "ms"},
        {"field": "frame_id", "dtype": "int32", "unit": "10hz_index"},
        {"field": "x", "dtype": "float32", "unit": "yards"},
        {"field": "y", "dtype": "float32", "unit": "yards"},
        {"field": "s", "dtype": "float32", "unit": "yards_per_second"},
        {"field": "a", "dtype": "float32", "unit": "yards_per_second_squared"},
        {"field": "o", "dtype": "float32", "unit": "degrees"},
        {"field": "dir", "dtype": "float32", "unit": "degrees"}
      ]
    },
    "sequence_policy": {
      "window_length_T": "variable_up_to_30",
      "stride": 1,
      "alignment": "ends_at_ball_release",
      "padding": {"mode": "left", "value": 0},
      "masking": {"enabled": true, "mask_value": 0},
      "truncation": "head",
      "variable_length": "allowed"
    },
    "feature_table": [
      {
        "feature_name": "player_x",
        "source": "input.x",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 120],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_y",
        "source": "input.y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 53.3],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_speed",
        "source": "input.s",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→robust_scaler→clip[0.01,0.99]",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 15],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_accel",
        "source": "input.a",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→robust_scaler→clip[0.01,0.99]",
        "missing_policy": "pad_to_T",
        "range_or_values": [-10, 10],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_orientation",
        "source": "input.o",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→cyclic_encoding",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 360],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_direction",
        "source": "input.dir",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "ffill→cyclic_encoding",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 360],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "player_position",
        "source": "input.player_position",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 8,
        "oov_policy": "min_freq>=5 → OOV_INDEX",
        "transform": "mode→index→embed",
        "missing_policy": "mode_imputation",
        "range_or_values": ["QB", "WR", "CB", "S", "LB", "DL", "TE", "RB", "OOV"],
        "leakage_risk": "none",
        "lineage": "static_player_attribute"
      },
      {
        "feature_name": "player_role",
        "source": "input.player_role",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 4,
        "oov_policy": "all_known",
        "transform": "mode→one_hot",
        "missing_policy": "mode_imputation",
        "range_or_values": ["Targeted Receiver", "Passer", "Defensive Coverage", "Other Route Runner"],
        "leakage_risk": "none",
        "lineage": "play_assignment"
      },
      {
        "feature_name": "player_side",
        "source": "input.player_side",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "all_known",
        "transform": "mode→one_hot",
        "missing_policy": "mode_imputation",
        "range_or_values": ["Offense", "Defense"],
        "leakage_risk": "none",
        "lineage": "team_assignment"
      },
      {
        "feature_name": "play_direction",
        "source": "input.play_direction",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "all_known",
        "transform": "mode→one_hot",
        "missing_policy": "mode_imputation",
        "range_or_values": ["left", "right"],
        "leakage_risk": "none",
        "lineage": "play_context"
      },
      {
        "feature_name": "qb_relative_x",
        "source": "player_x, qb_x",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "player_x - qb_x→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "qb_relative_y",
        "source": "player_y, qb_y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "player_y - qb_y→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "dist_to_qb",
        "source": "player_x, player_y, qb_x, qb_y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "euclidean_distance→robust_scaler→clip[0.01,0.99]",
        "missing_policy": "pad_to_T",
        "range_or_values": [0, 70],
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "speed_rolling_mean_5",
        "source": "player_speed",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "rolling_mean_5→robust_scaler→clip[0.01,0.99]",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "accel_rolling_std_3",
        "source": "player_accel",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "rolling_std_3→robust_scaler→clip[0.01,0.99]",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "x_lag_1",
        "source": "player_x",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "lag_1→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "y_lag_1",
        "source": "player_y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "lag_1→standard_scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "pre_pass_tracking ≤ t0"
      },
      {
        "feature_name": "time_delta_sec",
        "source": "frame_id",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "not_applicable",
        "transform": "diff→robust_scaler",
        "missing_policy": "impute_0_at_start",
        "range_or_values": [0.1, null],
        "leakage_risk": "none",
        "lineage": "frame_differences"
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
      "scope": "per_entity",
      "continuous_standard": ["player_x", "player_y", "qb_relative_x", "qb_relative_y", "x_lag_1", "y_lag_1"],
      "continuous_robust": ["player_speed", "player_accel", "dist_to_qb", "speed_rolling_mean_5", "accel_rolling_std_3", "time_delta_sec"]
    },
    "leakage_analysis": [
      {
        "risk": "ball_landing_coordinates",
        "mitigation": "removed_all_features_derived_from_ball_land_x_y",
        "status": "resolved"
      },
      {
        "risk": "future_frame_information", 
        "mitigation": "sequences_end_at_ball_release_t0",
        "status": "resolved"
      },
      {
        "risk": "temporal_contamination_across_games",
        "mitigation": "time_based_splits_by_game_week",
        "status": "implemented"
      }
    ],
    "validation_policy": {
      "split": "time_based_by_game_week",
      "folds": 3,
      "gaps": "1_week",
      "train_weeks": "weeks_1_12",
      "val_weeks": "weeks_13_15", 
      "test_weeks": "weeks_16_18"
    },
    "naming_conventions": {
      "style": "snake_case",
      "units": "explicit",
      "temporal_reference": "t0_ball_release"
    }
  },
  "issue_to_fix_matrix": [
    {
      "comment_id": "ISS-001",
      "comment": "ball_land_x and ball_land_y are used in derived features but these values represent the actual landing location which is unknown at prediction time",
      "fix": "Removed all ball landing coordinate features and derivatives. Replaced with QB-relative positioning features using only pre-pass information",
      "spec_section": "feature_table, leakage_analysis"
    },
    {
      "comment_id": "ISS-002", 
      "comment": "Window size of 30 frames may not align with actual pre-pass sequence lengths. No specification of alignment to outcome time t0",
      "fix": "Defined variable length sequences ending at ball release frame with left-padding for shorter sequences",
      "spec_section": "sequence_policy"
    },
    {
      "comment_id": "ISS-003",
      "comment": "Multiple derived features depend on ball_land_x/y creating data leakage",
      "fix": "Replaced ball-relative features with QB-relative features: qb_relative_x, qb_relative_y, dist_to_qb",
      "spec_section": "feature_table"
    },
    {
      "comment_id": "ISS-004",
      "comment": "No OOV strategy specified for player_position embedding",
      "fix": "Added OOV policy: min_freq>=5 → OOV_INDEX with position grouping for rare roles",
      "spec_section": "feature_table.player_position"
    },
    {
      "comment_id": "ISS-005",
      "comment": "No specification of train/validation/test split strategy considering temporal nature",
      "fix": "Implemented time-based splits by game week with explicit week ranges for train/val/test",
      "spec_section": "validation_policy"
    }
  ],
  "acceptance_checklist": [
    "All review comments mapped and resolved - 5/5 issues addressed",
    "No future information used in features - ball landing coordinates completely removed",
    "Sequence window/stride/padding/masking defined - variable length with left-padding and masking",
    "Embedding dims and OOV policy defined for all categorical features - OOV policies specified",
    "Normalization scopes documented - per-entity with mixed strategies",
    "Time-aware split policy documented - game week based splits implemented"
  ],
  "open_questions": [
    "How to identify QB position reliably across all plays?",
    "Should we include relative positioning to other players beyond QB?",
    "What is the maximum observed pre-pass sequence length for dimensioning?"
  ],
  "assumptions": [
    "QB position can be reliably identified from player_role='Passer'",
    "Ball release frame (t0) is clearly marked in the tracking data", 
    "Pre-pass sequences are typically ≤30 frames (3 seconds)"
  ]
}
```

```md
# NFL Big Data Bowl 2026 - BiLSTM Feature Specification

## Overview & Scope
This specification defines features for BiLSTM-based player movement prediction during pass plays. The model predicts (x,y) coordinates for all players during ball flight frames using **only pre-pass tracking data** ending at ball release moment (t0). All features are temporally valid with no future information leakage.

**Prediction Task**: Multi-step sequence-to-sequence prediction of player trajectories
**Input**: Pre-pass player tracking sequences (≤30 frames, 10Hz)
**Output**: (x,y) coordinates during pass flight frames
**Model**: BiLSTM with variable-length sequence handling

## Data Contract & Lineage

### Primary Entities
- `game_id`, `play_id`, `nfl_id`, `frame_id` - Composite key for sequences
- All tracking data filtered by `frame_id ≤ ball_release_frame`

### Schema Enforcement
| Field | Type | Unit | Constraints |
|-------|------|------|-------------|
| timestamp | int64 | ms | Monotonically increasing |
| frame_id | int32 | 10hz_index | 1-indexed per play |
| x, y | float32 | yards | [0,120], [0,53.3] |
| s | float32 | yards/sec | [0,15] typical |
| a | float32 | yards/sec² | [-10,10] typical |

### Data Lineage
- **Source**: NFL Next Gen Stats tracking data
- **Filter**: `frame_id ≤ ball_release_frame` (t0)
- **Scope**: Pre-pass movement only, no ball flight data
- **Validation**: Temporal integrity checks for monotonic timestamps

## Feature Table

### Motion Signals (Sequential)
| Feature | Source | Transform | Normalization | Risk |
|---------|--------|-----------|---------------|------|
| player_x | input.x | ffill→standard | per-entity | none |
| player_y | input.y | ffill→standard | per-entity | none |
| player_speed | input.s | ffill→robust→clip | per-entity | none |
| player_accel | input.a | ffill→robust→clip | per-entity | none |
| player_orientation | input.o | ffill→cyclic | per-entity | none |
| player_direction | input.dir | ffill→cyclic | per-entity | none |

### Context Features (Static)
| Feature | Source | Transform | Encoding | OOV Policy |
|---------|--------|-----------|----------|------------|
| player_position | input.player_position | mode→index | embedding_dim=8 | min_freq≥5→OOV |
| player_role | input.player_role | mode→index | one_hot | all known |
| player_side | input.player_side | mode→index | one_hot | all known |
| play_direction | input.play_direction | mode→index | one_hot | all known |

### Derived Features (Sequential)
| Feature | Equation | Transform | Purpose |
|---------|----------|-----------|---------|
| qb_relative_x | player_x - qb_x | standard | Relative positioning |
| qb_relative_y | player_y - qb_y | standard | Relative positioning |
| dist_to_qb | Euclidean(player, QB) | robust→clip | Proximity metric |
| speed_rolling_mean_5 | mean(speed, 5) | robust→clip | Motion smoothing |
| accel_rolling_std_3 | std(accel, 3) | robust→clip | Volatility measure |
| x_lag_1, y_lag_1 | lag(position, 1) | standard | Temporal dynamics |
| time_delta_sec | frame_diff / 10 | robust | Irregular timing |

## Sequence Policy

### Temporal Alignment
- **Alignment**: Sequences end at ball release frame (t0)
- **Length**: Variable up to 30 frames (3 seconds max)
- **Stride**: 1 frame (dense sampling)

### Padding & Masking
```python
sequence_policy = {
    "padding": "left",        # Pad shorter sequences at start
    "mask_value": 0,          # Mask padded positions
    "truncation": "head",     # Keep most recent frames if over limit
    "variable_length": true   # Support different sequence lengths
}
```

### BiLSTM Optimization
- **Left-padding** preserves temporal causality for BiLSTM
- **Masking** prevents padded values from affecting gradients
- **Variable length** handles realistic pre-pass durations

## Embedding Plan

| Categorical Feature | Embedding Dim | Sharing | Vocabulary Size |
|---------------------|---------------|---------|-----------------|
| player_position | 8 | all players | ~15 positions + OOV |
| player_role | 4 | all players | 4 roles |
| player_side | 2 | all players | 2 sides |
| play_direction | 2 | all plays | 2 directions |

**OOV Handling**: Positions with frequency <5 mapped to OOV_INDEX
**Embedding Sharing**: Reduces parameter count while maintaining specificity

## Normalization Strategy

### Per-Entity Scaling
All sequential features normalized within each (game_id, play_id, nfl_id) sequence:

**Standard Scaler** (mean=0, std=1):
- Positional features: player_x, player_y, qb_relative_x, qb_relative_y, lag features

**Robust Scaler** (median=0, IQR=1):
- Motion features: speed, acceleration, distances, rolling statistics
- Clipped at [0.01, 0.99] quantiles to handle outliers

**Cyclical Encoding**:
- Orientation/direction: sin/cos transformation for circular continuity

## Leakage Analysis

### Resolved Risks
| Risk | Mitigation | Status |
|------|------------|--------|
| Ball landing coordinates | Removed all ball_land_x/y features | ✅ Resolved |
| Future frame information | Sequences end at ball release t0 | ✅ Resolved |
| Temporal contamination | Time-based splits by game week | ✅ Implemented |

### Validation
- **No features** use information beyond ball release frame
- **All derivatives** computed from pre-pass data only
- **Temporal splits** prevent leakage across game weeks

## Validation & Splits

### Time-Based Strategy
```python
validation_policy = {
    "train_weeks": "Weeks 1-12",    # Early season games
    "val_weeks": "Weeks 13-15",     # Mid-season validation  
    "test_weeks": "Weeks 16-18",    # Late season testing
    "folds": 3,                     # Temporal cross-validation
    "gap": "1 week"                 # Prevent adjacent week leakage
}
```

### Evaluation Metric
**RMSE** on (x,y) coordinates:
```python
RMSE = √[0.5 * (MSE_x + MSE_y)]
```

## Issue→Fix Matrix

| Issue ID | Severity | Comment | Fix Applied |
|----------|----------|---------|-------------|
| ISS-001 | BLOCKER | Ball landing coordinates leakage | Removed all ball_land features |
| ISS-002 | MAJOR | Sequence alignment undefined | Variable length ending at t0 |
| ISS-003 | MAJOR | Derived features leakage | Replaced with QB-relative features |
| ISS-004 | MINOR | No OOV strategy | min_freq≥5→OOV_INDEX policy |
| ISS-005 | MINOR | No temporal splits | Game week based splits |

## Acceptance Checklist

- [x] **All review comments addressed** - 5/5 issues resolved
- [x] **No future information** - Ball landing coordinates completely removed
- [x] **Sequence policy defined** - Variable length with left-padding/masking
- [x] **Embedding OOV policies** - Specified for all categorical features  
- [x] **Normalization scopes** - Per-entity with mixed strategies
- [x] **Time-aware splits** - Game week based validation implemented

## Open Questions

1. **QB Identification**: How to reliably identify QB position across all plays?
2. **Additional Relativity**: Should we include relative positioning to other players beyond QB?
3. **Sequence Length**: What is the maximum observed pre-pass sequence length for dimensioning?

## Assumptions & Constraints

- QB position identifiable from `player_role = 'Passer'`
- Ball release frame (t0) clearly marked in tracking data
- Pre-pass sequences typically ≤30 frames (3 seconds maximum)
- 10Hz sampling rate consistent across all tracking data
```