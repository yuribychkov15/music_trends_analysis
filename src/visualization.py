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