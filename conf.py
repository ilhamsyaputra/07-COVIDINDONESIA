import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    'Portal Informasi COVID-19 Indonesia',
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{
        "name": "viewport",
        'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
        }]
    )
server = app.server