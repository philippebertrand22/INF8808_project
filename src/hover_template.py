# -*- coding: utf-8 -*-
'''
    Provides the templates for the tooltips of the visualisations.
'''


def line_chart_hover_template():
    '''
        Sets the template for the hover tooltips on the lines of
        visualisation 1.

        Shows the name of the characteristic, the year and the exact
        mean value.

        Returns:
            The hover template.
    '''
    return ('<span style="font-family:Oswald"><b>%{fullData.name}</b></span>'
            '<br><span style="font-family:Open Sans Condensed">'
            'Year : %{x}<br>'
            'Mean value : %{y:.3f}</span>'
            '<extra></extra>')\

def petal_chart_hover_template(genre, year, count):
    return (
        f'<b>{genre.capitalize()}</b><br>'
        f'Year: {year}<br>'
        f'Tracks: {count:,}'
        '<extra></extra>'
    )

def bar_chart_hover_template():
    '''
        Sets the template for the hover tooltips on the lines of
        visualisation xxx.

        Shows the name of the popularity class and the exact
        mean value.

        Returns:
            The hover template.
    '''
    return ('<span style="font-family:Oswald"><b>%{fullData.name}</b></span>'
            '<br><span style="font-family:Open Sans Condensed">'
            'Feature : %{y}<br>'
            'Mean value : %{x:.3f}<br>'
            '<extra></extra>')

def radar_chart_hover_template():
    return (
        '<b>%{fullData.name}</b><br>'
        'Feature: %{theta}<br>'
        'Mean value: %{r:.3f}'
        '<extra></extra>'
    )