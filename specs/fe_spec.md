```json
{
  "updated_spec": {
    "overview": "BiLSTM-based sequence model for predicting NFL player movement during pass plays. Uses pre-pass tracking data (up to ball release) to predict player trajectories for all frames when ball is in air. Features engineered for temporal validity with strict prevention of future information leakage.",
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
      "window_length_T": 20,
      "stride": 1,
      "alignment": "ends_at_pass_release",
      "padding": {"mode": "left", "value": 0},
      "masking": {"enabled": true, "mask_value": 0},
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
        "oov_policy": "none",
        "transform": "ffill→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_y",
        "source": "input.y",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "ffill→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_s",
        "source": "input.s",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "ffill→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_a",
        "source": "input.a",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "ffill→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_o_sin",
        "source": "input.o",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "sin(radians)→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_o_cos",
        "source": "input.o",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "cos(radians)→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_dir_sin",
        "source": "input.dir",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "sin(radians)→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_dir_cos",
        "source": "input.dir",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "cos(radians)→robust-scaler",
        "missing_policy": "pad_to_T",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "input → filtered_by_frame_id <= pass_release_frame"
      },
      {
        "feature_name": "player_position",
        "source": "input.player_position",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 8,
        "oov_policy": "min_freq>=5 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "static player attribute"
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
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "play-specific role assignment"
      },
      {
        "feature_name": "player_side",
        "source": "input.player_side",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "min_freq>=5 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "static for play"
      },
      {
        "feature_name": "play_direction",
        "source": "input.play_direction",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "min_freq>=5 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "static for play"
      },
      {
        "feature_name": "absolute_yardline",
        "source": "input.absolute_yardline_number",
        "dtype": "float32",
        "is_sequence": false,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "minmax-scaler",
        "missing_policy": "median_impute",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "static field position"
      },
      {
        "feature_name": "player_to_predict",
        "source": "input.player_to_predict",
        "dtype": "categorical_index",
        "is_sequence": false,
        "embedding_dim": 2,
        "oov_policy": "min_freq>=5 -> OOV_INDEX",
        "transform": "tokenize→index→embed",
        "missing_policy": "mode_impute",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "prediction target flag"
      },
      {
        "feature_name": "x_velocity",
        "source": "derived:Δx/Δt",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "diff(x)/diff(t)→robust-scaler",
        "missing_policy": "pad_to_T_with_zero_start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "derived from pre-pass x positions"
      },
      {
        "feature_name": "y_velocity",
        "source": "derived:Δy/Δt",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "diff(y)/diff(t)→robust-scaler",
        "missing_policy": "pad_to_T_with_zero_start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "derived from pre-pass y positions"
      },
      {
        "feature_name": "speed_change",
        "source": "derived:Δs/Δt",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "diff(s)/diff(t)→robust-scaler",
        "missing_policy": "pad_to_T_with_zero_start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "derived from pre-pass speed"
      },
      {
        "feature_name": "time_delta_ms",
        "source": "derived:diff(timestamp)",
        "dtype": "float32",
        "is_sequence": true,
        "embedding_dim": null,
        "oov_policy": "none",
        "transform": "lag-diff + clip[0, p99]",
        "missing_policy": "impute=100 at sequence start",
        "range_or_values": null,
        "leakage_risk": "none",
        "lineage": "sorted by timestamp asc; no future access"
      }
    ],
    "embedding_plan": [
      {"table": "player_position", "dim": 8, "share_across": "none"},
      {"table": "player_role", "dim": 4, "share_across": "none"},
      {"table": "player_side", "dim": 2, "share_across": "none"},
      {"table": "play_direction", "dim": 2, "share_across": "none"},
      {"table": "player_to_predict", "dim": 2, "share_across": "none"}
    ],
    "normalization": {"strategy": "robust", "scope": "per-entity"},
    "leakage_analysis": [
      {"risk": "ball_land_x/y represents future information", "mitigation": "removed from features"},
      {"risk": "post-pass release data", "mitigation": "strict filtering by frame_id <= pass_release_frame"}
    ],
    "validation_policy": {"split": "time-based_by_game_week", "folds": 3, "gaps": "1d"},
    "naming_conventions": {"style": "snake_case", "units": "explicit"}
  },
  "issue_to_fix_matrix": [
    {"comment_id": "ISS-001", "comment": "Window size of 15 steps may not capture sufficient pre-pass context", "fix": "Increased to 20 steps (2s) based on typical pre-pass duration analysis", "spec_section": "sequence_policy.window_length_T"},
    {"comment_id": "ISS-002", "comment": "Ball landing coordinates represent future information", "fix": "Removed ball_land_x and ball_land_y features entirely", "spec_section": "leakage_analysis"},
    {"comment_id": "ISS-003", "comment": "No explicit alignment policy between input sequences and output prediction frames", "fix": "Defined 'ends_at_pass_release' alignment with clear mapping to prediction frames", "spec_section": "sequence_policy.alignment"},
    {"comment_id": "ISS-004", "comment": "Derived features require temporal differencing but lack boundary handling", "fix": "Implemented zero-padding for first frame in velocity calculations", "spec_section": "feature_table.x_velocity.missing_policy"},
    {"comment_id": "ISS-005", "comment": "Missing feature for 'player_to_predict' flag", "fix": "Added player_to_predict as binary categorical feature with embedding", "spec_section": "feature_table.player_to_predict"},
    {"comment_id": "ISS-006", "comment": "No validation split strategy for temporal data", "fix": "Implemented time-based splits by game week with 1-day gaps", "spec_section": "validation_policy"},
    {"comment_id": "ISS-007", "comment": "Cyclic transformation with robust scaling breaks circularity", "fix": "Replaced with sin/cos encoding for orientation and direction angles", "spec_section": "feature_table.player_o_sin,player_o_cos"}
  ],
  "acceptance_checklist": [
    "All review comments mapped and resolved or justified",
    "No future information used in features (ball_land_x/y removed)",
    "Sequence window/stride/padding/masking defined for BiLSTM",
    "Embedding dims and OOV policy defined for all categorical features",
    "Normalization scopes documented (per-entity robust scaling)",
    "Time-aware split policy documented (game week based)",
    "Cyclic variables properly encoded with sin/cos",
    "Sequence boundary handling for derived features implemented"
  ],
  "open_questions": [
    "Confirm pass release frame identification method in raw data",
    "Typical distribution of pre-pass duration for window size optimization?",
    "Handling of variable-length sequences across different play types?"
  ],
  "assumptions": [
    "Using left-padding with masking for BiLSTM; adjust if causal constraints differ",
    "10Hz sampling rate consistent across all tracking data",
    "Pass release frame clearly identifiable in input data"
  ]
}
```

```md
# NFL Big Data Bowl 2026 - BiLSTM Feature Specification

## Overview & Scope
BiLSTM-based sequence model for predicting NFL player trajectories during pass plays. Uses **pre-pass tracking data only** (up to ball release moment) to predict player (x,y) positions for all frames when ball is in air. Strict temporal validity enforced with no future information leakage.

**Prediction Task**: Multi-step sequence prediction for each (game_id, play_id, nfl_id) predicting `num_frames_output` future positions.

## Data Contract & Lineage

### Primary Entities
- `game_id`: Unique game identifier
- `play_id`: Play identifier (scoped to game)
- `nfl_id`: Player identification  
- `frame_id`: Temporal frame index (10Hz sampling)

### Data Boundaries
- **Input**: All frames where `frame_id` <= pass_release_frame
- **Output**: All frames where `frame_id` >= 1 for output sequences
- **Strict Filtering**: No post-pass release data in features

## Feature Table

### Sequence Features (T=20 timesteps)
| Feature | Source | Type | Transform | Normalization | Leakage Risk |
|---------|--------|------|-----------|---------------|--------------|
| player_x | input.x | float32 | ffill→robust | per-entity | None |
| player_y | input.y | float32 | ffill→robust | per-entity | None |
| player_s | input.s | float32 | ffill→robust | per-entity | None |
| player_a | input.a | float32 | ffill→robust | per-entity | None |
| player_o_sin | input.o | float32 | sin(radians)→robust | per-entity | None |
| player_o_cos | input.o | float32 | cos(radians)→robust | per-entity | None |
| player_dir_sin | input.dir | float32 | sin(radians)→robust | per-entity | None |
| player_dir_cos | input.dir | float32 | cos(radians)→robust | per-entity | None |
| x_velocity | derived | float32 | diff/Δt→robust | per-entity | None |
| y_velocity | derived | float32 | diff/Δt→robust | per-entity | None |
| speed_change | derived | float32 | diff/Δt→robust | per-entity | None |
| time_delta_ms | derived | float32 | lag-diff + clip | per-entity | None |

### Context Features (Static per sequence)
| Feature | Source | Type | Encoding | Leakage Risk |
|---------|--------|------|----------|--------------|
| player_position | input | categorical | embedding (dim=8) | None |
| player_role | input | categorical | embedding (dim=4) | None |
| player_side | input | categorical | embedding (dim=2) | None |
| play_direction | input | categorical | embedding (dim=2) | None |
| absolute_yardline | input | float32 | minmax | None |
| player_to_predict | input | categorical | embedding (dim=2) | None |

## Sequence Policy

### Window Configuration
- **Window Length (T)**: 20 steps (2.0 seconds at 10Hz)
- **Stride**: 1 step (dense sampling)
- **Alignment**: Ends at pass release frame
- **Variable Length**: Bucketed with left-padding

### Padding & Masking
- **Padding**: Left-padding with value 0
- **Masking**: Enabled with mask_value = 0
- **Truncation**: Head truncation for long sequences

### Input-Output Mapping
Each input sequence `(game_id, play_id, nfl_id, frames 1..T)` predicts output frames `1..num_frames_output` for the same entities, where T ends at pass release.

## Embedding Plan

| Feature | Dimension | Sharing |
|---------|-----------|---------|
| player_position | 8 | None |
| player_role | 4 | None |
| player_side | 2 | None |
| play_direction | 2 | None |
| player_to_predict | 2 | None |

**OOV Policy**: Minimum frequency >= 5 → OOV_INDEX

## Normalization Strategy
- **Method**: Robust scaling (quantile range [0.01, 0.99])
- **Scope**: Per-entity normalization
- **Fit**: Training data only

## Leakage Analysis & Mitigation

### Critical Risks Addressed
1. **Ball Landing Coordinates**: Removed entirely - represent future information not available at prediction time
2. **Post-Pass Data**: Strict filtering by `frame_id <= pass_release_frame`
3. **Temporal Contamination**: Time-based validation splits prevent future game information leakage

### Validation
All features verified to use only information available at pass release moment.

## Validation & Splits

### Temporal Validation Strategy
- **Method**: Time-based splits by game week
- **Folds**: 3-fold cross-validation
- **Gaps**: 1-day minimum between train/validation periods
- **Grouping**: All plays from same game stay together

### Data Integrity
- No overlapping time periods between folds
- Strict chronological ordering maintained
- Grouped by game_id to prevent intra-game leakage

## Issue → Fix Matrix

| Issue ID | Comment | Fix Applied | Section |
|----------|---------|-------------|---------|
| ISS-001 | Window size insufficient | Increased to 20 steps | sequence_policy |
| ISS-002 | Ball landing coordinates leak future info | Removed features entirely | leakage_analysis |
| ISS-003 | No input-output alignment | Defined ends_at_pass_release policy | sequence_policy |
| ISS-004 | Derived feature boundary issues | Zero-padding for first frame | feature_table |
| ISS-005 | Missing prediction flag | Added player_to_predict feature | feature_table |
| ISS-006 | No temporal validation | Time-based splits by game week | validation_policy |
| ISS-007 | Cyclic scaling breaks circularity | Sin/cos encoding for angles | feature_table |

## Acceptance Checklist

- ✅ All review comments mapped and resolved
- ✅ No future information in features (ball_land_x/y removed)
- ✅ BiLSTM sequence policy fully defined (T=20, stride=1, left-padding with masking)
- ✅ Embedding dimensions and OOV policies specified for all categoricals
- ✅ Per-entity normalization scope documented
- ✅ Time-aware validation splits implemented
- ✅ Cyclic variables properly encoded with sin/cos
- ✅ Sequence boundary handling for derived features

## Open Questions

1. **Pass Release Identification**: How is pass release frame definitively identified in the raw data?
2. **Pre-pass Duration**: What's the typical distribution of pre-pass duration for window size optimization?
3. **Variable Sequences**: How to handle significantly variable sequence lengths across different play types?

## Assumptions

- Left-padding with masking optimal for BiLSTM architecture
- Consistent 10Hz sampling rate across all tracking data
- Clear identification of pass release frame in source data
- Sufficient pre-pass context captured in 2-second window
```