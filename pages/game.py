import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import os

dash.register_page(__name__, path='/game', name='game')

game_dates = ['red_sox_4-26_stats_clean.csv', 
              'red_sox_5-2_stats_clean.csv', 
              'red_sox_5-3_stats_clean.csv']

games_played = len(game_dates) - 1
df = pd.read_csv('clean_game_logs/' + game_dates[-1], header=0)

layout = html.Div([
    html.H2("This is the game page"),
    dcc.Slider(0, games_played,
               step=None,
               marks = {
                   0: '4/26',
                   1: '5/2',
                   games_played: '5/3'
               },
               value=games_played,
               id='chart_selection'
    ),
    html.Div(id='slider-output-container'),

    dbc.Row([
        # Table showing game stats
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'}, id = "overview_table")
        ], width=6),
        
    ]),
])

@callback(
    Output('overview_table', 'data'),
    Output('overview_table', 'columns'),
    Input('chart_selection', 'value')
    )

def update_table(chart_index):
    filepath = os.path.join('clean_game_logs', game_dates[chart_index])
    df = pd.read_csv(filepath, header=0)

    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]