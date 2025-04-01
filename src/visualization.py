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

        # temportal popularity trends
        plt.figure(figsize=(12, 12))
        sns.lineplot(data=merged_df, x='release_date', y='popularity')
        plt.title('Spotify Popularity Trend Over Time')
        plt.xticks(rotation=45)
        plt.savefig('visualizations/popularity_trend.png')

        # top artists analysis
        plt.figure(figsize=(16, 16))
        merged_df.groupby('artist')['popularity'].mean().nlargest(10).plot(kind="barh")
        plt.title('Top 10 Artists By Average Popularity')
        plt.xlabel('Average Popularity Score')
        plt.savefig('visualizations/top_artists.png')

        # enhanced scatter plot with regression line
        plt.figure(figsize=(10, 6))
        sns.regplot(x='this_week', y='popularity', data=merged_df, scatter_kws={'alpha':0.4})
        plt.title('Chart Position vs Streaming Popularity')
        plt.savefig('visualizations/chart_vs_popularity.png')

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