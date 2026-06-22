# -*- coding: utf-8 -*-
'''
    Visualisation 4: Radar chart comparing mean audio features
    across popularity classes (or other groupings).
'''
import plotly.graph_objects as go

import helper
import hover_template

def get_figure(decades_means):
    '''Radar chart comparing 3 time periods'''
    fig = go.Figure()

    features = [col for col in decades_means.columns if col != 'period']
    features_closed = features + [features[0]]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # nice distinct colors

    for i, (_, row) in enumerate(decades_means.iterrows()):
        values = [row[f] for f in features] + [row[features[0]]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=[f.capitalize() for f in features_closed],
            name=row['period'],
            line=dict(color=colors[i % len(colors)], width=3),
            opacity=0.75,
            hovertemplate=hover_template.radar_chart_hover_template()
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, showline=False, ticks=''),
            angularaxis=dict(tickfont=dict(size=13))
        ),
        height=560,
        title="Evolution of Audio Features Across Eras",
        legend=dict(title="Time Period", orientation="h", y=-0.15, x=0.5, xanchor='center')
    )

    fig = helper.adjust_layout(fig)
    return fig