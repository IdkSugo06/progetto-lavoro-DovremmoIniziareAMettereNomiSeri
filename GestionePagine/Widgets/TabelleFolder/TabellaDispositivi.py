from GestionePagine.Widgets.TabelleFolder.FakeTabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameDispositivoIntabellabile import *
from GestioneFiltri.GestoreFiltri import * 


class  TabellaDispositivi(FakeTabellaScorribile):


    # COSTRUTTORE
    def __init__(self, 
                 master : tk.Frame,
                 xPos : int = 0,
                 yPos : int = 0,
                 tableWidth : int = 250,
                 tableHeight : int = 250,
                 elementWidth : int = 50,
                 elementHeight : int = 50,
                 coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                 coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                 coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]):

        #Filtro
        self.__gestoreFiltri = GestoreFiltri(nomeFiltro = NOME_INTERNO_FILTRO_NOFILTRI,
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
                        coloreSfondo = coloreSfondo,
                        coloreElementi = coloreElementi,
                        coloreBordoElementi = coloreBordoElementi
                        )
   
    
    # AGGIORNAMENTO FRAME
    def CaricaTabella(self):
        self.RefreshFrameDispositivi(aggiornaAttributi=True)
        self.Show()

    #Aggiorna il numero di frame presenti sulla dashboard
    def RefreshFrameDispositivi(self, aggiornaAttributi : bool = False):
        numDispositiviRichiesto = self.__gestoreFiltri.GetNumElementi()
        #Aggiunge e rimuove gli elementi in base a quanti ne mancano e l'iteratore
        self.RefreshNumeroFrame(numDispositiviRichiesto, lambda i : FrameDispositivoIntabellabile(master = self.GetFrame(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self._dimensioniElemento[1], 
                                                                    width = self._dimensioniElemento[0], 
                                                                    height = self._dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = i))
        if aggiornaAttributi: 
            self.AggiornaAttributi()


    def CambioFiltro(self, nomeInternoFiltro : str):
        self.__gestoreFiltri.ImpostaFiltro(nomeFiltro = nomeInternoFiltro)
        self.RefreshFrameDispositivi(aggiornaAttributi = True)
    
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


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
        coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi, cambioColoreElementi = False)
        
        #Per ogni elemento aggiorno i colori
        FrameDispositivoIntabellabile.AggiornaImmagineTema()
        for elemento in self._elementiIntabellabili:
            elemento.AggiornaColoriTema()



    # METODI UPDATE FRAME
    def Update(self, deltaTime : float = 0): #Disabled
        return
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.Update(deltaTime)