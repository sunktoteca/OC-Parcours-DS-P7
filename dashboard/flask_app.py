#!/usr/bin/env python
# coding: utf-8

# Exemple
# https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-web-trader/app.py

#################
#### Imports #### 
#################

#import datetime

from flask import Flask
from flask import jsonify

import requests
import json

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

#import pandas as pd

#################
#### Constantes #### 
#################
URL_API = "http://laureP7.eu.pythonanywhere.com/api/clients"
#URL_API = "http://localhost:8050/"

PRENOMS_MASC = ["Gabriel", "Raphaël", "Léo", "Louis", "Lucas", "Adam", "Arthur", "Jules", "Hugo", "Maël",
    "Liam", "Ethan", "Paul", "Nathan", "Gabin", "Sacha", "Noah", "Tom", "Mohamed", "Aaron"]
PRENOMS_FEM = ["Emma", "Jade", "Louise", "Alice", "Chloé", "Lina", "Léa", "Rose", "Anna", "Mila", 
    "Inès", "Ambre", "Julia", "Mia", "Léna", "Manon", "Juliette", "Lou", "Camille", "Zoé"]

SEUIL = 0.3



#################
#### Serveur ####
#################
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    # routes_pathname_prefix='/dash/'
)

###################
#### Fonctions ####
###################
# API Requests for news div
#news_requests = requests.get(
#    "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=da8e2e705b914f9f86ed2e9692e66012"
#)
#
## API Call to update news
#def update_news():
#    json_data = news_requests.json()["articles"]
#    df = pd.DataFrame(json_data)
#    df = pd.DataFrame(df[["title", "url"]])
#    max_rows = 10
#    return html.Div(
#        children=[
#            html.P(className="p-news", children="Headlines"),
#            html.P(
#                className="p-news float-right",
#                children="Last update : "
#                + datetime.datetime.now().strftime("%H:%M:%S"),
#            ),
#            html.Table(
#                className="table-news",
#                children=[
#                    html.Tr(
#                        children=[
#                            html.Td(
#                                children=[
#                                    html.A(
#                                        className="td-link",
#                                        children=df.iloc[i]["title"],
#                                        href=df.iloc[i]["url"],
#                                        target="_blank",
#                                    )
#                                ]
#                            )
#                        ]
#                    )
#                    for i in range(min(len(df), max_rows))
#                ],
#            ),
#        ]
#    )


def get_data():
#    ref = requests.get(URL_API)
#    data_ref = json.loads(ref.content.decode('utf-8'))["data"]

    clients = requests.get(URL_API)
    data_clients = json.loads(clients.content.decode('utf-8'))["data"]
    
    return data_clients


##############################
#### Variables et données ####
##############################

colors = {
#    'background': '#1C1C1C',
    'text': 'red'
}


dico_clients = get_data()
liste_clients = []
for i in list(dico_clients.keys()):
    liste_clients.append({"label":i, "value":i})

#fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
#                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
#                     ])
                                
                                
@server.route('/api/ref/')
def ref():
    with open('./data/ref.json') as json_file:
        data = json.load(json_file)
    return jsonify({
      'status': 'ok', 
      'data': data
    })

@server.route('/api/clients/')
def clients():
    with open('./data/clients.json') as json_file:
        data = json.load(json_file)
    return jsonify({
      'status': 'ok', 
      'data': data
    })
   
######################
#### Mise en page ####
######################

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
        html.P("Numéro de client : ", style = {'margin':'20px 0 0 0'}),
        html.Div([
            dcc.Dropdown(
                id='no_client',
                options=liste_clients,
                style={
                       "padding" :"0px 20px 0px 0px",
                       "width" : "10em"}
                ),
            html.Div(id='nom_client',
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
            ),
            html.Div(id='type_contrat_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
            html.Div(id='montant_contrat_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
            html.Div(id='montant_annuite_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
            html.Div(id='revenu_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
            html.Div(id='duree_contrat_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
             html.Div(id='montant_achat_client',
                     style={ 'textAlign' : 'center',
                            "padding" :"20px",
                            'display' :'table-cell'}
            ),
                       
            ],
            style={'display':'table',
                   'margin' : '0 0 50px 0'
            }
        ),
        ######################
        ### Teableaux ###
        ######################
#        dash_table.DataTable(
#            id='table',
#            columns=[{"name": i, "id": i} for i in df.columns],
#            data=df.to_dict('records'),
#        ),
#        html.Div([
#                dcc.Graph(figure=fig)
#        ]),
#        html.Div([
#            html.Div(
#                className="div-news",
#                children=[html.Div(id="news", children=update_news())],
#                style={'display':'inline-block'}
#            ),
#            html.Div(
#                className="div-news",
#                children=[html.Div(id="news2", children=update_news())],
#                style={'display':'inline-block'}
#            )
#        ]),

        ######################
        ### Graphes ###
        ######################
        html.Div([
                dcc.Graph(
                        id='example1',
                        figure={
                                'data': [
                                    {'x': [1, 2], 'y': [1, 1], 'type': 'line', "line_width" :15, 'color' : 'green'},
                                    {'x': [1.5, 2.5], 'y': [2,2], 'type': 'line',  'color' : 'red'},
                                    {'x': [1.2], 'y': [1], 'marker': dict(color='blue', size=20, symbol="star-open")}
                                    ],
                                'layout': {
                                        'title': 'Donnée 1',
                                        "height": 300,
                                        "showlegend":False,
                                        #"margin" : "-20px",
                                        #"padding" : '-30px',
                                        "autosize":True,
                                        'margin':dict(l=0,r=20),
                                        "yaxis": {
                                            "fixedrange": True,
                                            "showline": False,
                                            "zeroline": False,
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "ticks": "",
                                            "color": "#a3a7b0",
                                            },
                                },
                        },
                        style={'width':'20%', 'display':'inline-block'}
                        ),
                dcc.Graph(
                        id='example2',
                        figure={
                                'data': [
                                    {'x': [1, 2], 'y': [1, 1], 'type': 'line', 'name': 'Boats', "line_width" :15, 'color' : 'green'},
                                    {'x': [1.5, 2.5], 'y': [2,2], 'type': 'line', 'name': 'Cars', 'color' : 'red'},
                                    {'x': [1.2], 'y': [1], 'marker': dict(color='blue', size=20, symbol="star-open")}
                                    ],
                                'layout': {
                                        'title': 'Donnée 2',
                                        "height": 300,
                                        "showlegend":False,
                                        #"margin" : "-20px",
                                        #"padding" : '-30px',
                                        "autosize":True,
                                        'margin':dict(l=20,r=20),
                                        "yaxis": {
                                            "fixedrange": True,
                                            "showline": False,
                                            "zeroline": False,
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "ticks": "",
                                            "color": "#a3a7b0",
                                            },

                                }
                        },
                        style={'width':'20%', 'display':'inline-block'}
                        ),
                dcc.Graph(
                        id='example3',
                        figure={
                                'data': [
                                    {'x': [1, 2], 'y': [1, 1], 'type': 'line', 'name': 'Boats', "line_width" :15, 'color' : 'green'},
                                    {'x': [1.5, 2.5], 'y': [2,2], 'type': 'line', 'name': 'Cars', 'color' : 'red'},
                                    {'x': [1.2], 'y': [1], 'marker': dict(color='blue', size=20, symbol="star-open")}
                                    ],
                                'layout': {
                                        'title': 'Donnée 3',
                                        "height": 300,
                                        "showlegend":False,
                                        #"margin" : "-20px",
                                        #"padding" : '-30px',
                                        "autosize":True,
                                        'margin':dict(l=20,r=20),
                                        "yaxis": {
                                            "fixedrange": True,
                                            "showline": False,
                                            "zeroline": False,
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "ticks": "",
                                            "color": "#a3a7b0",
                                            },

                                },
                        },
                        style={'width':'20%', 'display':'inline-block'}
                        ),
                dcc.Graph(
                        id='example4',
                        figure={
                                'data': [
                                    {'x': [1, 2], 'y': [1, 1], 'type': 'line', 'name': 'Boats', "line_width" :15, 'color' : 'green'},
                                    {'x': [1.5, 2.5], 'y': [2,2], 'type': 'line', 'name': 'Cars', 'color' : 'red'},
                                    {'x': [1.2], 'y': [1], 'marker': dict(color='blue', size=20, symbol="star-open")}
                                    ],
                                'layout': {
                                        'title': 'Donnée 4',
                                        "height": 300,
                                        "showlegend":False,
                                        #"margin" : "-20px",
                                        #"padding" : '-30px',
                                        "autosize":True,
                                        'margin':dict(l=20,r=20),
                                        "yaxis": {
                                            "fixedrange": True,
                                            "showline": False,
                                            "zeroline": False,
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "ticks": "",
                                            "color": "#a3a7b0",
                                            },

                                },
                        },
                        style={'width':'20%', 'display':'inline-block'}
                        ),
                dcc.Graph(
                        id='example5',
                        figure={
                                'data': [
                                    {'x': [1, 2], 'y': [1, 1], 'type': 'line', 'name': 'Boats', "line_width" :15, 'color' : 'green'},
                                    {'x': [1.5, 2.5], 'y': [2,2], 'type': 'line', 'name': 'Cars', 'color' : 'red'},
                                    {'x': [1.2], 'y': [1], 'marker': dict(color='blue', size=20, symbol="star-open")}
                                    ],
                                'layout': {
                                        'title': 'Donnée 5',
                                        "height": 300,
                                        "showlegend":False,
                                        #"margin" : "-20px",
                                        #"padding" : '-30px',
                                        "autosize":True,
                                        'margin':dict(l=20,r=0),
                                        "yaxis": {
                                            "fixedrange": True,
                                            "showline": False,
                                            "zeroline": False,
                                            "showgrid": False,
                                            "showticklabels": False,
                                            "ticks": "",
                                            "color": "#a3a7b0",
                                            },

                                },
                        },
                        style={'width':'20%', 'display':'inline-block'}
                        )
                ]),      

        ],
        style={
                'maxWidth':'1140px',
                'margin':'auto'
             }
        )

###################
#### Callbacks ####
###################


@app.callback(
    [Output('nom_client', 'children'),
     Output('age_client', 'children'),
     Output('score_client', 'children'),
     Output('type_contrat_client', 'children'),
     Output('montant_contrat_client', 'children'),
     Output('montant_annuite_client', 'children'),
     Output('revenu_client', 'children'),
     Output('duree_contrat_client', 'children'),
     Output('montant_achat_client', 'children')
    ],
    [Input('no_client', 'value')])
def update_output(value):
    if not value:
        raise PreventUpdate
    this_client = dico_clients[value]
    
    genre = this_client["CODE_GENDER"]
    # On ne connait pas le nom du client. on en invente un à partir d'une lsite
    if genre == 0:
        nom = "Mr " + PRENOMS_MASC[int(value)%len(PRENOMS_MASC)]
    else :
        nom = "Mme " + PRENOMS_FEM[int(value)%len(PRENOMS_FEM)]
    
    score = f'{this_client["score"]*100:.1f}'
    age = f'{-this_client["DAYS_BIRTH"]/365:.0f} ans'
    type_contrat = this_client["NAME_CONTRACT_TYPE"]
    montant_contrat = this_client["AMT_CREDIT"]
    montant_annuite = this_client["AMT_ANNUITY"]
    revenu = this_client["AMT_INCOME_TOTAL"]
    duree = f"{montant_contrat/montant_annuite*12:.1f} mois"
    montant_achat = this_client["AMT_GOODS_PRICE"]

    return nom, age, score, type_contrat, montant_contrat, montant_annuite, revenu, duree, montant_achat
#        return 'Bonjour {}'.format(value)

##############
#### Main ####
##############
if __name__ == '__main__':
    app.run_server(debug=True)

