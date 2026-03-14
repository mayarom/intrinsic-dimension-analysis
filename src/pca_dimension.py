import numpy as np
from sklearn.decomposition import PCA


def fit_pca(
    x: np.ndarray,
    n_components: int | None = None
) -> PCA:
    """
    Fit PCA to the input dataset.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).
    n_components : int | None
        Number of principal components to keep.
        If None, all components are kept.

    Returns
    -------
    PCA
        Fitted PCA object.
    """
    pca = PCA(n_components=n_components)
    pca.fit(x)
    return pca


def get_explained_variance_ratio(pca: PCA) -> np.ndarray:
    """
    Return the explained variance ratio of each principal component.

    Parameters
    ----------
    pca : PCA
        Fitted PCA object.

    Returns
    -------
    np.ndarray
        Explained variance ratio for each component.
    """
    return pca.explained_variance_ratio_


def get_cumulative_explained_variance(pca: PCA) -> np.ndarray:
    """
    Compute the cumulative explained variance ratio.

    Parameters
    ----------
    pca : PCA
        Fitted PCA object.

    Returns
    -------
    np.ndarray
        Cumulative explained variance ratio.
    """
    return np.cumsum(pca.explained_variance_ratio_)


def get_components_for_threshold(
    cumulative_variance: np.ndarray,
    threshold: float
) -> int:
    """
    Compute the number of principal components required to reach
    a given explained variance threshold.

    Parameters
    ----------
    cumulative_variance : np.ndarray
        Cumulative explained variance ratio.
    threshold : float
        Desired threshold, such as 0.90, 0.95, or 0.99.

    Returns
    -------
    int
        Number of components required to reach the threshold.
    """
    if not 0.0 < threshold <= 1.0:
        raise ValueError("Threshold must be in the interval (0, 1].")

    return int(np.argmax(cumulative_variance >= threshold) + 1)


def estimate_pca_dimensionality(
    x: np.ndarray,
    thresholds: tuple[float, ...] = (0.90, 0.95, 0.99)
) -> dict[str, object]:
    """
    Estimate dimensionality using PCA and variance thresholds.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).
    thresholds : tuple[float, ...]
        Variance thresholds for dimensionality estimation.

    Returns
    -------
    dict[str, object]
        Dictionary containing the PCA model, explained variance,
        cumulative explained variance, and required components
        for each threshold.
    """
    pca = fit_pca(x)
    explained_variance_ratio = get_explained_variance_ratio(pca)
    cumulative_variance = get_cumulative_explained_variance(pca)

    components_per_threshold: dict[float, int] = {}
    for threshold in thresholds:
        components_per_threshold[threshold] = get_components_for_threshold(
            cumulative_variance,
            threshold
        )

    return {
        "pca_model": pca,
        "explained_variance_ratio": explained_variance_ratio,
        "cumulative_explained_variance": cumulative_variance,
        "components_per_threshold": components_per_threshold,
    }


def print_pca_summary(results: dict[str, object]) -> None:
    """
    Print a readable summary of PCA dimensionality estimation results.

    Parameters
    ----------
    results : dict[str, object]
        Dictionary returned by estimate_pca_dimensionality().
    """
    explained_variance_ratio = results["explained_variance_ratio"]
    cumulative_variance = results["cumulative_explained_variance"]
    components_per_threshold = results["components_per_threshold"]

    if not isinstance(explained_variance_ratio, np.ndarray):
        raise TypeError("Expected explained_variance_ratio to be a NumPy array.")

    if not isinstance(cumulative_variance, np.ndarray):
        raise TypeError("Expected cumulative_explained_variance to be a NumPy array.")

    if not isinstance(components_per_threshold, dict):
        raise TypeError("Expected components_per_threshold to be a dictionary.")

    print("Number of PCA components fitted:", len(explained_variance_ratio))
    print("First 10 explained variance ratios:")
    print(explained_variance_ratio[:10])
    print()

    print("First 10 cumulative explained variance values:")
    print(cumulative_variance[:10])
    print()

    print("Number of components required for each threshold:")
    for threshold, n_components in components_per_threshold.items():
        print(f"{int(threshold * 100)}% variance: {n_components} components")


def main() -> None:
    """
    Run a small PCA dimensionality estimation demo on random data.
    """
    rng = np.random.default_rng(42)
    x_demo = rng.normal(size=(500, 20))

    results = estimate_pca_dimensionality(
        x_demo,
        thresholds=(0.90, 0.95, 0.99)
    )

    print_pca_summary(results)


if __name__ == "__main__":
    main()
