Anladım. Hata ayıklayıcı çıktılarını uygulayarak ve son halini oluşturarak sadece kod bloğunu vereceğim:

```python
import os
import sys
import json
import time
import asyncio
import logging
import unittest
import threading
import subprocess
from pathlib import Path
from enum import Enum, auto
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import wraps, lru_cache
from abc import ABC, abstractmethod
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV

# Constants
DEFAULT_CONFIG = {
    "model_params": {
        "n_estimators": 100,
        "max_depth": None,
        "random_state": 42
    },
    "preprocessing": {
        "test_size": 0.2,
        "random_state": 42,
        "k_best_features": 10
    }
}

class ModelType(Enum):
    CLASSIFICATION = auto()
    REGRESSION = auto()

@dataclass
class ModelConfig:
    model_type: ModelType
    params: Dict[str, Any]
    preprocessing: Dict[str, Any]

class BaseModel(ABC):
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

    @abstractmethod
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        pass

class RandomForestModel(BaseModel):
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = RandomForestClassifier(**config.params)
        self.preprocessor = self._build_preprocessor()
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
        self.feature_selector = SelectKBest(score_func=f_classif)

    def _build_preprocessor(self) -> ColumnTransformer:
        numeric_features = self._get_numeric_features()
        categorical_features = self._get_categorical_features()

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        return preprocessor

    def _get_numeric_features(self) -> List[str]:
        return self.X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    def _get_categorical_features(self) -> List[str]:
        return self.X.select_dtypes(include=['object', 'category']).columns.tolist()

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.X = X
        self.y = y

        # Preprocessing
        X_processed = self.preprocessor.fit_transform(X)

        # Feature selection
        X_selected = self.feature_selector.fit_transform(X_processed, y)

        # Model training
        self.model.fit(X_selected, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        X_processed = self.preprocessor.transform(X)
        X_selected = self.feature_selector.transform(X_processed)
        return self.model.predict(X_selected)

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        y_pred = self.predict(X)
        accuracy = accuracy_score(y, y_pred)
        report = classification_report(y, y_pred, output_dict=True)
        return {
            'accuracy': accuracy,
            'precision': report['weighted avg']['precision'],
            'recall': report['weighted avg']['recall'],
            'f1_score': report['weighted avg']['f1-score']
        }

class ModelTrainer:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or DEFAULT_CONFIG
        self.models: Dict[str, BaseModel] = {}

    def add_model(self, name: str, model: BaseModel) -> None:
        self.models[name] = model

    def train_all(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Dict[str, float]]:
        results = {}
        for name, model in self.models.items():
            model.train(X, y)
            results[name] = model.evaluate(X, y)
        return results

    def get_best_model(self, results: Dict[str, Dict[str, float]]) -> Tuple[str, Dict[str, float]]:
        return max(results.items(), key=lambda x: x[1]['accuracy'])

class DataLoader:
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_model(model: BaseModel, file_path: str) -> None:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)

    @staticmethod
    def load_model(file_path: str) -> BaseModel:
        with open(file_path, 'rb') as f:
            return pickle.load(f)

class Logger:
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

class AsyncTaskManager:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = Logger(__name__)

    async def run_in_thread(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args, **kwargs)

    def shutdown(self):
        self.executor.shutdown(wait=True)
        self.logger.info("Thread pool executor shutdown complete")

class TestModel(unittest.TestCase):
    def setUp(self):
        self.X = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
        self.y = pd.Series([0, 1, 0, 1, 0])

        config = ModelConfig(
            model_type=ModelType.CLASSIFICATION,
            params={"n_estimators": 10, "random_state": 42},
            preprocessing={"k_best_features": 2}
        )

        self.model = RandomForestModel(config)

    def test_model_training(self):
        self.model.train(self.X, self.y)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.y))

    def test_model_evaluation(self):
        self.model.train(self.X, self.y)
        metrics = self.model.evaluate(self.X, self.y)
        self.assertIn('accuracy', metrics)
        self.assertGreater(metrics['accuracy'], 0)

if __name__ == "__main__":
    unittest.main()
```