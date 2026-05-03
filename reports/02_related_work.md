# 2. Related Work

## 2.1 Trajectory Simplification Algorithms

Trajectory simplification has been extensively studied in computational geometry, geographic information systems (GIS), and data mining. Existing approaches can be broadly categorized into geometric, temporal, and semantic methods.

### 2.1.1 Geometric Methods

**Douglas-Peucker Algorithm (DP)**: The most widely used geometric simplification algorithm, originally proposed for line generalization [Douglas and Peucker, 1973]. It recursively finds the point with maximum perpendicular distance from the line segment connecting endpoints. If this distance exceeds a threshold ε, the algorithm recursively processes both sub-segments. DP has O(n²) worst-case complexity but O(n log n) average case. While effective for geometric preservation, DP ignores temporal and semantic information.

**Sliding Window (SW)**: A linear-time algorithm that maintains a window of points and extends it until the error exceeds a threshold [Keogh et al., 2001]. The last point before threshold violation is kept, and a new window starts. This method is efficient but may miss global patterns and is sensitive to local noise.

**Uniform Sampling (US)**: The simplest method, selecting points at regular intervals. While computationally efficient, it ignores trajectory shape and may skip important points.

### 2.1.2 Temporal Methods

**Time-Aware Simplification**: Methods that consider temporal aspects, such as preserving points with significant time gaps [Meratnia and de By, 2004]. These methods address irregular sampling but may not preserve semantic features.

**Speed-Based Methods**: Algorithms that adjust simplification based on speed, preserving more points in high-speed regions [Potamias et al., 2006]. However, these methods may not distinguish between important and unimportant speed changes.

### 2.1.3 Semantic Methods

**Stop-Preserving Methods**: Algorithms specifically designed to preserve stop locations [Long et al., 2013]. These methods identify stops and ensure their representation in simplified trajectories but may not handle turns or speed changes effectively.

**Turn-Preserving Methods**: Methods that detect and preserve turning points [Chen et al., 2018]. These approaches often use direction change thresholds but may not integrate with other semantic features.

**Multi-Feature Methods**: Recent work has attempted to preserve multiple features simultaneously [Zheng et al., 2019], but these methods often lack a unified framework for feature importance scoring.

## 2.2 Evaluation Metrics

### 2.2.1 Geometric Metrics

**Hausdorff Distance**: Measures the maximum distance between two trajectories, providing a worst-case error bound [Alt and Guibas, 1999].

**Average Point-to-Trajectory Error (APTE)**: Computes the average distance from original points to the simplified trajectory, providing a mean error measure.

**Frechet Distance**: Considers the order of points, measuring the minimum leash length needed to walk both trajectories simultaneously [Alt and Guibas, 1999]. This metric is more suitable for trajectories than Hausdorff distance.

### 2.2.2 Semantic Metrics

**Turn Preservation**: Measures the ratio of preserved turns in simplified trajectories [Chen et al., 2018]. However, existing metrics may not account for turn significance.

**Stop Preservation**: Evaluates how well stops are preserved [Long et al., 2013]. Similar to turn preservation, existing metrics may not consider stop duration or significance.

## 2.3 Research Gaps

While existing methods address various aspects of trajectory simplification, several gaps remain:

1. **Unified Feature Preservation**: Most methods focus on a single feature type (e.g., stops or turns) rather than integrating multiple semantic features.

2. **Fixed Budget Constraint**: Many methods use error thresholds rather than fixed compression budgets, making it difficult to control storage/transmission costs.

3. **Irregular Sampling Handling**: While some methods address irregular sampling, they often do not integrate this with semantic feature preservation.

4. **Comprehensive Evaluation**: Limited work provides comprehensive evaluation across both geometric and semantic metrics on real-world datasets.

## 2.4 Our Approach

This research addresses these gaps by:

1. Proposing a unified importance scoring framework that combines turn, stop, speed change, and irregularity scores
2. Designing an algorithm that works under fixed compression budgets
3. Integrating geometric refinement to ensure quality while preserving semantic features
4. Providing comprehensive evaluation on real-world GPS data with multiple metrics

