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

#import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

#import pandas as pd

#################
#### Constantes #### 
#################
#MODE = 'LOCAL'
MODE = 'SERVEUR'

URL_API = "http://laure.eu.pythonanywhere.com/api/clients"
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
def get_data():
#    ref = requests.get(URL_API)
#    data_ref = json.loads(ref.content.decode('utf-8'))["data"]

    if MODE == 'LOCAL':
        with open('./data/clients.json') as json_file:
            data_clients = json.load(json_file)

    else :
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
                                
                                
#@server.route('/api/ref/')
#def ref():
#    with open('./data/ref.json') as json_file:
#        data = json.load(json_file)
#    return jsonify({
#      'status': 'ok', 
#      'data': data
#    })

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
        html.H2("Informations demandeur"),
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
#                     style={ 'textAlign' : 'center',
#                            "padding" :"20px",
#                            'display' :'table-cell'},
                    className="info_client",
            ), 
            html.Div(id='age_client',
                    className="info_client",
            ),
            html.Div(id='score_client',
                    className="info_client",
            ),
            html.Div(id='type_contrat_client',
                    className="info_client",
            ),
            html.Div(id='montant_contrat_client',
                    className="info_client",
            ),
            html.Div(id='montant_annuite_client',
                    className="info_client",
            ),
            html.Div(id='revenu_client',
                    className="info_client",
            ),
            html.Div(id='duree_contrat_client',
                    className="info_client",
            ),
             html.Div(id='montant_achat_client',
                    className="info_client",
            ),
                       
            ],
            style={'display':'table',
                   'margin' : '0 0 50px 0'
            }
        ),

        ######################
        ### Graphes ###
        ######################
        html.H2("Zones de risque"),
            dcc.Graph(
                    id='risq_graph_1',
                    #style={'width':'20%', 'display':'inline-block', "height": 300}
                    className="facteur",
                    ),
             dcc.Graph(
                    id='risq_graph_2',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='risq_graph_3',
                    className="facteur"
                    ),
            dcc.Graph(
                    id='risq_graph_4',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='risq_graph_5',
                    className="facteur",
                    ),               
        html.H2("Critères favorables"),
            dcc.Graph(
                    id='fav_graph_1',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='fav_graph_2',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='fav_graph_3',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='fav_graph_4',
                    className="facteur",
                    ),
            dcc.Graph(
                    id='fav_graph_5',
                    className="facteur",
                    ),
               

        ],
        style={
                'maxWidth':'80%',
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
     Output('montant_achat_client', 'children'),
     Output('fav_graph_1', 'figure'),
     Output('fav_graph_2', 'figure'),
     Output('fav_graph_3', 'figure'),
     Output('fav_graph_4', 'figure'),
     Output('fav_graph_5', 'figure'),
     Output('risq_graph_1', 'figure'),
     Output('risq_graph_2', 'figure'),
     Output('risq_graph_3', 'figure'),
     Output('risq_graph_4', 'figure'),
     Output('risq_graph_5', 'figure'),     
    ],
    [Input('no_client', 'value')])
def update_output(value):
    if not value:
        raise PreventUpdate
    this_client = dico_clients[value]
    
    genre = this_client["CODE_GENDER"]
    # On ne connait pas le nom du client. on en invente un à partir d'une liste
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
    
    figures_fav = []
    figures_risq = []
    for i in range(5):
        for cas in range(2):
            if cas == 0:
                facteur = "favorable_" + str(i+1)
            else :
                facteur = "risque_"+str(i+1)
            facteur_name = this_client[facteur]["name"]
            fqb = this_client[facteur]["fqb"]
            fqh = this_client[facteur]["fqh"]
            fm = this_client[facteur]["fm"]
            rqb = this_client[facteur]["rqb"]
            rqh = this_client[facteur]["rqh"]
            rm = this_client[facteur]["rm"]
            client_value = this_client[facteur_name]
            
            data = [
                {'x': [fqb, fqh], 'y': [1, 1], 'type': 'line', 'line' : dict(width=5, color='green'), 
                     'marker': dict(size=5)},                   
                {'x': [rqb, rqh], 'y': [2,2], 'type': 'line', 'line' : dict(width=5, color='red'),
                     'marker': dict(size=5)},
                {'x': [fm], 'y': [1], 'marker': dict(color='green', size=10, symbol="diamond")},
                {'x': [rm], 'y': [2], 'marker': dict(color='red', size=10, symbol="diamond")},
                {'x': [client_value], 'y': [cas+1], 'marker': dict(color='blue', size=20, symbol="star")}
           ]
            
            layout = {
                'title': facteur_name,
#                "height": 300,
                "showlegend":False,
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
                }
            }
            figure = dict(data = data, layout = layout)  
            if cas == 0:
                figures_fav.append(figure)
            else:
                figures_risq.append(figure)
    
    return nom, age, score, type_contrat, montant_contrat, montant_annuite, revenu, duree, montant_achat, \
        figures_fav[0], figures_fav[1], figures_fav[2], figures_fav[3], figures_fav[4],\
        figures_risq[0], figures_risq[1], figures_risq[2], figures_risq[3],figures_risq[4]

##############
#### Main ####
##############
# https://help.pythonanywhere.com/pages/502BadGateway
if __name__ == '__main__':
    app.run_server(debug=True)

