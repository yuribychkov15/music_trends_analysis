import requests
import pandas as pd
import datetime

def fetch_billboard_data(date):
    """Fetch Billboard Hot 100 chart for a specific Saturday"""

    url = f"https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/{date}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {date}: Status {response.status_code}")
        return pd.DataFrame()
    
    try:
        data = response.json()
        entries = data.get("data", [])
        records = []

        for entry in entries:
            song_data = {
                "chart_date": date,
                "rank": entry.get("this_week"),
                "title": entry.get("song", "").strip().lower(),
                "artist": entry.get("artist", "").strip().title(),
                "last_week": entry.get("last_week", -1),
                "peak_position": entry.get("peak_position", -1),
                "weeks_on_chart": entry.get("weeksAtRank", 0),
            }
            records.append(song_data)
        return pd.DataFrame(records)
    except ValueError as e:
        print(f"Error parsing JSOn fro {date}: {e}")
        return pd.DataFrame()

def fetch_billboard_data_bulk(start_date, end_date):
    """Fetch weekly charts between dates, auto-adjusting to Saturdays"""

    # convert to datetime 
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # find the first saturday after start date
    current_date = start + datetime.timedelta(days=(5 - start.weekday()) % 7)
    all_weeks = []

    while current_date <= end:
        date_str = current_date.strftime("%Y-%m-%d")
        weekly_data = fetch_billboard_data(date_str)
        
        if not weekly_data.empty:
            all_weeks.append(weekly_data)
            print(f"Fetched {date_str}: {len(weekly_data)} entries")
        else:
            print(f"No data for {date_str}")
        
        current_date += datetime.timedelta(days=7)  # next saturday
    
    if len(all_weeks) > 0:
        return pd.concat(all_weeks, ignore_index=True)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # fetch data for all saturdays between 2024-01-06 and 2024-12-28
    billboard_df = fetch_billboard_data_bulk("2022-01-01", "2024-12-28")
    
    if not billboard_df.empty:
        billboard_df.to_csv("data/raw/billboard_hot_100_2024.csv", index=False)
        print(f"Saved {len(billboard_df)} chart entries")
    else:
        print("No data fetched")
