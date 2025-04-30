import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
    pivot_df = top_genre_trends.pivot(index='year released', columns='top genre', values='count').fillna(0)
    return pivot_df

def analyze_merged_data():
    """ 
        Analyze and visualize the merged Spotify and Billboard data
    """
    try:
        merged_df = pd.read_csv('data/processed/merged_data.csv')

        # temportal popularity trends
        merged_df['release_quarter'] = pd.to_datetime(merged_df['release_date']).dt.to_period('Q').astype(str)
        quarterly_avg = merged_df.groupby('release_quarter')['popularity'].mean().reset_index()
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=quarterly_avg, x='release_quarter', y='popularity')
        plt.title('Spotify Popularity Trend Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/popularity_trend.png')

        # top 10 artists by avg popularity
        plt.figure(figsize=(12, 8))
        merged_df.groupby('artist')['popularity'].mean().nlargest(10).plot(kind="barh")
        plt.title('Top 10 Artists By Average Popularity')
        plt.xlabel('Average Popularity Score')
        plt.tight_layout()
        plt.savefig('visualizations/top_artists.png')

        # scatter plot: success tier vs popularity
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=merged_df, x='days_since_release', y='popularity', hue='success_tier', alpha=0.6)
        plt.title('Popularity vs Days Since Release by Success Tier')
        plt.tight_layout()
        plt.savefig('visualizations/scatter_success_tier.png')

        # correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(merged_df[['popularity', 'duration_ms', 'days_since_release', 'rank', 'peak_position']].dropna().corr(), 
                    annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('visualizations/correlation_heatmap.png')

        # histograms of selected features
        for col in ['popularity', 'duration_ms', 'days_since_release']:
            plt.figure(figsize=(8, 4))
            sns.histplot(merged_df[col], kde=True, bins=30)
            plt.title(f'Distribution of {col}')
            plt.tight_layout()
            plt.savefig(f'visualizations/hist_{col}.png')

        # interactive 3D Plotly visualization
        fig = px.scatter_3d(
            merged_df,
            x='duration_ms',
            y='days_since_release',
            z='popularity',
            color='success_tier',
            hover_data=['artist', 'title', 'release_date'],
            title="3D Scatter: Duration vs Days Since Release vs Popularity"
        )
        fig.write_html('visualizations/3d_scatter.html')

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