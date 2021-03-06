import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas
from dash.dependencies import Input, Output

sd = geopandas.read_file("/home/dgillen/notebooks/Mar21-housing-insecurity/data/geo/nyc_school_districts.geojson")
ct = geopandas.read_file("/home/dgillen/notebooks/Mar21-housing-insecurity/data/geo/nyc_2010_tracts_formatted.geojson")
ct_fl = geopandas.read_file("/home/dgillen/notebooks/Mar21-housing-insecurity/data/geo/hillsborough_fl_2010_tracts_formatted.geojson")

ev = pd.read_csv("/home/dgillen/notebooks/Mar21-housing-insecurity/data/raw/nyc_evictions_geocoded.csv")
ev_fl = pd.read_csv("/home/dgillen/notebooks/Mar21-housing-insecurity/data/raw/hillsborough_county_evictions_geocoded.csv")
hillsborough_county_mortgage_foreclosures_geocoded.csv

ev[['lon','lat']] = ev.lon_lat.str.split(',', expand=True)

evGDF = geopandas.GeoDataFrame(ev, geometry=geopandas.points_from_xy(ev.lon, ev.lat,crs=ct.crs))
ctGDF = geopandas.sjoin(evGDF, ct, op='within',how='left')
ctGDF[['EVICTION_ADDRESS','lon','lat','census_tract_GEOID']]

ctg = ctGDF.groupby('census_tract_GEOID').size().reset_index()
ctg.columns = ['census_tract_GEOID','num_evictions']
cf = ct.merge(ctg,on='census_tract_GEOID',how='left')
cf

import json
with open('/home/dgillen/notebooks/Mar21-housing-insecurity/data/geo/nyc_2010_tracts_formatted.geojson') as json_file:
    ctGeoJson = json.load(json_file)

mean_long = -73.93865
mean_lat = 40.788143


scat_fig = px.choropleth_mapbox(cf, geojson=ctGeoJson, color="num_evictions",
                   color_discrete_sequence = px.colors.qualitative.Dark24,
                   locations="census_tract_GEOID", featureidkey="properties.census_tract_GEOID",opacity=0.5,
                   center={"lat": mean_lat ,"lon": mean_long},
                   mapbox_style="streets")
scat_fig.update_layout(height=1000,title = "Number of Evictions by Census Tract")
        #scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
scat_fig.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
                        mapbox_zoom=9, 
                        mapbox_center = {"lat": mean_lat, "lon": mean_long}
                        )   
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Eviction Plots'),
     dcc.Graph(
        id='scatterplot',
        figure=scat_fig
    )
])



# @app.callback(
#     Output('treemap', 'figure'),
#     [Input('dropDown','value'),
#     Input('colDropDown', 'value'),
#     Input('colValDropDown','value'),
#     Input('secColDropDown','value'),
#     Input('secValDropDown','value')],
#     Input('IncludeIndependentsCheckBox','value'))
# def update_figure(gb_cols,
#                   filter_col,
#                   vals_to_filter_on,
#                   second_filter_col,
#                   second_vals_to_filter_on,
#                   include_independents):
#     print("gb_cols = ",gb_cols)
#     print("filter_col = ",filter_col)
#     print("second_filter_col = ",filter_col)
#     print("vals_to_filter_on = ",vals_to_filter_on)
#     print("second_vals_to_filter_on = ",second_vals_to_filter_on)
#     print("include_independents = ",include_independents)


#     if len(vals_to_filter_on) > 0:
#         filteredDF = dfToPivot[dfToPivot[filter_col].isin(vals_to_filter_on)]
#     else:
#         filteredDF = dfToPivot
#     if len(second_vals_to_filter_on) > 0 :
#         filteredDF = filteredDF[filteredDF[second_filter_col].isin(second_vals_to_filter_on)]
#     else:
#         filteredDF = filteredDF   
#     if len(include_independents) == 0:
#        filteredDF =  filteredDF[filteredDF.broker_name != "Independent"]
#     rdf = filteredDF.groupby(gb_cols).agg({'retention':['mean'],
#                                         'buy_listing_guid':'nunique',
#                                         'agent_state_id' : 'nunique'
#                                        }).reset_index()
#     rdf.columns = gb_cols + ['mean_retention','num_resales','num_unq_agents']
#     if len(gb_cols) > 1:
#         totalBoxes = rdf[gb_cols[0]].nunique()
#         print("init totalBoxes = ",totalBoxes)
#         for i, gb_col in enumerate(gb_cols):
#             if i < len(gb_cols) - 1:
#                 boxesAtThisLevel = rdf[gb_cols[i+1]].nunique()
#                 totalBoxes = totalBoxes * boxesAtThisLevel
#                 print("totalBoxes = ",totalBoxes)

#         #maxBoxes = rdf.groupby(gb_cols[:-1])[gb_cols[-1]].nunique().max()
#         print("final totalBoxes = ",totalBoxes)
#         #print("maxBoxes = ",maxBoxes)
#         if totalBoxes > 5000:
#             print("num_resales must be > 100")
#             dfToVis = rdf[(rdf.num_resales > 100)]
#             if (dfToVis.shape[0] == 0):
#                 dfToVis = df[(rdf.num_resales > 0)]
#         elif (totalBoxes < 5000) & (totalBoxes > 500):
#             print("num_resales must be > 10")
#             dfToVis = rdf[(rdf.num_resales > 10)]
#             if (dfToVis.shape[0] == 0):
#                 dfToVis = df[(rdf.num_resales > 0)]
#         else:
#             dfToVis = rdf[(rdf.num_resales > 0)]
#     else:
#         dfToVis = rdf[(rdf.num_resales > 100)]
#     #dfToVis = rdf[(rdf.num_resales > 5)]
#     dfToVis['mean_retention_str'] = dfToVis.mean_retention.apply(lambda rate:"{:,.0f}% retained ".format(100*rate))
#     dfToVis['num_resales_str'] = dfToVis.num_resales.apply(lambda val: str(val) + " resales")
#     fig = px.treemap(dfToVis, path=gb_cols, values='num_resales',height=1000,custom_data=['mean_retention_str','num_resales_str'],
#                   color='mean_retention',range_color=[0.2,0.55],maxdepth=30)
#     #fig.data[0].text = dfToVis.mean_retention_str                 
#     #fig.data[0].textinfo = 'label+text+value'
#     fig.data[0].textposition = 'middle center'
#     fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[1]}<br>%{customdata[0]}"
#     return fig

# @app.callback(
#     [Output('barchart', 'figure'),Output('scatterplot','figure')],
#     [Input('treemap', 'clickData'),Input('dropDown', 'value')])
# def update_barchart(clickData,gb_cols):
#     if (clickData['points'] is not None):
#         idStr = clickData['points'][0]['id']
#         print(gb_cols)
#         print(idStr)
#         splits = idStr.split("/")
#         fdf = pd.DataFrame()
#         clickTitle = ""
#         if len(splits) == 4:
#             firstCol = gb_cols[0]
#             secondCol = gb_cols[1]
#             thirdCol = gb_cols[2]
#             fourthCol = gb_cols[3]
#             firstVal = splits[0]
#             secondVal = splits[1]
#             thirdVal = splits[2]
#             fourthVal = splits[3]
#             clickTitle = firstCol+"= "+firstVal+", "+secondCol+"= "+secondVal+", "+thirdCol+"= "+thirdVal+", "+fourthCol+"= "+fourthVal
#             fdf = dfToPivot.loc[(dfToPivot[firstCol]==firstVal) & 
#                                 (dfToPivot[secondCol]==secondVal) &
#                                 (dfToPivot[thirdCol]==thirdVal) &
#                                 (dfToPivot[fourthCol]==fourthVal)
#                                 ]
#         elif len(splits) == 3:
#             firstCol = gb_cols[0]
#             secondCol = gb_cols[1]
#             thirdCol = gb_cols[2]
#             firstVal = splits[0]
#             secondVal = splits[1]
#             thirdVal = splits[2]
#             clickTitle = firstCol+"= "+firstVal+", "+secondCol+"= "+secondVal+", "+thirdCol+"= "+thirdVal
#             fdf = dfToPivot.loc[(dfToPivot[firstCol]==firstVal) & 
#                                 (dfToPivot[secondCol]==secondVal) &
#                                 (dfToPivot[thirdCol]==thirdVal)
#                                 ]
#         elif len(splits) == 2:
#             firstCol = gb_cols[0]
#             secondCol = gb_cols[1]
#             firstVal = splits[0]
#             secondVal = splits[1]
#             clickTitle = firstCol+"= "+firstVal+", "+secondCol+"= "+secondVal
#             fdf = dfToPivot.loc[(dfToPivot[firstCol]==firstVal) & 
#                           (dfToPivot[secondCol]==secondVal)]
#         else:
#             return None
#         print(fdf.shape)
#         num_resales = fdf.shape[0]
#         num_unq_guids = fdf.buy_listing_guid.nunique()
#         print("num_resales =",num_resales)
#         print("num_unq_guids =",num_unq_guids)
#         dtdf = fdf.groupby(['resale_qtr','retention_str']).agg({
#                                         'buy_listing_guid':'nunique'
#                                        }).reset_index()
#         print("dtdf =",dtdf.shape)
#         dtdf.columns = ['resale_qtr','retention_str'] + ['num_resales']
#         bar_fig_title = "Temporal View of the "+str(num_resales)+" properties with "+clickTitle
#         bar_fig = px.bar(dtdf,x='resale_qtr',y='num_resales',color='retention_str',height = 900,title=bar_fig_title)
#         bar_fig.update_layout(xaxis={'categoryorder':'category ascending'})

#         #if num_resales < 200:
#         import plotly.graph_objects as go
#         mean_lat = fdf.latitude.mean()
#         mean_long = fdf.longitude.mean()
#         scat_fig_title = "Spatial Distribution of the "+str(num_resales)+" properties with "+clickTitle
#         hovertemplate1='<b>Addr</b>: %{customdata[0]} <br><b>ReSale Date</b>: %{customdata[1]} <br><b>BuyList</b>: %{customdata[2]} <br><b>ResaleBroker</b>: %{customdata[3]} <br>'


#         # df['num_resales'] = df.groupby("broker_name")['buy_listing_guid'].transform('nunique')
#         # df = df[df.num_resales > 10]
#         # scat_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",color="broker_name", 
#         #                               color_discrete_sequence = px.colors.qualitative.Dark24,
#         #                               size='buy_list_price',size_max=15, zoom=11)
    

#         # scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
#         # scat_fig.update_layout(height=800)
#         # scat_fig.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
#         #                 mapbox_zoom=8, mapbox_center = {"lat": mean_lat, "lon": mean_long}
#         #                 )
#         geoidDF = fdf.groupby(['GEOID']).agg({'buy_listing_guid':'nunique',
#                                               'retention':'mean',
#                                               'tapestry_segment':'max'
#                                              }).reset_index()
#         geoidDF.columns = ['GEOID','num_resale_rows','avg_retention','segment']
#         numTop = 10
#         topSegs = geoidDF.segment.value_counts().index[0:numTop].tolist()
#         geoidDF['top_seg'] = geoidDF.segment
#         geoidDF.loc[~geoidDF.segment.isin(topSegs),"top_seg"] = "Other"
#         print(geoidDF.top_seg.value_counts())
#         geoIdList = list(geoidDF.GEOID.values)
#         geoJson = [x for x in blockGroups['features'] if x['properties']['GEOID'] in geoIdList]
#         print("len of geoJson = ",len(geoJson))
#         geoJson = {'type':'FeatureCollection','features':geoJson}
#         scat_fig = go.Figure()
#         # scat_fig.add_trace(go.Choroplethmapbox(geojson=geoJson, locations=geoidDF.GEOID.values, z=geoidDF.num_resale_rows.values,
#         #                         #customdata=customdata1,
#         #                         featureidkey="properties.GEOID",colorscale="inferno",name="",#zmin=20,zmax=60,
#         #                         colorbar_title = '# of resales',
#         #                         #hovertemplate=hovertemplate1,
#         #                         marker_opacity=0.5, marker_line_width=1))        
#         # scat_fig = px.choropleth_mapbox(geoidDF, geojson=geoJson, color="top_seg",
#         #                    color_discrete_sequence = px.colors.qualitative.Dark24,
#         #                    locations="GEOID", featureidkey="properties.GEOID",opacity=0.5,
#         #                    center={"lat": mean_lat ,"lon": mean_long},
#         #                    mapbox_style="streets", zoom=9)
#         df = fdf[fdf.retention == 0]
#         customdata1  = np.stack((df.normalizedaddress.values,
#                          df.resale_date_str.values,
#                          df.buy_list_price_str.values, 
#                          df.resale_broker_name.values,
#                         ), axis=-1)
#         scat_fig.add_trace(go.Scattermapbox(name='NotRetained',
#                 lat=df.latitude.values,
#                 lon=df.longitude.values,
#                 customdata=customdata1,
#                 hovertemplate=hovertemplate1,
#                 mode='markers',
#                 marker=go.scattermapbox.Marker(size=10,color='blue',opacity=0.6),
#             ))
#         df = fdf[fdf.retention == 1]
#         customdata1  = np.stack((df.normalizedaddress.values,
#                          df.resale_date_str.values,
#                          df.buy_list_price_str.values, 
#                          df.resale_broker_name.values,
#                         ), axis=-1)
#         scat_fig.add_trace(go.Scattermapbox(name='Retained',
#                 lat=df.latitude.values,
#                 lon=df.longitude.values,
#                 customdata=customdata1,
#                 hovertemplate=hovertemplate1,
#                 mode='markers',
#                 marker=go.scattermapbox.Marker(size=10,color='red',opacity=0.6),
#             ))
#         scat_fig.update_layout(height=1000,title = scat_fig_title)
#         #scat_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0,'pad':15})
#         scat_fig.update_layout(mapbox_style="streets", mapbox_accesstoken='pk.eyJ1IjoiZGdpbGxlbiIsImEiOiJjam85OGFvaXIxZXRlM2tubG8zY3E0OHh1In0.KkjAoFhjOOFjXAEuZ1IRog',
#                         mapbox_zoom=11, mapbox_center = {"lat": mean_lat, "lon": mean_long}
#                         )                                    
#         return bar_fig,scat_fig

if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=8085)

