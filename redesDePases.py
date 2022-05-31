#FUNCIONES NECESARIAS
from funcionesAux import *

# Crear red partido completo
def crear_red_partido_completo(match_id, seleccion, cambio, temp_id):
    df=load_file(match_id)
    dfl=load_file_lineup(match_id)
    dfs=load_file_season(11,temp_id)

    #DEFINIR CAMPO
    pitch = Pitch(pitch_type = 'statsbomb', pitch_color = '#283747', line_color = 'white',  pad_right = 70)
    global ax
    fig, ax = pitch.draw(figsize=(16, 9))

    #PREPARACION VARIABLES
    iniciales, equipo = titulares(df, seleccion)
    total= total_pases_equipos(df, equipo)
    equipos = df['team_name'].unique()

    num = numeros(dfl, equipo)
    pases = df.query(f"type_name=='Pass'  and team_name=='{equipo}' and pass_type_name not in ['Throw-in'] and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']")
    jugadores = Jugadores(pases)
    numPases = dict(pases['player_name'].value_counts())
    aristas = pases.groupby(['player_name', 'pass_recipient_name']).size()

    for jugador in jugadores:
        if jugador not in numPases:
            numPases[jugador]=0

    pesos={}
    for clave in dict(aristas):
        if clave in pesos or (clave[1],clave[0]) in pesos:
            try:
                pesos[clave]+= aristas[clave]
            except:
                pesos[(clave[1],clave[0])]+= aristas[clave]
        else:
            pesos[clave]=aristas[clave]


    #DIBUJAR NODOS

    for jugador in jugadores:
        if jugador in iniciales:
            x, y = posicion_nodo(pases, jugador)
            tamaño, fs=tamano_nodo(numPases, jugador)
            ax.scatter(x, y, alpha=1, s=tamaño, color='#F39C12', edgecolors='black', zorder=1) 
            ax.text(x, y, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center")  #' '.join(jugador.split()[0:2])
        elif cambio:
            x, y = posicion_nodo(pases, jugador)
            tamaño, fs=tamano_nodo(numPases, jugador)
            ax.scatter(x, y, alpha=1, s=tamaño, color='grey',edgecolors='black', zorder=1)
            ax.text(x, y, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center")  #' '.join(jugador.split()[0:2])
        else: pass

    #DIBUJAR ARISTAS

    if cambio:
        for jugador in jugadores:
            if numPases[jugador] > 0:
                recibidores = aristas[jugador].index
                for recibidor in recibidores:
                    linewidth, opacidad = arista(jugador, recibidor, aristas)
                    x, y=posicion_nodo(pases, jugador)
                    xr,yr=posicion_nodo(pases, recibidor)
                    pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=ax, zorder=0)
                    
    elif not cambio:
        for jugador in iniciales:
            if numPases[jugador] > 0:
                recibidores = aristas[jugador].index
                for recibidor in recibidores:
                    if recibidor in iniciales:
                        linewidth, opacidad = arista(jugador, recibidor, aristas)
                        x, y=posicion_nodo(pases, jugador)
                        xr,yr=posicion_nodo(pases, recibidor)
                        pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=ax, zorder=0)


    #TEXTOS
    resul = resultado(dfs, match_id)
    ax.text(1.5, 78, f'{equipo}', fontweight='bold', color='white',fontsize=15 )
    ax.text(95, 78, f'Total pases: {total}', fontweight='bold', color='white',fontsize=15 )
    ax.text(1.5, 3, f'{equipos[0]} vs {equipos[1]}   {resul}', fontweight='bold', color='white', fontsize= 15)
    x=125
    y=5
    for clave in jugadores:
        if len(clave) > 30:
            ax.text(x, y, f'{num[clave]}: {clave[0:30]}...', fontweight='bold', fontsize=12,  color='white' )
            y+=2.5
        else:
            ax.text(x, y, f'{num[clave]}: {clave}', fontweight='bold', fontsize=12,  color='white' )
            y+=2.5

    sust = cambios(df, equipo)
    ax.text(125, 55, 'Cambios:', fontweight='bold', fontsize=15,  color='white')
    y2=60

    for clave in sust:
        jug1=sust[clave]['sale']
        jug2=sust[clave]['entra']
        minuto=sust[clave]['minuto']
        parte=sust[clave]['parte']
        minuto=int(minuto.split(':')[1])
        if parte==2:
            minuto += 45
        ax.text(125, y2, f"{minuto}':  {num[jug1]} ⇄ {num[jug2]}", fontweight='bold', fontsize=12,  color='white')
        y2+=2.5

    goals = goles(df)
    ax.text(150, 55, 'Goles:', fontweight='bold', fontsize=15,  color='white')
    y2=60

    for clave in goals:
        jug=goals[clave]['jugador']
        equipo=goals[clave]['equipo']
        num = numeros(dfl, equipo)
        minuto=goals[clave]['minuto']
        parte=goals[clave]['parte']
        minuto=int(minuto.split(':')[1])
        if parte==2:
            minuto += 45
            ax.text(150, y2, f"{minuto}':  {num[jug]} {equipo}", fontweight='bold', fontsize=12,  color='white')
        ax.text(150, y2, f"{minuto}':  {num[jug]} {equipo}", fontweight='bold', fontsize=12,  color='white')
        y2+=2.5


def crear_red_temporal(match_id, seleccion, cambio, temp_id,desde_minuto=0, hasta_minuto=90, parte=0):
    df=load_file(match_id)
    dfl=load_file_lineup(match_id)
    dfs=load_file_season(11,temp_id)
    
    #DEFINIR CAMPO
    pitch = Pitch(pitch_type = 'statsbomb', pitch_color = '#283747', line_color = 'white', pad_right = 70)
    global ax
    fig, ax = pitch.draw(figsize=(16, 9))
    if parte==1:
        franja="1º parte"
    elif parte == 2:
        franja="2º parte"
    else:
        franja= f"{desde_minuto}' - {hasta_minuto}'"

    #PREPARACION VARIABLES
    iniciales, equipo = titulares(df, seleccion)
    df_franja=recortar_df(df, desde_minuto, hasta_minuto, parte)
    pases = df_franja.query(f"type_name=='Pass'  and team_name=='{equipo}' and pass_type_name not in ['Throw-in'] and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']")
    total= total_pases_equipos(df_franja, equipo)
    equipos = df['team_name'].unique()
    jugadores = Jugadores(pases)
    num = numeros(dfl, equipo)
    numPases = dict(pases['player_name'].value_counts())
    aristas = pases.groupby(['player_name', 'pass_recipient_name']).size()

    for jugador in jugadores:
        if jugador not in numPases:
            numPases[jugador]=0

    pesos={}
    for clave in dict(aristas):
        if clave in pesos or (clave[1],clave[0]) in pesos:
            try:
                pesos[clave]+= aristas[clave]
            except:
                pesos[(clave[1],clave[0])]+= aristas[clave]
        else:
            pesos[clave]=aristas[clave]


    #DIBUJAR NODOS

    for jugador in jugadores:
        if jugador in iniciales:
            x, y = posicion_nodo(pases, jugador)
            tamaño, fs=tamano_nodo(numPases, jugador)
            ax.scatter(x, y, alpha=1, s=tamaño, color='#F39C12', edgecolors='black', zorder=1) 
            ax.text(x, y, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center")  #' '.join(jugador.split()[0:2])
        elif cambio:
            x, y = posicion_nodo(pases, jugador)
            tamaño, fs=tamano_nodo(numPases, jugador)
            ax.scatter(x, y, alpha=1, s=tamaño, color='grey',edgecolors='black', zorder=1)
            ax.text(x, y, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center")  #' '.join(jugador.split()[0:2])
        else: pass

    #DIBUJAR ARISTAS

    if cambio:
        for jugador in jugadores:
            if numPases[jugador] > 0:
                recibidores = aristas[jugador].index
                for recibidor in recibidores:
                    linewidth, opacidad = arista(jugador, recibidor, aristas)
                    x, y=posicion_nodo(pases, jugador)
                    xr,yr=posicion_nodo(pases, recibidor)
                    pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=ax, zorder=0)
                    
    elif not cambio:
        for jugador in iniciales:
            if jugador in jugadores:
                if numPases[jugador] > 0:
                    recibidores = aristas[jugador].index
                    for recibidor in recibidores:
                        if recibidor in iniciales:
                            linewidth, opacidad = arista(jugador, recibidor, aristas)
                            x, y=posicion_nodo(pases, jugador)
                            xr,yr=posicion_nodo(pases, recibidor)
                            pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=ax, zorder=0)

    #TEXTOS

    ax.text(1.5, 78, f'{equipo}', fontweight='bold', color='white',fontsize=15 )
    ax.text(95, 78, f'Total pases: {total}', fontweight='bold', color='white',fontsize=15 )
    ax.text(1.5, 3, f'{equipos[0]} vs {equipos[1]}   {resultado(dfs, match_id)}', fontweight='bold', color='white', fontsize= 15)
    ax.text(107.5, 3, f'{franja}', fontweight='bold', color='white', fontsize= 15)

    x=125
    y=5
    for clave in jugadores:
        if len(clave) > 30:
            ax.text(x, y, f'{num[clave]}: {clave[0:30]}...', fontweight='bold', fontsize=12,  color='white' )
            y+=2.5
        else:
            ax.text(x, y, f'{num[clave]}: {clave}', fontweight='bold', fontsize=12,  color='white' )
            y+=2.5

    sust = cambios(df, equipo)
    ax.text(125, 55, 'Cambios:', fontweight='bold', fontsize=15,  color='white')
    y2=60

    for clave in sust:
        jug1=sust[clave]['sale']
        jug2=sust[clave]['entra']
        minuto=sust[clave]['minuto']
        parte=sust[clave]['parte']
        minuto=int(minuto.split(':')[1])
        if parte==2:
            minuto += 45
        ax.text(125, y2, f"{minuto}':  {num[jug1]} ⇄ {num[jug2]}", fontweight='bold', fontsize=12,  color='white')
        y2+=2.5

    goals = goles(df)
    ax.text(150, 55, 'Goles:', fontweight='bold', fontsize=15,  color='white')
    y2=60

    for clave in goals:
        jug=goals[clave]['jugador']
        equipo=goals[clave]['equipo']
        num = numeros(dfl, equipo)
        minuto=goals[clave]['minuto']
        parte=goals[clave]['parte']
        minuto=int(minuto.split(':')[1])
        if parte==2:
            minuto += 45
            ax.text(150, y2, f"{minuto}':  {num[jug]} {equipo}", fontweight='bold', fontsize=12,  color='white')
        ax.text(150, y2, f"{minuto}':  {num[jug]} {equipo}", fontweight='bold', fontsize=12,  color='white')
        y2+=2.5
    

# Crear red ambos equipos partido completo
def crear_red_ambos_temporal(match_id, cambio, temp_id, desde_minuto=0, hasta_minuto=90, parte=0):
    df=load_file(match_id)
    dfl=load_file_lineup(match_id)
    dfs=load_file_season(11, temp_id)


    #DEFINIR CAMPO

    pitch = VerticalPitch(pitch_type = 'statsbomb', pitch_color = '#283747', line_color = 'white', pad_top=5, pad_bottom=5, pad_right=5, pad_left=5)
    global axs
    fig, axs = pitch.draw(ncols=2, figsize=(16, 9))

    if parte==1:
        franja="1º parte"
    elif parte == 2:
        franja="2º parte"
    elif parte == 3:
        franja=""
    else:
        franja= f"{desde_minuto}' - {hasta_minuto}'"


    df_franja=recortar_df(df, desde_minuto, hasta_minuto, parte)

    #PREPARACION VARIABLES
    for i in range(2):
        if i==0:
            seleccion = 'local'
        elif i==1:
            seleccion = 'visitante'
        
        iniciales, equipo = titulares(df, seleccion)
        total= total_pases_equipos(df_franja, equipo)
        equipos = df['team_name'].unique()


        num = numeros(dfl, equipo)
        pases = df_franja.query(f"type_name=='Pass'  and team_name=='{equipo}'and pass_type_name not in ['Throw-in'] and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']")
        jugadores = Jugadores(pases)
        numPases = dict(pases['player_name'].value_counts())
        aristas = pases.groupby(['player_name', 'pass_recipient_name']).size()

        for jugador in jugadores:
            if jugador not in numPases:
                numPases[jugador]=0

        pesos={}
        for clave in dict(aristas):
            if clave in pesos or (clave[1],clave[0]) in pesos:
                try:
                    pesos[clave]+= aristas[clave]
                except:
                    pesos[(clave[1],clave[0])]+= aristas[clave]
            else:
                pesos[clave]=aristas[clave]


        #DIBUJAR NODOS

        for jugador in jugadores:
            if jugador in iniciales:
                x, y = posicion_nodo(pases, jugador)
                tamaño, fs=tamano_nodo(numPases, jugador)
                axs[i].scatter(y, x, alpha=1, s=tamaño, color='#F39C12', edgecolors='black', zorder=1) 
                axs[i].text(y, x, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center") 
            elif cambio:
                x, y = posicion_nodo(pases, jugador)
                tamaño, fs=tamano_nodo(numPases, jugador)
                axs[i].scatter(y, x, alpha=1, s=tamaño, color='grey',edgecolors='black', zorder=1)
                axs[i].text(y, x, num[jugador], fontsize=fs, fontweight='bold', ha="center", va="center") 
            else: pass

        #DIBUJAR ARISTAS

        if cambio:
            for jugador in jugadores:
                if numPases[jugador] > 0:
                    recibidores = aristas[jugador].index
                    for recibidor in recibidores:
                        linewidth, opacidad = arista(jugador, recibidor, aristas)
                        x, y=posicion_nodo(pases, jugador)
                        xr,yr=posicion_nodo(pases, recibidor)
                        pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=axs[i], zorder=0)
                        
        elif not cambio:
            for jugador in iniciales:
                if jugador in jugadores:
                    if numPases[jugador] > 0:
                        recibidores = aristas[jugador].index
                        for recibidor in recibidores:
                            if recibidor in iniciales:
                                linewidth, opacidad = arista(jugador, recibidor, aristas)
                                x, y=posicion_nodo(pases, jugador)
                                xr,yr=posicion_nodo(pases, recibidor)
                                pitch.lines(x, y, xr,yr, lw=linewidth, alpha=opacidad, color='white', ax=axs[i], zorder=0)


    #DIBUJAR TEXTOS

        axs[i].text(0, 121.5, f'{equipo}', fontweight='bold', color='white',fontsize=15 )
        axs[i].text(0, -3.5, f'Total pases: {total}', fontweight='bold', color='white',fontsize=15 )
        axs[i].text(65, 121.5, f'{franja}', fontweight='bold', color='white', fontsize= 15)

