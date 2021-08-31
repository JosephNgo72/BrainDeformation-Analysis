from os import listdir
from os.path import isfile, join
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import h5py
import hvplot.pandas
import os
import holoviews as hv
import pandas as pd
import numpy as np
from bokeh.sampledata.iris import flowers


DIR_DATA_XYZ_MPS = 'C:/Users/josep/OneDrive/Desktop/Camarillo/Maximum Principal Strain/XYZ_mps'
DIR_DATA_XNYZ_MPS = 'C:/Users/josep/OneDrive/Desktop/Camarillo/Maximum Principal Strain/XNYZ_mps'


def main():
    f = h5py.File('mps_dataset.hdf5', 'r')
    datasetXYZ_names = [f for f in listdir(DIR_DATA_XYZ_MPS) if isfile(join(DIR_DATA_XYZ_MPS, f))]

    datasets = []
    counter = 0
    for dsname in datasetXYZ_names:
        dsloc = 'XYZ_MPS/' + dsname
        print("Working on: " + dsloc)
        dataset = f[dsloc]

        df_start = pd.DataFrame(np.array(dataset[0]))
        df_mid = pd.DataFrame(np.array(dataset[34]))
        df_end = pd.DataFrame(np.array(dataset[68]))

        print('making layout')
        layout_start = df_start.hvplot.scatter(x=0, y=0, width=1500, height=680,
                                               xlabel='Brain Element', ylabel='Brain Deformation',
                                               title='Traumatic Brain Injury  Blue = 0sec  Yellow = .034sec  '
                                                     'Orange = .069sec')
        layout_mid = df_mid.hvplot.scatter(x=0, y=0, width=1500, height=680)
        layout_end = df_end.hvplot.scatter(x=0, y=0, width=1500, height=680)
        final_layout = layout_start * layout_mid * layout_end
        if counter == 0:
            hv.save(final_layout, 'out'+str(counter)+'.html')
        datasets.append(df_end)
        counter += 1
        if counter == 10: break

    renderer = hv.renderer('bokeh')
    doc = renderer.server_doc(final_layout)
    doc.title = 'HW5 Visualization'

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='Simulated Impact #',
            min=min(range(len(datasets))),
            max=max(range(len(datasets))),
            value=min(range(len(datasets))),
            marks={str(impact): str(impact) for impact in range(len(datasets))},
            step=None
        )
    ])

    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('Simulated Impact #', 'value'))
    def update_figure(selected_impact_num):
        filtered_df = datasets[selected_impact_num]

        fig = px.scatter(filtered_df)

        fig.update_layout(transition_duration=500)

        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)

    print('program finished')


if __name__ == '__main__':
    main()