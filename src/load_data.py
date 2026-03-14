from pathlib import Path

import numpy as np
from sklearn.datasets import fetch_openml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
MNIST_DIR = RAW_DATA_DIR / "mnist"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"


def ensure_data_directories() -> None:
    """
    Create the required data directories if they do not already exist.
    """
    MNIST_DIR.mkdir(parents=True, exist_ok=True)
    (SYNTHETIC_DATA_DIR / "gaussian_noise").mkdir(parents=True, exist_ok=True)
    (SYNTHETIC_DATA_DIR / "plane_2d_in_10d").mkdir(parents=True, exist_ok=True)
    (SYNTHETIC_DATA_DIR / "swiss_roll").mkdir(parents=True, exist_ok=True)


def load_mnist(as_frame: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """
    Load the MNIST dataset from OpenML.

    Parameters
    ----------
    as_frame : bool
        Whether to return the data as a pandas DataFrame internally.
        The returned values are always converted to NumPy arrays.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        X : array of shape (70000, 784)
            Flattened grayscale digit images.
        y : array of shape (70000,)
            Digit labels as integers.
    """
    ensure_data_directories()

    mnist = fetch_openml(
        name="mnist_784",
        version=1,
        as_frame=as_frame,
        parser="auto",
        data_home=str(MNIST_DIR)
    )

    X = np.asarray(mnist.data, dtype=np.float64)
    y = np.asarray(mnist.target, dtype=np.int64)

    return X, y


def load_gaussian_noise() -> np.ndarray:
    """
    Load the saved Gaussian noise dataset.

    Returns
    -------
    np.ndarray
        Array of shape (n_samples, n_features).
    """
    filepath = (
        SYNTHETIC_DATA_DIR
        / "gaussian_noise"
        / "gaussian_noise.npy"
    )

    if not filepath.exists():
        raise FileNotFoundError(
            f"Gaussian noise dataset not found at: {filepath}"
        )

    return np.load(filepath)


def load_plane_2d_in_10d() -> np.ndarray:
    """
    Load the saved 2D plane embedded in 10D dataset.

    Returns
    -------
    np.ndarray
        Array of shape (n_samples, 10).
    """
    filepath = (
        SYNTHETIC_DATA_DIR
        / "plane_2d_in_10d"
        / "plane_2d_in_10d.npy"
    )

    if not filepath.exists():
        raise FileNotFoundError(
            f"2D plane in 10D dataset not found at: {filepath}"
        )

    return np.load(filepath)


def load_swiss_roll() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the saved Swiss roll dataset and its parameter array.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        X : array of shape (n_samples, 3)
            Swiss roll samples in 3D ambient space.
        t : array of shape (n_samples,)
            The univariate position parameter along the roll.
    """
    x_filepath = (
        SYNTHETIC_DATA_DIR
        / "swiss_roll"
        / "swiss_roll_X.npy"
    )
    t_filepath = (
        SYNTHETIC_DATA_DIR
        / "swiss_roll"
        / "swiss_roll_t.npy"
    )

    if not x_filepath.exists():
        raise FileNotFoundError(
            f"Swiss roll samples not found at: {x_filepath}"
        )

    if not t_filepath.exists():
        raise FileNotFoundError(
            f"Swiss roll parameter array not found at: {t_filepath}"
        )

    X = np.load(x_filepath)
    t = np.load(t_filepath)

    return X, t


def load_all_datasets() -> dict[str, object]:
    """
    Load all datasets used in the project.

    Returns
    -------
    dict[str, object]
        Dictionary containing all loaded datasets.
    """
    X_mnist, y_mnist = load_mnist()
    X_gaussian = load_gaussian_noise()
    X_plane = load_plane_2d_in_10d()
    X_swiss, t_swiss = load_swiss_roll()

    return {
        "mnist": {
            "X": X_mnist,
            "y": y_mnist,
        },
        "gaussian_noise": X_gaussian,
        "plane_2d_in_10d": X_plane,
        "swiss_roll": {
            "X": X_swiss,
            "t": t_swiss,
        },
    }


def main() -> None:
    """
    Load all datasets and print their shapes.
    """
    X_mnist, y_mnist = load_mnist()
    X_gaussian = load_gaussian_noise()
    X_plane = load_plane_2d_in_10d()
    X_swiss, t_swiss = load_swiss_roll()

    print("MNIST X shape:", X_mnist.shape)
    print("MNIST y shape:", y_mnist.shape)
    print("Gaussian noise shape:", X_gaussian.shape)
    print("2D plane in 10D shape:", X_plane.shape)
    print("Swiss roll X shape:", X_swiss.shape)
    print("Swiss roll t shape:", t_swiss.shape)


if __name__ == "__main__":
    main()
