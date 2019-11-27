import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

def make_plot():

    # Create a plot of the movies dataset
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

    chart = alt.Chart(vega_datasets.data.movies.url).mark_point(size=90).encode(
                alt.X('Release_Date:O', title = 'Release Date'),
                alt.Y('US_Gross:Q', title = 'US Gross ($)'),
                tooltip = ['Title:N', 'US_Gross:Q']
            ).properties(title='Movies',
                        width=500, height=350).interactive()

    return chart


app.layout = html.Div([

### ADD CONTENT HERE like: html.H1('text'),
    html.H1('Welcome to the Movie Dashboard'),

    ### ADD CONTENT HERE like: html.H1('text'),

    ### Let's now add an iframe to bring in HTML content

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='470',
        width='655',
        style={'border-width': '1px'},

        ################ The magic happens here
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
    dcc.Markdown('''
    
    ### Here is a markdown cell
    ![](https://media.wired.com/photos/5b7350e75fc74d47846ce4e4/master/pass/Popcorn-869302844.jpg, width="10%")

    #### Choose a genre from the dropdown box below
    

    '''),

    dcc.Dropdown(
        options=[
            {'label': 'Action', 'value': 'Action'},
            {'label': 'Adventure', 'value': 'Adventure'},
            {'label': 'Children', 'value': 'Children'},
            {'label': 'History', 'value': 'History'}
        ],
    placeholder="Please choose a genre",
     
    style=dict(width='85%')),
    
    dcc.Markdown('''
    
    ## This is a slider
    '''),

    dcc.Slider(
        min=1900,
        max=2000,
        marks={i: '{}'.format(i) for i in range(1900, 2000, 5)},
        value=1977
    ),

    dcc.Markdown('''
    
    ### This is a range slider
     
    '''),

    dcc.RangeSlider(
    count=1,
    min=-5,
    max=10,
    step=0.5,
    value=[-3, 7]
),

    dcc.Markdown('''
    
    |

    |
    
    |

    |

    |

    |

    |

    |

    |

    |

    |
    
    ''')
])

if __name__ == '__main__':
    app.run_server(debug=True)