import requests
import pandas as pd
import datetime

def fetch_billboard_data(date):
    """Fetch Billboard Hot 100 chart for a specific Saturday"""

    url = f"https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/{date}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        chart_df = pd.DataFrame(data["data"])
        chart_df["chart_date"] = date  # add tracking date
        return chart_df
    return pd.DataFrame()

def fetch_billboard_data_bulk(start_date="2024-01-01", end_date="2025-01-01"):
    """Fetch weekly charts between dates, auto-adjusting to Saturdays"""

    # convert to datetime 
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # find the first saturday after start date
    current_date = start + datetime.timedelta(days=(5 - start.weekday()) % 7)
    all_data = pd.DataFrame()

    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        weekly_data = fetch_billboard_data(date_str)
        
        if not weekly_data.empty:
            all_data = pd.concat([all_data, weekly_data], ignore_index=True)
            print(f"Fetched {date_str}: {len(weekly_data)} songs")
        else:
            print(f"No data for {date_str}")
        
        current_date += datetime.timedelta(days=7)  # next saturday
    
    return all_data

if __name__ == "__main__":
    # fetch data for all saturdays between 2024-01-06 and 2024-12-28
    billboard_df = fetch_billboard_data_bulk("2024-01-06", "2024-12-28")
    
    if not billboard_df.empty:
        billboard_df.to_csv("data/raw/billboard_hot_100_2024.csv", index=False)
        print(f"Saved {len(billboard_df)} chart entries")
    else:
        print("No data fetched")
