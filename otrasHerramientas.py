from funcionesAux import *

def convex_hull_titulares(match_id, seleccion):
    df= load_file(match_id)

    #EQUIPO Y ALINEACIÓN
    alineacion, equipo= titulares(df, seleccion)
    alineacion.pop(0)

    fig, axes = plt.subplots(nrows = 2,ncols = 5,figsize=(20,8))
    pitch = Pitch(pitch_color = '#283747', line_color = 'white')

    global ax
    for i, ax in enumerate(fig.axes):
        jugador = alineacion[i]
        pases=df.query(f"type_name=='Pass' and team_name=='{equipo}' and player_name == '{jugador}' and pass_type_name not in ['Throw-in', 'Corner'] and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']  ")
        pitch.draw(ax=ax)

        lista_pases = []
        for index, row in pases.iterrows():
            lista_pases.append([row['location'][0], row['location'][1]])
            ax.scatter(row['location'][0], row['location'][1], zorder = 1, s = 35, color='black')
        lista_pases=np.asarray(lista_pases) #Convertimos a array para poder aplicar el ConvexHull
        #lista_pases = (np.abs(stats.zscore(lista_pases) < .1))

        hull = ConvexHull(lista_pases)
        for simplex in hull.simplices:
            ax.plot(lista_pases[simplex, 0], lista_pases[simplex, 1], '#A50044',lw=3)
            ax.fill(lista_pases[hull.vertices,0], lista_pases[hull.vertices,1], c='white', alpha=0.05)
            ax.set_ylabel(ylabel=' ')
            ax.set_title(label=jugador,c='black',va='center',ha='center',fontsize=12,)

# Leyenda y pasar a subplot
def xg_flow(match_id):
    df= load_file(match_id)
    dfs = load_file_season(11, 90)

    local = df['team_name'].iloc[0]
    visitante = df['team_name'].iloc[1]

    tiros=df.query("type_name=='Shot'")    #Crea df solo con tiros del equipo elegido
    tiros_local =tiros.query(f"team_name=='{local}'")
    tiros_visitante = tiros.query(f"team_name=='{visitante}'")
    local_xg = xg(tiros_local)
    visitante_xg = xg(tiros_visitante)

    global ax
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.set_facecolor('#283747')
    ax.patch.set_facecolor('#283747')
    ax.grid(axis = "y", linestyle="--")
    ax.set_xticks([i*15 for i in range(8)])
    ax.set_xlabel('Minuto',color='white',fontsize=14)
    ax.set_ylabel('xG',color='white',fontsize=14)

    ax.step(local_xg.keys(), local_xg.values())
    ax.step(visitante_xg.keys(), visitante_xg.values(), color="orange")

    gol_local = min_gol(tiros_local)
    gol_visitante = min_gol(tiros_visitante)
    for gol in gol_local:
        ax.scatter(gol, local_xg[gol], color="white", zorder=5)
        ax.text(gol+2, local_xg[gol], f"Gol - {int(gol)}'", color="white")

    for gol in gol_visitante:
        ax.scatter(gol, visitante_xg[gol], color="white", zorder=5)
        ax.text(gol+2, visitante_xg[gol], f"Gol - {int(gol)}'", color="white")

    ax.legend(handles=[mpatches.Patch(label=f"{local} - {round(local_xg[max(local_xg, key=local_xg.get)], 2)}"), 
    mpatches.Patch(color="orange", label=f"{visitante} - {round(visitante_xg[max(visitante_xg, key=visitante_xg.get)], 2)}")])



def campo_calor(match_id, seleccion):
    df= load_file(match_id)
    alineacion, equipo= titulares(df, seleccion)

    pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                        ['#15242e', '#4393c4'], N=10)

    pases=df.query(f"type_name=='Pass' and team_name=='{equipo}' and pass_type_name not in ['Throw-in'] and pass_outcome_name not in ['Unknown','Out','Pass Offside','Injury Clearance','Incomplete']  ")    #Crea df solo con pases correctos del equio elegido
    pas_x = []
    pas_y = []

    for index,row in pases.iterrows():
        pas_x.append(row['pass_end_location'][0])
        pas_y.append(row['pass_end_location'][1])

    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#283747', line_color='white')
    # draw
    global ax
    fig, ax = pitch.draw(figsize=(10, 6))
    bin_statistic = pitch.bin_statistic_positional(pas_x, pas_y, statistic='count',
                                                positional='full', normalize=True)
    pitch.heatmap_positional(bin_statistic, ax=ax, cmap='coolwarm', edgecolors='#22312b')
    pitch.scatter(pas_x, pas_y, c='white', s=2, ax=ax)
    labels = pitch.label_heatmap(bin_statistic, color='black', fontsize=18,
                                ax=ax, ha='center', va='center',
                                str_format='{:.0%}')
