# Intrinsic Dimension Analysis
## of High-Dimensional Data

> **Final Project** - High-Dimensional Probability and Data Analysis  
> Department of Computer Science · 2026

---

```
  ambient space ──┐
                  ├──► intrinsic manifold ──► dimension estimate
  geometry ───────┘
```

---

## Abstract

Many modern datasets inhabit very high-dimensional ambient spaces, yet their meaningful structure resides on a substantially **lower-dimensional manifold**. Estimating this latent or intrinsic dimension is a foundational problem in probability, statistics, and data analysis - with implications for representation, compression, visualization, and learning.

This project presents an empirical investigation of intrinsic dimensionality estimation using **three complementary approaches**: a linear method based on Principal Component Analysis (PCA), the Grassberger-Procaccia correlation dimension, and the Levina-Bickel k-nearest-neighbours maximum-likelihood estimator.

The purpose is not merely to produce numerical estimates, but to examine where estimators **agree**, where they **diverge**, and what these differences reveal about the geometry and effective complexity of the data.

---

## Research Objective

The central objective is to study how different intrinsic dimension estimators behave across datasets with distinct geometric and statistical properties.

| Goal | Description |
|------|-------------|
| Compare approaches | Linear vs. non-linear estimation strategies |
| Validate methods | Synthetic datasets with known ground-truth dimension |
| Analyse real data | Behaviour on high-dimensional MNIST |
| Examine the gap | Ambient dimension vs. effective data complexity |
| Identify trade-offs | Practical strengths and limitations of each method |
| Interpret discrepancies | What disagreement reveals about underlying structure |

The broader motivation is to understand how dimensionality should be interpreted in realistic settings - where ambient representation may be misleadingly large.

---

## Methods

### 01 · PCA-Based Estimation

**File:** `pca_dimension.py`

Estimates intrinsic dimension as the number of principal components required to explain a target proportion of total variance. Thresholds examined: **90%, 95%, and 99%** explained variance.

PCA provides a **linear approximation** of dimensionality. It is computationally convenient and interpretable, but may overestimate dimension for data lying on a curved or non-linear manifold.

---

### 02 · Correlation Dimension

**File:** `correlation_dimension.py`

Based on the **Grassberger-Procaccia** framework. Studies how the number of point pairs within radius ε scales as ε varies, and estimates intrinsic dimension from the slope of the resulting log-log relationship:

```
d = d(log C(ε)) / d(log ε)
```

Unlike PCA, this method is sensitive to non-linear geometric structure - particularly useful when low-dimensional organization cannot be captured by a single linear subspace.

---

### 03 · kNN Maximum-Likelihood Estimator

**File:** `knn_dimension.py`

Follows the **Levina-Bickel** maximum-likelihood approach using nearest-neighbour distances. Estimates intrinsic dimension locally by examining the relative spacing of nearby points.

Non-linear and effective for manifold-like data, but behaviour depends on neighbourhood size, sample quality, and numerical stability. Careful handling of edge cases is therefore essential.

---

## Datasets

### Real-World

**MNIST** - loaded via `load_data.py`

Although each image is represented in a high-dimensional ambient space, MNIST is widely understood to possess substantial lower-dimensional structure due to the constrained nature of handwritten digit geometry. Data may be subsampled for computational tractability in pairwise or neighbourhood-based experiments.

---

### Synthetic - generated via `synthetic_data.py`

| Dataset | True Dimension | Purpose |
|---------|---------------|---------|
| **Gaussian Noise** | ~ ambient | Contrast case - no underlying manifold |
| **2D Plane in 10D** | 2 | Clean linear validation for PCA |
| **Swiss Roll** | 2 | Non-linear benchmark - curved geometry |

The Swiss Roll is the most informative benchmark: its true dimension is **2**, yet its curved geometry makes it a genuine challenge for linear methods, revealing precisely where PCA overestimates.

---

## Repository Structure

```text
intrinsic-dimension-analysis/
│
├── data/
│   └── synthetic/
│       ├── gaussian_noise/              ← stored Gaussian noise dataset
│       ├── plane_2d_in_10d/             ← stored 2D plane embedded in 10D dataset
│       └── swiss_roll/                  ← stored Swiss roll dataset
│
├── intrinsic_dimension_analysis/        ← generated figures used in the report
│
├── src/
│   ├── correlation_dimension.py         ← correlation-dimension estimator
│   ├── knn_dimension.py                 ← Levina-Bickel kNN estimator
│   ├── load_data.py                     ← dataset loading utilities
│   ├── main.py                          ← main script for the complete analysis pipeline
│   ├── pca_dimension.py                 ← PCA-based dimensionality estimator
│   ├── preprocessing.py                 ← preprocessing and sampling utilities
│   ├── synthetic_data.py                ← synthetic benchmark generation
│   └── visualizations.py                ← visualization and figure-generation utilities
│
├── .gitignore                           ← Git ignore rules
├── AI_USAGE.md                          ← AI-assisted development documentation
├── Project_Report.pdf                   ← final academic report
├── README.md                            ← repository guide and execution instructions
└── requirements.txt                     ← required Python packages
```
---

## Dependencies

```bash
pip install -r requirements.txt
```

**Core libraries:**

| Library | Role |
|---------|------|
| `numpy` | Numerical computation |
| `scipy` | Pairwise distances, statistics |
| `scikit-learn` | PCA, nearest neighbours |
| `pandas` | Data handling |
| `matplotlib` | Visualizations |
| `joblib` | Parallel computation |

---

## Execution

### 1 - Clone the repository

```bash
git clone https://github.com/mayarom/intrinsic-dimension-analysis.git
cd intrinsic-dimension-analysis
```

### 2 - Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3 - Install dependencies

```bash
pip install -r requirements.txt
```

### 4 - Run the full analysis pipeline

```bash
python src/main.py
```

Running the pipeline will:

- load the MNIST dataset
- generate all synthetic benchmark datasets
- apply all three intrinsic dimension estimators
- print numerical results to the console
- produce and save visual outputs

### 5 - Visual outputs

```
./visualizations/
```

---

## Output

The project produces both **numerical** and **visual** outputs:

- Explained-variance curves for PCA
- Log-log plots for correlation dimension analysis
- Sensitivity analyses for the kNN estimator across neighbourhood sizes
- Comparative summaries across all datasets
- Printed dimension estimates per method and dataset

These outputs form the empirical basis for the discussion in the report.

---

## Report

```
Project_Report.pdf
```

The full written report covers:

- Theoretical background
- Motivation for dataset selection
- Mathematical and algorithmic description of each estimator
- Experimental design
- Presentation of results
- Discussion of discrepancies between estimators
- Methodological limitations
- Final conclusions and insights

---

## Reproducibility

This repository was prepared with reproducibility as an explicit goal:

- All source code is included
- Synthetic datasets are generated programmatically with fixed procedures
- The real-world dataset is loaded automatically through the pipeline
- The full analysis can be reproduced by running a single command: `python main.py`
- Each estimator is modularized and can be inspected independently

---

## AI Usage

This project was developed with substantial use of AI tools, as explicitly required by the assignment guidelines.

Full documentation is provided in `AI_USAGE.md`, covering:

- which AI tools were used
- how they were used during development
- representative prompts
- outputs that required manual correction
- independent validation procedures

---

## Author

**Maya Rom** · 2026
