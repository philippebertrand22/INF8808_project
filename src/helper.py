# -*- coding: utf-8 -*-
'''
    This file contains the colors and some helper functions shared by the
    visualisations.
'''

# Color associated with each audio characteristic
FEATURE_COLORS = {
    'acousticness': '#264653',
    'danceability': '#2A9D8F',
    'energy': '#E76F51',
    'valence': '#F4A261',
    'speechiness': '#8AB17D',
    'instrumentalness': '#6D597A',
    'liveness': '#B56576',
    'explicit': '#E63946'
}

BACKGROUND_COLOR = '#FDFDFB'


def adjust_layout(fig):
    '''
        Applies the fonts and background shared by every figure of the
        article so that they look like they belong to the same page.

        Args:
            fig: The figure to adjust
        Returns:
            fig: The updated figure
    '''
    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font_family='Open Sans Condensed',
        font_color='#222222',
        font_size=14,
        title_font_family='Oswald',
        title_font_size=20,
        margin={'l': 60, 'r': 40, 't': 60, 'b': 50},
        dragmode=False)
    fig.update_layout(
        legend_font_family='Open Sans Condensed',
        legend_font_size=14)
    return fig
