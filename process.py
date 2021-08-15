import requests
import pandas as pd
import plotly.express as px

from datetime import datetime

populasi_indonesia = 269603400

read = requests.get('https://data.covid19.go.id/public/api/update.json')

data = read.json()

data_update = data['update']

df = pd.DataFrame(data_update['harian'])

# ekstrak value dari dictionary
v_ekstrak = ['jumlah_meninggal', 'jumlah_sembuh', 'jumlah_positif', 'jumlah_dirawat', 
             'jumlah_positif_kum', 'jumlah_sembuh_kum', 'jumlah_meninggal_kum', 'jumlah_dirawat_kum']

for i in v_ekstrak:
    df[i] = (
        df[i]
        .apply(lambda x: x['value'])
    )

# mengubah kolom dan menghapus kolom
df = (
    df
    .rename(columns={'key_as_string': 'date'})
    .drop(['key', 'doc_count'], axis=1)
)

# konversi kolom date ke datetime object
df['date'] = pd.to_datetime(df['date'])

# menambahkan kolom [persen sembuh dari positif, persen meninggal dari positif, persen positif dari populasi indonesia]
df['persen_sembuh'] = df['jumlah_sembuh_kum'] / df['jumlah_positif_kum'] * 100
df['persen_meninggal'] = df['jumlah_meninggal_kum'] / df['jumlah_positif_kum'] * 100
df['persen_positif_populasi'] = df['jumlah_positif_kum'] / populasi_indonesia * 100

# tanggal update data
tgl = datetime.strptime(data_update['penambahan']['tanggal'], '%Y-%m-%d')
tanggal_update = tgl.strftime('%d %B %Y')

# cek status pertambahan per-hari
def status_hari(status):
    jumlah_hari = df.shape[0]

    out = format(df[status][jumlah_hari-1], ',')

    return out

# fungsi generate chart
def get_chart(df, x, y, title, legend_title):
    chart = px.line(
        df,
        x=x,
        y=y,
        title=title,
        labels={
            'jumlah_positif':'Kasus Baru',
            'date':'Tanggal',
            'value': 'Jumlah',
            'variable': 'Variable'
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

positif = get_chart(
    df,
    x='date',
    y='jumlah_meninggal',
    title='Perkembangan Kasus Terkonfirmasi Positif Covid-19 Per-Hari',
    legend_title='Kasus Positif'
)

gabungan = get_chart(
    df,
    x='date',
    y=['jumlah_positif', 'jumlah_sembuh', 'jumlah_meninggal'],
    title='Perkembangan Kasus Per-Hari (Grafik Gabungan)',
    legend_title=''
)