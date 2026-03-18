# Intrinsic Dimension Analysis of High-Dimensional Data

> *A formal technical investigation into the geometric and statistical properties of high-dimensional datasets,*
> *developed for the course in High-Dimensional Probability and Data Analysis for Computer Science.*

---

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.23%2B-013243?style=flat-square&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.1%2B-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-11557C?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-2E8B57?style=flat-square)
![AI Disclosure](https://img.shields.io/badge/AI%20Usage-Documented-8B0000?style=flat-square)

**Author** · Maya Rom &emsp;|&emsp; **Language** · Python 3.x &emsp;|&emsp; **AI Disclosure** · Documented in `AI_USAGE.md`

---

## Abstract

This repository presents a rigorous empirical study of **intrinsic dimensionality estimation** — the problem of identifying the effective number of degrees of freedom in data whose ambient representation may be orders of magnitude larger. The central thesis is that real-world high-dimensional datasets frequently lie on or near low-dimensional manifolds, and that the choice of estimation method fundamentally affects the accuracy and interpretability of the recovered dimension. Three methodological frameworks are systematically compared: linear variance decomposition via PCA, geometric scaling via the correlation integral, and statistical neighbourhood analysis via maximum likelihood estimation.

---

## Table of Contents

1. [Research Goal](#research-goal)
2. [Methods and Technical Approach](#methods-and-technical-approach)
3. [Datasets Analysed](#datasets-analysed)
4. [Project Structure](#project-structure)
5. [Numerical Results and Insights](#numerical-results-and-insights)
6. [Reproducibility](#reproducibility)
7. [AI Usage Disclosure](#ai-usage-disclosure)

---

## Research Goal

The primary objective of this study is to evaluate the **performance and reliability** of various intrinsic dimension estimation methods across structured, unstructured, linear, and non-linear datasets.

By systematically comparing:

- PCA-based variance analysis
- Correlation integral scaling (Grassberger–Procaccia)
- k-Nearest Neighbours Maximum Likelihood Estimation (Levina–Bickel)

…the project seeks to characterise the internal complexity of both synthetic benchmarks and the real-world MNIST handwritten digit dataset, providing a comparative foundation for understanding when linear methods suffice and when non-linear approaches are required.

---

## Methods and Technical Approach

Three distinct methodological frameworks are implemented to provide a holistic view of data dimensionality.

---

### Method I — Linear Variance Estimation (PCA)

> **Framework:** Linear subspace decomposition via Principal Component Analysis.

Determines dimensionality by computing the minimum number of principal components required to cumulatively explain a prescribed fraction of total variance. Three variance thresholds are evaluated:

| Threshold | Interpretation |
| :-------: | :------------- |
| **90%** | Conservative lower bound on intrinsic dimension |
| **95%** | Standard criterion in dimensionality analysis |
| **99%** | Near-complete variance capture; sensitive to noise |

**Limitation:** PCA is a linear projection and cannot recover the geometry of curved or folded manifolds. It is expected to overestimate the intrinsic dimension of non-linear structures.

---

### Method II — Geometric Scaling (Correlation Dimension)

> **Framework:** Fractal-based geometric analysis via the Grassberger–Procaccia correlation integral.

Estimates intrinsic dimension by analysing the power-law scaling relationship:

$$C(\varepsilon) \sim \varepsilon^{d}$$

where $C(\varepsilon)$ is the correlation integral at radius $\varepsilon$, and $d$ is the estimated intrinsic dimension recovered from the slope of $\log C(\varepsilon)$ versus $\log \varepsilon$.

**Advantage:** Captures non-linear geometry and is robust to non-Euclidean manifold structure.

---

### Method III — Neighbourhood-Based MLE (kNN)

> **Framework:** Statistical maximum likelihood estimation via the Levina–Bickel estimator.

Derives intrinsic dimension from the local distribution of inter-point distances within a k-nearest neighbourhood. For each point $x_i$, the estimator computes:

$$\hat{d}_k(x_i) = \left[ \frac{1}{k-1} \sum_{j=1}^{k-1} \log \frac{T_k(x_i)}{T_j(x_i)} \right]^{-1}$$

where $T_j(x_i)$ is the distance from $x_i$ to its $j$-th nearest neighbour. The global estimate is the mean over all points.

**Advantage:** Statistically principled and locally adaptive; sensitive to intrinsic manifold geometry.

---

## Datasets Analysed

| Dataset | Type | Ambient Dim. | True Intrinsic Dim. | Analytical Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **MNIST** | Real-world | 784 | Unknown | Analysis of complex, non-linear image manifolds |
| **Gaussian Noise** | Synthetic | 20 | 20 | Baseline for fully unstructured high-dimensional data |
| **2D Plane in 10D** | Synthetic | 10 | 2 | Validation of linear dimensionality recovery |
| **Swiss Roll** | Synthetic | 3 | 2 | Testing non-linear manifold dimension estimation |

> **Note:** The Swiss Roll dataset is a canonical benchmark for non-linear dimensionality reduction. Despite being embedded in $\mathbb{R}^3$, its intrinsic structure is a 2-dimensional surface, making it an ideal test case for contrasting PCA against manifold-aware methods.

---

## Project Structure

```
intrinsic-dimension-analysis/
│
├── README.md                              # This document
├── AI_USAGE.md                            # Full documentation of LLM assistance
├── requirements.txt                       # Pinned environment dependencies
│
├── src/
│   ├── main.py                            # Central execution and orchestration script
│   ├── load_data.py                       # Dataset loading and ingestion utilities
│   ├── preprocessing.py                   # Standardisation, normalisation, feature filtering
│   ├── pca_dimension.py                   # Linear variance estimation (Method I)
│   ├── correlation_dimension.py           # Geometric scaling logic (Method II)
│   ├── knn_dimension.py                   # Levina–Bickel MLE implementation (Method III)
│   ├── synthetic_data.py                  # Synthetic dataset generation utilities
│   └── visualizations.py                  # Academic-grade plotting suite
│
├── data/
│   ├── raw/
│   │   └── mnist/                         # Raw MNIST source files
│   ├── processed/                         # Preprocessed and normalised data
│   └── synthetic/
│       ├── gaussian_noise/                # 20-dimensional unstructured baseline
│       ├── plane_2d_in_10d/               # Linear 2D manifold in 10D ambient space
│       └── swiss_roll/                    # Non-linear 2D manifold in 3D ambient space
│
└── intrinsic_dimension_analysis/          # Generated output figures
```

---

## Numerical Results and Insights

### Summary of Key Findings

---

#### Finding I — The Manifold Hypothesis is Supported

Analysis of MNIST demonstrates that while the ambient dimension is **784**, the intrinsic dimension recovered by all three estimators is significantly lower (estimated range: **12–40**, depending on method and threshold). This provides strong empirical support for the manifold hypothesis: that natural high-dimensional data distributions are concentrated near low-dimensional substructures.

---

#### Finding II — PCA Overestimates Non-Linear Intrinsic Dimension

For the Swiss Roll dataset — whose true intrinsic dimension is **2** — PCA consistently returns estimates of **3** or higher, reflecting its fundamental inability to account for manifold curvature. In contrast, both the correlation dimension and the kNN estimator correctly recover dimension ≈ 2, confirming that non-linear methods are essential for curved manifold structures.

---

#### Finding III — kNN Estimates are Stable but Sensitive to Local Density

The Levina–Bickel estimator demonstrates stability across a range of neighbourhood sizes $k \in [5, 20]$, with variance increasing at the extremes. In regions of non-uniform local density — prevalent in high-dimensional spaces due to the *curse of dimensionality* — local fluctuations can introduce systematic bias, particularly for datasets with complex topology such as MNIST.

---

### Comparative Results Overview

| Dataset | PCA (95%) | Correlation Dim. | kNN MLE | True Dim. |
| :--- | :---: | :---: | :---: | :---: |
| Gaussian Noise | ~20 | ~20 | ~20 | 20 |
| 2D Plane in 10D | 2 | ~2 | ~2 | 2 |
| Swiss Roll | 3 | ~2 | ~2 | 2 |
| MNIST | ~154 | ~14 | ~18 | Unknown |

> *MNIST results are approximate and depend on preprocessing and sample size.*

---

## Reproducibility

### Environment Requirements

| Dependency | Version |
| :--- | :--- |
| Python | ≥ 3.9 |
| NumPy | ≥ 1.23 |
| scikit-learn | ≥ 1.1 |
| Matplotlib | ≥ 3.5 |
| SciPy | ≥ 1.9 |

---

### Setup

**Step 1.** Clone the repository:

```bash
git clone https://github.com/mayarom/intrinsic-dimension-analysis.git
cd intrinsic-dimension-analysis
```

**Step 2.** Initialise a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Step 3.** Execute the full analysis pipeline:

```bash
python3 src/main.py
```

**Step 4.** Generate the visualisation suite:

```bash
python3 src/visualizations.py
```

Output figures and numerical summaries are written to the `outputs/` directory.

---

## AI Usage Disclosure

In compliance with the assignment requirements, this project integrated Large Language Models (LLMs) during the development lifecycle. AI assistance was utilised for the following purposes:

| Domain | Scope of Use |
| :--- | :--- |
| **Mathematical derivation** | Refinement and verification of estimator formulations |
| **Numerical code** | Refactoring of high-performance array operations |
| **Report structure** | Structural organisation and clarity of written sections |

> A detailed log of all prompts submitted and AI-generated contributions is available in [`AI_USAGE.md`](./AI_USAGE.md), in full compliance with the course transparency policy.

---

## Author

**Maya Rom**
*Course Project — High-Dimensional Probability and Data Analysis for Computer Science*

---

*Last updated: 2025*
