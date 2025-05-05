import dash
from dash import html, Dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    #html.H1("Red Sox Data Visual"),
    html.Div([
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Team", href="/team", active="exact"),
            dbc.NavLink("Player", href="/player", active="exact"),
        ], pills=True),
    ], className="mb-4"),
    dash.page_container  # This renders the current page
])

if __name__ == '__main__':
    app.run(debug=True)