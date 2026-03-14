# AI_USAGE.md

## AI Usage Statement

This project made extensive and deliberate use of large language model (LLM) assistance during the design, implementation, refinement, and documentation process. The use of AI was integrated as a productivity and support tool, while all final technical decisions, interpretation of results, and validation of correctness were performed manually and critically.

The purpose of using AI in this project was not to replace understanding or independent work, but rather to accelerate development, improve code structure, support technical writing, and help refine the final presentation of the project.

---

## Tools Used

The main AI tool used in this project was:

- **ChatGPT**

The tool was used iteratively throughout the project in a collaborative manner. In practice, AI functioned as a coding assistant, writing assistant, explanation assistant, and review assistant.

---

## How AI Was Used in This Project

AI was used in the following major areas:

### 1. Project Topic Refinement and Planning

AI was used to help shape the project into a form that would be both academically strong and technically feasible.

This included:
- refining the project topic,
- clarifying the difference between ambient dimension and intrinsic dimension,
- selecting an appropriate analytical direction,
- structuring the project as a comparison between multiple dimensionality estimation methods,
- organizing the work into a clear sequence of implementation steps.

AI assistance was particularly useful in converting a broad course requirement into a coherent and focused project plan.

---

### 2. Dataset Selection and Experimental Design

AI was used to help evaluate which datasets would be most suitable for the project goals.

This included support in selecting:
- **MNIST** as the real-world high-dimensional dataset,
- **Gaussian noise** as a high-dimensional unstructured baseline,
- **a 2D plane embedded in 10D** as a validation dataset with known intrinsic dimension,
- **Swiss roll** as a nonlinear manifold example.

AI was also used to help formulate the reasoning behind these choices in academically appropriate language for the report.

---

### 3. Code Generation and Code Structuring

AI was used extensively to assist in writing and refining Python code across the project.

This included support for:
- generating synthetic datasets,
- loading data from OpenML and local files,
- building the preprocessing pipeline,
- implementing PCA-based dimensionality estimation,
- implementing correlation-dimension estimation,
- implementing a kNN-based intrinsic-dimension estimator,
- building the main analysis pipeline,
- generating figures and visualizations,
- generating a DOCX report with embedded figures.

AI assistance was especially useful for:
- creating well-structured functions,
- improving code readability,
- adding docstrings,
- improving naming consistency,
- adding type hints,
- refactoring repetitive logic,
- improving code organization across multiple files.

However, the code was not accepted blindly. Every major function was inspected, revised where necessary, and integrated manually into the project structure.

---

### 4. Mathematical Explanation and Method Formulation

AI was used to help explain the mathematical ideas behind the implemented methods, including:
- PCA-based dimensionality estimation,
- correlation dimension,
- the Levina-Bickel kNN maximum-likelihood estimator.

This was useful both for implementation and for writing the report in a technically correct and readable way.

In particular, AI was used to:
- rephrase technical definitions,
- turn formulas into report-ready explanations,
- help connect the methods to the project’s broader analytical goal.

All mathematical explanations included in the final report were reviewed manually for consistency with the implemented code and with the numerical results obtained.

---

### 5. Visualization Design and Refinement

AI was used heavily in the creation and refinement of the project’s visual outputs.

This included help with:
- deciding which figures to generate,
- structuring the visualizations by dataset and by method,
- improving plot clarity,
- fixing overlap and layout issues,
- refining titles, labels, legends, and annotations,
- reducing unnecessary visual clutter,
- improving consistency across figures,
- designing comparison plots between multiple methods.

The final visualization pipeline was produced through multiple iterations. AI-generated suggestions were not accepted automatically; the figures were repeatedly reviewed visually, and several rounds of manual refinement were made based on actual output quality.

---

### 6. Interpretation of Results

AI was used to help articulate the meaning of the numerical results and visual outputs.

This included help in describing:
- why PCA behaves differently from nonlinear geometric methods,
- why the Swiss roll is an important counterexample to purely linear reasoning,
- why Gaussian noise behaves as a high-dimensional dataset,
- why MNIST exhibits a gap between variance-based and geometry-based dimensionality estimates,
- how the kNN results strengthen the interpretation of the project.

The final interpretations in the report were based on the actual outputs produced by the code and were checked manually against the results.

---

### 7. Academic Writing and Report Drafting

AI was used extensively in drafting and refining the written report.

This included:
- improving the academic tone,
- restructuring paragraphs,
- refining section titles,
- writing clearer explanations,
- generating figure captions,
- drafting result sections,
- drafting the kNN section,
- improving transitions between parts of the report,
- producing polished English prose.

The final wording was reviewed manually and adjusted to ensure that it matched the actual project results and the intended level of academic clarity.

---

### 8. Documentation and Submission Materials

AI was used to help prepare final project documentation, including:
- `README.md`,
- `AI_USAGE.md`,
- figure captions,
- report-ready text,
- document generation scripts,
- organization of the final submission materials.

---

## Files That Were Significantly Assisted by AI

AI contributed meaningfully to the development or refinement of the following files:

- `src/synthetic_data.py`
- `src/load_data.py`
- `src/preprocessing.py`
- `src/pca_dimension.py`
- `src/correlation_dimension.py`
- `src/knn_dimension.py`
- `src/main.py`
- `src/visualizations.py`
- `src/generate_report_docx.py`
- `README.md`
- `AI_USAGE.md`
- sections of the final report

This does **not** mean these files were copied directly from AI output without review. Rather, AI was used as an iterative assistant while the code and text were manually inspected, revised, and integrated.

---

## What Was Changed Manually

Substantial manual work was performed throughout the project, including:

- deciding the final project structure,
- choosing the datasets,
- determining the final set of methods,
- reviewing generated code before adoption,
- fixing environment and dependency issues,
- adjusting preprocessing behavior,
- checking whether the outputs matched expectations,
- modifying plot layout and content based on visual inspection,
- selecting which results should appear in the report body versus appendices,
- refining the written interpretation to match actual experimental output,
- deciding which comparisons were scientifically meaningful,
- reviewing the final submission materials as a complete package.

In particular, multiple rounds of manual review were required for:
- figure layout quality,
- wording of report sections,
- method comparison logic,
- clarity of table structure,
- output formatting.

---

## How Correctness Was Verified

AI-generated or AI-assisted content was not treated as automatically correct. Instead, correctness was verified in several ways:

### 1. Execution-Based Validation
All major code files were executed and tested directly. If code failed to run, it was corrected and re-tested.

### 2. Sanity Checks Against Expected Behavior
The results were compared against known expectations:
- the 2D plane dataset should produce estimates close to 2,
- the Swiss roll should be intrinsically close to 2 despite nonlinear embedding,
- Gaussian noise should appear high-dimensional,
- MNIST should show substantial structure but not trivial low dimensionality.

These sanity checks were essential in validating that the implementations behaved reasonably.

### 3. Cross-Method Comparison
The project intentionally used multiple methods so that results could be compared:
- PCA,
- correlation dimension,
- kNN-based estimation.

Agreement and disagreement between methods were used as part of the validation process.

### 4. Visual Inspection
All generated figures were reviewed manually. Several figures were revised multiple times to improve clarity and to ensure that they accurately reflected the numerical results.

### 5. Manual Review of Explanations
All AI-assisted written explanations were checked manually against:
- the implemented code,
- the numerical outputs,
- the intended scientific interpretation.

---

## Limitations of AI Use

AI was helpful, but not infallible. In practice, it sometimes produced:
- code that needed refinement,
- formatting choices that were visually suboptimal,
- wording that was correct in spirit but too broad or insufficiently tied to the actual outputs,
- suggestions that required manual adjustment to fit the project structure.

For that reason, AI was used as a support tool rather than as an authoritative source.

---

## Final Statement

AI played a substantial and meaningful role in this project, particularly in code drafting, technical explanation, writing refinement, and visualization design. However, the project remained a supervised and critically evaluated process. All final design choices, interpretation of results, output validation, and submission preparation were reviewed manually.

The final submission reflects not only AI assistance, but also deliberate human judgment in selecting methods, validating outputs, refining the implementation, and interpreting the results in an academically appropriate way.
