import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

def load_data():
    # load the merged dataset
    try: 
        df = pd.read_csv("data/processed/merged_data.csv")
        return df
    except FileNotFoundError:
        print("Merged data file not found. Please run data_processing.py first.")
        return None
    
def train_popularity_prediction_model(df):
    """
        Train a model to predict popularity based on available features
    """
    # select features and target
    features = ['duration_ms', 'weeks_on_chart', 'peak_position']
    X = df[features]
    y = df['popularity'] # Spotify popularity score

    # Temporal split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # train linear regression model
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    # train random forest model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    # evaulate models
    linear_pred = linear_model.predict(X_test)
    rf_pred = rf_model.predict(X_test)

    linear_rmse = math.sqrt(mean_squared_error(y_test, linear_pred))
    linear_mae = mean_absolute_error(y_test, linear_pred)

    rf_rmse = math.sqrt(mean_squared_error(y_test, rf_pred))
    rf_mae = mean_absolute_error(y_test, rf_pred)

    results = {
        'linear_model': {
            'model': linear_model,
            'rmse': linear_rmse,
            'mae': linear_mae
        },
        'random_forest': {
            'model': rf_model,
            'rmse': rf_rmse,
            'mae': rf_mae
        }
    }

    # visualize results
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, rf_pred, alpha=0.5)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
    plt.xlabel('Actual Popularity')
    plt.ylabel('Predicted Popularity')
    plt.title('Random Forest: Actual vs. Predicted Popularity')
    plt.savefig('visualizations/popularity_prediction.png')

    # feature importance for Random Forest
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(features)), importances[indices])
    plt.xticks(range(len(features)), [features[i] for i in indices])
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Feature Importance for Popularity Prediction')
    plt.savefig('visualizations/feature_importance.png')

    return results

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        results = train_popularity_prediction_model(df)
        print("Linear Regression - RMSE:", results['linear_model']['rmse'])
        print("Random Forest - RMSE:", results['random_forest']['rmse'])
