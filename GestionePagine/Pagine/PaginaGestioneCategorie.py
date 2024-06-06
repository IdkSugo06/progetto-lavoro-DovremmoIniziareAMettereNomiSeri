from GestionePagine.Pagine.PaginaCategoriaSingola import *


#Stati di una statemachine (stati derivati da paginaGenerica, statemachine : GestorePagine)
class PaginaGestioneCategorie(PaginaGenerica): #Singleton

    #Creo un'istanza statica
    paginaDispositivi = None

    # COSTRUTTORE E GETTER INSTANZA STATICA
    @staticmethod
    def Init():
        if PaginaGestioneCategorie.paginaDispositivi == None:
            PaginaGestioneCategorie.paginaDispositivi = PaginaGestioneCategorie()
    @staticmethod
    def GetPaginaDispositivi():
        if PaginaGestioneCategorie.paginaDispositivi == None:
            PaginaGestioneCategorie.paginaDispositivi = PaginaGestioneCategorie()  
        return PaginaGestioneCategorie.paginaDispositivi
    

    # COSTRUTTORE 
    def __init__(self):

        #Salvo i colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__fontColor = Impostazioni.Tema.IGetFontColor("testo")
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]

        #Aggiungo la pagina
        PaginaGenerica.AggiungiPagina(NOME_INTERNO_PAGINA_CATEGORIE)
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
        self.__tabellaDispositivi = TabellaCategorie(master = self.__fFrameInternoCanvasScorrevole,
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi * 2,
                                            tableWidth = self.__dimensioniTabellaDispositivi[0],
                                            tableHeight = self.__dimensioniTabellaDispositivi[1],
                                            elementWidth = self.__dimensioniTabellaDispositivi[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi)
        self.__tabellaDispositivi.RefreshFrameElementi()


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
                                            text = "Categorie",
                                            background = self.__coloreSfondo,
                                            foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                            font = Impostazioni.Tema.IGetFont("titolo")
                                            )
        self.__lTitoloDispositivi.pack(side = "left", fill="both", anchor="sw")


        #FRAME DELLE SCRITTE SOPRA LA TABELLA
        self.__fFrameIntroTabella = tk.Frame(master = self.__fFrameInternoCanvasScorrevole, background = Impostazioni.Tema.IGetColoriSfondo("secondario")[2], highlightcolor = self.__coloreBordo, highlightthickness = 1)
        self.__fFrameIntroTabella.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi*2, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, anchor = "nw")
        self.__fFrameIntroTabella.columnconfigure(0, weight = 1)
        self.__fFrameIntroTabella.rowconfigure(0, weight = 1)
        self.__fFrameIntroTabella.grid_propagate(False)
        self.__fFrameIntroTabella.pack_propagate(False)
        #Creo il label 
        self.__lIntroTabella = tk.Label(master= self.__fFrameIntroTabella,
                                text = "Categoria",
                                bg = self.__coloreSfondo,
                                font = self.__font,
                                fg = self.__fontColor
                                )
        self.__lIntroTabella.grid(row = 0, column = 0, sticky="nsew")
        self.__lIntroTabella.pack(side="left")


        # CREO IL FRAME PRINCIPALE - MODIFICA ATTRIBUTI
        self.__fFrameAggiuntaCategoria = tk.Frame(master = self.__fFrameInternoCanvasScorrevole, background = self.__coloreSfondo, highlightcolor = Impostazioni.Tema.IGetColoriSfondo("secondario")[3], highlightthickness = 1)
        self.__fFrameAggiuntaCategoria.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, anchor = "nw")
        self.__fFrameAggiuntaCategoria.rowconfigure(0, weight = 1)
        self.__fFrameAggiuntaCategoria.columnconfigure(0, weight = int(100 * (1 - (PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI/2))))
        self.__fFrameAggiuntaCategoria.columnconfigure(1, weight = int(100 * (PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI/2)))
        self.__fFrameAggiuntaCategoria.grid_propagate(False)

        # BARRA INSERIMENTO NOME
        self.__myBarraInserimentoNome = MyBarraInserimento(master = self.__fFrameAggiuntaCategoria, text = "Categoria", looseContentOnFirstFocus = True, hover = True)
        self.__myBarraInserimentoNome.grid(row = 0, column = 0, sticky="nsew")

        # DEFINISCO PROPORZIONI BOTTONI SPAZIO BOTTONI
        self.__rapportoSpaziAltoBottoni = 0.05
        self.__rapportoSpaziLatoBottoni = 0.10
        self.__mantieniProporzioniImmagine = False
        dimBottoni = (20,20)
        # SUPPORTO BOTTONE
        self.__fFrameSupportoBottoneAggiuntaCategoria = tk.Frame(master = self.__fFrameAggiuntaCategoria, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameSupportoBottoneAggiuntaCategoria.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameSupportoBottoneAggiuntaCategoria.rowconfigure(0, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoneAggiuntaCategoria.rowconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziAltoBottoni * 2)))
        self.__fFrameSupportoBottoneAggiuntaCategoria.rowconfigure(2, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoneAggiuntaCategoria.columnconfigure(0, weight = int(100 * self.__rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoneAggiuntaCategoria.columnconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoneAggiuntaCategoria.columnconfigure(2, weight = int(100 * self.__rapportoSpaziLatoBottoni * 1.5))
        self.__fFrameSupportoBottoneAggiuntaCategoria.grid_propagate(False)
        self.__fFrameSupportoBottoneAggiuntaCategoria.pack_propagate(False)
        # IMMAGINE CONFERMA
        self.__fFrameBottoneAggiuntaCategoria = tk.Frame(master = self.__fFrameSupportoBottoneAggiuntaCategoria, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneAggiuntaCategoria.grid(row = 1, column = 1, sticky = "nsew")
        self.__fFrameBottoneAggiuntaCategoria.rowconfigure(0, weight = 1)
        self.__fFrameBottoneAggiuntaCategoria.columnconfigure(0, weight = 1)
        self.__fFrameBottoneAggiuntaCategoria.grid_propagate(False)
        self.__fFrameBottoneAggiuntaCategoria.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneAggiuntaCategoria = tk.Canvas(master = self.__fFrameBottoneAggiuntaCategoria, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneAggiuntaCategoria.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneAggiuntaCategoria.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneAggiuntaCategoria.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneAggiuntaCategoria.grid_propagate(False)
        self.__cCanvasBottoneAggiuntaCategoria.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneAggiuntaCategoria = MyImageButton(canvas = self.__cCanvasBottoneAggiuntaCategoria, command = lambda event : self.__ConfermaAggiuntaCategoria(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneAggiuntaCategoria.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneAggiuntaCategoria.Show()

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
        self.__coloreSfondoTabella = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__fontColor = Impostazioni.Tema.IGetFontColor("testo")
        self.__tabellaDispositivi.AggiornaColoriTema()
        self.AggiornaColori()

    def AggiornaColori(self):

        #Aggiorno i colori del titolo
        self.__fFrameTitoloDispositivi.configure(background = self.__coloreSfondoTabella)
        self.__lTitoloDispositivi.configure(background = self.__coloreSfondoTabella,
                                          foreground = Impostazioni.Tema.IGetFontColor("titolo"),
                                          font = Impostazioni.Tema.IGetFont("titolo"))
        
        #
        self.__fFrameInternoCanvasScorrevole.configure(background=self.__coloreSfondoTabella)
        self.__cCanvasScorrevole.configure(background=self.__coloreSfondoTabella)
        
        #Cambio i colori della barra della tabella
        self.__fFrameIntroTabella.configure(background=self.__coloreSfondoTabella, highlightcolor=self.__coloreBordo)
        self.__fFramePrincipale.configure(background=self.__coloreSfondoTabella, highlightcolor=self.__coloreBordo)
        self.__fFrameAggiuntaCategoria.configure(background=self.__coloreSfondoTabella, highlightcolor=self.__coloreBordo)
        self.__fFrameSupportoBottoneAggiuntaCategoria.configure(background=self.__coloreSfondoTabella, highlightcolor=self.__coloreBordo)
        self.__myBarraInserimentoNome.AggiornaColoriTema()
        self.__lIntroTabella.configure(background = self.__coloreSfondoTabella,
                                 font = self.__font, 
                                 foreground = self.__fontColor, 
                                 highlightcolor = self.__coloreBordo)
        self.__lTitoloDispositivi.configure(background = self.__coloreSfondoTabella,
                                 font = self.__font, 
                                 foreground = self.__fontColor, 
                                 highlightcolor = self.__coloreBordo)
        
        #Aggiorno i bottoni
        dimBottoni = (20,20)
        self.__myImgbBottoneAggiuntaCategoria.ChangeImage(Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_CONFERMA_AGGIUNTA_PAG_DISPOSITIVI))
        self.__myImgbBottoneAggiuntaCategoria.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneAggiuntaCategoria.Show()
            
        
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


        #Resize i frame
        self.__fFrameIntroTabella.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard, anchor = "nw")
        self.__fFrameAggiuntaCategoria.place(x = SPAZIO_LATI_PAGINA_DISPOSITIVI, y = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, width = self.__dimensioniTabellaDispositivi[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi, anchor = "nw")

        #Resize tabella
        self.__tabellaDispositivi.ChangeDim(
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI + Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi * 2,
                                            tableWidth = self.__dimensioniTabellaDispositivi[0],
                                            tableHeight = self.__dimensioniTabellaDispositivi[1],
                                            elementWidth = self.__dimensioniTabellaDispositivi[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                                            coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                            coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[3])

    # METODI EVENTI
    def __ConfermaAggiuntaCategoria(self, eventTk = None):
        nomeCategoria = self.__myBarraInserimentoNome.Get()

        if  GestoreDispositivi.IAddCategoria(nomeCategoria):
            GestorePagine.ICategoriaAggiunta(nomeCategoria)
            self.__myBarraInserimentoNome.Set("Categoria aggiunta")
            return
        
        self.__myBarraInserimentoNome.Set("Categoria già presente")
        
PaginaGestioneCategorie.Init()