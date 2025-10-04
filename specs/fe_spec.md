## Feature Specification Table

| Name | Source | Intent | Type | Transform Pipeline | Outlier Policy | Per-Seq Norm? | Leakage Risk | Dtype | Timestep Dim |
|------|--------|--------|------|-------------------|----------------|---------------|--------------|-------|-------------|
| player_x | input.x | Signal | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| player_y | input.y | Signal | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| player_speed | input.s | Signal | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| player_accel | input.a | Signal | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| player_orientation | input.o | Signal | Continuous | ffill→cyclic→none | None | Yes | Low | float32 | 2 |
| player_direction | input.dir | Signal | Continuous | ffill→cyclic→none | None | Yes | Low | float32 | 2 |
| ball_land_x | input.ball_land_x | Context | Continuous | median→none→minmax | None | No | Low | float32 | 1 |
| ball_land_y | input.ball_land_y | Context | Continuous | median→none→minmax | None | No | Low | float32 | 1 |
| player_position | input.player_position | Context | Categorical | mode→embedding→none | None | No | Low | int64 | 8 |
| player_role | input.player_role | Context | Categorical | mode→one_hot→none | None | No | Low | int64 | 4 |
| player_side | input.player_side | Context | Categorical | mode→one_hot→none | None | No | Low | int64 | 2 |
| play_direction | input.play_direction | Context | Categorical | mode→one_hot→none | None | No | Low | int64 | 2 |
| rel_to_ball_x | player_x, ball_land_x | Derived | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| rel_to_ball_y | player_y, ball_land_y | Derived | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| dist_to_ball | player_x, player_y, ball_land_x, ball_land_y | Derived | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| speed_towards_ball | player_speed, player_direction, ball_land_x, ball_land_y | Derived | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| speed_rolling_mean_5 | player_speed | Derived | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| accel_rolling_std_3 | player_accel | Derived | Continuous | ffill→none→robust | Quantile [0.01,0.99] | Yes | Low | float32 | 1 |
| x_lag_1 | player_x | Derived | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| y_lag_1 | player_y | Derived | Continuous | ffill→none→standard | IQR capping | Yes | Low | float32 | 1 |
| frame_id_normalized | input.frame_id | Time | Continuous | none→none→minmax | None | No | Low | float32 | 1 |

## Derived Features (Equations)

**Relative to Ball Landing:**
- `rel_to_ball_x = player_x - ball_land_x`
- `rel_to_ball_y = player_y - ball_land_y`
- `dist_to_ball = sqrt((player_x - ball_land_x)² + (player_y - ball_land_y)²)`

**Speed Towards Ball:**
- `angle_to_ball = atan2(ball_land_y - player_y, ball_land_x - player_x)`
- `speed_towards_ball = player_speed * cos(player_direction_rad - angle_to_ball)`

**Temporal Features:**
- `speed_rolling_mean_5 = mean(player_speed over 5 frames)`
- `accel_rolling_std_3 = std(player_accel over 3 frames)`
- `x_lag_1 = player_x at t-1`
- `y_lag_1 = player_y at t-1`

**Cyclical Encoding:**
- `player_orientation_sin = sin(2π * player_orientation / 360)`
- `player_orientation_cos = cos(2π * player_orientation / 360)`
- `player_direction_sin = sin(2π * player_direction / 360)`
- `player_direction_cos = cos(2π * player_direction / 360)`

## JSON Output

```json
{
  "sequence_params": {
    "sampling_rate_hz": 10,
    "resampling": {"method": "forward_fill", "max_gap_s": 0.5},
    "window_size": {"unit": "steps", "value": 30},
    "stride": {"unit": "steps", "value": 1},
    "padding": {"side": "pre", "value": 0.0},
    "max_seq_len": 30,
    "mask_value": -999.0,
    "bucket_by_length": true
  },
  "features": [
    {
      "name": "player_x",
      "source": ["input.x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "player_y",
      "source": ["input.y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "player_speed",
      "source": ["input.s"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "player_accel",
      "source": ["input.a"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "player_orientation",
      "source": ["input.o"],
      "intent": "signal",
      "type": "continuous",
      "derived": "sin_cos_encoding",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 2}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "player_direction",
      "source": ["input.dir"],
      "intent": "signal",
      "type": "continuous",
      "derived": "sin_cos_encoding",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 2}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Pre-pass tracking data only"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "ball_land_x",
      "source": ["input.ball_land_x"],
      "intent": "context",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "median", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "minmax", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Known at pass release"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "ball_land_y",
      "source": ["input.ball_land_y"],
      "intent": "context",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "median", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "minmax", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Known at pass release"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "player_position",
      "source": ["input.player_position"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "embedding", "params": {"dim": 8}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Static player attribute"},
      "dtype": "int64",
      "timestep_dim": 8
    },
    {
      "name": "player_role",
      "source": ["input.player_role"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {"dim": 4}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Known role assignment"},
      "dtype": "int64",
      "timestep_dim": 4
    },
    {
      "name": "player_side",
      "source": ["input.player_side"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {"dim": 2}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Team assignment"},
      "dtype": "int64",
      "timestep_dim": 2
    },
    {
      "name": "play_direction",
      "source": ["input.play_direction"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {"dim": 2}},
      "scaling": {"method": "none", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Play context"},
      "dtype": "int64",
      "timestep_dim": 2
    },
    {
      "name": "rel_to_ball_x",
      "source": ["player_x", "ball_land_x"],
      "intent": "derived",
      "type": "continuous",
      "derived": "player_x - ball_land_x",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Derived from pre-pass data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "rel_to_ball_y",
      "source": ["player_y", "ball_land_y"],
      "intent": "derived",
      "type": "continuous",
      "derived": "player_y - ball_land_y",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Derived from pre-pass data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "dist_to_ball",
      "source": ["player_x", "player_y", "ball_land_x", "ball_land_y"],
      "intent": "derived",
      "type": "continuous",
      "derived": "sqrt((player_x - ball_land_x)^2 + (player_y - ball_land_y)^2)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Derived from pre-pass data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "speed_towards_ball",
      "source": ["player_speed", "player_direction", "ball_land_x", "ball_land_y"],
      "intent": "derived",
      "type": "continuous",
      "derived": "player_speed * cos(player_direction_rad - angle_to_ball)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Derived from pre-pass data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "speed_rolling_mean_5",
      "source": ["player_speed"],
      "intent": "derived",
      "type": "continuous",
      "derived": "rolling_mean(window=5)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Only uses past information"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "accel_rolling_std_3",
      "source": ["player_accel"],
      "intent": "derived",
      "type": "continuous",
      "derived": "rolling_std(window=3)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"low_q": 0.01, "high_q": 0.99}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Only uses past information"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "x_lag_1",
      "source": ["player_x"],
      "intent": "derived",
      "type": "continuous",
      "derived": "lag(1)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Only uses past information"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_lag_1",
      "source": ["player_y"],
      "intent": "derived",
      "type": "continuous",
      "derived": "lag(1)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.05, 0.95]}},
      "outliers": {"method": "iqr", "params": {"factor": 1.5}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "Only uses past information"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "frame_id_normalized",
      "source": ["input.frame_id"],
      "intent": "time",
      "type": "continuous",
      "derived": "normalized_by_max_frame",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {"dim": 1}},
      "scaling": {"method": "minmax", "fit": "train_only", "params": {"clip_q": [0.0, 1.0]}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "Temporal context only"},
      "dtype": "float32",
      "timestep_dim": 1
    }
  ],
  "final_dimensions": {"per_timestep": 32, "tensor": "(B,T,32)"}
}
```