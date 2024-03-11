from scipy import stats
import numpy as np

def detect_outliers(col, threshold=3):
    
    """Detects outliers in a numerical series using the Z-score method.
    
    Args:
        col (pandas.Series): The numerical series to analyze.
        threshold (int): The Z-score threshold for detecting outliers.
    
    Returns:
        df that has row # outlier value and z-score
    """

    z_scores = np.abs(stats.zscore(col))
    outliers = col[(z_scores > threshold)]
    outlier_df = pd.DataFrame({'Row #': outliers.index, 'Outlier Value': outliers.values, 'Z-Score': z_scores[z_scores > threshold]})
    return outlier_df

# Example usage:
# outlier_df = detect_outliers(df['column_name'])

def detect_all_outliers(df, threshold=3):
    """Detects outliers in all numerical columns of a DataFrame using the Z-score method.
    
    Args:
        df (pandas.DataFrame): The DataFrame to analyze.
        threshold (int): The Z-score threshold for detecting outliers.
    
    Returns:
        dict: A dictionary containing the column name as key and the outlier DataFrame as value.
    """
    
    outlier_dict = {}
    for col in df.select_dtypes(include='number'):
        outlier_df = detect_outliers(df[col], threshold)
        if not outlier_df.empty:
            outlier_dict[col] = outlier_df
    return outlier_dict

def highlight_outliers(val):
    """Apply a CSS class to highlight outliers in a DataFrame."""
    
    color = 'red' if isinstance(val, (float, int)) else 'black'
    return f'color: {color}'

# Example usage:
# outlier_dict = detect_all_outliers(df)
# for col, df in outlier_dict.items():
#     st.write(f"### {col}")
#     st.dataframe(df.style.applymap(highlight_outliers))
