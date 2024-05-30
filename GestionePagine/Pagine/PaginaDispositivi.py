from GestionePagine.GestorePagine import *
from GestionePagine.Widgets.Tabelle import *

#Stati di una statemachine (stati derivati da paginaGenerica, statemachine : GestorePagine)
class PaginaDispositivi(PaginaGenerica): #Singleton
    #Creo un'istanza statica
    paginaDispositivi = None

    # COSTRUTTORE E GETTER INSTANZA STATICA
    @staticmethod
    def Init():
        if PaginaDispositivi.paginaDispositivi == None:
            PaginaDispositivi.paginaDispositivi = PaginaDispositivi()
    @staticmethod
    def GetPaginaDispositivi():
        if PaginaDispositivi.paginaDispositivi == None:
            PaginaDispositivi.paginaDispositivi = PaginaDispositivi()  
        return PaginaDispositivi.paginaDispositivi
    

    # COSTRUTTORE 
    def __init__(self):

        #Salvo i colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__fontColor = Impostazioni.Tema.IGetFontColor("testo")

        #Aggiungo la pagina
        PaginaGenerica.AggiungiPagina(NOME_INTERNO_PAGINA_DISPOSITIVI)
        GestorePagine.IAddPagina(self)
        self.__dimensioniPagina = [int(Impostazioni.sistema.dimensioniFinestra[0] * (1 - Impostazioni.PROPORZIONE_MENU_PAGINA)), Impostazioni.sistema.dimensioniFinestra[1]]
        self.__dimensioniPaginaScorrevole = [self.__dimensioniPagina[0], ALTEZZA_PAGINA_DISPOSITIVI]
    
        # FRAME PRINCIPALE
        self.__fFramePrincipale = tk.Frame(master = GestorePagine.IGetFramePagina())
        self.__fFramePrincipale.columnconfigure(0, weight = 1)
        self.__fFramePrincipale.rowconfigure(0, weight = 1)
        self.__fFramePrincipale.grid_propagate(False)


        # CREO IL CANVAS SCORREVOLE PER SCORRERE LA PAGINA
        self.__cCanvasScorrevole = tk.Canvas(master = self.__fFramePrincipale, 
                                             scrollregion = (0, 0, self.__dimensioniPaginaScorrevole[0], self.__dimensioniPaginaScorrevole[1]),
                                             bg = self.__coloreSfondo)
        self.__cCanvasScorrevole.configure(yscrollincrement='1')
        self.__cCanvasScorrevole.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasScorrevole.grid_propagate(False)
        self.__cCanvasScorrevole.pack_propagate(False)
        # FRAME INTERNO AL CANVAS
        self.__fFrameInternoCanvasScorrevole = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo)
        self.__fFrameInternoCanvasScorrevole.place(x = 0, y = 0, width = self.__dimensioniPaginaScorrevole[0], height = self.__dimensioniPaginaScorrevole[1], anchor= "nw")
        self.__fFrameInternoCanvasScorrevole.columnconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.rowconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.grid_propagate(False)
        self.__fFrameInternoCanvasScorrevole.pack_propagate(False)
        # GENERO IL FRAME
        self.__ultimoCanvasId = self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniPaginaScorrevole[0],
                                              height = self.__dimensioniPaginaScorrevole[1])


        # CREO LA TABELLA
        self.__dimensioniTabellaDispositivi = [int(self.__dimensioniPagina[0] - SPAZIO_LATI_PAGINA_DISPOSITIVI * 2),
                                                self.__dimensioniPagina[1] - SPAZIO_ALTO_PAGINA_DISPOSITIVI * 2]
        self.__tabellaDispositivi = TabellaDispositivi(master = self.__fFrameInternoCanvasScorrevole,
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            tableWidth = self.__dimensioniTabellaDispositivi[0],
                                            tableHeight = self.__dimensioniTabellaDispositivi[1],
                                            elementWidth = self.__dimensioniTabellaDispositivi[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi)
        self.__tabellaDispositivi.RefreshFrameDispositivi()


        #FRAME SUPPORTO TITOLO
        self.__fFrameTitoloDispositivi = tk.Frame(master = self.__fFrameInternoCanvasScorrevole, background = self.__coloreSfondo)
        self.__fFrameTitoloDispositivi.place(x = SPAZIO_LATI_PAGINA_DASHBOARD + SPAZIO_LATI_PAGINA_DASHBOARD // 2, 
                                           y = SPAZIO_ALTO_PAGINA_DASHBOARD // 2, 
                                           width = self.__dimensioniTabellaDispositivi[0] // 2,
                                           height = SPAZIO_ALTO_PAGINA_DASHBOARD // 2)
        self.__fFrameTitoloDispositivi.rowconfigure(0, weight=0)
        self.__fFrameTitoloDispositivi.columnconfigure(0, weight=0)
        self.__fFrameTitoloDispositivi.grid_propagate(False)
        self.__fFrameTitoloDispositivi.pack_propagate(False)
        #LABEL TITOLO
        self.__lTitoloDispositivi = tk.Label(master = self.__fFrameTitoloDispositivi,
                                            text = "Dispositivi",
                                            background = self.__coloreSfondo,
                                            foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                            font = Impostazioni.Tema.IGetFont("titolo")
                                           )
        self.__lTitoloDispositivi.pack(side = "left", fill="both", anchor="sw")


        # FRAME SUPPORTO AGGIUNTA DISPOSITIVO
        self.__fFrameBottoneAggiuntaDispositivo = tk.Frame(master = self.__fFrameInternoCanvasScorrevole)
        self.__dimBottone = (150, 40)
        self.__offsetBottone = (8,8)
        self.__fFrameBottoneAggiuntaDispositivo.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI + self.__dimensioniTabellaDispositivi[0] - (self.__dimBottone[0] + self.__offsetBottone[0]), 
                                                      y = SPAZIO_ALTO_PAGINA_DISPOSITIVI - (self.__dimBottone[1] + self.__offsetBottone[1]), width = self.__dimBottone[0], height = self.__dimBottone[1], anchor= "nw")
        self.__fFrameBottoneAggiuntaDispositivo.columnconfigure(0, weight = 1)
        self.__fFrameBottoneAggiuntaDispositivo.rowconfigure(0, weight = 1)
        self.__fFrameBottoneAggiuntaDispositivo.grid_propagate(False)
        self.__fFrameBottoneAggiuntaDispositivo.pack_propagate(False)
        # BOTTONE AGGIUNTA DISPOSITIVO
        self.__bBottoneAggiuntaDispositivo = ctk.CTkButton(master = self.__fFrameBottoneAggiuntaDispositivo,
                                                        command = self.AggiungiDispositivo, 
                                                        text="+ Dispositivo",
                                                        fg_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                                        font = Impostazioni.Tema.IGetFont_ctkFormat("sottotitolo"),
                                                        text_color = Impostazioni.Tema.IGetFontColor("sottotitolo"),
                                                        bg_color = self.__coloreSfondo,
                                                        hover_color = Impostazioni.Tema.IGetColoriSfondo("terziario")[1],
                                                        border_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[3],
                                                        border_width = 2,
                                                        corner_radius = 15)
        self.__bBottoneAggiuntaDispositivo.grid(row = 0, column=0, sticky="nsew")


        #FRAME DELLE SCRITTE SOPRA LA TABELLA
        self.__fFrameTextLabel = tk.Frame(master = self.__fFrameInternoCanvasScorrevole)
        self.__fFrameTextLabel.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, anchor = "nw")
        self.__fFrameTextLabel.columnconfigure(0, weight = int(100 * PROPORZIONI_NOME_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFrameTextLabel.columnconfigure(1, weight = int(100 * PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFrameTextLabel.columnconfigure(2, weight = int(100 * PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFrameTextLabel.columnconfigure(3, weight = int(100 * PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFrameTextLabel.columnconfigure(4, weight = int(100 * PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI))
        self.__fFrameTextLabel.rowconfigure(0, weight = 1)
        self.__fFrameTextLabel.grid_propagate(False)
        self.__fFrameTextLabel.pack_propagate(False)


        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaNome = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaNome.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameScrittaNome.rowconfigure(0, weight = 1)
        self.__fFrameScrittaNome.columnconfigure(0, weight = 1)
        self.__fFrameScrittaNome.grid_propagate(False)
        self.__fFrameScrittaNome.pack_propagate(False)

        # FRAME SUPPORTO SCRITTA INDIRIZZO IP
        self.__fFrameScrittaIndirizzoIP = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaIndirizzoIP.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameScrittaIndirizzoIP.rowconfigure(0, weight = 1)
        self.__fFrameScrittaIndirizzoIP.columnconfigure(0, weight = 1)
        self.__fFrameScrittaIndirizzoIP.grid_propagate(False)
        self.__fFrameScrittaIndirizzoIP.pack_propagate(False)

        # FRAME SUPPORTO SCRITTA PORTA
        self.__fFrameScrittaPorta = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaPorta.grid(row = 0, column = 2, sticky = "nsew")
        self.__fFrameScrittaPorta.rowconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.columnconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.grid_propagate(False)
        self.__fFrameScrittaPorta.pack_propagate(False)

        # FRAME SUPPORTO SCRITTA TEMPO TRA PING
        self.__fFrameScrittaTempoTraPing = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaTempoTraPing.grid(row = 0, column = 3, sticky = "nsew")
        self.__fFrameScrittaTempoTraPing.rowconfigure(0, weight = 1)
        self.__fFrameScrittaTempoTraPing.columnconfigure(0, weight = 1)
        self.__fFrameScrittaTempoTraPing.grid_propagate(False)
        self.__fFrameScrittaTempoTraPing.pack_propagate(False)

        # FRAME SUPPORTO SCRITTA TASTI MODDEL
        self.__fFrameScrittaTastiModdel = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaTastiModdel.grid(row = 0, column = 4, sticky = "nsew")
        self.__fFrameScrittaTastiModdel.rowconfigure(0, weight = 1)
        self.__fFrameScrittaTastiModdel.columnconfigure(0, weight = 1)
        self.__fFrameScrittaTastiModdel.grid_propagate(False)
        self.__fFrameScrittaTastiModdel.pack_propagate(False)

        #SCRITTE SOPRA LA TABELLA
        self.__textLabels = []
        # Create and position the text labels
        for i in range(5):
            textLabel = tk.Label(master= self.__fFrameScrittaNome if i==0 else self.__fFrameScrittaIndirizzoIP if i==1 else self.__fFrameScrittaPorta if i==2 else self.__fFrameScrittaTempoTraPing if i==3 else self.__fFrameScrittaTastiModdel,
                                text = "Nome dispositivo" if i==0 else "Indirizzo ip" if i==1 else "Porta" if i==2 else "Frequenza ping (sec)" if i==3 else "",
                                bg = self.__coloreSfondo,
                                font = self.__font,
                                fg = self.__fontColor
                                )
            textLabel.grid(row = 0, column = i, sticky="nsew", rowspan=1, columnspan=1)
            textLabel.pack(side="left")
            #textLabel.configure(highlightthickness = 1, highlightcolor = Impostazioni.Tema.IGetColoriSfondo("secondario")[3])
            self.__textLabels.append(textLabel)

        # EVENT BIND
        self.__fFramePrincipale.bind("<MouseWheel>", lambda event : self.__cCanvasScorrevole.yview_scroll(int(-event.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella), "units"))
        self.__fFrameInternoCanvasScorrevole.bind("<MouseWheel>", lambda event : self.__cCanvasScorrevole.yview_scroll(int(-event.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella), "units"))
        
                                           


    # METODI CAMBIO PAGINA E UPDATE
    def CaricaPagina(self, args = []):
        #Mostro la pagina
        self.MostraPagina()

        #Aggiorno i dispositivi
        self.__tabellaDispositivi.CaricaTabella()

    def NascondiPagina(self):
        self.__fFramePrincipale.grid_forget()

    def MostraPagina(self):
        self.__fFramePrincipale.grid_propagate(True)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.grid_propagate(False)

    def UpdatePagina(self, deltaTime : float = 0): #Disabled
        return 
    

    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__tabellaDispositivi.AggiornaColoriTema()
        self.AggiornaColori()

    def AggiornaColori(self):

        #Aggiorno i colori del titolo
        self.__fFrameTitoloDispositivi.configure(background = self.__coloreSfondo)
        self.__lTitoloDispositivi.configure(background = self.__coloreSfondo,
                                          foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                          font = Impostazioni.Tema.IGetFont("titolo"))
        
        #
        self.__fFrameInternoCanvasScorrevole.configure(background=self.__coloreSfondo)
        self.__cCanvasScorrevole.configure(background=self.__coloreSfondo)
        self.__bBottoneAggiuntaDispositivo.configure( require_redraw = True,
                                                      fg_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                                      text_color = Impostazioni.Tema.IGetFontColor("sottotitolo"),
                                                      border_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[3],
                                                      hover_color = Impostazioni.Tema.IGetColoriSfondo("terziario")[1],
                                                      font = Impostazioni.Tema.IGetFont_ctkFormat("sottotitolo"),
                                                      bg_color = self.__coloreSfondo)
        
        #Cambio i colori della barra della tabella
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fFrameScrittaNome.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaIndirizzoIP.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaPorta.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaTempoTraPing.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaTastiModdel.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        for textLabel in self.__textLabels:
            textLabel.configure(background = coloreSfondo,
                                 font = Impostazioni.Tema.IGetFont("testo"), 
                                 foreground = Impostazioni.Tema.IGetFontColor("testo"), 
                                 highlightcolor = coloreBordo)
            
        
    def CambioDimFrame(self):
        #Resize dimensioni
        self.__dimensioniPagina = [int(Impostazioni.sistema.dimensioniFinestra[0] * (1 - PROPORZIONE_MENU_PAGINA)), Impostazioni.sistema.dimensioniFinestra[1]]
        self.__dimensioniPaginaScorrevole = [self.__dimensioniPagina[0], ALTEZZA_PAGINA_DISPOSITIVI]
        self.__dimensioniTabellaDispositivi[0] = int(self.__dimensioniPagina[0] - SPAZIO_LATI_PAGINA_DISPOSITIVI * 2)
        
        #Resize canvas scorrevole
        self.__cCanvasScorrevole.configure(scrollregion = (0, 0, Impostazioni.sistema.dimensioniFinestra[0] * (1-PROPORZIONE_MENU_PAGINA), ALTEZZA_PAGINA_DASHBOARD))
        thisCanvasId = self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width =  self.__dimensioniPaginaScorrevole[0],
                                              height = self.__dimensioniPaginaScorrevole[1])

        self.__cCanvasScorrevole.delete(self.__ultimoCanvasId)
        self.__ultimoCanvasId = thisCanvasId

        #Ripos button
        self.__fFrameBottoneAggiuntaDispositivo.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI + self.__dimensioniTabellaDispositivi[0] - (self.__dimBottone[0] + self.__offsetBottone[0]), 
                                                      y = SPAZIO_ALTO_PAGINA_DISPOSITIVI - (self.__dimBottone[1] + self.__offsetBottone[1]), width = self.__dimBottone[0], height = self.__dimBottone[1], anchor= "nw")
        
        self.__fFrameTextLabel.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard, anchor = "nw")


        #Resize tabella
        self.__tabellaDispositivi.ChangeDim(
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            tableWidth = self.__dimensioniTabellaDispositivi[0],
                                            tableHeight = self.__dimensioniTabellaDispositivi[1],
                                            elementWidth = self.__dimensioniTabellaDispositivi[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                                            coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                            coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[3])

    # METODI EVENTI
    def AggiungiDispositivo(self):
        GestorePagine.ICaricaPaginaConNome(NOME_INTERNO_PAGINA_AGGIUNGI_DISPOSITIVO)

PaginaDispositivi.Init()