# 07-COVIDINDONESIA
Web App dashboard that visualize the Covid-19 condition statistics of Indonesia and its provinces. 

The aim of this project is to get the latest covid-19 condition in Indonesia and its provinces.
This web app so far have this information:
- Total confirmed case
- Total active case
- Total recovered case
- Total death case
- Time series chart of confirmed case, total recovered case, total death case
- Choropleth map that shown statistics for each provinces in Indonesia
- Symptoms for positive patients in provinces
- Comorbid for positive patients in provinces
- Positive patients group-by age
- Positive patients group-by gender

## Dataset Description
- Covid-19 dataset is from https://data.covid19.go.id, since the code access directly to the https://data.covid19.go.id so the data shown in the app is up-to-date.
- Spatial data of each provinces area is from https://github.com/superpikar/indonesia-geojson

## Dependency
- `dash`
- `dash_html_components`
- `dash_core_components`
- `dash_bootstrap_components`
- `requests`
- `pandas`
- `geopandas`
- `plotly`

## File Description
- `RH_COVIDINDONESIA.ipynb` is a jupyter notebook which contains steo-by-step while exploring the dataset and visualizing the data
- `conf.py` contains dash app configuration 
- `app.py` contains app layout and to run the dash app
- `layout.py` contains the app layout in detail
- `process.py` contains the code to show Indonesian Covid-19 condition
- `process_prov.py` contains the code to process provinces data to visualize
- `process_prov_map.py` contains the code to process and visualize covid-19 condition on choropleth map
- `requirements.txt` contains all the required packages to run the dash app, needed to deploy the app to heroku
- `runtime.txt` is a python version, needed to deploy the app to heroku
- `Procfile` is a configuration file needed to deploy the app to heroku
- `Aptfile` is a configuration file needed to install GDAL packages to heroku
- `assets/indonesia.geojson` is a JSON file contains the spatial data for every province to visualize in choropleth map

To run the app locally, download this repo and run `python app.py` inside the folder. To test the deployed version you can go to this link: https://rh-covidindonesia.herokuapp.com/ (struggling with timeout problem)


## Screenshot
![RH-COVIDINDONESIA](https://i.imgur.com/STCYxv0.png)
![RH-COVIDINDONESIA](https://i.imgur.com/abQDGUY.png)
![RH-COVIDINDONESIA](https://i.imgur.com/hajOpeq.png)
![RH-COVIDINDONESIA](https://i.imgur.com/xpAyMJ5.png)
![RH-COVIDINDONESIA](https://i.imgur.com/ovv2fpH.png)
