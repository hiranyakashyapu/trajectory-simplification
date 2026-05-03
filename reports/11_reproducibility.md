# PHASE 11: Reproducibility

## 11.1 Folder Structure

```
CSIT-8-PROJECT/
├── data/
│   ├── geolife/              # Raw GeoLife dataset
│   │   └── Data/             # User folders with .plt files
│   └── processed/            # Preprocessed trajectories
│       ├── trajectories.pkl
│       └── trajectory_properties.csv
├── src/
│   ├── algorithms/           # Simplification algorithms
│   │   ├── baseline_algorithms.py
│   │   └── proposed_method.py
│   ├── metrics/             # Evaluation metrics
│   │   └── evaluation_metrics.py
│   ├── utils/               # Utility functions
│   │   ├── geolife_loader.py
│   │   ├── preprocess_geolife.py
│   │   └── synthetic_generator.py
│   └── experiments/         # Experiment runners
│       ├── run_experiments.py
│       └── generate_plots.py
├── notebooks/               # Jupyter notebooks
│   └── 01_dataset_analysis.ipynb
├── results/
│   ├── figures/             # Generated plots
│   └── tables/              # Result tables
│       ├── experiment_results.csv
│       └── summary_table.csv
├── reports/                 # Thesis/report sections
│   ├── 01_introduction.md
│   ├── 02_related_work.md
│   ├── ...
│   └── 11_reproducibility.md
├── config/                  # Configuration files
│   └── experiment_config.yaml
├── requirements.txt         # Python dependencies
├── README.md               # Project overview
└── .gitignore             # Git ignore file
```

## 11.2 Notebook Layout

### 11.2.1 Dataset Analysis Notebook

`notebooks/01_dataset_analysis.ipynb`:
- Load and visualize trajectories
- Compute trajectory properties
- Analyze sampling irregularity
- Plot examples

### 11.2.2 Experiment Notebooks (Optional)

Additional notebooks can be created for:
- Algorithm comparison
- Parameter sensitivity analysis
- Case studies

## 11.3 Experiment Configuration

### 11.3.1 Configuration File

Create `config/experiment_config.yaml`:

```yaml
experiments:
  max_trajectories: 50
  compression_ratios: [2.0, 5.0, 10.0, 20.0]
  algorithms:
    - original
    - dp
    - squish
    - vw
    - sw
    - rw
    - proposed
  
  algorithm_params:
    adaptive:
      base_epsilon: 10.0
      speed_weight: 0.5
    proposed:
      weights:
        turn: 0.3
        stop: 0.3
        speed: 0.2
        irregular: 0.2

dataset:
  data_file: "data/processed/trajectories.pkl"
  min_points: 100
  max_points: 5000

output:
  results_dir: "results"
  figures_dir: "results/figures"
  tables_dir: "results/tables"
```

### 11.3.2 Using Configuration

```python
import yaml

with open('config/experiment_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use config in experiments
max_trajectories = config['experiments']['max_trajectories']
compression_ratios = config['experiments']['compression_ratios']
```

## 11.4 Seed Control

### 11.4.1 Setting Seeds

Always set random seeds for reproducibility:

```python
import numpy as np
import random

# Set seeds
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# For reproducibility, set seed at the start of each script
```

### 11.4.2 Seed in Experiments

```python
# In run_experiments.py
def main():
    np.random.seed(42)
    random.seed(42)
    # ... rest of code
```

## 11.5 Reproducibility Checklist

### 11.5.1 Code Reproducibility

- [ ] All random operations use fixed seeds
- [ ] Code is well-documented with comments
- [ ] Functions have docstrings explaining parameters
- [ ] Version numbers for dependencies are specified
- [ ] Code is organized and modular

### 11.5.2 Data Reproducibility

- [ ] Dataset source is documented
- [ ] Preprocessing steps are clearly described
- [ ] Preprocessed data is saved and versioned
- [ ] Data loading is deterministic

### 11.5.3 Experiment Reproducibility

- [ ] All parameters are documented
- [ ] Configuration files are included
- [ ] Experiment scripts are executable
- [ ] Results are saved with timestamps/versions
- [ ] Random seeds are set and documented

### 11.5.4 Result Reproducibility

- [ ] Results tables are saved
- [ ] Plots are saved with code
- [ ] Summary statistics are computed
- [ ] Results match across runs

## 11.6 Running Experiments

### 11.6.1 Step-by-Step Execution

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Dataset**:
   - Download GeoLife dataset to `data/geolife/`
   - Or use synthetic data for testing

3. **Preprocess Data**:
   ```bash
   python src/utils/preprocess_geolife.py
   ```

4. **Run Experiments**:
   ```bash
   python src/experiments/run_experiments.py \
       --max-trajectories 50 \
       --compression-ratios 2.0 5.0 10.0 20.0 \
       --algorithms original dp squish vw sw rw proposed
   ```

5. **Generate Plots**:
   ```bash
   python src/experiments/generate_plots.py
   ```

### 11.6.2 Expected Outputs

After running experiments, you should have:

- `results/experiment_results.csv`: Detailed results
- `results/summary_table.csv`: Aggregated statistics
- `results/figures/trajectory_comparison.png`: Trajectory visualizations
- `results/figures/compression_error_curves.png`: Error curves
- `results/figures/runtime_scalability.png`: Performance plots
- `results/figures/metric_comparison_*.png`: Metric comparisons

## 11.7 Version Control

### 11.7.1 Git Setup

```bash
git init
git add .
git commit -m "Initial commit: Trajectory simplification project"
```

### 11.7.2 .gitignore

Create `.gitignore`:

```
# Data files (too large for git)
data/geolife/
data/processed/*.pkl
data/processed/*.csv

# Results (regenerated)
results/figures/*
results/tables/*

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 11.8 Documentation

### 11.8.1 Code Documentation

- All functions should have docstrings
- Complex algorithms should have inline comments
- Mathematical formulas should be explained

### 11.8.2 README

The README.md should include:
- Project overview
- Setup instructions
- Usage examples
- Dataset information
- Citation information

## 11.9 Testing

### 11.9.1 Unit Tests (Optional)

Create `tests/` directory with unit tests for key functions:

```python
# tests/test_algorithms.py
import unittest
from src.algorithms.baseline_algorithms import douglas_peucker

class TestAlgorithms(unittest.TestCase):
    def test_dp_basic(self):
        # Test DP on simple trajectory
        trajectory = ...
        result = douglas_peucker(trajectory, epsilon=10.0)
        self.assertLessEqual(len(result), len(trajectory))
```

### 11.9.2 Validation

- Test on small examples first
- Verify results make sense
- Compare with known baselines
- Check edge cases (very short trajectories, etc.)

## 11.10 Sharing and Publication

### 11.10.1 Code Repository

- Use GitHub/GitLab for code sharing
- Include clear README
- Add license file
- Tag releases

### 11.10.2 Data Sharing

- Provide dataset download instructions
- Include preprocessing scripts
- Document data format

### 11.10.3 Paper/Report

- Include reproducibility section
- Provide code/data links
- Document all parameters
- Include example commands

## 11.11 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and paths are correct
2. **Memory Issues**: Reduce number of trajectories or use smaller subset
3. **Slow Execution**: Use smaller compression ratios or fewer trajectories for testing
4. **Missing Data**: Check dataset path and preprocessing

### Getting Help

- Check error messages carefully
- Review code documentation
- Test on small examples first
- Verify data format

