import requests

import pandas as pd
import geopandas as gpd
import plotly.express as px

from datetime import date

# list provinsi, digunakan dalam looping pengumpulan informasi terkini untuk choropleth map
list_provinsi=[
         {'label': 'Aceh', 'value': 'Aceh'},
         {'label': 'Bali', 'value': 'Bali'},
         {'label': 'Kepulauan Bangka Belitung', 'value': 'Kepulauan Bangka Belitung'},
         {'label': 'Banten', 'value': 'Banten'},
         {'label': 'Bengkulu', 'value': 'Bengkulu'},
         {'label': 'Daerah Istimewa Yogyakarta', 'value': 'Daerah Istimewa Yogyakarta'},
         {'label': 'DKI Jakarta', 'value': 'DKI Jakarta'},
         {'label': 'Gorontalo', 'value': 'Gorontalo'},
         {'label': 'Jambi', 'value': 'Jambi'},
         {'label': 'Jawa Barat', 'value': 'Jawa Barat'},
         {'label': 'Jawa Tengah', 'value': 'Jawa Tengah'},
         {'label': 'Jawa Timur', 'value': 'Jawa Timur'},
         {'label': 'Kalimantan Barat', 'value': 'Kalimantan Barat'},
         {'label': 'Kalimantan Selatan', 'value': 'Kalimantan Selatan'},
         {'label': 'Kalimantan Tengah', 'value': 'Kalimantan Tengah'},
         {'label': 'Kalimantan Timur', 'value': 'Kalimantan Timur'},
         {'label': 'Kalimantan Utara', 'value': 'Kalimantan Utara'},
         {'label': 'Kepulauan Riau', 'value': 'Kepulauan Riau'},
         {'label': 'Lampung', 'value': 'Lampung'},
         {'label': 'Maluku', 'value': 'Maluku'},
         {'label': 'Maluku Utara', 'value': 'Maluku Utara'},
         {'label': 'Nusa Tenggara Barat', 'value': 'Nusa Tenggara Barat'},
         {'label': 'Nusa Tenggara Timur', 'value': 'Nusa Tenggara Timur'},
         {'label': 'Papua', 'value': 'Papua'},
         {'label': 'Papua Barat', 'value': 'Papua Barat'},
         {'label': 'Riau', 'value': 'Riau'},
         {'label': 'Sulawesi Barat', 'value': 'Sulawesi Barat'},
         {'label': 'Sulawesi Selatan', 'value': 'Sulawesi Selatan'},
         {'label': 'Sulawesi Tengah', 'value': 'Sulawesi Tengah'},
         {'label': 'Sulawesi Tenggara', 'value': 'Sulawesi Tenggara'},
         {'label': 'Sulawesi Utara', 'value': 'Sulawesi Utara'},
         {'label': 'Sumatera Barat', 'value': 'Sumatera Barat'},
         {'label': 'Sumatera Selatan', 'value': 'Sumatera Selatan'},
         {'label': 'Sumatera Utara', 'value': 'Sumatera Utara'},
]

# inisiasi dataframe kosong
df_prov = pd.DataFrame()

# looping di setiap provinsi, menambahkan statistik perawatan, sembuh, meninggal dan jumlah kasus ke dataframe
for i in range(len(list_provinsi)):
    prov = list_provinsi[i]['label'].upper().replace(' ', '_')
    link = 'https://data.covid19.go.id/public/api/prov_detail_' + prov + '.json'
    a = requests.get(link)
    data = a.json()

    df_perprov = pd.DataFrame(data['list_perkembangan'])
    df_perprov['tanggal'] = df_perprov['tanggal'].apply(lambda x: date.fromtimestamp(x/1000))

    akhir = df_perprov.shape[0]

    kasus = df_perprov['AKUMULASI_KASUS'][akhir-1]
    perawatan = df_perprov['AKUMULASI_DIRAWAT_OR_ISOLASI'][akhir-1]
    sembuh = df_perprov['AKUMULASI_SEMBUH'][akhir-1]
    meninggal = df_perprov['AKUMULASI_MENINGGAL'][akhir-1]

    df_prov = df_prov.append({
        'provinsi': data['provinsi'],
        'perawatan': perawatan,
        'sembuh': sembuh,
        'meninggal': meninggal,
        'kasus': kasus
        }, ignore_index=True)

df_prov.index=df_prov.provinsi
    

# Load data geojson
provinsi = gpd.read_file('./assets/indonesia.geojson')
provinsi['state'] = provinsi['state'].apply(lambda x: x.upper())
provinsi.index = provinsi.state

# Rename nama provinsi agar sesuai dengan dataframe covid
provinsi.at['BANGKA-BELITUNG', 'state'] = 'KEPULAUAN BANGKA BELITUNG'
provinsi.at['JAKARTA RAYA', 'state'] = 'DKI JAKARTA'
provinsi.at['YOGYAKARTA', 'state'] = 'DAERAH ISTIMEWA YOGYAKARTA'
provinsi.index = provinsi.state

# Choropleth map
map = px.choropleth_mapbox(
    df_prov, 
    geojson=provinsi.geometry,
    color='kasus',
    locations='provinsi',
    center={'lat': -0.789275, 'lon': 118.0148634},
    mapbox_style='carto-positron', 
    hover_name='provinsi',
    hover_data=['provinsi', 'kasus', 'perawatan', 'sembuh', 'meninggal'],
    zoom=3.9,
    width=400,
    title='Kasus Per-Provinsi',
)
map.update_layout(
    margin=dict(l=20, r=20, t=30, b=20)
)