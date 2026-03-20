from __future__ import annotations

from typing import Final

import numpy as np

from correlation_dimension import estimate_correlation_dimension
from knn_dimension import estimate_knn_dimension, estimate_knn_dimension_over_k_range
from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from pca_dimension import estimate_pca_dimensionality
from preprocessing import preprocessing_pipeline, sample_dataset

# ---------------------------------------------------------------------
# Project-wide constants
# ---------------------------------------------------------------------

MNIST_SAMPLE_SIZE_FOR_GEOMETRIC_METHODS: Final[int] = 1000
RANDOM_STATE: Final[int] = 42
DEFAULT_KNN_K: Final[int] = 10
DEFAULT_KNN_K_VALUES: Final[tuple[int, ...]] = (5, 8, 10, 12, 15, 20)

CORRELATION_N_RADII: Final[int] = 30
CORRELATION_MIN_PERCENTILE: Final[float] = 1.0
CORRELATION_MAX_PERCENTILE: Final[float] = 50.0
CORRELATION_SCALING_REGION_START: Final[int] = 5
CORRELATION_SCALING_REGION_END: Final[int] = 20

PCA_THRESHOLDS: Final[tuple[float, ...]] = (0.90, 0.95, 0.99)


# ---------------------------------------------------------------------
# Utility and validation helpers
# ---------------------------------------------------------------------

def get_processed_array(
    results: dict[str, object],
    key: str = "x_processed",
) -> np.ndarray:
    """
    Extract a processed NumPy array from a preprocessing results dictionary.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by ``preprocessing_pipeline``.
    key : str, default="x_processed"
        Key under which the processed array is stored.

    Returns
    -------
    np.ndarray
        The processed feature matrix.

    Raises
    ------
    TypeError
        If the requested value is not a NumPy array.
    """
    value = results.get(key)

    if not isinstance(value, np.ndarray):
        raise TypeError(f"Expected '{key}' to be a NumPy array.")

    return value


def preprocess_for_analysis(x: np.ndarray) -> np.ndarray:
    """
    Apply the standard preprocessing configuration used throughout the project.

    The preprocessing pipeline removes constant features, optionally filters by
    variance threshold, and applies feature standardization.

    Parameters
    ----------
    x : np.ndarray
        Input feature matrix.

    Returns
    -------
    np.ndarray
        Preprocessed feature matrix.
    """
    preprocessing_results = preprocessing_pipeline(
        x,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False,
    )
    return get_processed_array(preprocessing_results)


def print_separator(char: str = "=", width: int = 100) -> None:
    """
    Print a horizontal separator line.

    Parameters
    ----------
    char : str, default="="
        Character used to construct the separator.
    width : int, default=100
        Total width of the separator line.
    """
    print(char * width)


def print_title(title: str) -> None:
    """
    Print a formatted section title.

    Parameters
    ----------
    title : str
        Section title.
    """
    print_separator("=")
    print(title)
    print_separator("=")


def print_subtitle(subtitle: str) -> None:
    """
    Print a formatted subsection title.

    Parameters
    ----------
    subtitle : str
        Subsection title.
    """
    print(subtitle)
    print_separator("-")


def validate_pca_results(
    results: dict[str, object],
) -> tuple[dict[float, int], np.ndarray, np.ndarray]:
    """
    Validate and extract the main PCA outputs.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by ``estimate_pca_dimensionality``.

    Returns
    -------
    tuple[dict[float, int], np.ndarray, np.ndarray]
        A tuple containing:
        - the number of components required for each variance threshold,
        - the explained variance ratio per component,
        - the cumulative explained variance.

    Raises
    ------
    TypeError
        If any required field has an unexpected type.
    """
    components_per_threshold = results.get("components_per_threshold")
    explained_variance_ratio = results.get("explained_variance_ratio")
    cumulative_explained_variance = results.get("cumulative_explained_variance")

    if not isinstance(components_per_threshold, dict):
        raise TypeError("Expected components_per_threshold to be a dictionary.")
    if not isinstance(explained_variance_ratio, np.ndarray):
        raise TypeError("Expected explained_variance_ratio to be a NumPy array.")
    if not isinstance(cumulative_explained_variance, np.ndarray):
        raise TypeError("Expected cumulative_explained_variance to be a NumPy array.")

    return (
        components_per_threshold,
        explained_variance_ratio,
        cumulative_explained_variance,
    )


def validate_correlation_results(results: dict[str, object]) -> float:
    """
    Validate and extract the estimated correlation dimension.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by ``estimate_correlation_dimension``.

    Returns
    -------
    float
        Estimated correlation dimension.

    Raises
    ------
    TypeError
        If the extracted estimate is not a float.
    """
    estimated_dimension = results.get("estimated_dimension")

    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")

    return estimated_dimension


def validate_knn_main_results(
    results: dict[str, object],
) -> tuple[int, float, float, float, float]:
    """
    Validate and extract the main kNN intrinsic-dimension summary.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by ``estimate_knn_dimension``.

    Returns
    -------
    tuple[int, float, float, float, float]
        A tuple containing:
        - selected k,
        - global estimated dimension,
        - mean local dimension,
        - median local dimension,
        - standard deviation of local dimensions.

    Raises
    ------
    TypeError
        If any extracted field has an unexpected type.
    """
    k = results.get("k")
    estimated_dimension = results.get("estimated_dimension")
    mean_local_dimension = results.get("mean_local_dimension")
    median_local_dimension = results.get("median_local_dimension")
    std_local_dimension = results.get("std_local_dimension")

    if not isinstance(k, int):
        raise TypeError("Expected k to be an integer.")
    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")
    if not isinstance(mean_local_dimension, float):
        raise TypeError("Expected mean_local_dimension to be a float.")
    if not isinstance(median_local_dimension, float):
        raise TypeError("Expected median_local_dimension to be a float.")
    if not isinstance(std_local_dimension, float):
        raise TypeError("Expected std_local_dimension to be a float.")

    return (
        k,
        estimated_dimension,
        mean_local_dimension,
        median_local_dimension,
        std_local_dimension,
    )


def validate_knn_range_results(
    results: dict[str, object],
) -> tuple[np.ndarray, np.ndarray, float, float, float, float]:
    """
    Validate and extract the k-range sensitivity analysis outputs.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by ``estimate_knn_dimension_over_k_range``.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, float, float, float, float]
        A tuple containing:
        - tested k values,
        - dimension estimate for each k,
        - mean estimate across k,
        - standard deviation across k,
        - minimum estimate across k,
        - maximum estimate across k.

    Raises
    ------
    TypeError
        If any extracted field has an unexpected type.
    """
    k_values = results.get("k_values")
    dimension_estimates = results.get("dimension_estimates")
    mean_estimate = results.get("mean_estimate")
    std_estimate = results.get("std_estimate")
    min_estimate = results.get("min_estimate")
    max_estimate = results.get("max_estimate")

    if not isinstance(k_values, np.ndarray):
        raise TypeError("Expected k_values to be a NumPy array.")
    if not isinstance(dimension_estimates, np.ndarray):
        raise TypeError("Expected dimension_estimates to be a NumPy array.")
    if not isinstance(mean_estimate, float):
        raise TypeError("Expected mean_estimate to be a float.")
    if not isinstance(std_estimate, float):
        raise TypeError("Expected std_estimate to be a float.")
    if not isinstance(min_estimate, float):
        raise TypeError("Expected min_estimate to be a float.")
    if not isinstance(max_estimate, float):
        raise TypeError("Expected max_estimate to be a float.")

    return (
        k_values,
        dimension_estimates,
        mean_estimate,
        std_estimate,
        min_estimate,
        max_estimate,
    )


# ---------------------------------------------------------------------
# Core analysis pipeline
# ---------------------------------------------------------------------

def analyze_dataset(
    dataset_name: str,
    x_raw: np.ndarray,
    use_sampling_for_geometric_methods: bool = False,
) -> dict[str, object]:
    """
    Run the complete intrinsic-dimension analysis pipeline for a single dataset.

    The pipeline includes:
    1. preprocessing,
    2. PCA-based dimensionality estimation,
    3. correlation-dimension estimation,
    4. kNN-based intrinsic-dimension estimation,
    5. kNN sensitivity analysis over a range of k values.

    For large datasets such as MNIST, a sampled subset may be used for the
    computationally heavier geometric methods.

    Parameters
    ----------
    dataset_name : str
        Human-readable dataset name.
    x_raw : np.ndarray
        Raw feature matrix.
    use_sampling_for_geometric_methods : bool, default=False
        Whether to sample the dataset before running correlation-dimension and
        kNN-based methods.

    Returns
    -------
    dict[str, object]
        Dictionary containing all outputs needed for reporting and comparison.
    """
    x_processed = preprocess_for_analysis(x_raw)

    if use_sampling_for_geometric_methods:
        x_sampled, _ = sample_dataset(
            x=x_raw,
            y=None,
            n_samples=MNIST_SAMPLE_SIZE_FOR_GEOMETRIC_METHODS,
            random_state=RANDOM_STATE,
        )
        x_geometric_processed = preprocess_for_analysis(x_sampled)
    else:
        x_geometric_processed = x_processed

    pca_results = estimate_pca_dimensionality(
        x_processed,
        thresholds=PCA_THRESHOLDS,
    )

    correlation_results = estimate_correlation_dimension(
        x=x_geometric_processed,
        n_radii=CORRELATION_N_RADII,
        min_percentile=CORRELATION_MIN_PERCENTILE,
        max_percentile=CORRELATION_MAX_PERCENTILE,
        scaling_region_start=CORRELATION_SCALING_REGION_START,
        scaling_region_end=CORRELATION_SCALING_REGION_END,
    )

    knn_main_results = estimate_knn_dimension(
        x=x_geometric_processed,
        k=DEFAULT_KNN_K,
        metric="euclidean",
        aggregate="mean",
        n_jobs=None,
    )

    knn_range_results = estimate_knn_dimension_over_k_range(
        x=x_geometric_processed,
        k_values=list(DEFAULT_KNN_K_VALUES),
        metric="euclidean",
        aggregate="mean",
        n_jobs=None,
    )

    return {
        "dataset_name": dataset_name,
        "x_raw_shape": x_raw.shape,
        "x_processed_shape": x_processed.shape,
        "x_geometric_processed_shape": x_geometric_processed.shape,
        "pca_results": pca_results,
        "correlation_results": correlation_results,
        "knn_main_results": knn_main_results,
        "knn_range_results": knn_range_results,
    }


# ---------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------

def print_dataset_results(result: dict[str, object]) -> None:
    """
    Print the analysis results for a single dataset in a structured format.

    Parameters
    ----------
    result : dict[str, object]
        Dictionary returned by ``analyze_dataset``.

    Raises
    ------
    TypeError
        If any required field has an unexpected type.
    """
    dataset_name = result.get("dataset_name")
    x_raw_shape = result.get("x_raw_shape")
    x_processed_shape = result.get("x_processed_shape")
    x_geometric_processed_shape = result.get("x_geometric_processed_shape")
    pca_results = result.get("pca_results")
    correlation_results = result.get("correlation_results")
    knn_main_results = result.get("knn_main_results")
    knn_range_results = result.get("knn_range_results")

    if not isinstance(dataset_name, str):
        raise TypeError("Expected dataset_name to be a string.")
    if not isinstance(x_raw_shape, tuple):
        raise TypeError("Expected x_raw_shape to be a tuple.")
    if not isinstance(x_processed_shape, tuple):
        raise TypeError("Expected x_processed_shape to be a tuple.")
    if not isinstance(x_geometric_processed_shape, tuple):
        raise TypeError("Expected x_geometric_processed_shape to be a tuple.")
    if not isinstance(pca_results, dict):
        raise TypeError("Expected pca_results to be a dictionary.")
    if not isinstance(correlation_results, dict):
        raise TypeError("Expected correlation_results to be a dictionary.")
    if not isinstance(knn_main_results, dict):
        raise TypeError("Expected knn_main_results to be a dictionary.")
    if not isinstance(knn_range_results, dict):
        raise TypeError("Expected knn_range_results to be a dictionary.")

    pca_thresholds, explained_variance_ratio, cumulative_explained_variance = (
        validate_pca_results(pca_results)
    )
    correlation_dimension = validate_correlation_results(correlation_results)
    knn_k, knn_estimate, knn_mean_local, knn_median_local, knn_std_local = (
        validate_knn_main_results(knn_main_results)
    )
    k_values, dimension_estimates, mean_estimate, std_estimate, min_estimate, max_estimate = (
        validate_knn_range_results(knn_range_results)
    )

    print_separator("=")
    print(f"DATASET: {dataset_name}")
    print_separator("=")
    print(f"Raw shape:                          {x_raw_shape}")
    print(f"Processed shape (PCA):             {x_processed_shape}")
    print(f"Processed shape (geometric/kNN):   {x_geometric_processed_shape}")
    print()

    print_subtitle("PCA-based dimensionality estimation")
    print(f"Components for 90% variance:       {pca_thresholds[0.90]}")
    print(f"Components for 95% variance:       {pca_thresholds[0.95]}")
    print(f"Components for 99% variance:       {pca_thresholds[0.99]}")
    print(f"First explained variance ratio:    {float(explained_variance_ratio[0]):.6f}")
    print(f"Cumulative variance at component 1:{float(cumulative_explained_variance[0]):.6f}")
    print()

    print_subtitle("Correlation dimension estimation")
    print(f"Estimated correlation dimension:   {correlation_dimension:.4f}")
    print()

    print_subtitle("kNN-based intrinsic dimension estimation")
    print("Method:                            kNN Levina-Bickel MLE")
    print(f"Selected k:                        {knn_k}")
    print(f"Headline estimate:                 {knn_estimate:.4f}")
    print(f"Mean local estimate:               {knn_mean_local:.4f}")
    print(f"Median local estimate:             {knn_median_local:.4f}")
    print(f"Std. local estimate:               {knn_std_local:.4f}")
    print()

    print_subtitle("kNN sensitivity analysis across k")
    for k_value, estimate in zip(k_values, dimension_estimates):
        print(f"k = {int(k_value):>2d} -> estimated dimension = {float(estimate):.4f}")
    print()
    print(f"Mean estimate across k:            {mean_estimate:.4f}")
    print(f"Std. across k:                     {std_estimate:.4f}")
    print(f"Min estimate across k:             {min_estimate:.4f}")
    print(f"Max estimate across k:             {max_estimate:.4f}")
    print()

    k_values_list = [int(value) for value in k_values]
    stability_text = "good" if std_estimate < 1.0 else "moderate"

    print_subtitle("Suggested report sentence")
    print(
        f"For {dataset_name}, the kNN-based intrinsic-dimension estimate "
        f"(Levina-Bickel MLE, k={knn_k}) was {knn_estimate:.2f}. "
        f"Across the tested range k={k_values_list}, the estimates remained within "
        f"[{min_estimate:.2f}, {max_estimate:.2f}] with a mean of {mean_estimate:.2f}, "
        f"indicating {stability_text} stability."
    )
    print()


def print_final_summary_table(results: list[dict[str, object]]) -> None:
    """
    Print a final comparison table across all analyzed datasets.

    Parameters
    ----------
    results : list[dict[str, object]]
        List of dictionaries returned by ``analyze_dataset``.
    """
    print_title("FINAL SUMMARY TABLE")
    print(
        f"{'Dataset':<30} "
        f"{'Ambient Dim':>12} "
        f"{'Processed Dim':>14} "
        f"{'PCA 90%':>10} "
        f"{'Corr Dim':>12} "
        f"{'kNN (k=10)':>12} "
        f"{'kNN Mean(k)':>12}"
    )
    print_separator("-")

    for result in results:
        dataset_name = result.get("dataset_name")
        x_raw_shape = result.get("x_raw_shape")
        x_processed_shape = result.get("x_processed_shape")
        pca_results = result.get("pca_results")
        correlation_results = result.get("correlation_results")
        knn_main_results = result.get("knn_main_results")
        knn_range_results = result.get("knn_range_results")

        if not isinstance(dataset_name, str):
            raise TypeError("Expected dataset_name to be a string.")
        if not isinstance(x_raw_shape, tuple):
            raise TypeError("Expected x_raw_shape to be a tuple.")
        if not isinstance(x_processed_shape, tuple):
            raise TypeError("Expected x_processed_shape to be a tuple.")
        if not isinstance(pca_results, dict):
            raise TypeError("Expected pca_results to be a dictionary.")
        if not isinstance(correlation_results, dict):
            raise TypeError("Expected correlation_results to be a dictionary.")
        if not isinstance(knn_main_results, dict):
            raise TypeError("Expected knn_main_results to be a dictionary.")
        if not isinstance(knn_range_results, dict):
            raise TypeError("Expected knn_range_results to be a dictionary.")

        pca_thresholds, _, _ = validate_pca_results(pca_results)
        correlation_dimension = validate_correlation_results(correlation_results)
        _, knn_estimate, _, _, _ = validate_knn_main_results(knn_main_results)
        _, _, mean_estimate, _, _, _ = validate_knn_range_results(knn_range_results)

        ambient_dim = x_raw_shape[1]
        processed_dim = x_processed_shape[1]

        print(
            f"{dataset_name:<30} "
            f"{ambient_dim:>12d} "
            f"{processed_dim:>14d} "
            f"{pca_thresholds[0.90]:>10d} "
            f"{correlation_dimension:>12.2f} "
            f"{knn_estimate:>12.2f} "
            f"{mean_estimate:>12.2f}"
        )


# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------

def main() -> None:
    """
    Execute the complete intrinsic-dimension analysis workflow.

    The workflow includes:
    - loading all datasets used in the project,
    - preprocessing each dataset,
    - estimating intrinsic dimensionality using PCA,
    - estimating correlation dimension,
    - estimating kNN-based intrinsic dimension,
    - evaluating kNN sensitivity across multiple k values,
    - printing per-dataset summaries and a final comparison table.
    """
    print("\nLoading datasets...\n")

    x_mnist, _ = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, _ = load_swiss_roll()

    results: list[dict[str, object]] = [
        analyze_dataset(
            dataset_name="MNIST",
            x_raw=x_mnist,
            use_sampling_for_geometric_methods=True,
        ),
        analyze_dataset(
            dataset_name="Gaussian Noise",
            x_raw=x_gaussian,
            use_sampling_for_geometric_methods=False,
        ),
        analyze_dataset(
            dataset_name="2D Plane Embedded in 10D",
            x_raw=x_plane,
            use_sampling_for_geometric_methods=False,
        ),
        analyze_dataset(
            dataset_name="Swiss Roll",
            x_raw=x_swiss,
            use_sampling_for_geometric_methods=False,
        ),
    ]

    print_title("INTRINSIC DIMENSION ANALYSIS - COMPLETE PIPELINE REPORT")

    for result in results:
        print_dataset_results(result)

    print_final_summary_table(results)
    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
