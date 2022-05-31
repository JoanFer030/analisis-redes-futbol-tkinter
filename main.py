import sys
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
import webbrowser
import customtkinter 
from PIL import ImageTk, Image
from funcionesAux import desplegable_opciones, desplegable_temp

HEIGHT = 500
WIDHT = 500

def cerrar():
    sys.exit()
    
root = customtkinter.CTk()
root.protocol("WM_DELETE_WINDOW", cerrar)
root.title("Análisis | Redes de pases")
root.iconbitmap("images/logo.ico")
  
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def abrir_web():
    webbrowser.open("https://redesdepases.herokuapp.com/")

def inicio(l):
    limpiar_ventana(l)
    main()

def limpiar_ventana(l):
    for elem in l:
        elem.destroy()

class Analisis1:
    def realizar_analisis_1(self, lis_eliminar):
        import redesDeCampo
        try:
            match_name = self.combo_partido.get()
            min_pases = self.input_min_pases.get()
            cuadrantes_y = self.input_cuadrantes_y.get()
            cuadrantes_x = self.input_cuadrantes_x.get()
            seleccion = self.seleccion.get()
            destacar_pases = self.destacar_pases.get()
            temp_name = self.combo_temp.get()

            limpiar_ventana(lis_eliminar)
            redesDeCampo.crear_red(self.ids[match_name], seleccion, int(min_pases), int(cuadrantes_y), int(cuadrantes_x), destacar_pases, self.opciones_season[temp_name])
            ax = redesDeCampo.ax
            canvas = FigureCanvasTkAgg(ax.figure, master=root)
            root.attributes('-fullscreen', True)
            customtkinter.set_appearance_mode("light")
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.update()
            button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
            button_inicio.place(relx=0.02, rely=0.02, relwidth=0.08, relheight=0.05)
            button_quit = customtkinter.CTkButton(text = "Cerrar", command = cerrar)
            button_quit.place(relx=0.9, rely=0.02, relwidth=0.08, relheight=0.05) 

            plot = canvas.get_tk_widget()
            plot.pack(expand=Y)
            lis_eliminar = [plot, toolbar, button_inicio, button_quit]
        except:
            messagebox.showerror("ERROR", "Los datos introducidos son erroneos")
            self.ventana_analysis_1([])

    def selection_changed(self, event):
        selection = self.combo_partido.get()
        aux= selection.split("|")

        self.local_button.config(text=aux[0].split("-")[0][4:])
        self.visitante_button.config(text=aux[0].split("-")[1])

    def selection_changed_temp(self, event):
        selection = self.combo_temp.get()
        self.ids = desplegable_opciones(self.opciones_season[selection])
        opciones = list(self.ids.keys())
        self.combo_partido.config(values=opciones)
        self.combo_partido.set(opciones[0])
        try:
            self.selection_changed("")
        except:
            pass

    def ventana_analysis_1(self, lis_eliminar):
        # Limpiamos la ventana
        limpiar_ventana(lis_eliminar)
        # Creamos variables necesarias
        self.seleccion = StringVar()
        self.destacar_pases = BooleanVar()

        # Titulo
        self.label_titulo = customtkinter.CTkLabel(root, text="Redes de Campo", fg_color=("white", "gray38"), text_font=("",15, ""))
        self.label_titulo.place(relx=0.25, rely=0.02, relwidth=0.5)

        # Apartado temporadas
        self.opciones_season = desplegable_temp()
        self.combo_temp = ttk.Combobox(root, values=list(self.opciones_season.keys()), state="readonly")
        self.combo_temp.bind("<<ComboboxSelected>>", self.selection_changed_temp)
        self.combo_temp.place(relx=0.15, rely=0.12, relwidth=0.7, height=30)

        # Apartado partido
        self.combo_partido = ttk.Combobox(root, state="readonly")
        self.combo_partido.bind("<<ComboboxSelected>>", self.selection_changed)
        self.combo_partido.place(relx=0.15, rely=0.22, relwidth=0.7, height=30)
        self.combo_temp.set("Temporada")
        self.combo_partido.set("Partido")

        # Apartado pases mínimos
        label_min_pases = customtkinter.CTkLabel(root, text="Número mín. de pases: ")
        label_min_pases.place(relx=0.02, rely=0.32)
        self.input_min_pases = customtkinter.CTkEntry(root)
        self.input_min_pases.place(relx=0.4, rely=0.32, relwidth=0.55, height=30)
        self.input_min_pases.insert(0, "2")

        # Apartado cuadrantes
        label_cuadrantes_x = customtkinter.CTkLabel(root, text="Cuadrantes eje X: ")
        label_cuadrantes_x.place(relx=0.02, rely=0.42)
        self.input_cuadrantes_x = customtkinter.CTkEntry(root)
        self.input_cuadrantes_x.place(relx=0.4, rely=0.42, relwidth=0.55, height=30)
        label_cuadrantes_y = customtkinter.CTkLabel(root, text="Cuadrantes eje Y: ")
        label_cuadrantes_y.place(relx=0.02, rely=0.52)
        self.input_cuadrantes_y = customtkinter.CTkEntry(root)
        self.input_cuadrantes_y.place(relx=0.4, rely=0.52, relwidth=0.55, height=30)
        self.input_cuadrantes_x.insert(0, "10")
        self.input_cuadrantes_y.insert(0, "10")

        # Apartado selección
        label_seleccion = customtkinter.CTkLabel(root, text="Seleccionar equipo: ")
        label_seleccion.place(relx=0.02, rely=0.62)
        self.local_button = customtkinter.CTkRadioButton(root, text="Local", variable=self.seleccion, value="local")
        self.local_button.place(relx=0.4, rely=0.625)
        self.visitante_button = customtkinter.CTkRadioButton(root, text="Visitante", variable=self.seleccion, value="visitante")
        self.visitante_button.place(relx=0.7, rely=0.625)

        # Apartado destacar pases
        label_destacar_pases = customtkinter.CTkLabel(root, text="Destacar pases: ")
        label_destacar_pases.place(relx=0.02, rely=0.72)
        destacar_button = customtkinter.CTkRadioButton(root, text="Sí", variable=self.destacar_pases, value=True)
        destacar_button.place(relx=0.4, rely=0.725)
        no_destacar_button = customtkinter.CTkRadioButton(root, text="No", variable=self.destacar_pases, value=False)
        no_destacar_button.place(relx=0.7, rely=0.725)

        # Botones fijos
        button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
        button_inicio.place(relx=0.01, rely=0.94, relwidth=0.15, relheight=0.05)

        # Botones análisis
        search_button = customtkinter.CTkButton(root, text = "Realizar analisis", 
        command= lambda: self.realizar_analisis_1(lis_eliminar))
        search_button.place(relx=0.35, rely=0.905, relwidth=0.3, relheight=0.05)
        
        
        lis_eliminar = [self.combo_partido, self.combo_temp, label_min_pases, self.input_min_pases, label_cuadrantes_y, self.input_cuadrantes_y, label_cuadrantes_x,
        self.input_cuadrantes_x, label_seleccion, self.local_button, self.visitante_button, label_destacar_pases, destacar_button, no_destacar_button,
         search_button, button_inicio, self.label_titulo]

class Analisis2:
    def realizar_analisis_2(self, tipo, lis_eliminar):
        import redesDePases    
        try:
            if tipo=="completo_equipo":
                seleccion = self.seleccion.get()
                match_name = self.combo_partido.get()
                cambio = self.cambios.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_partido_completo(self.ids[match_name], seleccion, cambio, self.opciones_season[temp_name])
                ax = redesDePases.ax
            elif tipo =="parte_equipo":
                match_name = self.combo_partido.get()
                seleccion = self.seleccion.get()
                cambio = self.cambios.get()
                parte = self.parte.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_temporal(self.ids[match_name], seleccion, cambio, self.opciones_season[temp_name], parte=int(parte))
                ax = redesDePases.ax
            elif tipo == "temporal_equipo":
                match_name = self.combo_partido.get()
                seleccion = self.seleccion.get()
                cambio = self.cambios.get()
                ini = self.ini_input.get()
                fin = self.fin_input.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_temporal(self.ids[match_name], seleccion, cambio, self.opciones_season[temp_name], int(ini), int(fin))
                ax = redesDePases.ax
            elif tipo == "completo":
                match_name = self.combo_partido.get()
                cambio = self.cambios.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_ambos_temporal(self.ids[match_name], cambio, self.opciones_season[temp_name], parte=3)
                ax = redesDePases.axs[0]
            elif tipo =="parte":
                match_name = self.combo_partido.get()
                parte = int(self.parte.get())
                cambio = self.cambios.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_ambos_temporal(self.ids[match_name], cambio, self.opciones_season[temp_name],  parte=parte)
                ax = redesDePases.axs[0]
            elif tipo == "temporal":
                match_name = self.combo_partido.get()
                ini = self.ini_input.get()
                fin = self.fin_input.get()
                cambio = self.cambios.get()
                temp_name = self.combo_temp.get()
                limpiar_ventana(lis_eliminar)
                redesDePases.crear_red_ambos_temporal(self.ids[match_name], cambio, self.opciones_season[temp_name], int(ini), int(fin))
                ax = redesDePases.axs[0]
                        
            canvas = FigureCanvasTkAgg(ax.figure, master=root)
            root.attributes('-fullscreen', True)
            customtkinter.set_appearance_mode("light")
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.update()
            button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
            button_inicio.place(relx=0.02, rely=0.02, relwidth=0.08, relheight=0.05)
            button_quit = customtkinter.CTkButton(text = "Cerrar", command = cerrar)
            button_quit.place(relx=0.9, rely=0.02, relwidth=0.08, relheight=0.05) 

            plot = canvas.get_tk_widget()
            plot.pack(expand=Y)
            lis_eliminar = [plot, toolbar, button_inicio, button_quit]
        except:
            messagebox.showerror("ERROR", "Los datos introducidos son erroneos")
            self.ventana_analysis_2(tipo, [])

    def selection_changed(self, event):
        selection = self.combo_partido.get()
        aux= selection.split("|")

        self.local_button.config(text=aux[0].split("-")[0][4:])
        self.visitante_button.config(text=aux[0].split("-")[1])

    def selection_changed_temp(self, event):
        selection = self.combo_temp.get()
        self.ids = desplegable_opciones(self.opciones_season[selection])
        opciones = list(self.ids.keys())
        self.combo_partido.config(values=opciones)
        self.combo_partido.set(opciones[0])
        try:
            self.selection_changed("")
        except:
            pass

    def ventana_analysis_2(self, tipo, lis_eliminar):
        limpiar_ventana(lis_eliminar)
        self.label_titulo = customtkinter.CTkLabel(root, fg_color=("white", "gray38"), text_font=("",15, ""))
        self.label_titulo.place(relx=0.15, rely=0.02, relwidth=0.7)
        # Titulo
        if tipo=="completo_equipo":
            self.label_titulo.config(text="Completo (1 equipo)")
        elif tipo =="parte_equipo":
            self.label_titulo.config(text="Una parte (1 equipo)")
        elif tipo == "temporal_equipo":
            self.label_titulo.config(text="Franja temporal (1 equipo)")
        elif tipo == "completo":
            self.label_titulo.config(text="Completo (2 equipos)")
        elif tipo =="parte":
            self.label_titulo.config(text="Una parte (2 equipo)")
        elif tipo == "temporal":
            self.label_titulo.config(text="Franja temporal (2 equipo)")


        # Apartado temporadas
        self.opciones_season = desplegable_temp()
        self.combo_temp = ttk.Combobox(root, values=list(self.opciones_season.keys()), state="readonly")
        self.combo_temp.bind("<<ComboboxSelected>>", self.selection_changed_temp)
        self.combo_temp.place(relx=0.15, rely=0.12, relwidth=0.7, height=30)

        # Apartado partido
        self.combo_partido = ttk.Combobox(root, state="readonly")
        if "equipo" in tipo:
            self.combo_partido.bind("<<ComboboxSelected>>", self.selection_changed)
        self.combo_partido.place(relx=0.15, rely=0.22, relwidth=0.7, height=30)
        self.combo_temp.set("Temporada")
        self.combo_partido.set("Partido")

        # Apartado mostrar cambios
        self.cambios = BooleanVar()
        label_cambios = customtkinter.CTkLabel(root, text="Mostrar cambios: ")
        label_cambios.place(relx=0.02, rely=0.72)
        mostrar_cambios_button = customtkinter.CTkRadioButton(root, text="Sí", variable=self.cambios, value=True)
        mostrar_cambios_button.place(relx=0.4, rely=0.725)
        no_mostrar_cambios_button = customtkinter.CTkRadioButton(root, text="No", variable=self.cambios, value=False)
        no_mostrar_cambios_button.place(relx=0.7, rely=0.725)
        lis_eliminar = [self.label_titulo, self.combo_partido, self.combo_temp, label_cambios, mostrar_cambios_button, no_mostrar_cambios_button]

        if "equipo" in tipo:
            self.seleccion = StringVar()
            # Apartado selección
            label_seleccion = customtkinter.CTkLabel(root, text="Seleccionar equipo: ")
            label_seleccion.place(relx=0.02, rely=0.6)
            self.local_button = customtkinter.CTkRadioButton(root, text="Local", variable=self.seleccion, value="local")
            self.local_button.place(relx=0.4, rely=0.605)
            self.visitante_button = customtkinter.CTkRadioButton(root, text="Visitante", variable=self.seleccion, value="visitante")
            self.visitante_button.place(relx=0.7, rely=0.605)
            lis_eliminar += [label_seleccion, self.local_button, self.visitante_button]

        if "parte" in tipo:
            self.parte = IntVar()
            # Apartado parte
            label_parte = customtkinter.CTkLabel(root, text="Seleccionar parte: ")
            label_parte.place(relx=0.02, rely=0.48)
            primera_button = customtkinter.CTkRadioButton(root, text="1º parte", variable=self.parte, value=1)
            primera_button.place(relx=0.4, rely=0.485)
            segunda_button = customtkinter.CTkRadioButton(root, text="2º parte", variable=self.parte, value=2)
            segunda_button.place(relx=0.7, rely=0.485)
            lis_eliminar += [label_parte, primera_button, segunda_button]

        if "temporal" in tipo:
            ini_label = customtkinter.CTkLabel(root, text="Minuto inicial: ", justify=LEFT)
            ini_label.place(relx=0.02, rely=0.36)
            self.ini_input = customtkinter.CTkEntry(root)
            self.ini_input.place(relx=0.4, rely=0.36, relwidth=0.55, height=30)
            self.ini_input.insert(0, "15")

            fin_label = customtkinter.CTkLabel(root, text="Minuto final: ", justify=LEFT)
            fin_label.place(relx=0.02, rely=0.48)
            self.fin_input = customtkinter.CTkEntry(root)
            self.fin_input.place(relx=0.4, rely=0.48, relwidth=0.55, height=30)
            self.fin_input.insert(0, "30")

            lis_eliminar += [ini_label, fin_label, self.ini_input, self.fin_input]

        button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
        button_inicio.place(relx=0.01, rely=0.94, relwidth=0.15, relheight=0.05)
        lis_eliminar += [button_inicio]


        search_button = customtkinter.CTkButton(root, text = "Realizar analisis", command= lambda: self.realizar_analisis_2(tipo, lis_eliminar))
        search_button.place(relx=0.35, rely=0.905, relwidth=0.3, relheight=0.05)
        lis_eliminar += [search_button]

    def ventana_inicio_2(self, lis_eliminar):
        limpiar_ventana(lis_eliminar)

        # Titulo
        self.label_titulo = customtkinter.CTkLabel(root, text="Redes de Pases", fg_color=("white", "gray38"), text_font=("",15, ""))
        self.label_titulo.place(relx=0.15, rely=0.02, relwidth=0.7)

        button_analysis_21 = customtkinter.CTkButton(root, text="Completo (1 equipo)", command= lambda:self.ventana_analysis_2("completo_equipo", lis_eliminar))
        button_analysis_22 = customtkinter.CTkButton(root, text="Una parte (1 equipo)", command= lambda:self.ventana_analysis_2("parte_equipo", lis_eliminar))
        button_analysis_23 = customtkinter.CTkButton(root, text="Franja temporal (1 equipo)", command= lambda:self.ventana_analysis_2("temporal_equipo", lis_eliminar))
        button_analysis_24 = customtkinter.CTkButton(root, text="Completo (2 equipos)", command= lambda:self.ventana_analysis_2("completo", lis_eliminar))
        button_analysis_25 = customtkinter.CTkButton(root, text="Una parte (2 equipo)", command= lambda:self.ventana_analysis_2("parte", lis_eliminar))
        button_analysis_26 = customtkinter.CTkButton(root, text="Franja temporal (2 equipo)", command= lambda:self.ventana_analysis_2("temporal", lis_eliminar))

        button_analysis_21.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.065)
        button_analysis_22.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.065)
        button_analysis_23.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.065)
        button_analysis_24.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.065)
        button_analysis_25.place(relx=0.25, rely=0.55, relwidth=0.5, relheight=0.065)
        button_analysis_26.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.065)


        button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
        button_inicio.place(relx=0.01, rely=0.94, relwidth=0.15, relheight=0.05)

        lis_eliminar = [button_analysis_21, button_analysis_22, button_analysis_23, button_analysis_24, button_analysis_25, button_analysis_26, button_inicio, self.label_titulo]


class Analisis3:
    def realizar_analisis_3(self, tipo, l):
        import otrasHerramientas  
        try:
            if tipo=="xG":
                match_name = self.combo_partido.get()
                limpiar_ventana(l)
                otrasHerramientas.xg_flow(self.ids[match_name])
                ax = otrasHerramientas.ax
            elif tipo =="convehull_equipo":
                match_name = self.combo_partido.get()
                seleccion = self.seleccion.get()
                limpiar_ventana(l)
                otrasHerramientas.convex_hull_titulares(self.ids[match_name], seleccion)
                ax = otrasHerramientas.ax
            elif tipo == "heatmap_equipo":
                match_name = self.combo_partido.get()
                seleccion = self.seleccion.get()
                limpiar_ventana(l)
                otrasHerramientas.campo_calor(self.ids[match_name], seleccion)
                ax = otrasHerramientas.ax
                        
            canvas = FigureCanvasTkAgg(ax.figure, master=root)
            root.attributes('-fullscreen', True)
            customtkinter.set_appearance_mode("light")
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.update()
            button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
            button_inicio.place(relx=0.02, rely=0.02, relwidth=0.08, relheight=0.05)
            button_quit = customtkinter.CTkButton(text = "Cerrar", command = cerrar)
            button_quit.place(relx=0.9, rely=0.02, relwidth=0.08, relheight=0.05) 

            plot = canvas.get_tk_widget()
            plot.pack(expand=Y)
            lis_eliminar = [plot, toolbar, button_inicio, button_quit]
        except:
            messagebox.showerror("ERROR", "Los datos introducidos son erroneos")
            self.ventana_analysis_3(tipo, [])

    def selection_changed(self, event):
        selection = self.combo_partido.get()
        aux= selection.split("|")

        self.local_button.config(text=aux[0].split("-")[0][4:])
        self.visitante_button.config(text=aux[0].split("-")[1])

    def selection_changed_temp(self, event):
        selection = self.combo_temp.get()
        self.ids = desplegable_opciones(self.opciones_season[selection])
        opciones = list(self.ids.keys())
        self.combo_partido.config(values=opciones)
        self.combo_partido.set(opciones[0])
        try:
            self.selection_changed("")
        except:
            pass

    def ventana_analysis_3(self, tipo, l):
        limpiar_ventana(l)
        self.label_titulo = customtkinter.CTkLabel(root, fg_color=("white", "gray38"), text_font=("",15, ""))
        self.label_titulo.place(relx=0.15, rely=0.02, relwidth=0.7)
        # Titulo
        if tipo == "xG":
            self.label_titulo.config(text="Probabilidad de gol (xG)")
        elif tipo == "convehull_equipo":
            self.label_titulo.config(text="Zona de influencia (1 equipo)")
        elif tipo == "heatmap_equipo":
            self.label_titulo.config(text="Mapa de calor (1 equipo)")

        # Apartado temporadas
        self.opciones_season = desplegable_temp()
        self.combo_temp = ttk.Combobox(root, values=list(self.opciones_season.keys()), state="readonly")
        self.combo_temp.bind("<<ComboboxSelected>>", self.selection_changed_temp)
        self.combo_temp.place(relx=0.15, rely=0.12, relwidth=0.7, height=30)

        # Apartado partido
        self.combo_partido = ttk.Combobox(root, state="readonly")
        if "equipo" in tipo:
            self.combo_partido.bind("<<ComboboxSelected>>", self.selection_changed)
        self.combo_partido.place(relx=0.15, rely=0.22, relwidth=0.7, height=30)
        self.combo_temp.set("Temporada")
        self.combo_partido.set("Partido")

        lis_eliminar = [self.label_titulo, self.combo_temp, self.combo_partido]

        if "equipo" in tipo:
            self.seleccion = StringVar()
            # Apartado selección
            label_seleccion = customtkinter.CTkLabel(root, text="Seleccionar equipo: ")
            label_seleccion.place(relx=0.02, rely=0.6)
            self.local_button = customtkinter.CTkRadioButton(root, text="Local", variable=self.seleccion, value="local")
            self.local_button.place(relx=0.4, rely=0.605)
            self.visitante_button = customtkinter.CTkRadioButton(root, text="Visitante", variable=self.seleccion, value="visitante")
            self.visitante_button.place(relx=0.7, rely=0.605)
            lis_eliminar += [label_seleccion, self.local_button, self.visitante_button]

        button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
        button_inicio.place(relx=0.01, rely=0.94, relwidth=0.15, relheight=0.05)
        lis_eliminar += [button_inicio]

        search_button = customtkinter.CTkButton(root, text = "Realizar analisis", command= lambda: self.realizar_analisis_3(tipo, lis_eliminar))
        search_button.place(relx=0.35, rely=0.905, relwidth=0.3, relheight=0.05)
        lis_eliminar += [search_button]



    def ventana_inicio_3(self, l):
        limpiar_ventana(l)

        self.label_titulo = customtkinter.CTkLabel(root, text="Otras herramientas", fg_color=("white", "gray38"), text_font=("",15, ""))
        self.label_titulo.place(relx=0.15, rely=0.02, relwidth=0.7)
        
        button_analysis_21 = customtkinter.CTkButton(root, text="Probabilidad de gol (xG)", command= lambda:self.ventana_analysis_3("xG", lis_eliminar))
        button_analysis_22 = customtkinter.CTkButton(root, text="Zona de influencia (1 equipo)", command= lambda:self.ventana_analysis_3("convehull_equipo", lis_eliminar))
        button_analysis_23 = customtkinter.CTkButton(root, text="Mapa de calor (1 equipo)", command= lambda:self.ventana_analysis_3("heatmap_equipo", lis_eliminar))
        
        button_analysis_21.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.065)
        button_analysis_22.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.065)
        button_analysis_23.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.065)

        button_inicio = customtkinter.CTkButton(text = "Inicio", command = lambda: inicio(lis_eliminar))
        button_inicio.place(relx=0.01, rely=0.94, relwidth=0.15, relheight=0.05)

        lis_eliminar = [button_analysis_21, button_analysis_22, button_analysis_23, button_inicio, self.label_titulo]



def main():
    customtkinter.set_appearance_mode("System")# Modes: "System" (standard), "Dark", "Light"             
    root.attributes('-fullscreen', False)
    root.geometry(f'{WIDHT}x{HEIGHT}')

    analysis1 = Analisis1()
    analysis2 = Analisis2()
    analysis3 = Analisis3()

    button_analysis_1 = customtkinter.CTkButton(root, text="Redes de campo", command= lambda:analysis1.ventana_analysis_1(lis_eliminar))
    button_analysis_2 = customtkinter.CTkButton(root, text="Redes de pases", command= lambda:analysis2.ventana_inicio_2(lis_eliminar))
    button_analysis_3 = customtkinter.CTkButton(root, text="Otras herramientas", command= lambda:analysis3.ventana_inicio_3(lis_eliminar))
    button_analysis_4 = customtkinter.CTkButton(root, text="Redes de pases | Web", command= abrir_web)

    img = ImageTk.PhotoImage(Image.open("images/logo.png"))
    img_panel = customtkinter.CTkLabel(root, image = img)
    img_panel.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=0.5)

    lis_eliminar = [button_analysis_1, button_analysis_2, button_analysis_3, button_analysis_4, img_panel] 

    button_analysis_1.place(relx=0.25, rely=0.12, relwidth=0.5, relheight=0.065)
    button_analysis_2.place(relx=0.25, rely=0.22, relwidth=0.5, relheight=0.065)
    button_analysis_3.place(relx=0.25, rely=0.32, relwidth=0.5, relheight=0.065)
    button_analysis_4.place(relx=0.25, rely=0.42, relwidth=0.5, relheight=0.065)

    root.mainloop()

if __name__ == "__main__":
    main()
    