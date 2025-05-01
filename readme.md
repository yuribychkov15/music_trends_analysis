**Midterm Report Video Link:** https://youtu.be/NjSm3KxVdu0
# Music Trends Analysis: Predicting Popularity from Billboard Charts and Genre Attributes

## How to Build and Run the Code
### Setup Instructions

1. Clone the repository:
git clone <your-repo-url>
cd music_trends_analysis

2. Set up the virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
make setup

### Run Full Pipeline
make all

This includes data collection, preprocessing, model training, visualizations, and test runs.

### Run Individually
- Run pipeline + model: make run-model
- Run only visualizations: make run-viz
- Run tests: make test
- Clean all output: make clean

## Music Consumption Trends Analysis
### Description:
Analyze the evolution of music trends by collecting data from Spotify and Billboard. The project will explore how factors like artist popularity, genre shifts, and streaming numbers change over time.

## Project Overview
This project explores the relationship between Billboard chart success and Spotify popularity. The pipeline:
- Collects and cleans music data from both Billboard and Spotify
- Merges datasets into a unified, feature-rich CSV
- Trains regression models to predict streaming popularity
- Outputs visualizations to interpret feature relationships and trends
  
**Primary Goal:** Predict future music popularity trends (e.g., streaming counts or chart positions for artists/tracks).

**Our hypothesis:** Songs that rank high or last long on Billboard charts also tend to have higher Spotify popularity, but other factors like release timing and duration also matter.

## Data Collection and Processing
### Sources:

- Spotify API (via Spotipy): Tracks, durations, popularity scores, and release dates

- Billboard Hot 100 (GitHub JSON archive): Weekly chart positions and longevity

- Billboard Hot weekly charts dataset from data.world: Billboard and Spotify data from 1958-present (https://data.world/kcmillersean/billboard-hot-100-1958-2017)

### Processing Details
**Billboard JSON Archive:**
- Cleaned artist and title columns for merging
- Filled missing or year-only dates with full YYYY-01-01
- Created new features:
  - days_since_release and log_days_since_release
  - success_tier: Top Hit (1-10), Moderate (11-50), Niche (51-100)
  - 
**Data.world dataset:**
- merged multiple chart entries into one containing most relevant features
- merged Billboard dataset with audio feature dataset
- created new features:
  - 4 classes based on peak chart position
  - 9 broad genre categories extrapolated from existing data

## Modeling
We trained three models to predict popularity:
**Features Used:**
- duration_ms

- peak_position

- weeks_on_chart

- days_since_release

**Models & Metrics**
Model                     RMSE           MAE

Linear Regression        12.44           9.67

Random Forest Regressor  12.06           9.08

HistGradientBoosting     12.21           9.08

Random Forest performed best with good error reduction and ability to model non-linear interactions.
**Key Takeaways**
- Billboard rank and peak position strongly inform popularity

- Newer tracks (lower days_since_release) often rank higher

- Longer tracks (~2–4 minutes) cluster near peak popularity

**Analyzing Audio Features**
Random Forest Classifier: used to determine importance of each feature (tempo, energy, etc.)

Principal Component Analysis and Random Forest Regressor: trained on audio features to attempt to model chart prevalence/longevity

Autoregressive Integrated Moving Average (ARIMA): Trained on recent genre data and chart prevalence of genres to predict future trends
  
##  Visualization
 insert images
  
## Testing and Automation
### Pipeline Testing
test_pipeline.py checks:

- That Spotify and Billboard data are successfully processed

- That merged dataset is not empty

- That models train and achieve RMSE < 20

**Makefile**
Automates the full flow:
make all     # end-to-end pipeline
make test    # run tests
make clean   # cleanup
