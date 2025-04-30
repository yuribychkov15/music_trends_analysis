import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
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
    df['release_date'] = pd.to_datetime(df['release_date'])

    # temporal split (80% trainm, 20% test)
    cutoff = df['release_date'].quantile(0.8)
    train = df[df['release_date'] <= cutoff]
    test = df[df['release_date'] > cutoff]

    features = ['duration_ms', 'weeks_on_chart', 'peak_position', 'days_since_release']

    # Temporal split (80% train, 20% test)
    X_train, X_test = train[features], test[features]
    y_train, y_test = train['popularity'], test['popularity']


    results = {}

    # linear regression
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    linear_pred = linear_model.predict(X_test)
    results['linear_model'] = {
        'model': linear_model,
        'rmse': math.sqrt(mean_squared_error(y_test, linear_pred)),
        'mae': mean_absolute_error(y_test, linear_pred)
    }

    # random forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    results['random_forest'] = {
        'model': rf_model,
        'rmse': math.sqrt(mean_squared_error(y_test, rf_pred)),
        'mae': mean_absolute_error(y_test, rf_pred)
    }

    # HistGradientBoosting
    hgb_model = HistGradientBoostingRegressor()
    hgb_model.fit(X_train, y_train)
    hgb_pred = hgb_model.predict(X_test)
    results['hist_gradient_boosting'] = {
        'model': hgb_model,
        'rmse': math.sqrt(mean_squared_error(y_test, hgb_pred)),
        'mae': mean_absolute_error(y_test, hgb_pred)
    }


    # visualize results, scatter: actual vs. predicted (random forest)
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
        for name, res in results.items():
            print(f"{name.replace('_', ' ').title()} - RMSE: {res['rmse']:.2f} | MAE: {res['mae']:.2f}")
