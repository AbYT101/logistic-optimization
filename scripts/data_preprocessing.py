import pandas as pd

class DataPreprocessing:
    @staticmethod
    def handle_missing_values(df):
        df['Trip Start Time'].fillna(df['Trip Start Time'].mode()[0], inplace=True)
        df['Trip End Time'].fillna(df['Trip End Time'].mode()[0], inplace=True)
        return df

    @staticmethod
    def handle_outliers(df, columns):
        for column in columns:
            # Convert columns to datetime if they are not already in datetime format
            if not pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = pd.to_datetime(df[column])
            
            # Convert datetime to numeric timestamps for quantile calculations
            df[column + '_timestamp'] = df[column].apply(lambda x: x.timestamp())
        
        # Calculate IQR for the timestamp columns
        Q1 = df[[col + '_timestamp' for col in columns]].quantile(0.25)
        Q3 = df[[col + '_timestamp' for col in columns]].quantile(0.75)
        IQR = Q3 - Q1

        # Filter out outliers
        df = df[~((df[[col + '_timestamp' for col in columns]] < (Q1 - 1.5 * IQR)) | (df[[col + '_timestamp' for col in columns]] > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        # Drop the temporary timestamp columns
        df.drop(columns=[col + '_timestamp' for col in columns], inplace=True)
        
        return df
