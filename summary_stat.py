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

app.layout = html.Div(children=[
    html.H4(children='Movies database - summary statistics'),
    #generate_table(df),
    html.Div(dcc.RangeSlider(
        id='year_slider',
        min=1900,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1930, 2010, 5)},
        value=[1950, 2000])), 
    html.Div(id='slider-output-container'),
])

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def update_output(year_slider):
    k = df[(df['Release_Date'] > year_slider[0][0]) & (df['Release_Date'] < year_slider[0][1]) ].sort_values(by = "US_Gross",ascending = False)
    k_US_Gross = round(k.iloc[1,1]/1000000,3)
    k_movie = k.iloc[1,0]
    return (k_movie, "was the highest US grossing movie in the period", year_slider,"at",k_US_Gross, " M USD")

if __name__ == '__main__':
    app.run_server(debug=True)