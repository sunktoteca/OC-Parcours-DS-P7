#!/usr/bin/env python
# coding: utf-8

# Exemple
# https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-web-trader/app.py

#################
#### Imports #### 
#################

#import datetime

from flask import Flask
#from flask import jsonify
from flask import render_template

import requests
import json

#import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

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

SEUIL = 10

#Liste des colonnes pour les colonnes sélectionnées par l'utilisateur
#Pour l'instant ce sont les colonnes de la table principale (à l'exception de quelques unes)
#A préciser avec le client.
LISTE_COLONNES = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 
   'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_TYPE_SUITE', 
   'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'REGION_POPULATION_RELATIVE', 
   'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE',
   'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 
   'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY', 'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START', 
   'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY', 
   'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 
   'EXT_SOURCE_3', 'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 
   'COMMONAREA_AVG', 'ELEVATORS_AVG', 'ENTRANCES_AVG', 'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG', 
   'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG', 'NONLIVINGAREA_AVG', 'APARTMENTS_MODE', 
   'BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE', 'YEARS_BUILD_MODE', 'COMMONAREA_MODE', 'ELEVATORS_MODE', 
   'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE', 'LANDAREA_MODE', 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE', 
   'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE', 'APARTMENTS_MEDI', 'BASEMENTAREA_MEDI', 
   'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI', 'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI', 
   'FLOORSMAX_MEDI', 'FLOORSMIN_MEDI', 'LANDAREA_MEDI', 'LIVINGAPARTMENTS_MEDI', 'LIVINGAREA_MEDI', 
   'NONLIVINGAPARTMENTS_MEDI', 'NONLIVINGAREA_MEDI', 'FONDKAPREMONT_MODE', 'HOUSETYPE_MODE', 'TOTALAREA_MODE', 
   'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE', 'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 
   'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 'AMT_REQ_CREDIT_BUREAU_HOUR', 
   'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 
   'AMT_REQ_CREDIT_BUREAU_YEAR']

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

    if MODE == 'LOCAL':
        with open('../api/data/clients.json') as json_file:
            data_clients = json.load(json_file)
        with open('../api/data/histo.json') as json_file:
            data_histo = json.load(json_file)

    else :
        app.logger.info('Before') 
        server.logger.info('server logger') 
        response = requests.get(URL_API)
        if response.status_code != 200:
#            raise ValueError(response)  #a remettre si on utilise le errorhandler
            raise ValueError(response.status_code, response.reason, response.url)
           
        content = json.loads(response.content.decode('utf-8'))
        data_clients = content["clients"]
        data_histo = content["histo"]
    
    return data_clients, data_histo

#Pour l'instant ceci n'est pas utilisé car si il y a une erreur sur get_data, 
#elle se produit avant la creation de app.layout et donc avant que le serveur ne soit
#reellement lancé. Ce serait utilisé si l'erreur se produisait dans une route définie
# par @serveur.route("/").
# Mais on ne peut pas mettre app.layout dans une route. 
# Il faudrait revoir l'architecture
# En attendant, le message d'erreur s'affiche dans la console.
@server.errorhandler(ValueError)
def erreurExcept(error):
    return render_template("erreur.html", 
                           no_erreur=error.args[0].status_code, 
                           cause_erreur=error.args[0].reason,
                           url=error.args[0].url)


##############################
#### Variables et données ####
##############################

colors = {
#    'background': '#1C1C1C',
    'text': 'red'
}



dico_clients, dico_histo = get_data()
liste_clients = []
for i in list(dico_clients.keys()):
    liste_clients.append({"label":i, "value":i})
liste_colonnes = []
for i in LISTE_COLONNES:
    liste_colonnes.append({"label":i, "value":i})
df_histo = pd.DataFrame(dico_histo)


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
                                            'margin': 'auto'
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
        
        html.Div([
            html.Div([
                html.Label("Numéro de client : "),
                dcc.Dropdown(
                    id='no_client',
                    options=liste_clients,
#                    style={
#                          # "padding" :"0px 20px 0px 0px",
#                           "width" : "10em",
#                           "display":"inline_block"}
                    ),
                ],
                    className="selection",
            ),
            html.Div([
                html.Label("Données complémentaires : "),
                dcc.Dropdown(
                    id='more_data',
                    options=liste_colonnes,
                    multi=True,
                    value=['DAYS_BIRTH', 'AMT_INCOME_TOTAL', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 
                            'AMT_GOODS_PRICE']
#                    style={
#                          # "padding" :"0px 20px 0px 0px",
#                           "display":"inline_block"}
                    ),
                ],
                    id='box_more_data',
                    className="selection",
            ),
            ],
            className="bloc_selection",
        ),
        html.Div([
            html.Div([
                html.Div(
                        [html.P(id='nom_client',), html.Label("nom")],                        
                        className="info_client",
                        
                ), 
                html.Div([html.P(id='type_contrat_client'), html.Label("type contrat")], 
                        className="info_client",
                ),
                html.Div([html.P(id='montant_contrat_client'), html.Label("montant contrat")], 
                        className="info_client",
                ),
                html.Div([html.P(id='duree_contrat_client'), html.Label("duree contrat")], 
                        className="info_client",
                ),
                html.Div([html.P(id='score_client', style={"color":"blue", "box-shadow": "4px 4px 3px lightgrey"}, ), 
                          html.Label("score")
                        ],
                        id='box_score_client',
                        className="info_client_score"                                        
                ),
                ],
                className="ligne_info_client"
            ),
            html.Div([                                                             
                html.Div([html.P(id='libre_1',), html.Label(" ", id="label_libre_1")],  
                        className="info_client",
                ),
                html.Div([html.P(id='libre_2',), html.Label(id="label_libre_2")],  
                        className="info_client",
                ),
                 html.Div([html.P(id='libre_3',), html.Label(id="label_libre_3")],  
                        className="info_client",
                ), 
                 html.Div([html.P(id='libre_4',), html.Label(id="label_libre_4")],  
                        className="info_client",
                ), 
                 html.Div([html.P(id='libre_5',), html.Label(id="label_libre_5")],  
                        className="info_client",
                ), 
                          
                ],
                className="ligne_info_client"
            ),
            ],
                className="bloc_info_client"
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
        html.Div([
            html.H2("Répartition des scores"),

            html.Div([
                html.Div([
                    html.Label("Homme/Femme/XNA : "),
                    dcc.Checklist(
                        options=[
                            {'label': 'Homme', 'value': 'M'},
                            {'label': 'Femme', 'value': 'F'},
                            {'label': 'XNA', 'value': 'XNA'}
                        ],
                        value=['M', 'F', 'XNA'],
                        id="ckl_HF",
                    )
                    ],                    
                    className="selection",
                ),
#                html.Div([
#                    html.Label("Niveau d'études: "),
#                    dcc.Checklist(
#                        options=[
#                            {'label': 'Lower secondary', 'value': 'LS'},
#                            {'label': 'Secondary / secondary special', 'value': 'S'},
#                            {'label': 'Incomplete higher', 'value': 'IH'},
#                            {'label': 'Higher education', 'value': 'H'},
#                            {'label': 'Academic degree', 'value': 'A'},
#                        ],
#                        value=['LS', 'S', 'IH', 'H', 'A'],
#                        id="ckl_etudes",
#                    )  ,
#                    ],
#                        className="selection",
#                ),
                html.Div([
                    html.Label("Revenu annuel: "),                        
                    dcc.RangeSlider(
                        min=0,
                        max=300_000,
                        step=1000,
                        value = [0, 300_000],
                        tooltip={'placement':'top'},
                        marks={
                            0: {'label': '0 °C'},
                            100_000: {'label': '100 000'},
                            200_000: {'label': '200 000'},
                            300_000: {'label': '>300 000'}
                        },
                        id="slider_revenu",
                    )
                ],
                    className="selection",
                ),
                ],
                className="bloc_selection",
                ),
    
            html.Div([                                                             
                dcc.Graph(
                    id='graph_score_distrib',
                ),
            ],
                className="bloc_info_client"
            ),


        ]),
               

        ],
        id='layout',
#        style={
#                'maxWidth':'80%',
#                'margin':'auto'
#             }
        )

#############################
#### Callbacks dashbaord ####
#############################
@app.callback(
    [Output('nom_client', 'children'),
     Output('score_client', 'children'),
     Output('type_contrat_client', 'children'),
     Output('montant_contrat_client', 'children'),
     Output('duree_contrat_client', 'children'),
     Output('libre_1', 'children'),
     Output('libre_2', 'children'),
     Output('libre_3', 'children'),
     Output('libre_4', 'children'),
     Output('libre_5', 'children'),
     Output('label_libre_1', 'children'),
     Output('label_libre_2', 'children'),
     Output('label_libre_3', 'children'),
     Output('label_libre_4', 'children'),
     Output('label_libre_5', 'children'),
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
    [Input('no_client', 'value'),
     Input('more_data', 'value')])
def update_output(no_client, more_data):
    if not no_client:
        raise PreventUpdate
    this_client = dico_clients[no_client]
    
    genre = this_client["CODE_GENDER"]
    # On ne connait pas le nom du client. on en invente un à partir d'une liste
    if genre == 'M':
        nom = "Mr " + PRENOMS_MASC[int(no_client)%len(PRENOMS_MASC)]
    else :
        nom = "Mme " + PRENOMS_FEM[int(no_client)%len(PRENOMS_FEM)]
    
    score = f'{this_client["score"]*100:.1f}'
    type_contrat = this_client["NAME_CONTRACT_TYPE"]
    montant_contrat = this_client["AMT_CREDIT"]
    montant_annuite = this_client["AMT_ANNUITY"]
    duree = f'{montant_contrat/montant_annuite*12:.0f} mois'
    montant_contrat = f'{montant_contrat:_.0f}'.replace("_", " ") + " €"
    
    libres=[]
    labels_libres=[]
    for info in more_data:
        libres.append(this_client[info])
        labels_libres.append(info)
    while len(libres) < 5:
        libres.append("")
        labels_libres.append("")
    
    figures_fav = []
    figures_risq = []
    for i in range(5):
        for cas in range(2):
            if cas == 0:
                facteur = "favorable_" + str(i+1)
            else :
                facteur = "risque_"+str(i+1)
            facteur_name = this_client[facteur]["name"]
            if this_client[facteur]["type"]=="quant":
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
            else:
                x = this_client[facteur]["x"]
                y0 = this_client[facteur]["y0"]
                y1 = this_client[facteur]["y1"]
                client_value = this_client[facteur_name]
                data = [
                    {'x': x, 'y': y0, 'type': 'bar', 'marker': dict(color='green')},
                    {'x': x, 'y': y1, 'type': 'bar', 'marker': dict(color='red')},
                    {'x': [client_value], 'y':[1], 'marker': dict(color='blue', size=20, symbol="star")}
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
                },
                "xaxis":{
                    "zeroline" : False,}
            }
            figure = dict(data = data, layout = layout)  
            if cas == 0:
                figures_fav.append(figure)
            else:
                figures_risq.append(figure)
    
    return nom, score, type_contrat, montant_contrat, duree,  \
        libres[0], libres[1], libres[2], libres[3], libres[4],\
        labels_libres[0], labels_libres[1],  labels_libres[2], labels_libres[3], labels_libres[4], \
        figures_fav[0], figures_fav[1], figures_fav[2], figures_fav[3], figures_fav[4],\
        figures_risq[0], figures_risq[1], figures_risq[2], figures_risq[3],figures_risq[4]


@app.callback([Output('score_client', 'style'), Output('box_score_client', 'style')], 
               [Input('score_client', 'children')])
def update_style(value):
    if float(value) > SEUIL:
        return {'color': 'red'}, {"box-shadow": "4px 4px 3px tomato"}
    else :
        return {'color': 'green'}, {"box-shadow": "4px 4px 3px lightgreen"}

@app.callback(
    Output('graph_score_distrib', 'figure'),
    [Input('ckl_HF', 'value'),
     Input('slider_revenu', 'value')])
def update_histo(ckl_HF, slider_revenu):
#    cond = f"(df_histo['CODE_GENDER'].apply(lambda x: x in {ckl_HF}))"
#    cond = cond + f" & (df_histo['AMT_INCOME_TOTAL']>= {slider_revenu[0]})"
#    if slider_revenu[1] < 300_000:
#        cond = cond + f" & (df_histo['AMT_INCOME_TOTAL']<= {slider_revenu[1]})"
    query = f"CODE_GENDER in {ckl_HF}"
    query += f" and AMT_INCOME_TOTAL >= {slider_revenu[0]}"
    if slider_revenu[1] < 300_000:
        query += f" and AMT_INCOME_TOTAL <= {slider_revenu[1]}"
#    app.logger.info('query', query) 
    array, bins = np.histogram(df_histo.query(query)["score"], bins=50, range=(0,100))
    data = [
        {'x': bins, 'y': array, 'type': 'bar'},                   
    ]
    layout = {
                'title': {"text": "Répartition des scores",
                          "font": {"size":24}},
                "height": 300,
                "showlegend":False,
                "autosize":True,
#                'margin':dict(l=0,r=20),
                "yaxis": {
#                    "fixedrange": True,
                    "showline": True,
                    "zeroline": True,
#                    "showgrid": False,
#                    "showticklabels": False,
#                    "ticks": "",
#                    "color": "#a3a7b0",
                },
                "xaxis":{
#                    "zeroline" : False,
                     "nticks":51, #np.arange(51),
                     "tick0":0,
                     "dtick":2,
                     "showticklabels": True,
                     "fixedrange": True,
                     "range": [0, 100],
                     "title":"score",
                }
    }

    figure = dict(data = data, layout = layout)  
    return figure
    
    

##############
#### Main ####
##############
if __name__ == '__main__':
    app.run_server(debug=False)

