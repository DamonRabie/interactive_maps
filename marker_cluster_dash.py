import dash
import dash_leaflet as dl
from dash import html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np

app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], prevent_initial_callbacks=True)


def _load_data(path: str, lat_col_name: str = 'lat', long_col_name: str = 'long') -> [np.array, np.array]:
    file_type = path.split('.')[-1].lower()
    if file_type == 'excel':
        df = pd.read_excel(path)
    elif file_type == 'csv':
        df = pd.read_csv(path)
    else:
        raise "Not a valid type"

    return np.array(df[lat_col_name]), np.array(df[long_col_name])


def _generate_map(lats: np.array, longs: np.array, title: str):
    n = len(lats)
    markers = [dl.Marker(id=str(i), position=(lats[i], longs[i]), title=title) for i in range(n)]
    cluster = dl.MarkerClusterGroup(children=markers, id=title)

    return cluster


@app.callback(Output("log", "children"), [Input("cluster", "click_marker_id")])
def marker_click(marker_id):
    return marker_id


def run(path_list: list):
    cluster_list = []
    avg_lat = 0
    avg_long = 0

    for item in path_list:
        _tmp_lat, _tmp_long = _load_data(path=item['path'], lat_col_name=item['lat_name'],
                                         long_col_name=item['long_name'])
        cluster_list.append(_generate_map(_tmp_lat, _tmp_long, title=item['title']))
        avg_lat = _tmp_lat.mean()
        avg_long = _tmp_long.mean()

    app.layout = html.Div([
        dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.de/{z}/{x}/{y}.png")] + cluster_list,
               style={'width': "100%", 'height': "100%"}, center=[avg_lat, avg_long], zoom=5, id="map",
               preferCanvas=True),
        html.P(id="log")],
        style={"position": "relative", 'width': '100%', 'height': '1000px'})
    app.run_server(debug=False)


if __name__ == '__main__':
    files = [{
        "title": "GPS",
        "path": "data/GPS Trajectory/go_track_trackspoints.csv",
        "lat_name": "latitude",
        "long_name": "longitude"
    }
    ]

    run(files)
