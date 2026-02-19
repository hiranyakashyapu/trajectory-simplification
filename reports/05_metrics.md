# 5. Evaluation Metrics

## 5.1 Geometric Metrics

### 5.1.1 Hausdorff Distance

The Hausdorff distance measures the maximum distance between two trajectories, providing a worst-case error bound.

**Definition**:
```
H(A, B) = max(h(A, B), h(B, A))
```

where
```
h(A, B) = max_{a ∈ A} min_{b ∈ B} d(a, b)
```

and d(a, b) is the Haversine distance between points a and b.

**Interpretation**: Lower values indicate better geometric preservation. The Hausdorff distance is sensitive to outliers and provides a conservative error bound.

**Complexity**: O(n × m) where n and m are the sizes of the two trajectories.

### 5.1.2 Average Point-to-Trajectory Error (APTE)

APTE measures the average distance from original points to the simplified trajectory.

**Definition**:
```
APTE = (1/n) × Σ_{i=1}^n min_{p ∈ S} d(original_i, p)
```

where S is the simplified trajectory and d is the distance function (considering both points and line segments).

**Interpretation**: Lower values indicate better average geometric preservation. APTE is less sensitive to outliers than Hausdorff distance.

**Complexity**: O(n × m) where we check each original point against all simplified points and segments.

### 5.1.3 Frechet Distance

The Frechet distance considers the order of points, measuring the minimum leash length needed to walk both trajectories simultaneously.

**Definition**: The discrete Frechet distance is computed using dynamic programming:

```
F(i, j) = max(d(orig[i], simpl[j]), 
              min(F(i-1, j), F(i, j-1), F(i-1, j-1)))
```

where F(i, j) is the Frechet distance between prefixes of length i and j.

**Interpretation**: Lower values indicate better trajectory similarity considering point order. Frechet distance is more suitable for trajectories than Hausdorff distance as it respects temporal ordering.

**Complexity**: O(n × m) using dynamic programming.

## 5.2 Semantic Metrics

### 5.2.1 Turn Preservation Metric

Measures how well turns in the original trajectory are preserved in the simplified trajectory.

**Definition**:
1. Identify turns in original: points with direction change > threshold (e.g., 30°)
2. For each turn, check if there's a selected point within a window
3. Preservation ratio = preserved_turns / total_turns

**Window Size**: Adaptive based on compression ratio: window = max(1, n / k) where n is original size and k is simplified size.

**Interpretation**: Higher values (closer to 1.0) indicate better turn preservation. A value of 1.0 means all turns are preserved.

### 5.2.2 Stop Preservation Metric

Measures how well stops in the original trajectory are preserved.

**Definition**:
1. Identify stop regions: contiguous points with speed < threshold (e.g., 1 m/s) and duration ≥ min_duration (e.g., 30 seconds)
2. For each stop region, check if there's a selected point within the region or nearby
3. Preservation ratio = preserved_stops / total_stops

**Interpretation**: Higher values indicate better stop preservation. Stops are important semantic features that should be preserved even if geometrically close to neighbors.

## 5.3 Compression Metrics

### 5.3.1 Compression Ratio

**Definition**: compression_ratio = original_size / simplified_size

**Interpretation**: Higher values indicate more compression. Typical values range from 2x to 20x.

## 5.4 Performance Metrics

### 5.4.1 Runtime

Execution time in seconds, measured using Python's `time.time()`.

### 5.4.2 Memory Usage

Peak memory usage in megabytes, measured using `tracemalloc`.

### 5.4.3 Throughput

Points processed per second: throughput = trajectory_size / runtime

## 5.5 Metric Selection Rationale

We selected these metrics to provide comprehensive evaluation:

1. **Geometric Quality**: Hausdorff, APTE, and Frechet distances cover worst-case, average, and order-aware geometric errors.

2. **Semantic Quality**: Turn and stop preservation metrics evaluate feature preservation, which is the main contribution of our method.

3. **Efficiency**: Runtime and memory metrics assess practical applicability.

4. **Compression**: Compression ratio ensures fair comparison across methods.

## 5.6 Metric Limitations

- **Hausdorff Distance**: May be overly conservative, sensitive to single outliers
- **Frechet Distance**: Computationally expensive for large trajectories
- **Turn/Stop Preservation**: Window-based matching may not capture all preservation scenarios
- **Runtime**: Depends on implementation and hardware

Despite these limitations, the selected metrics provide a comprehensive evaluation framework.

