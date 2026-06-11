# -*- coding: utf-8 -*-
'''
    File name: app.py
    Course: INF8808E
    Python Version: 3.8+

    This file contains the source code for the project of team 5 :
    "Mapping the evolution of global music trends (1921-2020)".

    The application is a scrollable, article-like page. The user scrolls
    through a story told by five visualisations, each accompanied by a
    short explanation of what to look at.

    Current state : article header, introduction and visualisation 1.
    The other four visualisations will be added one section at a time.
'''
import dash
from dash import dcc, html

import preprocess as preproc
import line_chart

app = dash.Dash(__name__)
app.title = 'Project | INF8808E'

yearly_means = preproc.load_data()

GRAPH_CONFIG = {
    'showTips': False,
    'showAxisDragHandles': False,
    'displayModeBar': False,
    'scrollZoom': False
}

fig1 = line_chart.get_figure(yearly_means)


app.layout = html.Div(children=[
    html.Header(className='hero', children=[
        html.P('INF8808E — Data visualization — Team 5',
               className='kicker'),
        html.H1('The Changing DNA of Popular Music'),
        html.P('Mapping the evolution of global music trends, 1921 – 2020',
               className='subtitle'),
        html.P('Alexander Lelouche · Taro Sugiura · Gaspard Juillet · '
               'Eva Mosny · Philippe Bertrand · Charles-Emmanuel Joyal',
               className='byline')
    ]),

    html.Article(className='article', children=[

        # ------------------------------------------------- Introduction
        html.P(className='lead', children=(
            'Music is a constantly shifting mix of genres, sounds and '
            'personalities. Artists rise and fall, sounds evolve, and '
            'cultural moments leave permanent marks on the landscape. '
            'But over the last decade, it is the way we listen that has '
            'changed the most : around 2015, streaming became the '
            'uncontested mainstream way of consuming music, and '
            'short-form content turned attention into the scarcest '
            'resource of all.')),
        html.P(className='lead', children=(
            'Using a Spotify dataset of more than 586,000 tracks released '
            'between 1921 and 2020, we ask one question : how have the '
            'characteristics of popular music shifted over the past '
            'century — and has music structurally adapted its DNA to fit '
            'the streaming era ? Scroll down to follow the story.')),

        # ------------------------------------------------ Visualisation 1
        html.H2('1. A century of sound, scarred by history'),
        html.P(children=(
            'Spotify describes every track with a set of audio '
            'characteristics scored between 0 and 1 : energy (intensity '
            'and activity), valence (how positive a track sounds), '
            'danceability and acousticness. Averaged over every track '
            'released in a year, they sketch a portrait of each era. Two '
            'long-term movements stand out immediately : a relentless '
            'rise in energy — from about 0.28 in the early 1920s to 0.64 '
            'today — and the collapse of acousticness after the 1950s, '
            'when electric instruments and studio production took over.')),
        html.P(children=(
            'The shaded bands mark major global crises. Look at valence '
            'during World War II : the average positivity of new music '
            'slides from 0.59 in 1939 to 0.49 in 1945, and only recovers '
            'in the post-war years — a gradual, multi-year shift rather '
            'than an immediate one. Hover over a line to read the exact '
            'mean value of a characteristic for a given year.')),
        dcc.Graph(id='line-chart', figure=fig1, config=GRAPH_CONFIG,
                  className='graph'),

        html.Footer(className='footer', children=[
            html.P(children=[
                'Data : ',
                html.A('Spotify Dataset 1921–2020, 600k+ Tracks '
                       '(Yamac Eren Ay, Kaggle)',
                       href='https://www.kaggle.com/datasets/yamaerenay/'
                            'spotify-dataset-19212020-600k-tracks',
                       target='_blank'),
                ' — collected through the Spotify API.']),
            html.P('INF8808E — Data visualization, Polytechnique '
                   'Montréal — Summer 2026, Team 5.')
        ])
    ])
])
