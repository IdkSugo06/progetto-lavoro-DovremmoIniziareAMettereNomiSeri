from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *


#Questa classe simulerà un canvas scorribile anche se conterra solamente il numero minimo necessario di dispositivi
class FakeTabellaScorribile(tk.Frame):

    # COSTRUTTORE
    def __init__(self, 
             master : tk.Frame,
             funzionePopolamentoListaPerIndice : lambda i : None, #Questa funzione deve poter convertire un indice in un argomento passabile in "elementoIntabellabile.AggiornaAttributiElemento"
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
        
        #Creo il frame
        super().__init__(master, width= tableWidth, height= tableHeight, bg = coloreSfondo)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.place(x = xPos, y = yPos, width = tableWidth, height = tableHeight)
        self.grid_propagate(False)

        #Salvo i colori
        self._coloreSfondo = coloreSfondo
        self._coloreElementi = coloreElementi
        self._coloreBordoElementi = coloreBordoElementi

        #Salvo le dimensioni
        self._dimensioniTabella = [tableWidth, tableHeight]
        self._dimensioniElemento = [elementWidth, elementHeight]

        #Creo la lista per contenere gli elementi intabellabili
        self._numOf_elementiIntabellabili = 0
        self._numOf_elementiMassimo = (self._dimensioniTabella[1] // self._dimensioniElemento[1]) + 1
        self._numOf_elementiFinti = 0
        self._elementiIntabellabili = []

        #Attributi tabella
        self._funzionePopolamentoLista = funzionePopolamentoListaPerIndice
        self._puntatoreInizioTabella = 0
        self._indiciElementiInterni = [0,0]
        self._altezzaElementi = 0
        self._scrollablePixels = self._altezzaElementi - self._dimensioniTabella[1]

        #Bind
        self.bind("<MouseWheel>", lambda event : self.__Event_MouswheelScroll(event))



    # GETTER E SETTER    
    def AggiungiElemento(self, elemento : ElementoIntabellabile):
        elemento.myBind("<MouseWheel>", lambda event : self.__Event_MouswheelScroll(event))
        self._elementiIntabellabili.append(elemento)
        
    def RimuoviElemento(self, idElemento : int):
        self._elementiIntabellabili.pop(idElemento)
        self._numOf_elementiFinti -= 1
        self._indiciElementiInterni[1] -= 1
        self._altezzaElementi = self._numOf_elementiFinti * self._dimensioniElemento[1]
        self._scrollablePixels = self._altezzaElementi - self._dimensioniTabella[1]


    # SHOW E REFRESH ATTRIBUTI
    def RefreshElemento(self, idElemento : int):
        if idElemento < self._indiciElementiInterni[0] or idElemento > self._indiciElementiInterni[1]:
            return
        
        self._elementiIntabellabili[idElemento - self._indiciElementiInterni[0]].AggiornaAttributiElemento(self._funzionePopolamentoLista(idElemento))

    def RefreshNumeroFrame(self, numElementiRichiesti : int, funzioneCostruttoreDaId : any = lambda x : ElementoIntabellabile(master=tk.Frame()), aggiornaAttributi : bool = True):
        #Aggiorno i valori di scroll
        self._numOf_elementiFinti = numElementiRichiesti
        numElementiRichiesti = min(numElementiRichiesti, self._numOf_elementiMassimo)
        numElementiAttuali = self._numOf_elementiIntabellabili 
        #Aggiorno gli attributi per lo scroll
        self._numOf_elementiIntabellabili = numElementiRichiesti 
        self._altezzaElementi = self._numOf_elementiFinti * self._dimensioniElemento[1]
        self._scrollablePixels = self._altezzaElementi - self._dimensioniTabella[1]

        #Se si deve aggiungere o rimuovere dispositivi, poi aggiorno
        if numElementiRichiesti > numElementiAttuali:
            for i in range(numElementiAttuali, numElementiRichiesti):
                self.AggiungiElemento(funzioneCostruttoreDaId(i))
        elif numElementiRichiesti < numElementiAttuali:
            for i in range(numElementiAttuali-1, numElementiRichiesti-1, -1):
                self.RimuoviElemento(i)
        
        self.__SetPointerPosition(self._puntatoreInizioTabella, show = False) #Esegue check dei bordi ecc.. 
        self.Show()

    def Show(self):
        dimEly = self._dimensioniElemento[1] #local reassignment for faster access
        y_elementoIntabellabile = -((self._puntatoreInizioTabella - self._dimensioniElemento[1]) % self._dimensioniElemento[1]) #Calcolo l'offset dall'inizio della tabella
        i = self._indiciElementiInterni[0]
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.SetPos(0, y_elementoIntabellabile)
            elementoIntabellabile.Hide()
            elementoIntabellabile.Show()
            y_elementoIntabellabile += dimEly
            i += 1

    # METODI SCROLL
    def __SetPointerPosition(self, pixelPosition : int, show : bool = True):
        self._puntatoreInizioTabella = pixelPosition

        if self._scrollablePixels < 0: return
        #Borers check
        altezzaElementi = self._numOf_elementiFinti * self._dimensioniElemento[1]
        if self._puntatoreInizioTabella < 0:
            self._puntatoreInizioTabella = 0
        elif (self._puntatoreInizioTabella + self._dimensioniTabella[1])> altezzaElementi - 2:
            self._puntatoreInizioTabella = (altezzaElementi - self._dimensioniTabella[1]) - 2

        #Controllo chi è dentro e chi fuori dalla tabella dopo
        idPrimoDentroOra = floor((self._puntatoreInizioTabella + 2) / self._dimensioniElemento[1]) 
        idUltimoDentroOra = floor(((self._puntatoreInizioTabella + self._dimensioniTabella[1] - 2) / self._dimensioniElemento[1])) 
        self._indiciElementiInterni[0] = idPrimoDentroOra
        self._indiciElementiInterni[1] = idUltimoDentroOra
        
        if show == True: 
            self.Show()

    def __Scroll(self, pixelToScroll : int): #Soggetto a sensibilita scorrimento rotella
        if self._scrollablePixels < 0:
            return
        
        #Controllo che si debba scrollare e salvo le variabilii che serviranno in seguito
        altezzaElementoSingolo = self._dimensioniElemento[1]
        altezzaSchermo = self._dimensioniTabella[1]

        #Aumento il ptr e borders check
        kScroll = int(pixelToScroll * Impostazioni.sistema.sensibilita_scorrimento_rotella)
        fine = False
        self._puntatoreInizioTabella += kScroll
        if self._puntatoreInizioTabella < 1:
            self._puntatoreInizioTabella = 1
        elif (self._puntatoreInizioTabella + altezzaSchermo) > self._altezzaElementi - 2:
            fine = True
            self._puntatoreInizioTabella = (self._altezzaElementi - altezzaSchermo) - 2

        #Controllo chi è dentro e chi fuori dalla tabella dopo
        idPrimoDentroOra = floor((self._puntatoreInizioTabella + 2) / altezzaElementoSingolo) 
        idUltimoDentroOra = ceil((((self._puntatoreInizioTabella + altezzaSchermo)) / altezzaElementoSingolo)) - 1
        
        #Nascondo e mostro quelli entrati/usciti
        if idPrimoDentroOra > self._indiciElementiInterni[0]:
            #Scroll verso il basso
            i_inizioLista = idPrimoDentroOra - self._indiciElementiInterni[0]
            i_fineLista = len(self._elementiIntabellabili) - 1
            if fine: i_fineLista -= 1
            self._elementiIntabellabili = self._elementiIntabellabili[i_inizioLista:] + self._elementiIntabellabili[:i_inizioLista]
            for i in range(i_fineLista - i_inizioLista, i_fineLista + 1):
                self._elementiIntabellabili[i].AggiornaAttributiElemento(self._funzionePopolamentoLista(idPrimoDentroOra + i))
                self._elementiIntabellabili[i].Hide()
                self._elementiIntabellabili[i].Show()
        elif idPrimoDentroOra < self._indiciElementiInterni[0]:
            #Scroll verso l'alto
            i_inizioLista = idPrimoDentroOra - self._indiciElementiInterni[0] #Negative
            self._elementiIntabellabili = self._elementiIntabellabili[i_inizioLista:] + self._elementiIntabellabili[:i_inizioLista]
            for i in range(0, (-i_inizioLista)):
                self._elementiIntabellabili[i].AggiornaAttributiElemento(self._funzionePopolamentoLista(idPrimoDentroOra + i))
                self._elementiIntabellabili[i].Hide()
                self._elementiIntabellabili[i].Show()
        
        #Aggiorno gli indici
        self._indiciElementiInterni[0] = idPrimoDentroOra
        self._indiciElementiInterni[1] = idUltimoDentroOra

        dimEly = self._dimensioniElemento[1] #local reassignment for faster access
        y_elementoIntabellabile = -((self._puntatoreInizioTabella - self._dimensioniElemento[1]) % self._dimensioniElemento[1]) #Calcolo l'offset dall'inizio della tabella
        i = self._indiciElementiInterni[0]
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.SetPos(0, y_elementoIntabellabile)
            elementoIntabellabile.Show()
            y_elementoIntabellabile += dimEly
            i += 1
    
    def __Event_MouswheelScroll(self, eventTk = None):
        self.__Scroll(pixelToScroll = -eventTk.delta)

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
        self.RefreshNumeroFrame(self._numOf_elementiFinti, aggiornaAttributi = False)
        self.__SetPointerPosition(self._puntatoreInizioTabella, show = False) #Esegue check dei bordi ecc..
        self.Show()