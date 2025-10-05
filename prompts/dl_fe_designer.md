# BiLSTM Feature Spec (Guardrailed & Verifiable)

**Role:** Elite Feature Engineering Strategist for BiLSTM sequence models.

**Objective:** From the provided DATA_SPEC, produce a verifiable, leakage-safe feature spec and sequence policy optimized for BiLSTM.

## Inputs
- **TASK:** {{classification|**regression**|sequence_labeling}}
- **TARGET:** {{TARGET = ['x', 'y'], prediction horizon/alignment (t or t+Δ), loss}}
- **DOMAIN:** {{National Football League player movement prediction during the pass play}}
- **SAMPLING:** {{base rate, jitter characteristics, timezone, DST policy}}
- **DATA_SPEC:** 
  - Schema: columns with dtypes & units
  - Missingness % per column
  - Categorical cardinalities
  - Label definition & provenance
  - Known artifacts (clock drift, duplicates, gaps)

## Requirements

### 1) Feature Map (table)
For each feature: `name | source | intent | type | transform pipeline (impute→encode→scale) | outlier policy | per-seq norm? | leakage risk | dtype | timestep_dim`.

### 2) Derived Features (with equations)
- Temporal: lags/leads, deltas, rolling stats (mean/std/min/max, quantiles), EWMs, slopes.
- Frequency: STFT/FFT bands (only if evenly sampled); specify window, hop, and bands.
- Event structure: inter-arrival time, time-since-last, counts in window.
- Cyclical: sin/cos encodings for hour-of-day, day-of-week, etc.

### 3) Normalization & Encoding
- Per-feature scaler: `standard | robust | min-max | none`, with clip quantiles (e.g., [0.01, 0.99]).
- Per-sequence vs global normalization (justify choice).
- Categorical: `one-hot` (low-card) or `embedding` with dimension rule `min(50, round(1.6 * cardinality^0.56))`.
- Rare-category binning threshold (e.g., <0.5% frequency).
 - Skew-aware transforms: allow `log1p | boxcox` prior to scaling for heavy tails.
 - Categorical vocab: build on TRAIN only; reserve tokens `<UNK>`, `<PAD>`; define OOV policy and hashing fallback.

### 4) Sequence Processing
- Resampling: `none | forward_fill | linear | kalman`; `max_gap_s`.
- Windowing: `window_size`, `stride`; padding side `pre|post` (justify).
- Truncation: `max_seq_len`; provide `mask_value` and enable length bucketing/sort-by-length.
 - Irregular time handling: include `delta_t` channel and `gap_mask`; specify resampling params (e.g., kalman/linear smoothing).

### 5) Final Dimensionality
- Report per-timestep dims (include embeddings/one-hot expansions).
- Provide final tensor shape `(batch, time, features)`.
 - Feature budget: cap per-timestep dims; justify any exceedances.

### 6) Data Quality & Risk
- Missing-value strategy per feature; outlier handling (IQR/quantile capping).
- **Leakage Register:** potential sources, mechanism, mitigation.
- Split discipline: group/time-aware; scaler fit on **TRAIN only**.
 - Quality gates: monotonic timestamps; no NaN/Inf post-transform; unit consistency; mask alignment.

### 7) Online/Inference Readiness & Train–Serve Skew
- Availability per feature at inference; online source, expected latency and max staleness.
- Train–serve skew checks: vocab freeze point, OOV handling, and pipeline parity.
- Latency/freshness limits for end-to-end inference; define global and per-feature constraints.
- Padding/mask channel must be explicit; ensure `mask_value` never collides with scaled zeros.

### 8) JSON Output (strict; single object)
Use this schema exactly:

{
  "sequence_params": {
    "sampling_rate_hz": number,
    "resampling": {"method": "none|forward_fill|linear|kalman", "max_gap_s": number, "params": {}},
    "window_size": {"unit": "steps|seconds", "value": number},
    "stride": {"unit": "steps|seconds", "value": number},
    "padding": {"side": "pre|post", "value": number},
    "max_seq_len": number,
    "mask_value": number,
    "bucket_by_length": boolean
  },
  "aux_channels": {"mask": boolean, "delta_t": boolean},
  "features": [
    {
      "name": "string",
      "source": ["string"],
      "intent": "signal|context|control|time",
      "type": "continuous|categorical|datetime|event_flag",
      "derived": "formula or operation",
      "transform": {"distribution": "none|log1p|boxcox", "params": {}},
      "imputation": {"method":"none|mean|median|ffill|bfill|mode", "params":{}},
      "encoding": {"method":"none|one_hot|target|embedding", "params":{"dim": number}},
      "scaling": {"method":"standard|minmax|robust|none", "fit":"train_only", "params":{"clip_q":[number,number]}},
      "outliers": {"method":"iqr|quantile|none", "params":{}},
      "per_sequence_normalization": boolean,
      "leakage_risk": {"flag": boolean, "note": "string"},
      "availability": {"online_source": "string", "expected_latency_ms": number, "staleness_max_s": number},
      "oov_policy": {"method": "vocab+unk|hashing", "freeze_after_train": boolean},
      "post_checks": {"allow_nan": boolean, "allow_inf": boolean},
      "dtype": "float32|int64|bool",
      "timestep_dim": number
    }
  ],
  "online_constraints": {"global_latency_ms": number, "freshness_s": number, "train_serve_skew_checks": boolean},
  "feature_budget": {"per_timestep_max": number, "total_max": number},
  "augmentation": {"train_only": boolean, "params": {"jitter": boolean, "time_warp": boolean, "cutout": boolean}},
  "spec_version": "string",
  "data_spec_hash": "string",
  "final_dimensions": {"per_timestep": number, "tensor": "(B,T,F)"}
}

## QA Rubric (check all)
- [ ] Shape totals match (feature table vs JSON).
- [ ] No transform uses future info.
- [ ] Normalization parameters fit on TRAIN only.
- [ ] Timezone/DST & irregular gaps handled.
- [ ] Categorical plan addresses high cardinality & rare bins.
- [ ] Mask/padding compatible with BiLSTM packing.
- [ ] Units & equations specified for reproducibility.
 - [ ] Online availability, latency/freshness, and train–serve skew checks defined.
 - [ ] OOV policy and vocab freeze point specified; hashing fallback if needed.
 - [ ] `delta_t` and `gap_mask` present when irregular sampling occurs.
 - [ ] Feature budget respected or justified.
 - [ ] Augmentations are TRAIN-only and unit-safe.
 - [ ] Spec version and DATA_SPEC hash recorded.

**Output exactly two artifacts**:  
1) A readable table for humans.  
2) The JSON object (valid to the schema).  
No extra commentary.
