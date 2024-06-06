from GestionePagine.GestorePagine import *
from Utility.FUtility import *
import Utility.Impostazioni.Impostazioni as Impostazioni

#Conterra le informazioni del frame, nome mostrato e nome pagina interno
class ElementoMenu(tk.Frame): #Occuperà meno del frame a disposizione

    def myDistruttore(self):
        self.place_forget()
        
    def __init__(self, 
                 master : tk.Frame,
                 nomePaginaMostrato : str,
                 nomePaginaInterno : str,
                 pathImmagine : str = None,
                 width : int = 0,
                 height : int = 0,
                 xPos : int = 0,
                 yPos : int = 0
                ):
                

        #Attributi pagina
        self.__master = master
        self.__nomePaginaMostrato = nomePaginaMostrato
        self.__nomePaginaInterno = nomePaginaInterno
        self.__pathImmagine = pathImmagine
        self.__posizione = [xPos, yPos]
        self.__dimensione = [width, height]

        #Attributi colorazione
        self.__elementoSelezionato = True
        self.__coloreStandard = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreSelezionato = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__coloreFont = Impostazioni.Tema.IGetFontColor("testo")

        #Creo il frame principale
        super().__init__(master = self.__master, width = width, height = height, bg = self.__coloreStandard)
        self.place(x = xPos, y = yPos, width = width, height = height, anchor = "nw")
        self.rowconfigure(0, weight = int(100 * PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_ALTEZZA))
        self.rowconfigure(1, weight = int(100 * (1-PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_ALTEZZA)))
        self.rowconfigure(2, weight = int(100 * PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_ALTEZZA))
        self.columnconfigure(0, weight = int((100/2) * PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_LARGHEZZA))
        self.columnconfigure(1, weight = int(100 * PROPORZIONE_IMMAGINE_SCRITTA_ELEMENTO_MENU * (1 - PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_LARGHEZZA)))
        self.columnconfigure(2, weight = int(100 * (1 - PROPORZIONE_IMMAGINE_SCRITTA_ELEMENTO_MENU) * (1 - PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_LARGHEZZA)))
        self.columnconfigure(3, weight = int((100/2) * PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_LARGHEZZA))
        self.grid_propagate(False)
        self.pack_propagate(False)
        
        
        #Creo due sottoframe, uno per l'eventuale immagine da mostrare, l'altro per il testo

        # FRAME SUPPORTO IMMAGINE
        self.__fFrameImmagine = tk.Frame(master = self, highlightthickness = 0)
        self.__fFrameImmagine.place(x = 0, y = 0, width = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[0]+1, height = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[1])
        #Creo il canvas per l'immagine
        self.__cCanvasImmagine = tk.Canvas(master = self.__fFrameImmagine, background = self.__coloreStandard, highlightthickness= 0)
        self.__cCanvasImmagine.place(x = 0, y = 0, width = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[0]+1, height = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[1])
        #Creo l'immagine
        self.__myImgImmagine = MyImageTk(canvas = self.__cCanvasImmagine, path = Impostazioni.Tema.IGetPathTemaCorrente(self.__pathImmagine))
        self.__myImgImmagine.Resize(width = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[0], height = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[1])
        self.__myImgImmagine.Show()

        # FRAME SUPPORTO SCRITTA
        self.__fFrameScrittaPagina = tk.Frame(master = self, bg = self.__coloreStandard)
        self.__fFrameScrittaPagina.place(x = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[0] + 1, y = 0, width = 250, height = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)
        self.__fFrameScrittaPagina.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaPagina_str = tk.StringVar() 
        self.__vScrittaPagina_str.set(self.__nomePaginaMostrato)
        #Creo la scritta
        self.__lScrittaPagina = tk.Label(master = self.__fFrameScrittaPagina, 
                                         textvariable = self.__vScrittaPagina_str, 
                                         font = self.__font, 
                                         fg =  self.__coloreFont,
                                         bg = self.__coloreStandard)
        self.__lScrittaPagina.pack(side = "left", fill = "both", expand = True)


        #Bindo gli eventi importanti
        self.CambioColore(self.__coloreSelezionato) #Lo inizializzo selezionato, verranno deselezionati quelli non caricati
        self.myBind("<Button-1>", lambda event : self.__ElementoPremuto(event))
        self.myBind("<Enter>", lambda event : self.__CursorEntered(event))
        self.myBind("<Leave>", lambda event : self.__CursorExited(event))


    # GET
    def GetNomePaginaInterno(self):
        return self.__nomePaginaInterno
    def GetFramePrincipale(self):
        return self
    def SetPos(self, x : int, y : int): #Setta la posizione
        self.__posizione = [x, y]


    # METODI
    def CambioColore(self, colore : str):
        self.configure(background=colore)
        self.__fFrameImmagine.configure(background=colore)
        self.__fFrameScrittaPagina.configure(background=colore)
        self.__lScrittaPagina.configure(background=colore)


     # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        self.__coloreStandard = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreSelezionato = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
        self.__font = Impostazioni.Tema.IGetFont("testo")
        self.__coloreFont = Impostazioni.Tema.IGetFontColor("testo")

        #Cambio la path dell'immagine
        self.__myImgImmagine.ChangeImage(newPath = Impostazioni.Tema.IGetPathTemaCorrente(self.__pathImmagine))
        self.__myImgImmagine.Resize(width = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[0], height = DIMENSIONI_IMMAGINE_ELEMENTO_MENU[1])
        self.__myImgImmagine.Show()
        
        #Lo imposto come selezionato e faccio partire la deselezione elemento 
        self.__elementoSelezionato = True
        self.CambioColore(self.__coloreSelezionato)
        self.__lScrittaPagina.configure(background=self.__coloreSelezionato, font = self.__font, fg= self.__coloreFont)


    # METODI UPDATE
    def Update(self, deltaTime : float = 0): #Disabled
        return              
            

    # METODI EVENTI
    def __ElementoPremuto(self, eventTk = None):
        self.__ElementoSelezionato()
        GestorePagine.ICaricaPaginaConNome(self.__nomePaginaInterno)

    def __ElementoSelezionato(self):
        self.__elementoSelezionato = True
        self.CambioColore(self.__coloreSelezionato)
    
    def ElementoDeselezionato(self):
        if self.__elementoSelezionato == False:
            return
        self.__elementoSelezionato = False
        self.CambioColore(self.__coloreStandard)

    def __CursorEntered(self, tkEvent = None):
        if self.__elementoSelezionato == True:
            return
        self.CambioColore(self.__coloreEvidenziato)

    def __CursorExited(self, tkEvent = None):
        if self.__elementoSelezionato == True:
            return
        self.CambioColore(self.__coloreStandard)
    
    def myBind(self, evento : str, funzione):
        self.bind(evento, funzione)
        self.__fFrameImmagine.bind(evento, funzione)
        self.__fFrameScrittaPagina.bind(evento, funzione)
        self.__lScrittaPagina.bind(evento, funzione)

    
    # METODI RICONFIG
    def CambioDimFrame(self, width : int, height : int):
        self.place(x = self.__posizione[0], y = self.__posizione[1], width = width, height = height, anchor = "nw")