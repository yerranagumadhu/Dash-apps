import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Div import Div
import dash_table
import pandas as pd
import pathlib
import plotly.express as px

#import the main app
from app import app

#Create the base path to read the data
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

#Read the data
df_covid = pd.read_excel(DATA_PATH.joinpath("COVID_19.xlsx"))

#I am Intrested only the Countries, Deaths and cases
df_covid_grp = df_covid.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()

#print(df_covid_grp)

#
layout = html.Div([
    html.H3('App 3-To Demonstrate BAR and PIE Charts'),
    html.Div([
                html.Div([dcc.Link('Go to App 1', href='/apps/app1')],className='three columns'),
                html.Div([dcc.Link('Go to App 2', href='/apps/app2')],className='three columns'),
                html.Div([dcc.Link('Go to App 3', href='/apps/app3')],className='three columns'),
                html.Div([dcc.Link('Go to App 4', href='/apps/app4')],className='three columns'),
    
    ],className='row'),
    html.Br(),
    html.Div([
                dash_table.DataTable(
                                        id='datatable_id',
                                        data=df_covid_grp.to_dict('records'),
                                        columns=[
                                            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_covid_grp.columns
                                        ],
                                        editable=False,
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="multi",
                                        row_selectable="multi",
                                        row_deletable=False,
                                        selected_rows=[],
                                        page_action="native",
                                        page_current= 0,
                                        page_size= 6,
   
                                        style_cell_conditional=[
                                            {'if': {'column_id': 'countriesAndTerritories'},
                                                'width': '40%', 'textAlign': 'left'},
                                            {'if': {'column_id': 'deaths'},
                                                'width': '30%', 'textAlign': 'left'},
                                            {'if': {'column_id': 'cases'},
                                                'width': '30%', 'textAlign': 'left'},
                                        ],
                                    ),
            ],className='row'),
    html.Div([
                html.Div([
                    dcc.Dropdown(id='linedropdown',
                        options=[
                                {'label': 'Deaths', 'value': 'deaths'},
                                {'label': 'Cases', 'value': 'cases'}
                        ],
                        value='deaths',
                        multi=False,
                        clearable=False
                    ),
                ],className='six columns'),

                html.Div([
                dcc.Dropdown(id='piedropdown',
                    options=[
                            {'label': 'Deaths', 'value': 'deaths'},
                            {'label': 'Cases', 'value': 'cases'}
                    ],
                    value='cases',
                    multi=False,
                    clearable=False
                ),
                ],className='six columns'),

            ],className='row'),
    html.Div([
                html.Div([
                    dcc.Graph(id='linechart'),
                ],className='six columns'),

                html.Div([
                    dcc.Graph(id='piechart'),
                ],className='six columns'),

            ],className='row')
])

#------------------------------------------------------------------
@app.callback(
    [dash.dependencies.Output('piechart', 'figure'),
     dash.dependencies.Output('linechart', 'figure')],
    [dash.dependencies.Input('datatable_id', 'selected_rows'),
     dash.dependencies.Input('piedropdown', 'value'),
     dash.dependencies.Input('linedropdown', 'value')]
)
def update_data(chosen_rows,piedropval,linedropval):
    if len(chosen_rows)==0:
        df_filterd = df_covid_grp[df_covid_grp['countriesAndTerritories'].isin(['China','Iran','Spain','Italy'])]
    else:
        print(chosen_rows)
        df_filterd = df_covid_grp[df_covid_grp.index.isin(chosen_rows)]

    pie_chart=px.pie(
            data_frame=df_filterd,
            names='countriesAndTerritories',
            values=piedropval,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            )


    #extract list of chosen countries
    list_chosen_countries=df_filterd['countriesAndTerritories'].tolist()
    #filter original df according to chosen countries
    #because original df has all the complete dates
    df_line = df_covid[df_covid['countriesAndTerritories'].isin(list_chosen_countries)]

    line_chart = px.line(
            data_frame=df_line,
            x='dateRep',
            y=linedropval,
            color='countriesAndTerritories',
            labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
            )
    line_chart.update_layout(uirevision='foo')

    return (pie_chart,line_chart)