import pandas as pd

def process_spotify_data():
    """ 
        Process Spotify data by cleaning 
        returns: pd.dataFrame
    """
    spotify_df = pd.read_csv("data/raw/spotify_recently_played.csv")

    # convert release_date to datetime
    spotify_df["release_date"] = pd.to_datetime(spotify_df["release_date"])

    # drop rows with missing release_dates
    spotify_df = spotify_df.dropna(subset=["release_date"])

    # add year and month columns for temporal analysis
    spotify_df["year"] = spotify_df["release_date"].dt.year
    spotify_df["month"] = spotify_df["release_date"].dt.month

    # drop any unnecessary columns
    spotify_df = spotify_df.drop(columns=["danceability", "energy"], errors="ignore")

    return spotify_df

def process_billboard_data():
    """
        Process Billboard data 
        returns: pd.DataFrame
    """
    billboard_df = pd.read_csv("data/raw/billboard_hot_100.csv")

    # convert weeks_on_chart to numeric
    billboard_df["weeks_on_chart"] = pd.to_numeric(billboard_df["weeks_on_chart"])

    # fill any missing weeks_on_chart values
    billboard_df["weeks_on_chart"] = billboard_df["weeks_on_chart"].fillna(0)

    # remove duplicates based on title and artists
    billboard_df = billboard_df.drop_duplicates(subset=["title", "artist"])
    
    return billboard_df

def merge_data(spotify_db, billboard_df):
    """
        Merge Spotify and Billboard data based on artist name
        Args:
            Proccessed Spotify and Billboard data
        returns:
            pd.DataFrame: merged dataset
    """
    # merge based off artist name
    merged_df = pd.merge(
        spotify_db,
        billboard_df,
        left_on="artist",
        right_on="artist",
        how="inner",
    )

    # add a combined popularity score
    merged_df["popularity_score"] = merged_df["rank"] * merged_df["weeks_on_chart"]

    return merged_df

if __name__ == "__main__":
    # process raw data
    print("Processing Spotify data...")
    spotify_data = process_spotify_data()

    print("Processing Billboard data...")
    billboard_data = process_billboard_data()

    print("Merging Spotify and Billboard data...")
    merged_data = merge_data(spotify_data, billboard_data)

    # save processed data
    merged_data.to_csv("data/processed/merged_data.csv", index=False)
    print("Processed data saved")