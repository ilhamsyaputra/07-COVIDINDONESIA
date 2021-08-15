import dash_html_components as html
import layout
import process_prov

from conf import app
from conf import server


app.title = 'Portal Informasi COVID-19 Indonesia'

app.layout = html.Div([
    html.H1('Portal Informasi COVID-19 Indonesia'),
    layout.tanggal,
    html.Hr(),
    layout.section1,
    layout.section2,
    layout.section3,
    process_prov.section4

], style={'margin-top': '1%', 'margin-bottom': '1%', 'margin-left': '10%', 'margin-right': '10%'})


if __name__ == '__main__':
    app.run_server(debug=True)