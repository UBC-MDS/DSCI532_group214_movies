import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import vega_datasets
app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Dash app with pure Altair HTML'
## Magic happens here
def make_plot(x_axis='US_Gross:Q',
              y_axis='US_Gross:Q', 
              years=[1915, 2010]):
    movies = alt.UrlData(data.movies.url,
    format=alt.DataFormat(parse={"Release_Date":"date"}))
    # Attribution: https://altair-viz.github.io/gallery/multiple_interactions.html
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # Add theme here
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
    chart = alt.Chart(movies).mark_circle(size=90).transform_calculate(
        Release_Year="year(datum.Release_Date)"
        ).transform_filter(
            filter="datum.Release_Year>{} & datum.Release_Year<{}".format(years[0], years[1])
        ).encode(
                alt.X(x_axis, 
                title = x_axis.replace("_", " ")[:-2]),
                alt.Y(y_axis,
                title = y_axis.replace("_", " ")[:-2]),
                tooltip = ['Title:N', 'Director:N']
            ).properties(title=x_axis[:-2].replace("_", " ") + " vs. " + y_axis[:-2].replace("_", " "),
                        width=500, height=350).interactive()
    return chart

def make_plot2(x_axis='US_Gross:Q',
              y_axis='US_Gross:Q'):
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # Add theme here
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }
    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)
    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default
    movies = alt.UrlData(data.movies.url,
    format=alt.DataFormat(parse={"Release_Date":"date"})
    
    # Attribution: https://altair-viz.github.io/gallery/multiple_interactions.html
)

    chart = alt.Chart(movies).mark_circle(size=90).transform_calculate(
        Release_Year="year(datum.Release_Date)"
        ).encode(
                alt.X(x_axis, 
                title = x_axis.replace("_", " ")[:-2]),
                alt.Y(y_axis,
                title = y_axis.replace("_", " ")[:-2]),
                tooltip = ['Title:N', 'Director:N']
            ).properties(title=x_axis[:-2].replace("_", " ") + " vs. " + y_axis[:-2].replace("_", " "),
                        width=500, height=350).interactive()
    return chart

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
            {'label': 'Release Dates', 'value': 'Release_Year:O'},

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
        id='year-slider',
        min=1900,
        max=2010,
        marks={i: '{}'.format(i) for i in range(1900, 2010, 5)},
        value=[1977, 1999]),
])


@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value'),
     dash.dependencies.Input('dd-chart-y','value'),
     dash.dependencies.Input('year-slider', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name,
                year_filter):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,
                             yaxis_column_name,
                             year_filter).to_html()
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