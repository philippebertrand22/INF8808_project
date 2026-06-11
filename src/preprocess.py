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
import os

import pandas as pd

TRACKS_PATH = '../data/tracks.csv'
CACHE_DIR = './assets/data'

# The audio features shown in visualisation 1. They are all
# normalized between 0 and 1 in the original dataset.
AUDIO_FEATURES = ['acousticness', 'danceability', 'energy', 'valence']


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
