#visualizations.py:

from __future__ import annotations

from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from sklearn.linear_model import LinearRegression

from correlation_dimension import estimate_correlation_dimension
from knn_dimension import estimate_knn_dimension_over_k_range
from load_data import (
    load_gaussian_noise,
    load_mnist,
    load_plane_2d_in_10d,
    load_swiss_roll,
)
from pca_dimension import estimate_pca_dimensionality
from preprocessing import preprocessing_pipeline, sample_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = PROJECT_ROOT / "intrinsic_dimension_analysis"

DATASET_DISPLAY_NAMES: dict[str, str] = {
    "mnist": "MNIST",
    "gaussian_noise": "Gaussian Noise",
    "plane_2d_in_10d": "2D Plane Embedded in 10D",
    "swiss_roll": "Swiss Roll",
}

PCA_THRESHOLDS: Final[tuple[float, float, float]] = (0.90, 0.95, 0.99)
KNN_K_VALUES: Final[tuple[int, ...]] = (5, 8, 10, 12, 15, 20)
MNIST_SAMPLE_SIZE: Final[int] = 1000
RANDOM_STATE: Final[int] = 42

_BLUE = "#2166AC"
_RED = "#D6604D"
_GREEN = "#4DAC26"
_ORANGE = "#F4A582"
_GREY = "#636363"

THRESHOLD_COLORS: Final[tuple[str, str, str]] = (_RED, _ORANGE, _GREY)
TRIPLE_BAR_COLORS: Final[tuple[str, str, str]] = (_BLUE, _RED, _GREEN)


def configure_matplotlib() -> None:
    """
    Configure matplotlib for clean, publication-style figures.
    """
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.format": "png",
        "font.family": "serif",
        "font.serif": [
            "Palatino Linotype",
            "Palatino",
            "Book Antiqua",
            "Georgia",
            "DejaVu Serif",
        ],
        "mathtext.fontset": "cm",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "axes.titleweight": "bold",
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.title_fontsize": 10,
        "axes.prop_cycle": plt.cycler(color=[_BLUE, _RED, _GREEN, _ORANGE, _GREY, "#762A83"]),
        "lines.linewidth": 1.8,
        "lines.markersize": 4.5,
        "axes.grid": True,
        "grid.color": "#CCCCCC",
        "grid.alpha": 0.5,
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.linewidth": 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.minor.size": 2,
        "ytick.minor.size": 2,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "figure.constrained_layout.use": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "legend.framealpha": 0.9,
        "legend.edgecolor": "#AAAAAA",
        "legend.frameon": True,
        "legend.borderpad": 0.5,
        "legend.labelspacing": 0.4,
    })


def ensure_figures_directory() -> None:
    """
    Create the figures directory if it does not already exist.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(filename: str) -> None:
    """
    Save the current matplotlib figure to the figures directory.
    """
    filepath = FIGURES_DIR / filename
    plt.savefig(filepath, bbox_inches="tight", facecolor="white")
    plt.close()


def _style_spine(ax: plt.Axes) -> None:
    """
    Apply consistent spine thickness and tick appearance to an axes object.
    """
    for spine in ("left", "bottom"):
        ax.spines[spine].set_linewidth(0.8)
        ax.spines[spine].set_color("#333333")
    ax.tick_params(which="both", color="#333333", labelcolor="#222222")


def get_processed_array(
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


def preprocess_for_analysis(x: np.ndarray) -> np.ndarray:
    """
    Apply the standard preprocessing configuration used in the project.
    """
    preprocessing_results = preprocessing_pipeline(
        x,
        remove_constants=True,
        variance_threshold=0.0,
        apply_standardization=True,
        apply_normalization=False,
    )
    return get_processed_array(preprocessing_results)


def get_pca_results(x_processed: np.ndarray) -> dict[str, object]:
    """
    Run PCA dimensionality estimation and validate the returned structure.
    """
    results = estimate_pca_dimensionality(x_processed)

    if not isinstance(results, dict):
        raise TypeError("Expected PCA results to be a dictionary.")

    return results


def extract_pca_arrays(
    pca_results: dict[str, object],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract validated PCA arrays from the PCA results dictionary.
    """
    explained_variance_ratio = pca_results.get("explained_variance_ratio")
    cumulative_variance = pca_results.get("cumulative_explained_variance")

    if not isinstance(explained_variance_ratio, np.ndarray):
        raise TypeError("Expected explained_variance_ratio to be a NumPy array.")
    if not isinstance(cumulative_variance, np.ndarray):
        raise TypeError("Expected cumulative_explained_variance to be a NumPy array.")

    return explained_variance_ratio, cumulative_variance


def extract_threshold_components(pca_results: dict[str, object]) -> dict[float, int]:
    """
    Extract validated PCA threshold summary.
    """
    components_per_threshold = pca_results.get("components_per_threshold")

    if not isinstance(components_per_threshold, dict):
        raise TypeError("Expected components_per_threshold to be a dictionary.")

    validated: dict[float, int] = {}
    for key, value in components_per_threshold.items():
        if not isinstance(key, float):
            raise TypeError("Expected PCA threshold keys to be floats.")
        if not isinstance(value, int):
            raise TypeError("Expected PCA threshold values to be integers.")
        validated[key] = value

    return validated


def extract_correlation_dimension(results: dict[str, object]) -> float:
    """
    Extract the estimated correlation dimension.
    """
    estimated_dimension = results.get("estimated_dimension")

    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")

    return estimated_dimension


def plot_mnist_samples(
    x_mnist: np.ndarray,
    y_mnist: np.ndarray,
    n_rows: int = 2,
    n_cols: int = 5,
    random_state: int = 42,
) -> None:
    """
    Plot a grid of randomly sampled MNIST digit images.
    """
    n_images = n_rows * n_cols
    rng = np.random.default_rng(random_state)
    indices = rng.choice(len(x_mnist), size=n_images, replace=False)

    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(12, 5.5),
        gridspec_kw={"hspace": 0.40, "wspace": 0.12},
    )
    axes = np.asarray(axes).ravel()

    for i, idx in enumerate(indices):
        image = x_mnist[idx].reshape(28, 28)
        axes[i].imshow(image, cmap="gray", interpolation="nearest")
        axes[i].set_title(f"Label: {y_mnist[idx]}", fontsize=9.5, pad=5)
        axes[i].set_xticks([])
        axes[i].set_yticks([])
        for spine in axes[i].spines.values():
            spine.set_visible(False)

    fig.suptitle("Random Sample of MNIST Digit Images", fontsize=13, fontweight="bold", y=0.97)
    save_figure("mnist_samples.png")


def plot_pca_cumulative_variance(
    dataset_name: str,
    x_processed: np.ndarray,
    output_filename: str,
    x_zoom_max: int | None = None,
    show_markers: bool = False,
) -> dict[float, int]:
    """
    Plot cumulative explained variance for PCA and mark threshold crossings.
    """
    pca_results = get_pca_results(x_processed)
    _, cumulative_variance = extract_pca_arrays(pca_results)
    threshold_components = extract_threshold_components(pca_results)

    components = np.arange(1, len(cumulative_variance) + 1)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _style_spine(ax)

    ax.plot(
        components,
        cumulative_variance,
        marker="o" if show_markers else None,
        linewidth=2.0,
        markersize=4.0,
        color=_BLUE,
        zorder=3,
    )

    if dataset_name in {
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        DATASET_DISPLAY_NAMES["swiss_roll"],
    }:
        all_same_component = len({threshold_components[t] for t in PCA_THRESHOLDS}) == 1
    else:
        all_same_component = False

    if all_same_component:
        shared_component = threshold_components[PCA_THRESHOLDS[0]]

        for threshold, color in zip(PCA_THRESHOLDS, THRESHOLD_COLORS):
            ax.axhline(
                threshold,
                linestyle="--",
                linewidth=1.1,
                color=color,
                alpha=0.8,
                zorder=2,
            )

        ax.axvline(
            shared_component,
            linestyle=":",
            linewidth=1.3,
            color=_GREY,
            alpha=0.9,
            zorder=2,
        )
        ax.scatter(
            [shared_component],
            [cumulative_variance[shared_component - 1]],
            s=45,
            color=_BLUE,
            edgecolors="white",
            linewidths=0.8,
            zorder=5,
        )
        ax.annotate(
            f"All thresholds (90/95/99%) reached at PC {shared_component}",
            xy=(shared_component, cumulative_variance[shared_component - 1]),
            xytext=(shared_component + 0.15, 0.63),
            fontsize=8.7,
            color=_GREY,
            arrowprops={"arrowstyle": "-", "lw": 0.8, "alpha": 0.65, "color": _GREY},
        )
    else:
        for threshold, color in zip(PCA_THRESHOLDS, THRESHOLD_COLORS):
            component_count = threshold_components[threshold]

            ax.axhline(
                threshold,
                linestyle="--",
                linewidth=1.1,
                color=color,
                alpha=0.8,
                zorder=2,
            )
            ax.axvline(
                component_count,
                linestyle=":",
                linewidth=1.1,
                color=color,
                alpha=0.8,
                zorder=2,
            )
            ax.scatter(
                [component_count],
                [threshold],
                s=36,
                color=color,
                zorder=5,
                edgecolors="white",
                linewidths=0.8,
            )

            annotation_text = f"{int(threshold * 100)}% -> PC {component_count}"
            x_text = component_count + max(1, int(0.015 * len(cumulative_variance)))
            y_text = min(threshold + 0.02, 1.02)

            if dataset_name == DATASET_DISPLAY_NAMES["mnist"] and threshold == 0.99:
                x_text = component_count - 80
                y_text = threshold - 0.035
            elif dataset_name == DATASET_DISPLAY_NAMES["gaussian_noise"]:
                if threshold == 0.90:
                    x_text = component_count - 3.0
                    y_text = threshold + 0.010
                elif threshold == 0.95:
                    x_text = component_count - 3.0
                    y_text = threshold - 0.015
                elif threshold == 0.99:
                    x_text = component_count - 3.0
                    y_text = threshold - 0.040

            ax.annotate(
                annotation_text,
                xy=(component_count, threshold),
                xytext=(x_text, y_text),
                textcoords="data",
                fontsize=8.8,
                color=color,
                ha="left",
                va="bottom",
                arrowprops={
                    "arrowstyle": "-",
                    "lw": 0.8,
                    "color": color,
                    "alpha": 0.7,
                },
            )

    ax.set_xlabel("Number of Principal Components", labelpad=8)
    ax.set_ylabel("Cumulative Explained Variance", labelpad=8)
    ax.set_title(f"PCA Cumulative Explained Variance - {dataset_name}", fontsize=12, fontweight="bold", pad=10)
    ax.set_ylim(0.0, 1.05)

    if x_zoom_max is None:
        ax.set_xlim(1, len(cumulative_variance))
    else:
        ax.set_xlim(1, x_zoom_max)

    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
    fig.tight_layout()
    save_figure(output_filename)

    return threshold_components


def plot_pca_scree(
    dataset_name: str,
    x_processed: np.ndarray,
    output_filename: str,
    max_components: int | None = None,
) -> None:
    """
    Plot the scree plot of explained variance ratios.
    """
    pca_results = get_pca_results(x_processed)
    explained_variance_ratio, _ = extract_pca_arrays(pca_results)

    if max_components is not None:
        explained_variance_ratio = explained_variance_ratio[:max_components]

    components = np.arange(1, len(explained_variance_ratio) + 1)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _style_spine(ax)

    ax.plot(
        components,
        explained_variance_ratio,
        marker="o",
        linewidth=1.8,
        markersize=4.0,
        color=_BLUE,
        markerfacecolor="white",
        markeredgecolor=_BLUE,
        markeredgewidth=1.1,
        zorder=3,
    )

    should_annotate = dataset_name in {
        DATASET_DISPLAY_NAMES["mnist"],
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
    }

    if should_annotate and len(explained_variance_ratio) >= 2:
        annotation_count = 1 if dataset_name == DATASET_DISPLAY_NAMES["mnist"] else 2

        for i in range(annotation_count):
            x_offset = 0.6
            y_offset = 0.008 if i == 0 else 0.005
            ax.annotate(
                f"PC {i + 1}",
                xy=(components[i], explained_variance_ratio[i]),
                xytext=(components[i] + x_offset, explained_variance_ratio[i] + y_offset),
                fontsize=8.5,
                color=_GREY,
                arrowprops={"arrowstyle": "-", "lw": 0.8, "alpha": 0.6},
            )

    ax.set_xlabel("Principal Component", labelpad=8)
    ax.set_ylabel("Explained Variance Ratio", labelpad=8)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
    ax.set_title(f"Scree Plot - {dataset_name}", fontsize=12, fontweight="bold", pad=10)
    ax.set_xlim(1, len(explained_variance_ratio))
    fig.tight_layout()
    save_figure(output_filename)


def plot_correlation_loglog(
    dataset_name: str,
    x_processed: np.ndarray,
    output_filename: str,
    n_radii: int = 30,
    min_percentile: float = 1.0,
    max_percentile: float = 50.0,
    scaling_region_start: int = 5,
    scaling_region_end: int | None = 20,
) -> float:
    """
    Plot the log-log correlation integral curve and highlight the scaling region.
    """
    results = estimate_correlation_dimension(
        x=x_processed,
        n_radii=n_radii,
        min_percentile=min_percentile,
        max_percentile=max_percentile,
        scaling_region_start=scaling_region_start,
        scaling_region_end=scaling_region_end,
    )

    log_radii = results["log_radii"]
    log_correlation_integral = results["log_correlation_integral"]
    log_radii_region = results["log_radii_region"]
    log_correlation_region = results["log_correlation_region"]
    regression_model = results["regression_model"]
    estimated_dimension = results["estimated_dimension"]

    if not isinstance(log_radii, np.ndarray):
        raise TypeError("Expected log_radii to be a NumPy array.")
    if not isinstance(log_correlation_integral, np.ndarray):
        raise TypeError("Expected log_correlation_integral to be a NumPy array.")
    if not isinstance(log_radii_region, np.ndarray):
        raise TypeError("Expected log_radii_region to be a NumPy array.")
    if not isinstance(log_correlation_region, np.ndarray):
        raise TypeError("Expected log_correlation_region to be a NumPy array.")
    if not isinstance(regression_model, LinearRegression):
        raise TypeError("Expected regression_model to be a LinearRegression instance.")
    if not isinstance(estimated_dimension, float):
        raise TypeError("Expected estimated_dimension to be a float.")

    fitted_line = regression_model.predict(log_radii_region.reshape(-1, 1))

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _style_spine(ax)

    ax.plot(
        log_radii,
        log_correlation_integral,
        marker="o",
        linewidth=1.5,
        markersize=4.0,
        color="#555555",
        alpha=0.85,
        label="Log-log curve",
        zorder=2,
    )
    ax.plot(
        log_radii_region,
        log_correlation_region,
        marker="o",
        linewidth=2.0,
        markersize=4.8,
        color=_BLUE,
        label="Scaling region",
        zorder=3,
    )
    ax.plot(
        log_radii_region,
        fitted_line,
        linestyle="--",
        linewidth=2.0,
        color=_RED,
        label=rf"Linear fit  $\hat{{d}}_C = {estimated_dimension:.2f}$",
        zorder=4,
    )

    ax.set_xlabel(r"$\log(r)$", labelpad=8)
    ax.set_ylabel(r"$\log\,C(r)$", labelpad=8)
    ax.set_title(f"Correlation Dimension Log-Log Plot - {dataset_name}", fontsize=12, fontweight="bold", pad=10)
    ax.legend(loc="upper left", frameon=True, handlelength=1.6, fontsize=8.8)
    fig.tight_layout()
    save_figure(output_filename)

    return estimated_dimension


def plot_knn_sensitivity(
    dataset_name: str,
    x_processed: np.ndarray,
    output_filename: str,
    k_values: tuple[int, ...] = KNN_K_VALUES,
) -> tuple[float, float]:
    """
    Plot kNN intrinsic-dimension estimates as a function of k.

    Returns
    -------
    tuple[float, float]
        Headline estimate at k=10 and mean estimate across all tested k values.
    """
    results = estimate_knn_dimension_over_k_range(
        x=x_processed,
        k_values=list(k_values),
        metric="euclidean",
        aggregate="mean",
        n_jobs=None,
    )

    k_array = results["k_values"]
    estimates = results["dimension_estimates"]
    mean_estimate = results["mean_estimate"]

    if not isinstance(k_array, np.ndarray):
        raise TypeError("Expected k_values to be a NumPy array.")
    if not isinstance(estimates, np.ndarray):
        raise TypeError("Expected dimension_estimates to be a NumPy array.")
    if not isinstance(mean_estimate, float):
        raise TypeError("Expected mean_estimate to be a float.")

    k10_mask = k_array == 10
    if not np.any(k10_mask):
        raise ValueError("k_values must include 10 for the headline estimate.")

    k10_estimate = float(estimates[k10_mask][0])

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    _style_spine(ax)

    ax.plot(
        k_array,
        estimates,
        marker="o",
        linewidth=1.8,
        markersize=4.5,
        color=_GREEN,
        markerfacecolor="white",
        markeredgecolor=_GREEN,
        markeredgewidth=1.2,
        zorder=3,
    )
    ax.axhline(
        mean_estimate,
        linestyle="--",
        linewidth=1.1,
        color=_GREY,
        alpha=0.85,
        label=f"Mean across k = {mean_estimate:.2f}",
        zorder=2,
    )
    ax.scatter(
        [10],
        [k10_estimate],
        s=50,
        color=_RED,
        edgecolors="white",
        linewidths=0.8,
        zorder=4,
        label=f"Headline estimate at k = 10 ({k10_estimate:.2f})",
    )

    ax.set_xlabel("Number of Nearest Neighbors (k)", labelpad=8)
    ax.set_ylabel("Estimated Intrinsic Dimension", labelpad=8)
    ax.set_title(f"kNN Sensitivity Analysis - {dataset_name}", fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks(k_array.astype(int))
    ax.legend(loc="best", frameon=True, fontsize=8.6)
    fig.tight_layout()
    save_figure(output_filename)

    return k10_estimate, mean_estimate


def add_bar_labels(
    ax: plt.Axes,
    x_positions: np.ndarray,
    values: list[float],
    fmt: str,
    additive_offset: float | None = None,
    multiplicative_offset: float | None = None,
    fontsize: float = 8.8,
) -> None:
    """
    Add numeric labels above bar positions.
    """
    for x_pos, value in zip(x_positions, values):
        if multiplicative_offset is not None:
            y_pos = value * multiplicative_offset
        elif additive_offset is not None:
            y_pos = value + additive_offset
        else:
            y_pos = value

        ax.text(
            x_pos,
            y_pos,
            fmt.format(value),
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color="#222222",
        )


def plot_grouped_dimension_comparison(
    dataset_names: list[str],
    pca_summary: dict[str, int],
    correlation_summary: dict[str, float],
    knn_summary: dict[str, float],
    output_filename: str,
    title: str,
    use_log_scale: bool,
) -> None:
    """
    Plot a grouped bar chart comparing PCA, correlation dimension, and kNN estimates.
    """
    pca_values = [pca_summary[name] for name in dataset_names]
    correlation_values = [correlation_summary[name] for name in dataset_names]
    knn_values = [knn_summary[name] for name in dataset_names]

    x_positions = np.arange(len(dataset_names))
    width = 0.24

    fig, ax = plt.subplots(figsize=(10.6, 5.7))
    _style_spine(ax)

    ax.bar(
        x_positions - width,
        pca_values,
        width,
        color=TRIPLE_BAR_COLORS[0],
        alpha=0.88,
        edgecolor="white",
        linewidth=0.6,
        label="PCA (90% variance threshold)",
        zorder=3,
    )
    ax.bar(
        x_positions,
        correlation_values,
        width,
        color=TRIPLE_BAR_COLORS[1],
        alpha=0.88,
        edgecolor="white",
        linewidth=0.6,
        label="Correlation dimension",
        zorder=3,
    )
    ax.bar(
        x_positions + width,
        knn_values,
        width,
        color=TRIPLE_BAR_COLORS[2],
        alpha=0.88,
        edgecolor="white",
        linewidth=0.6,
        label="kNN dimension (k=10)",
        zorder=3,
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(dataset_names, rotation=12, ha="right")
    ax.set_ylabel("Estimated Dimension (log scale)" if use_log_scale else "Estimated Dimension", labelpad=8)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.legend(loc="upper right", frameon=True, handlelength=1.5, fontsize=8.5)
    ax.grid(True, axis="y", alpha=0.4, linestyle="--", linewidth=0.6)
    ax.set_axisbelow(True)

    if use_log_scale:
        ax.set_yscale("log")
        add_bar_labels(
            ax=ax,
            x_positions=x_positions - width,
            values=[float(v) for v in pca_values],
            fmt="{:.0f}",
            multiplicative_offset=1.04,
        )
        add_bar_labels(
            ax=ax,
            x_positions=x_positions,
            values=correlation_values,
            fmt="{:.2f}",
            multiplicative_offset=1.04,
        )
        add_bar_labels(
            ax=ax,
            x_positions=x_positions + width,
            values=knn_values,
            fmt="{:.2f}",
            multiplicative_offset=1.04,
        )
    else:
        add_bar_labels(
            ax=ax,
            x_positions=x_positions - width,
            values=[float(v) for v in pca_values],
            fmt="{:.0f}",
            additive_offset=0.18,
        )
        add_bar_labels(
            ax=ax,
            x_positions=x_positions,
            values=correlation_values,
            fmt="{:.2f}",
            additive_offset=0.18,
        )
        add_bar_labels(
            ax=ax,
            x_positions=x_positions + width,
            values=knn_values,
            fmt="{:.2f}",
            additive_offset=0.18,
        )

    fig.tight_layout()
    save_figure(output_filename)


def plot_dimension_comparison_all_methods(
    pca_summary: dict[str, int],
    correlation_summary: dict[str, float],
    knn_summary: dict[str, float],
) -> None:
    """
    Plot the all-datasets comparison using log scale.
    """
    dataset_names = list(pca_summary.keys())
    plot_grouped_dimension_comparison(
        dataset_names=dataset_names,
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
        output_filename="dimension_comparison_all_methods.png",
        title="Comparison of PCA, Correlation Dimension, and kNN Estimates",
        use_log_scale=True,
    )


def plot_dimension_comparison_synthetic_all_methods(
    pca_summary: dict[str, int],
    correlation_summary: dict[str, float],
    knn_summary: dict[str, float],
) -> None:
    """
    Plot the synthetic-only comparison using linear scale.
    """
    synthetic_names = [
        DATASET_DISPLAY_NAMES["gaussian_noise"],
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        DATASET_DISPLAY_NAMES["swiss_roll"],
    ]
    plot_grouped_dimension_comparison(
        dataset_names=synthetic_names,
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
        output_filename="dimension_comparison_synthetic_all_methods.png",
        title="Comparison of PCA, Correlation Dimension, and kNN - Synthetic Datasets",
        use_log_scale=False,
    )


def main() -> None:
    """
    Generate all required visualizations and save them in the figures directory.
    """
    configure_matplotlib()
    ensure_figures_directory()

    x_mnist, y_mnist = load_mnist()
    x_gaussian = load_gaussian_noise()
    x_plane = load_plane_2d_in_10d()
    x_swiss, _ = load_swiss_roll()

    x_mnist_processed = preprocess_for_analysis(x_mnist)
    x_gaussian_processed = preprocess_for_analysis(x_gaussian)
    x_plane_processed = preprocess_for_analysis(x_plane)
    x_swiss_processed = preprocess_for_analysis(x_swiss)

    x_mnist_sampled, _ = sample_dataset(
        x=x_mnist,
        y=y_mnist,
        n_samples=MNIST_SAMPLE_SIZE,
        random_state=RANDOM_STATE,
    )
    x_mnist_sampled_processed = preprocess_for_analysis(x_mnist_sampled)

    plot_mnist_samples(x_mnist, y_mnist)

    mnist_thresholds = plot_pca_cumulative_variance(
        dataset_name=DATASET_DISPLAY_NAMES["mnist"],
        x_processed=x_mnist_processed,
        output_filename="pca_cumulative_mnist.png",
        x_zoom_max=None,
        show_markers=False,
    )
    gaussian_thresholds = plot_pca_cumulative_variance(
        dataset_name=DATASET_DISPLAY_NAMES["gaussian_noise"],
        x_processed=x_gaussian_processed,
        output_filename="pca_cumulative_gaussian_noise.png",
        x_zoom_max=None,
        show_markers=False,
    )
    plane_thresholds = plot_pca_cumulative_variance(
        dataset_name=DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        x_processed=x_plane_processed,
        output_filename="pca_cumulative_plane_2d_in_10d.png",
        x_zoom_max=4,
        show_markers=True,
    )
    swiss_thresholds = plot_pca_cumulative_variance(
        dataset_name=DATASET_DISPLAY_NAMES["swiss_roll"],
        x_processed=x_swiss_processed,
        output_filename="pca_cumulative_swiss_roll.png",
        x_zoom_max=3,
        show_markers=True,
    )

    plot_pca_scree(
        dataset_name=DATASET_DISPLAY_NAMES["mnist"],
        x_processed=x_mnist_processed,
        output_filename="scree_mnist.png",
        max_components=100,
    )
    plot_pca_scree(
        dataset_name=DATASET_DISPLAY_NAMES["gaussian_noise"],
        x_processed=x_gaussian_processed,
        output_filename="scree_gaussian_noise.png",
    )
    plot_pca_scree(
        dataset_name=DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        x_processed=x_plane_processed,
        output_filename="scree_plane_2d_in_10d.png",
    )
    plot_pca_scree(
        dataset_name=DATASET_DISPLAY_NAMES["swiss_roll"],
        x_processed=x_swiss_processed,
        output_filename="scree_swiss_roll.png",
    )

    mnist_corr_dim = plot_correlation_loglog(
        dataset_name=DATASET_DISPLAY_NAMES["mnist"],
        x_processed=x_mnist_sampled_processed,
        output_filename="correlation_loglog_mnist.png",
    )
    gaussian_corr_dim = plot_correlation_loglog(
        dataset_name=DATASET_DISPLAY_NAMES["gaussian_noise"],
        x_processed=x_gaussian_processed,
        output_filename="correlation_loglog_gaussian_noise.png",
    )
    plane_corr_dim = plot_correlation_loglog(
        dataset_name=DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        x_processed=x_plane_processed,
        output_filename="correlation_loglog_plane_2d_in_10d.png",
    )
    swiss_corr_dim = plot_correlation_loglog(
        dataset_name=DATASET_DISPLAY_NAMES["swiss_roll"],
        x_processed=x_swiss_processed,
        output_filename="correlation_loglog_swiss_roll.png",
    )

    mnist_knn_k10, mnist_knn_mean = plot_knn_sensitivity(
        dataset_name=DATASET_DISPLAY_NAMES["mnist"],
        x_processed=x_mnist_sampled_processed,
        output_filename="knn_sensitivity_mnist.png",
    )
    gaussian_knn_k10, gaussian_knn_mean = plot_knn_sensitivity(
        dataset_name=DATASET_DISPLAY_NAMES["gaussian_noise"],
        x_processed=x_gaussian_processed,
        output_filename="knn_sensitivity_gaussian_noise.png",
    )
    plane_knn_k10, plane_knn_mean = plot_knn_sensitivity(
        dataset_name=DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
        x_processed=x_plane_processed,
        output_filename="knn_sensitivity_plane_2d_in_10d.png",
    )
    swiss_knn_k10, swiss_knn_mean = plot_knn_sensitivity(
        dataset_name=DATASET_DISPLAY_NAMES["swiss_roll"],
        x_processed=x_swiss_processed,
        output_filename="knn_sensitivity_swiss_roll.png",
    )

    pca_summary = {
        DATASET_DISPLAY_NAMES["mnist"]: mnist_thresholds[0.90],
        DATASET_DISPLAY_NAMES["gaussian_noise"]: gaussian_thresholds[0.90],
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"]: plane_thresholds[0.90],
        DATASET_DISPLAY_NAMES["swiss_roll"]: swiss_thresholds[0.90],
    }

    correlation_summary = {
        DATASET_DISPLAY_NAMES["mnist"]: mnist_corr_dim,
        DATASET_DISPLAY_NAMES["gaussian_noise"]: gaussian_corr_dim,
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"]: plane_corr_dim,
        DATASET_DISPLAY_NAMES["swiss_roll"]: swiss_corr_dim,
    }

    knn_summary = {
        DATASET_DISPLAY_NAMES["mnist"]: mnist_knn_k10,
        DATASET_DISPLAY_NAMES["gaussian_noise"]: gaussian_knn_k10,
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"]: plane_knn_k10,
        DATASET_DISPLAY_NAMES["swiss_roll"]: swiss_knn_k10,
    }

    knn_mean_summary = {
        DATASET_DISPLAY_NAMES["mnist"]: mnist_knn_mean,
        DATASET_DISPLAY_NAMES["gaussian_noise"]: gaussian_knn_mean,
        DATASET_DISPLAY_NAMES["plane_2d_in_10d"]: plane_knn_mean,
        DATASET_DISPLAY_NAMES["swiss_roll"]: swiss_knn_mean,
    }

    plot_grouped_dimension_comparison(
        dataset_names=list(pca_summary.keys()),
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
        output_filename="dimension_comparison.png",
        title="Comparison of PCA, Correlation Dimension, and kNN Estimates",
        use_log_scale=True,
    )

    plot_grouped_dimension_comparison(
        dataset_names=[
            DATASET_DISPLAY_NAMES["gaussian_noise"],
            DATASET_DISPLAY_NAMES["plane_2d_in_10d"],
            DATASET_DISPLAY_NAMES["swiss_roll"],
        ],
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
        output_filename="dimension_comparison_synthetic_only.png",
        title="Comparison of PCA, Correlation Dimension, and kNN - Synthetic Datasets",
        use_log_scale=False,
    )

    plot_dimension_comparison_all_methods(
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
    )
    plot_dimension_comparison_synthetic_all_methods(
        pca_summary=pca_summary,
        correlation_summary=correlation_summary,
        knn_summary=knn_summary,
    )

    print("All figures were generated successfully.")
    print("Figures saved in:", FIGURES_DIR)
    print()
    print("Headline kNN estimates (k=10):")
    for dataset_name, estimate in knn_summary.items():
        print(f" - {dataset_name}: {estimate:.4f}")
    print()
    print("Mean kNN estimates across tested k values:")
    for dataset_name, estimate in knn_mean_summary.items():
        print(f" - {dataset_name}: {estimate:.4f}")


if __name__ == "__main__":
    main()
