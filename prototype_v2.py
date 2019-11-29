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

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Interactive Movie Database'

df = pd.read_json('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json', orient = 'columns')
df['Release_Date'] =  pd.to_datetime(df['Release_Date'], infer_datetime_format=True)
df['Release_Date'] = df['Release_Date'].dt.year


def make_barchart(
    # x_axis='US_Gross:Q',
            #   y_axis='US_Gross:Q',
              year_slider = [1950, 2000],
              genre = "Comedy"):

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
    ).transform_filter(
        alt.datum.Major_Genre == genre
    ).transform_fold(
        ['International_Gross', 'US_Gross'],
    ).encode(
        alt.Y('value:Q', aggregate = "mean", axis=alt.Axis(title='Dollars')),
        alt.X('Release_Year:O', axis=alt.Axis(title='Year')),
        color = alt.Color("key:N", legend=alt.Legend(orient="bottom"))
    ).properties(
        title = "Average Gross",
        height = 300,
        width = 300
    )

    return barchart


def make_heatmap(
    # x_axis='US_Gross:Q',
            #   y_axis='US_Gross:Q',
              year_slider = [1950, 2000],
              genre = "Comedy"):

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
    ).transform_filter(
        alt.datum.Major_Genre == genre
    ).encode(
        alt.X('IMDB_Rating:Q', bin = alt.Bin(maxbins = 50), axis = alt.Axis(title = 'IMDB Rating')),
        alt.Y('Profit_Ratio:Q', bin = alt.Bin(maxbins = 50), axis = alt.Axis(title = 'Profit Ratio ((Gross - Budget)/Budget)')),
        alt.Color('count(Profit_Ratio):Q', scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(orient="bottom"))
    ).properties(
        title = "Average Gross",
        height = 300,
        width = 300
    )

    return heatmap

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
       width=300, 
       height=300
    )

    return genre_hist

jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                 html.Img(src='https://i.imgur.com/36p2VrM.jpg', 
                       width='100px'),
                html.H1("Movies! Movies! Movies!", className="display-3"),
                html.P(
                    "Welcome to the movies dashboard",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)



    ### ADD CONTENT HERE like: html.H1('text'),
    # html.H1('Interactive Movie Database'),
    # html.H3('Box Office Performance Based on Genre'),
    # html.H3('Here is our first plot:'),
    
    
content = dbc.Container(
    [
        dbc.Row([       ## Main row with 3 columns
            dbc.Row(    ## Top row with filters
                    [
                    #dbc.Row([   ## First row of first column, contains dropdown
            dbc.Col([
        dcc.Dropdown(
        id='genre_choice',
        options=[
            {'label': 'Action', 'value': 'Action'},
            {'label': 'Adventure', 'value': 'Adventure'},
            {'label': 'Black Comedy', 'value': 'Black Comedy'},
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
        clearable=False,
        style={'width':'100%', 'justify':'start'}
        ),
            
                                      ## End column1 row1
        #dbc.Row(                        ## Second row of left-most column, contains year slider

        dcc.RangeSlider(
            id='year_slider',
            min=1930,
            max=2010,
            marks={i: '{}'.format(i) for i in range(1930, 2010, 20)},
            value=[1950, 2000]
        )
        
            ], width=12
            )
            
                    ]
                    
            
            ),
        #)
         #             )              ## End column1, row2
        #], 
        #,    ## End of first column

        dbc.Row([                       ## Second (main) row  with all graphs
            dbc.Col(                      ## First column with barchart and heatmap
                    [
                        dbc.Row([           ## Row with barchart
        
        html.Iframe(
            sandbox='allow-scripts',
            id='barchart',
            height=450,
            width=575,
            style={'border-width': '0'},
            srcDoc=make_barchart().to_html()
            )
            ]
            ),

                        dbc.Row([       ## Row with heatmap
        
        html.Iframe(
            sandbox='allow-scripts',
            id='heatmap',
            height=450,
            width=550,
            style={'border-width': '0'},
            srcDoc=make_heatmap().to_html()
            ) 
            ]
            )
                    ], width=6      
                ),          ## End column1

        
         dbc.Col(               ## Col with hist and summary stats
             [
             dbc.Row([
            html.Iframe(
            sandbox='allow-scripts',
            id='plot3',
            height=450,
            width=450,
            style={'border-width': '0'},
            srcDoc=make_highlight_hist().to_html()
            )
            ]), ## end row

            dbc.Col([

            dbc.Row([html.Div("______________________________________________________")]),
			dbc.Row([html.Div(id = "text1")]),
			dbc.Row([html.Div("______________________________________________________")]),
			dbc.Row([html.Div(id = "text2")]),
			dbc.Row([html.Div("______________________________________________________  ")]),
			dbc.Row([html.Div(id = "text3")]),
			dbc.Row([html.Div("______________________________________________________  ")]),
			dbc.Row([html.Div(id = "text4")]),

			])



             ], width=6     
             )              ## End column2
            ]               ## End second row
    )
        ]
        )
    ]
)                           ## End container



       
footer = dbc.Container([dbc.Row(dbc.Col(html.P('This Dash app was made collaboratively by Team 214: Vignesh, James, and Matt'))),
         ])
        
        
app.layout = html.Div([jumbotron,
                       content,
                       footer])

@app.callback(
    dash.dependencies.Output('barchart', 'srcDoc'),
    [
     dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])
def update_barchart(
                year_slider,
                genre_choice):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_barchart(
                             year_slider,
                             genre_choice).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('heatmap', 'srcDoc'),
    [
     dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])
def update_heatmap(
                year_slider,
                genre_choice):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot2 = make_heatmap(
        year_slider,
        genre_choice).to_html()
    return updated_plot2

@app.callback(
    dash.dependencies.Output('plot3', 'srcDoc'),
    [dash.dependencies.Input('year_slider','value'),
    dash.dependencies.Input('genre_choice','value')])    
def update_plot3(year_slider,
                genre_choice):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot3 = make_highlight_hist(year_slider,
                             genre_choice
                             ).to_html()
    return updated_plot3

@app.callback(
     dash.dependencies.Output('text1', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])    
def biggest_success(year_info, genre_input):
    '''This function gives you the highest WW grossing movie and the amount.
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A string (see example)
    
    Example
        'The most succesful movie was Titanic at a worldwide gross of 797.9 Million USD'        
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = (df[(df['Release_Date'] > year_info[0]) & (df['Release_Date'] < year_info[1]) ]
     .sort_values(by = "US_Gross",ascending = False))
    k_WW_Gross = k.iloc[1].loc['Worldwide_Gross']/1000000
    k_movie = k.iloc[0].loc['Title']
    return "The highest worldwide box office of genre type "  + genre_input + " over the years " + str(year_info[0]) + '-' + str(year_info[1])  + " was " + k_movie + " grossing " + str(k_WW_Gross) + " Million USD"


@app.callback(
     dash.dependencies.Output('text2', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def biggest_flop(year_info, genre_input):
    '''This function gives you the biggest flop from the movies dataset.
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information from the callback above
                    'Drama', 'Any'
    Returns
        A string (see example)
    
    Example
        'The biggest worldwide flop was Men of War'
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = (df[(df['Release_Date'] > year_info[0]) & (df['Release_Date'] < year_info[1]) ])
    k['Profit'] = df['Worldwide_Gross'] - df['Production_Budget']
    k = k.sort_values(by = "Profit")
    topflopgross = k.iloc[0].loc["Worldwide_Gross"] / 1000000
    topflopgross = round(topflopgross, 2)
    topflopname = k.iloc[0].loc["Title"]
    topflopbudget = k.iloc[0].loc["Production_Budget"] / 1000000
    b = "The biggest flop of genre type " + genre_input + " over the years " + str(year_info[0]) + '-' + str(year_info[1])  + " was "+topflopname + " with a box office of " + str(topflopgross) + " Million USD against a budget of " + str(topflopbudget) + " Million USD"
    return b

@app.callback(
     dash.dependencies.Output('text3', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def how_big(year_info, genre_input):
    '''This function gives you an estimate of how big the movie industry 
        was in that period for that genre
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A string (see example)
    
    Example
        ''The average return on investment during the period 1970-2000 was 56.73 Million USD'        
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = df[(df['Release_Date'] > year_info[0]) & (df['Release_Date'] < year_info[1]) ]
    average_returns = round(np.sum(k['Worldwide_Gross'] - k['Production_Budget'])/1000000000,2)
    return ("The total worldwide box office of genre type " + genre_input + " over the years " 
            + str(year_info[0]) + '-' + str(year_info[1]) 
            + ' was ' + str(average_returns) + " Billion USD" )

@app.callback(
     dash.dependencies.Output('text4', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def average_returns(year_info, genre_input):
    '''This function gives you the average return on investment during the period.
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A string (see example)
    
    Example
        ''The average return on investment during the period 1970-2000 was 56.73 Million USD'        
    
    '''
    
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = df[(df['Release_Date'] > year_info[0]) & (df['Release_Date'] < year_info[1]) ]
    average_returns = round(np.mean(k['Worldwide_Gross'] - k['Production_Budget'])/1000000,2)
    return ("The average return on investment of genre type " + genre_input + " over the years " 
            + str(year_info[0]) + '-' + str(year_info[1]) 
            + ' was ' + str(average_returns) + " Million USD" )

if __name__ == '__main__':
    app.run_server(debug=True)