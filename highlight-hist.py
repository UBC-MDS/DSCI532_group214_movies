import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np
from vega_datasets import data
alt.data_transformers.enable('json')

app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Dash app with pure Altair HTML'
## Magic happens here
def make_plot(x_axis='US_Gross:Q',
              y_axis='US_Gross:Q'):

    chart = alt.Chart('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json'
    ).mark_circle(size=90
    ).encode(
                alt.X(x_axis, 
                title = x_axis.replace("_", " ")[:-2]),
                alt.Y(y_axis,
                title = y_axis.replace("_", " ")[:-2]),
                tooltip = ['Title:N', 'Director:N']
            ).properties(title=x_axis[:-2].replace("_", " ") + " vs. " + y_axis[:-2].replace("_", " "),
                        width=500, height=350).interactive()
    return chart

def make_highlight_hist(year_slider = [1950, 2000],
                genre = "Comedy"):

    df = alt.UrlData(
        data.movies.url
        )


    genre_hist = alt.Chart(df).mark_bar(

    ).transform_calculate(
        Release_Year = "year(datum.Release_Date)",
        International_Gross = "datum.Worldwide_Gross - datum.US_Gross"
    ).transform_filter(
        alt.datum.Release_Year < year_slider[1]
    ).transform_filter(
        alt.datum.Major_Genre != None
    ).transform_filter(
        alt.datum.Release_Year > year_slider[0]
    ).encode(
        alt.X('Major_Genre:N', 
            axis=alt.Axis(title='Genre',
                        labelAngle=-20)),
        alt.Y('count()'),
        color=alt.condition(
                    alt.datum.Major_Genre == genre,
                        alt.value("orange"),
                        alt.value("gray"))
    ).properties(
        title = "Histogram of Genres",
       width=500, 
       height=350
    )

    return genre_hist

app.layout = html.Div([
    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    html.H3('Here is an image'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='10%'),
    html.H3('Here is our first plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='470',
        width='655',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
        ############### Plot 3 ###########
        html.Iframe(
        sandbox='allow-scripts',
        id='plot3',
        height='470',
        width='655',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_highlight_hist().to_html()
        ################ The magic happens here
        ),
        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Worldwide Gross', 'value': 'Worldwide_Gross:Q'},
            {'label': 'US DVD Sales', 'value': 'US_DVD_Sales:Q'},
            {'label': 'US Gross', 'value': 'US_Gross:Q'},
            {'label': 'Release Dates', 'value': 'Release_Date:O'}
            

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
        dcc.Dropdown(
        id='genre_choice',
        options=[
            {'label': 'Action', 'value': 'Action'},
            {'label': 'Adventure', 'value': 'Adventure'},
            {'label': 'Black Comedy', 'value': 'Black_Comedy'},
            {'label': 'Comedy', 'value': 'Comedy'},
            {'label': 'Documentary', 'value': 'Documentary'},
            {'label': 'Drama', 'value': 'Drama'},
            {'label': 'Horror', 'value': 'Horror'},
            {'label': 'Musical', 'value': 'Musical'},
            {'label': 'RomCom', 'value': 'Romantic Comedy'},
            {'label': 'Thriller', 'value': 'Thriller/Suspense'},
            {'label': 'Western', 'value': 'Western'}

        ],
        value='Drama',
        style=dict(width='45%',
                   verticalAlign="middle"),
        clearable=False
        ),
        dcc.RangeSlider(
        id='year_slider',
        min=1900,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1930, 2010, 5)},
        value=[1950, 2000]),
])


@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value'),
     dash.dependencies.Input('dd-chart-y','value')])
def update_plot(xaxis_column_name,
                yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,
                             yaxis_column_name).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('year_slider','value'),
    dash.dependencies.Input('genre_choice','value')])
def update_plot3(year_slider,
                genre_choice):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_3 = make_highlight_hist(year_slider,
                             genre_choice
                             ).to_html()
    return updated_plot3

if __name__ == '__main__':
    app.run_server(debug=True)