import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np
from vega_datasets import data
import dash_bootstrap_components as dbc
alt.data_transformers.enable('json')

df = pd.read_json('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json', orient = 'columns')
df['Release_Date'] =  pd.to_datetime(df['Release_Date'], infer_datetime_format=True)
df['Release_Date'] = df['Release_Date'].dt.year

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    

# def generate_table(dataframe, max_rows=10):

#      return html.Table(
        
#         # # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] 

#         # # Body
#         # [html.Tr([
#         #     html.Td(dataframe.iloc[5][col]) for col in dataframe.columns
#         # ]) for i in range(min(len(dataframe), max_rows))]
        
    # )



row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("Genre [Year1 Year2]"))),
        dbc.Row(
            [
                dbc.Col(html.Div(id='slider-output-container-1')),
                dbc.Col(html.Div(id='slider-output-container-2')),
                dbc.Col(html.Div(id='slider-output-container-3')),
            ]
        ),
    ]
)

app.layout = html.Div(children=[
    html.H4(children='Movies database - summary statistics'),
    #generate_table(df),
    row,
    html.Div(dcc.RangeSlider(
        id='year_slider',
        min=1900,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1930, 2010, 5)},
        value=[1950, 2000])), 
])

@app.callback(
    dash.dependencies.Output('slider-output-container-1', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def highest_grossing(value):
    k = df[(df['Release_Date'] > value[0]) & (df['Release_Date'] < value[1]) ].sort_values(by = "US_Gross",ascending = False)
    k_US_Gross = k.iloc[1].loc['US_Gross']/1000
    k_movie = k.iloc[0].loc['Title']
    a = "The highest grossing \n movie in the US was " + k_movie + " at " + str(k_US_Gross) + " M USD "
    return a

@app.callback(
    dash.dependencies.Output('slider-output-container-2', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def lowest_grossing(value):
    k = df[(df['Release_Date'] > value[0]) & (df['Release_Date'] < value[1]) ].sort_values(by = "US_Gross",ascending = True)
    k_US_Gross = k.iloc[1].loc['US_Gross']/1000
    k_movie = k.iloc[0].loc['Title']
    b = "The lowest grossing movie in the US was " + k_movie + " at " + str(k_US_Gross) + "K USD"
    return b



@app.callback(
    dash.dependencies.Output('slider-output-container-3', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def lowest_(year_info):
    '''This function gives you the WW GRossing 
    
    Inputs :
        year_info : Takes in the year information from the callback above
        genre_input : (To be programmed) : takes in the genre information
    '''

    genre_input = 'Drama' #Implement as Callback
    k = df[df['Major_Genre'] == genre_input]
    k = df[(df['Release_Date'] > year_info[0]) & (df['Release_Date'] < year_info[1]) ].sort_values(by = "US_Gross",ascending = True)
    k_US_Gross = k.iloc[1].loc['Worldwide_Gross']/1000
    k_movie = k.iloc[0].loc['Title']
    return "The lowest grossing movie WW was " + k_movie + " at " + str(k_US_Gross) + "K USD"

    


if __name__ == '__main__':
    app.run_server(debug=True)