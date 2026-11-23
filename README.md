# Image Comparison Forensic Report

A simple, focused Python tool that compares two images and produces a **pure numerical forensic report**.

The goal is to separate raw, reproducible data from interpretation. The script outputs only objective metrics. Any analysis or opinion is left to the reader (or to an AI of their choice).

## Features

- File size, format, mode and dimensions
- Pixel-level difference statistics (max, mean, median, std)
- MSE, PSNR and approximate SSIM
- Per-channel breakdown (R, G, B)
- Clean, plain-text report ready to paste into any AI or document

## Requirements

```bash
pip install Pillow numpy scipy
```

## Quick Start

```bash
python image_forensic_report.py image_a.jpg image_b.png
```

The report is printed to the console and also saved as `forensic_report.txt`.

## Example

See the `examples/` folder for a real JPEG → PNG conversion pair, the generated report, and a sample analysis.

## Philosophy

> Data first. Interpretation second.

The report contains only numbers. This makes the tool useful as a neutral reference when discussing image quality, format conversion side-effects, or decoder differences.

## License

MIT
