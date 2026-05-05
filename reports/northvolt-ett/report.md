# Northvolt Ett: Industrial Site Screening

## Overview
This report provides a satellite imagery comparison for the Northvolt Ett industrial site located at `64.7340328, 21.0870825`. The analysis focuses on detecting significant land-use or structural changes between 2016 and 2025.

## Analysis Summary
The comparison between 2016 and 2025 shows a significant change in the site's appearance, likely due to the rapid industrial development of the Northvolt battery gigafactory.

| Period | Cosine Similarity | L2 Distance | Change Detected |
| :--- | :--- | :--- | :--- |
| 2016 $\rightarrow$ 2025 | -0.1997 | 4.2912 | **Yes** |
| 2024 $\rightarrow$ 2024 | 0.9971 | 0.3239 | No |
| 2024 $\rightarrow$ 2025 | 0.9937 | 0.4781 | No |

## Data Source
- **Satellite**: Sentinel-2 Level-2A
- **Provider**: Microsoft Planetary Computer STAC
- **Processing**: RGB previews from B04/B03/B02; Clay v1.5
