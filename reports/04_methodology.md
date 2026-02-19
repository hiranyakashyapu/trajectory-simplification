# 4. Methodology

## 4.1 Baseline Algorithms

We implemented four baseline algorithms for comparison:

### 4.1.1 Douglas-Peucker (RDP)

**Algorithm**: Recursive point elimination based on perpendicular distance.

**Parameters**: ε (error threshold)

**Complexity**: O(n²) worst case, O(n log n) average

**Strengths**: 
- Excellent geometric preservation
- Well-established and widely used

**Weaknesses**:
- Ignores temporal and semantic information
- May remove important points in irregular sampling regions
- Sensitive to noise

### 4.1.2 Sliding Window

**Algorithm**: Linear-time window-based simplification.

**Parameters**: ε (error threshold)

**Complexity**: O(n)

**Strengths**:
- Fast execution
- Handles local variations

**Weaknesses**:
- May miss global patterns
- Does not preserve semantic features
- Sensitive to local noise

### 4.1.3 Uniform Sampling

**Algorithm**: Select points at regular intervals.

**Parameters**: k (number of points)

**Complexity**: O(n)

**Strengths**:
- Extremely fast
- Simple implementation
- Predictable compression

**Weaknesses**:
- Ignores trajectory shape
- May skip important points
- Not adaptive to trajectory characteristics

### 4.1.4 Adaptive Threshold

**Algorithm**: Sliding window with speed-adaptive error threshold.

**Parameters**: base_ε, speed_weight

**Complexity**: O(n)

**Strengths**:
- Considers speed information
- Adapts to trajectory dynamics

**Weaknesses**:
- Sensitive to speed measurement noise
- Does not explicitly preserve stops or turns
- May not handle irregular sampling well

## 4.2 Proposed Method

### 4.2.1 Overview

Our proposed method combines geometric and semantic importance scoring to preserve important trajectory features under fixed compression budgets. The algorithm consists of three main steps:

1. **Importance Scoring**: Compute multi-dimensional importance scores for all points
2. **Point Selection**: Select top-k points by importance
3. **Geometric Refinement**: Refine selection to ensure geometric quality

### 4.2.2 Importance Scoring Framework

We define the importance of a point p_i as a weighted combination of four components:

```
importance(p_i) = w_turn × turn_score(p_i) + 
                  w_stop × stop_score(p_i) + 
                  w_speed × speed_change_score(p_i) + 
                  w_irregular × irregularity_score(p_i)
```

where w_turn + w_stop + w_speed + w_irregular = 1.

#### Turn Score

The turn score measures the significance of direction changes:

1. Compute bearings (directions) for each segment
2. Calculate direction changes between consecutive segments
3. Smooth direction changes to reduce noise
4. Normalize to [0, 1]
5. Boost scores for points with high local variance (sharp turns)

**Mathematical Formulation**:
- Bearing: θ_i = atan2(sin(Δlon) × cos(lat₂), cos(lat₁) × sin(lat₂) - sin(lat₁) × cos(lat₂) × cos(Δlon))
- Direction change: Δθ_i = min(|θ_i - θ_{i-1}|, 360° - |θ_i - θ_{i-1}|)
- Turn score: turn_score(p_i) = normalized(Δθ_i) × (1 + 0.5 × local_variance)

#### Stop Score

The stop score measures the significance of low-speed regions:

1. Compute speeds for each point
2. Identify stop regions (speed < threshold, e.g., 1 m/s)
3. Compute stop durations
4. Score based on duration (longer stops are more important)
5. Boost scores for stops above minimum duration threshold

**Mathematical Formulation**:
- Speed: v_i = distance(p_i, p_{i-1}) / time_interval(i, i-1)
- Stop indicator: is_stop(p_i) = 1 if v_i < threshold, else 0
- Stop duration: duration(p_i) = length of contiguous stop region containing p_i
- Stop score: stop_score(p_i) = normalized(duration(p_i)) × boost_factor

#### Speed Change Score

The speed change score measures acceleration/deceleration significance:

1. Compute speeds for each point
2. Calculate speed changes (|v_i - v_{i-1}|)
3. Smooth to reduce noise
4. Normalize to [0, 1]

**Mathematical Formulation**:
- Speed change: Δv_i = |v_i - v_{i-1}|
- Speed change score: speed_score(p_i) = normalized(smoothed(Δv_i))

#### Irregularity Score

The irregularity score measures sampling sparsity:

1. Compute time intervals between consecutive points
2. Normalize by median interval
3. Boost scores for points with very large gaps

**Mathematical Formulation**:
- Time interval: Δt_i = timestamp(p_i) - timestamp(p_{i-1})
- Median interval: median_Δt = median({Δt_i})
- Irregularity score: irregular_score(p_i) = min(Δt_i / (3 × median_Δt), 1.0)
- Boost: irregular_score(p_i) = 1.0 if Δt_i > 5 × median_Δt

### 4.2.3 Point Selection

Given a compression budget k:

1. Compute importance scores for all points
2. Always include first and last points (importance = 1.0)
3. Select top-(k-2) points from remaining points
4. Sort selected indices

### 4.2.4 Geometric Refinement

To ensure geometric quality while preserving semantic features:

1. For each consecutive pair of selected points (p_i, p_j):
   - Compute maximum perpendicular error for intermediate points
   - If error > threshold and budget allows:
     - Add point with maximum error
2. If budget exceeded, remove least important points (except first/last)

### 4.2.5 Algorithm Pseudocode

```
function ProposedSimplification(T, budget, weights):
    // T: trajectory, budget: target number of points
    
    // Step 1: Compute importance scores
    turn_scores = ComputeTurnScores(T)
    stop_scores = ComputeStopScores(T)
    speed_scores = ComputeSpeedChangeScores(T)
    irregular_scores = ComputeIrregularityScores(T)
    
    // Step 2: Combine scores
    importance = weights.turn × turn_scores +
                 weights.stop × stop_scores +
                 weights.speed × speed_scores +
                 weights.irregular × irregular_scores
    
    importance[0] = 1.0  // Always include first
    importance[-1] = 1.0  // Always include last
    
    // Step 3: Select top-k points
    selected = [0] + top_k(importance[1:-1], budget-2) + [len(T)-1]
    selected = sort(selected)
    
    // Step 4: Geometric refinement
    refined = GeometricRefinement(T, selected, budget, error_threshold)
    
    return T[refined], refined
```

### 4.2.6 Why It Handles Irregular Sampling and Noise Better

1. **Irregular Sampling**: The irregularity score explicitly identifies points in sparse regions, ensuring they are preserved even if geometrically close to neighbors.

2. **Noise Robustness**: 
   - Turn and speed change scores use smoothing to reduce noise impact
   - Stop scores use duration-based scoring, which is more robust than single-point speed measurements
   - Geometric refinement ensures quality even with noisy importance scores

3. **Semantic Preservation**: By explicitly scoring turns, stops, and speed changes, the method preserves these features even when they don't align with geometric error minimization.

4. **Fixed Budget**: Unlike threshold-based methods, the algorithm works directly with compression budgets, making it suitable for storage/transmission-constrained applications.

## 4.3 Implementation Details

### 4.3.1 Default Parameters

- Turn threshold: 30 degrees
- Stop threshold: 1.0 m/s (≈ 3.6 km/h)
- Minimum stop duration: 30 seconds
- Default weights: w_turn = 0.3, w_stop = 0.3, w_speed = 0.2, w_irregular = 0.2
- Geometric error threshold: 5.0 meters

### 4.3.2 Complexity Analysis

- Importance scoring: O(n) for each component, total O(n)
- Point selection: O(n log k) for top-k selection
- Geometric refinement: O(n × k) in worst case
- **Total Complexity**: O(n × k) worst case, O(n log k) average case

This is comparable to RDP's O(n log n) average case and better than RDP's O(n²) worst case when k << n.

