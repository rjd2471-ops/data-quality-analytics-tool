import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:

    def __init__(self, df):
        self.df = df

    def plot_numeric_distributions(self, column):
        #check whether the column exists
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        # Check whether the column is numerical
        if not pd.api.types.is_numeric_dtype(self.df[column]):#api: an interface through which Pandas exposes certain utilities.
            raise TypeError(f"Column '{column}' is not numerical.")

        # Remove missing values for plotting
        values = self.df[column].dropna()

        if values.empty:
            raise ValueError(f"Column '{column}' has no valid numerical values.")
        
        fig,ax = plt.subplots()
        ax.hist(values,bins = 10,color = "lightgreen",edgecolor = "black",label=f"{column}")#This show the spread of the numberical data.
        ax.set_xlabel(column)                    # X-axis: numerical values
        ax.set_ylabel("Frequency")               # Y-axis: number of observations
        ax.set_title(f"Distribution of {column}") # Chart title
        ax.legend()

        fig.tight_layout()
        return fig
        

    def plot_numeric_boxplot(self, column):

        # Check whether the column exists
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        # Check whether the column is numerical
        if not pd.api.types.is_numeric_dtype(self.df[column]):#api: an interface through which Pandas exposes certain utilities.
            raise TypeError(f"Column '{column}' is not numerical.")

        # Remove missing values for plotting
        values = self.df[column].dropna()

        if values.empty:
            raise ValueError(f"Column '{column}' has no valid numerical values.")

        # Create the figure and axes
        fig, ax = plt.subplots()

        # Generate the box plot
        ax.boxplot(values)
        ax.grid()
        ax.set_ylabel(column)
        ax.set_title(f"Box Plot of {column}")

        fig.tight_layout()

        return fig


    
    def plot_categorical_bar(self, column):
        # Check whether the column exists
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        # Check whether the column is categorical
        if not (
            pd.api.types.is_object_dtype(self.df[column])
            or pd.api.types.is_categorical_dtype(self.df[column])
            or pd.api.types.is_string_dtype(self.df[column])
        ):
            raise TypeError(f"Column '{column}' is not categorical.")

        # Count the occurrences of each category
        count = self.df[column].value_counts()

        if count.empty:
            raise ValueError(
                f"Column '{column}' has no valid categorical values."
            )

        # Create the bar chart
        fig, ax = plt.subplots()

        ax.bar(count.index.astype(str), count.values)

        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Frequency of {column}")

        # Improve readability when category names are long
        ax.tick_params(axis="x", labelrotation=45)

        fig.tight_layout()
        return fig


    def plot_missing_values_heatmap(self):
        # A heatmap requires at least one row and one column
        if self.df.empty:
            raise ValueError("Cannot create a heatmap from an empty DataFrame.")

        # True means missing; False means present
        missing = self.df.isnull()

        fig, ax = plt.subplots()

        ax.imshow(
            missing.to_numpy(),
            aspect="auto",
            interpolation="nearest"
        )

        # Label the columns and rows
        ax.set_xticks(range(len(self.df.columns)))
        ax.set_xticklabels(
            self.df.columns.tolist(),
            rotation=45,
            ha="right"
        )

        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
        ax.set_title("Missing Values Heatmap")

        fig.tight_layout()
        return fig


    def generate_all_charts(self):
        charts = {}

        # Numerical columns → histograms
        for column in self.df.select_dtypes(include=["number"]).columns:
            # Skip columns with no valid numerical values
            if self.df[column].dropna().empty:
                continue

            charts[f"histogram_{column}"] = (
                self.plot_numeric_distributions(column)
            )

        # Categorical columns → bar charts
        categorical_columns = self.df.select_dtypes(
            include=["object", "category", "string"]
        ).columns

        for column in categorical_columns:
            # Skip columns with no valid categorical values
            if self.df[column].dropna().empty:
                continue

            charts[f"bar_{column}"] = self.plot_categorical_bar(column)

        # Whole DataFrame → missing-values heatmap
        if not self.df.empty:
            charts["missing_values_heatmap"] = (
                self.plot_missing_values_heatmap()
            )

        return charts
