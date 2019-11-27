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

    chart = alt.Chart('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json').mark_circle(size=90).encode(
                alt.X(x_axis, 
                title = x_axis.replace("_", " ")[:-2]),
                alt.Y(y_axis,
                title = y_axis.replace("_", " ")[:-2]),
                tooltip = ['Title:N', 'Director:N']
            ).properties(title=x_axis[:-2].replace("_", " ") + " vs. " + y_axis[:-2].replace("_", " "),
                        width=500, height=350).interactive()
    return chart

def make_plot2(x_axis='US_Gross:Q', y_axis='US_Gross:Q'):

    df = pd.read_csv('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json')

    df["Release_Date"] = pd.to_datetime(df["Release_Date"]) # Converting to datetime format
    df["year"] = df['Release_Date'].dt.year # Creating years column for future use
    df = df.query("year < 2010") # years above 2010 are either mislabeled or the sample size is too small 

    df["International_Gross"] = df["Worldwide_Gross"] - df["US_Gross"]

    df_boxoffice = df[["International_Gross", "year", "US_Gross"]]

    df_boxoffice = df_boxoffice.melt(id_vars = "year",
        var_name = "type",
        value_name = "dollars")


    bo_chart = alt.Chart(df_boxoffice.dropna()).mark_bar().encode(
        alt.Y('dollars:Q', axis=alt.Axis(title='Dollars')),
        alt.X('year:O', axis=alt.Axis(title='Year')),
        color = "type:N"
        ),
    
    # bo_chart = alt.Chart('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json').mark_circle(size=90).encode(
    #             alt.X(x_axis, 
    #             title = x_axis.replace("_", " ")[:-2]),
    #             alt.Y(y_axis,
    #             title = y_axis.replace("_", " ")[:-2]),
    #             tooltip = ['Title:N', 'Director:N']
    #         ).properties(title="asdfsad")

    return bo_chart

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
        ############### Plot 2 ###########
        html.Iframe(
        sandbox='allow-scripts',
        id='plot2',
        height='470',
        width='655',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot2().to_html()
        ################ The magic happens here
        ),
        dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': 'Worldwide Gross', 'value': 'Worldwide_Gross:Q'},
            {'label': 'US DVD Sales', 'value': 'US_DVD_Sales:Q'},
            {'label': 'US Gross', 'value': 'US_Gross:Q'},
            {'label': 'Release Dates', 'value': 'year:O'},

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
        min=1900,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1900, 2010, 5)},
        value=[1977, 1999]),
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
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-y', 'value'),
     dash.dependencies.Input('dd-chart','value')])
def update_plot2(xaxis_column_name,
                yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot2 = make_plot2(xaxis_column_name,
                             yaxis_column_name).to_html()
    return updated_plot2

if __name__ == '__main__':
    app.run_server(debug=True)