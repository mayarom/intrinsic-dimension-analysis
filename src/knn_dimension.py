
from __future__ import annotations

from typing import Final

import numpy as np
from sklearn.neighbors import NearestNeighbors

from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from preprocessing import preprocessing_pipeline, sample_dataset


_EPSILON: Final[float] = 1e-12
DEFAULT_K: Final[int] = 10
DEFAULT_K_VALUES: Final[tuple[int, ...]] = (5, 8, 10, 12, 15, 20)
MNIST_SAMPLE_SIZE: Final[int] = 1000
RANDOM_STATE: Final[int] = 42


def _validate_input_array(x: np.ndarray) -> np.ndarray:
    """
    Validate the input feature matrix.

    Parameters
    ----------
    x : np.ndarray
        Input data matrix of shape (n_samples, n_features).

    Returns
    -------
    np.ndarray
        Validated floating-point array.

    Raises
    ------
    TypeError
        If x is not a NumPy array.
    ValueError
        If x is not a 2D array or contains too few samples/features.
    """
    if not isinstance(x, np.ndarray):
        raise TypeError("Expected x to be a NumPy array.")

    if x.ndim != 2:
        raise ValueError("Expected x to be a 2D array of shape (n_samples, n_features).")

    n_samples, n_features = x.shape

    if n_samples < 3:
        raise ValueError("At least 3 samples are required.")
    if n_features < 1:
        raise ValueError("At least 1 feature is required.")

    return x.astype(np.float64, copy=False)


def _validate_k(k: int, n_samples: int) -> int:
    """
    Validate the neighborhood size k.

    Parameters
    ----------
    k : int
        Number of nearest neighbors to use in the estimator.
    n_samples : int
        Number of samples in the dataset.

    Returns
    -------
    int
        Validated neighborhood size.

    Raises
    ------
    TypeError
        If k is not an integer.
    ValueError
        If k is outside the valid range.
    """
    if not isinstance(k, int):
        raise TypeError("Expected k to be an integer.")

    if k < 2:
        raise ValueError("k must be at least 2 for the Levina-Bickel estimator.")

    if k >= n_samples:
        raise ValueError("k must be smaller than the number of samples.")

    return k


def _compute_knn_distances(
    x: np.ndarray,
    n_neighbors: int,
    metric: str = "euclidean",
    n_jobs: int | None = None,
) -> np.ndarray:
    """
    Compute nearest-neighbor distances for all samples.

    Notes
    -----
    The first returned neighbor is each point itself at distance zero.
    Therefore, if the estimator needs k neighbors excluding self, this
    function should be called with n_neighbors = k + 1.

    Parameters
    ----------
    x : np.ndarray
        Data matrix of shape (n_samples, n_features).
    n_neighbors : int
        Number of neighbors to query, including self.
    metric : str
        Distance metric passed to scikit-learn NearestNeighbors.
    n_jobs : int | None
        Number of parallel jobs.

    Returns
    -------
    np.ndarray
        Distance matrix of shape (n_samples, n_neighbors).
    """
    model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric=metric,
        n_jobs=n_jobs,
    )
    model.fit(x)
    distances, _ = model.kneighbors(x, return_distance=True)
    return distances


def _levina_bickel_local_estimates(
    neighbor_distances: np.ndarray,
    k: int,
) -> np.ndarray:
    """
    Compute local intrinsic-dimension estimates using the Levina-Bickel MLE.

    Parameters
    ----------
    neighbor_distances : np.ndarray
        Distance matrix of shape (n_samples, k + 1), where the first column
        is the self-distance (zero), and the next k columns are the nearest
        neighbors excluding self.
    k : int
        Number of neighbors excluding self used by the estimator.

    Returns
    -------
    np.ndarray
        Local intrinsic-dimension estimates of shape (n_samples,).

    Notes
    -----
    For each sample x_i, the estimator is:

        m_i = [ (1 / (k - 1)) * sum_{j=1}^{k-1} log(T_k / T_j) ]^{-1}

    where T_j is the distance from x_i to its j-th nearest neighbor.
    """
    if not isinstance(neighbor_distances, np.ndarray):
        raise TypeError("Expected neighbor_distances to be a NumPy array.")

    if neighbor_distances.ndim != 2:
        raise ValueError("Expected neighbor_distances to be a 2D array.")

    if neighbor_distances.shape[1] != k + 1:
        raise ValueError("Expected neighbor_distances to have k + 1 columns.")

    knn_distances = neighbor_distances[:, 1:]
    t_j = knn_distances[:, : k - 1]
    t_k = knn_distances[:, [k - 1]]

    t_j = np.maximum(t_j, _EPSILON)
    t_k = np.maximum(t_k, _EPSILON)

    log_ratios = np.log(t_k / t_j)
    mean_log_ratios = np.mean(log_ratios, axis=1)
    mean_log_ratios = np.maximum(mean_log_ratios, _EPSILON)

    local_estimates = 1.0 / mean_log_ratios
    return local_estimates


def estimate_knn_dimension(
    x: np.ndarray,
    k: int = DEFAULT_K,
    metric: str = "euclidean",
    aggregate: str = "mean",
    n_jobs: int | None = None,
) -> dict[str, object]:
    """
    Estimate intrinsic dimension using the kNN-based Levina-Bickel MLE.

    Parameters
    ----------
    x : np.ndarray
        Input data matrix of shape (n_samples, n_features).
    k : int, default=10
        Number of nearest neighbors excluding self.
    metric : str, default="euclidean"
        Distance metric used for nearest-neighbor search.
    aggregate : str, default="mean"
        Aggregation strategy for the global estimate.
        Supported values are "mean" and "median".
    n_jobs : int | None, default=None
        Number of parallel jobs passed to NearestNeighbors.

    Returns
    -------
    dict[str, object]
        Dictionary containing the local estimates, summary statistics,
        and the final global intrinsic-dimension estimate.
    """
    x_valid = _validate_input_array(x)
    n_samples, n_features = x_valid.shape
    k_valid = _validate_k(k, n_samples)

    if aggregate not in {"mean", "median"}:
        raise ValueError("aggregate must be either 'mean' or 'median'.")

    neighbor_distances = _compute_knn_distances(
        x=x_valid,
        n_neighbors=k_valid + 1,
        metric=metric,
        n_jobs=n_jobs,
    )

    local_estimates = _levina_bickel_local_estimates(
        neighbor_distances=neighbor_distances,
        k=k_valid,
    )

    mean_local_dimension = float(np.mean(local_estimates))
    median_local_dimension = float(np.median(local_estimates))
    std_local_dimension = float(np.std(local_estimates, ddof=0))

    if aggregate == "mean":
        estimated_dimension = mean_local_dimension
    else:
        estimated_dimension = median_local_dimension

    return {
        "method": "kNN Levina-Bickel MLE",
        "k": k_valid,
        "metric": metric,
        "aggregate": aggregate,
        "n_samples": n_samples,
        "n_features": n_features,
        "neighbor_distances": neighbor_distances,
        "local_estimates": local_estimates,
        "estimated_dimension": float(estimated_dimension),
        "mean_local_dimension": mean_local_dimension,
        "median_local_dimension": median_local_dimension,
        "std_local_dimension": std_local_dimension,
        "min_local_dimension": float(np.min(local_estimates)),
        "max_local_dimension": float(np.max(local_estimates)),
    }


def estimate_knn_dimension_over_k_range(
    x: np.ndarray,
    k_values: list[int] | np.ndarray,
    metric: str = "euclidean",
    aggregate: str = "mean",
    n_jobs: int | None = None,
) -> dict[str, object]:
    """
    Estimate intrinsic dimension over a range of k values.

    Parameters
    ----------
    x : np.ndarray
        Input data matrix of shape (n_samples, n_features).
    k_values : list[int] | np.ndarray
        Sequence of k values to evaluate.
    metric : str, default="euclidean"
        Distance metric used for nearest-neighbor search.
    aggregate : str, default="mean"
        Aggregation strategy for the global estimate.
    n_jobs : int | None, default=None
        Number of parallel jobs passed to NearestNeighbors.

    Returns
    -------
    dict[str, object]
        Summary dictionary containing k values and resulting estimates.
    """
    x_valid = _validate_input_array(x)

    if not isinstance(k_values, (list, np.ndarray, tuple)):
        raise TypeError("Expected k_values to be a list, tuple, or NumPy array.")

    k_array = np.asarray(k_values)

    if k_array.ndim != 1:
        raise ValueError("Expected k_values to be a 1D sequence.")

    if len(k_array) == 0:
        raise ValueError("k_values must not be empty.")

    estimates: list[float] = []

    for k_value in k_array:
        if not isinstance(k_value, (int, np.integer)):
            raise TypeError("All k_values must be integers.")

        result = estimate_knn_dimension(
            x=x_valid,
            k=int(k_value),
            metric=metric,
            aggregate=aggregate,
            n_jobs=n_jobs,
        )

        estimated_dimension = result["estimated_dimension"]
        if not isinstance(estimated_dimension, float):
            raise TypeError("Expected estimated_dimension to be a float.")

        estimates.append(estimated_dimension)

    estimates_array = np.asarray(estimates, dtype=np.float64)

    return {
        "k_values": k_array.astype(int),
        "dimension_estimates": estimates_array,
        "mean_estimate": float(np.mean(estimates_array)),
        "std_estimate": float(np.std(estimates_array, ddof=0)),
        "min_estimate": float(np.min(estimates_array)),
        "max_estimate": float(np.max(estimates_array)),
    }


def _get_processed_array(
    results: dict[str, object],
    key: str = "x_processed",
) -> np.ndarray:
    """
    Extract a processed NumPy array from a preprocessing results dictionary.
    """
    value = results.get(key)

    if not isinstance(value, np.ndarray):
        raise TypeError(f"Expected '{key}' to be a NumPy array.")

    return value


def preprocess_for_knn(x: np.ndarray) -> np.ndarray:
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
    return _get_processed_array(preprocessing_results)


def analyze_dataset_with_knn(
    dataset_name: str,
    x: np.ndarray,
    k: int = DEFAULT_K,
    k_values: tuple[int, ...] = DEFAULT_K_VALUES,
    metric: str = "euclidean",
    aggregate: str = "mean",
    n_jobs: int | None = None,
) -> dict[str, object]:
    """
    Run the complete kNN-based intrinsic-dimension analysis for one dataset.

    Parameters
    ----------
    dataset_name : str
        Display name of the dataset.
    x : np.ndarray
        Input feature matrix.
    k : int, default=10
        Main k value used for the headline estimate.
    k_values : tuple[int, ...], default=(5, 8, 10, 12, 15, 20)
        Range of k values used for sensitivity analysis.
    metric : str, default="euclidean"
        Distance metric for nearest-neighbor search.
    aggregate : str, default="mean"
        Aggregation strategy for the global estimate.
    n_jobs : int | None, default=None
        Number of parallel jobs.

    Returns
    -------
    dict[str, object]
        Full analysis results for the dataset.
    """
    x_processed = preprocess_for_knn(x)

    main_result = estimate_knn_dimension(
        x=x_processed,
        k=k,
        metric=metric,
        aggregate=aggregate,
        n_jobs=n_jobs,
    )

    range_result = estimate_knn_dimension_over_k_range(
        x=x_processed,
        k_values=list(k_values),
        metric=metric,
        aggregate=aggregate,
        n_jobs=n_jobs,
    )

    return {
        "dataset_name": dataset_name,
        "x_processed": x_processed,
        "main_result": main_result,
        "range_result": range_result,
    }


def print_knn_analysis_report(analysis_result: dict[str, object]) -> None:
    """
    Print a report-friendly summary of one dataset's kNN-based analysis.
    """
    dataset_name = analysis_result["dataset_name"]
    x_processed = analysis_result["x_processed"]
    main_result = analysis_result["main_result"]
    range_result = analysis_result["range_result"]

    if not isinstance(dataset_name, str):
        raise TypeError("Expected dataset_name to be a string.")
    if not isinstance(x_processed, np.ndarray):
        raise TypeError("Expected x_processed to be a NumPy array.")
    if not isinstance(main_result, dict):
        raise TypeError("Expected main_result to be a dictionary.")
    if not isinstance(range_result, dict):
        raise TypeError("Expected range_result to be a dictionary.")

    shape = x_processed.shape
    estimated_dimension = main_result["estimated_dimension"]
    mean_local_dimension = main_result["mean_local_dimension"]
    median_local_dimension = main_result["median_local_dimension"]
    std_local_dimension = main_result["std_local_dimension"]
    k = main_result["k"]

    k_values = range_result["k_values"]
    dimension_estimates = range_result["dimension_estimates"]
    mean_estimate = range_result["mean_estimate"]
    std_estimate = range_result["std_estimate"]
    min_estimate = range_result["min_estimate"]
    max_estimate = range_result["max_estimate"]

    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")
    if not isinstance(mean_local_dimension, float):
        raise TypeError("Expected mean_local_dimension to be a float.")
    if not isinstance(median_local_dimension, float):
        raise TypeError("Expected median_local_dimension to be a float.")
    if not isinstance(std_local_dimension, float):
        raise TypeError("Expected std_local_dimension to be a float.")
    if not isinstance(k, int):
        raise TypeError("Expected k to be an integer.")
    if not isinstance(k_values, np.ndarray):
        raise TypeError("Expected k_values to be a NumPy array.")
    if not isinstance(dimension_estimates, np.ndarray):
        raise TypeError("Expected dimension_estimates to be a NumPy array.")

    print("=" * 88)
    print(f"DATASET: {dataset_name}")
    print("=" * 88)
    print(f"Processed shape: {shape}")
    print()
    print("Headline kNN intrinsic-dimension estimate")
    print("-" * 88)
    print(f"Method:               kNN Levina-Bickel MLE")
    print(f"Distance metric:      euclidean")
    print(f"Aggregation:          mean")
    print(f"Selected k:           {k}")
    print(f"Estimated dimension:  {estimated_dimension:.4f}")
    print(f"Mean local estimate:  {mean_local_dimension:.4f}")
    print(f"Median local estimate:{median_local_dimension:.4f}")
    print(f"Std. local estimate:  {std_local_dimension:.4f}")
    print()
    print("Sensitivity analysis across k values")
    print("-" * 88)
    for k_value, estimate in zip(k_values, dimension_estimates):
        print(f"k = {int(k_value):>2d} -> estimated dimension = {float(estimate):.4f}")
    print()
    print("Stability summary")
    print("-" * 88)
    print(f"Mean estimate across k: {mean_estimate:.4f}")
    print(f"Std. across k:          {std_estimate:.4f}")
    print(f"Min estimate across k:  {min_estimate:.4f}")
    print(f"Max estimate across k:  {max_estimate:.4f}")
    print()
    print("Suggested report sentence")
    print("-" * 88)
    print(
        f"For {dataset_name}, the kNN-based intrinsic-dimension estimate "
        f"(Levina-Bickel MLE, k={k}) was {estimated_dimension:.2f}. "
        f"Across the tested range k={list(k_values.astype(int))}, the estimates "
        f"remained within [{min_estimate:.2f}, {max_estimate:.2f}] "
        f"with a mean of {mean_estimate:.2f}, indicating "
        f"{'good' if std_estimate < 1.0 else 'moderate'} stability."
    )
    print()


def main() -> None:
    """
    Run the kNN-based intrinsic-dimension analysis on all project datasets and
    print a report-ready summary.

    Notes
    -----
    - MNIST is sampled to 1000 observations for computational efficiency.
    - All datasets use the same preprocessing pipeline as the rest of the project.
    """
    print("\nLoading datasets...\n")

    x_mnist, y_mnist = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, _ = load_swiss_roll()

    x_mnist_sampled, _ = sample_dataset(
        x=x_mnist,
        y=y_mnist,
        n_samples=MNIST_SAMPLE_SIZE,
        random_state=RANDOM_STATE,
    )

    dataset_map: list[tuple[str, np.ndarray]] = [
        ("MNIST (sampled)", x_mnist_sampled),
        ("Gaussian Noise", x_gaussian),
        ("2D Plane Embedded in 10D", x_plane),
        ("Swiss Roll", x_swiss),
    ]

    all_results: list[dict[str, object]] = []

    for dataset_name, x_data in dataset_map:
        result = analyze_dataset_with_knn(
            dataset_name=dataset_name,
            x=x_data,
            k=DEFAULT_K,
            k_values=DEFAULT_K_VALUES,
            metric="euclidean",
            aggregate="mean",
            n_jobs=None,
        )
        all_results.append(result)

    print("\n" + "#" * 88)
    print("kNN-BASED INTRINSIC DIMENSION ANALYSIS - COMPLETE REPORT")
    print("#" * 88 + "\n")

    for result in all_results:
        print_knn_analysis_report(result)

    print("=" * 88)
    print("FINAL SUMMARY TABLE")
    print("=" * 88)
    print(
        f"{'Dataset':<30} {'k':>4} {'Main Estimate':>16} "
        f"{'Mean Across k':>16} {'Std Across k':>14}"
    )
    print("-" * 88)

    for result in all_results:
        dataset_name = result["dataset_name"]
        main_result = result["main_result"]
        range_result = result["range_result"]

        if not isinstance(dataset_name, str):
            raise TypeError("Expected dataset_name to be a string.")
        if not isinstance(main_result, dict):
            raise TypeError("Expected main_result to be a dictionary.")
        if not isinstance(range_result, dict):
            raise TypeError("Expected range_result to be a dictionary.")

        k = main_result["k"]
        main_estimate = main_result["estimated_dimension"]
        mean_across_k = range_result["mean_estimate"]
        std_across_k = range_result["std_estimate"]

        if not isinstance(k, int):
            raise TypeError("Expected k to be an integer.")
        if not isinstance(main_estimate, float):
            raise TypeError("Expected main_estimate to be a float.")
        if not isinstance(mean_across_k, float):
            raise TypeError("Expected mean_across_k to be a float.")
        if not isinstance(std_across_k, float):
            raise TypeError("Expected std_across_k to be a float.")

        print(
            f"{dataset_name:<30} {k:>4d} {main_estimate:>16.4f} "
            f"{mean_across_k:>16.4f} {std_across_k:>14.4f}"
        )

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
