import json
import random
import dash
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np

data = pd.read_excel('Store Lat lng.xlsx')
data['Vendor'] = 'Canbo'

avgLat = data['lat'].mean()
avgLong = data['lng'].mean()

lats = np.array(data.lat)
lons = np.array(data.lng)

n = len(lats)
markers1 = [dl.Marker(id=str(i), position=(lats[i], lons[i]), title='Canbo') for i in range(n)]
cluster1 = dl.MarkerClusterGroup(children=markers1, id="Canbo")

data = pd.read_excel('useraddress.xlsx').head(1000)
data['Vendor'] = 'Zooket'

avgLat = data['latitude'].mean()
avgLong = data['longitude'].mean()

lats = np.array(data.latitude)
lons = np.array(data.longitude)

n = len(lats)
markers2 = [dl.Marker(id=str(i), position=(lats[i], lons[i]), title='Zooket') for i in range(n)]
cluster2 = dl.MarkerClusterGroup(children=markers2, id="Zooket")

app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.de/{z}/{x}/{y}.png"), cluster1, cluster2],
           style={'width': "100%", 'height': "100%"}, center=[avgLat, avgLong], zoom=5, id="map", preferCanvas=True), html.P(id="log")],
    style={"position": "relative", 'width': '100%', 'height': '1000px'})



@app.callback(Output("log", "children"), [Input("cluster", "click_marker_id")])
def marker_click(marker_id):
    return marker_id

if __name__ == '__main__':
    app.run_server(debug=False)