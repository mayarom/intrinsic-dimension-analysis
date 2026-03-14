from pathlib import Path

import numpy as np
from sklearn.datasets import make_swiss_roll


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_DATA_DIR = PROJECT_ROOT / "data" / "synthetic"


def ensure_directories() -> None:
    """
    Create the synthetic data directories if they do not already exist.
    """
    (SYNTHETIC_DATA_DIR / "gaussian_noise").mkdir(parents=True, exist_ok=True)
    (SYNTHETIC_DATA_DIR / "plane_2d_in_10d").mkdir(parents=True, exist_ok=True)
    (SYNTHETIC_DATA_DIR / "swiss_roll").mkdir(parents=True, exist_ok=True)


def generate_gaussian_noise(
    n_samples: int = 2000,
    n_features: int = 20,
    random_state: int = 42
) -> np.ndarray:
    """
    Generate high-dimensional Gaussian noise.

    Parameters
    ----------
    n_samples : int
        Number of samples.
    n_features : int
        Number of ambient dimensions.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Array of shape (n_samples, n_features).
    """
    rng = np.random.default_rng(random_state)
    X = rng.normal(loc=0.0, scale=1.0, size=(n_samples, n_features))
    return X


def generate_2d_plane_in_10d(
    n_samples: int = 2000,
    noise_std: float = 0.01,
    random_state: int = 42
) -> np.ndarray:
    """
    Generate points that lie approximately on a 2D plane embedded in 10D.

    Parameters
    ----------
    n_samples : int
        Number of samples.
    noise_std : float
        Standard deviation of Gaussian noise added after embedding.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Array of shape (n_samples, 10).
    """
    rng = np.random.default_rng(random_state)

    # Generate intrinsic 2D coordinates
    z = rng.uniform(low=-5.0, high=5.0, size=(n_samples, 2))

    # Create a random linear embedding from 2D to 10D
    embedding_matrix = rng.normal(loc=0.0, scale=1.0, size=(2, 10))

    # Embed the 2D coordinates into the 10D ambient space
    X = z @ embedding_matrix

    # Add a small amount of noise to make the dataset more realistic
    if noise_std > 0:
        X += rng.normal(loc=0.0, scale=noise_std, size=X.shape)

    return X


def generate_swiss_roll_dataset(
    n_samples: int = 2000,
    noise: float = 0.05,
    random_state: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate the Swiss roll dataset.

    Parameters
    ----------
    n_samples : int
        Number of samples.
    noise : float
        Standard deviation of Gaussian noise added to the manifold.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        X : array of shape (n_samples, 3)
            Swiss roll samples in 3D ambient space.
        t : array of shape (n_samples,)
            The univariate position parameter along the roll.
    """
    X, t = make_swiss_roll(
        n_samples=n_samples,
        noise=noise,
        random_state=random_state
    )
    return X, t


def save_array(array: np.ndarray, filepath: Path) -> None:
    """
    Save a NumPy array to disk as an .npy file.

    Parameters
    ----------
    array : np.ndarray
        Array to save.
    filepath : Path
        Destination path.
    """
    np.save(filepath, array)


def main() -> None:
    """
    Generate all synthetic datasets and save them in an organised directory structure.
    """
    ensure_directories()

    gaussian_noise = generate_gaussian_noise(
        n_samples=2000,
        n_features=20,
        random_state=42
    )
    save_array(
        gaussian_noise,
        SYNTHETIC_DATA_DIR / "gaussian_noise" / "gaussian_noise.npy"
    )

    plane_2d_in_10d = generate_2d_plane_in_10d(
        n_samples=2000,
        noise_std=0.01,
        random_state=42
    )
    save_array(
        plane_2d_in_10d,
        SYNTHETIC_DATA_DIR / "plane_2d_in_10d" / "plane_2d_in_10d.npy"
    )

    swiss_roll_X, swiss_roll_t = generate_swiss_roll_dataset(
        n_samples=2000,
        noise=0.05,
        random_state=42
    )
    save_array(
        swiss_roll_X,
        SYNTHETIC_DATA_DIR / "swiss_roll" / "swiss_roll_X.npy"
    )
    save_array(
        swiss_roll_t,
        SYNTHETIC_DATA_DIR / "swiss_roll" / "swiss_roll_t.npy"
    )

    print("Synthetic datasets were generated successfully.")
    print(
        "Saved Gaussian noise to:",
        SYNTHETIC_DATA_DIR / "gaussian_noise" / "gaussian_noise.npy"
    )
    print(
        "Saved 2D plane in 10D to:",
        SYNTHETIC_DATA_DIR / "plane_2d_in_10d" / "plane_2d_in_10d.npy"
    )
    print(
        "Saved Swiss roll samples to:",
        SYNTHETIC_DATA_DIR / "swiss_roll" / "swiss_roll_X.npy"
    )
    print(
        "Saved Swiss roll parameter to:",
        SYNTHETIC_DATA_DIR / "swiss_roll" / "swiss_roll_t.npy"
    )


if __name__ == "__main__":
    main()
