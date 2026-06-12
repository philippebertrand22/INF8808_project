# -*- coding: utf-8 -*-
'''
    Contains the functions to preprocess the data used in the visualisations.

    The raw dataset (586k+ tracks, stored with Git LFS in 'data/') is
    aggregated once and the resulting summary tables are cached as small
    CSV files in 'assets/data/'. The cached files are committed to the
    repository, so the application runs out of the box without the raw
    data ; 'data/tracks.csv' is only needed to rebuild the cache after a
    change to the preprocessing.
'''
import ast
import os

import pandas as pd

TRACKS_PATH = '../data/tracks.csv'
ARTISTS_PATH = '../data/artists.csv'
CACHE_DIR = './assets/data'

# The audio features shown in visualisation 1. They are all
# normalized between 0 and 1 in the original dataset.
AUDIO_FEATURES = ['acousticness', 'danceability', 'energy', 'valence']

# Mapping of detailed genres to mainstream categories
GENRE_MAPPING = {
    # Jazz and related
    'jazz': 'jazz', 'vintage jazz': 'jazz', 'swing': 'jazz', 'stride': 'jazz',
    'bebop': 'jazz', 'cool jazz': 'jazz', 'hard bop': 'jazz', 'soul jazz': 'jazz',
    'new orleans jazz': 'jazz', 'jazz trumpet': 'jazz', 'jazz piano': 'jazz',
    'jazz saxophone': 'jazz', 'jazz blues': 'jazz', 'dixieland': 'jazz',
    'jazz trombone': 'jazz', 'jazz clarinet': 'jazz', 'jazz guitar': 'jazz',
    'jazz violin': 'jazz', 'jazz drums': 'jazz', 'gypsy jazz': 'jazz',
    'french jazz': 'jazz', 'british jazz': 'jazz', 'west african jazz': 'jazz',
    'jump blues': 'jazz', 'swing italiano': 'jazz', 'modern swing': 'jazz',
    'british dance band': 'jazz',
    
    # Classical and related
    'classical': 'classical', 'classical performance': 'classical',
    'classical piano': 'classical', 'classical guitar': 'classical',
    'classical bass': 'classical', 'classical soprano': 'classical',
    'classical tenor': 'classical', 'classical mezzo-soprano': 'classical',
    'classical baritone': 'classical', 'classical contralto': 'classical',
    'string quartet': 'classical', 'orchestra': 'classical',
    'orchestral performance': 'classical', 'historic orchestral performance': 'classical',
    'early romantic era': 'classical', 'late romantic era': 'classical',
    'post-romantic era': 'classical', 'impressionism': 'classical',
    'baroque': 'classical', 'german baroque': 'classical', 'early music': 'classical',
    'neoclassicism': 'classical', 'early modern classical': 'classical',
    'american modern classical': 'classical', 'british modern classical': 'classical',
    'russian modern classical': 'classical', 'german romanticism': 'classical',
    'french romanticism': 'classical', 'italian romanticism': 'classical',
    'russian romanticism': 'classical', 'classical era': 'classical',
    'historic piano performance': 'classical', 'historic classical performance': 'classical',
    'historic string quartet': 'classical', 'american orchestra': 'classical',
    'german orchestra': 'classical', 'austrian orchestra': 'classical',
    'french orchestra': 'classical', 'italian orchestra': 'classical',
    'british orchestra': 'classical', 'american classical piano': 'classical',
    'russian classical piano': 'classical', 'french classical piano': 'classical',
    'latin american classical piano': 'classical', 'austrian classical piano': 'classical',
    'german classical piano': 'classical', 'british classical piano': 'classical',
    'hungarian classical piano': 'classical', 'polish classical piano': 'classical',
    'polish classical': 'classical', 'ukrainian classical': 'classical',
    'czech classical': 'classical', 'violin': 'classical', 'cello': 'classical',
    'classical cello': 'classical', 'viola': 'classical', 'brass ensemble': 'classical',
    'art song': 'classical', 'choral': 'classical', 'opera': 'classical',
    'german opera': 'classical', 'french opera': 'classical', 'italian opera': 'classical',
    'operetta': 'classical', 'acousmatic': 'classical', 'exotica': 'classical',
    'library music': 'classical',
    
    # Blues and related
    'blues': 'blues', 'traditional blues': 'blues', 'country blues': 'blues',
    'delta blues': 'blues', 'chicago blues': 'blues', 'acoustic blues': 'blues',
    'piano blues': 'blues', 'texas blues': 'blues', 'memphis blues': 'blues',
    'louisiana blues': 'blues', 'new orleans blues': 'blues',
    'barrelhouse piano': 'blues', 'boogie-woogie': 'blues', 'ragtime': 'blues',
    'pre-war blues': 'blues', 'gospel blues': 'blues', 'harmonica blues': 'blues',
    'piedmont blues': 'blues', 'electric blues': 'blues',
    
    # Folk and related
    'folk': 'folk', 'traditional folk': 'folk', 'appalachian folk': 'folk',
    'old-time': 'folk', 'bluegrass': 'folk', 'progressive bluegrass': 'folk',
    'bluegrass gospel': 'folk', 'american folk revival': 'folk',
    'protest folk': 'folk', 'vintage old-time': 'folk',
    'vintage country folk': 'folk', 'american folk revival': 'folk',
    'banjo': 'folk', 'string band': 'folk', 'jug band': 'folk',
    
    # Pop/Standards
    'adult standards': 'pop/standards', 'torch song': 'pop/standards',
    'lounge': 'pop/standards', 'easy listening': 'pop/standards',
    'vintage hollywood': 'pop/standards', 'brill building pop': 'pop/standards',
    'ye ye': 'pop/standards', 'movie tunes': 'pop/standards', 'broadway': 'pop/standards',
    'tin pan alley': 'pop/standards', 'vintage chanson': 'pop/standards',
    'hollywood': 'pop/standards',
    
    # Tango
    'tango': 'tango', 'vintage tango': 'tango', 'orquesta tipica': 'tango',
    'bandoneon': 'tango',
    
    # Latin/World
    'samba': 'latin', 'velha guarda': 'latin', 'calypso': 'latin',
    'rebetiko': 'latin', 'musica tradicional cubana': 'latin',
    'son cubano': 'latin', 'son cubano clasico': 'latin',
    'flamenco': 'latin', 'nueva cancion': 'latin',
    'cumbia ecuatoriana': 'latin', 'folklore ecuatoriano': 'latin',
    'classic colombian pop': 'latin', 'rumba': 'latin', 'merengue': 'latin',
    'mento': 'latin', 'canzone napoletana': 'latin', 'classic italian pop': 'latin',
    'vintage italian pop': 'latin', 'italian adult pop': 'latin',
    'classic italian folk pop': 'latin', 'canzone genovese': 'latin',
    'classic arab pop': 'latin', 'arab folk': 'latin', 'belly dance': 'latin',
    'bouzouki': 'latin', 'greek clarinet': 'latin', 'greek indie': 'latin',
    'greek swing': 'latin', 'copla': 'latin', 'muzica populara': 'latin',
    'anadolu rock': 'latin', 'turkish rock': 'latin', 'turkish psych': 'latin',
    'turkish jazz': 'latin', 'turkish instrumental': 'latin',
    
    # Soul/R&B
    'soul': 'soul/r&b', 'rhythm and blues': 'soul/r&b',
    
    # Country
    'traditional country': 'country', 'country gospel': 'country',
    'cowboy western': 'country', 'oklahoma country': 'country',
    'bakersfield sound': 'country', 'sertanejo tradicional': 'country',
    'nashville sound': 'country', 'western swing': 'country',
    'canadian country': 'country', 'canadian singer-songwriter': 'country',
    'country boogie': 'country',
    
    # Indian/Bollywood
    'classic bollywood': 'indian', 'filmi': 'indian', 'ghazal': 'indian',
    'sufi': 'indian', 'carnatic': 'indian', 'rabindra sangeet': 'indian',
    'desi pop': 'indian', 'hindustani classical': 'indian',
    'indian classical': 'indian', 'classic tollywood': 'indian',
    'carnatic vocal': 'indian', 'bhajan': 'indian', 'classic pakistani pop': 'indian',
    'pakistani pop': 'indian', 'indie bollywood': 'indian',
    
    # Rock/Alternative
    'psychedelic rock': 'rock', 'blues rock': 'rock', 'romanian rock': 'rock',
    'german oi': 'rock', 'german punk': 'rock',
    
    # Harlem Renaissance (historical/blues-adjacent)
    'harlem renaissance': 'blues', 'vaudeville': 'pop/standards',
}


def normalize_genre(genre):
    '''Maps detailed genre to mainstream category. Returns None for unmapped genres.'''
    genre_lower = genre.lower().strip()
    return GENRE_MAPPING.get(genre_lower, None)


def add_release_year(my_df):
    '''
        Extracts the release year from the column 'release_date' and keeps
        only the tracks released between 1921 and 2020.

        Args:
            my_df: The raw tracks dataframe
        Returns:
            my_df: The dataframe with a new 'release_year' column
    '''
    my_df = my_df.copy()
    my_df['release_year'] = pd.to_numeric(
        my_df['release_date'].astype(str).str[:4], errors='coerce')
    my_df = my_df[(my_df['release_year'] >= 1921)
                  & (my_df['release_year'] <= 2020)]
    my_df['release_year'] = my_df['release_year'].astype(int)
    return my_df


def get_yearly_means(my_df):
    '''
        Computes the yearly mean of the audio features used in
        visualisation 1.

        Args:
            my_df: The tracks dataframe with a 'release_year' column
        Returns:
            The dataframe with one row per year and one column per feature
    '''
    yearly = my_df.groupby('release_year')[AUDIO_FEATURES].mean()
    return yearly.reset_index()


def get_genre_year_counts(tracks_df):
    '''
        Builds a long-format table counting unique tracks per genre per year.

        Args:
            tracks_df: The tracks dataframe with a 'release_year' column
        Returns:
            A dataframe with columns: release_year, genre, track_count
    '''
    artists = pd.read_csv(ARTISTS_PATH, usecols=['id', 'genres'])
    artists['id'] = artists['id'].str.strip()
    artists['genres'] = artists['genres'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )

    tracks_df = tracks_df.copy()
    tracks_df['id_artists'] = tracks_df['id_artists'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    exploded_artists = (
        tracks_df[['id', 'release_year', 'id_artists']]
        .explode('id_artists')
    )
    exploded_artists['id_artists'] = exploded_artists['id_artists'].str.strip()

    merged = exploded_artists.merge(
        artists, left_on='id_artists', right_on='id', how='inner'
    )

    exploded_genres = merged.explode('genres')
    exploded_genres = exploded_genres.dropna(subset=['genres'])
    exploded_genres = exploded_genres[exploded_genres['genres'].str.strip() != '']
    
    # Normalize genres to mainstream categories and filter out unmapped genres
    exploded_genres['genres'] = exploded_genres['genres'].apply(normalize_genre)
    exploded_genres = exploded_genres.dropna(subset=['genres'])

    genre_year_counts = (
        exploded_genres.groupby(['release_year', 'genres'])['id_x']
        .nunique()
        .reset_index()
        .rename(columns={'id_x': 'track_count', 'genres': 'genre'})
        .sort_values(['release_year', 'track_count'], ascending=[True, False])
    )

    genre_year_counts = genre_year_counts[genre_year_counts['track_count'] > 10]

    return genre_year_counts


def load_genre_year_counts():
    '''
        Loads the genre-year track count table.

        If the cached file is missing, reads and aggregates the raw CSVs
        and caches the result in 'assets/data/'.

        Returns:
            genre_year_counts: DataFrame with columns release_year, genre, track_count
    '''
    cache_path = f'{CACHE_DIR}/genre_year_counts.csv'

    if os.path.exists(cache_path):
        return pd.read_csv(cache_path)

    print('Building genre-year counts from raw CSV files. '
          'This may take a minute...')

    tracks = pd.read_csv(TRACKS_PATH)
    tracks = add_release_year(tracks)
    genre_year_counts = get_genre_year_counts(tracks)

    os.makedirs(CACHE_DIR, exist_ok=True)
    genre_year_counts.to_csv(cache_path, index=False)

    return genre_year_counts


def load_data():
    '''
        Loads the aggregated table used by visualisation 1.

        If the cached file is missing, the raw tracks CSV is read and
        aggregated, and the result is cached in 'assets/data/'.

        Returns:
            yearly_means: The data for visualisation 1
    '''
    cache_path = f'{CACHE_DIR}/yearly_means.csv'

    if os.path.exists(cache_path):
        return pd.read_csv(cache_path)

    print('Building the aggregated data from the raw CSV file. '
          'This is only done once and takes a few seconds...')

    tracks = pd.read_csv(TRACKS_PATH)
    tracks = add_release_year(tracks)
    yearly_means = get_yearly_means(tracks)

    os.makedirs(CACHE_DIR, exist_ok=True)
    yearly_means.to_csv(cache_path, index=False)

    return yearly_means
