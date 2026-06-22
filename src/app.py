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

#edit test
import dash
from dash import dcc, html

import preprocess as preproc
import line_chart
import petal_chart
import bar_chart
import radar_chart

app = dash.Dash(__name__)
app.title = 'Project | INF8808E'
server = app.server  # exposed for the production server (gunicorn)

yearly_means = preproc.load_data()
genre_counts = preproc.load_genre_year_counts()
means_by_popularity = preproc.load_bar_chart_data()
decades_means = preproc.load_decades_means_data()

GRAPH_CONFIG = {
    'showTips': False,
    'showAxisDragHandles': False,
    'displayModeBar': False,
    'scrollZoom': False,
    'responsive': True
}

fig1 = line_chart.get_figure(yearly_means)
fig2 = petal_chart.get_figure(genre_counts)
fig3 = bar_chart.get_figure(means_by_popularity)
fig4 = radar_chart.get_figure(decades_means)

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
            'Music is a constantly changing scene, artists rise and fall '
            'as the years pass. Trends appear, some are here to stay, and '
            'others vanish. But one thing is for sure, during the last 15 '
            'years, the way we listen to music has drastically changed. We '
            'went from buying CDs and listening to the radio to streaming '
            'most of what we listen to. All while short form content rose '
            'and turned attention into a scarce resource.')),
        html.P(className='lead', children=(
            'Using a Spotify dataset of more than 586,000 tracks between '
            '1921 and 2020. So, have the characteristics of popular music '
            'shifted over the past century? And did music structurally '
            'adapt to fit short form content and streaming?')),

        # ------------------------------------------------ Visualisation 1
        html.H2('A Century of Music'),
        html.P(children=(
            'Spotify describes characteristics based on a score going from '
            '0 to 1. Here we display Energy that is a measure of intensity '
            'and activity, valence (how positive a track sounds), '
            'danceability and acousticness. All the characteristics are '
            'averaged out over a year. We can directly identify two '
            'long-term movements in the graph: first we see a long and '
            'steady rise of energy, rising from around 0.3 in the 20s to '
            '0.64 in 2020. The second notable trend is the collapse of '
            'acousticness starting in the 1950s, which corroborates with '
            'the introduction of electrical instruments.')),
        html.P(children=(
            'We marked important historical events with shaded bars. For '
            'example the average valence goes from 0.59 in 1939 to 0.49 '
            'in 1945, it will only recover in post-war years. To see '
            'specific values, hover over the lines.')),
        dcc.Graph(id='line-chart', figure=fig1, config=GRAPH_CONFIG,#viz1----------------location
                  className='graph'),

        # ------------------------------------------------ Visualisation 2
        html.H2('A Century of Genre Evolution'),
        html.P(children=(
            'Each petal chart is a snapshot of one year, sampled every '
            'decade from 1930 to 2020. Around each chart, every spoke is '
            'one of the ten most prevalent genres in the dataset, and a '
            'petal\u2019s length encodes the number of unique tracks '
            'released that year — the longer the petal, the more tracks. '
            'Read the grid left to right, top to bottom, to see genres '
            'rise and fall across the century.')),
        html.P(children=(
            'We can see throughout the decades the rise and fall of jazz '
            'and rock, as well as the rise of Latin music.')),
        dcc.Graph(id='petal-chart', figure=fig2, config=GRAPH_CONFIG,
                  className='graph'),

        # ------------------------------------------------ Visualisation 3
        html.H2('Audio Features Through Decades'),
        html.P(children=(
            'This radar chart compares the average profile of tracks across seven key '
            'audio features. Each line represents three decades of music. The blue line represents the period from 1930 to 1960, '
            'the orange line represents 1960 to 1990, and the green line represents 1990 to 2020. '
            'Through the decades tracks features clearly move toward more energy and lower acousticness.')),
        dcc.Graph(id='radar-chart', figure=fig4, config=GRAPH_CONFIG,
                  className='graph'),

        # ------------------------------------------------ Visualisation 4
        html.H2("Today's Popular Audio Features"),
        html.P(children=(
            'This bar chart compares the average values of key audio features '
            'across four popularity tiers: Very Low (<25), Low (25–50), High (50–75), '
            'and Very High (>75). '
            'Each group of bars represents one audio feature. '
            'Taller bars mean higher average values of the audio feature. '
            'The red bars (Very High popularity) show what characteristics dominate '
            'in today’s most popular tracks.')),
        html.P(children=(
            'Higher popularity strongly correlates with higher danceability '
            'and energy. On the other hand, acousticness and instrumentalness correlate with lower popularity. '
            'This suggests that modern popular music tends to be more upbeat, rhythmic, and produced for '
            'immediate listening. Likely an adaptation to streaming and short-form content.')),
        dcc.Graph(id='bar-chart', figure=fig3, config=GRAPH_CONFIG,
                  className='graph'),

        # ------------------------------------------------ Conclusion
        html.H2('Conclusion'),
        html.P(children=(
            'After exploring this dataset and creating these visualizations, '
            'we feel that we can draw a few conclusions. We believe that the '
            'premise under which music has adapted to streaming and short form '
            'content is true. As we look at the different graphs, bar charts, '
            'etc., time and time again we see that duration seems to diminish, '
            'genre diversity seems to crash and some key characteristics seem '
            'to be valued (e.g.: the rise and fall of energy and acousticness).')),
        html.P(children=(
            'But in the end this analysis was done on characteristics; we don’t '
            'have access to the precise tracks or their lyrics. It would have been '
            'very interesting to work on the evolution of word diversity in music, '
            'the mapping of rhythmic types, keys, chord progressions and so on. '
            'For future work, a direct access to the core data (tracks and lyrics) '
            'could let us dive deep into the adaptation of music to our modern world.')),

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
