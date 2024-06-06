from GestionePagine.Widgets.TabelleFolder.FakeTabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameCategoriaIntabellabile import *
from GestioneFiltri.GestoreFiltri import * 


class TabellaCategorie(FakeTabellaScorribile):

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

        
        #Chiamo il costruttore della classe padre
        super().__init__(
                        master = master,
                        funzionePopolamentoListaPerIndice = lambda i : i,
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
        
        MyEventHandler.BindEvent(MyCategoriaAggiunta, lambda nomeCategoria : self.__Notifica_RebuildListaNecessario(nomeCategoria))
        MyEventHandler.BindEvent(MyCategoriaEliminata, lambda nomeCategoria : self.__Notifica_RebuildListaNecessario(nomeCategoria))
        MyEventHandler.BindEvent(MyCategoriaModificata, lambda nomeCategoriaPrecedente, nomeCategoriaNuovo : self.__Notifica_RefreshListaNecessario(nomeCategoriaNuovo))
   
    
    # AGGIORNAMENTO FRAME
    def CaricaTabella(self):
        self.RefreshFrameElementi(aggiornaAttributi=True)
        self.Show()

    #Aggiorna il numero di frame presenti sulla dashboard
    def RefreshFrameElementi(self, aggiornaAttributi : bool = False):
        numElementiRichiesto = len(Dispositivo.categorie)
        #Aggiunge e rimuove gli elementi in base a quanti ne mancano e l'iteratore
        self.RefreshNumeroFrame(numElementiRichiesto, lambda i : FrameCategoriaIntabellabile(master = self.GetFrame(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self._dimensioniElemento[1], 
                                                                    width = self._dimensioniElemento[0], 
                                                                    height = self._dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idCategoria = i))
        if aggiornaAttributi: 
            self.AggiornaAttributi()
        self.Show()
    
    # FUNZIONI NOTIFICA
    def __Notifica_AggiornamentoElementoNecessario(self, idElemento : int, stato : bool):
        if idElemento < self._indiciElementiInterni[0] or idElemento > self._indiciElementiInterni[1]: 
            return
        idFakeElemento = idElemento - self._indiciElementiInterni[0]
        self._elementiIntabellabili[idFakeElemento].AggiornaAttributiElemento(i_categoria = idElemento)
    def __Notifica_RefreshListaNecessario(self, nomeCategoria : int):
        self.RefreshFrameElementi(aggiornaAttributi = True)
    def __Notifica_RebuildListaNecessario(self, nomeCategoria : int):
        self.RefreshFrameElementi(aggiornaAttributi = True)


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi, cambioColoreElementi = False)
        
        #Per ogni elemento aggiorno i colori
        FrameCategoriaIntabellabile.AggiornaImmagineTema()
        for elemento in self._elementiIntabellabili:
            elemento.AggiornaColoriTema()



    # METODI UPDATE FRAME
    def Update(self, deltaTime : float = 0): #Disabled
        return
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.Update(deltaTime)