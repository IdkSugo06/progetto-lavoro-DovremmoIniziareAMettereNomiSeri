from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *

class FrameDispositivoIntabellabile(ElementoIntabellabile):

    def __init__(self,
                 master, 
                 x : int = 0, 
                 y : int = 0,
                 width : int = 250, 
                 height : int = 50,
                 isShown : bool = True,
                 idDispositivo : int = 0):
        
        #Salvo i colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreSfondoEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreTesto = Impostazioni.Tema.IGetFontColor("testo")

        # Chiamo il costruttore della classe padre
        super().__init__(
                 master,
                 x, 
                 y,
                 width, 
                 height,
                 False,
                 colore = self.__coloreSfondo,
                 coloreBordo = self.__coloreBordo,
                 spessoreBordo = 0)
        
        #Attributi 
        self.__idDispositivoAssociato = None    

        # CREO IL FRAME PRINCIPALE
        self.__fFramePrincipale = tk.Frame(self, bg =  self.__coloreSfondo)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.rowconfigure(0, weight = 1)
        self.__fFramePrincipale.columnconfigure(0, weight = int(100 * PROPORZIONI_NOME_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFramePrincipale.columnconfigure(1, weight = int(100 * PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFramePrincipale.columnconfigure(2, weight = int(100 * PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFramePrincipale.columnconfigure(3, weight = int(100 * PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDISPOSITIVO))
        self.__fFramePrincipale.columnconfigure(4, weight = int(100 * PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI))
        self.__fFramePrincipale.grid_propagate(False)
        

        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaNome = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaNome.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameScrittaNome.rowconfigure(0, weight = 1)
        self.__fFrameScrittaNome.columnconfigure(0, weight = 1)
        self.__fFrameScrittaNome.grid_propagate(False)
        self.__fFrameScrittaNome.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaNome_str = tk.StringVar() 
        self.__vScrittaNome_str.set("Nome")
        #Creo la scritta
        self.__lScrittaNome = tk.Label(master = self.__fFrameScrittaNome, 
                                         textvariable = self.__vScrittaNome_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaNome.pack(side = "left")


        # FRAME SUPPORTO SCRITTA INDIRIZZO IP
        self.__fFrameScrittaIndirizzoIP = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaIndirizzoIP.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameScrittaIndirizzoIP.rowconfigure(0, weight = 1)
        self.__fFrameScrittaIndirizzoIP.columnconfigure(0, weight = 1)
        self.__fFrameScrittaIndirizzoIP.grid_propagate(False)
        self.__fFrameScrittaIndirizzoIP.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaIndirizzoIP_str = tk.StringVar() 
        self.__vScrittaIndirizzoIP_str.set("IndirizzoIp")
        #Creo la scritta
        self.__lScrittaIndirizzoIP = tk.Label(master = self.__fFrameScrittaIndirizzoIP, 
                                         textvariable = self.__vScrittaIndirizzoIP_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaIndirizzoIP.pack(side = "left")


        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaPorta = tk.Frame(master = self.__fFramePrincipale, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaPorta.grid(row = 0, column = 2, sticky = "nsew")
        self.__fFrameScrittaPorta.rowconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.columnconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.grid_propagate(False)
        self.__fFrameScrittaPorta.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaPorta_str = tk.StringVar() 
        self.__vScrittaPorta_str.set("ScrittaPorta")
        #Creo la scritta
        self.__lScrittaPorta = tk.Label(master = self.__fFrameScrittaPorta, 
                                         textvariable = self.__vScrittaPorta_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaPorta.pack(side = "left")

    
        # FRAME SUPPORTO SCRITTA TEMPO PING
        self.__fFrameScrittaTempoPing = tk.Frame(master = self.__fFramePrincipale, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaTempoPing.grid(row = 0, column = 3, sticky = "nsew")
        self.__fFrameScrittaTempoPing.rowconfigure(0, weight = 1)
        self.__fFrameScrittaTempoPing.columnconfigure(0, weight = 1)
        self.__fFrameScrittaTempoPing.grid_propagate(False)
        self.__fFrameScrittaTempoPing.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaTempoPing_str = tk.StringVar() 
        self.__vScrittaTempoPing_str.set("1 sec")
        #Creo la scritta
        self.__lScrittaTempoPing = tk.Label(master = self.__fFrameScrittaTempoPing, 
                                         textvariable = self.__vScrittaTempoPing_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaTempoPing.pack(side = "left")


        # DEFINISCO PROPORZIONI BOTTONI SPAZIO BOTTONI
        rapportoSpaziAltoBottoni = 0.05
        rapportoSpaziLatoBottoni = 0.10
        mantieniProporzioniImmagine = False
        self.__proporzioneBottoniPaginaX = PROPORZIONE_LARGHEZZA_TABELLA_DISPOSITIVI_LARGHEZZA_PAGINA * PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI * (1 - rapportoSpaziLatoBottoni * 3.5) * 0.5
        self.__proporzioneBottoniAltezzaElDispositivo = (1 - rapportoSpaziAltoBottoni * 2)
        dimBottoni = self.__getDimensioniPulsantiBottoni()

        # SUPPORTO BOTTONI
        self.__fFrameSupportoBottoni = tk.Frame(master = self.__fFramePrincipale, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameSupportoBottoni.grid(row = 0, column = 4, sticky = "nsew")
        self.__fFrameSupportoBottoni.rowconfigure(0, weight = int(100 * rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoni.rowconfigure(1, weight = int(100 * (1 - rapportoSpaziAltoBottoni * 2)))
        self.__fFrameSupportoBottoni.rowconfigure(2, weight = int(100 * rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoni.columnconfigure(0, weight = int(100 * rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoni.columnconfigure(1, weight = int(100 * (1 - rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoni.columnconfigure(2, weight = int(100 * rapportoSpaziLatoBottoni * 1.5))
        self.__fFrameSupportoBottoni.columnconfigure(3, weight = int(100 * (1 - rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoni.columnconfigure(4, weight = int(100 * rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoni.grid_propagate(False)
        self.__fFrameSupportoBottoni.pack_propagate(False)

        # FRAME SUPPORTO BOTTONE MODIFICA
        self.__fFrameBottoneModifica = tk.Frame(master = self.__fFrameSupportoBottoni, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneModifica.grid(row = 1, column = 1, sticky = "nsew")
        self.__fFrameBottoneModifica.rowconfigure(0, weight = 1)
        self.__fFrameBottoneModifica.columnconfigure(0, weight = 1)
        self.__fFrameBottoneModifica.grid_propagate(False)
        self.__fFrameBottoneModifica.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneModifica = tk.Canvas(master = self.__fFrameBottoneModifica, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneModifica.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneModifica.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneModifica.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneModifica.grid_propagate(False)
        self.__cCanvasBottoneModifica.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneModifica = MyImageButton(canvas = self.__cCanvasBottoneModifica, command = lambda event : self.__ModificaDispositivoAssociato(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_MODIFICA_PAG_DISPOSITIVI))
        self.__myImgbBottoneModifica.Resize(dimBottoni[0], dimBottoni[1], mantieniProporzioniImmagine)
        self.__myImgbBottoneModifica.Show()
        


        self.__fFrameBottoneElimina = tk.Frame(master = self.__fFrameSupportoBottoni, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneElimina.grid(row = 1, column = 3, sticky = "nsew")
        self.__fFrameBottoneElimina.rowconfigure(0, weight = 1)
        self.__fFrameBottoneElimina.columnconfigure(0, weight = 1)
        self.__fFrameBottoneElimina.grid_propagate(False)
        self.__fFrameBottoneElimina.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneElimina = tk.Canvas(master = self.__fFrameBottoneElimina, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneElimina.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneElimina.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneElimina.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneElimina.grid_propagate(False)
        self.__cCanvasBottoneElimina.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneElimina = MyImageButton(canvas = self.__cCanvasBottoneElimina, command = lambda event : self.__EliminaDispositivoAssociato(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneElimina.Resize(dimBottoni[0], dimBottoni[1], mantieniProporzioniImmagine)
        self.__myImgbBottoneElimina.Show()


        #Associo il dispositivo specificato
        self.AssociaDispositivo(idDispositivo)
        self.Show()


        # METODI EVENTI
        self.myBind("<Enter>", lambda event : self.__CursorEntered(event))
        self.myBind("<Leave>", lambda event : self.__CursorExited(event))



    # METODI PRIVATI
    def __getDimensioniPulsantiBottoni(self):
        return (int(self.__proporzioneBottoniPaginaX * (1-Impostazioni.PROPORZIONE_MENU_PAGINA) * Impostazioni.sistema.dimensioniFinestra[0]), int(self.__proporzioneBottoniAltezzaElDispositivo * Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi))



    # METODI GESTIONE DISPOSITIVI
    def AssociaDispositivo(self, idDispositivo : int):
        #Controllo se è un nuovo dispositivo
        if (self.__idDispositivoAssociato == idDispositivo):
            return

        #Se no aggiorno i valori
        self.__idDispositivoAssociato = idDispositivo
        self.RefreshAttributiElemento()

    def RefreshAttributiElemento(self):
        dispositivo = GestoreDispositivi.IGetDispositivo(self.__idDispositivoAssociato)
        self.__vScrittaNome_str.set(dispositivo.GetNome())
        self.__vScrittaIndirizzoIP_str.set(dispositivo.GetHost())
        self.__vScrittaPorta_str.set(dispositivo.GetPorta())
        self.__vScrittaTempoPing_str.set(str(dispositivo.GetTempoTraPing()))

    def __ModificaDispositivoAssociato(self, eventTk = None):
        InterfacciaGestioneDispositivi.IRemoveDispositivo(self.__idDispositivoAssociato)
        GestorePagine.ICaricaPagina(PaginaGenerica.GetIdPagina(NOME_INTERNO_PAGINA_MODIFICA_DISPOSITIVO), self.__idDispositivoAssociato)

    def __EliminaDispositivoAssociato(self, eventTk = None):
        GestorePagine.IRicaricaPagina()



    # METODI START UPDATE FINISH
    def Update(self, deltaTime : float = 0): #Disabled
        return
    


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreSfondoEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreTesto = Impostazioni.Tema.IGetFontColor("testo")
        self.AggiornaColori()

    def AggiornaColori(self):
        #Frame
        self.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondo, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        self.__lScrittaPorta.configure(background=self.__coloreSfondo, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)



    # METODI EVENTI
    def __Evidenzia(self):
        #Frame
        self.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondoEvidenziato)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondoEvidenziato)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondoEvidenziato)
        self.__lScrittaPorta.configure(background=self.__coloreSfondoEvidenziato)

    def __TogliEvidenziatura(self):
        #Frame
        self.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondo)
        self.__lScrittaPorta.configure(background=self.__coloreSfondo)

    def __CursorEntered(self, tkEvent = None):
        self.__Evidenzia()
        
    def __CursorExited(self, tkEvent = None):
        self.__TogliEvidenziatura()

    def myBind(self, evento : str, funzione):

        #Frame principali
        self.bind(evento, funzione)
        self.__fFramePrincipale.bind(evento, funzione)
        
        #Frame scritte
        self.__fFrameScrittaIndirizzoIP.bind(evento, funzione)
        self.__fFrameScrittaNome.bind(evento, funzione)
        self.__fFrameScrittaPorta.bind(evento, funzione)
        self.__fFrameScrittaTempoPing.bind(evento, funzione)

        #Scritte
        self.__lScrittaIndirizzoIP.bind(evento, funzione)
        self.__lScrittaNome.bind(evento, funzione)
        self.__lScrittaPorta.bind(evento, funzione)
        self.__lScrittaTempoPing.bind(evento, funzione)

        #Frame bottoni
        self.__fFrameSupportoBottoni.bind(evento, funzione)
        self.__fFrameBottoneElimina.bind(evento, funzione)
        self.__fFrameBottoneModifica.bind(evento, funzione)

        #Canvas
        self.__cCanvasBottoneElimina.bind(evento, funzione)
        self.__cCanvasBottoneModifica.bind(evento, funzione)



    # METODI DI SPECIFICA LAYOUT

    

