import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import requests
import json
import numpy as np
from mplsoccer import Pitch, VerticalPitch
from scipy.spatial import ConvexHull
from scipy import stats
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap


def load_file(match_id):
    resp = requests.get(f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json")
    match_dict = json.loads(resp.text)
    df = pd.json_normalize(match_dict, sep="_")
    return df

def load_file_lineup(match_id):
    resp = requests.get(f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/{match_id}.json")
    match_dict = json.loads(resp.text)
    df = pd.json_normalize(match_dict, sep="_")
    return df

def load_file_season(competition_id=11, season_id=90):
    resp = requests.get(f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json")
    match_dict = json.loads(resp.text)
    df = pd.json_normalize(match_dict, sep="_")
    return df

def load_competitions():
    resp = requests.get(f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json")
    match_dict = json.loads(resp.text)
    df = pd.json_normalize(match_dict, sep="_")
    return df

def resultado(df, match_id):
    for index, row in df.iterrows():
        if row['match_id']==int(match_id):
            return f"{row['home_score']}-{row['away_score']}"
        else:
            pass
def numeros(df, equipo):
    dicNum={}
    if equipo == df['team_name'][0]:
        iniciales = df['lineup'][0]
    elif equipo == df['team_name'][1]:
        iniciales = df['lineup'][1]
    for i in range(len(iniciales)):
        dicNum[iniciales[i]['player_name']]=iniciales[i]['jersey_number']
    return dicNum

def goles(df):
    dictGoles={}
    for index, row in df.iterrows():
        if row['shot_outcome_name']=='Goal': 
            dictGoles[index]={'jugador':row['player_name'], 'equipo':row['possession_team_name'],'parte': row['period'],'minuto':row['timestamp'],'posesion':row['possession'],  'location':row['location'], 'end_location':row['shot_end_location']}
    return dictGoles

def total_pases_equipos(df, equipo):
    pases=df.query(f"type_name=='Pass' and team_name=='{equipo}' and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete'] ")
    total_pases= pases.shape[0]
    return total_pases

def cambios(df, equipo):
    dictCambios={}
    for index, row in df.iterrows():
        if row['type_name']=='Substitution' and row['team_name']== equipo:
            dictCambios[index]={'sale':row['player_name'],'entra':row['substitution_replacement_name'], 'equipo':row['team_name'], 'parte': row['period'],'minuto':row['timestamp']}
    return dictCambios

def formacion(df):
    dictFormacion={}
    for index, row in df.iterrows():
        if row['type_name']=='Starting XI':
            dictFormacion[row['team_name']]=str(int(row['tactics_formation']))
        elif row['type_name']=='Tactical Shift':
            dictFormacion['cambio']={ 'index':index, 'Equipo':row['team_name'], 'minuto':row['timestamp'], 'nueva_formacion':str(int(row['tactics_formation']))}
    return dictFormacion

def titulares(df, seleccion):
    if seleccion == 'local':
        iniciales = df['tactics_lineup'][0]
        alineacion=[]
        equipo=df['team_name'][0]
    elif seleccion == 'visitante':
        iniciales = df['tactics_lineup'][1]
        alineacion=[]
        equipo=df['team_name'][1]
    for i in range(len(iniciales)):
        jug= iniciales[i]['player']['name']
        alineacion.append(jug)
    return alineacion, equipo

def Jugadores(df):
    jugadores= df['player_name'].unique()
    reciben = df['pass_recipient_name'].unique()
    return list(set(jugadores).union(set(reciben)))

def portero_rival(df, equipo):
    if equipo == 'local':
        iniciales = df['tactics_lineup'][0]
    elif equipo == 'visitante':
        iniciales = df['tactics_lineup'][1]

    return iniciales[0]['player']['name']


def posicion_nodo(df, jugador):
    """
    Calcula la posicion media de un jugador a lo largo de todo el partido.
    
    """
    try:
        dfJug =df.loc[df['player_name']==jugador,['location']]
        x=[]
        y=[]
        for row in dfJug.iterrows():
            try:
                x.append(row[1][0][0])
                y.append(row[1][0][1])
            except: pass

        x= sum(x)/len(x)
        y= sum(y)/len(y)
    except:
        dfJug =df.loc[df['pass_recipient_name']==jugador,['pass_end_location']]
        x=[]
        y=[]
        for row in dfJug.iterrows():
            try:
                x.append(row[1][0][0])
                y.append(row[1][0][1])
            except: pass

        x= sum(x)/len(x)
        y= sum(y)/len(y)
    return x, y
    
def tamano_nodo(numPases, jugador):
    """
    Se calcula el tamaño de los nodos y de la letra del nombre según el número de pases que ha dado el jugador. Para el tamaño se cálcula el peso máximo al q se le asigna un tamaño de 3500 y a partir de ese se calcula proporcionalmente los demas.
    Para el tamaño de la letra se calcula proporcionalmente al número de pases pero se establece un minimo de 8 para que sea legible.

    """

    num_pases_max = numPases[max(numPases, key=numPases.get)]
    tamaño=numPases[jugador]*3000/num_pases_max
    fontsize=numPases[jugador]*20/num_pases_max
    if fontsize < 10:
        fontsize=10

    if int(tamaño) == 0:
        tamaño = 200

    return tamaño, fontsize

def arista(jugador, recibidor, pesos):
    """
    Se calcula el color y grosor de la arista. Para el color se crean los percentiles y se establecen colores para los pases que esten en esos rango.
    Para el grosor se cálcula el peso máximo al q se le asigna un tamaño de 20 y a partir de ese se calcula proporcionalmente los demas.
    """
    try:
        pesojug=pesos[(jugador, recibidor)]
    except:
        pesojug=pesos[(recibidor, jugador)]
    peso_max=max(pesos.values)
    peso_min=min(pesos.values)
    linewidth = pesojug*18/peso_max
    opacidad = (pesojug-peso_min)/(peso_max-peso_min)
    
    if opacidad < 0.3:
        opacidad=0.3
    elif np.isnan(opacidad):
        opacidad=0.3
    return linewidth, opacidad

def arista_tiro(jugador, pesos):
    """
    Se calcula el color y grosor de la arista. Para el color se crean los percentiles y se establecen colores para los pases que esten en esos rango.
    Para el grosor se cálcula el peso máximo al q se le asigna un tamaño de 20 y a partir de ese se calcula proporcionalmente los demas.
    """
    pesojug=pesos[jugador]
    peso_max=max(pesos.values)
    peso_min=min(pesos.values)
    linewidth = pesojug*18/peso_max
    opacidad = (pesojug-peso_min)/(peso_max-peso_min)
    
    if opacidad < 0.3:
        opacidad=0.3
    elif np.isnan(opacidad):
        opacidad=0.3
    return linewidth, opacidad

def recortar_df(df, ini, fin, parte):
    if parte == 1:
        for index, row in df.iterrows():
            if row['period']==2:
                df_ini = 0
                df_fin= index
                break

    elif parte == 2:
        for index, row in df.iterrows():
            if row['period']==2:
                df_ini = index
                df_fin= len(df)-1
                break
    elif parte == 3:
        df_ini = 0
        df_fin = len(df)-1
    else:
        for index, row in df.iterrows():
            if row['minute'] == ini:
                df_ini= index
                break
        for index, row in df[df_ini:].iterrows():    
            if row['minute'] >= fin:
                df_fin = index
                break

    return df[df_ini:df_fin]

def xg_acum(dic_xg):
    dic_aux = {0:0}
    lis = list(dic_xg.items())
    for i in range(len(lis)):
        suma = 0
        for j in lis[:i]:
            suma += j[1]
        dic_aux[lis[i][0]] = suma
    return dic_aux
            
def xg(df):
    dic_xg = {}
    for index, row in df.iterrows():
        dic_xg[row["minute"]+round(row["second"]/60, 2)] = row["shot_statsbomb_xg"]
    acum = xg_acum(dic_xg)
    if list(acum.keys())[-1] < 90:
        acum[90] = acum[max(acum, key=acum.get)]
    return acum

def min_gol(df):
    lis  =  []
    for index, row in df.iterrows():
        if row['shot_outcome_name']=='Goal':
            lis.append(row["minute"]+round(row["second"]/60, 2))

    return lis

def desplegable_opciones(id):
    df = load_file_season(11, id)
    df = df.sort_values("match_week", ascending=True)
    dic = {}
    for index, row in df.iterrows():
        dic[f"J{row['match_week']}  {row['home_team_home_team_name']} - {row['away_team_away_team_name']} | {row['home_score']}-{row['away_score']}"] = row['match_id']
    
    return dic

def desplegable_temp():
    df = load_competitions()
    df = df.loc[df["competition_id"]==11]
    dic = {}
    for index, row in df.iterrows():
        dic[f"{row['competition_name']} - {row['season_name']}"] = row['season_id']
    return dic