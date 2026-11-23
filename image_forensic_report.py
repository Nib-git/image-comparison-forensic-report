#!/usr/bin/env python3
"""
Image Comparison Forensic Report Generator
==========================================
Compares two images (typically original JPG vs converted PNG)
and generates a pure numerical report for later analysis.

Usage:
    python image_forensic_report.py image1.jpg image2.png

Output: plain-text report ready to paste into any AI.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
    import numpy as np
    from scipy.ndimage import uniform_filter
except ImportError:
    print("ERROR: Pillow, NumPy and SciPy are required.")
    print("Install with: pip install Pillow numpy scipy")
    sys.exit(1)


def get_file_info(path: Path) -> dict:
    size_bytes = path.stat().st_size
    return {
        "path": str(path),
        "name": path.name,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 2),
        "size_mb": round(size_bytes / (1024 * 1024), 3),
    }


def load_image(path: Path) -> tuple:
    im = Image.open(path)
    arr = np.array(im.convert("RGB"))
    return im, arr


def compute_metrics(arr1: np.ndarray, arr2: np.ndarray) -> dict:
    if arr1.shape != arr2.shape:
        return {"error": "Images have different dimensions", "shape1": arr1.shape, "shape2": arr2.shape}

    diff = np.abs(arr1.astype(np.int32) - arr2.astype(np.int32))
    mse = np.mean((arr1.astype(np.float64) - arr2.astype(np.float64)) ** 2)

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10((255 ** 2) / mse)

    # SSIM simplificado (versión básica multicanal)
    ssim_val = compute_ssim_simple(arr1, arr2)

    total_pixels = diff.size
    different_pixels = np.count_nonzero(diff)

    return {
        "identical": bool(np.array_equal(arr1, arr2)),
        "max_diff": int(diff.max()),
        "mean_abs_diff": round(float(diff.mean()), 6),
        "median_abs_diff": float(np.median(diff)),
        "std_abs_diff": round(float(diff.std()), 6),
        "mse": round(float(mse), 6),
        "psnr_db": round(float(psnr), 2) if psnr != float("inf") else "inf",
        "ssim": round(float(ssim_val), 6),
        "different_pixels": int(different_pixels),
        "total_pixels": int(total_pixels),
        "percent_different": round(100 * different_pixels / total_pixels, 4),
        "per_channel": {
            "R": channel_stats(diff[:, :, 0]),
            "G": channel_stats(diff[:, :, 1]),
            "B": channel_stats(diff[:, :, 2]),
        },
    }


def channel_stats(ch_diff: np.ndarray) -> dict:
    return {
        "max": int(ch_diff.max()),
        "mean": round(float(ch_diff.mean()), 4),
        "median": float(np.median(ch_diff)),
        "percent_diff": round(100 * np.count_nonzero(ch_diff) / ch_diff.size, 2),
    }


def compute_ssim_simple(img1: np.ndarray, img2: np.ndarray, win_size: int = 11) -> float:
    """SSIM básico multicanal usando scipy (rápido)."""
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    ssim_channels = []
    for c in range(3):
        x = img1[:, :, c].astype(np.float64)
        y = img2[:, :, c].astype(np.float64)

        mu_x = uniform_filter(x, size=win_size)
        mu_y = uniform_filter(y, size=win_size)
        mu_x_sq = mu_x ** 2
        mu_y_sq = mu_y ** 2
        mu_xy = mu_x * mu_y

        sigma_x_sq = uniform_filter(x ** 2, size=win_size) - mu_x_sq
        sigma_y_sq = uniform_filter(y ** 2, size=win_size) - mu_y_sq
        sigma_xy = uniform_filter(x * y, size=win_size) - mu_xy

        numerator = (2 * mu_xy + c1) * (2 * sigma_xy + c2)
        denominator = (mu_x_sq + mu_y_sq + c1) * (sigma_x_sq + sigma_y_sq + c2)
        ssim_map = numerator / denominator
        ssim_channels.append(np.mean(ssim_map))

    return float(np.mean(ssim_channels))


def uniform_filter_fallback(img, size):
    # Ya no se usa; scipy está disponible
    pass


def generate_report(path1: Path, path2: Path) -> str:
    info1 = get_file_info(path1)
    info2 = get_file_info(path2)

    im1, arr1 = load_image(path1)
    im2, arr2 = load_image(path2)

    metrics = compute_metrics(arr1, arr2)

    lines = []
    lines.append("=" * 72)
    lines.append("IMAGE COMPARISON FORENSIC REPORT")
    lines.append("=" * 72)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("FILES")
    lines.append("-" * 72)
    lines.append(f"Image A : {info1['name']}")
    lines.append(f"  Path   : {info1['path']}")
    lines.append(f"  Size   : {info1['size_kb']} KB ({info1['size_bytes']} bytes)")
    lines.append(f"  Format : {im1.format}")
    lines.append(f"  Mode   : {im1.mode}")
    lines.append(f"  Dim.   : {im1.size[0]} × {im1.size[1]} px")
    lines.append("")
    lines.append(f"Image B : {info2['name']}")
    lines.append(f"  Path   : {info2['path']}")
    lines.append(f"  Size   : {info2['size_kb']} KB ({info2['size_bytes']} bytes)")
    lines.append(f"  Format : {im2.format}")
    lines.append(f"  Mode   : {im2.mode}")
    lines.append(f"  Dim.   : {im2.size[0]} × {im2.size[1]} px")
    lines.append("")

    if "error" in metrics:
        lines.append("ERROR")
        lines.append("-" * 72)
        lines.append(str(metrics))
        return "\n".join(lines)

    lines.append("GLOBAL METRICS")
    lines.append("-" * 72)
    lines.append(f"Identical pixels      : {'YES' if metrics['identical'] else 'NO'}")
    lines.append(f"Maximum difference    : {metrics['max_diff']}")
    lines.append(f"Mean absolute diff.   : {metrics['mean_abs_diff']}")
    lines.append(f"Median absolute diff. : {metrics['median_abs_diff']}")
    lines.append(f"Std. deviation        : {metrics['std_abs_diff']}")
    lines.append(f"MSE                   : {metrics['mse']}")
    lines.append(f"PSNR                  : {metrics['psnr_db']} dB")
    lines.append(f"SSIM (approx.)        : {metrics['ssim']}")
    lines.append(f"Different pixels      : {metrics['different_pixels']:,} / {metrics['total_pixels']:,}")
    lines.append(f"Percent different     : {metrics['percent_different']} %")
    lines.append("")

    lines.append("PER-CHANNEL METRICS")
    lines.append("-" * 72)
    for ch in ["R", "G", "B"]:
        s = metrics["per_channel"][ch]
        lines.append(f"Channel {ch}:")
        lines.append(f"  Max difference   : {s['max']}")
        lines.append(f"  Mean             : {s['mean']}")
        lines.append(f"  Median           : {s['median']}")
        lines.append(f"  % pixels ≠       : {s['percent_diff']} %")
        lines.append("")

    lines.append("NOTES")
    lines.append("-" * 72)
    lines.append("- PSNR = ∞ and SSIM = 1.0 indicate pixel-perfect identity.")
    lines.append("- PSNR > 40 dB is generally considered visually excellent.")
    lines.append("- PSNR 30–40 dB is typical of medium-to-high quality JPEG.")
    lines.append("- SSIM close to 1.0 indicates high structural similarity.")
    lines.append("- This report contains only pure numerical data.")
    lines.append("=" * 72)

    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: python image_forensic_report.py <image1> <image2>")
        print("Example: python image_forensic_report.py original.jpg converted.png")
        sys.exit(1)

    path1 = Path(sys.argv[1])
    path2 = Path(sys.argv[2])

    if not path1.exists():
        print(f"ERROR: File not found: {path1}")
        sys.exit(1)
    if not path2.exists():
        print(f"ERROR: File not found: {path2}")
        sys.exit(1)

    report = generate_report(path1, path2)
    print(report)

    # Save report to file
    out_path = Path("forensic_report.txt")
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
