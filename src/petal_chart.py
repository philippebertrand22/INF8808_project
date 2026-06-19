# -*- coding: utf-8 -*-
'''
    Visualisation 2 (small multiples version): a grid of static petal
    charts, each one a "frame" sampled from the original animation,
    showing the track count of the top 10 genres at different years.
'''
import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import helper
import hover_template

TOP_N = 10
START, END = 1921, 2020
YEAR_STEP = 10
N_COLS = 4

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
        r = max(r, 0.08)
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
            legendgroup=genre,
        ))
    return traces


def get_figure(genre_year_counts):
    years = list(range(START, END + 1))
    top_genres, raw_data, g_max, genre_colors = _build_raw_data(genre_year_counts)

    N = len(top_genres)
    angle_step = 360 / N
    petal_width = angle_step * 0.8

    sample_years = list(range(START, END + 1, YEAR_STEP))
    if sample_years[-1] != END:
        sample_years.append(END)
    sample_years = [y for y in sample_years if y != 1921]  # drop the 1921 panel
    n_panels = len(sample_years)
    n_cols = N_COLS
    n_rows = math.ceil(n_panels / n_cols)

    last_row_count = n_panels - n_cols * (n_rows - 1)
    last_row_offset = (n_cols - last_row_count) // 2  # cells to skip on the left

    specs = [[{'type': 'polar'}] * n_cols for _ in range(n_rows - 1)]
    last_row_specs = [None] * n_cols
    for c in range(last_row_offset, last_row_offset + last_row_count):
        last_row_specs[c] = {'type': 'polar'}
    specs.append(last_row_specs)

    positions = []
    for panel_idx in range(n_panels):
        if panel_idx < n_cols * (n_rows - 1):
            row = panel_idx // n_cols + 1
            col = panel_idx % n_cols + 1
        else:
            row = n_rows
            col = last_row_offset + (panel_idx - n_cols * (n_rows - 1)) + 1
        positions.append((row, col))

    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        specs=specs,
        subplot_titles=[str((y // 10) * 10) for y in sample_years],
        horizontal_spacing=0.13,
        vertical_spacing=0.06,
    )

    for panel_idx, year in enumerate(sample_years):
        row, col = positions[panel_idx]
        year_idx = years.index(year)

        traces = _make_traces(
            year_idx, top_genres, raw_data, g_max,
            angle_step, petal_width, years, genre_colors,
            show_legend=False,
        )
        for trace in traces:
            fig.add_trace(trace, row=row, col=col)

    polar_layout = dict(
        radialaxis=dict(visible=False, range=[0, 1.05]),
        angularaxis=dict(
            tickmode='array',
            tickvals=[i * angle_step for i in range(N)],
            ticktext=[g.capitalize() for g in top_genres],
            direction='clockwise',
            rotation=90,
            tickfont={'size': 14},
        ),
        bgcolor='rgba(0,0,0,0)',
    )

    polar_updates = {}
    for panel_idx in range(n_panels):
        key = 'polar' if panel_idx == 0 else f'polar{panel_idx + 1}'
        polar_updates[key] = polar_layout

    fig.update_layout(
        height=300 * n_rows,
        autosize=True,
        margin=dict(l=80, r=80, t=60, b=40),
        showlegend=False,
        title=dict(
            text='Top 10 genres by track count, sampled every '
                 f'{YEAR_STEP} years ({START}\u2013{END})',
            x=0.5,
        ),
        **polar_updates,
    )

    for ann in fig['layout']['annotations']:
        ann['font'] = dict(size=16)
        ann['yshift'] = -12

    fig = helper.adjust_layout(fig)
    return fig