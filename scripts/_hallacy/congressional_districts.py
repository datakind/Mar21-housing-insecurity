import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas
from dash.dependencies import Input, Output
import git
import json

repo = git.Repo('.', search_parent_directories=True)
repo_path = repo.working_tree_dir

ev_fl = pd.read_csv(f"{repo_path}/data/_volunteer_created_datasets/_hallacy/hillsborough_county_evictions_geocoded.csv")
mean_long = -82.640305
mean_lat = 28.027870


# State Senate Districts
state_senate_gdf = geopandas.read_file(f"zip://{repo_path}/data/geo/florida_sdist_2021.zip").to_crs(4326)

ctg = ev_fl.groupby('state_senate_district').size().reset_index()
ctg.columns = ['state_senate_district','num_evictions']
ctg = ctg.rename(columns={"state_senate_district":"DISTRICT"})
state_senate_gdf['DISTRICT'] = state_senate_gdf['DISTRICT'].astype(float)

state_senate_gdf = state_senate_gdf.merge(ctg,on='DISTRICT',how='left')
# Get rid of NaNs
state_senate_gdf["num_evictions"] = state_senate_gdf["num_evictions"].apply(lambda x: x if x==x else 0)

jsondata = json.loads(state_senate_gdf.to_json())

scat_fig = px.choropleth_mapbox(state_senate_gdf, geojson=jsondata, color="num_evictions",
                   color_discrete_sequence = px.colors.qualitative.Dark24,
                   locations="DISTRICT", featureidkey="properties.DISTRICT",opacity=0.5,
                   center={"lat": mean_lat ,"lon": mean_long},
                   mapbox_style="streets")
scat_fig.update_layout(height=1000,title = "Number of Evictions by State Senate District")
        #scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
scat_fig.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
                        mapbox_zoom=9, 
                        mapbox_center = {"lat": mean_lat, "lon": mean_long}
                        )   
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# US districts
us_gdf = geopandas.read_file(f"zip://{repo_path}/data/geo/florida_usdist_2021.zip").to_crs(4326)


ctg = ev_fl.groupby('us_district').size().reset_index()
ctg.columns = ['us_district','num_evictions']
ctg = ctg.rename(columns={"us_district":"DISTRICT"})
us_gdf['DISTRICT'] = us_gdf['DISTRICT'].astype(float)

us_gdf = us_gdf.merge(ctg,on='DISTRICT',how='left')
# Get rid of NaNs
us_gdf["num_evictions"] = us_gdf["num_evictions"].apply(lambda x: x if x==x else 0)
us_gdf

jsondata = json.loads(us_gdf.to_json())

scat_fig_us = px.choropleth_mapbox(us_gdf, geojson=jsondata, color="num_evictions",
                   color_discrete_sequence = px.colors.qualitative.Dark24,
                   locations="DISTRICT", featureidkey="properties.DISTRICT",opacity=0.5,
                   center={"lat": mean_lat ,"lon": mean_long},
                   mapbox_style="streets")
scat_fig_us.update_layout(height=1000,title = "Number of Evictions by US District")
        #scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
scat_fig_us.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
                        mapbox_zoom=9, 
                        mapbox_center = {"lat": mean_lat, "lon": mean_long}
                        )   
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children='Eviction Plots by US District'),
        dcc.Graph(
            id='scatterplotUS',
            figure=scat_fig_us
        ),
        html.H1(children='Eviction Plots by State Senate District'),
        dcc.Graph(
            id='scatterplotStateSenate',
            figure=scat_fig
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=8086)

