# Northvolt Ett: Industrial Site Screening

## Overview
This report provides a satellite imagery comparison for the Northvolt Ett industrial site located at `64.7340328, 21.0870825`. The analysis focuses on visible/spectral change between a valid early Sentinel-2 baseline and 2025.

## Analysis Summary
The original 2016 tile was blank/all-zero and has been retired from the report. A valid 2017 baseline shows only minor change in the broad 2.56 km Clay embedding, while the RGB preview still provides visual context for localized site development.

| Period | Cosine Similarity | L2 Distance | Change Detected |
| :--- | :--- | :--- | :--- |
| 2017 $\rightarrow$ 2025 | 0.9304 | 1.6063 | Minor embedding change |
| 2018 $\rightarrow$ 2025 | 0.9262 | 1.6339 | Minor embedding change |
| 2024 $\rightarrow$ 2024 | 0.9971 | 0.3239 | No |
| 2024 $\rightarrow$ 2025 | 0.9937 | 0.4781 | No |

## Data Source
- **Satellite**: Sentinel-2 Level-2A
- **Provider**: Microsoft Planetary Computer STAC
- **Processing**: RGB previews from B04/B03/B02; Clay v1.5
