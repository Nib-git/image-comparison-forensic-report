# User Manual

## Installation

```bash
pip install Pillow numpy scipy
```

## Usage

```bash
python image_forensic_report.py <image1> <image2>
```

### Example

```bash
python image_forensic_report.py JPEG.jpg PNG.png
```

## Output

The script prints a formatted report to the terminal and writes the same content to `forensic_report.txt` in the current directory.

## Interpreting the Report

| Metric | Meaning |
|--------|---------|
| Identical pixels | YES only if every pixel value matches exactly |
| Maximum difference | Highest absolute difference found in any channel (0–255) |
| Mean absolute difference | Average absolute difference across all pixels and channels |
| PSNR | Peak Signal-to-Noise Ratio in dB. Higher is better. ∞ means identical. |
| SSIM | Structural Similarity Index (0–1). Closer to 1.0 is better. |
| Percent different | Percentage of pixels that are not exactly equal |

### Typical Ranges

- **PSNR > 40 dB**: Usually considered visually excellent
- **PSNR 30–40 dB**: Common for medium-to-high quality JPEG material
- **SSIM > 0.95**: High structural similarity

## Notes

- The comparison is performed on RGB channels only. An alpha channel (if present) is ignored.
- Small differences between a JPEG and a PNG derived from it are normal and usually come from decoder variations (chroma upsampling, rounding, color conversion precision), not from the PNG format itself.
- PNG is lossless. Any difference observed is not introduced by the PNG encoding step.

## Troubleshooting

- **“Images have different dimensions”**: The two images must have the same width and height.
- **Missing libraries**: Install the requirements listed above.
