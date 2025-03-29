import requests
import pandas as pd

# Billboard API setup
API_HOST = "billboard-api2.p.rapidapi.com"
API_KEY = "107f60d81fmsh7a65c11e1bd1f59p134ab2jsna9950a6f8bcb"

def fetch_billboard_data(date="2024-05-11", range="1-10"):
    "Fetch Billboard Hot 100 chart data for a given date and range"

    url = f"https://{API_HOST}/hot-100"
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    params = {"date": date, "range": range}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        # parse JSON into DataFrame
        content = data.get("content", {})
        if isinstance(content, dict):
            songs = [
                {
                    "rank": song_data.get("rank"),
                    "title": song_data.get("title"),
                    "artist": song_data.get("artist"),
                    "weeks_on_chart": song_data.get("weeks on chart"),
                    "last_week_rank": song_data.get("last week"),
                    "peak_position": song_data.get("peak position"),
                    "detail": song_data.get("detail")
                }
                for key, song_data in content.items()
            ]
            return pd.DataFrame(songs)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return pd.DataFrame()
    
if __name__ == "__main__":
    billboard_df = fetch_billboard_data(date="2025-03-22", range="1-10")

    print("Billboard Data:")
    print(billboard_df)

    # save to CSV
    if not billboard_df.empty:
        billboard_df.to_csv("data/raw/billboard_hot_100.csv", index=False)
    else:
        print("No data available to save.")
