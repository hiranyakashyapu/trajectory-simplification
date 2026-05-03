# Trajectory Simplification under Irregular Sampling and Noise
## MSc (15 Credit) Research Project

### Project Overview
This project implements and evaluates trajectory simplification algorithms, with a focus on handling irregular sampling and noise while preserving important trajectory features (turns, stops, speed changes).

### Project Structure
```
CSIT-8-PROJECT/
├── data/
│   ├── geolife/          # Raw GeoLife GPS dataset
│   └── processed/        # Preprocessed trajectories
├── src/
│   ├── algorithms/       # Simplification algorithms
│   ├── metrics/         # Evaluation metrics
│   ├── utils/           # Utility functions
│   └── experiments/     # Experiment runners
├── notebooks/           # Jupyter notebooks for analysis
├── results/
│   ├── figures/         # Generated plots
│   └── tables/          # Result tables
├── reports/             # Thesis/report sections
├── config/              # Configuration files
└── requirements.txt     # Python dependencies
```

### Setup Instructions

1. **Create Virtual Environment (Recommended)**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Linux/Mac
   # OR
   venv\Scripts\activate     # On Windows
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
   Alternatively, use the setup script:
   ```bash
   ./venv_setup.sh
   source venv/bin/activate
   ```

2. **Download GeoLife Dataset**
   - Visit: https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/
   - Download and extract to `data/geolife/`
   - The dataset should contain folders like `Data/000/Trajectory/` with `.plt` files

3. **Run Preprocessing**
   ```bash
   python src/utils/preprocess_geolife.py
   ```

4. **Run Experiments**
   ```bash
   python src/experiments/run_experiments.py
   ```

5. **Generate Visualizations**
   ```bash
   python src/experiments/generate_plots.py
   ```

6. **Generate OSM Comparison Map (Original + Multiple Algorithms)**
   ```bash
   ./venv/bin/python src/experiments/visualize_osm.py \
     --comparison \
     --trajectories-file data/processed/trajectories.pkl \
     --output-file results/figures/trajectories_osm_comparison.html \
     --max-trajectories 5 \
     --compression-ratio 5.0 \
     --algorithms original,dp,squish,vw,sw,rw,proposed
   ```

### Project Phases
- **PHASE 1**: Dataset loading and preprocessing
- **PHASE 2**: Baseline algorithms implementation
- **PHASE 3**: Proposed method design and implementation
- **PHASE 4**: Evaluation metrics
- **PHASE 5**: Experiment pipeline
- **PHASE 6**: Visualization
- **PHASE 7**: Scalability study
- **PHASE 8**: Report writing
- **PHASE 9**: Result interpretation
- **PHASE 10**: Viva preparation
- **PHASE 11**: Reproducibility setup

### Citation
If using this code, please cite the GeoLife dataset:
```
Zheng, Y., Li, Q., Chen, Y., Xie, X., & Ma, W. Y. (2008). Understanding mobility based on GPS data. 
In Proceedings of the 10th international conference on Ubiquitous computing (pp. 312-321).
```

