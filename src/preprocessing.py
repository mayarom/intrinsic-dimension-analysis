from typing import Optional

import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def standardize_data(x: np.ndarray) -> tuple[np.ndarray, StandardScaler]:
    """
    Standardize the dataset so that each feature has zero mean and unit variance.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).

    Returns
    -------
    tuple[np.ndarray, StandardScaler]
        x_scaled : np.ndarray
            Standardized data.
        scaler : StandardScaler
            Fitted scaler object.
    """
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    return x_scaled, scaler


def normalize_data(x: np.ndarray) -> tuple[np.ndarray, MinMaxScaler]:
    """
    Normalize the dataset so that each feature is scaled to the range [0, 1].

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).

    Returns
    -------
    tuple[np.ndarray, MinMaxScaler]
        x_normalized : np.ndarray
            Normalized data.
        scaler : MinMaxScaler
            Fitted scaler object.
    """
    scaler = MinMaxScaler()
    x_normalized = scaler.fit_transform(x)
    return x_normalized, scaler


def remove_constant_features(
    x: np.ndarray,
    threshold: float = 0.0
) -> tuple[np.ndarray, VarianceThreshold]:
    """
    Remove features with variance less than or equal to the given threshold.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).
    threshold : float
        Features with variance less than or equal to this value are removed.

    Returns
    -------
    tuple[np.ndarray, VarianceThreshold]
        x_reduced : np.ndarray
            Data after removing low-variance features.
        selector : VarianceThreshold
            Fitted feature selector object.
    """
    selector = VarianceThreshold(threshold=threshold)
    x_reduced = selector.fit_transform(x)
    return x_reduced, selector


def sample_dataset(
    x: np.ndarray,
    y: Optional[np.ndarray] = None,
    n_samples: int = 1000,
    random_state: int = 42
) -> tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Randomly sample a subset of the dataset without replacement.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_total_samples, n_features).
    y : Optional[np.ndarray]
        Optional label array of shape (n_total_samples,).
    n_samples : int
        Number of samples to draw.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    tuple[np.ndarray, Optional[np.ndarray]]
        x_sampled : np.ndarray
            Sampled feature matrix.
        y_sampled : Optional[np.ndarray]
            Sampled labels if provided, otherwise None.
    """
    if n_samples > x.shape[0]:
        raise ValueError(
            f"Requested n_samples={n_samples}, but dataset only contains {x.shape[0]} samples."
        )

    rng = np.random.default_rng(random_state)
    indices = rng.choice(x.shape[0], size=n_samples, replace=False)

    x_sampled = x[indices]

    if y is None:
        return x_sampled, None

    y_sampled = y[indices]
    return x_sampled, y_sampled


def preprocessing_pipeline(
    x: np.ndarray,
    remove_constants: bool = True,
    variance_threshold: float = 0.0,
    apply_standardization: bool = True,
    apply_normalization: bool = False
) -> dict[str, object]:
    """
    Apply a configurable preprocessing pipeline to the input dataset.

    Parameters
    ----------
    x : np.ndarray
        Input data of shape (n_samples, n_features).
    remove_constants : bool
        Whether to remove constant or near-constant features.
    variance_threshold : float
        Variance threshold used when removing low-variance features.
    apply_standardization : bool
        Whether to standardize the data.
    apply_normalization : bool
        Whether to normalize the data to the range [0, 1].

    Returns
    -------
    dict[str, object]
        Dictionary containing the processed data and fitted preprocessing objects.
    """
    x_processed = x.copy()

    results: dict[str, object] = {
        "x_original": x,
        "x_processed": None,
        "variance_selector": None,
        "standard_scaler": None,
        "minmax_scaler": None,
    }

    if remove_constants:
        x_processed, variance_selector = remove_constant_features(
            x_processed,
            threshold=variance_threshold
        )
        results["variance_selector"] = variance_selector

    if apply_standardization:
        x_processed, standard_scaler = standardize_data(x_processed)
        results["standard_scaler"] = standard_scaler

    if apply_normalization:
        x_processed, minmax_scaler = normalize_data(x_processed)
        results["minmax_scaler"] = minmax_scaler

    results["x_processed"] = x_processed
    return results


def main() -> None:
    """
    Run a small preprocessing demo on random data.
    """
    rng = np.random.default_rng(42)
    x_demo = rng.normal(size=(100, 5))

    pipeline_results = preprocessing_pipeline(
        x_demo,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False
    )

    x_processed = pipeline_results["x_processed"]

    if not isinstance(x_processed, np.ndarray):
        raise TypeError("Expected x_processed to be a NumPy array.")

    print("Original shape:", x_demo.shape)
    print("Processed shape:", x_processed.shape)
    print("Preprocessing completed successfully.")


if __name__ == "__main__":
    main()
