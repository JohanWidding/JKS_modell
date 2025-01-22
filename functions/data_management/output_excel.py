import pandas as pd
import inspect

def save_dfs_to_excel(file_name, dfs, file_location, sheet_names=None):
    """
    Save multiple DataFrames to an Excel file, each in a separate sheet, with column widths adjusted.

    Args:
        file_name (str): The name of the Excel file to create (without extension).
        dfs (list): A list of pandas DataFrames to save.
        file_location (str): The directory location to save the Excel file.
        sheet_names (list, optional): A list of names for the sheets. If not provided, defaults to numbering (1, 2, 3, ...).

    Returns:
        None
    """
    # Get the caller's local variables
    caller_locals = inspect.currentframe().f_back.f_locals

    # Match DataFrame objects to their variable names
    df_names = {id(v): k for k, v in caller_locals.items() if isinstance(v, pd.DataFrame)}

    # Full file path
    file_path = f"{file_location}/{file_name}.xlsx"

    # Default sheet names to numbers if not provided
    if sheet_names is None:
        sheet_names = [str(i + 1) for i in range(len(dfs))]

    # Write to Excel
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for i, df in enumerate(dfs):
            # Try to get the variable name, fallback to provided or numbered name
            sheet_name = sheet_names[i] if i < len(sheet_names) else df_names.get(id(df), f"Sheet{i + 1}")
            # Ensure valid Excel sheet names (max 31 characters)
            sheet_name = sheet_name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=True)

            # Adjust column widths
            worksheet = writer.sheets[sheet_name]
            for col_num, column in enumerate(df.columns, start=1):  # Columns are 1-indexed in Excel
                max_width = max(
                    df[column].astype(str).map(len).max(),  # Max length of column values
                    len(column)  # Length of column header
                )
                worksheet.set_column(col_num, col_num, max_width)  # Double the width

    print(f"Excel file saved at {file_path}")
