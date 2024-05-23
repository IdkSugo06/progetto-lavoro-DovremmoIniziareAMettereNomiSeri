from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *

class FrameImpostazioniIntabellabile(ElementoIntabellabile):

    def __init__(self,
                 proporzionePeso : float,
                 tipoWidget : type,         
                 argomentiCostruttoreWidget : dict[str : any],          #Parametri costruttore inputwidget, master escluso
                 tipoImpostazione : str,
                 master, 
                 x : int = 0, 
                 y : int = 0,
                 width : int = 250, 
                 height : int = 50,):
        self.__colore = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        

        # Chiamo il costruttore della classe padre
        super().__init__(
                 master,
                 x, 
                 y,
                 width, 
                 height,
                 False,
                 colore = self.__colore,
                 coloreBordo = self.__coloreBordo,
                 spessoreBordo = 0)
        


        # CREO IL FRAME PRINCIPALE
        self.__fFramePrincipale = tk.Frame(self, bg = self.__colore, highlightbackground="#DDDDDD", highlightthickness=1)
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.rowconfigure(0, weight = 1)
        self.__fFramePrincipale.columnconfigure(0, weight = 100)  #questo peso cambia la grandezza del widget
        self.__fFramePrincipale.columnconfigure(1, weight = int(100*( proporzionePeso /(1-proporzionePeso))))
        self.__fFramePrincipale.grid_propagate(False)
        

        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaImpostazione = tk.Frame(master = self.__fFramePrincipale, 
                                                    bg = self.__colore, 
                                                    highlightbackground = self.__coloreBordo)
        self.__fFrameScrittaImpostazione.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameScrittaImpostazione.rowconfigure(0,weight=1) 
        self.__fFrameScrittaImpostazione.columnconfigure(0,weight=1)
        self.__fFrameScrittaImpostazione.grid_propagate(False)


        #creo il lable che starà a sinistra
        self.__lScrittaImpostazione = tk.Label(master = self.__fFrameScrittaImpostazione, 
                                         text= tipoImpostazione, 
                                         font = Impostazioni.Tema.IGetFont("testo"), 
                                         fg = Impostazioni.Tema.IGetFontColor("testo"),
                                         bg = self.__colore)
        self.__lScrittaImpostazione.pack(side = "left")
        

        # Frame Widget che starà a destra   questo
        self.__fFrameInputWidget = tk.Frame(master = self.__fFramePrincipale, 
                                            bg = self.__colore, 
                                            highlightbackground= self.__coloreBordo)
        self.__fFrameInputWidget.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameInputWidget.rowconfigure(0, weight = 1)
        self.__fFrameInputWidget.columnconfigure(0, weight = 1)
        self.__fFrameInputWidget.grid_propagate(False)
        self.__fFrameInputWidget.pack_propagate(False)

        # Create a new grid within the input widget
        self.__inputGrid = tk.Frame(master = self.__fFrameInputWidget)

        # Set the weight for the rows and columns of the new grid
        self.__inputGrid.grid(row = 0, column = 0, sticky = "nsew")
        self.__inputGrid.rowconfigure(0, weight = 1)
        self.__inputGrid.columnconfigure(0, weight = 1)
        
        #Inizializzo il widget
        argomentiCostruttoreWidget["master"] = self.__inputGrid
        self.__myIWwidget = tipoWidget.Init(argomentiCostruttoreWidget)
        self.Show()


    # METODI
    def myBind(self, evento : str, funzione):

        #Frame principali
        self.bind(evento, funzione)
        self.__fFramePrincipale.bind(evento, funzione)
        self.__fFrameInputWidget.bind(evento, funzione)
        self.__fFrameInputWidget.bind(evento, funzione)
        self.__myIWwidget.myBind(evento, funzione)


    def GetWidget(self):
        return self.__myIWwidget