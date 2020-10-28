import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import dash_table
import pandas as pd
import pathlib
import requests


'''
Added this since we are using the Dash with Flask Combination!!
'''
app = dash.Dash(
    __name__,
    requests_pathname_prefix='/app1/'
)

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read the ZIP code CSV file 
df_zip = pd.read_csv(DATA_PATH.joinpath("uszips.csv"),dtype={'zip':'string'})

#Keep only the Required Columns "zip","city","state_name"
df_zip = df_zip[["zip","city","state_name"]]

#Select the list of disitnct State names and City names
st_name   = sorted(df_zip['state_name'].unique())
citi_name = sorted(df_zip['city'].unique())

# we are intreseted in only the Following Categories from the weather API
categories=["observation_time","temperature","wind_speed","precip","humidity",
            "cloudcover","feelslike","uv_index","visibility"]


#Create a function to call the Weather API depending upon the City and State
def update_weather(citi,st):

    if citi or st:
        newdf_zip = min(df_zip[(df_zip.city == citi) & (df_zip.state_name == st)]['zip'])
    else:
        newdf_zip = '00601'


    params = {
    'access_key': 'e214c8b16f3a24174e4f5120113f4a04',
    'query': newdf_zip
    }

    weather_requests = requests.get('http://api.weatherstack.com/current', params)
    json_data = weather_requests.json()
    df = pd.DataFrame(json_data)
    return([
            html.Table(
                className='table-weather',
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    name+": "+str(data)
                                ]
                            )
                        ]
                    )
            for name,data in zip(categories,df['current'][categories])
        ])
    ])


def return_weather_api(app):
       return   html.Div(
                            [
                                    dcc.Interval  (
                                                    id='my_interval',
                                                    disabled=False,     #if True the counter will no longer update
                                                    n_intervals=0,      #number of times the interval has passed
                                                    interval=300*1000,  #increment the counter n_intervals every 5 minutes
                                                    max_intervals=100,  #number of times the interval will be fired.
                                                                        #if -1, then the interval has no limit (the default)
                                                                        #and if 0 then the interval stops running.
                                                 ),    
                                    html.Div(
                                            [html.H3("Weather API")],
                                            className="seven columns main-title",
                                        ),  
                                    html.Br(),    
                                    html.Div([
                                        dcc.Dropdown(
                                                        id='state_name',
                                                        options=[ {'label':st, 'value': st}  for st in st_name],
                                                        value="Puerto Rico"
                                                    ),
                                        dcc.Dropdown(
                                                        id='city',
                                                        #options=[ {'label':i, 'value': i}  for i in citi_name],
                                                        value="Adjuntas"
                                                    ),
                                        html.Button('Click Me', id='button', n_clicks=0)

                                    ],
                                    className="search_box",
                                    id="multi_drop_down",
                                    style={'width': '40%'}
                                    ),
                                    html.Br(),
                                    html.Div(id="weather")
    ])



app.layout = html.Div([
    html.H3('App 1-To Demonstrate API Calls'),
    html.Div([
                html.Div([html.A("Go to App 1", href='/app1/')],className='three columns'),
                html.Div([html.A("Go to App 2", href='/app2/')],className='three columns'),
                html.Div([html.A("Go to App 3", href='/app3/')],className='three columns'),
                html.Div([html.A("Go to App 4", href='/app4/')],className='three columns'),
    
    ],className='row'),
    html.Br(),    
    html.Div([
        dcc.Dropdown(
                        id='state_name',
                        options=[ {'label':st, 'value': st}  for st in st_name],
                        value="Puerto Rico"
                    ),
        dcc.Dropdown(
                        id='city',
                        #options=[ {'label':i, 'value': i}  for i in citi_name],
                        value="Adjuntas"
                    ),
        html.Button('Click Me', id='button', n_clicks=0)

    ],
    className="search_box",
    id="multi_drop_down",
    style={'width': '30%'}
    ),
    html.Br(),
    html.Div(id="weather")
])

@app.callback(
dash.dependencies.Output('weather', 'children'),
[
    dash.dependencies.Input('button', 'n_clicks')
],
[
    
    dash.dependencies.State('state_name', 'value'),
    dash.dependencies.State('city', 'value')
]    
)
def update_temp(n_clicks,state_name,city):
    #time.sleep(2)
    print(state_name,city,n_clicks)
    if n_clicks >= 1:        
        return update_weather(city,state_name)
    else: 
        return update_weather('Adjuntas','Puerto Rico')


@app.callback(
    dash.dependencies.Output('city', 'options'),
    [dash.dependencies.Input('state_name', 'value')]
)
def update_dropdown(st):
    k = sorted(df_zip[df_zip.state_name == st]['city'].unique())    
    #print(k)
    return [ {'label':i, 'value': i}  for i in k]