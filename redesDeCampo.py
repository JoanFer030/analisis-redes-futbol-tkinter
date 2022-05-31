# Importamos librerias necesarias
from funcionesAux import *


def crear_red(match_id, seleccion, min_pases, cuadrantes_y, cuadrantes_x, destacar_pases, temp_id):
    #RED DE CAMPO
    df= load_file(match_id)
    dfs = load_file_season(11, temp_id)

    #EQUIPO Y ALINEACIÓN
    alineacion, equipo= titulares(df, seleccion)

    pases=df.query(f"type_name=='Pass' and team_name=='{equipo}' and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']  ")    #Crea df solo con pases correctos del equio elegido

    #DIBUJAR CAMPO
    numeroCuadrados=(cuadrantes_x,cuadrantes_y)

    xlist=list(np.arange(0,120,120/numeroCuadrados[0]))
    xlist.append(120)
    ylist=list(np.arange(0,80,80/numeroCuadrados[1]))
    ylist.append(80)
    pitch=Pitch(line_zorder=1, line_color='black')

    global ax
    fig, ax= pitch.draw(figsize=(10,15))
    ax.vlines(xlist,0,80,zorder=1, linestyles="--")
    ax.hlines(ylist,0,120,zorder=1, linestyles="--")


    equipos=df['team_name'].unique()
    ax.text(0,-2, f'{equipos[0]} vs {equipos[1]} {resultado(dfs, match_id)}', fontweight='bold' )
    ax.text(0, 82, f'{equipo}', fontweight='bold' )
    ax.quiver(55,82,40-30, 0, color='blue', alpha=1, zorder= 0, scale=1,scale_units='xy', angles='xy')
    ax.text(48, 82.5, 'Attack',fontweight='bold')


    numNodos=numeroCuadrados[0]*numeroCuadrados[1]

    nodos=[]
    for i in range(len(xlist)):
        xi=xlist[i]-(120/numeroCuadrados[0])/2
        for j in range(len(ylist)):
            yi=ylist[j]-(80/numeroCuadrados[1])/2
            if xi>0 and yi>0:
                nodos.append((xi,yi))
                
    dicEntrada={}
    dicSalida={}
    dicPases={}
    listPases=[]

    for elem in nodos:
        dicEntrada[elem]=0
        dicSalida[elem]=0
    for index, row in pases.iterrows():
        xy=row['location']
        xyend= row['pass_end_location']
        i=0
        while xy[0] > xlist[i]:
            i+=1
            pass
        xini= xlist[i]-(120/numeroCuadrados[0])/2
        i=0
        while xyend[0] > xlist[i]:
            i+=1
            pass
        xfin= xlist[i]-(120/numeroCuadrados[0])/2
        
        
        i=0
        while xy[1] > ylist[i]:
            i+=1
            pass
        yini= ylist[i]-(80/numeroCuadrados[1])/2
        
        i=0
        while xyend[1] > ylist[i]:
            i+=1
            if i+1 > len(ylist):
                i = len(ylist)-1
                break
            pass
        yfin= ylist[i]-(80/numeroCuadrados[1])/2       
        dicSalida[(xini,yini)]+=1
        dicEntrada[(xfin,yfin)]+=1
        if ((xini,yini),(xfin,yfin)) not in listPases:
            listPases.append(((xini,yini),(xfin,yfin)))
            dicPases[((xini,yini),(xfin,yfin))]=1
        else:

            dicPases[((xini,yini),(xfin,yfin))]+=1

    if destacar_pases:
        for pase in listPases:
            if dicPases[pase]>min_pases:
                ax.quiver(pase[0][0],pase[0][1],pase[1][0]-pase[0][0], pase[1][1]-pase[0][1], alpha=0.8, zorder= 1, scale=1,scale_units='xy', angles='xy', headlength=5, color='red')
            else:
                ax.quiver(pase[0][0],pase[0][1],pase[1][0]-pase[0][0], pase[1][1]-pase[0][1], alpha=0.5, zorder= 0, scale=1,scale_units='xy', angles='xy', headlength=5, color='blue')
        for elem in nodos:
            ax.scatter(elem[0], elem[1], s=(dicEntrada[elem]+dicSalida[elem])**1.2, color='orange',edgecolors='black', alpha=1)

    else:
        for pase in listPases:
            if dicPases[pase]>min_pases:
                ax.quiver(pase[0][0],pase[0][1],pase[1][0]-pase[0][0], pase[1][1]-pase[0][1], color='blue', alpha=1, zorder= 0, scale=1,scale_units='xy', angles='xy')

        for elem in nodos:
            ax.scatter(elem[0], elem[1], s=(dicEntrada[elem]+dicSalida[elem])**1.2, color='orange',edgecolors='black', alpha=1)
