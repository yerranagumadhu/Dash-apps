import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import dash_table
import pandas as pd
import pathlib


'''
Added this since we are using the Dash with Flask Combination!!
'''
app = dash.Dash(
    __name__,
    requests_pathname_prefix='/app2/'
)

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

df_int = pd.read_csv(DATA_PATH.joinpath("internet_cleaned.csv"))

int_year = sorted(df_int['year'].unique())

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

app.layout = html.Div([
    html.H3('App 2-To Demonstrate Table Features'),    
    html.Div([
                html.Div([html.A("Go to App 1", href='/app1/')],className='three columns'),
                html.Div([html.A("Go to App 2", href='/app2/')],className='three columns'),
                html.Div([html.A("Go to App 3", href='/app3/')],className='three columns'),
                html.Div([html.A("Go to App 4", href='/app4/')],className='three columns'),
    
    ],className='row'),
    html.Br(),
    html.Div([  
    html.Div([
            dcc.Dropdown(
                    id='demo-dropdown',
                    options=[ {'label':i, 'value': i}  for i in int_year],
                    value=2010
                ),

    ],style={'width': '40%'}),          

    html.Br(),
    html.Div(id='dd-output-container')

]),
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return internet_clean(value)