"""
PHASE 4: Evaluation Metrics for Trajectory Simplification

This module implements various metrics to evaluate the quality of simplified trajectories:

1. Hausdorff Distance: Maximum distance between trajectories
2. Average Point-to-Trajectory Error: Mean distance from original points to simplified trajectory
3. Frechet Distance: Similarity measure considering order of points
4. Turn Preservation Metric: How well turns are preserved
5. Stop Preservation Metric: How well stops are preserved

Formulas:
- Hausdorff: H(A,B) = max(h(A,B), h(B,A)) where h(A,B) = max_{a in A} min_{b in B} d(a,b)
- Average PTE: (1/n) * sum_{i=1}^n min_{p in S} d(original_i, p)
- Frechet: Minimum leash length needed to walk both trajectories simultaneously
- Turn Preservation: Ratio of preserved turns
- Stop Preservation: Ratio of preserved stops
"""

import numpy as np
import pandas as pd
from typing import Union, Tuple, List, Dict
from scipy.spatial.distance import cdist
from src.algorithms.baseline_algorithms import haversine_distance, point_to_line_distance


def hausdorff_distance(original: np.ndarray, simplified: np.ndarray) -> float:
    """
    Compute Hausdorff distance between two trajectories.
    
    Hausdorff distance is the maximum distance from any point in one trajectory
    to the nearest point in the other trajectory.
    
    Formula:
        H(A,B) = max(h(A,B), h(B,A))
        where h(A,B) = max_{a in A} min_{b in B} d(a,b)
    
    Args:
        original: Original trajectory points (N x 2) with (lat, lon)
        simplified: Simplified trajectory points (M x 2) with (lat, lon)
        
    Returns:
        Hausdorff distance in meters
    """
    if len(original) == 0 or len(simplified) == 0:
        return float('inf')
    
    # Convert to approximate metric coordinates for distance calculation
    # For small distances, we can use simple approximation
    # For better accuracy, we use Haversine for each pair
    
    # Compute distance from each original point to nearest simplified point
    def min_dist_to_trajectory(point, trajectory):
        """Find minimum distance from point to any point in trajectory."""
        min_dist = float('inf')
        for traj_point in trajectory:
            dist = haversine_distance(tuple(point), tuple(traj_point))
            min_dist = min(min_dist, dist)
        return min_dist
    
    # h(original, simplified)
    h_orig_simpl = 0
    for orig_point in original:
        dist = min_dist_to_trajectory(orig_point, simplified)
        h_orig_simpl = max(h_orig_simpl, dist)
    
    # h(simplified, original)
    h_simpl_orig = 0
    for simpl_point in simplified:
        dist = min_dist_to_trajectory(simpl_point, original)
        h_simpl_orig = max(h_simpl_orig, dist)
    
    # Hausdorff distance
    hausdorff = max(h_orig_simpl, h_simpl_orig)
    
    return hausdorff


def average_point_to_trajectory_error(original: np.ndarray, 
                                      simplified: np.ndarray) -> float:
    """
    Compute average point-to-trajectory error.
    
    For each point in the original trajectory, find the minimum distance
    to any point or segment in the simplified trajectory, then average.
    
    Formula:
        APTE = (1/n) * sum_{i=1}^n min_{p in S} d(original_i, p)
    
    Args:
        original: Original trajectory points (N x 2)
        simplified: Simplified trajectory points (M x 2)
        
    Returns:
        Average error in meters
    """
    if len(original) == 0 or len(simplified) == 0:
        return float('inf')
    
    errors = []
    
    for orig_point in original:
        min_dist = float('inf')
        
        # Check distance to points
        for simpl_point in simplified:
            dist = haversine_distance(tuple(orig_point), tuple(simpl_point))
            min_dist = min(min_dist, dist)
        
        # Check distance to line segments
        for i in range(len(simplified) - 1):
            dist = point_to_line_distance(
                tuple(orig_point),
                tuple(simplified[i]),
                tuple(simplified[i + 1])
            )
            min_dist = min(min_dist, dist)
        
        errors.append(min_dist)
    
    return np.mean(errors)


def frechet_distance(original: np.ndarray, simplified: np.ndarray) -> float:
    """
    Compute discrete Frechet distance between two trajectories.
    
    Frechet distance is the minimum leash length needed to walk both trajectories
    simultaneously, where one person walks along the original and another along
    the simplified trajectory.
    
    Algorithm: Dynamic programming
    - F(i,j) = max(d(orig[i], simpl[j]), 
                   min(F(i-1,j), F(i,j-1), F(i-1,j-1)))
    
    Args:
        original: Original trajectory points (N x 2)
        simplified: Simplified trajectory points (M x 2)
        
    Returns:
        Frechet distance in meters
    """
    if len(original) == 0 or len(simplified) == 0:
        return float('inf')
    
    n, m = len(original), len(simplified)
    
    # Precompute distance matrix
    dist_matrix = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            dist_matrix[i, j] = haversine_distance(
                tuple(original[i]),
                tuple(simplified[j])
            )
    
    # Dynamic programming table
    F = np.zeros((n, m))
    F[0, 0] = dist_matrix[0, 0]
    
    # Initialize first row
    for j in range(1, m):
        F[0, j] = max(F[0, j-1], dist_matrix[0, j])
    
    # Initialize first column
    for i in range(1, n):
        F[i, 0] = max(F[i-1, 0], dist_matrix[i, 0])
    
    # Fill table
    for i in range(1, n):
        for j in range(1, m):
            F[i, j] = max(
                dist_matrix[i, j],
                min(F[i-1, j], F[i, j-1], F[i-1, j-1])
            )
    
    return F[n-1, m-1]


def turn_preservation_metric(original: pd.DataFrame,
                            simplified: pd.DataFrame,
                            original_indices: List[int],
                            turn_threshold: float = 30.0) -> Tuple[float, Dict]:
    """
    Compute turn preservation metric.
    
    Measures how well turns in the original trajectory are preserved
    in the simplified trajectory.
    
    Args:
        original: Original trajectory DataFrame
        simplified: Simplified trajectory DataFrame
        original_indices: Indices of original points that were kept
        turn_threshold: Direction change threshold for turn (degrees)
        
    Returns:
        Tuple of (preservation_ratio, metrics_dict)
    """
    from src.utils.geolife_loader import compute_trajectory_properties
    
    # Compute turns in original trajectory
    orig_props = compute_trajectory_properties(original)
    
    if 'direction_changes' not in orig_props:
        return 0.0, {}
    
    # Identify turns in original
    orig_turns = orig_props['direction_changes'] > turn_threshold
    orig_turn_indices = np.where(orig_turns)[0].tolist()
    
    if len(orig_turn_indices) == 0:
        return 1.0, {'original_turns': 0, 'preserved_turns': 0, 'preservation_ratio': 1.0}
    
    # Check which turns are preserved (within small window of selected points)
    preserved_turns = 0
    window_size = max(1, len(original) // len(simplified))
    
    for turn_idx in orig_turn_indices:
        # Check if there's a selected point near this turn
        for sel_idx in original_indices:
            if abs(sel_idx - turn_idx) <= window_size:
                preserved_turns += 1
                break
    
    preservation_ratio = preserved_turns / len(orig_turn_indices)
    
    metrics = {
        'original_turns': len(orig_turn_indices),
        'preserved_turns': preserved_turns,
        'preservation_ratio': preservation_ratio
    }
    
    return preservation_ratio, metrics


def stop_preservation_metric(original: pd.DataFrame,
                            simplified: pd.DataFrame,
                            original_indices: List[int],
                            stop_threshold: float = 1.0,
                            min_duration: float = 30.0) -> Tuple[float, Dict]:
    """
    Compute stop preservation metric.
    
    Measures how well stops in the original trajectory are preserved
    in the simplified trajectory.
    
    Args:
        original: Original trajectory DataFrame
        simplified: Simplified trajectory DataFrame
        original_indices: Indices of original points that were kept
        stop_threshold: Speed threshold for stop (m/s)
        min_duration: Minimum duration for significant stop (seconds)
        
    Returns:
        Tuple of (preservation_ratio, metrics_dict)
    """
    from src.utils.geolife_loader import compute_trajectory_properties
    
    # Compute stops in original trajectory
    orig_props = compute_trajectory_properties(original)
    
    if 'speeds' not in orig_props:
        return 0.0, {}
    
    # Identify stop regions
    speeds = orig_props['speeds']
    is_stop = speeds < stop_threshold
    
    # Find contiguous stop regions
    stop_regions = []
    i = 0
    while i < len(is_stop):
        if is_stop[i]:
            start = i
            while i < len(is_stop) and is_stop[i]:
                i += 1
            end = i - 1
            
            # Check duration
            if 'timestamp' in original.columns:
                duration = (pd.to_datetime(original['timestamp'].iloc[end]) - 
                           pd.to_datetime(original['timestamp'].iloc[start])).total_seconds()
            else:
                duration = end - start  # Assume 1 second per point
            
            if duration >= min_duration:
                stop_regions.append((start, end))
        else:
            i += 1
    
    if len(stop_regions) == 0:
        return 1.0, {'original_stops': 0, 'preserved_stops': 0, 'preservation_ratio': 1.0}
    
    # Check which stops are preserved
    preserved_stops = 0
    window_size = max(1, len(original) // len(simplified))
    
    for start, end in stop_regions:
        # Check if there's a selected point in this stop region
        stop_center = (start + end) // 2
        for sel_idx in original_indices:
            if start <= sel_idx <= end or abs(sel_idx - stop_center) <= window_size:
                preserved_stops += 1
                break
    
    preservation_ratio = preserved_stops / len(stop_regions)
    
    metrics = {
        'original_stops': len(stop_regions),
        'preserved_stops': preserved_stops,
        'preservation_ratio': preservation_ratio
    }
    
    return preservation_ratio, metrics


def compression_ratio(original: np.ndarray, simplified: np.ndarray) -> float:
    """
    Compute compression ratio.
    
    Args:
        original: Original trajectory
        simplified: Simplified trajectory
        
    Returns:
        Compression ratio (original_size / simplified_size)
    """
    if len(simplified) == 0:
        return float('inf')
    return len(original) / len(simplified)


def compute_all_metrics(original: pd.DataFrame,
                       simplified: np.ndarray,
                       original_indices: List[int] = None) -> Dict:
    """
    Compute all evaluation metrics for a simplified trajectory.
    
    Args:
        original: Original trajectory DataFrame
        simplified: Simplified trajectory points (N x 2)
        original_indices: Indices of original points (if available)
        
    Returns:
        Dictionary with all metrics
    """
    original_points = original[['lat', 'lon']].values
    
    # Geometric metrics
    hausdorff = hausdorff_distance(original_points, simplified)
    apte = average_point_to_trajectory_error(original_points, simplified)
    frechet = frechet_distance(original_points, simplified)
    
    # Compression
    comp_ratio = compression_ratio(original_points, simplified)
    
    metrics = {
        'hausdorff_distance': hausdorff,
        'average_pte': apte,
        'frechet_distance': frechet,
        'compression_ratio': comp_ratio,
        'original_points': len(original_points),
        'simplified_points': len(simplified)
    }
    
    # Feature preservation metrics (if indices available)
    if original_indices is not None:
        # Create simplified DataFrame for feature metrics
        simplified_df = pd.DataFrame(simplified, columns=['lat', 'lon'])
        if 'timestamp' in original.columns:
            simplified_df['timestamp'] = original.iloc[original_indices]['timestamp'].values
        
        turn_pres, turn_metrics = turn_preservation_metric(
            original, simplified_df, original_indices
        )
        stop_pres, stop_metrics = stop_preservation_metric(
            original, simplified_df, original_indices
        )
        
        metrics.update({
            'turn_preservation': turn_pres,
            'stop_preservation': stop_pres,
            **turn_metrics,
            **stop_metrics
        })
    
    return metrics


if __name__ == "__main__":
    # Example usage
    import pandas as pd
    
    # Create sample trajectories
    n = 100
    original = pd.DataFrame({
        'lat': np.linspace(0, 1, n) + np.random.normal(0, 0.01, n),
        'lon': np.linspace(0, 1, n) + np.random.normal(0, 0.01, n),
        'timestamp': pd.date_range('2023-01-01', periods=n, freq='1min')
    })
    
    # Simplified (every 5th point)
    simplified = original.iloc[::5][['lat', 'lon']].values
    indices = list(range(0, n, 5))
    
    # Compute metrics
    metrics = compute_all_metrics(original, simplified, indices)
    
    print("Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")

