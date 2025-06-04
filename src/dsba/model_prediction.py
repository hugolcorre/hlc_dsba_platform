import logging
import pandas as pd
from sklearn.base import ClassifierMixin
from dsba.preprocessing import preprocess_dataframe, split_features_and_target


def classify_dataframe(model, df: pd.DataFrame, target_column: str = None) -> pd.DataFrame:
    df_processed = preprocess_dataframe(df)

    # On enlève la colonne cible si elle est présente (pour éviter de prédire avec)
    if target_column and target_column in df_processed.columns:
        X, _ = split_features_and_target(df_processed, target_column)
    else:
        X = df_processed

    predictions = model.predict(X)
    df["prediction"] = predictions
    return df

def classify_record(
    model: ClassifierMixin, record: dict, target_column: str
) -> int | float | str:
    df = pd.DataFrame([record])
    _check_target_column(df, target_column)
    df = classify_dataframe(model, df, target_column)
    return df.iloc[0][target_column]


def _check_target_column(df: pd.DataFrame, target_column: str) -> None:
    """
    As a convenience, we allow the user to pass a dataframe that already has the target column in the input
    but this is quite suspicious, so we warn the user.
    then we need to drop the target column before we can continue to have the right shape for the prediction
    """
    if target_column in df.columns:
        logging.warning(
            f"Target column {target_column} already exists in the DataFrame."
        )
        df.drop(columns=[target_column], inplace=True)
