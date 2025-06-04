"""
This module is just a convenience to train a simple classifier.
Its presence is a bit artificial for the exercice and not required to develop an MLOps platform.
The MLOps course is not about model training.
"""


from dataclasses import dataclass
import logging
import pandas as pd
import xgboost as xgb
from datetime import datetime
from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from dsba.model_registry import ClassifierMetadata
from .preprocessing import split_features_and_target, preprocess_dataframe


def train_multiple_classifiers(
    df: pd.DataFrame, target_column: str, model_id_prefix: str, random_state: int = 42
) -> tuple[ClassifierMixin, ClassifierMetadata]:
    logging.info("🚀 Start training multiple classifiers")
    df = preprocess_dataframe(df)
    X, y = split_features_and_target(df, target_column)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=random_state)

    models = {
        "xgboost": xgb.XGBClassifier(random_state=random_state),
        "random_forest": RandomForestClassifier(random_state=random_state),
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "svm": SVC(probability=True, random_state=random_state),
        "decision_tree": DecisionTreeClassifier(random_state=random_state),
    }

    best_score = -1
    best_model = None
    best_name = None

    for name, model in models.items():
        logging.info(f"🔧 Training {name}")
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        score = f1_score(y_val, preds, average="macro")
        logging.info(f"📊 {name} f1-score: {score:.4f}")

        if score > best_score:
            best_score = score
            best_model = model
            best_name = name

    model_id = f"{model_id_prefix}_{best_name}"
    metadata = ClassifierMetadata(
        id=model_id,
        created_at=str(datetime.now()),
        algorithm=best_name,
        target_column=target_column,
        hyperparameters={"random_state": random_state},
        description="Best model selected among XGBoost, RandomForest, LogisticRegression, SVM, DecisionTree",
        performance_metrics={"f1_score": best_score},
    )

    logging.info(f"🏆 Best model: {model_id} with f1-score {best_score:.4f}")
    return best_model, metadata
