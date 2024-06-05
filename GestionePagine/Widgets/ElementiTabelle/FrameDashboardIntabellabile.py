from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *

class FrameDashboardIntabellabile(ElementoIntabellabile):

    __mySMI_statusImage = MySharedMultiImg(pathsDict = {"offline" : Impostazioni.Tema.IGetPathTemaCorrente(Impostazioni.PATH_IMG_STATUS_OFFLINE_PAG_DASHBOARD),
                                                         "online" : Impostazioni.Tema.IGetPathTemaCorrente(Impostazioni.PATH_IMG_STATUS_ONLINE_PAG_DASHBOARD)})
    __mySMI_statusImage.ResizeAll(DIMENSIONI_IMMAGINE_STATUS_DASHBOARD[0], DIMENSIONI_IMMAGINE_STATUS_DASHBOARD[1])

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
        self.__fFramePrincipale = tk.Frame(self, bg = self.__coloreSfondo)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.rowconfigure(0, weight = 1)
        self.__fFramePrincipale.columnconfigure(0, weight = int(100 * PROPORZIONI_NOME_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFramePrincipale.columnconfigure(1, weight = int(100 * PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFramePrincipale.columnconfigure(2, weight = int(100 * PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFramePrincipale.columnconfigure(3, weight = int(100 * PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDASHBOARD))
        self.__fFramePrincipale.columnconfigure(4, weight = int(100 * PROPORZIONI_STATUS_DISPOSITIVO_TABELLA_DASHBOARD))
        self.__fFramePrincipale.columnconfigure(5, weight = int(100 * PROPORZIONI_PINGMANUALE_DISPOSITIVO_TABELLA_DASHBOARD))
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
        self.__fFrameScrittaIndirizzoIP = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
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
        self.__fFrameScrittaPorta = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaPorta.grid(row = 0, column = 2, sticky = "nsew")
        self.__fFrameScrittaPorta.rowconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.columnconfigure(0, weight = 1)
        self.__fFrameScrittaPorta.grid_propagate(False)
        self.__fFrameScrittaPorta.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaPorta_str = tk.StringVar() 
        self.__vScrittaPorta_str.set("Porta")
        #Creo la scritta
        self.__lScrittaPorta = tk.Label(master = self.__fFrameScrittaPorta, 
                                         textvariable = self.__vScrittaPorta_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaPorta.pack(side = "left")


        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaTempoTraPing = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaTempoTraPing.grid(row = 0, column = 3, sticky = "nsew")
        self.__fFrameScrittaTempoTraPing.rowconfigure(0, weight = 1)
        self.__fFrameScrittaTempoTraPing.columnconfigure(0, weight = 1)
        self.__fFrameScrittaTempoTraPing.grid_propagate(False)
        self.__fFrameScrittaTempoTraPing.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaTempoTraPing_str = tk.StringVar() 
        self.__vScrittaTempoTraPing_str.set("1 sec")
        #Creo la scritta
        self.__lScrittaTempoTraPing = tk.Label(master = self.__fFrameScrittaTempoTraPing, 
                                         textvariable = self.__vScrittaTempoTraPing_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaTempoTraPing.pack(side = "left")


        # SUPPORTO STATUS DISPOSITIVO
        self.__fFrameSupportoStatusDispositivo = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground = self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameSupportoStatusDispositivo.grid(row = 0, column = 4, sticky = "nsew")
        self.__fFrameSupportoStatusDispositivo.grid_propagate(False)
        self.__fFrameSupportoStatusDispositivo.pack_propagate(False)

        # CAVAS IMMAGINE STATUS DISPOSITIVO
        self.__cCanvasStatusDispositivo = tk.Canvas(master = self.__fFrameSupportoStatusDispositivo, bg = self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasStatusDispositivo.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasStatusDispositivo.rowconfigure(0, weight = 1)
        self.__cCanvasStatusDispositivo.columnconfigure(0, weight = 1)
        self.__cCanvasStatusDispositivo.grid_propagate(False)
        self.__cCanvasStatusDispositivo.pack_propagate(False)

        # IMMAGINE STATUS ONLINE
        self.__mySMIi_status = FrameDashboardIntabellabile.__mySMI_statusImage.Show(canvas = self.__cCanvasStatusDispositivo, pathKey = "offline")

        # FRAME SUPPORTO BOTTONE PING MANUALE
        self.__fFrameBottonePingManuale = tk.Frame(master = self.__fFramePrincipale, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameBottonePingManuale.grid(row = 0, column = 5, sticky = "nsew")
        self.__fFrameBottonePingManuale.rowconfigure(0, weight = 1)
        self.__fFrameBottonePingManuale.columnconfigure(0, weight = 1)
        self.__fFrameBottonePingManuale.grid_propagate(False)
        self.__fFrameBottonePingManuale.pack_propagate(False)
        #Creo il bottone
        self.__bBottonePingManuale = tk.Button(master = self.__fFrameBottonePingManuale, text = "Test", font = self.__fontTesto, fg = self.__coloreTesto, bg = self.__coloreSfondo, highlightbackground = self.__coloreBordo, highlightthickness=0.5, command = self.__BottonePingManuale)
        self.__bBottonePingManuale.grid(row = 0, column = 0, sticky="nsew")

        #Associo il dispositivo specificato
        self.AssociaDispositivo(idDispositivo)
        self.Show()

        # METODI EVENTI
        self.myBind("<Enter>", lambda event : self.__CursorEntered(event))
        self.myBind("<Leave>", lambda event : self.__CursorExited(event))


    # GETTER E SETTER
    def GetIdAssociato(self) -> Dispositivo:
        return self.__idDispositivoAssociato
    def GetDispositivoAssociato(self) -> Dispositivo:
        return GestoreDispositivi.IGetDispositivo(self.__idDispositivoAssociato)
    

    # METODI AGGIORNAMENTO FRAME
    def AggiornaAttributiElemento(self, idDispositivo : int, status : bool = None):
        self.AssociaDispositivo(idDispositvo = idDispositivo, aggiornamentoForzato = True, status = status)

    def AssociaDispositivo(self, idDispositvo : int, aggiornamentoForzato : bool = False, status : bool = None):
        #Controllo se è un nuovo dispositivo
        if ((self.__idDispositivoAssociato == idDispositvo) and not aggiornamentoForzato):
            return
        
        #Se no aggiorno i valori
        self.__idDispositivoAssociato = idDispositvo
        self.RefreshAttributiElemento(status)

    def RefreshAttributiElemento(self, status : bool = None):
        dispositivo = GestoreDispositivi.IGetDispositivo(self.__idDispositivoAssociato)
        self.__vScrittaNome_str.set(dispositivo.GetNome())
        self.__vScrittaIndirizzoIP_str.set(dispositivo.GetHost())
        self.__vScrittaPorta_str.set(dispositivo.GetPorta())
        self.__vScrittaTempoTraPing_str.set(str(dispositivo.GetTempoTraPing()))
        if status == None: 
            status = dispositivo.GetStatusConnessione() 
        self.SetStatus(status)

    def SetStatus(self, status : bool):
        if status == True: 
            print("ONLINE inserito")
            self.__mySMIi_status = FrameDashboardIntabellabile.__mySMI_statusImage.Show(self.__cCanvasStatusDispositivo, pathKey = "online", instanceId = self.__mySMIi_status)
        else:
            print("OFFLINE inserito")
            self.__mySMIi_status = FrameDashboardIntabellabile.__mySMI_statusImage.Show(self.__cCanvasStatusDispositivo, pathKey = "offline", instanceId = self.__mySMIi_status)
    
    

    # METODI AGGIORNAMENTO
    def Update(self, deltaTime : float = 0): #Disabled 
        return
    
    

    # METODI PERSONALIZZAZIONE
    @staticmethod
    def AggiornaTemaImmagini():
        FrameDashboardIntabellabile.__mySMI_statusImage.ChangePaths(newPathsDict = {"offline" : Impostazioni.Tema.IGetPathTemaCorrente(Impostazioni.PATH_IMG_STATUS_OFFLINE_PAG_DASHBOARD),
                                                                    "online" : Impostazioni.Tema.IGetPathTemaCorrente(Impostazioni.PATH_IMG_STATUS_ONLINE_PAG_DASHBOARD)})
        FrameDashboardIntabellabile.__mySMI_statusImage.ResizeAll(DIMENSIONI_IMMAGINE_STATUS_DASHBOARD[0], DIMENSIONI_IMMAGINE_STATUS_DASHBOARD[1])
    
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreSfondoEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreTesto = Impostazioni.Tema.IGetFontColor("testo")
        pathKey = "online" if GestoreDispositivi.IGetDispositivo(self.__idDispositivoAssociato).GetStatusConnessione() == True else "offline"
        self.__mySMIi_status = FrameDashboardIntabellabile.__mySMI_statusImage.Show(canvas = self.__cCanvasStatusDispositivo, pathKey = pathKey, instanceId = self.__mySMIi_status)
        self.AggiornaColori()

    def AggiornaColori(self):
        #Frame
        self.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaTempoTraPing.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo, font = self.__fontTesto, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondo, font = self.__fontTesto, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        self.__lScrittaPorta.configure(background=self.__coloreSfondo, font = self.__fontTesto,  foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        self.__lScrittaTempoTraPing.configure(background=self.__coloreSfondo, font = self.__fontTesto, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)
        #Canvas
        self.__cCanvasStatusDispositivo.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        #Bottone
        self.__fFrameBottonePingManuale.configure(background=self.__coloreSfondo, highlightbackground= self.__coloreBordo)
        self.__bBottonePingManuale.configure(background=self.__coloreSfondo, font = self.__fontTesto, foreground=self.__coloreTesto, highlightbackground = self.__coloreBordo, highlightcolor = self.__coloreBordo)


    # METODI EVENTI
    def __Evidenzia(self):
        #Frame
        self.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaTempoTraPing.configure(background=self.__coloreSfondoEvidenziato)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondoEvidenziato)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondoEvidenziato)
        self.__lScrittaPorta.configure(background=self.__coloreSfondoEvidenziato)
        self.__lScrittaTempoTraPing.configure(background=self.__coloreSfondoEvidenziato)
        #Canvas
        self.__cCanvasStatusDispositivo.configure(background=self.__coloreSfondoEvidenziato)

    def __TogliEvidenziatura(self):
        #Frame
        self.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaIndirizzoIP.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaPorta.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaTempoTraPing.configure(background=self.__coloreSfondo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo)
        self.__lScrittaIndirizzoIP.configure(background=self.__coloreSfondo)
        self.__lScrittaPorta.configure(background=self.__coloreSfondo)
        self.__lScrittaTempoTraPing.configure(background=self.__coloreSfondo)
        #Canvas
        self.__cCanvasStatusDispositivo.configure(background=self.__coloreSfondo)

    def __CursorEntered(self, tkEvent = None):
        self.__Evidenzia()
        
    def __CursorExited(self, tkEvent = None):
        self.__TogliEvidenziatura()

    def __BottonePingManuale(self, eventTk = None):
        GestoreDispositivi.IPingManuale(self.__idDispositivoAssociato)

    def myBind(self, evento : str, funzione):

        #Frame principali
        self.bind(evento, funzione)
        self.__fFramePrincipale.bind(evento, funzione)
        
        #Frame scritte
        self.__fFrameScrittaIndirizzoIP.bind(evento, funzione)
        self.__fFrameScrittaNome.bind(evento, funzione)
        self.__fFrameScrittaPorta.bind(evento, funzione)
        self.__fFrameScrittaTempoTraPing.bind(evento, funzione)
        self.__fFrameBottonePingManuale.bind(evento, funzione)

        #Scritte
        self.__lScrittaIndirizzoIP.bind(evento, funzione)
        self.__lScrittaNome.bind(evento, funzione)
        self.__lScrittaPorta.bind(evento, funzione)
        self.__lScrittaTempoTraPing.bind(evento, funzione)

        #Bottone
        self.__bBottonePingManuale.bind(evento, funzione)

        #Frame status dispositivo
        self.__fFrameSupportoStatusDispositivo.bind(evento, funzione)
        self.__cCanvasStatusDispositivo.bind(evento, funzione)




    # METODI DI SPECIFICA LAYOUT

    

