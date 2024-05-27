from GestionePagine.Widgets.TabelleFolder.TabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameDispositivoIntabellabile import *

class  TabellaDispositivi(TabellaScorribile):


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



    # METODI MODIFICA LISTA
    def AggiungiDispositivo(self, idDispositivo : int):
        self.AggiungiElemento(FrameDispositivoIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self.dimensioniElemento[1], 
                                                                    width = self.dimensioniElemento[0], 
                                                                    height = self.dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = idDispositivo))
    
    def RimuoviDispositivo(self, idPosizionale : int):
        self._elementiIntabellabili.pop(idPosizionale)
        self._numOf_elementiIntabellabili -= 1

    def ClearFrameDispositivi(self): # NON FUNZIONANTE SE NON VUOTA
        self._elementiIntabellabili = []
        self._numOf_elementiIntabellabili = 0

    
    
    # AGGIORNAMENTO FRAME
    def CaricaTabella(self):
        self.RefreshFrameDispositivi(aggiornaAttributi=True)
        self.Show()

    #Aggiorna il numero di frame presenti sulla dashboard
    def RefreshFrameDispositivi(self, aggiornaAttributi : bool = False): 
        numDispositiviRichiesto = len(GestoreDispositivi.IGetListaDispositivi())
        #Aggiunge e rimuove gli elementi in base a quanti ne mancano e l'iteratore
        self.RefreshNumeroFrame(numDispositiviRichiesto, lambda i : FrameDispositivoIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self.dimensioniElemento[1], 
                                                                    width = self.dimensioniElemento[0], 
                                                                    height = self.dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = i),
                                                                    aggiornaAttributi = False)
        if aggiornaAttributi:
            self.RefreshAttributiElementi()



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