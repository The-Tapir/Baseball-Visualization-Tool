import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/team', name='team')

df = pd.read_csv('clean_game_logs/combined_input.csv', header=0)

"""
# Trimming columns to keep and dumping those that we are not using
columns_to_keep = ["Number", "Last", "First", "GP", "PA", "AB", "AVG", "OBP", "OPS", "SLG", "H", "1B", "2B", "3B", "HR", "RBI", "R", "BB", "SO", "HBP", "BB/K", "BABIP", "SF"]
df = df[columns_to_keep]

# Combine duplicate players stats
for col in df.columns[3:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
combined = df.groupby([df.columns[0], df.columns[1], df.columns[2]], as_index=False).sum()

# Recalculating stats that are based on other columns
combined['AVG'] = round(combined['H'] / combined['AB'], 3)
combined['OBP'] = round((combined['H'] + combined['BB'] + combined['HBP']) / (combined['AB'] + combined['BB'] + combined['HBP'] + combined['SF']), 3)
combined['SLG'] = round((combined['1B'] + combined['2B'] * 2 + combined['3B'] * 3 + combined['HR'] * 4) / combined['AB'], 3)
combined['OPS'] = round(combined['OBP'] + combined['SLG'], 3)
combined['BB/K'] = round(combined['BB'] / combined['SO'], 3)
combined['BABIP'] = round((combined['H'] - combined['HR']) / (combined['AB'] - combined['HR'] - combined['SO'] + combined['SF']), 3)

combined.to_csv("combined_input.csv", index = False)
df = pd.read_csv('combined_input.csv')
"""

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

@callback(
    Output(component_id='stat_graph', component_property='figure'),
    Input(component_id='graph_selection', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='First', y=col_chosen, histfunc='avg')
    return fig