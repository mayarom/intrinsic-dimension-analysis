import numpy as np
from scipy.spatial.distance import pdist
from sklearn.linear_model import LinearRegression


def compute_pairwise_distances(x: np.ndarray) -> np.ndarray:
    """
    Compute all pairwise Euclidean distances between samples.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).

    Returns
    -------
    np.ndarray
        Condensed array of pairwise distances.
    """
    return pdist(x, metric="euclidean")


def generate_radius_values(
    distances: np.ndarray,
    n_radii: int = 30,
    min_percentile: float = 1.0,
    max_percentile: float = 50.0
) -> np.ndarray:
    """
    Generate a sequence of radius values based on pairwise distance percentiles.

    Parameters
    ----------
    distances : np.ndarray
        Condensed array of pairwise distances.
    n_radii : int
        Number of radius values to generate.
    min_percentile : float
        Lower percentile used to define the minimum radius.
    max_percentile : float
        Upper percentile used to define the maximum radius.

    Returns
    -------
    np.ndarray
        Log-spaced radius values.
    """
    if distances.size == 0:
        raise ValueError("Distance array is empty.")

    if not 0.0 <= min_percentile < max_percentile <= 100.0:
        raise ValueError(
            "Percentiles must satisfy 0 <= min_percentile < max_percentile <= 100."
        )

    r_min = np.percentile(distances, min_percentile)
    r_max = np.percentile(distances, max_percentile)

    if r_min <= 0.0:
        positive_distances = distances[distances > 0.0]
        if positive_distances.size == 0:
            raise ValueError("All pairwise distances are zero.")
        r_min = positive_distances.min()

    if r_max <= r_min:
        raise ValueError("Maximum radius must be greater than minimum radius.")

    return np.logspace(np.log10(r_min), np.log10(r_max), num=n_radii)


def compute_correlation_integral(
    distances: np.ndarray,
    radii: np.ndarray
) -> np.ndarray:
    """
    Compute the correlation integral C(r) for each radius value.

    Parameters
    ----------
    distances : np.ndarray
        Condensed array of pairwise distances.
    radii : np.ndarray
        Radius values.

    Returns
    -------
    np.ndarray
        Correlation integral values for each radius.
    """
    if distances.size == 0:
        raise ValueError("Distance array is empty.")

    sorted_distances = np.sort(distances)
    counts = np.searchsorted(sorted_distances, radii, side="right")
    correlation_integral = counts / sorted_distances.size

    return correlation_integral


def select_scaling_region(
    log_radii: np.ndarray,
    log_correlation_integral: np.ndarray,
    start_index: int = 5,
    end_index: int | None = 20
) -> tuple[np.ndarray, np.ndarray]:
    """
    Select a subset of the log-log curve as the scaling region.

    Parameters
    ----------
    log_radii : np.ndarray
        Logarithm of radius values.
    log_correlation_integral : np.ndarray
        Logarithm of correlation integral values.
    start_index : int
        Start index of the scaling region.
    end_index : int | None
        End index of the scaling region.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Selected log_radii and log_correlation_integral arrays.
    """
    if end_index is None:
        end_index = len(log_radii)

    if not 0 <= start_index < end_index <= len(log_radii):
        raise ValueError("Invalid scaling region indices.")

    return (
        log_radii[start_index:end_index],
        log_correlation_integral[start_index:end_index],
    )


def estimate_correlation_dimension_from_logs(
    log_radii_region: np.ndarray,
    log_correlation_region: np.ndarray
) -> tuple[float, LinearRegression]:
    """
    Estimate the correlation dimension from the selected log-log region.

    Parameters
    ----------
    log_radii_region : np.ndarray
        Logarithm of radii in the selected scaling region.
    log_correlation_region : np.ndarray
        Logarithm of correlation integral values in the selected scaling region.

    Returns
    -------
    tuple[float, LinearRegression]
        Estimated correlation dimension and fitted linear regression model.
    """
    if log_radii_region.ndim != 1 or log_correlation_region.ndim != 1:
        raise ValueError("Input arrays must be one-dimensional.")

    if log_radii_region.size != log_correlation_region.size:
        raise ValueError("Input arrays must have the same length.")

    if log_radii_region.size < 2:
        raise ValueError("At least two points are required for linear regression.")

    model = LinearRegression()
    model.fit(log_radii_region.reshape(-1, 1), log_correlation_region)

    estimated_dimension = float(model.coef_[0])
    return estimated_dimension, model


def estimate_correlation_dimension(
    x: np.ndarray,
    n_radii: int = 30,
    min_percentile: float = 1.0,
    max_percentile: float = 50.0,
    scaling_region_start: int = 5,
    scaling_region_end: int | None = 20
) -> dict[str, object]:
    """
    Estimate the correlation dimension of a dataset.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).
    n_radii : int
        Number of radius values to generate.
    min_percentile : float
        Lower percentile for radius generation.
    max_percentile : float
        Upper percentile for radius generation.
    scaling_region_start : int
        Start index of the selected scaling region.
    scaling_region_end : int | None
        End index of the selected scaling region.

    Returns
    -------
    dict[str, object]
        Dictionary containing intermediate results and the final estimate.
    """
    distances = compute_pairwise_distances(x)
    radii = generate_radius_values(
        distances=distances,
        n_radii=n_radii,
        min_percentile=min_percentile,
        max_percentile=max_percentile
    )

    correlation_integral = compute_correlation_integral(
        distances=distances,
        radii=radii
    )

    valid_mask = (radii > 0.0) & (correlation_integral > 0.0)
    radii = radii[valid_mask]
    correlation_integral = correlation_integral[valid_mask]

    log_radii = np.log(radii)
    log_correlation_integral = np.log(correlation_integral)

    log_radii_region, log_correlation_region = select_scaling_region(
        log_radii=log_radii,
        log_correlation_integral=log_correlation_integral,
        start_index=scaling_region_start,
        end_index=scaling_region_end
    )

    estimated_dimension, regression_model = estimate_correlation_dimension_from_logs(
        log_radii_region=log_radii_region,
        log_correlation_region=log_correlation_region
    )

    return {
        "pairwise_distances": distances,
        "radii": radii,
        "correlation_integral": correlation_integral,
        "log_radii": log_radii,
        "log_correlation_integral": log_correlation_integral,
        "log_radii_region": log_radii_region,
        "log_correlation_region": log_correlation_region,
        "estimated_dimension": estimated_dimension,
        "regression_model": regression_model,
    }


def print_correlation_dimension_summary(results: dict[str, object]) -> None:
    """
    Print a readable summary of correlation dimension estimation results.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by estimate_correlation_dimension().
    """
    radii = results["radii"]
    correlation_integral = results["correlation_integral"]
    estimated_dimension = results["estimated_dimension"]

    if not isinstance(radii, np.ndarray):
        raise TypeError("Expected radii to be a NumPy array.")

    if not isinstance(correlation_integral, np.ndarray):
        raise TypeError("Expected correlation_integral to be a NumPy array.")

    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")

    print("Number of radius values:", len(radii))
    print("First 10 radii:")
    print(radii[:10])
    print()

    print("First 10 correlation integral values:")
    print(correlation_integral[:10])
    print()

    print("Estimated correlation dimension:")
    print(f"{estimated_dimension:.6f}")


def main() -> None:
    """
    Run a small correlation dimension demo on random data.
    """
    rng = np.random.default_rng(42)
    x_demo = rng.normal(size=(500, 10))

    results = estimate_correlation_dimension(
        x=x_demo,
        n_radii=30,
        min_percentile=1.0,
        max_percentile=50.0,
        scaling_region_start=5,
        scaling_region_end=20
    )

    print_correlation_dimension_summary(results)


if __name__ == "__main__":
    main()
