import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_external_spotify_data():
    """
        Load external Spotify top 100 dataset with genre information
    """
    file_path = 'data/external/Spotify 2010 - 2019 Top 100.csv'
    spotify_genres_df = pd.read_csv(file_path)

    # basic cleanup
    spotify_genres_df['year released'] = spotify_genres_df['year released'].fillna(-1).astype(int)
    return spotify_genres_df

def analyze_genre_trends(df):
    """
        Analyze genre popularity over time
    """
    # count genres by year
    genre_by_year = df.groupby(['year released', 'top genre']).size().reset_index(name='count')

    # find top 10 genres across all year
    top_genres = df['top genre'].value_counts().head(10).index.tolist()
    # filter for top genres only
    top_genre_trends = genre_by_year[genre_by_year['top genre'].isin(top_genres)]
    # pivot data (visualization)
    pivot_df = top_genre_trends.pivot(index='year released', columns='top genre', values='count')
    pivot_df = pivot_df.fillna(0)
    return pivot_df

def analyze_merged_data():
    """ 
        Analyze and visualize the merged Spotify and Billboard data
    """
    try:
        merged_df = pd.read_csv('data/processed/merged_data.csv')

        # visualize correlation between chart position and popularity
        plt.figure(figsize=(10, 6))
        plt.scatter(merged_df['rank'], merged_df['popularity'], alpha=0.6)
        plt.xlabel('Billboard Chart Position')
        plt.ylabel('Spotify Popularity Score')
        plt.title('Relationship Between Chart Position and Popularity')
        plt.gca().invert_xaxis() # invert so #1 on right side
        plt.savefig('visualizations/chart_vs_popularity.png')

        # visualize weeks on chart by popularity
        plt.figure(figsize=(10, 6))
        plt.scatter(merged_df['weeks_on_chart'], merged_df['popularity'], alpha=0.6)
        plt.xlabel('Weeks on Chart')
        plt.ylabel('Spotify Popularity Score')
        plt.title('Relationship Between Longevity and Popularity')
        plt.savefig('visualizations/longevity_vs_popularity.png')

        return merged_df
    except FileNotFoundError:
        print("Merged data file not found. Please run data_processing.py first")
        return None



def plot_genre_trends(genre_pivot_df):
    """
        Visualize genre trends over time
    """
    plt.figure(figsize=(12, 8))

    # plot line chart for genre trends
    for genre in genre_pivot_df.columns:
        plt.plot(genre_pivot_df.index, genre_pivot_df[genre], marker='o', linewidth=2, label=genre)

        plt.title('Evolution of Music Genres (2010-2019)', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Songs in Top 100', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

        # save visualization
        plt.savefig('visualizations/genre_trends_over_time.png')


if __name__ == "__main__":
    # load external Spotify data
    spotify_genres_df = load_external_spotify_data()

    # analyze and visualize genre trends
    genre_pivot = analyze_genre_trends(spotify_genres_df)
    plot_genre_trends(genre_pivot)

    print("Genre visualizations complete!")

    # analyze merged data
    print("\nAnalyzing merged Spotify and Billboard data...")
    merged_df = analyze_merged_data()
    if merged_df is not None:
        print("Merged data visualizations complete!")