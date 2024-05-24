from GestionePagine.GestorePagine import *
from GestionePagine.Widgets.Tabelle import *

#Stati di una statemachine (stati derivati da paginaGenerica, statemachine : GestorePagine)
class PaginaDashboard(PaginaGenerica): #Singleton
    #Creo un'istanza statica
    paginaDashboard = None

    # COSTRUTTORE E GETTER INSTANZA STATICA
    @staticmethod
    def Init():
        if PaginaDashboard.paginaDashboard == None:
            PaginaDashboard.paginaDashboard = PaginaDashboard()
    @staticmethod
    def GetPaginaDashboard():
        if PaginaDashboard.paginaDashboard == None:
            PaginaDashboard.paginaDashboard = PaginaDashboard()  
        return PaginaDashboard.paginaDashboard
    

    # COSTRUTTORE 
    def __init__(self):
        
        #Attributi
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__fontColor = Impostazioni.Tema.IGetFontColor("testo")

        #Aggiungo la pagina
        PaginaGenerica.AggiungiPagina(NOME_INTERNO_PAGINA_DASHBOARD)
        GestorePagine.IAddPagina(self)
        self.__dimensioniPagina = [int(Impostazioni.sistema.dimensioniFinestra[0] * (1 - PROPORZIONE_MENU_PAGINA)), Impostazioni.sistema.dimensioniFinestra[1]]
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
        self.__dimensioniTabellaDashboard = [int(self.__dimensioniPagina[0] - SPAZIO_LATI_PAGINA_DISPOSITIVI * 2),
                                                self.__dimensioniPagina[1] - SPAZIO_ALTO_PAGINA_DISPOSITIVI * 2]
        # CREO LE TABELLE
        self.__tabellaDashboard = TabellaDashboard(master = self.__fFrameInternoCanvasScorrevole,
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard,
                                            tableWidth = self.__dimensioniTabellaDashboard[0],
                                            tableHeight = self.__dimensioniTabellaDashboard[1],
                                            elementWidth = self.__dimensioniTabellaDashboard[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard)
        self.__tabellaDashboard.RefreshFrameDispositivi()

        #FRAME SUPPORTO TITOLO
        self.__fFrameTitoloDashboard = tk.Frame(master = self.__fFrameInternoCanvasScorrevole, background = self.__coloreSfondo)
        self.__fFrameTitoloDashboard.place(x = SPAZIO_LATI_PAGINA_DASHBOARD + SPAZIO_LATI_PAGINA_DASHBOARD//2, 
                                           y = SPAZIO_ALTO_PAGINA_DASHBOARD // 2, 
                                           width = self.__dimensioniTabellaDashboard[0] // 2,
                                           height = SPAZIO_ALTO_PAGINA_DASHBOARD // 2)
        self.__fFrameTitoloDashboard.rowconfigure(0, weight=0)
        self.__fFrameTitoloDashboard.columnconfigure(0, weight=0)
        self.__fFrameTitoloDashboard.grid_propagate(False)
        self.__fFrameTitoloDashboard.pack_propagate(False)
        #LABEL TITOLO
        self.__lTitoloDashboard = tk.Label(master = self.__fFrameTitoloDashboard,
                                            text= "Dashboard",
                                            background = self.__coloreSfondo,
                                            foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                            font = Impostazioni.Tema.IGetFont("titolo")
                                           )
        self.__lTitoloDashboard.pack(side = "left", fill="both", anchor="sw")

        #FRAME DELLE SCRITTE SOPRA LA TABELLA
        self.__fFrameTextLabel = tk.Frame(master = self.__fFrameInternoCanvasScorrevole)
        self.__fFrameTextLabel.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI, width = self.__dimensioniTabellaDashboard[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard, anchor = "nw")
        self.__fFrameTextLabel.columnconfigure(0, weight = int(100 * PROPORZIONI_NOME_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFrameTextLabel.columnconfigure(1, weight = int(100 * PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFrameTextLabel.columnconfigure(2, weight = int(100 * PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFrameTextLabel.columnconfigure(3, weight = int(100 * PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFrameTextLabel.columnconfigure(4, weight = int(100 * PROPORZIONI_STATUS_DISPOSITIVO_TABELLA_DASHBOARD))
        self.__fFrameTextLabel.columnconfigure(5, weight = int(100 * PROPORZIONI_PINGMANUALE_DISPOSITIVO_TABELLA_DASHBOARD))
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

        # FRAME SUPPORTO SCRITTA STATUS
        self.__fFrameScrittaStatus = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaStatus.grid(row = 0, column = 4, sticky = "nsew")
        self.__fFrameScrittaStatus.rowconfigure(0, weight = 1)
        self.__fFrameScrittaStatus.columnconfigure(0, weight = 1)
        self.__fFrameScrittaStatus.grid_propagate(False)
        self.__fFrameScrittaStatus.pack_propagate(False)

        # FRAME SUPPORTO SCRITTA PING MANUALE
        self.__fFrameScrittaPingManuale = tk.Frame(master = self.__fFrameTextLabel, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness=1)
        self.__fFrameScrittaPingManuale.grid(row = 0, column = 5, sticky = "nsew")
        self.__fFrameScrittaPingManuale.rowconfigure(0, weight = 1)
        self.__fFrameScrittaPingManuale.columnconfigure(0, weight = 1)
        self.__fFrameScrittaPingManuale.grid_propagate(False)
        self.__fFrameScrittaPingManuale.pack_propagate(False)

        #SCRITTE SOPRA LA TABELLA
        self.__textLabels = []
        # Create and position the text labels
        for i in range(6):
            textLabel = tk.Label(master= self.__fFrameScrittaNome if i==0 else self.__fFrameScrittaIndirizzoIP if i==1 else self.__fFrameScrittaPorta if i==2 else self.__fFrameScrittaTempoTraPing if i==3 else self.__fFrameScrittaStatus if i==4 else self.__fFrameScrittaPingManuale,
                                text = "Nome dispositivo" if i==0 else "Indirizzo ip" if i==1 else "Porta" if i==2 else "Frequenza ping (sec)" if i==3 else "Status" if i==4 else "Ping",
                                font = self.__font,
                                fg = self.__fontColor,
                                bg = self.__coloreSfondo
                                )
            textLabel.grid(row = 0, column = i, sticky="nsew")
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
        self.__tabellaDashboard.CaricaTabella()

    def NascondiPagina(self):
        self.__fFramePrincipale.grid_forget()
        #Metto in pausa i processi
        Dispositivo.pausaFinitaEvent.clear()

    def MostraPagina(self):
        self.__fFramePrincipale.grid_propagate(True)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.grid_propagate(False)
        Dispositivo.pausaFinitaEvent.set()

    def UpdatePagina(self, deltaTime : float = 0): #Disabled
        return
        #Chiamo l'update
        #self.__tabellaDashboard.Update(deltaTime)


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__tabellaDashboard.AggiornaColoriTema()
        self.AggiornaColori()

    def AggiornaColori(self):
        self.__fFrameInternoCanvasScorrevole.configure(background=self.__coloreSfondo)
        self.__cCanvasScorrevole.configure(background=self.__coloreSfondo)

        #Aggiorno i colori del titolo
        self.__fFrameTitoloDashboard.configure(background = self.__coloreSfondo)
        self.__lTitoloDashboard.configure(background = self.__coloreSfondo,
                                          foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                          font = Impostazioni.Tema.IGetFont("titolo"))

        #Cambio i colore della barra della tabella
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fFrameScrittaNome.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaIndirizzoIP.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaPorta.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaTempoTraPing.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaStatus.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameScrittaPingManuale.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        for textLabel in self.__textLabels:
            textLabel.configure(background = coloreSfondo,
                                 font = Impostazioni.Tema.IGetFont("testo"), 
                                 foreground = Impostazioni.Tema.IGetFontColor("testo"), 
                                 highlightcolor = coloreBordo)
        
    def CambioDimFrame(self):
        #Resize dimensioni
        self.__dimensioniPagina = [int(Impostazioni.sistema.dimensioniFinestra[0] * (1 - PROPORZIONE_MENU_PAGINA)), Impostazioni.sistema.dimensioniFinestra[1]]
        self.__dimensioniPaginaScorrevole = [self.__dimensioniPagina[0], ALTEZZA_PAGINA_DISPOSITIVI]
        self.__dimensioniTabellaDashboard[0] = int(self.__dimensioniPagina[0] - SPAZIO_LATI_PAGINA_DISPOSITIVI * 2)
        
        #Resize canvas scorrevole
        self.__cCanvasScorrevole.configure(scrollregion = (0, 0, Impostazioni.sistema.dimensioniFinestra[0] * (1-PROPORZIONE_MENU_PAGINA), ALTEZZA_PAGINA_DASHBOARD))
        thisCanvasId = self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width =  self.__dimensioniPaginaScorrevole[0],
                                              height = self.__dimensioniPaginaScorrevole[1])

        self.__cCanvasScorrevole.delete(self.__ultimoCanvasId)
        self.__ultimoCanvasId = thisCanvasId

        self.__fFrameTextLabel.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI, width = self.__dimensioniTabellaDashboard[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard, anchor = "nw")

        #Resize tabella
        self.__tabellaDashboard.ChangeDim(
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard,
                                            tableWidth = self.__dimensioniTabellaDashboard[0],
                                            tableHeight = self.__dimensioniTabellaDashboard[1],
                                            elementWidth = self.__dimensioniTabellaDashboard[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                                            coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                            coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[3])

PaginaDashboard.Init()