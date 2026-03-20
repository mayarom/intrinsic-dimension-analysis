# AI Usage Documentation

> Transparent and complete documentation of AI-assisted development  
> Prepared in accordance with course requirements

---

## Overview

This project was developed with **substantial assistance from AI tools**, in accordance with the explicit course requirement to make meaningful use of LLM-based systems during implementation.

AI tools functioned as development assistants throughout the project - not as unquestioned sources of final truth. They contributed to initial implementations, algorithmic scaffolding, code organization, debugging, and documentation refinement. All generated outputs were reviewed critically, tested empirically, and revised where necessary.

**The final responsibility for correctness, validation, interpretation, and submission remained entirely with the author.**

---

## AI Tools Used

| Tool | Primary Role |
|------|-------------|
| **ChatGPT** | Algorithmic design, implementation scaffolding, debugging |
| **Cursor AI** | In-editor code generation, iterative code refinement |

These tools were used at different stages of development and often in an iterative manner - especially when refining implementations or resolving numerical issues.

---

## Scope of AI Assistance

AI assistance contributed to several major aspects of the project:

- Generating initial implementations of all three intrinsic dimension estimators
- Structuring the project into modular, independent Python files
- Suggesting improvements to computational efficiency
- Assisting in debugging numerical and indexing issues
- Refining the analysis workflow and code readability
- Improving the clarity and organization of the documentation

In particular, AI tools were used to generate a substantial portion of the initial codebase - consistent with the lecturer's explicit requirement that students make real and documented use of AI tools.

---

## Representative Prompt Examples

### Prompt 01 - Correlation Dimension

```
Implement the Grassberger-Procaccia correlation dimension estimator using
pairwise distances. Use scipy.pdist for efficiency, compute the slope of
log(C(epsilon)) versus log(epsilon), and make sure to handle numerical
stability issues such as zero distances.
```

**Why this prompt was used:**  
I wanted an implementation that was both mathematically aligned with the standard formulation and computationally more efficient than a naive nested-loop approach.

---

### Prompt 02 - kNN Estimator

```
Implement the Levina-Bickel intrinsic dimension estimator using k-nearest
neighbours. Use sklearn NearestNeighbors and ensure numerical stability
when computing log ratios from neighbour distances.
```

**Why this prompt was used:**  
This estimator is more delicate than PCA because it depends on local neighbour structure and logarithmic expressions. The prompt therefore explicitly requested both the standard method and numerical safeguards.

---

### Prompt 03 - PCA-Based Estimator

```
Write a function that estimates intrinsic dimension using PCA by finding
the number of components required to explain a target proportion of
variance, such as 95 percent.
```

**Why this prompt was used:**  
I wanted a clean baseline estimator that could serve both as a benchmark and as a linear contrast to the non-linear methods.

---

### Prompt 04 - Repository and Pipeline Structure

```
Help me organize the project into separate Python modules so that each
intrinsic dimension method is implemented independently and the main
script can run all methods on multiple datasets in a consistent pipeline.
```

**Why this prompt was used:**  
Beyond individual functions, I also used AI to think about project structure and modularity - keeping the repository readable and suitable for submission.

---

## Iterative Refinement of AI-Generated Code

AI-generated code was never accepted automatically. In practice, it required **multiple rounds of manual inspection and correction**.

Among the main issues encountered were:

| Issue | Description |
|-------|-------------|
| Numerical instability | Zero or near-zero values in distance computations |
| Division-by-zero | Risks in nearest-neighbour logarithmic expressions |
| Shape mismatches | Array dimension errors in matrix operations |
| Indexing mistakes | Incorrect neighbour index handling |
| Computational inefficiency | Naive pairwise distance implementations |
| Missing edge cases | Insufficient handling of degenerate experimental conditions |

These issues became visible only after testing implementations on synthetic datasets and comparing results with theoretical expectations.

---

## Concrete Example of Manual Correction

A clear example of necessary manual intervention appeared in the AI-generated implementation of the kNN maximum-likelihood estimator.

### Problem

The nearest-neighbour distance matrix occasionally contained **zero values** - for example, when points were duplicated or numerically indistinguishable. Since the estimator applies logarithmic operations to ratios involving these distances, this created a risk of unstable computations and division-by-zero errors.

The initial AI-generated version did not adequately guard against this.

### Fix Applied

```python
distances, indices = knn.kneighbors(X)
distances = np.maximum(distances, 1e-10)
```

### Why This Fix Was Necessary

This modification ensured that:

- no neighbour distance used in the estimator would be exactly zero
- logarithmic expressions remained numerically stable across all inputs
- the implementation behaved robustly across different datasets and subsampling conditions

This example captures the general pattern: AI as a **strong starting point**, not a substitute for technical judgment and manual verification.

---

## Additional Manual Improvements

Beyond the correction above, several further manual improvements were applied to AI-generated outputs:

- Replacing naive pairwise-distance loops with `scipy.pdist` for efficiency
- Improving modular separation between data loading, estimation, and the main pipeline
- Cleaning code structure and naming for readability
- Adjusting implementation details to better support experimental reproducibility
- Refining plotting and output presentation to improve clarity of comparisons
- Tuning parts of the workflow to remain computationally practical on the selected datasets

---

## Validation and Independent Verification

A central part of the project was verifying that AI-assisted implementations produced **meaningful and theoretically plausible results**.

Validation was performed in several ways:

- Testing on synthetic datasets with known intrinsic dimension
- Comparing outputs of different estimators on the same dataset
- Checking whether observed behaviour matched theoretical expectations
- Inspecting both numerical outputs and visualizations

---

### Validation Example - Swiss Roll

The Swiss Roll served as the most important validation case because its true intrinsic dimension is known to be **2**.

| Method | Expected | Observed Behaviour |
|--------|----------|--------------------|
| PCA | overestimate | Overestimated - manifold is non-linear |
| Correlation Dimension | ≈ 2 | Returned values close to 2 |
| kNN Estimator | ≈ 2 | Returned values approximately consistent with 2 |

This provided concrete evidence that the non-linear estimators were implemented correctly enough to recover the underlying geometry in a standard benchmark setting.

---

## AI Assistance in Documentation

AI tools were also used in the preparation of written documentation.

This included assistance with:

- structuring the README
- refining the wording of technical explanations
- improving clarity and coherence in methodological descriptions
- drafting and polishing the AI usage documentation itself

Even in these cases, the final text was manually reviewed, edited, and adapted to reflect the actual work performed.

---

## Author Responsibility

Although AI tools played a substantial role in accelerating development, they did not replace independent work.

Responsibilities retained and exercised personally:

- Reviewing the generated code
- Correcting errors and weaknesses
- Testing the estimators on benchmark datasets
- Interpreting the numerical and visual results
- Writing and refining the final conclusions
- Ensuring the submitted work accurately reflects the implemented project

**The final responsibility for the technical quality and academic integrity of this submission remains entirely mine.**

---

## Compliance Statement

This document is provided to comply fully and transparently with course requirements regarding AI usage.

| Requirement | Status |
|-------------|--------|
| AI tools used substantially | Satisfied |
| Use documented explicitly | Satisfied |
| Representative prompts included | Satisfied |
| Concrete manual corrections described | Satisfied |
| Independent validation documented | Satisfied |
| Author responsibility clearly stated | Satisfied |

---

## Summary

AI tools played a **significant and legitimate role** in this project. They accelerated implementation, supported code organization, and assisted with debugging and documentation. At the same time, generated outputs were not treated as automatically correct - they were tested, revised, and in several cases manually repaired.

The final project is therefore best described as:

```
AI-assisted · independently validated · fully authored
```

---

**Maya Rom** · 2026
