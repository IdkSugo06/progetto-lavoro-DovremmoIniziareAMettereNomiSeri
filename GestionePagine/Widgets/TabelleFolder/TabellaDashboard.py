from GestionePagine.Widgets.TabelleFolder.FakeTabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameDashboardIntabellabile import *
from GestioneFiltri.GestoreFiltri import * 


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

        #Filtro
        self.__gestoreFiltri = GestoreFiltri(nomeFiltro = NOME_INTERNO_FILTRO_STATUSOFFON,
                                             funzioneElementoCambiato = lambda x,y : self.__Notifica_AggiornamentoElementoNecessario(x,y),
                                             funzioneRefreshTabella = self.__Notifica_RefreshListaNecessario,
                                             funzioneRebuildTabella = self.__Notifica_RebuildListaNecessario)
        
        #Chiamo il costruttore della classe padre
        super().__init__(
                        master = master,
                        funzionePopolamentoListaPerIndice = lambda i : self.__gestoreFiltri.GetIdDispositivo(i),
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
        


    # AGGIORNA FRAMES E MOSTRA
    def GetFrameTabella(self):
        return self
    def CaricaTabella(self):
        GestoreDispositivi.IOrdinaListaDispositivi()
        self.RefreshFrameDispositivi()
        Dispositivo.pausaFinitaEvent.set()
        
    def CambioFiltro(self, nomeInternoFiltro : str):
        self.__gestoreFiltri.ImpostaFiltro(nomeFiltro = nomeInternoFiltro)
        self.RefreshFrameDispositivi(aggiornaAttributi = True)

    #Aggiorna i frame e gli attributi di essi
    def RefreshFrameDispositivi(self, aggiornaAttributi : bool = False): 
        #Aggiorno il numero di frame
        self.__semaforoPosizionamentoDispositivi.acquire()
        numDispositiviRichiesto = self.__gestoreFiltri.GetNumElementi()
        self.RefreshNumeroFrame(numDispositiviRichiesto, lambda i : FrameDashboardIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = 0, 
                                                                    width = self._dimensioniElemento[0], 
                                                                    height = self._dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = i)) #Li aggiornerò dopo aver riassegnato gli id
        if aggiornaAttributi: 
            self.AggiornaAttributi()
        self.__semaforoPosizionamentoDispositivi.release()

    # FUNZIONI NOTIFICA
    def __Notifica_AggiornamentoElementoNecessario(self, idElemento : int, stato : bool):
        if idElemento < self._indiciElementiInterni[0] or idElemento > self._indiciElementiInterni[1]: 
            return
        idFakeElemento = idElemento - self._indiciElementiInterni[0]
        self._elementiIntabellabili[idFakeElemento].AggiornaAttributiElemento(idDispositivo = self.__gestoreFiltri.GetIdDispositivo(idElemento), status = stato)
    def __Notifica_RefreshListaNecessario(self):
        self.RefreshFrameDispositivi(aggiornaAttributi = True) 
    def __Notifica_RebuildListaNecessario(self):
        self.RefreshFrameDispositivi(aggiornaAttributi = True)


    # METODI RESIZE E PERSONALIZZAZIONE
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
        #Cambio la dimensione degli elementi
        for elemento in self._elementiIntabellabili:
            elemento.SetDim(self._dimensioniElemento[0], self._dimensioniElemento[1])
        self.Show()
