from GestionePagine.GestorePagine import *
from GestionePagine.Widgets.TabelleFolder.TabellaImpostazioni import *

#Stati di una statemachine (stati derivati da paginaGenerica, statemachine : GestorePagine)
class PaginaImpostazioni(PaginaGenerica): #Singleton
    #Creo un'istanza statica
    paginaImpostazioni = None
    sfondoPaginaImpostazioni = Impostazioni.Tema.IGetColoriSfondo("primario")

    # COSTRUTTORE E GETTER INSTANZA STATICA
    @staticmethod
    def Init():
        if PaginaImpostazioni.paginaImpostazioni == None:
            PaginaImpostazioni.paginaImpostazioni = PaginaImpostazioni()
    @staticmethod
    def GetPaginaImpostazioni():
        if PaginaImpostazioni.paginaImpostazioni == None:
            PaginaImpostazioni.paginaImpostazioni = PaginaImpostazioni()  
        return PaginaImpostazioni.paginaImpostazioni
    

    # COSTRUTTORE 
    def __init__(self):

        #Aggiungo la pagina
        PaginaGenerica.AggiungiPagina(NOME_INTERNO_PAGINA_IMPOSTAZIONI)
        GestorePagine.IAddPagina(self)
        self.__dimensioniPagina = [int(Impostazioni.sistema.dimensioniFinestra[0] * (1 - Impostazioni.sistema.PROPORZIONE_MENU_PAGINA)), Impostazioni.sistema.dimensioniFinestra[1]]
        self.__dimensioniPaginaScorrevole = [self.__dimensioniPagina[0], ALTEZZA_PAGINA_IMPOSTAZIONI]
    
        # FRAME PRINCIPALE
        self.__fFramePrincipale = tk.Frame(master = GestorePagine.IGetFramePagina())
        self.__fFramePrincipale.columnconfigure(0, weight = 1)
        self.__fFramePrincipale.rowconfigure(0, weight = 1)
        self.__fFramePrincipale.grid_propagate(False)


        # CREO IL CANVAS SCORREVOLE PER SCORRERE LA PAGINA
        self.__cCanvasScorrevole = tk.Canvas(master = self.__fFramePrincipale, 
                                             scrollregion = (0, 0, self.__dimensioniPaginaScorrevole[0], self.__dimensioniPaginaScorrevole[1]),
                                             bg = PaginaImpostazioni.sfondoPaginaImpostazioni)
        self.__cCanvasScorrevole.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasScorrevole.grid_propagate(False)
        self.__cCanvasScorrevole.pack_propagate(False)
        # FRAME INTERNO AL CANVAS
        self.__fFrameInternoCanvasScorrevole = tk.Frame(master = self.__fFramePrincipale, bg = PaginaImpostazioni.sfondoPaginaImpostazioni)
        self.__fFrameInternoCanvasScorrevole.place(x = 0, y = 0, width = self.__dimensioniPaginaScorrevole[0], height = self.__dimensioniPaginaScorrevole[1], anchor= "nw")
        self.__fFrameInternoCanvasScorrevole.columnconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.rowconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.grid_propagate(False)
        self.__fFrameInternoCanvasScorrevole.pack_propagate(False)
        # GENERO IL FRAME
        self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniPaginaScorrevole[0],
                                              height = self.__dimensioniPaginaScorrevole[1])


        # CREO LA TABELLA
        self.__dimensioniTabellaImpostazioni = [int(self.__dimensioniPagina[0] - SPAZIO_LATI_PAGINA_IMPOSTAZIONI * 2),
                                                self.__dimensioniPagina[1] - SPAZIO_ALTO_PAGINA_IMPOSTAZIONI * 2]
        self.__tabellaImpostazioni = TabellaImpostazioni(master = self.__fFrameInternoCanvasScorrevole,
                                            xPos = SPAZIO_LATI_PAGINA_IMPOSTAZIONI,
                                            yPos = SPAZIO_ALTO_PAGINA_IMPOSTAZIONI,
                                            tableWidth = self.__dimensioniTabellaImpostazioni[0],
                                            tableHeight = self.__dimensioniTabellaImpostazioni[1],
                                            elementWidth = self.__dimensioniTabellaImpostazioni[0],
                                            elementHeight = Impostazioni.personalizzazioni.altezza_elemento_tabella_paginaDispositivi)

         # EVENT BIND
        self.__fFramePrincipale.bind("<MouseWheel>", lambda event : self.__cCanvasScorrevole.yview_scroll(int(-event.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella), "units"))
        self.__fFrameInternoCanvasScorrevole.bind("<MouseWheel>", lambda event : self.__cCanvasScorrevole.yview_scroll(int(-event.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella), "units"))
         
                                           

    # METODI CAMBIO PAGINA E UPDATE
    def CaricaPagina(self, args = []):
        #Mostro la pagina
        self.__fFramePrincipale.grid_propagate(True)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.grid_propagate(False)


    def NascondiPagina(self):
        self.__fFramePrincipale.grid_forget()

    def UpdatePagina(self, deltaTime : float = 0):
        self.__tabellaImpostazioni.Update(deltaTime)

PaginaImpostazioni.Init()