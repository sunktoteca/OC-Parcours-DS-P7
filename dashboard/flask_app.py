#!/usr/bin/env python
# coding: utf-8

# # Imports, constantes et chargement des données

from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd


server = Flask(__name__)

# @server.route('/')
# def index():
#     return 'Hello Flask app'

#@app.route('/dashboard/')
#def dashboard():
#    return render_template("dashboard.html")


app = dash.Dash(
    __name__,
    server=server,
    # routes_pathname_prefix='/dash/'
)

colors = {
#    'background': '#1C1C1C',
    'text': 'red'
}

#liste_clients = [
#    {"label": "12375", "value" :{"Prenom": "Joséphine", "Age":"24", "Score" : "0.1"}},
#    {"label": "45672", "value" :{"Prenom": "Albert", "Age":"35", "Score" : "0.03"}},
#    {"label": "753145", "value" :{"Prenom": "Carole", "Age":"42", "Score" : "0.71"}},
#    {"label": "846384", "value" :{"Prenom": "Nathalie", "Age":"72", "Score" : "0.18"}},
#    {"label": "49635", "value" :{"Prenom": "Gérald", "Age":"53", "Score" : "0.34"}},
#]
#liste_clients = [
#    {"label": "12375", "value" :"Joséphine"},
#    {"label": "45672", "value" :"Albert"},
#    {"label": "753145", "value" :"Carole"},
#    {"label": "846384", "value" :"Nathalie"},
#    {"label": "49635", "value" :"Gérald"},
#]
liste_clients = [
    {"label": "12375", "value" :"12375"},
    {"label": "45672", "value" :"45672"},
    {"label": "753145", "value" :"753145"},
    {"label": "846384", "value" :"846384"},
    {"label": "49635", "value" :"49635"},
]

data = [["12375", "Joséphine", "24", "0.1"],
                 ["45672", "Albert", "35", "0.03"],
                 ["753145", "Carole", "42","0.71"],
                 ["846384", "Nathalie", "72", "0.18"],
                 ["49635", "Gérald","53","0.34"]]

df = pd.DataFrame(data=data, columns = ["id", "prenom", "age", "score"])

app.title = "Home Credit"

app.layout =  html.Div([
        ##############
        ### Entête ###
        ##############
        html.Div(
                className="app-header",
                children=[
                        html.Img(src='/assets/homecredit.png', height="100", width="100",
                                 style={'verticalAlign':'top'}
                                 ), 
                        html.Div(
                                html.H1("Home Credit - Fiche Client", 
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'width':'100%',
                                            'margin':'auto'
#                                            'display': 'inline-block'
                                            }),
                                style={
#                                       'height':'100px',
                                       'display':'inline-block',
                                        'width': '80%', 
                                        'margin':'30px',
                                        }
                                )
                        ],
                style ={'marginBottom' : '50px'}
                ),

        ######################
        ### Données client ###
        ######################
#        html.Div([
#                html.Label("Numéro de client : "),
#                dcc.Dropdown(id='no_client')
#                ]),
        html.P("Numéro de client : ", style = {'margin':'20px 0 0 0'}),
        html.Div([
            dcc.Dropdown(
                id='no_client',
                options=liste_clients,
                style={
                       "margin" :"0px 20px 20px 0",
                       "width" : "10em"}
                ),
            html.Div(id='prenom_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ), 
            html.Div(id='age_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
            html.Div(id='score_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            )

           
            ],
            style={'display':'table'}
        ),
        ######################
        ### Graphes ###
        ######################
        html.Div(
                dcc.Graph(
                        id='example',
                        figure={
                                'data': [
                                    {'x': [1, 2, 3, 4, 5], 'y': [9, 6, 2, 1, 5], 'type': 'line', 'name': 'Boats'},
                                    {'x': [1, 2, 3, 4, 5], 'y': [8, 7, 2, 7, 3], 'type': 'bar', 'name': 'Cars'}
                                    ],
                                'layout': {'title': 'Basic Dash Example'}
                                }
                        )
                )      
        ],
        style={
                'maxWidth':'1140px',
                'margin':'auto'
             }
        )




#@app.callback(
#    dash.dependencies.Output("no_client", "options"),
#    [dash.dependencies.Input("no_client", "search_value")],
#)
#def update_options(search_value):
#    if not search_value:
#        raise PreventUpdate
#    return [cl for cl in liste_clients if search_value in cl["label"]]

@app.callback(
    [Output('prenom_client', 'children'),
     Output('age_client', 'children'),
     Output('score_client', 'children')
    ],
    [dash.dependencies.Input('no_client', 'value')])
def update_output(value):
    if not value:
        raise PreventUpdate
    prenom, age, score = df.loc[df["id"]==value, ["prenom", "age", "score"]].values[0]
    return prenom, age, score
#        return 'Bonjour {}'.format(value)


##### CODE COPIE - A SUPPRIMER ###        
#options = [
#    {"label": "New York City", "value": "NYC"},
#    {"label": "Montreal", "value": "MTL"},
#    {"label": "San Francisco", "value": "SF"},
#]
#
#app.layout = html.Div(
#    [
#        html.Label(["Single dynamic Dropdown", dcc.Dropdown(id="my-dynamic-dropdown")]),
#        html.Label(
#            [
#                "Multi dynamic Dropdown",
#                dcc.Dropdown(id="my-multi-dynamic-dropdown", multi=True),
#            ]
#        ),
#    ]
#)
#
#
#@app.callback(
#    dash.dependencies.Output("my-dynamic-dropdown", "options"),
#    [dash.dependencies.Input("my-dynamic-dropdown", "search_value")],
#)
#def update_options(search_value):
#    if not search_value:
#        raise PreventUpdate
#    return [o for o in options if search_value in o["label"]]
#
#
#app.layout = html.Div([
#    dcc.Dropdown(
#        id='demo-dropdown',
#        options=[
#            {'label': 'New York City', 'value': 'NYC'},
#            {'label': 'Montreal', 'value': 'MTL'},
#            {'label': 'San Francisco', 'value': 'SF'}
#        ],
#        value='NYC'
#    ),
#    html.Div(id='dd-output-container')
#])
#
#
#@app.callback(
#    dash.dependencies.Output('dd-output-container', 'children'),
#    [dash.dependencies.Input('demo-dropdown', 'value')])
#def update_output(value):
#    return 'You have selected "{}"'.format(value)

#### FIN CODE COPIE ####

#@app.callback(
#    Output(component_id='info_client', component_property='children'),
#    [Input(component_id='no_client', component_property='value')]
#)
#def update_value(input_data):
#    return 'Bonjour  "{}"'.format(input_data)


if __name__ == '__main__':
    app.run_server(debug=True)

