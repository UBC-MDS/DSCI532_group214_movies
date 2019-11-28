import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np
from vega_datasets import data

app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Interactive Movie Database'

## Magic happens here

def make_barchart(x_axis='US_Gross:Q',
              y_axis='US_Gross:Q',
              year_slider = [1950, 2000]):

    df = alt.UrlData(
        data.movies.url
        )


    barchart = alt.Chart(df).mark_bar().transform_calculate(
        Release_Year = "year(datum.Release_Date)",
        International_Gross = "datum.Worldwide_Gross - datum.US_Gross"
    ).transform_filter(
        alt.datum.Release_Year <= year_slider[1]
    ).transform_filter(
        alt.datum.Release_Year >= year_slider[0]
    ).transform_fold(
        ['International_Gross', 'US_Gross'],
    ).encode(
        alt.Y('value:Q', aggregate = "mean", axis=alt.Axis(title='Dollars')),
        alt.X('Release_Year:O', axis=alt.Axis(title='Year')),
        color = "key:N"
    ).properties(
        title = "Average Gross",
        height = 400,
        width = 800
    )

    return barchart


def make_heatmap(x_axis='US_Gross:Q',
              y_axis='US_Gross:Q',
              year_slider = [1950, 2000]):

    df = alt.UrlData(
        data.movies.url
        )

    heatmap = alt.Chart(df).mark_rect().transform_filter(
        alt.datum.Production_Budget > 0
    ).transform_calculate(
        Release_Year = "year(datum.Release_Date)",
        Profit = "datum.Worldwide_Gross - datum.Production_Budget",
        Profit_Ratio = "datum.Profit / datum.Production_Budget"
    ).transform_filter(
        alt.datum.Release_Year <= year_slider[1]
    ).transform_filter(
        alt.datum.Release_Year >= year_slider[0]
    ).transform_filter(
        alt.datum.Profit_Ratio < 10
    ).encode(
        alt.X('IMDB_Rating:Q', bin = alt.Bin(maxbins = 50), axis = alt.Axis(title = 'IMDB Rating')),
        alt.Y('Profit_Ratio:Q', bin = alt.Bin(maxbins = 50), axis = alt.Axis(title = 'Profit Ratio ((Gross - Budget)/Budget)')),
        alt.Color('count(Profit_Ratio):Q', scale=alt.Scale(scheme='greenblue'))
    ).properties(
        title = "Average Gross",
        height = 400,
        width = 800
    )

    return heatmap

app.layout = html.Div([
    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('Interactive Movie Database'),
    html.H3('Box Office Performance Based on Genre'),
    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='barchart',
        height='600',
        width='1200',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_barchart().to_html()
        ################ The magic happens here
        ),
        ############### Plot 2 ###########
        html.Iframe(
        sandbox='allow-scripts',
        id='heatmap',
        height='600',
        width='1200',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_heatmap().to_html()
        ################ The magic happens here
        ),
        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Worldwide Gross', 'value': 'Worldwide_Gross:Q'},
            {'label': 'US DVD Sales', 'value': 'US_DVD_Sales:Q'},
            {'label': 'US Gross', 'value': 'US_Gross:Q'},
            {'label': 'Release Dates', 'value': 'Release_Date:O'},

        ],
        value='US_Gross:Q',
        style=dict(width='45%',
                   verticalAlign="middle"),
        clearable=False
        ),
        dcc.Dropdown(
        id='dd-chart-y',
        options=[
            {'label': 'Worldwide Gross', 'value': 'Worldwide_Gross:Q'},
            {'label': 'US DVD Sales', 'value': 'US_DVD_Sales:Q'},
            {'label': 'US Gross', 'value': 'US_Gross:Q'}
        ],
        value='US_Gross:Q',
        style=dict(width='45%',
                   verticalAlign="middle"),
        clearable=False
        ),
        dcc.RangeSlider(
        id='year_slider',
        min=1930,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1930, 2010, 5)},
        value=[1950, 2000]),
        html.Div(id='slider-output-container'),
])


@app.callback(
    dash.dependencies.Output('barchart', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value'),
     dash.dependencies.Input('dd-chart-y','value'),
     dash.dependencies.Input('year_slider','value')])
def update_barchart(xaxis_column_name,
                yaxis_column_name,
                year_slider):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_barchart(xaxis_column_name,
                             yaxis_column_name,
                             year_slider).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('heatmap', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-y', 'value'),
     dash.dependencies.Input('dd-chart','value'),
     dash.dependencies.Input('year_slider','value')])
def update_heatmap(xaxis_column_name,
                yaxis_column_name,
                year_slider):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot2 = make_heatmap(xaxis_column_name,
                             yaxis_column_name,
                             year_slider).to_html()
    return updated_plot2

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def update_output(value):
    return "You have selected movies from " + str(value[0]) + ' to ' + str(value[1])


if __name__ == '__main__':
    app.run_server(debug=True)