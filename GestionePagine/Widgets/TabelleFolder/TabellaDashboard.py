from GestionePagine.Widgets.TabelleFolder.FakeTabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameDashboardIntabellabile import *

class FakeTabellaDashboard(FakeTabellaScorribile):


    # COSTRUTTORE
    def __init__(self, 
                 master : tk.Frame,
                 xPos : int = 0,
                 yPos : int = 0,
                 tableWidth : int = 250,
                 tableHeight : int = 250,
                 elementWidth : int = 50,
                 elementHeight : int = 50):


        #Chiamo il costruttore della classe padre
        super().__init__(
                        master = master,
                        funzionePopolamentoListaPerIndice = lambda i : GestoreDispositivi.IGetIdDispositivoDaIdListaOrdinata(i),
                        xPos = xPos,
                        yPos = yPos,
                        tableWidth = tableWidth,
                        tableHeight = tableHeight,
                        elementWidth = elementWidth,
                        elementHeight = elementHeight,
                        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                        coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
                        )
        
        #Attributi ordinamento frame
        self.__semaforoPosizionamentoDispositivi = Lock()
        GestoreDispositivi.ISetFunzioneNotificaCambioStatus(self.__Notifica_CambioStatoDispositivo)


    # AGGIORNA FRAMES E MOSTRA
    def GetFrameTabella(self):
        return self
    def CaricaTabella(self):
        GestoreDispositivi.IOrdinaListaDispositivi()
        self.RefreshFrameDispositivi()
        Dispositivo.pausaFinitaEvent.set()
        

    #Aggiorna i frame e gli attributi di essi
    def RefreshFrameDispositivi(self): 
        #Aggiorno il numero di frame
        self.__semaforoPosizionamentoDispositivi.acquire()
        numDispositiviRichiesto = len(GestoreDispositivi.IGetListaDispositivi())
        self.RefreshNumeroFrame(numDispositiviRichiesto, lambda i : FrameDashboardIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = 0, 
                                                                    width = self._dimensioniElemento[0], 
                                                                    height = self._dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = i),
                                                                    aggiornaAttributi = True) #Li aggiornerò dopo aver riassegnato gli id

        self.__semaforoPosizionamentoDispositivi.release()
    
    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
        coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi, cambioColoreElementi = False)
        
        #Per ogni elemento aggiorno i colori
        FrameDashboardIntabellabile.AggiornaTemaImmagini()
        for elemento in self._elementiIntabellabili:
            elemento.AggiornaColoriTema()


    # FUNZIONI NOTIFICA
    def __Notifica_CambioStatoDispositivo(self, idDispositivo : int, nuovoStato : bool = True): #Viene chiamata quando c'è un cambio stato
        idDispSuListaOrdinata = GestoreDispositivi.IGetIdListaOrdinataDaIdDispositivo(idDispositivo)
        if idDispSuListaOrdinata < self._indiciElementiInterni[0] or idDispSuListaOrdinata > self._indiciElementiInterni[1]:
            return
        self._elementiIntabellabili[idDispSuListaOrdinata - self._indiciElementiInterni[0]].AggiornaAttributiElemento(idDispositivo = idDispositivo, status = nuovoStato)

    # METODI RESIZE E PERSONALIZZAZIONE
    def CambioColore(self, coloreSfondo : str, coloreElementi : str, coloreBordoElementi : str, cambioColoreElementi : bool = False):
        #Imposto i colori
        self._coloreSfondo = coloreSfondo
        self._coloreElementi = coloreElementi
        self._coloreBordoElementi = coloreBordoElementi

        #Aggiorno i colori
        self.configure(background=coloreSfondo, highlightthickness=0)

        if cambioColoreElementi == False:
            return
        
        #Per ogni elemento aggiorno i colori
        for elemento in self._elementiIntabellabili:
            elemento.CambioColore(coloreElementi, coloreBordoElementi)

    def ChangeDim(self, 
                 xPos : int = 0,
                 yPos : int = 0,
                 tableWidth : int = 250,
                 tableHeight : int = 250,
                 elementWidth : int = 50,
                 elementHeight : int = 50,
                 coloreSfondo : str = "#FFFFFF",
                 coloreElementi : str = "#DDDDDD",
                 coloreBordoElementi : str = "#555555"
                 ):
        
        #Piazzo il frame
        self.place(x = xPos, y = yPos, width = tableWidth, height = tableHeight)
        #Aggiorno i colori
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi)
        #Aggiorno le dimensioni
        self._dimensioniTabella = [tableWidth, tableHeight]
        self._dimensioniElemento = [elementWidth, elementHeight]
        #Aggiorno i numeri elementi
        self._numOf_elementiMassimo = (tableHeight // elementHeight) + 1
        self.RefreshFrameDispositivi()
        self.Show()
