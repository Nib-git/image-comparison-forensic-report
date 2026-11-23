# Sample Analysis

**Source report:** `examples/forensic_report.txt`  
**Images:** `JPEG.jpg` (JPEG, RGB) vs `PNG.png` (PNG, RGBA)

## File-Level Observations

- True format conversion confirmed (JPEG → PNG).
- Dimensions identical (768 × 1344).
- File size increased from 193 KB to 1.2 MB (≈ 6.2×), which is expected for photographic content stored losslessly.
- PNG contains an alpha channel (RGBA); the comparison was performed on the RGB channels.

## Pixel Metrics

| Metric | Value |
|--------|-------|
| Identical pixels | NO |
| Maximum difference | 106 |
| Mean absolute difference | 3.62 |
| Median absolute difference | 3.0 |
| PSNR | 34.13 dB |
| SSIM | 0.952 |
| Percent different | 90.27 % |

## Interpretation

The measured differences are characteristic of normal inter-decoder variation when the same JPEG is decoded by two different implementations, **not** of quality loss introduced by the conversion to PNG.

PNG is a lossless format. It stores exactly the pixel values produced by whichever JPEG decoder was used at the moment of conversion. Small discrepancies (mean absolute difference ≈ 3.6 levels, PSNR ≈ 34 dB, SSIM ≈ 0.95) fall within the expected range caused by:

- Different chroma upsampling methods
- Integer vs. floating-point color conversion
- Rounding conventions
- ICC profile handling

The maximum difference of 106 is localized. Combined with the low mean and median values, it does not indicate widespread degradation.

## Conclusion

The PNG is a faithful lossless container of one particular decoding of the original JPEG.  
No evidence of additional lossy compression, resampling, or significant color-space errors beyond standard JPEG decoding differences.
