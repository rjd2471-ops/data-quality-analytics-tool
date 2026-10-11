import pandas as pd 


class Dataanalyser :
    def __init__(self, df):
        self.df = df


    def numerical_statistics(self):
        
        data = {}
        for col in self.df.select_dtypes(include = ["number"]):
            
            data[col] = {
                "Mean":self.df[col].mean(),
                "Mode" : self.df[col].mode()[0],
                "Median": self.df[col].median(),
                "standared_deviation":self.df[col].std(),
                "minimum": self.df[col].min(),
                "count" : self.df[col].count(),#This only count the non missing value but len(self.df[col]) this will include all both zero and non zero.
                "q1" : self.df[col].quantile(.25),
                "q3": self.df[col].quantile(.75),
                "maximum": self.df[col].max(),
                "varaince": self.df[col].var()
            }
        return data


    def categorical_statistics(self):
        """
        Generate categorical statistics for the DataFrame.
        
        Returns:
            dict: Dictionary containing categorical statistics.
        """
        data = {}
        for col in self.df.select_dtypes(include = ["object","category","string"]):
            data[col] = {
                "Most_frequent": self.df[col].mode()[0],
                "Number of Unique values": self.df[col].nunique(),
                "Value_Counts": self.df[col].value_counts(),
                "missing" : self.df[col].isna().sum()
            }
        return data

    def analyze(self):
        data = {
        "numerical_statistics":self.numerical_statistics(),
        "categorical_statistics":self.categorical_statistics()
        }
        return  data

    