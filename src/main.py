"""
import numpy as np

from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from preprocessing import preprocessing_pipeline


def main() -> None:
    x_mnist, y_mnist = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, t_swiss = load_swiss_roll()

    mnist_results = preprocessing_pipeline(x_mnist)
    gaussian_results = preprocessing_pipeline(x_gaussian)
    plane_results = preprocessing_pipeline(x_plane)
    swiss_results = preprocessing_pipeline(x_swiss)

    x_mnist_processed = mnist_results["x_processed"]
    x_gaussian_processed = gaussian_results["x_processed"]
    x_plane_processed = plane_results["x_processed"]
    x_swiss_processed = swiss_results["x_processed"]

    if not isinstance(x_mnist_processed, np.ndarray):
        raise TypeError("Expected x_mnist_processed to be a NumPy array.")

    if not isinstance(x_gaussian_processed, np.ndarray):
        raise TypeError("Expected x_gaussian_processed to be a NumPy array.")

    if not isinstance(x_plane_processed, np.ndarray):
        raise TypeError("Expected x_plane_processed to be a NumPy array.")

    if not isinstance(x_swiss_processed, np.ndarray):
        raise TypeError("Expected x_swiss_processed to be a NumPy array.")

    print("MNIST original shape:", x_mnist.shape)
    print("MNIST processed shape:", x_mnist_processed.shape)
    print("MNIST labels shape:", y_mnist.shape)
    print()

    print("Gaussian noise original shape:", x_gaussian.shape)
    print("Gaussian noise processed shape:", x_gaussian_processed.shape)
    print()

    print("2D plane in 10D original shape:", x_plane.shape)
    print("2D plane in 10D processed shape:", x_plane_processed.shape)
    print()

    print("Swiss roll original shape:", x_swiss.shape)
    print("Swiss roll processed shape:", x_swiss_processed.shape)
    print("Swiss roll parameter shape:", t_swiss.shape)


if __name__ == "__main__":
    main()
"""
from __future__ import annotations

"""
import numpy as np

from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from pca_dimension import estimate_pca_dimensionality, print_pca_summary
from preprocessing import preprocessing_pipeline


def get_processed_array(results: dict[str, object], key: str = "x_processed") -> np.ndarray:


    value = results.get(key)

    if not isinstance(value, np.ndarray):
        raise TypeError(f"Expected '{key}' to be a NumPy array.")

    return value


def run_preprocessing_and_pca(
    dataset_name: str,
    x: np.ndarray
) -> None:

    print("=" * 80)
    print(f"Dataset: {dataset_name}")
    print("=" * 80)

    preprocessing_results = preprocessing_pipeline(
        x,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False
    )

    x_processed = get_processed_array(preprocessing_results)

    print("Original shape:", x.shape)
    print("Processed shape:", x_processed.shape)
    print()

    pca_results = estimate_pca_dimensionality(
        x_processed,
        thresholds=(0.90, 0.95, 0.99)
    )
    print_pca_summary(pca_results)
    print()


def main() -> None:

    x_mnist, y_mnist = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, t_swiss = load_swiss_roll()

    print("All datasets loaded successfully.")
    print("MNIST labels shape:", y_mnist.shape)
    print("Swiss roll parameter shape:", t_swiss.shape)
    print()

    run_preprocessing_and_pca("MNIST", x_mnist)
    run_preprocessing_and_pca("Gaussian Noise", x_gaussian)
    run_preprocessing_and_pca("2D Plane Embedded in 10D", x_plane)
    run_preprocessing_and_pca("Swiss Roll", x_swiss)


if __name__ == "__main__":
    main()
"""
"""
import numpy as np

from correlation_dimension import (
    estimate_correlation_dimension,
    print_correlation_dimension_summary,
)
from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from pca_dimension import estimate_pca_dimensionality, print_pca_summary
from preprocessing import preprocessing_pipeline, sample_dataset


def get_processed_array(
    results: dict[str, object],
    key: str = "x_processed"
) -> np.ndarray:

    value = results.get(key)

    if not isinstance(value, np.ndarray):
        raise TypeError(f"Expected '{key}' to be a NumPy array.")

    return value


def run_preprocessing_and_pca(
    dataset_name: str,
    x: np.ndarray
) -> None:
    print("=" * 80)
    print(f"PCA Analysis - {dataset_name}")
    print("=" * 80)

    preprocessing_results = preprocessing_pipeline(
        x,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False
    )

    x_processed = get_processed_array(preprocessing_results)

    print("Original shape:", x.shape)
    print("Processed shape:", x_processed.shape)
    print()

    pca_results = estimate_pca_dimensionality(
        x_processed,
        thresholds=(0.90, 0.95, 0.99)
    )
    print_pca_summary(pca_results)
    print()


def run_preprocessing_and_correlation_dimension(
    dataset_name: str,
    x: np.ndarray,
    sample_size: int | None = None,
    random_state: int = 42,
    n_radii: int = 30,
    min_percentile: float = 1.0,
    max_percentile: float = 50.0,
    scaling_region_start: int = 5,
    scaling_region_end: int | None = 20
) -> None:

    print("=" * 80)
    print(f"Correlation Dimension Analysis - {dataset_name}")
    print("=" * 80)

    x_input = x

    if sample_size is not None:
        x_input, _ = sample_dataset(
            x=x,
            y=None,
            n_samples=sample_size,
            random_state=random_state
        )
        print("Original shape:", x.shape)
        print("Sampled shape:", x_input.shape)
    else:
        print("Original shape:", x.shape)

    preprocessing_results = preprocessing_pipeline(
        x_input,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False
    )

    x_processed = get_processed_array(preprocessing_results)

    print("Processed shape:", x_processed.shape)
    print()

    correlation_results = estimate_correlation_dimension(
        x=x_processed,
        n_radii=n_radii,
        min_percentile=min_percentile,
        max_percentile=max_percentile,
        scaling_region_start=scaling_region_start,
        scaling_region_end=scaling_region_end
    )
    print_correlation_dimension_summary(correlation_results)
    print()


def main() -> None:

    x_mnist, y_mnist = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, t_swiss = load_swiss_roll()

    print("All datasets loaded successfully.")
    print("MNIST labels shape:", y_mnist.shape)
    print("Swiss roll parameter shape:", t_swiss.shape)
    print()

    run_preprocessing_and_pca("MNIST", x_mnist)
    run_preprocessing_and_pca("Gaussian Noise", x_gaussian)
    run_preprocessing_and_pca("2D Plane Embedded in 10D", x_plane)
    run_preprocessing_and_pca("Swiss Roll", x_swiss)

    run_preprocessing_and_correlation_dimension(
        dataset_name="MNIST",
        x=x_mnist,
        sample_size=1000,
        random_state=42,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20
    )

    run_preprocessing_and_correlation_dimension(
        dataset_name="Gaussian Noise",
        x=x_gaussian,
        sample_size=None,
        random_state=42,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20
    )

    run_preprocessing_and_correlation_dimension(
        dataset_name="2D Plane Embedded in 10D",
        x=x_plane,
        sample_size=None,
        random_state=42,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20
    )

    run_preprocessing_and_correlation_dimension(
        dataset_name="Swiss Roll",
        x=x_swiss,
        sample_size=None,
        random_state=42,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20
    )


if __name__ == "__main__":
    main()
"""

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

MNIST_SAMPLE_SIZE_FOR_GEOMETRIC_METHODS: Final[int] = 1000
RANDOM_STATE: Final[int] = 42
DEFAULT_KNN_K: Final[int] = 10
DEFAULT_KNN_K_VALUES: Final[tuple[int, ...]] = (5, 8, 10, 12, 15, 20)


def get_processed_array(
        results: dict[str, object],
        key: str = "x_processed",
) -> np.ndarray:
    """
    Extract a processed NumPy array from a preprocessing results dictionary.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by preprocessing_pipeline().
    key : str, default="x_processed"
        Key under which the processed array is stored.

    Returns
    -------
    np.ndarray
        Extracted processed NumPy array.
    """
    value = results.get(key)

    if not isinstance(value, np.ndarray):
        raise TypeError(f"Expected '{key}' to be a NumPy array.")

    return value


def preprocess_for_analysis(x: np.ndarray) -> np.ndarray:
    """
    Apply the standard preprocessing configuration used in the project.

    Parameters
    ----------
    x : np.ndarray
        Input feature matrix.

    Returns
    -------
    np.ndarray
        Processed feature matrix.
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
    Print a separator line.

    Parameters
    ----------
    char : str, default="="
        Character used for the separator.
    width : int, default=100
        Separator width.
    """
    print(char * width)


def print_title(title: str) -> None:
    """
    Print a section title.

    Parameters
    ----------
    title : str
        Title text.
    """
    print_separator("=")
    print(title)
    print_separator("=")


def print_subtitle(subtitle: str) -> None:
    """
    Print a subsection title.

    Parameters
    ----------
    subtitle : str
        Subtitle text.
    """
    print(subtitle)
    print_separator("-")


def validate_pca_results(results: dict[str, object]) -> tuple[dict[float, int], np.ndarray, np.ndarray]:
    """
    Validate and extract PCA results.

    Parameters
    ----------
    results : dict[str, object]
        PCA results dictionary.

    Returns
    -------
    tuple[dict[float, int], np.ndarray, np.ndarray]
        Components per threshold, explained variance ratio, cumulative explained variance.
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

    return components_per_threshold, explained_variance_ratio, cumulative_explained_variance


def validate_correlation_results(results: dict[str, object]) -> float:
    """
    Validate and extract the estimated correlation dimension.

    Parameters
    ----------
    results : dict[str, object]
        Correlation-dimension results dictionary.

    Returns
    -------
    float
        Estimated correlation dimension.
    """
    estimated_dimension = results.get("estimated_dimension")

    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")

    return estimated_dimension


def validate_knn_main_results(results: dict[str, object]) -> tuple[int, float, float, float, float]:
    """
    Validate and extract the main kNN estimation summary.

    Parameters
    ----------
    results : dict[str, object]
        kNN results dictionary.

    Returns
    -------
    tuple[int, float, float, float, float]
        k, estimated_dimension, mean_local_dimension, median_local_dimension,
        std_local_dimension.
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


def validate_knn_range_results(results: dict[str, object]) -> tuple[np.ndarray, np.ndarray, float, float, float, float]:
    """
    Validate and extract the k-range kNN summary.

    Parameters
    ----------
    results : dict[str, object]
        k-range kNN results dictionary.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, float, float, float, float]
        k_values, dimension_estimates, mean_estimate, std_estimate,
        min_estimate, max_estimate.
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


def analyze_dataset(
        dataset_name: str,
        x_raw: np.ndarray,
        use_sampling_for_geometric_methods: bool = False,
) -> dict[str, object]:
    """
    Run the full analysis pipeline for one dataset.

    Parameters
    ----------
    dataset_name : str
        Dataset display name.
    x_raw : np.ndarray
        Raw feature matrix.
    use_sampling_for_geometric_methods : bool, default=False
        Whether to use sampling for correlation dimension and kNN methods.

    Returns
    -------
    dict[str, object]
        Full results dictionary for the dataset.
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

    pca_results = estimate_pca_dimensionality(x_processed)

    correlation_results = estimate_correlation_dimension(
        x=x_geometric_processed,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20,
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


def print_dataset_results(result: dict[str, object]) -> None:
    """
    Print all results for a single dataset in a report-friendly format.

    Parameters
    ----------
    result : dict[str, object]
        Dataset results dictionary.
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

    pca_thresholds, explained_variance_ratio, cumulative_explained_variance = validate_pca_results(pca_results)
    correlation_dimension = validate_correlation_results(correlation_results)
    knn_k, knn_estimate, knn_mean_local, knn_median_local, knn_std_local = validate_knn_main_results(knn_main_results)
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
    print(
        f"Cumulative variance at component 1:{float(cumulative_explained_variance[0]):.6f}"
    )
    print()

    print_subtitle("Correlation dimension estimation")
    print(f"Estimated correlation dimension:   {correlation_dimension:.4f}")
    print()

    print_subtitle("kNN-based intrinsic dimension estimation")
    print(f"Method:                            kNN Levina-Bickel MLE")
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
    Print a final summary table across all datasets.

    Parameters
    ----------
    results : list[dict[str, object]]
        List of dataset results.
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


def main() -> None:
    """
    Run the complete intrinsic-dimension analysis pipeline on all project datasets.

    The pipeline includes:
    - data loading
    - preprocessing
    - PCA-based dimensionality estimation
    - correlation dimension estimation
    - kNN-based intrinsic dimension estimation
    - sensitivity analysis over multiple k values
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
