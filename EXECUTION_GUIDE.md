# Complete Execution Guide

## Prerequisites

1. Python 3.8 or higher
2. All dependencies installed: `pip install -r requirements.txt`
3. GeoLife dataset (already present in `data/geolife/`)

## Complete Workflow

### Step 1: Preprocess GeoLife Dataset

```bash
cd /home/sanjay/Desktop/CSIT-8-PROJECT
python src/utils/preprocess_geolife.py
```

**Expected Output**:
- `data/processed/trajectories.pkl` - Preprocessed trajectories
- `data/processed/trajectory_properties.csv` - Trajectory statistics

**Time**: ~5-10 minutes depending on dataset size

### Step 2: Run Full Experiments

```bash
python src/experiments/run_experiments.py \
    --max-trajectories 50 \
    --compression-ratios 2.0 5.0 10.0 20.0 \
    --algorithms rdp sliding_window uniform adaptive proposed \
    --data-file data/processed/trajectories.pkl
```

**Expected Output**:
- `results/experiment_results.csv` - Detailed results for all experiments
- `results/summary_table.csv` - Aggregated statistics

**Time**: ~30-60 minutes depending on number of trajectories

### Step 3: Generate All Visualizations

```bash
python src/experiments/generate_plots.py \
    --results-file results/experiment_results.csv \
    --trajectories-file data/processed/trajectories.pkl \
    --output-dir results/figures
```

**Expected Output**:
- `results/figures/trajectory_comparison.png` - Algorithm comparison
- `results/figures/compression_error_curves.png` - Error vs compression
- `results/figures/runtime_scalability.png` - Performance analysis
- `results/figures/metric_comparison_*.png` - Metric comparisons

**Time**: ~2-5 minutes

### Step 4: Analyze Results

#### Option A: Using Python

```python
import pandas as pd

# Load results
results = pd.read_csv('results/experiment_results.csv')
summary = pd.read_csv('results/summary_table.csv')

# View summary
print(summary)

# Filter by algorithm
rdp_results = results[results['algorithm'] == 'rdp']
proposed_results = results[results['algorithm'] == 'proposed']

# Compare turn preservation
print("RDP Turn Preservation:", rdp_results['turn_preservation'].mean())
print("Proposed Turn Preservation:", proposed_results['turn_preservation'].mean())
```

#### Option B: Using Jupyter Notebook

```bash
jupyter notebook notebooks/01_dataset_analysis.ipynb
```

## Quick Test (Small Scale)

For quick testing with fewer trajectories:

```bash
# Preprocess (small subset)
python src/utils/preprocess_geolife.py  # Will process available trajectories

# Run experiments (small scale)
python src/experiments/run_experiments.py \
    --max-trajectories 5 \
    --compression-ratios 5.0 10.0 \
    --algorithms rdp proposed

# Generate plots
python src/experiments/generate_plots.py
```

## Testing Individual Components

### Test Dataset Loading

```python
from src.utils.geolife_loader import GeoLifeLoader

loader = GeoLifeLoader("data/geolife")
trajectories = loader.load_all_trajectories(max_users=5, min_points=100)
print(f"Loaded {len(trajectories)} trajectories")
```

### Test Single Algorithm

```python
import pickle
from src.algorithms.baseline_algorithms import simplify_with_budget

# Load trajectory
with open('data/processed/trajectories.pkl', 'rb') as f:
    trajectories = pickle.load(f)

traj = trajectories[0]
budget = len(traj) // 5  # 5x compression

# Test RDP
simplified = simplify_with_budget(traj, 'rdp', budget)
print(f"RDP: {len(traj)} -> {len(simplified)} points")
```

### Test Proposed Method

```python
from src.algorithms.proposed_method import proposed_simplification

simplified, indices = proposed_simplification(traj, budget)
print(f"Proposed: {len(traj)} -> {len(simplified)} points")
print(f"Selected {len(indices)} indices")
```

### Test Metrics

```python
from src.metrics.evaluation_metrics import compute_all_metrics

metrics = compute_all_metrics(traj, simplified, indices)
for key, value in metrics.items():
    print(f"{key}: {value}")
```

## Scalability Testing

```python
from src.utils.synthetic_generator import scalability_test

results = scalability_test(
    algorithms=['rdp', 'sliding_window', 'uniform', 'proposed'],
    trajectory_sizes=[100, 200, 500, 1000, 2000, 5000],
    compression_ratio=5.0,
    n_trajectories_per_size=3
)

# Save results
results.to_csv('results/scalability_results.csv', index=False)

# Analyze
print(results.groupby(['algorithm', 'trajectory_size'])['runtime_seconds'].mean())
```

## Customizing Experiments

### Change Algorithm Parameters

Edit `config/experiment_config.yaml` or pass parameters directly:

```python
from src.experiments.run_experiments import ExperimentRunner
import pickle

with open('data/processed/trajectories.pkl', 'rb') as f:
    trajectories = pickle.load(f)

runner = ExperimentRunner(trajectories)

# Custom parameters
algorithm_params = {
    'proposed': {
        'weights': {'turn': 0.4, 'stop': 0.4, 'speed': 0.1, 'irregular': 0.1}
    }
}

results = runner.run_batch_experiments(
    algorithms=['proposed'],
    compression_ratios=[5.0],
    algorithm_params=algorithm_params
)
```

### Add New Metrics

Edit `src/metrics/evaluation_metrics.py` to add new metrics, then update `compute_all_metrics()`.

### Add New Algorithms

1. Implement algorithm in `src/algorithms/`
2. Add to `simplify_with_budget()` in `baseline_algorithms.py`
3. Add to experiment runner

## Troubleshooting

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from project root directory:
```bash
cd /home/sanjay/Desktop/CSIT-8-PROJECT
python src/experiments/run_experiments.py
```

Or add to Python path:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```

### Memory Issues

**Error**: Out of memory

**Solutions**:
- Reduce `--max-trajectories`
- Process in batches
- Use smaller compression ratios
- Close other applications

### Slow Execution

**Solutions**:
- Use fewer trajectories for testing
- Skip expensive metrics (comment out Frechet distance)
- Use uniform sampling for quick tests
- Run on faster hardware

### Missing Data

**Error**: File not found

**Solutions**:
- Check file paths
- Run preprocessing first
- Verify dataset is in correct location

## Expected Results Format

### experiment_results.csv

Columns:
- `trajectory_id`: Trajectory index
- `algorithm`: Algorithm name
- `compression_ratio`: Compression ratio used
- `budget`: Number of points in simplified trajectory
- `hausdorff_distance`: Hausdorff distance (meters)
- `average_pte`: Average point-to-trajectory error (meters)
- `frechet_distance`: Frechet distance (meters)
- `turn_preservation`: Turn preservation ratio [0, 1]
- `stop_preservation`: Stop preservation ratio [0, 1]
- `runtime_seconds`: Execution time
- `memory_mb`: Peak memory usage

### summary_table.csv

Aggregated statistics (mean ± std) grouped by algorithm and compression ratio.

## Next Steps After Execution

1. **Analyze Results**: Review `results/experiment_results.csv`
2. **Update Reports**: Fill in actual numbers in report sections
3. **Generate Thesis**: Combine report sections into final thesis
4. **Prepare Defense**: Review viva preparation guide
5. **Write Paper**: Use results for publication (if applicable)

## Performance Benchmarks

Expected performance on typical hardware:

- **Preprocessing**: ~1-2 seconds per trajectory
- **RDP**: ~0.1-1 second per trajectory (depends on size)
- **Proposed Method**: ~0.2-2 seconds per trajectory
- **Metrics**: ~0.5-5 seconds per trajectory (Frechet is expensive)

For 50 trajectories × 4 compression ratios × 5 algorithms = 1000 experiments:
- Total time: ~1-3 hours (depending on trajectory sizes)

## Tips for Success

1. **Start Small**: Test with 5-10 trajectories first
2. **Monitor Progress**: Use `tqdm` progress bars
3. **Save Frequently**: Results are saved incrementally
4. **Check Logs**: Review any error messages
5. **Validate Results**: Check that results make sense
6. **Backup Data**: Keep backups of processed data

## Getting Help

- Check code docstrings for function documentation
- Review report sections for methodology
- Test individual components before full pipeline
- Use synthetic data for quick testing
- Check error messages carefully

---

**Ready to execute!** Follow the steps above to run the complete project workflow.

