# Data Quality & Analytics Tool

A Python-based application for exploring datasets, detecting data quality issues, cleaning data, analyzing statistics, and visualizing results through a Streamlit dashboard.

## Features

- Load CSV and Excel datasets.
- Profile datasets by examining rows, columns, data types, missing values, unique values, and summary statistics.
- Detect supported data quality issues.
- Apply selected data-cleaning operations.
- Compare the resulting cleaned data and cleaning log.
- Calculate numerical and categorical statistics.
- Generate visualizations using Matplotlib.
- Export cleaned data to CSV and Excel.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- OpenPyXL

## Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the Application

```bash
streamlit run app.py
```

## Project Structure

- `app.py` — Streamlit dashboard and application workflow.
- `data_loader.py` — Data loading.
- `data_profiling.py` — Dataset profiling.
- `data_quality_checker.py` — Data quality detection.
- `data_cleaning.py` — Data-cleaning operations.
- `Dataanalyser.py` — Statistical analysis.
- `data_visulazer.py` — Data visualization.

## Current Version

V1 — Initial data quality and analytics workflow.

## Future Improvements

Potential improvements will be considered after testing V1, based on identified limitations and user needs.