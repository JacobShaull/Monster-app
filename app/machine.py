import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import pandas as pd
from pandas import DataFrame

class Machine:
    def __init__(self, model=None):
        self.model = model if model else RandomForestClassifier(random_state=42)
        self.name = 'RandomForest Classifier'

    @classmethod
    def from_dataframe(cls, df: DataFrame):
        machine = cls()
        target = df['Rarity']
        features = df.drop(columns=['Rarity'])
        machine.model.fit(features, target)
        return machine

    def __call__(self, pred_basis: pd.DataFrame):
        prediction = self.model.predict(pred_basis.values.reshape(1, -1))
        probabilities = self.model.predict_proba(pred_basis.values.reshape(1, -1))
        max_probability = max(probabilities[0])
        return prediction[0], max_probability

    def save(self, filepath):
        joblib.dump(self.model, filepath)

    @staticmethod
    def open(filepath):
        model = joblib.load(filepath)
        return Machine(model)

    def info(self):
        return f"Base Model: {self.name}\nTimestamp:{datetime.now()}"