#!/usr/bin/env python
# coding: utf-8

# # Imports, constantes et chargement des données

from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

server = Flask(__name__)

# @server.route('/')
# def index():
#     return 'Hello Flask app'

app = dash.Dash(
    __name__,
    server=server,
    # routes_pathname_prefix='/dash/'
)

app.layout =  html.Div(children = [
        html.H1("Home Credit - Fiche Client"),
        dcc.Input(id='no_client', type='text'),
        html.Div(id='info_client'),
        dcc.Graph(
            id='example',
            figure={
                'data': [
                    {'x': [1, 2, 3, 4, 5], 'y': [9, 6, 2, 1, 5], 'type': 'line', 'name': 'Boats'},
                    {'x': [1, 2, 3, 4, 5], 'y': [8, 7, 2, 7, 3], 'type': 'bar', 'name': 'Cars'}
                ],
                'layout': {
                    'title': 'Basic Dash Example'
                }
            }
        )
        ])

@app.callback(
    Output(component_id='info_client', component_property='children'),
    [Input(component_id='no_client', component_property='value')]
)
def update_value(input_data):
    return 'Bonjour  "{}"'.format(input_data)


if __name__ == '__main__':
    app.run_server(debug=True)

