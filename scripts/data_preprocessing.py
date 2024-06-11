import pandas as pd

class DataPreprocessing:
    @staticmethod
    def handle_missing_values(df):
        df['Trip Start Time'].fillna(df['Trip Start Time'].mode()[0], inplace=True)
        df['Trip End Time'].fillna(df['Trip End Time'].mode()[0], inplace=True)
        return df

    @staticmethod
    def handle_outliers(df, columns):
        Q1 = df[columns].quantile(0.25)
        Q3 = df[columns].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
        return df
