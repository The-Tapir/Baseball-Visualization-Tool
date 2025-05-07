import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import os

dash.register_page(__name__, path='/game', name='game')

game_dates = ['red_sox_3-8_stats_clean.csv',
              'red_sox_3-20_stats_clean.csv',
              'red_sox_3-22_stats_clean.csv',
              'red_sox_3-26_stats_clean.csv',
              'red_sox_3-29_stats_clean.csv',
              'red_sox_3-31_stats_clean.csv',
              'red_sox_4-7_stats_clean.csv',
              'red_sox_4-22_stats_clean.csv',
              'red_sox_4-26_stats_clean.csv', 
              'red_sox_5-2_stats_clean.csv', 
              'red_sox_5-3_stats_clean.csv']

games_played = len(game_dates) - 1
df = pd.read_csv('clean_game_logs/' + game_dates[-1], header=0)
# Top 5 players by AVG
leader_df = df.sort_values(by='AVG', ascending=False).head(5)

layout = html.Div([
    html.H2("This is the game page"),
    # Slider with all of the dates of games
    dcc.Slider(0, games_played,
               step=None,
               marks = {
                   0: '3/8',
                   1: '3/20',
                   2: '3/22',
                   3: '3/26',
                   4: '3/29',
                   5: '3/31',
                   6: '4/7',
                   7: '4/22',
                   8: '4/26',
                   9: '5/2',
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
        # Drop down menu to chose which stat leader(s) to show
        dbc.Col([
            dcc.Dropdown(
                id='leader_metric',
                options=[{'label': col, 'value': col} for col in ['H', '2B', 'RBI', 'BB']],
                value='H'),
        # Table showing leaders in chosen stat from dropdown
        dash_table.DataTable(
        id='leaders_table',
        data=leader_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in leader_df.columns],
        style_table={'overflowX': 'auto'},
        page_size=5,
        )
    
        ], width = 6),    

    ]),
])

# Updating which .csv file to read from based on the slider with the dates
@callback(
    Output('overview_table', 'data'),
    Output('overview_table', 'columns'),
    Input('chart_selection', 'value')
    )
def update_table(chart_index):
    filepath = os.path.join('clean_game_logs', game_dates[chart_index])
    df = pd.read_csv(filepath, header=0)

    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

# Updating the leader chart based on the dropdown option chosen
@callback(
    Output('leaders_table', 'data'),
    Output('leaders_table', 'columns'),
    Output('leaders_table', 'style_cell_conditional'),
    Input('leader_metric', 'value'),
    Input('chart_selection', 'value')  # if reading from different games
)
def update_leaders(metric, game_index):
    df = pd.read_csv('clean_game_logs/' + game_dates[game_index])

    # Sort descending, get top 5
    leader_df = df.sort_values(by=metric, ascending=False).head(5)[['First', 'Last', metric]]
    columns = [{"name": i, "id": i} for i in leader_df.columns]
    
    data = leader_df.to_dict('records')
    
    style = [
        {'if': {'column_id': 'First'}, 'width': '100px', 'textAlign': 'center'},
        {'if': {'column_id': 'Last'}, 'width': '100px', 'textAlign': 'center'},
        {'if': {'column_id': metric}, 'width': '100px', 'textAlign': 'center'}     
    ]

    return data, columns, style