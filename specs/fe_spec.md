## Feature Map

| name | source | intent | type | transform pipeline | outlier policy | per-seq norm? | leakage risk | dtype | timestep_dim |
|------|--------|--------|------|-------------------|----------------|---------------|--------------|-------|--------------|
| x_pos | x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| y_pos | y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| speed | s | signal | continuous | mean→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |
| acceleration | a | signal | continuous | mean→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |
| orientation | o | signal | continuous | mean→none→none | none | false | false | float32 | 2 |
| direction | dir | signal | continuous | mean→none→none | none | false | false | float32 | 2 |
| player_position | player_position | context | categorical | mode→embedding→none | none | false | false | float32 | 8 |
| player_side | player_side | context | categorical | mode→one_hot→none | none | false | false | float32 | 2 |
| player_role | player_role | context | categorical | mode→embedding→none | none | false | false | float32 | 6 |
| play_direction | play_direction | context | categorical | mode→one_hot→none | none | false | false | float32 | 2 |
| absolute_yardline | absolute_yardline_number | context | continuous | mean→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| ball_land_x | ball_land_x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| ball_land_y | ball_land_y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| x_velocity | x,frame_id | signal | continuous | none→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |
| y_velocity | y,frame_id | signal | continuous | none→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |
| dist_to_ball_land | x,y,ball_land_x,ball_land_y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| x_lag1 | x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| y_lag1 | y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| speed_roll3 | s | signal | continuous | mean→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |
| accel_roll3 | a | signal | continuous | mean→none→robust | quantile[0.01,0.99] | false | false | float32 | 1 |

## Derived Features

**Temporal Features:**
- `x_velocity = (x_t - x_{t-1}) / 0.1` (10 fps → 0.1s intervals)
- `y_velocity = (y_t - y_{t-1}) / 0.1`
- `x_lag1 = x_{t-1}`, `y_lag1 = y_{t-1}`
- `speed_roll3 = rolling_mean(s, window=3)`
- `accel_roll3 = rolling_mean(a, window=3)`

**Spatial Features:**
- `dist_to_ball_land = sqrt((x - ball_land_x)² + (y - ball_land_y)²)`

**Angular Encoding:**
- `orientation`: [sin(o * π/180), cos(o * π/180)]
- `direction`: [sin(dir * π/180), cos(dir * π/180)]

## Normalization & Encoding

**Continuous Features:** Standard/Robust scaling with [0.01, 0.99] quantile clipping
**Categorical Encoding:**
- Low cardinality (<5): one-hot encoding
- High cardinality: embedding with dim = min(50, round(1.6 * cardinality^0.56))
- Rare category threshold: <0.5% frequency → "OTHER"

**Global normalization** chosen over per-sequence to maintain consistent field coordinate interpretation across plays.

## Sequence Processing

- **Resampling:** Forward fill for gaps ≤0.2s (2 frames)
- **Window:** Variable length based on input frames (typically 20-50 frames pre-pass)
- **Padding:** Pre-padding with mask_value=-999
- **Max length:** 60 frames (6 seconds max pre-pass tracking)

```json
{
  "sequence_params": {
    "sampling_rate_hz": 10,
    "resampling": {"method": "forward_fill", "max_gap_s": 0.2},
    "window_size": {"unit": "steps", "value": 60},
    "stride": {"unit": "steps", "value": 1},
    "padding": {"side": "pre", "value": -999},
    "max_seq_len": 60,
    "mask_value": -999,
    "bucket_by_length": true
  },
  "features": [
    {
      "name": "x_pos",
      "source": ["x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass position data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_pos",
      "source": ["y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass position data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "speed",
      "source": ["s"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass speed data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "acceleration",
      "source": ["a"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass acceleration data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "orientation",
      "source": ["o"],
      "intent": "signal",
      "type": "continuous",
      "derived": "[sin(o * π/180), cos(o * π/180)]",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass orientation data"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "direction",
      "source": ["dir"],
      "intent": "signal",
      "type": "continuous",
      "derived": "[sin(dir * π/180), cos(dir * π/180)]",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pre-pass direction data"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "player_position",
      "source": ["player_position"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "embedding", "params": {"dim": 8}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "static player attribute"},
      "dtype": "float32",
      "timestep_dim": 8
    },
    {
      "name": "player_side",
      "source": ["player_side"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "static player attribute"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "player_role",
      "source": ["player_role"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "embedding", "params": {"dim": 6}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "play-specific role assignment"},
      "dtype": "float32",
      "timestep_dim": 6
    },
    {
      "name": "play_direction",
      "source": ["play_direction"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "play context known pre-pass"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "absolute_yardline",
      "source": ["absolute_yardline_number"],
      "intent": "context",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "field position context"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "ball_land_x",
      "source": ["ball_land_x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pass target provided as input"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "ball_land_y",
      "source": ["ball_land_y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "none",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "pass target provided as input"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "x_velocity",
      "source": ["x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "(x_t - x_{t-1}) / 0.1",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "derived from pre-pass positions"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_velocity",
      "source": ["y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "(y_t - y_{t-1}) / 0.1",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "derived from pre-pass positions"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "dist_to_ball_land",
      "source": ["x", "y", "ball_land_x", "ball_land_y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "sqrt((x - ball_land_x)² + (y - ball_land_y)²)",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "distance to known target location"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "x_lag1",
      "source": ["x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "x_{t-1}",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "lagged position feature"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_lag1",
      "source": ["y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "y_{t-1}",
      "imputation": {"method": "none", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "lagged position feature"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "speed_roll3",
      "source": ["s"],
      "intent": "signal",
      "type": "continuous",
      "derived": "rolling_mean(s, window=3)",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "rolling average of speed"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "accel_roll3",
      "source": ["a"],
      "intent": "signal",
      "type": "continuous",
      "derived": "rolling_mean(a, window=3)",
      "imputation": {"method": "mean", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {"lower": 0.01, "upper": 0.99}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "rolling average of acceleration"},
      "dtype": "float32",
      "timestep_dim": 1
    }
  ],
  "final_dimensions": {"per_timestep": 34, "tensor": "(B,T,34)"}
}
```