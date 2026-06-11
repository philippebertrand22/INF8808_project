# -*- coding: utf-8 -*-
'''
    Visualisation 1 : line chart showing the yearly mean of the audio
    characteristics, with the major global crises highlighted.
'''
import plotly.graph_objects as go

import helper
import hover_template

# The historical events highlighted on the chart. Periods are drawn as
# shaded regions, one-year events as vertical lines.
CRISES = [
    {'name': 'Great Depression', 'start': 1929, 'end': 1933, 'level': 1.04},
    {'name': 'World War II', 'start': 1939, 'end': 1945, 'level': 1.10},
    {'name': '2008 crash', 'start': 2008, 'end': 2009, 'level': 1.04},
    {'name': 'COVID-19', 'start': 2020, 'end': 2020.9, 'level': 1.10}
]


def get_figure(yearly_means):
    '''
        Generates the line chart of the mean audio characteristics per
        year, between 1921 and 2020.

        Args:
            yearly_means: The dataframe with one row per year and one
                column per characteristic
        Returns:
            fig: The generated figure
    '''
    fig = go.Figure()

    features = [col for col in yearly_means.columns
                if col != 'release_year']
    for feature in features:
        fig.add_trace(go.Scatter(
            x=yearly_means['release_year'],
            y=yearly_means[feature],
            mode='lines',
            name=feature.capitalize(),
            line={'color': helper.FEATURE_COLORS[feature], 'width': 2},
            hovertemplate=hover_template.line_chart_hover_template()))

    for crisis in CRISES:
        fig.add_vrect(
            x0=crisis['start'], x1=crisis['end'],
            fillcolor='#9A9A9A', opacity=0.18, line_width=0)
        center = min((crisis['start'] + crisis['end']) / 2, 2020)
        fig.add_annotation(
            x=center, y=crisis['level'],
            yref='paper', showarrow=False,
            text=crisis['name'],
            xanchor='right' if center >= 2019 else 'center',
            font={'family': 'Oswald', 'size': 12, 'color': '#555555'})

    fig.update_layout(
        height=520,
        xaxis={'title': 'Release year', 'showgrid': False,
               'range': [1921, 2020]},
        yaxis={'title': 'Mean value (0 – 1)', 'range': [0, 1],
               'gridcolor': '#E8E8E3'},
        legend={'orientation': 'h', 'y': -0.18, 'x': 0.5,
                'xanchor': 'center'},
        hovermode='closest')

    fig = helper.adjust_layout(fig)
    return fig
