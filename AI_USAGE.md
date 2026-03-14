# 🤖 AI Usage Disclosure & Transparency Report

This document outlines the deliberate and strategic integration of Large Language Models (LLMs) in the design, implementation, and documentation of the **Intrinsic Dimension Analysis** project. 

---

## 🛠️ Core AI Stack & Methodology

While **ChatGPT (OpenAI)** served as the primary conversational agent for this project, the following tools are recommended as high-performance alternatives for scientific computing and high-dimensional data analysis:

### **Recommended Complementary AI Tools**
* **Claude 3.5 Sonnet (Anthropic):** Often superior for complex mathematical reasoning and generating concise, dry Python code for scientific research.
* **Perplexity AI:** An "Academic Discovery" engine, ideal for sourcing formal definitions of manifold learning and existing literature.
* **GitHub Copilot / Cursor:** IDE-integrated AI that excels at refactoring large codebases and ensuring type-hint consistency across multiple files.
* **DeepSeek-V3:** Highly efficient for generating optimized numerical algorithms and high-performance NumPy/SciPy operations.

---

## 📋 Domains of AI Integration

The use of AI was integrated as a productivity and support tool across the following project phases:

### 1. Project Planning & Dataset Selection
AI assisted in refining the project scope and selecting representative datasets to test the limits of linear vs. non-linear estimators:
* **MNIST:** Real-world high-dimensional manifold.
* **Gaussian Noise:** Unstructured baseline for the "Curse of Dimensionality."
* **Swiss Roll:** A canonical non-linear manifold test case.
* **2D Plane in 10D:** Validation baseline for linear recovery.

### 2. Code Engineering & Implementation
AI was used to accelerate the development of the Python suite, specifically for:
* **Mathematical Formulations:** Skeletal implementations of the **Levina–Bickel (kNN MLE)** and **Grassberger–Procaccia (Correlation Dimension)** algorithms.
* **Refactoring:** Improving code readability, adding type hints, and ensuring consistent docstring documentation across `src/`.
* **Automation:** Developing the `generate_report_docx.py` script for automated result aggregation.

### 3. Visualization & Interpretation
AI was heavily utilized to design the academic-grade plotting suite in `visualizations.py`, focusing on:
* Multi-panel figure layouts for method comparison.
* Refining plot clarity, labels, and annotations for high-dimensional projections.
* Drafting initial interpretations of the gap between PCA variance and geometric intrinsic dimension.

---

## ⚖️ Verification & Human Oversight

**AI-assisted content was never treated as an authoritative source.** To ensure scientific integrity, the following verification protocols were applied:

| Layer | Verification Method |
| :--- | :--- |
| **Execution-Based** | All scripts were tested in a clean virtual environment to ensure 100% reproducibility. |
| **Sanity Checks** | Results were validated against known benchmarks (e.g., verifying that the Swiss Roll returns $d \approx 2$ regardless of embedding). |
| **Mathematical Review** | AI-generated formulas were manually checked against course materials and formal papers (Levina & Bickel, 2004). |
| **Manual Refinement** | Every paragraph in the final report was edited to ensure technical accuracy and academic tone. |

---

## 📁 Files with Significant AI Contribution

The following files were developed through an iterative collaboration with LLMs:
* `src/knn_dimension.py` & `src/correlation_dimension.py` (Algorithm structure)
* `src/visualizations.py` (Plotting logic and aesthetics)

---

## ⚠️ Limitations Encountered
AI tools occasionally provided suboptimal vectorization for very large matrices or broad generalizations regarding the "Manifold Hypothesis." In these instances, manual adjustments were made to ensure the logic remained grounded in the specific numerical results of the experiments.

---

## Final Statement
This project reflects a **human-led** scientific investigation. AI tools were utilized to enhance productivity and linguistic clarity, while the intellectual ownership, experimental design, and final conclusions remain the sole responsibility of the author.

**Author:** Maya Rom  
**Course:** High-Dimensional Probability and Data Analysis for Computer Science  
**Last Updated:** 2025
