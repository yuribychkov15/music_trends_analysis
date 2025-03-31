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
