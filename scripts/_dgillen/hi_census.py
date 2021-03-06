import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas
from dash.dependencies import Input, Output

data_path = "/home/dgillen/notebooks/Mar21-housing-insecurity/data/"
df = pd.read_csv(data_path + 'processed/hillsborough_fl_processed_2017_to_2019_20210225.csv')

import json
with open("/home/dgillen/notebooks/Mar21-housing-insecurity/data/geo/hillsborough_fl_2010_tracts_formatted.geojson") as json_file:
    ct_fl_geo_json = json.load(json_file)

mean_long = -73.93865
mean_lat = 40.788143

mean_long_fl = -82.640305
mean_lat_fl = 28.027870

colList = df.columns.values
firstColDropDownList = [{'label':colVal,'value':colVal} for colVal in colList]
secondColDropDownList = [{'label':colVal,'value':colVal} for colVal in colList]
first_col = 'pct-owner-occupied'
second_col = 'total-evictions'

def create_fig(col_name):
    print("col_name = ",col_name)
    fig = px.choropleth_mapbox(df, geojson=ct_fl_geo_json, color=col_name,
                       color_discrete_sequence = px.colors.qualitative.Dark24,
                       locations="census_tract_GEOID", featureidkey="properties.census_tract_GEOID",opacity=0.5,
                       mapbox_style="streets")
    fig.update_layout(height=1000,title = "")
            #scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
    fig.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
                            mapbox_zoom=9, 
                            mapbox_center = {"lat": mean_lat_fl, "lon": mean_long_fl}
                            )  
    return fig

fig1 = create_fig(first_col)
fig2 = create_fig(second_col)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H4('Choose 1st Column to Color Census Tracts:'),
            dcc.Dropdown(
                id='firstColDropDown',
                options = firstColDropDownList,
                value=first_col,
                multi=False
            ),
            dcc.Graph(id='fig1', figure=fig1)
        ], className="six columns"),

        html.Div([
            html.H4('Choose 2nd Column to Color Census Tracts:'),
                        dcc.Dropdown(
                id='secondolDropDown',
                options = secondColDropDownList,
                value=second_col,
                multi=False
            ),
            dcc.Graph(id='fig2', figure=fig2)
        ], className="six columns"),
    ], className="row")
])

@app.callback(
    Output('fig1', 'figure'),
    [Input('firstColDropDown','value')])
def update_first_fig(first_col):
    print("first_col = ",first_col)
    fig1 = create_fig(first_col)
    return fig1

@app.callback(
    Output('fig2', 'figure'),
    [Input('secondolDropDown','value')])
def update_second_fig(second_col):
    print("second_col = ",second_col)
    fig2 =  create_fig(second_col)
    return fig2



if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=8084)

