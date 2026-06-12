# -*- coding: utf-8 -*-
'''
    Visualisation 2 : animated petal (rose) chart showing the yearly
    track count of the top N genres, between 1921 and 2020.
'''
import numpy as np
import plotly.graph_objects as go

import helper
import hover_template

TOP_N = 10
START, END = 1921, 2020

PALETTE = [
    '#378ADD', '#1D9E75', '#D85A30', '#7F77DD', '#BA7517',
    '#D4537E', '#639922', '#888780', '#E24B4A', '#0F6E56',
]


def _build_raw_data(genre_year_counts):
    '''
        Pivots the long-format genre_year_counts table into a dict of
        {genre: [count_per_year]} for every year in [START, END].

        Args:
            genre_year_counts: DataFrame with columns release_year, genre,
                track_count
        Returns:
            top_genres: Ordered list of the top N genre names
            raw_data:   Dict mapping each genre to a list of yearly counts
            g_max:      Global maximum count (used for scaling)
            genre_colors: Dict mapping each genre to a stable color
    '''
    years = list(range(START, END + 1))

    top_genres = (
        genre_year_counts.groupby('genre')['track_count']
        .sum()
        .nlargest(TOP_N)
        .index.tolist()
    )

    # Assign a colour to each genre by its rank position — no hardcoding
    genre_colors = {genre: PALETTE[i % len(PALETTE)]
                    for i, genre in enumerate(top_genres)}

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
    '''
        Builds one Barpolar trace per genre for a single year.

        Args:
            year_idx:    Index into the years list
            top_genres:  Ordered list of genre names
            raw_data:    Dict of {genre: [yearly counts]}
            g_max:       Global maximum (for radius scaling)
            angle_step:  Angular separation between petals (degrees)
            petal_width: Angular width of each petal (degrees)
            years:       Full list of years
            genre_colors: Dict mapping each genre to a color
            show_legend: Whether to render legend entries
        Returns:
            List of Barpolar traces
    '''
    traces = []
    for i, genre in enumerate(top_genres):
        val = raw_data[genre][year_idx]
        r = np.sqrt(val / g_max) if g_max > 0 else 0
        traces.append(go.Barpolar(
            r=[r],
            theta=[i * angle_step],
            width=[petal_width],
            name=genre.capitalize(),
            marker_color=genre_colors[genre],
            marker_opacity=0.82,
            hovertemplate=hover_template.petal_chart_hover_template(
                genre, years[year_idx], val),
            showlegend=show_legend,
        ))
    return traces


def get_figure(genre_year_counts):
    '''
        Generates the animated petal chart of track counts per genre
        per year, between 1921 and 2020.

        Args:
            genre_year_counts: DataFrame with columns release_year, genre,
                track_count
        Returns:
            fig: The generated figure
    '''
    years = list(range(START, END + 1))
    top_genres, raw_data, g_max, genre_colors = _build_raw_data(genre_year_counts)

    N = len(top_genres)
    angle_step = 360 / N
    petal_width = angle_step * 0.44

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
                  dict(frame=dict(duration=200, redraw=True),
                       mode='immediate')],
            label=str(y),
            method='animate',
        )
        for y in years
    ]

    init_traces = _make_traces(0, top_genres, raw_data, g_max,
                               angle_step, petal_width, years,
                               show_legend=True, genre_colors=genre_colors)

    fig = go.Figure(
        data=init_traces,
        frames=frames,
        layout=go.Layout(
            height=750,
            margin=dict(l=80, r=80, t=80, b=120),
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 1.15]),
                angularaxis=dict(
                    tickmode='array',
                    tickvals=[i * angle_step for i in range(N)],
                    ticktext=[g.capitalize() for g in top_genres],
                    direction='clockwise',
                    rotation=90,
                    tickfont={'size': 11},
                ),
                bgcolor='rgba(0,0,0,0)',
                domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]),
            ),
            legend=dict(
                orientation='h',
                y=-0.18, x=0.5,
                xanchor='center',
                font={'size': 11},
            ),
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                y=1.06, x=0.5, xanchor='center',
                buttons=[
                    dict(
                        label='▶  Play',
                        method='animate',
                        args=[None, dict(
                            frame=dict(duration=200, redraw=True),
                            fromcurrent=True,
                            mode='immediate')]),
                    dict(
                        label='⏸  Pause',
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
                    font={'size': 14},
                    xanchor='center',
                    visible=True,
                ),
                pad=dict(t=50),
                len=0.9,
                x=0.05,
                steps=[
                    dict(
                        args=[[str(y)],
                              dict(frame=dict(duration=100, redraw=True),
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