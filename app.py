
import streamlit as st
import data_loader as dl
import data_profiling as dp
import data_quality_checker as dqc
import data_cleaning as dc
import Dataanalyser as da
import data_visulazer as dv
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("📊 Data Quality & Analytics Tool")

st.write(
    "Upload your data, explore its profile, find quality issues, "
    "clean it, analyze it, and visualize insights.")


st.sidebar.subheader("📁 Upload Data")
st.sidebar.write("Supported formats: CSV, Excel")

file = st.sidebar.file_uploader(
    "Choose a file",
    type=["csv", "xlsx"])


if file is not None:
#------------------------------------------------------------------------------------------------
# 1. Data loading
    df, metadata = dl.load_file(file)

    if df.empty:
        st.error("The uploaded dataset is empty. ""Please upload a dataset containing rows and columns.")
        st.stop() 

    file_id = (file.name, file.size)

    if st.session_state.get("loaded_file_id") != file_id:
        st.session_state.loaded_file_id = file_id
        st.session_state.cleaned_df = df.copy()
        st.session_state.cleaning_log = []

    cleaned_df = st.session_state.cleaned_df
    st.subheader("Data Overview")

    preview_col, metadata_col = st.columns([3, 2])

    with preview_col:
        st.caption("First 5 rows")
        st.dataframe(df.head(), use_container_width=True)

    with metadata_col:
        st.caption("File Metadata")

        metadata_df = pd.DataFrame(list(metadata.items()),columns=["Property", "Value"])

        st.dataframe(metadata_df,hide_index=True,use_container_width=True)
#-----------------------------------------------------------------------------------------------
    

#-----------------------------------------------------------------------------------------------
# 2. Data Profiling
    st.subheader("Data Profiling")
    profile = dp.profiling(df)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", profile["num_rows"])
    col2.metric("Total Columns", profile["num_columns"])
    col3.metric("Duplicate Rows", profile["duplicate_rows"])
    col4.metric("Memory (MB)", round(profile["memory_usage"], 2))

    # Missing-value summary
    total_missing = sum(profile["missing_values"].values())
    total_cells = df.shape[0] * df.shape[1]
    missing_percentage = ((total_missing / total_cells) * 100 if total_cells else 0)

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Missing Cells", total_missing)
    col6.metric("Missing Cells (%)", f"{missing_percentage:.2f}%")
    col7.metric("Duplicate Rows (%)",f"{profile['duplicate_percentage']:.2f}%")
    
    columns_with_missing = sum(count > 0 for count in profile["missing_values"].values())
    col8.metric("Columns with Missing Values", columns_with_missing)

    # Column-level profiling table
    st.subheader("Column Details")

    column_details = pd.DataFrame({
        "Data Type": profile["data_types"],
        "Missing Values": profile["missing_values"],
        "Missing (%)": profile["missing_percentage"],
        "Unique Values": profile["unique_values"]
    })

    st.dataframe(column_details, use_container_width=True)

    # Summary statistics
    st.subheader("Summary Statistics")

    summary_df = pd.DataFrame(profile["summary_statistics"])
    st.dataframe(summary_df, use_container_width=True)
#----------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
# 3. Data quality checking
    st.subheader("Data Quality Issues")
    dq_checker = dqc.Data_quality_Checker(df)
    quality = dq_checker.detect_all_issues()

    # Calculate issue counts
    total_issues = len(quality)
    high_count = sum(issue["severity"] == "high" for issue in quality)
    medium_count = sum(issue["severity"] == "medium" for issue in quality)
    low_count = sum(issue["severity"] == "low" for issue in quality)

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Issues", total_issues)
    col2.metric("High Severity", high_count)
    col3.metric("Medium Severity", medium_count)
    col4.metric("Low Severity", low_count)

    
    # Display detailed issues
    if quality:
        quality_df = pd.DataFrame(quality)

        # Make column names easier to read
        quality_df = quality_df.rename(columns={
            "issue_type": "Issue Type",
            "affected_column": "Affected Column",
            "count": "Affected Count",
            "percentage": "Affected (%)",
            "severity": "Severity",
            "description": "Description",
            "recommendation": "Recommendation"
        })

        # Format percentage values
        quality_df["Affected (%)"] = quality_df["Affected (%)"].map(lambda value: f"{value:.2f}%")

        st.dataframe(quality_df,hide_index=True,use_container_width=True)
    else:
        st.success("No data quality issues detected.")

#---------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# 4. Data cleaning
    st.subheader("Data Cleaning")

    cleaning_options = {
        "Remove duplicates": "remove_duplicates",
        "Remove missing values": "remove_missing_values",
        "Trim whitespace": "trim_whitespace",
        "Standardize categories": "standardize_categories",
        "Standardize column names": "standardize_column_names"
    }

    selected_actions = st.multiselect(
        "Choose cleaning operations",
        options=list(cleaning_options.keys())
    )

    if st.button("Apply cleaning"):

        choices = {
            action: action in [
                cleaning_options[label]
                for label in selected_actions
            ]
            for action in cleaning_options.values()
        }

        cleaner = dc.DataCleaner(st.session_state.cleaned_df)

        cleaned_df, cleaning_log = cleaner.user_control_actions(choices)

        st.session_state.cleaned_df = cleaned_df
        st.session_state.cleaning_log = cleaning_log

    cleaned_df = st.session_state.cleaned_df
    cleaning_log = st.session_state.cleaning_log

    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df,hide_index= True,use_container_width= True)

    st.subheader("Cleaning Log")

    if cleaning_log:
        st.dataframe(cleaning_log,hide_index= True, use_container_width= True)
    else:
        st.info("No cleaning actions were selected.")
#-----------------------------------------------------------------------------       


#-----------------------------------------------------------------------------
# 5. Statistical analysis
    st.subheader("Statistical Analysis")

    analyser = da.Dataanalyser(cleaned_df)
    results = analyser.analyze()

    numerical_results = results["numerical_statistics"]
    categorical_results = results["categorical_statistics"]

    st.write("Numerical Statistics")
    if numerical_results:
        st.dataframe(numerical_results)
    else:
        st.info("No numerical columns found.")

    st.write("Categorical Statistics")
    if categorical_results:
        st.dataframe(categorical_results)
    else:
        st.info("No categorical columns found.")


    
    # Data visualization
    import matplotlib.pyplot as plt

    visual = dv.Visualizer(cleaned_df)

    st.subheader("Data Visualizer")

    # Select the column to visualize
    selected_column = st.selectbox(
        "Select a column",
        cleaned_df.columns.tolist()
    )

    # Select the type of chart
    chart_type = st.selectbox(
        "Select chart type",
        ["Histogram", "Box Plot", "Bar Chart", "Missing Values Heatmap"]
    )

    if st.button("Generate Chart"):
        try:
            if chart_type == "Histogram":
                fig = visual.plot_numeric_distributions(selected_column)

            elif chart_type == "Box Plot":
                fig = visual.plot_numeric_boxplot(selected_column)

            elif chart_type == "Bar Chart":
                fig = visual.plot_categorical_bar(selected_column)

            else:
                fig = visual.plot_missing_values_heatmap()

            st.pyplot(fig)
            plt.close(fig)

        except (ValueError, TypeError) as error:
            st.warning(str(error))
#-----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
# Data export

    st.subheader("Export Cleaned Data")

    # Option 1: Export as CSV
    csv_data = cleaned_df.to_csv(index=False)

    st.download_button(
        label="Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv")
    

    # Option 2: Export as Excel
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")

    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="Download Cleaned Excel",
        data=excel_data,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    















# """
# Python File Handling — Short Notes

# 1. Basic Concepts

# - I/O: Input/Output — reading data into a program and writing/sending data out.
# - Disk: Permanent storage for files (SSD/HDD).
# - RAM: Temporary working memory used by running programs.
# - Bits/Bytes: Basic units of computer data; 1 byte = 8 bits.
# - Buffer: Temporary memory area that holds data during transfer or processing.

# 2. File Handling

# - "open(file, 'r')" — read.
# - "open(file, 'w')" — write; clears existing content first.
# - "open(file, 'a')" — append; preserves existing content and writes at the end.
# - "f.tell()" — current file position.
# - "f.seek(n)" — move file position.
# - EOF: End of file; no more data is available to read.
# - "with open(...)" — automatically closes the file when the block ends.

# 3. Text vs Bytes

# - Text ("str"): Human-readable characters.
# - Bytes ("bytes"): Encoded data used for storage and transfer.
# - "text.encode('utf-8')" → text to bytes.
# - "data.decode('utf-8')" → bytes to text.
# - Binary files must be interpreted according to their file format; not all bytes are text.

# 4. CSV vs Excel

# - CSV: Plain-text tabular data; simple and lightweight.
# - Excel (".xlsx"): Structured workbook; supports multiple sheets, formatting and formulas.
# - Renaming ".csv" to ".xlsx" does not convert the file format.

# 5. DataFrame → Download

# - DataFrame: Tabular data structure in RAM.
# - Serialization: Converting in-memory data into a file format.
# - "df.to_csv(index=False)" → CSV text.
# - ".encode('utf-8')" → CSV text to bytes.
# - "df.to_excel(...)" → creates Excel-format output using an Excel-writing engine.
# - "BytesIO()" → in-memory binary buffer; does not automatically create a disk file.
# - "buffer.getvalue()" → retrieves bytes from the buffer.
# - "st.download_button()" → sends the file data to the user's browser for downloading.

# 6. Project Workflow

# DataFrame → CSV/Excel serialization → file bytes → browser → user downloads file.

# Remember:

# - CSV can be generated directly as a string, then encoded into bytes.
# - Excel needs a workbook writer; "BytesIO" can hold its output in memory.
# - Downloading does not require permanently saving the file on the server.
# - A buffer uses RAM; it does not automatically improve speed or reduce memory usage
# """