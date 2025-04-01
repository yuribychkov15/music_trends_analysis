# How to Run:
## Clone the repository ##

[https://github.com/yuribychkov15/cs506#]

## Create and activate virtual enviornment ##

python3 -m venv venv

source venv/bin/activate 

## Install dependencies ##

pip install -r requirements.txt

## To Deactivate Virtual Enviornment ##

deactivate

# Project Proposal

## Music Consumption Trends Analysis
### Description:
Analyze the evolution of music trends by collecting data from Spotify and Billboard. The project will explore how factors like artist popularity, genre shifts, and streaming numbers change over time.

### Goal(s):

**Primary Goal:** Predict future music popularity trends (e.g., streaming counts or chart positions for artists/tracks).

**Secondary Goal:** Identify emerging genres or artists based on historical data trends.

### Data Collection:

**What Data:** Artist names, track titles, genres, streaming counts, chart positions, release dates, etc.

**How to Collect:**
Use the Spotify API (via libraries like Spotipy) to fetch current and historical streaming data.
Scrape Billboard charts using Python libraries such as requests and BeautifulSoup to extract chart positions and other metadata.

### Data Modeling Approaches:

**Time Series Forecasting:** Apply ARIMA or Facebook Prophet to predict future streaming numbers or chart positions.
**Regression Models:** Use linear or non-linear regression to relate features (e.g., social media mentions, historical performance) with future popularity.

### Data Visualization Techniques:

**Line Plots:** To display trends in streaming counts and chart positions over time.

**Scatter Plots:** To compare relationships between different features (e.g., genre vs. streaming numbers).

**Interactive Dashboards:** Use tools like Plotly or Dash for dynamic exploration of trends.

### Test Plan:

**Approach:**
Temporally split the data (e.g., train on data until a certain month and test on data from the subsequent month).
Reserve the last 20% of the time-series data as a holdout test set.
Evaluate performance using error metrics such as RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error).

# Midterm Report

## Data Collection

  - **Spotipy (Spotify API):** extracted track details including artist names, track titles, release dates, popularity scores, and duration metrics
  - **Billboard API:** collected Hot 100 chart data featuring ranking information, artist names, song titles, and chart performance metrics like peak position and number of weeks on chart 

## Data Processing
  **Step-by-step breakdown:**
  - Converting date fields to proper date/time format
  - Extracting temporal features (year and month)
  - Handling missing values in the weeks_on_chart column
  - Removing duplicate entries based on title and artist combinations
  - Merging Spotify and Billboard datasets using artist names as the joining field

## Model Selection and Training
  **Goal:** Predict song popularity based on various features extracted from APIs
  Models used:
  
  **1. Linear Regression:** A baseline approach establishing fundamental relationships between features and popularity
  
  - Benefits: computationally efficient, interpretable results show clear correlation if such a relationship exists
    
  **2. Random Forest Regressor:** A more complex ensemble method to capture non-linear patterns
  
  -  Benefits: able to handle nonlinearity, mitigates overfitting, less sensitive to outliers/noise

![image](https://github.com/user-attachments/assets/282ea1df-6671-48f5-9ded-79ffd5d27e6b)
- Actual probability vs. predicted probability using random forests
  
![image](https://github.com/user-attachments/assets/b4f9905f-1535-4ad4-a193-abcd9af888d2)
- Demonstrates which extracted features were most important in predicting a song's popularity in order of most to least important

  
## Preliminary Results and Visualization
![image](https://github.com/user-attachments/assets/d8c8fe7d-90c0-4bcb-aa46-a848fe025978)
- Shows relationship between popularity over time and release dates

![image](https://github.com/user-attachments/assets/14be84aa-9e54-4e30-aa6a-e566f4c8538b)
- Top 10 current artists on Spotify and their average popularity

## Challenges and Future Plans
**Challenges**
- Aligning track titles between Spotify and Billboard when merging data due to naming conventions, addressed by standardizing the formatting in preprocessing
- Many older Billboard charts have missing information for some records, we can remedy this by filtering out these entries or reducing data to only include entries past a certain date where it can be verified that all records are complete

**Future Plans**
- Refining our models with additional algorithms, like ARIMA for time-series forecasting or neural networks for modeling more complex patterns
- Incorporate other metrics of popularity like social media mentions or playlist inclusions
- Analyze more audio features beyond track statistics such as genre, BPM, and valence
- Create interactive dashboards using tools like Plotly or Dash for accessibility
