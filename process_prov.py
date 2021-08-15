import requests
import process_prov_map

import plotly.express as px
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import datetime, date
from conf import app
from conf import server


# Section 4. dropdown provinsi
section4 = html.Div([
    html.Br(),
    html.H3('Informasi Per-Provinsi'),
    dcc.Dropdown(
        id='list-provinsi',
        options=process_prov_map.list_provinsi,
        placeholder='Masukkan provinsi',
        value='Jambi',
        multi=False
    ),

    html.Div(id='output')
])


@app.callback(
    Output('output', 'children'),
    Input('list-provinsi', 'value')
)
def update_info(value):

    # fungsi card
    def card(angka, status, penambahan):
        '''
        Untuk card status kasus aktif, sembuh, meninggal dan dirawat
        '''
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

    # fungsi bar chart
    def get_bar(dataframe, title):
        '''
        Generate barchart data covid indonesia
        '''
        chart = px.bar(
            dataframe, 
            x='key', 
            y='doc_count',
            title=title,
            labels={'doc_count': '(Persen (%))'},
            color='key',
            )
        chart.update_layout(
                xaxis=dict(
                    showgrid=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgrey',
                ),
                plot_bgcolor='white',
                title_x=0.5,
                showlegend=False,

                hoverlabel= dict(
                    bgcolor='white'
                )
            )
        chart.update_yaxes(fixedrange=True)
        chart.update_xaxes(fixedrange=True, title_text='')
        return chart

    def get_pie(dataframe, title):
        '''
        Generate pie chart untuk kelompok usia dan jenis kelamin
        '''
        chart = px.pie(
            dataframe, 
            title=title,
            values='doc_count', 
            names='key',
            hover_name='key',
            labels={
                'key': 'Key',
                'doc_count': 'Persen'
            }
        )
        chart.update_layout(
            title_x=0.5,
            hoverlabel = dict(
                bgcolor='white'
            )
        )
        return chart

    def generate_chart(kondisi, mode, title):
        '''
        Fungsi untuk generate chart
        kondisi: nama kolom pada dataframe
        mode: bar/pie
        title: chart title
        '''
        jumlah_data = data['data']['kasus'][kondisi]['current_data']
        dataframe = pd.DataFrame(data['data']['kasus'][kondisi]['list_data'])
        
        if mode == 'bar':
            out = get_bar(
                dataframe, 
                title='%s Provinsi %s (%s data)' % (title, provinsi.title(), jumlah_data),
            )
        elif mode == 'pie':
            out = get_pie(
                dataframe, 
                title='%s Provinsi %s (%s data)' % (title, provinsi.title(), jumlah_data),
            )
        else:
            print('Periksa kembali parameter mode (pie/bar)')
        
        return out

    def get_chart(df, x, y, title, legend_title):
        chart = px.line(
            df,
            x=x,
            y=y,
            title=title,
            labels={
                'KASUS':'Kasus Baru',
                'tanggal':'Tanggal',
                'MENINGGAL': 'Meninggal',
                'SEMBUH': 'Sembuh'
                },
            )
        chart.update_yaxes(title_text='', fixedrange=True)
        chart.update_xaxes(title_text='')
        chart.update_layout(
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey',
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            plot_bgcolor='white',
            title_x=0.5,
            height=600,
            legend_title_text=legend_title,
            hovermode='x unified'
        )

        return chart


    if value != None:
        prov = value.upper().replace(' ', '_')
        link = 'https://data.covid19.go.id/public/api/prov_detail_' + prov + '.json'
        a = requests.get(link)
        data = a.json()

        # ubah format tanggal
        tgl = datetime.strptime(data['last_date'], '%Y-%m-%d')
        tanggal_update = tgl.strftime('%d %B %Y')

        # membuat dataframe untuk plot
        df_perprov = pd.DataFrame(data['list_perkembangan'])

        # merubah timestamp ke datetime object
        df_perprov['tanggal'] = df_perprov['tanggal'].apply(lambda x: date.fromtimestamp(x/1000))

        # jumlah data
        akhir = df_perprov.shape[0]

        # Nama provinsi
        provinsi = data['provinsi']

        # total kasus
        total_kasus = df_perprov['AKUMULASI_KASUS'][akhir-1]
        total_sembuh = df_perprov['AKUMULASI_SEMBUH'][akhir-1]
        total_meninggal = df_perprov['AKUMULASI_MENINGGAL'][akhir-1]
        total_dirawat = df_perprov['AKUMULASI_DIRAWAT_OR_ISOLASI'][akhir-1]

        # statistik provinsi
        gabungan = get_chart(
            df_perprov,
            x='tanggal',
            y=['KASUS', 'MENINGGAL', 'SEMBUH'],
            title='Perkembangan Kasus Per-Hari (Grafik Gabungan) Provinsi %s' % (provinsi),
            legend_title=''
        )

        # Gejala positif covid
        gejala_positif = generate_chart(
            kondisi='gejala',
            mode='bar',
            title='Gejala Positif Covid-19'
        )

        # Kondisi penyerta positif covid-19
        kondisi_penyerta = generate_chart(
            kondisi='kondisi_penyerta',
            mode='bar',
            title='Kondisi Penyerta Positif Covid-19'
        )

        # Kelompok umur
        kelompok_umur = generate_chart(
            kondisi='kelompok_umur',
            mode='pie',
            title='Kelompok Umur Positif Covid-19'
        )

        # Kelompok jenis kelamin
        kelompok_jk = generate_chart(
            kondisi='jenis_kelamin',
            mode='pie',
            title='Jenis Kelamin Positif Covid-19'
        )

        # Variable yang akan di return
        out = html.Div([
            html.Br(),

            # Row nama provinsi
            dbc.Row([
                html.H2(provinsi),
            ], justify='center'),

            # Row statistik provinsi
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        card(
                            format(total_kasus, ','),
                            'TERKONFIRMASI',
                            '+%s Kasus' % (format(df_perprov['KASUS'][akhir-1], ','))
                        ), color='primary')
                ]),

                dbc.Col([
                    dbc.Card(
                        card(
                            format(total_dirawat, ','),
                            'KASUS AKTIF',
                            '+%s Kasus Aktif' % (format(df_perprov['DIRAWAT_OR_ISOLASI'][akhir-1], ','))
                        ), color='warning')
                ]),

                dbc.Col([
                    dbc.Card(
                        card(
                            format(total_sembuh, ','),
                            'SEMBUH',
                            '+%s Kasus Sembuh' % (format(df_perprov['SEMBUH'][akhir-1], ','))
                        ), color='success')
                ]),

                dbc.Col([
                    dbc.Card(
                        card(
                            format(total_meninggal, ','),
                            'MENINGGAL',
                            '+%s Kasus Meninggal' % (format(df_perprov['MENINGGAL'][akhir-1], ','))
                        ), color='danger')
                ]),


            ], style={'color': 'white'}),

            # Row chart provinsi
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=gabungan, config={'displayModeBar': False})
                ])
            ]),

            # Row statistik gejala
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=gejala_positif,
                        config={'displayModeBar': False})
                ]),

                dbc.Col([
                    dcc.Graph(
                        figure=kondisi_penyerta,
                        config={'displayModeBar': False})
                ]),

            ]),

            # Row kelompok usia dan jenis kelamin
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=kelompok_umur,
                        config={'displayModeBar': False}
                    )
                ]),

                dbc.Col([
                    dcc.Graph(
                        figure=kelompok_jk,
                        config={'displayModeBar': False}
                    )
                ])

            ])


        ])


        return out