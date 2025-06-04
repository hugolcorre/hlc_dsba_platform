from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# from sklearn.model_selection import train_test_split


def split_features_and_target(
    df: DataFrame, target_column: str
) -> tuple[DataFrame, Series]:
    """
    Splits a DataFrame into features and target, which is a common format used by machine learning libraries such as scikit-learn.
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in the DataFrame.")
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y


def split_dataframe(
    df: DataFrame, test_size: float = 0.2
) -> tuple[DataFrame, DataFrame]:
    return train_test_split(df, test_size=test_size, random_state=42)


def preprocess_dataframe(df, target_column=None):
    """
    Preprocess DataFrame by encoding categorical columns.
    ML algorithms typically can't only handle numbers, so there may be quite a lot of feature engineering and preprocessing with other types of data.
    Here, we take a very simplistic approach of applying the same treatment to all non-numeric columns.
    """

    df = df.copy()

    #Deleting useless columns that won't impact the prediction
    df.drop(columns=["Name", "Ticket", "Cabin", "PassengerId"], inplace=True, errors="ignore")

    # Handling NaN values
    for col in df.columns:
        if col == target_column:
            continue 
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    # Encoding categorical variables
    for column in df.select_dtypes(include=["object"]):
        if column == target_column:
            continue  
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))

    return df


