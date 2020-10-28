import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import pathlib

#import the main app
from app import app


#Create the base path to read the data
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("hospital_beds_USA_v1.csv"))

#This will be used on the Filter the data 
df['id'] = df['state']
df.set_index('id', inplace=True, drop=False)

df = df.drop(columns='source_url')
df_agg = df.groupby(['state','county','year'], as_index=False)[['population']].sum()
#print(df_agg)


#Created the function to return the Modal table data based on the selected cell 

def agg_state_data(state):
    print('Inside the function agg_state_data: ',state)
    df_agg_filter = df_agg[df_agg['state']==state]
    #print(df_agg_filter)
    return [ 
                dash_table.DataTable(
                                id='int_table',
                                columns=[{"name": i, "id": i, "selectable": True,"hideable":True} for i  in df_agg_filter.columns],
                                data=df_agg_filter.to_dict('records'),
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



layout = html.Div(
    [
        html.H3('App 4-To Demonstrate Modal Box'),
        html.Div([
                html.Div([dcc.Link('Go to App 1', href='/apps/app1')],className='three columns'),
                html.Div([dcc.Link('Go to App 2', href='/apps/app2')],className='three columns'),
                html.Div([dcc.Link('Go to App 3', href='/apps/app3')],className='three columns'),
                html.Div([dcc.Link('Go to App 4', href='/apps/app4')],className='three columns'),
    
                ],className='row'),
        html.Br(),
        dbc.Button("Open modal", id="open"),
        dbc.Modal(
                        [
                            dbc.ModalHeader("Header"),
                            dbc.ModalBody(
                                html.Div(id='modal_table')
                            ),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="close", className="ml-auto")
                            ),
                        ],
            id="modal",
            size="lg",
            scrollable=True,
        ),
        html.Div([
                dash_table.DataTable(
                                        id='selecttable_id',
                                        data=df.to_dict('records'),
                                        columns=[
                                            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns if i != 'id'
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
                                        selected_cells=[],
                                        derived_virtual_selected_rows=[],
   
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
        html.Br()        
    ]
)


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output('modal_table', 'children'),
              [Input('selecttable_id', 'active_cell')],
              [
               State('selecttable_id', 'data'),
               State('selecttable_id','selected_cells'),
               State('selecttable_id','derived_virtual_selected_row_ids'),
               State('selecttable_id','selected_row_ids')
              ])
def get_active_letter(active_cell,data,sele_cell,dvsri,sri):
    #print(active_cell)
    #print(sele_cell)
    #print(dvsri)
    #print(sri)
    #print(active_cell['row_id'])
    #print(data[active_cell['row']][active_cell['column_id']])
    #print(pd.DataFrame(data).iat[active_cell['row'], active_cell['column']])
    #k = data[active_cell['row']][active_cell['column_id']]
    state = active_cell['row_id']
    return agg_state_data(state)