from GestionePagine.Menu.WidgetMenu.ListaMenu import *

# La pagina menù 
class Menu:

    def __init__(self):
        
        # CREO IL FRAME PRINCIPALE
        self.__fFramePrincipale = tk.Frame(master = GestorePagine.IGetFrameMenu(), background=Impostazioni.Tema.IGetColoriSfondo("secondario")[1])
        self.__fFramePrincipale.grid(row = 0, column=0, sticky="nsew")
        self.__fFramePrincipale.columnconfigure(0, weight=1)
        self.__fFramePrincipale.rowconfigure(0, weight=int(100 * (1 - PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA)))
        self.__fFramePrincipale.rowconfigure(1, weight=int(100 * PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA))
        self.__fFramePrincipale.grid_propagate(False)
        

        # FRAME LOGO
        self.__fFrameLogo = tk.Frame(master = self.__fFramePrincipale)
        self.__fFrameLogo.grid(row = 0, column=0, sticky="nsew")
        self.__fFrameLogo.rowconfigure(0, weight = 1)
        self.__fFrameLogo.columnconfigure(0, weight = 1)
        self.__fFrameLogo.grid_propagate(False)


        # CAVAS IMMAGINE LOGO
        self.__cCanvasLogo = tk.Canvas(master = self.__fFrameLogo, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[2], highlightthickness = 0)
        self.__cCanvasLogo.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasLogo.rowconfigure(0, weight = 1)
        self.__cCanvasLogo.columnconfigure(0, weight = 1)
        self.__cCanvasLogo.grid_propagate(False)
        self.__cCanvasLogo.pack_propagate(False)

        # IMMAGINE LOGO
        self.__myMImgLogo = MyImageTk(canvas = self.__cCanvasLogo, 
                                                      path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMMAGINE_LOGO))
        self.__myMImgLogo.Resize(int(Impostazioni.sistema.dimensioniFinestra[0] * (PROPORZIONE_MENU_PAGINA)), int(Impostazioni.sistema.dimensioniFinestra[1] * (1-PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA)))
        self.__myMImgLogo.Show()

        # FRAME LISTA MENU
        self.__fFrameListaMenu = tk.Frame(master = self.__fFramePrincipale, bg = Impostazioni.Tema.IGetColoriSfondo("secondario")[1], highlightbackground= "#000000", highlightthickness=1)
        self.__fFrameListaMenu.grid(row = 1, column=0, sticky="nsew")
        self.__fFrameListaMenu.rowconfigure(0, weight=1)
        self.__fFrameListaMenu.columnconfigure(0, weight=1)
        self.__fFrameListaMenu.grid_propagate(False)
        # creo la lista menu
        self.__listaMenu = ListaMenu(self.__fFrameListaMenu, LISTA_PAGINE_MENU)

        # CARICA MENU
        self.CaricaMenu()


    # METODI START UPDATE END
    def CaricaMenu(self):
        self.__fFramePrincipale.grid_propagate(True)
        self.__fFramePrincipale.grid(row = 0, column=0, sticky="nsew")
        self.__fFramePrincipale.grid_propagate(False)

    def Update(self, deltaTime : float = 0):
        self.__listaMenu.Update(deltaTime)

    
    # ALTRI METODI
    def EvidenziaPaginaSelezionata(self, nomePaginaInternoSelezionato : str):
        self.__listaMenu.EvidenziaPaginaSelezionata(nomePaginaInternoSelezionato)


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__listaMenu.AggiornaColoriTema()
        self.AggiornaColori()

    def AggiornaColori(self):
        self.__cCanvasLogo.configure(background=self.__coloreSfondo)

        #Cambio i colore della barra della tabella
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fFrameLogo.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        self.__fFrameListaMenu.configure(background=coloreSfondo, highlightcolor=coloreBordo)
        
    # METODI EVENTI    
    # METODO RICONFIGURAZIONE
    def CambioFont(self):
        pass

    def CambioDimFrame(self):
        #Resetto i frame
        self.__myMImgLogo.Resize(int(Impostazioni.sistema.dimensioniFinestra[0] * (PROPORZIONE_MENU_PAGINA)), int(Impostazioni.sistema.dimensioniFinestra[1] * (1-PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA)))
        self.__myMImgLogo.Show()
        self.__listaMenu.CambioDimFrame()

    
GestorePagine.ISetMenu(Menu())