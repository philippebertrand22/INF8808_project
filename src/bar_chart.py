# -*- coding: utf-8 -*-
'''
    Visualisation xxx : The bar chart showing if there is a correlation
between popularity and song characteristics
'''
import plotly.graph_objects as go

import helper
import hover_template

# Necessary settings are also defined 
# in app, preprocess, helper and hovertemplate.py.

def get_figure(means_by_popularity):
    '''
        Generates the bar chart of the mean audio characteristics by popularity

        Args:
            means_by_popularity
            
        Returns:
            fig: The generated figure
    '''
    #print(helper.BAR_CHART_COLORS)
    fig = go.Figure()
    
    
    popularity_labels = means_by_popularity["popularity_class"].values
    features = [col for col in means_by_popularity.columns]
    features.remove('popularity_class') 

    for label in popularity_labels:
        mask = means_by_popularity["popularity_class"] == label
        
        fig.add_trace(go.Bar(
            y = [feature.capitalize() for feature in features],
            x = means_by_popularity[mask][features].values[0],
            name = label.capitalize(),
            marker_color= helper.BAR_CHART_COLORS[label]['color'],
            orientation='h',
            legendrank = helper.BAR_CHART_COLORS[label]['rank'],
            hovertemplate=hover_template.bar_chart_hover_template()
        )
        )
    fig.update_layout(
    height=520,
    xaxis={'title': 'Mean value (0 - 1)', 'range': [0, 1],
            'gridcolor': '#E8E8E3'},
    #legend={'orientation': 'h', 'y': -0.18, 'x': 0.5,
    #        'xanchor': 'center'},
        legend={'title':"Pupularity"},
    hovermode='closest')
    
    fig = helper.adjust_layout(fig)
    return fig
