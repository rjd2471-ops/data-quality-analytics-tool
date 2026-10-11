import pandas as pd 

import data_profiling as dp
# def has_outliers(column):
#     if column.dtype == 'object':
#         return False  # Categorical columns are not considered for outlier detection
#     if len(column) <= 0:
#         raise ValueError("The column is empty. Please provide a non-empty column for outlier detection.")
#     # Calculate the first and third quartiles (Q1 and Q3)
#     Q1 = column.quantile(0.25)
#     Q3 = column.quantile(0.75)
    
#     # Calculate the interquartile range (IQR)
#     IQR = Q3 - Q1
    
#     # Define the lower and upper bounds for outliers
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
    
#     # Check if there are any values outside the bounds
#     outliers = column[(column < lower_bound) | (column > upper_bound)]
#     outlier_count = len(outliers.to_dict())  # Convert the outliers to a dictionary with index as keys and outlier values as values
#     outlier_percentage = (len(outliers) / len(column)) * 100  # Calculate the percentage of outliers in the column
#     return not outliers.empty, outlier_count, outlier_percentage  # Return True if there are outliers, False otherwise


class Data_quality_Checker:
    def __init__(self, df):
        self.df = df
        self.profiling_info = dp.profiling(df)

    def get_severity(self, issue_type,percentage):#This check how serious the issue is based on the percentage of affected rows or columns. It returns a severity level as a string ("low", "medium", or "high") based on predefined thresholds for each issue type.
        if issue_type == "duplicate":
            if percentage > 10:
                return "high"
            elif percentage > 5:
                return "medium"
            else:
                return "low"
        elif issue_type == "missing_value":
            if percentage > 20:
                return "high"
            elif percentage > 10:
                return "medium"
            else:
                return "low"
        # elif issue_type == "outlier":
        #     if percentage > 5:
        #         return "high"
        #     elif percentage > 2:
        #         return "medium"
        #     else:
        #         return "low"
        # elif issue_type == "range":
        #     if percentage > 10:
        #         return "high"
        #     elif percentage > 5:
        #         return "medium"
        #     else:
        #         return "low"
        elif issue_type == "whitespace":
            if percentage > 10:
                return "high"
            elif percentage > 5:
                return "medium"
            else:
                return "low"
        elif issue_type == "invalid_data_type":
            if percentage > 10:
                return "high"
            elif percentage > 5:
                return "medium"
            else:
                return "low"
        elif issue_type == "date_format":
            if percentage > 10:
                return "high"
            elif percentage > 5:
                return "medium"
            else:
                return "low"
        elif issue_type == "category_inconsistency":
            if percentage > 10:
                return "high"
            elif percentage > 5:
                return "medium"
            else:
                return "low"

    def check_duplicates(self):
        duplicate_count = self.profiling_info['duplicate_rows']
        duplicate_percentage = self.profiling_info['duplicate_percentage']
        severity = self.get_severity("duplicate", duplicate_percentage)
        
        return {"issue_type": "duplicate", "affected_column": ["All columns"], "count": int(duplicate_count), "percentage": float(duplicate_percentage),"severity": severity, "description": "Duplicate rows found", "recommendation": "Remove duplicate rows"}

    def check_missing_values(self):
        issues = []
        missing_counts = self.profiling_info['missing_values']
        missing_percentage = self.profiling_info['missing_percentage']
        for column, count in missing_counts.items():
            if count > 0:
                severity = self.get_severity("missing_value", missing_percentage[column])
                issues.append({"issue_type": "missing_value", "affected_column": [column], "count": int(count), "percentage": float(missing_percentage[column]), "severity": severity, "description": f"Column '{column}' has missing values", "recommendation": "Handle missing values appropriately"})
        return issues


        
    # def check_outliers(self):
    #     issue = []
    #     outlier_columns = []
    #     for column in self.df.columns:
    #         if self.df[column].dtype != 'object':  # Only check numerical columns for outliers
    #             has_outliers_result, outlier_values, outlier_percentage = has_outliers(self.df[column])
    #             if has_outliers_result:
    #                 outlier_columns.append([column, outlier_values, outlier_percentage])
            
    #     for col in outlier_columns:
    #         severity = self.get_severity("outlier", col[2])
    #         issue.append({"issue_type": "outlier", "affected_column": [col[0]], "count": int(col[1]), "percentage": float(col[2]), "severity": severity, "description": f"Column '{col[0]}' has outlier values", "recommendation": "Investigate and handle outlier values appropriately"})
    #     return issue



    # def check_range(self,col,min_value, max_value):
    #     if len(col) <= 0:
    #         raise ValueError("The column is empty. Please provide a non-empty column for range checking.")
    #     invalid_values = col[(col < min_value) | (col > max_value)]
    #     invalid_count = len(invalid_values)
    #     invalid_percentage = (invalid_count / len(col)) * 100
    #     severity = self.get_severity("range", invalid_percentage)
    #     return {"issue_type": "range", "affected_column": [col.name], "count": int(invalid_count), "percentage": float(invalid_percentage), "severity": severity, "description": f"Column '{col.name}' has values outside the range [{min_value}, {max_value}]", "recommendation": "Correct or remove values outside the specified range"}



    def detect_whitespace_issues(self):
        whitespace_issues = []
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                invalid_values = self.df[col][self.df[col] != self.df[col].str.strip()]
                if not invalid_values.empty:
                    severity = self.get_severity("whitespace", len(invalid_values) / len(self.df[col].dropna()) * 100 if not self.df[col].dropna().empty else 0)
                    whitespace_issues.append({"issue_type": "whitespace", "affected_column": [col], "count": int(len(invalid_values)), "percentage": float(len(invalid_values) / len(self.df[col].dropna()) * 100) if not self.df[col].dropna().empty else 0, "severity": severity, "description": f"Column '{col}' has values with leading or trailing whitespace.", "recommendation": "Remove leading and trailing whitespace from values."})
        return whitespace_issues



    def detect_invalid_data_types(self):
        invalid_data_types = []
        
        for col in self.df.columns:
            type_counts = self.df[col].dropna().apply(type).value_counts()#type_counts is a pandas Series.
            #Here the type_counts variable is a pandas Series that contains the counts of each unique data type in the column. 
            # The dropna() method is used to exclude any missing values (NaN) from the count, and the apply(type) function is used to determine the data type of each non-null value in the column.
            #  The value_counts() method then counts the occurrences of each unique data type and returns a Series with the data types as the index and their corresponding counts as the values.
            if  type_counts.empty:
                continue  # Skip empty columns
            data_type = type_counts.index[0]  # Get the most common data type
            dominant_count = type_counts.iloc[0]  # iloc[0] means the integer count of the most common data type
            inconsistent_count = len(self.df[col].dropna()) - dominant_count  # Count of invalid data types
            if inconsistent_count > 0:
                severity = self.get_severity("invalid_data_type", inconsistent_count / len(self.df[col].dropna()) * 100 if not self.df[col].dropna().empty else 0)
                invalid_data_types.append({"issue_type": "invalid_data_type", "affected_column": [col], "count": int(inconsistent_count), "percentage": float(inconsistent_count / len(self.df[col].dropna()) * 100) if not self.df[col].dropna().empty else 0, "severity": severity, "description": f"Column '{col}' has values with invalid data types.", "recommendation": "Correct or remove values with invalid data types."})
        return invalid_data_types



    def check_date_format(self):
        date_format_issues = []
        for col in self.df.columns:
            column = self.df[col].dropna()  # Exclude missing values for date format checking
            if column.empty:
                continue  # Skip empty columns
            a = pd.to_datetime(column, errors='coerce',format='mixed')  # Convert to datetime, invalid parsing will be set as NaT
            b = len(column)  # Count of non-null values
            c = a.isna().sum()  # Count of invalid date formats
            if c ==0:
                continue  # Skip columns with no invalid date formats
            valid_count = b - c  # Count of valid date formats
            if valid_count > c:#Its mean the data type is datetime
                #format="mixed" explicitly tells Pandas:
               #“Yes, I know the values may have different formats; parse them individually.”
                severity = self.get_severity("date_format", c / b * 100)
                date_format_issues.append({"issue_type": "date_format", "affected_column": [col], "count": int(c), "percentage": float(c / b * 100), "severity": severity, "description": f"Column '{col}' has values with invalid date formats.", "recommendation": "Correct the date format in the column."})
        return date_format_issues

    
    def check_category_consistency(self):
        category_inconsistencies = []
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                column = self.df[col].dropna()  # Exclude missing values for category consistency checking
                if column.empty:
                    continue  # Skip empty columns
                cleaned_column = column.str.strip().str.lower()  # Clean the column by stripping whitespace and converting to lowercase
                if cleaned_column.nunique() < column.nunique():  # Check if the number of unique values decreased after cleaning
                    severity = self.get_severity("category_inconsistency", (column.nunique() - cleaned_column.nunique()) / column.nunique() * 100)
                    category_inconsistencies.append({"issue_type": "category_inconsistency", "affected_column": [col], "count": int(column.nunique() - cleaned_column.nunique()), "percentage": float((column.nunique() - cleaned_column.nunique()) / column.nunique() * 100), "severity": severity, "description": f"Column '{col}' has inconsistent category values (e.g., leading/trailing whitespace or case differences).", "recommendation": "Standardize category values."})
        return category_inconsistencies

    def detect_all_issues(self):
        issues = []
        
        if self.profiling_info['duplicate_rows'] > 0:
            issues.append(self.check_duplicates())
        issues.extend(self.check_missing_values())
        #issues.extend(self.check_outliers())
        issues.extend(self.detect_whitespace_issues())
        issues.extend(self.detect_invalid_data_types())
        issues.extend(self.check_date_format())
        issues.extend(self.check_category_consistency())

        return issues
if __name__ == "__main__":
    import data_loader as dl
    df = dl.load_data(r"C:\Users\PC\Desktop\DataCleaning_Tool\student-data-v2.csv")
    dq_checker = Data_quality_Checker(df)
    all_issues = dq_checker.detect_all_issues() 
    print(all_issues)
