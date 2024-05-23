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
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI,
                                            tableWidth = self.__dimensioniTabellaDashboard[0],
                                            tableHeight = self.__dimensioniTabellaDashboard[1],
                                            elementWidth = self.__dimensioniTabellaDashboard[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDashboard)
        self.__tabellaDashboard.RefreshFrameDispositivi()


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

        #Resize tabella
        self.__tabellaDashboard.ChangeDim(
                                            xPos = SPAZIO_LATI_PAGINA_DISPOSITIVI,
                                            yPos = SPAZIO_ALTO_PAGINA_DISPOSITIVI,
                                            tableWidth = self.__dimensioniTabellaDashboard[0],
                                            tableHeight = self.__dimensioniTabellaDashboard[1],
                                            elementWidth = self.__dimensioniTabellaDashboard[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi,
                                            coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                                            coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                            coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[3])

PaginaDashboard.Init()