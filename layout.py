import process
import process_prov_map

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="RH-COVIDINDONESIA",
    brand_href="#",
    color="dark",
    dark=True,
)

# Footer
footer = html.Div([
    html.Hr(),
    dcc.Markdown('''
    Dataset Source: Our World in Data  
    Code by [M. Ilham Syaputra](https://www.linkedin.com/in/m-ilham-syaputra/)
    '''),
])

# Tanggal update
tanggal = html.Div([
    html.P('Sumber data: data.covid19.go.id | Data per - %s' % (process.tanggal_update))
])

# fungsi card
def card(angka, status, penambahan):
    card_content = [
        dbc.CardBody(
            [
                html.H2(angka, className="card-title"),
                html.H5(status),
                html.P(
                    penambahan,
                    className='card-text',
                ),
            ]
        ),
    ]
    return card_content

# Section 1 card
section1 = html.Div([
    dbc.Row([
        dbc.Col(dbc.Card(
            card(
                process.status_hari('jumlah_positif_kum'), 
                'TERKONFIRMASI',
                '+%s Kasus' % (process.status_hari('jumlah_positif'))
            ), color='primary')),

        dbc.Col(dbc.Card(
            card(
                process.status_hari('jumlah_dirawat_kum'), 
                'KASUS AKTIF',
                '%s Kasus Aktif' % (process.status_hari('jumlah_dirawat'))
            ), 
            color='warning')),

        dbc.Col(dbc.Card(
            card(
                process.status_hari('jumlah_sembuh_kum'), 
                'SEMBUH',
                '+%s Kasus Sembuh' % (process.status_hari('jumlah_sembuh'))
            ), 
            color='success')),

        dbc.Col(dbc.Card(
            card(
                process.status_hari('jumlah_meninggal_kum'), 
                'MENINGGAL',
                '+%s Kasus Meninggal' % (process.status_hari('jumlah_meninggal'))
            ), 
            color='danger'))
    ], justify='center'),


], style={'color': 'white'})

# Section 2, chart
section2 = html.Div([
    dcc.Graph(
        figure=process.positif,
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        figure=process.gabungan,
        config={'displayModeBar': False}
    )
])

# Section 3. Choropleth map
section3 = html.Div([
    dcc.Graph(
        figure=process_prov_map.map,
        config={'displayModeBar': False}
    )
])

# Section 4. dropdown provinsi
section4 = html.Div([
    dcc.Dropdown(
        id='list-provinsi',
        options=process_prov_map.list_provinsi,
        placeholder='Masukkan provinsi',
        value=['Jambi'],
        multi=False
    ),

    html.Div(id='output')
])