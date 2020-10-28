import dash
import dash_table
import pandas as pd
import pathlib
import requests
import dash_html_components as html
import dash_core_components as dcc
import time


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("hospital_beds_USA_v1.csv"))

categories=["observation_time","temperature","wind_speed","precip","humidity",
            "cloudcover","feelslike","uv_index","visibility"]

# Read the ZIP code CSV file 

df_zip = pd.read_csv(DATA_PATH.joinpath("uszips.csv"),dtype={'zip':'string'})
#"zip","city","state_name"
df_zip = df_zip[["zip","city","state_name"]]
#print(df_zip)

#newdf = df_zip[(df_zip.city == 'Adjuntas') & (df_zip.state_name == 'Puerto Rico')]['zip']

#print(df_zip.dtypes)
#print(newdf)

st_name   = sorted(df_zip['state_name'].unique())
citi_name = sorted(df_zip['city'].unique())

def update_weather(citi,st):

    if citi or st:
        newdf_zip = min(df_zip[(df_zip.city == citi) & (df_zip.state_name == st)]['zip'])
    else:
        newdf_zip = '00601'
    # newdf_zip = df_zip[(df_zip.city == citi) & (df_zip.state_name == st)]['zip']

    print(newdf_zip)
    # print(df_zip[(df_zip.city == citi) & (df_zip.state_name == st)])
    
    params = {
    'access_key': 'e214c8b16f3a24174e4f5120113f4a04',
    'query': newdf_zip
    }

    weather_requests = requests.get('http://api.weatherstack.com/current', params)
    json_data = weather_requests.json()
    df = pd.DataFrame(json_data)
    # print(df)
    # print(df['current'][categories])
    #print (df.columns)
    #print (df[:20])
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




df_int = pd.read_csv(DATA_PATH.joinpath("internet_cleaned.csv"))

int_year = sorted(df_int['year'].unique())
#print(int_year)

def internet_clean(year_filter):
    df_int_filter = df_int[df_int['year']==year_filter]
    
    return [ 
                dash_table.DataTable(
                                id='int_table',
                                columns=[{"name": i, "id": i, "selectable": True,"hideable":True} for i  in df_int_filter.columns if i not in 'year'],
                                data=df_int_filter.to_dict('records'),
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                column_selectable="multi",
                                row_selectable="multi",
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                export_format="csv",
                                export_columns="visible",
                                editable=True
                            )
            ]
#{'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2020-10-24 18:59', 'localtime_epoch': 1603565940, 'utc_offset': '-4.0'}, 'current': {'observation_time': '10:59 PM', 'temperature': 17, 'weather_code': 122, 'weather_icons': ['https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'], 'weather_descriptions': ['Overcast'], 'wind_speed': 15, 'wind_degree': 290, 'wind_dir': 'WNW', 'pressure': 1015, 'precip': 0.1, 'humidity': 53, 'cloudcover': 100, 'feelslike': 17, 'uv_index': 4, 'visibility': 16, 'is_day': 'yes'}}


#Dash app entry point
app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
            dcc.Location(id="url", refresh=False), html.Div(id="page-content")
        ]),

    html.Div([    
         dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i, "selectable": True,"hideable":True} for i in df.columns],
                                data=df.to_dict('records'),
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                column_selectable="multi",
                                row_selectable="multi",
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                export_format="csv",
                                export_columns="visible",
                                editable=True
                            ),
        dcc.Dropdown(
                        id='demo-dropdown',
                        options=[ {'label':i, 'value': i}  for i in int_year],
                        value=2010
                    ),
        html.Br(),
        html.Div(id='dd-output-container')

    ]),
    html.Br(),
    html.Div([
            dcc.Interval(
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
    ])




@app.callback(
    dash.dependencies.Output('city', 'options'),
    [dash.dependencies.Input('state_name', 'value')]
)
def update_dropdown(st):
    k = sorted(df_zip[df_zip.state_name == st]['city'].unique())    
    #print(k)
    return [ {'label':i, 'value': i}  for i in k]


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


# Retrun the function
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return internet_clean(value) #'You have selected "{}"'.format(value)
 


if __name__ == '__main__':
    app.run_server(debug=True)