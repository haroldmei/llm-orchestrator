## Feature Map

| name | source | intent | type | transform pipeline | outlier policy | per-seq norm? | leakage risk | dtype | timestep_dim |
|------|--------|--------|------|-------------------|----------------|---------------|--------------|-------|--------------|
| x_pos | x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| y_pos | y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| speed | s | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| acceleration | a | signal | continuous | none→none→robust | quantile[0.005,0.995] | false | false | float32 | 1 |
| orientation | o | signal | continuous | none→none→none | none | false | false | float32 | 2 |
| direction | dir | signal | continuous | none→none→none | none | false | false | float32 | 2 |
| position_emb | player_position | context | categorical | none→embedding→none | none | false | false | float32 | 8 |
| role_emb | player_role | context | categorical | none→embedding→none | none | false | false | float32 | 4 |
| side_flag | player_side | context | categorical | none→one_hot→none | none | false | false | float32 | 2 |
| rel_ball_x | x,ball_land_x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| rel_ball_y | y,ball_land_y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| ball_distance | x,y,ball_land_x,ball_land_y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| x_velocity | x | signal | continuous | none→none→standard | quantile[0.01,0.99] | true | false | float32 | 1 |
| y_velocity | y | signal | continuous | none→none→standard | quantile[0.01,0.99] | true | false | float32 | 1 |
| x_lag1 | x | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| y_lag1 | y | signal | continuous | none→none→standard | quantile[0.01,0.99] | false | false | float32 | 1 |
| speed_rolling_mean | s | signal | continuous | none→none→standard | quantile[0.01,0.99] | true | false | float32 | 1 |
| accel_rolling_std | a | signal | continuous | none→none→robust | quantile[0.005,0.995] | true | false | float32 | 1 |
| direction_change | dir | signal | continuous | none→none→robust | quantile[0.01,0.99] | true | false | float32 | 1 |
| predict_flag | player_to_predict | control | categorical | none→none→none | none | false | false | bool | 1 |

## Derived Features (with equations)

**Temporal Features:**
- `x_velocity = diff(x) * 10` (10 fps to yards/sec)
- `y_velocity = diff(y) * 10` 
- `x_lag1 = lag(x, 1)`, `y_lag1 = lag(y, 1)`
- `speed_rolling_mean = rolling_mean(s, window=3)`
- `accel_rolling_std = rolling_std(a, window=3)`
- `direction_change = abs(diff(dir))` with 360° wrapping

**Spatial Relationships:**
- `rel_ball_x = ball_land_x - x`
- `rel_ball_y = ball_land_y - y`  
- `ball_distance = sqrt((ball_land_x - x)² + (ball_land_y - y)²)`

**Cyclical Encodings:**
- `orientation = [sin(o * π/180), cos(o * π/180)]`
- `direction = [sin(dir * π/180), cos(dir * π/180)]`

## Normalization & Encoding

**Scalers:**
- Position/speed: `standard` scaler, clip [0.01, 0.99] quantiles
- Acceleration/derivatives: `robust` scaler, clip [0.005, 0.995] quantiles  
- Angular features: `none` (already normalized sin/cos)

**Categorical Encoding:**
- `player_position`: embedding dim = min(50, round(1.6 * 25^0.56)) = 8
- `player_role`: embedding dim = min(50, round(1.6 * 4^0.56)) = 4  
- `player_side`: one-hot (2 categories)
- Rare category threshold: <0.5% → 'OTHER'

**Normalization Policy:**
- Global normalization for position/speed (consistent field scale)
- Per-sequence for derivatives/rolling stats (play-specific dynamics)

## Sequence Processing

**Resampling:** `none` (already 10 fps uniform)
**Windowing:** Variable length sequences (5-25 frames), stride=1
**Padding:** `pre` padding with mask_value=-999 (preserves temporal causality)
**Truncation:** max_seq_len=30, length bucketing enabled

## Final Dimensionality

**Per-timestep features:** 38
- Continuous: 26 (positions, speeds, derivatives, distances)
- Embeddings: 12 (position=8, role=4)  
- One-hot: 2 (side)
- Flags: 1 (predict_flag)
- **Total: 41**

**Tensor shape:** `(batch, time≤30, 41)`

## Data Quality & Risk

**Missing Values:** Forward fill for tracking data, mean impute for player attributes
**Outliers:** Position/speed clipped at 1-99%, acceleration at 0.5-99.5%
**Leakage Register:** 
- ✓ Ball landing position known at t=0 (provided feature)
- ✓ Only pre-throw data used for prediction
- ✓ No future frame information in derived features

**Split Discipline:** Group by game_id, time-aware, scaler fit on TRAIN only

```json
{
  "sequence_params": {
    "sampling_rate_hz": 10,
    "resampling": {"method": "none", "max_gap_s": 0.2},
    "window_size": {"unit": "steps", "value": 30},
    "stride": {"unit": "steps", "value": 1},
    "padding": {"side": "pre", "value": -999},
    "max_seq_len": 30,
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
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical position data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_pos", 
      "source": ["y"],
      "intent": "signal",
      "type": "continuous", 
      "derived": "none",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical position data"},
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
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical speed data"},
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
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.005, 0.995]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical acceleration data"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "orientation",
      "source": ["o"],
      "intent": "signal",
      "type": "continuous", 
      "derived": "[sin(o * π/180), cos(o * π/180)]",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical orientation data"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "direction",
      "source": ["dir"],
      "intent": "signal",
      "type": "continuous",
      "derived": "[sin(dir * π/180), cos(dir * π/180)]", 
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "historical direction data"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "position_emb",
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
      "name": "role_emb",
      "source": ["player_role"],
      "intent": "context",
      "type": "categorical",
      "derived": "none", 
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "embedding", "params": {"dim": 4}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "play-specific role assignment"},
      "dtype": "float32", 
      "timestep_dim": 4
    },
    {
      "name": "side_flag",
      "source": ["player_side"],
      "intent": "context",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "one_hot", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "team assignment known"},
      "dtype": "float32",
      "timestep_dim": 2
    },
    {
      "name": "rel_ball_x",
      "source": ["x", "ball_land_x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "ball_land_x - x",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "ball landing location is provided feature"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "rel_ball_y",
      "source": ["y", "ball_land_y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "ball_land_y - y",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "ball landing location is provided feature"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "ball_distance",
      "source": ["x", "y", "ball_land_x", "ball_land_y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "sqrt((ball_land_x - x)² + (ball_land_y - y)²)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "ball landing location is provided feature"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "x_velocity",
      "source": ["x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "diff(x) * 10",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "computed from historical positions only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_velocity", 
      "source": ["y"],
      "intent": "signal",
      "type": "continuous",
      "derived": "diff(y) * 10",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "computed from historical positions only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "x_lag1",
      "source": ["x"],
      "intent": "signal",
      "type": "continuous",
      "derived": "lag(x, 1)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "lagged historical position"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "y_lag1",
      "source": ["y"],
      "intent": "signal", 
      "type": "continuous",
      "derived": "lag(y, 1)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "lagged historical position"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "speed_rolling_mean",
      "source": ["s"],
      "intent": "signal",
      "type": "continuous",
      "derived": "rolling_mean(s, window=3)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "standard", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "backward-looking rolling window"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "accel_rolling_std",
      "source": ["a"],
      "intent": "signal",
      "type": "continuous",
      "derived": "rolling_std(a, window=3)",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.005, 0.995]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "backward-looking rolling window"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "direction_change",
      "source": ["dir"],
      "intent": "signal",
      "type": "continuous",
      "derived": "abs(diff(dir)) with 360° wrapping",
      "imputation": {"method": "ffill", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "robust", "fit": "train_only", "params": {"clip_q": [0.01, 0.99]}},
      "outliers": {"method": "quantile", "params": {}},
      "per_sequence_normalization": true,
      "leakage_risk": {"flag": false, "note": "computed from historical direction only"},
      "dtype": "float32",
      "timestep_dim": 1
    },
    {
      "name": "predict_flag",
      "source": ["player_to_predict"],
      "intent": "control",
      "type": "categorical",
      "derived": "none",
      "imputation": {"method": "mode", "params": {}},
      "encoding": {"method": "none", "params": {}},
      "scaling": {"method": "none", "fit": "train_only", "params": {}},
      "outliers": {"method": "none", "params": {}},
      "per_sequence_normalization": false,
      "leakage_risk": {"flag": false, "note": "evaluation mask flag"},
      "dtype": "bool",
      "timestep_dim": 1
    }
  ],
  "final_dimensions": {"per_timestep": 41, "tensor": "(B,T,F)"}
}
```