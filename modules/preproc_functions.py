
# ------Description: This file contains functions for data preprocessing------

#function to count number of duplicate rows in dataframe

def count_duplicate_rows(df):
    """
    Count the number of duplicate rows in a DataFrame

    Args:
        df (pandas.DataFrame): The DataFrame to analyze

    Returns:
        int: The number of duplicate rows
    """
    return df.duplicated().sum()

#returns df of duplicate rows

def get_duplicate_rows(df):

    return df[df.duplicated(keep=False)]

#function to remove duplicate rows from dataframe

def remove_duplicate_rows(df):
    """
    Remove duplicate rows from a DataFrame

    Args:
        df (pandas.DataFrame): The DataFrame to clean

    Returns:
        pandas.DataFrame: The DataFrame with duplicate rows removed
    """
    df_clean = df.copy()  # Create a copy of the DataFrame
    df_clean.drop_duplicates(inplace=True)
    return df_clean


#function to count number of missing values in dataframe

def get_total_missing_values(df):
    '''return the number of missing values in the data set'''
    return df.isna().sum().sum()

#function to count number of missing values in each column of dataframe

def get_missing_values_by_feature(df):
    '''return the number of missing values in each column of the data set'''
    return df.isna().sum()

def fill_missing_values(df, fill_method, fill_feature, fill_value):
    '''fill missing values in the data set'''
    if fill_method == "Fill with mean":
        df[fill_feature] = df[fill_feature].fillna(df[fill_feature].mean())
    elif fill_method == "Fill with median":
        df[fill_feature] = df[fill_feature].fillna(df[fill_feature].median())
    elif fill_method == "Fill with mode":
        df[fill_feature] = df[fill_feature].fillna(df[fill_feature].mode()[0])
    elif fill_method == "Fill with custom value":
        df[fill_feature] = df[fill_feature].fillna(fill_value)
    return df

#--------------------------------OUTLIER HANDLING--------------------------------

#function to count number of outliers in dataframe feature

def count_outliers(df, feature, threshold):
    '''return the number of outliers in the data set'''
    z_scores = (df[feature] - df[feature].mean()) / df[feature].std()
    return (z_scores > threshold).sum()

#function to remove outliers from dataframe feature

def remove_outliers(df, feature, threshold):
    '''remove outliers from the data set'''
    z_scores = (df[feature] - df[feature].mean()) / df[feature].std()
    df_clean = df.copy()  # Create a copy of the DataFrame
    df_clean = df_clean[z_scores <= threshold]
    return df_clean

#function to copy rows with outliers to a new dataframe

def get_outliers(df, feature, threshold):
    '''return the rows with outliers in the data set'''
    z_scores = (df[feature] - df[feature].mean()) / df[feature].std()
    return df[z_scores > threshold]

#function that returns the location of the outliers in the dataframe, their value and their z-scores
#as a table for display

def get_outliers_table(df, feature, threshold):
    '''return the location of the outliers in the data set, their value and their z-scores'''
    z_scores = (df[feature] - df[feature].mean()) / df[feature].std()
    outliers = df[z_scores > threshold]
    outliers_table = outliers.assign(z_score=z_scores[z_scores > threshold])
    return outliers_table

#get all numerical features in the dataframe

def get_numerical_features(df):
    '''return the numerical features in the data set'''
    return df.select_dtypes(include=[np.number]).columns.tolist()   

#get all categorical features in the dataframe

def get_categorical_features(df):
    '''return the categorical features in the data set'''
    return df.select_dtypes(include=['object']).columns.tolist()




