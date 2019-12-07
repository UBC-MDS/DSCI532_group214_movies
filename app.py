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

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Interactive Movie Database'

df = pd.read_json('https://raw.githubusercontent.com/vega/vega-datasets/master/data/movies.json', orient = 'columns')
df['Release_Date'] =  pd.to_datetime(df['Release_Date'], infer_datetime_format=True)
df['Release_Date'] = df['Release_Date'].dt.year

def make_areachart(
              year_slider = [1950, 2000],
              genre = "Comedy"):
    '''
    Takes in a year range and genre and filters with the criteria 
    to create our Altair figure

    An area chart of box office of movies of selected genre in selected year range
    with domestic and international data
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A area chart Altair object      
    
    '''

    df = alt.UrlData(
        data.movies.url
        )


    areachart = alt.Chart(df).mark_area().transform_calculate(
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
        color = alt.Color("key:N", legend=alt.Legend(orient="bottom"), scale = alt.Scale(scheme='yelloworangebrown'))
    ).properties(
        title = "Average Gross",
        height = 300,
        width = 300
    )

    return areachart


def make_heatmap(
              year_slider = [1950, 2000],
              genre = "Comedy"):

    '''
    Takes in a year range and genre and filters with the criteria 
    to create our Altair figure

    A heatmap of box office profit ratio against IMDb ratings
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A heatmap Altair object      
    
    '''

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
        alt.X('IMDB_Rating:Q', bin = alt.Bin(maxbins = 20), axis = alt.Axis(title = 'IMDB Rating')),
        alt.Y('Profit_Ratio:Q', bin = alt.Bin(maxbins = 20), axis = alt.Axis(title = 'Profit Ratio ((Gross - Budget)/Budget)')),
        alt.Color('mean(Profit_Ratio):Q', scale=alt.Scale(scheme='yelloworangebrown'), legend=alt.Legend(orient="bottom")),
        tooltip = ['Title:N']
    ).properties(
        title = "Profit Ratio against IMDb Ratings",
        height = 300,
        width = 300
    )

    return heatmap

def make_highlight_hist(year_slider = [1950, 2000],
                genre = "Comedy"):
    '''
    Takes in a year range and genre and filters with the criteria 
    to create our Altair figure

    A highlighted histogram of counts of movies of different genres
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A histogram Altair object      
    
    '''

    df = alt.UrlData(
        data.movies.url
        )

    genre_hist = alt.Chart(df).mark_bar(
    ).transform_calculate(
        Release_Year = "year(datum.Release_Date)",
        International_Gross = "datum.Worldwide_Gross - datum.US_Gross"
    ).transform_filter(
        alt.datum.Release_Year <= year_slider[1]
    ).transform_filter(
        alt.datum.Major_Genre != None
    ).transform_filter(
        alt.datum.Release_Year >= year_slider[0]
    ).encode(
        alt.Y('Major_Genre:N', 
            axis=alt.Axis(title='Genre')),
        alt.X('count()'),
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
            [ dbc.Row([html.Img(src='https://i.imgur.com/N2UOAry.jpg',
                       width='200px'),
                html.H2("Interactive Movie Dashboard", className="display-3")]
        )]
        )
    ]
)

    
    
content = dbc.Container(
    [dbc.Row([                                      ## Top row with filters
        dbc.Col([                                   ## Column containing the two mini-rows in the top row
                
                          
        dbc.Row([                                   ## Row for the range slider
            dbc.Col([                               ## Column for the range slider
        dcc.RangeSlider(
            id='year_slider',
            min=1930,
            max=2010,
            marks={i: '{}'.format(i) for i in range(1930, 2010, 5)},
            value=[1950, 2000]
                    ),
        html.Div("\n\n")
        
            ], width=12,
            style={'white-space':'pre-line'})       ## Allows use of newline character (\n)
            ]),

        dbc.Row(                                    ## Row with dropdown filter

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
        value='Action',
        clearable=False,
        style={'width':'100%', 'justify':'start'}
                )
            ),
                ] 
            ),
        ]),
        dbc.Row([                                   ## Second (main) row  with all graphs
            dbc.Col(                                ## First column with barchart and heatmap
                [dbc.Row([                          ## Row with barchart
        
        html.Iframe(
            sandbox='allow-scripts',
            id='areachart',
            height=450,
            width=575,
            style={'border-width': '0'},
            srcDoc=make_areachart().to_html()
                )
                        ]),

                dbc.Row([                           ## Row with heatmap
        
        html.Iframe(
            sandbox='allow-scripts',
            id='heatmap',
            height=450,
            width=550,
            style={'border-width': '0'},
            srcDoc=make_heatmap().to_html()
                    ) 
                        ])
                ], width=6      
            ),                                      ## End column1

        dbc.Col(                                    ## Col with hist and summary stats
             [
            dbc.Row(                                ## Row with highlighted histogram
            html.Iframe(
            sandbox='allow-scripts',
            id='plot3',
            height=450,
            width=500,
            style={'border-width': '0'},
            srcDoc=make_highlight_hist().to_html()
                )
            ),

        dbc.Row([                               ## Row with summary stats
            dbc.Col([
            dbc.Row([html.Div(html.H3("Summary"))]),
			dbc.Row([html.Div(id = "text1")]),
			#dbc.Row([html.Div("\n\n\n")]),
			dbc.Row([html.Div(id = "text2")]),
			#dbc.Row([html.Div("______________________________________________________  ")]),
			dbc.Row([html.Div(id = "text3")]),
			#dbc.Row([html.Div("______________________________________________________  ")]),
			dbc.Row([html.Div(id = "text4")])
            ]),
             ], justify='left')
			
             ], width=6,
                style={'white-space':'pre-line', 'font-family':'impact'},
                
                
                )       ## End summary stats row
                                               ## End column2 of main body
            ],                               ## End second main row
        )
    ]
)                                               ## End container

    

       
footer = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.P('This Dash app was made collaboratively by Team 214: Vignesh Chandrasekaran, James Huang, and Matthew Connell')
            )
        ),
    ])
        

tab1_content=([
        html.Div([
        content,
        footer])
    ])

tab2_content=([
        dbc.Row([
                dbc.Col([
            html.Div(html.H3("Who should use this app?")),
            html.Div("If you are nascent to investing in the movie industry, your search ends right here! As a new investor, there are several fundamental questions you would like answered:"),
            html.Div("1. What genre has been most profitable?"),
            html.Div("2. How much does audience reception affect profit?  "),
            html.Div("3. What are the popularity levels of genres that typically produced? "),
            html.Div(html.H3("How to use this app:")),
            html.Div("1. Use the slider to observe the performance of the industry over the selected years."),
            html.Div("2. Use the drop down menu to filter on genre"),
            html.Div(
                dcc.Markdown('''
            [Data Source](https://github.com/vega/vega-datasets/blob/master/data/movies.json)
                        
            [Github Repo for this app](https://github.com/UBC-MDS/DSCI532_group214_movies)

            '''
                )
            )
                ],
              
             width=6,
             style={'justify': 'center', 'font-family':'helvetica', 'white-space':'pre-line'}),
        ], justify='center')
    ])



tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label = "Graphs"),
    dbc.Tab(tab2_content, label="Documentation"),
    ])

app.layout=html.Div([jumbotron,
            tabs])

@app.callback(
    dash.dependencies.Output('areachart', 'srcDoc'),
    [
     dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])
def update_areachart(
                year_slider,
                genre_choice):
    '''
    Takes in a year range and genre and calls make_plot to update our Altair figure
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A areachart html object      
    
    '''
    updated_plot = make_areachart(
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
    Takes in a year range and genre and calls make_plot to update our Altair figure
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A heatmap html object      
    
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
    Takes in a year range and genre and calls make_plot to update our Altair figure
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information
                    'Drama', 'Any'
    
    Returns
        A histogram html object      
    
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
    ''''This function returns the greatest box office from the movies dataset based on filtering inputs, 
        formatted to help create an info table
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information from the callback above
                    'Drama', 'Any'
    Returns
        A specifically formatted string
          
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = (k[(k['Release_Date'] >= year_info[0]) & (k['Release_Date'] <= year_info[1]) ]
     .sort_values(by = "Worldwide_Gross",ascending = False))
    k_WW_Gross = k.iloc[0].loc['Worldwide_Gross']/1000000
    k_movie = k.iloc[0].loc['Title']
    return (" ======== " + genre_input + " Movies from " + str(year_info[0]) + ' to ' + str(year_info[1])  + " ======== \nTop Grossing Film: " + k_movie + "\nBox Office returns: $" + str(round(k_WW_Gross, 2)) + "M")


@app.callback(
     dash.dependencies.Output('text2', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def biggest_flop(year_info, genre_input):
    '''''This function returns the biggest box office flop from the movies dataset based on filtering inputs, 
        formatted to help create an info table
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information from the callback above
                    'Drama', 'Any'
    Returns
        A specifically formatted string
          
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = (k[(k['Release_Date'] >= year_info[0]) & (k['Release_Date'] <= year_info[1]) ])
    k['Profit'] = k['Worldwide_Gross'] - k['Production_Budget']
    k = k.sort_values(by = "Profit")
    topflopgross = k.iloc[0].loc["Worldwide_Gross"] / 1000000
    topflopgross = round(topflopgross, 2)
    topflopname = k.iloc[0].loc["Title"]
    topflopbudget = k.iloc[0].loc["Production_Budget"] / 1000000
    return (" ============== Biggest flop ============== " + "\nTitle: " + topflopname + "\nBox Office: $" + str(topflopgross) + "M\nBudget: $" + str(topflopbudget) + "M")

@app.callback(
     dash.dependencies.Output('text3', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def how_big(year_info, genre_input):
    ''''This function returns the total box office from the movies dataset based on filtering inputs, 
        formatted to help create an info table
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information from the callback above
                    'Drama', 'Any'
    Returns
        A specifically formatted string
          
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = k[(k['Release_Date'] > year_info[0]) & (k['Release_Date'] < year_info[1]) ]
    average_returns = round(np.sum(k['Worldwide_Gross'] - k['Production_Budget'])/1000000000,2)
    return ("=========== Total =========== " + "\nWorldwide box office: $" + str(average_returns) + "B" )

@app.callback(
     dash.dependencies.Output('text4', 'children'),
     [dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('genre_choice','value')])  

def average_returns(year_info, genre_input):
    ''''This function returns average total box office from the movies dataset based on filtering inputs, 
        formatted to help create an info table
    
    Inputs :
        year_info : List with 2 values, takes in the year information from the callback above
                    [1970,1985]
        genre_input : (To be programmed) : takes in the genre information from the callback above
                    'Drama', 'Any'
    Returns
        A specifically formatted string
          
    
    '''
    #Condition to wrangle based on 'Any' genre
    if genre_input != 'Any': 
        k = df[df['Major_Genre'] == genre_input]
    
    #Condition to have data between those years
    k = k[(k['Release_Date'] > year_info[0]) & (k['Release_Date'] < year_info[1]) ]
    average_returns = round(np.mean(k['Worldwide_Gross'] - k['Production_Budget'])/1000000,2)
    return ("Average return on investment: $" + str(average_returns) + "M" )


# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('year_slider', 'value')])
# # def update_output(value):
#      return "You have selected movies from " + str(value[0]) + ' to ' + str(value[1])


if __name__ == '__main__':
    app.run_server(debug=True)
