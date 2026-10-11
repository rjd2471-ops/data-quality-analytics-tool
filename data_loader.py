import pandas as pd


def load_file(file):
    """
    Read a CSV or Excel file.

    Returns:
        df: Pandas DataFrame
        metadata: dictionary containing file information
    """

    # --------------------------------------------------
    # 1. Basic validation
    # --------------------------------------------------

    if file is None:
        raise ValueError("No file was provided.")

    filename = file.name
    extension = filename.split(".")[-1].lower()

    # --------------------------------------------------
    # 2. File size
    # --------------------------------------------------

    file_size_mb = file.size / (1024 ** 2)

    if file_size_mb > 100:
        print(
            f"Warning: Large file detected ({file_size_mb:.2f} MB). "
            "Processing may take longer.")

    # --------------------------------------------------
    # 3. CSV
    # --------------------------------------------------

    if extension == "csv":

        # Read a small portion to detect the delimiter
        file.seek(0)#this is used to go back of pointer to initial position

        sample = file.read(4096)#This is in bytes so we need to convert this into the text

        if isinstance(sample, bytes):  # Check if the sample is in bytes format
            sample = sample.decode("utf-8", errors="ignore")  # Convert bytes into text using UTF-8
        # Check supported delimiters
        delimiters = [",", ";", "\t"]#the delimiter tells Pandas where one column ends and the next column begins.

        delimiter_counts = {
            delimiter: sample.count(delimiter)
            for delimiter in delimiters
        }

        delimiter = max(
            delimiter_counts,
            key=delimiter_counts.get
        )

        # Start reading from beginning again
        file.seek(0)

        # Try UTF-8 first
        try:
            df = pd.read_csv(
                file,
                delimiter=delimiter,
                encoding="utf-8"
            )

        # If UTF-8 fails, try Latin-1
        except UnicodeDecodeError:

            file.seek(0)

            df = pd.read_csv(
                file,
                delimiter=delimiter,
                encoding="latin-1"
            )

    # --------------------------------------------------
    # 4. Excel
    # --------------------------------------------------

    elif extension in ["xlsx", "xls"]:
        
        engine = "openpyxl" if extension == "xlsx" else "xlrd"
        

        file.seek(0)

        try:
            # Get available sheets
            excel_file = pd.ExcelFile(file,engine = engine)
            sheet_names = excel_file.sheet_names

            # For now, load the first sheet
            df = pd.read_excel(
                excel_file,
                sheet_name=sheet_names[0]
            )

        except Exception as e:
            raise ValueError(
                f"Could not read Excel file: {e}"
            )

    # --------------------------------------------------
    # 5. Unsupported format
    # --------------------------------------------------

    else:
        raise ValueError(
            "Unsupported file format. "
            "Please provide a CSV or Excel file."
        )

    # --------------------------------------------------
    # 6. Empty file validation
    # --------------------------------------------------

    if df.empty:
        raise ValueError(
            "The uploaded file is empty."
        )

    # --------------------------------------------------
    # 7. Metadata
    # --------------------------------------------------

    metadata = {
        "filename": filename,
        "format": extension,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory": df.memory_usage(deep=True).sum(),
        "file_size_mb": round(file_size_mb, 2)
    }

    # --------------------------------------------------
    # 8. Return
    # --------------------------------------------------

    return df, metadata