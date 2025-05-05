import dash
from dash import html
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.CERULEAN]

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    #html.H1("Red Sox Data Visual"),
    html.Div([
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Season", href="/season", active="exact"),
            dbc.NavLink("Game", href="/game", active="exact"),
        ], pills=True),
    ], className="mb-4"),
    dash.page_container  # This renders the current page
])

if __name__ == '__main__':
    app.run(debug=True)