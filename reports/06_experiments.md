# 6. Experiments

## 6.1 Experimental Setup

### 6.1.1 Dataset

We used the GeoLife GPS dataset, preprocessed as described in Chapter 3. For experiments, we selected a subset of trajectories with the following criteria:

- Minimum length: 100 points
- Maximum length: 5000 points (for computational feasibility)
- Total trajectories: 20 trajectories (for comprehensive evaluation)
- Total experiments: 400 (20 trajectories × 5 algorithms × 4 compression ratios)

### 6.1.2 Algorithms

We compared the following algorithms:

1. **RDP**: Douglas-Peucker with binary search for budget constraint
2. **Sliding Window**: Window-based with binary search for budget
3. **Uniform**: Uniform sampling
4. **Adaptive**: Adaptive threshold with base_ε=10.0, speed_weight=0.5
5. **Proposed**: Our method with default weights (turn=0.3, stop=0.3, speed=0.2, irregular=0.2)

### 6.1.3 Compression Ratios

We tested the following compression ratios:
- 2x (50% of original points)
- 5x (20% of original points)
- 10x (10% of original points)
- 20x (5% of original points)

### 6.1.4 Evaluation Metrics

For each experiment, we computed:
- Geometric metrics: Hausdorff distance, APTE, Frechet distance
- Semantic metrics: Turn preservation, Stop preservation
- Performance metrics: Runtime, Memory usage
- Compression: Compression ratio

### 6.1.5 Experimental Environment

- **Hardware**: Standard desktop/laptop configuration
- **Software**: Python 3.8+, NumPy, Pandas, SciPy
- **Measurement**: Runtime using `time.time()`, memory using `tracemalloc`
- **Reproducibility**: Fixed random seeds, deterministic algorithms

## 6.2 Experimental Procedure

1. Load preprocessed trajectories
2. For each trajectory:
   - For each algorithm:
     - For each compression ratio:
       - Run simplification
       - Measure runtime and memory
       - Compute all metrics
       - Record results
3. Aggregate results and generate summary statistics

## 6.3 Results Overview

We conducted 400 experiments across 20 trajectories, 5 algorithms, and 4 compression ratios. The results demonstrate clear trade-offs between geometric quality, semantic preservation, and computational efficiency.

### 6.3.1 Geometric Quality

**Hausdorff Distance (meters, mean ± std)**:
- Uniform: 101.18 ± 226.93 (best geometric quality)
- Adaptive: 182.45 ± 213.32
- Sliding Window: 221.57 ± 230.40
- Proposed: 273.37 ± 353.46
- RDP: 629.47 ± 641.98 (highest error, but note: RDP often produces very few points)

**Average Point-to-Trajectory Error (APTE, meters, mean ± std)**:
- Adaptive: 0.02 ± 0.09 (best)
- Sliding Window: 0.01 ± 0.03
- Uniform: 0.65 ± 2.61
- Proposed: 3.52 ± 9.99
- RDP: Not applicable (often produces only endpoints)

**Frechet Distance (meters, mean ± std)**:
- Uniform: 140.99 ± 251.56 (best)
- Adaptive: 258.79 ± 258.44
- Proposed: 370.13 ± 417.12
- Sliding Window: 302.87 ± 280.76
- RDP: Very high (due to extreme compression)

**Key Observations**:
- Uniform sampling achieves the best geometric quality across all metrics
- Proposed method has moderate geometric error (273m Hausdorff) but significantly better than RDP
- RDP's high error is partly due to its tendency to produce very few points (often just 3-6 points)

### 6.3.2 Semantic Preservation

**Turn Preservation (ratio, mean ± std)**:
- Proposed: 0.718 ± 0.202 (72% of turns preserved on average)
- Range: 0.260 - 1.000 (26% to 100% depending on trajectory and compression)
- Other algorithms: Not measured (geometric methods don't explicitly preserve turns)

**Stop Preservation (ratio, mean ± std)**:
- Proposed: 0.707 ± 0.252 (71% of stops preserved on average)
- Range: 0.162 - 1.000 (16% to 100% depending on trajectory and compression)
- Other algorithms: Not measured (geometric methods don't explicitly preserve stops)

**Key Observations**:
- Proposed method successfully preserves 72% of turns and 71% of stops on average
- Preservation decreases with higher compression ratios (as expected)
- At 2x compression, preservation is near-perfect (99%+)
- At 20x compression, preservation drops to 32-53% but still maintains semantic features

### 6.3.3 Performance

**Runtime (seconds, mean ± std)**:
- Uniform: 0.0009 ± 0.0002 (fastest, O(n))
- Proposed: 0.3094 ± 0.2953 (very fast, comparable to RDP)
- RDP: 1.2230 ± 1.2371
- Adaptive: 48.2229 ± 80.0032 (slowest, due to speed computation)
- Sliding Window: 54.8183 ± 74.7062 (slowest, due to iterative error checking)

**Memory Usage (MB, mean ± std)**:
- Uniform: 0.0225 ± 0.0217 (lowest)
- Sliding Window: 0.0295 ± 0.0186
- Proposed: 0.1026 ± 0.0877
- Adaptive: 0.1015 ± 0.0888
- RDP: Variable (depends on recursion depth)

**Key Observations**:
- Uniform sampling is fastest (sub-millisecond)
- Proposed method is very efficient (0.31s average), 4x faster than RDP
- Adaptive and Sliding Window are slow due to iterative computations
- All methods use minimal memory (< 0.5 MB)

## 6.4 Statistical Analysis

### 6.4.1 Compression Ratio Impact

The performance of all algorithms degrades with higher compression ratios, as expected:

**Hausdorff Distance by Compression Ratio**:
- **2x compression**: Uniform (23.17m), Proposed (112.87m)
- **5x compression**: Adaptive (105.06m), Sliding Window (120.06m), Uniform (69.62m), Proposed (218.81m)
- **10x compression**: Adaptive (243.71m), Sliding Window (297.19m), Uniform (93.19m), Proposed (354.11m)
- **20x compression**: Adaptive (237.33m), Sliding Window (414.70m), Uniform (336.33m), Proposed (626.14m)

**Semantic Preservation by Compression Ratio (Proposed Method)**:
- **2x compression**: Turn preservation 99.4%, Stop preservation 99.1%
- **5x compression**: Turn preservation 66.6%, Stop preservation 66.0%
- **10x compression**: Turn preservation decreases further
- **20x compression**: Turn preservation 32.4%, Stop preservation 53.3%

### 6.4.2 Algorithm Comparison Summary

| Algorithm | Hausdorff (m) | APTE (m) | Frechet (m) | Turn Pres. | Stop Pres. | Runtime (s) |
|-----------|---------------|----------|-------------|------------|------------|-------------|
| Uniform | 101.18 | 0.65 | 140.99 | N/A | N/A | 0.0009 |
| Adaptive | 182.45 | 0.02 | 258.79 | N/A | N/A | 48.22 |
| Sliding Window | 221.57 | 0.01 | 302.87 | N/A | N/A | 54.82 |
| Proposed | 273.37 | 3.52 | 370.13 | 0.718 | 0.707 | 0.31 |
| RDP | 629.47 | N/A | Very high | N/A | N/A | 1.22 |

## 6.5 Reproducibility

All experiments were run with fixed random seeds where applicable. Code and data are available for reproducibility.

