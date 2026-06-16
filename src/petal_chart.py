# -*- coding: utf-8 -*-
'''
    Visualisation 2 : animated petal chart showing the yearly
    track count of the top 10 genres
'''
import numpy as np
import plotly.graph_objects as go

import helper
import hover_template

TOP_N = 10
START, END = 1921, 2020

PALETTE = [
    '#378ADD'
]


def _build_raw_data(genre_year_counts):
    years = list(range(START, END + 1))

    top_genres = (
        genre_year_counts.groupby('genre')['track_count']
        .sum()
        .nlargest(TOP_N)
        .index.tolist()
    )

    genre_colors = PALETTE

    filtered = genre_year_counts[
        genre_year_counts['genre'].isin(top_genres)
    ]
    pivot = filtered.pivot_table(
        index='genre', columns='release_year',
        values='track_count', fill_value=0
    )

    raw_data = {
        genre: [int(pivot.loc[genre, y]) if y in pivot.columns else 0
                for y in years]
        for genre in top_genres
    }

    g_max = max(v for series in raw_data.values() for v in series)
    return top_genres, raw_data, g_max, genre_colors


def _make_traces(year_idx, top_genres, raw_data, g_max,
                 angle_step, petal_width, years, genre_colors,
                 show_legend):
    traces = []
    for i, genre in enumerate(top_genres):
        val = raw_data[genre][year_idx]
        r = np.sqrt(val / g_max) if g_max > 0 else 0
        r = max(r, 0.04)
        traces.append(go.Barpolar(
            r=[r],
            theta=[i * angle_step],
            width=[petal_width],
            name=genre.capitalize(),
            marker_color=genre_colors[i % len(genre_colors)],
            marker_line=dict(color='white', width=1.5),
            marker_opacity=0.92,
            hovertemplate=hover_template.petal_chart_hover_template(
                genre, years[year_idx], val),
            showlegend=show_legend,
        ))
    return traces

def get_figure(genre_year_counts):
    years = list(range(START, END + 1))
    top_genres, raw_data, g_max, genre_colors = _build_raw_data(genre_year_counts)

    N = len(top_genres)
    angle_step = 360 / N
    petal_width = angle_step * 0.62

    frames = [
        go.Frame(
            data=_make_traces(yi, top_genres, raw_data, g_max,
                              angle_step, petal_width, years,
                              show_legend=False, genre_colors=genre_colors),
            name=str(year)
        )
        for yi, year in enumerate(years)
    ]

    slider_steps = [
        dict(
            args=[[str(y)],
                  dict(frame=dict(duration=150, redraw=True),
                       mode='immediate')],
            label=str(y),
            method='animate',
        )
        for y in years
    ]

    init_traces = _make_traces(0, top_genres, raw_data, g_max,
                               angle_step, petal_width, years,
                               show_legend=False, genre_colors=genre_colors)

    fig = go.Figure(
        data=init_traces,
        frames=frames,
        layout=go.Layout(
            height=750,
            margin=dict(l=80, r=80, t=80, b=120),
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 1.05]),
                angularaxis=dict(
                    tickmode='array',
                    tickvals=[i * angle_step for i in range(N)],
                    ticktext=[g.capitalize() for g in top_genres],
                    direction='clockwise',
                    rotation=90,
                    tickfont={'size': 15},
                ),
                bgcolor='rgba(0,0,0,0)',
                domain=dict(x=[0.05, 0.95], y=[0.05, 0.95]),
            ),
            legend=dict(
                orientation='h',
                y=-0.18, x=0.5,
                xanchor='center',
                font={'size': 15},
            ),
            updatemenus=[dict(
            type='buttons',
            showactive=False,
            direction='left',
            x=0.0, xanchor='left',
            y=0, yanchor='top',
            pad=dict(t=50, r=10),
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[None, dict(
                        frame=dict(duration=150, redraw=True),
                        fromcurrent=True,
                        mode='immediate')]),
                dict(
                    label='Pause',
                    method='animate',
                    args=[[None], dict(
                        frame=dict(duration=0),
                        mode='immediate')]),
            ],
        )],
        sliders=[dict(
            active=0,
            currentvalue=dict(
                prefix='Year: ',
                font={'size': 15},
                xanchor='center',
                visible=True,
            ),
            pad=dict(t=50),
            len=0.80,
            x=0.18,
            steps=[
                dict(
                    args=[[str(y)],
                        dict(frame=dict(duration=150, redraw=True),
                            mode='immediate')],
                    label=str(y),
                    method='animate',
                )
                for y in years
            ],
        )],
        )
    )

    fig = helper.adjust_layout(fig)
    return fig