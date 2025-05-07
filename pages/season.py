import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/season', name='season')

df = pd.read_csv('clean_game_logs/combined_input.csv', header=0)

layout = dbc.Container([
    dbc.Row([
        html.Div('GameChanger Data Visualization Tool', className="text-primary text-center fs-3")
    ]),

    # Buttons to select graph
    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in ['OPS', '2B', 'PA']],
                       value='OPS',
                       inline=True,
                       id='graph_selection')
    ]),

    #horizontal line
    html.Hr(),

    dbc.Row([
        # Table showing all stats
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),
        # Graph
        dbc.Col([
            dcc.Graph(figure={}, id='stat_graph')
        ], width=6),
    ]),

], fluid=True)

# Updating the graph based on the button selected
@callback(
    Output(component_id='stat_graph', component_property='figure'),
    Input(component_id='graph_selection', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='First', y=col_chosen, histfunc='sum')
    return fig