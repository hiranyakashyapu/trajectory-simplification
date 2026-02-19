# Quick Start Guide

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download GeoLife Dataset** (Optional - you can use synthetic data for testing):
   - Visit: https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/
   - Extract to `data/geolife/Data/`
   - Structure should be: `data/geolife/Data/000/Trajectory/*.plt`

## Quick Test (Using Synthetic Data)

If you don't have the GeoLife dataset yet, you can test with synthetic data:

```python
from src.utils.synthetic_generator import generate_synthetic_trajectory
from src.algorithms.proposed_method import proposed_simplification
from src.metrics.evaluation_metrics import compute_all_metrics
import pandas as pd

# Generate synthetic trajectory
traj = generate_synthetic_trajectory(200, irregular_sampling=True, include_turns=True, seed=42)

# Simplify with proposed method
budget = 40  # 5x compression
simplified, indices = proposed_simplification(traj, budget)

# Evaluate
metrics = compute_all_metrics(traj, simplified, indices)
print("Metrics:", metrics)
```

## Full Workflow

### Step 1: Preprocess Data (if using GeoLife)

```bash
python src/utils/preprocess_geolife.py
```

This will:
- Load trajectories from `data/geolife/`
- Clean and preprocess
- Save to `data/processed/trajectories.pkl`

### Step 2: Run Experiments

```bash
python src/experiments/run_experiments.py \
    --max-trajectories 20 \
    --compression-ratios 2.0 5.0 10.0 \
    --algorithms rdp sliding_window uniform adaptive proposed
```

This will:
- Run all algorithms on trajectories
- Test multiple compression ratios
- Compute all metrics
- Save results to `results/experiment_results.csv`

### Step 3: Generate Visualizations

```bash
python src/experiments/generate_plots.py
```

This will generate:
- Trajectory comparison plots
- Compression vs error curves
- Runtime scalability plots
- Metric comparison charts

### Step 4: Analyze Results

Open `results/experiment_results.csv` and `results/summary_table.csv` to analyze results.

Or use the Jupyter notebook:
```bash
jupyter notebook notebooks/01_dataset_analysis.ipynb
```

## Project Structure Overview

- **`src/algorithms/`**: All simplification algorithms
- **`src/metrics/`**: Evaluation metrics
- **`src/utils/`**: Data loading, preprocessing, synthetic generation
- **`src/experiments/`**: Experiment runners and visualization
- **`notebooks/`**: Jupyter notebooks for analysis
- **`reports/`**: Thesis/report sections
- **`config/`**: Configuration files

## Key Files

- **`src/algorithms/baseline_algorithms.py`**: RDP, Sliding Window, Uniform, Adaptive
- **`src/algorithms/proposed_method.py`**: Our proposed turn/speed/stop-aware method
- **`src/metrics/evaluation_metrics.py`**: All evaluation metrics
- **`src/experiments/run_experiments.py`**: Main experiment runner
- **`src/experiments/generate_plots.py`**: Visualization generator

## Common Tasks

### Test a Single Algorithm

```python
from src.algorithms.baseline_algorithms import simplify_with_budget
import pandas as pd

# Load trajectory
traj = pd.read_pickle('data/processed/trajectories.pkl')[0]

# Simplify with RDP
budget = len(traj) // 5  # 5x compression
simplified = simplify_with_budget(traj, 'rdp', budget)
print(f"Simplified from {len(traj)} to {len(simplified)} points")
```

### Compare Algorithms Visually

```python
from src.experiments.generate_plots import plot_trajectory_comparison
import pickle

# Load trajectory
with open('data/processed/trajectories.pkl', 'rb') as f:
    trajectories = pickle.load(f)

traj = trajectories[0]

# Plot comparison
plot_trajectory_comparison(
    traj,
    ['rdp', 'sliding_window', 'uniform', 'proposed'],
    compression_ratio=5.0,
    output_path='comparison.png'
)
```

### Run Scalability Test

```python
from src.utils.synthetic_generator import scalability_test

results = scalability_test(
    algorithms=['rdp', 'sliding_window', 'uniform', 'proposed'],
    trajectory_sizes=[100, 200, 500, 1000, 2000],
    compression_ratio=5.0
)

print(results.groupby(['algorithm', 'trajectory_size'])['runtime_seconds'].mean())
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the project root:
```bash
cd /home/sanjay/Desktop/CSIT-8-PROJECT
python src/experiments/run_experiments.py
```

Or add the project root to Python path:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```

### Memory Issues

If you run out of memory:
- Reduce `--max-trajectories`
- Use smaller compression ratios
- Process trajectories in batches

### Slow Execution

For faster testing:
- Use fewer trajectories (`--max-trajectories 5`)
- Use fewer compression ratios
- Skip expensive metrics (Frechet distance)

## Next Steps

1. Read the full README.md for detailed documentation
2. Review report sections in `reports/` for thesis content
3. Check `reports/10_viva_preparation.md` for defense preparation
4. Review `reports/11_reproducibility.md` for reproducibility guidelines

## Getting Help

- Check code docstrings for function documentation
- Review report sections for methodology explanations
- Test on small examples first
- Check error messages carefully

