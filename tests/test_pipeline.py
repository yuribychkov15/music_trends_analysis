# test_pipeline.py

import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import process_spotify_data, process_billboard_data, merge_data
from src.train_model import train_popularity_prediction_model

def test_data_pipeline():
    try:
        spotify_df = process_spotify_data()
        billboard_df = process_billboard_data()
        merged_df = merge_data(spotify_df, billboard_df)

        assert not merged_df.empty, "Merged DataFrame is empty"
        assert {'popularity', 'duration_ms'}.issubset(merged_df.columns), "Expected columns missing"

        print("Data pipeline test passed")
    except Exception as e:
        print("Data pipeline test failed: {e}")

def test_model_training():
    try:
        df = pd.read_csv("data/processed/merged_data.csv")
        results = train_popularity_prediction_model(df)
        assert 'random_forest' in results, "Random Forest results missing"
        assert results['random_forest']['rmse'] < 20, "Model RMSE too high"
        print("Model training test passed.")
    except Exception as e:
        print(f"Model training test failed: {e}")

if __name__ == "__main__":
    test_data_pipeline()
    test_model_training()