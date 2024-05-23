from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *


#Classe 
class TabellaScorribile(tk.Frame): #Occuperà tutto lo spazio disponibile

    __scrollWheelNotify = lambda x : x

    def __init__(self, 
                 master : tk.Frame,
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
        self._pointerCanvas = 0
        self._coloreSfondo = coloreSfondo
        self._coloreElementi = coloreElementi
        self._coloreBordoElementi = coloreBordoElementi

        #Creo la lista per contenere gli elementi intabellabili
        self._numOf_elementiIntabellabili = 0
        self._elementiIntabellabili = [] 

        #Salvo le dimensioni
        self.__dimensioniTabella = [tableWidth, tableHeight]
        self.dimensioniElemento = [elementWidth, elementHeight]

        #Creo il canvas scorrevole
        self.__cCanvasScorrevole = tk.Canvas(master = self, 
                                             scrollregion = (0, 0, self.__dimensioniTabella[0], 0),
                                             bg = self._coloreSfondo, highlightbackground= Impostazioni.Tema.IGetColoriSfondo("secondario")[2])
        self.__cCanvasScorrevole.configure(yscrollincrement='1')
        self.__cCanvasScorrevole.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasScorrevole.grid_propagate(False)
        self.__cCanvasScorrevole.pack_propagate(False)

        #Creo il frame interno al canvas
        self.__fFrameInternoCanvasScorrevole = tk.Frame(master = self, bg = self._coloreSfondo)
        self.__fFrameInternoCanvasScorrevole.place(x = 0, y = 0, width = self.__dimensioniTabella[0], height = 0, anchor= "nw")
        self.__fFrameInternoCanvasScorrevole.columnconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.rowconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.grid_propagate(False)
        self.__fFrameInternoCanvasScorrevole.pack_propagate(False)

        # genero il frame interno al canvas
        self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniTabella[0],
                                              height = 0)
        
        # EVENT BIND
        self.__cCanvasScorrevole.bind("<MouseWheel>", lambda event : self.__Event_Scrolled(event))



    # GETTER E SETTER
    def GetFramePrincipale(self):
        return self
    def GetFrameTabella(self):
        return self.__fFrameInternoCanvasScorrevole
        
   

    # METODI TABELLA
    # MODIFICA ELEMENTI
    def AggiungiElemento(self, elementoIntabellabile : ElementoIntabellabile): #Aggiungo un elemento
        elementoIntabellabile.myBind("<MouseWheel>", lambda event : self.__Event_Scrolled(event))
        self._numOf_elementiIntabellabili += 1
        self._elementiIntabellabili.append(elementoIntabellabile)

    def RimuoviElemento(self, idElemento : int): #Rimuovo un elemento
        self._numOf_elementiIntabellabili -= 1
        return self._elementiIntabellabili.pop(idElemento)
    
    def Clear(self):
        self._elementiIntabellabili = []
        self._numOf_elementiIntabellabili = 0

    

    # AGGIORNA FRAME E MOSTRA
    #Aggiunge e rimuove gli elementiTabellabili in base a quanti ne mancano e l'iteratore
    def RefreshNumeroFrame(self, numElementiRichiesti : int, funzioneItoCostruttoreEl = lambda i : ElementoIntabellabile(), aggiornaAttributi : bool = False): 
        numElementiAttuale = self._numOf_elementiIntabellabili 
        
        #Se si deve aggiungere o rimuovere dispositivi, poi aggiorno
        if numElementiRichiesti > numElementiAttuale:
            for i in range(numElementiAttuale, numElementiRichiesti):
                self.AggiungiElemento(funzioneItoCostruttoreEl(i))
        elif numElementiRichiesti < numElementiAttuale:
            for i in range(numElementiAttuale-1, numElementiRichiesti-1, -1):
                self.RimuoviElemento(i)
        
        #Se richiesto aggiorno gli attributi
        if aggiornaAttributi == True: 
            self.RefreshAttributiElementi()  

    #Per ogni elemento, aggiorno gli attributi
    def RefreshAttributiElementi(self):  #Aggiorna posizione e dimensione di ogni elemento
        #Border check, most often this function is called when an element is added or removed
        altezzaElementi = self.dimensioniElemento[1] * len(self._elementiIntabellabili)
        if self._pointerCanvas < 1:
            self._pointerCanvas = 1
        elif self._pointerCanvas + self.__dimensioniTabella[1] > altezzaElementi:
            self._pointerCanvas = (altezzaElementi - self.__dimensioniTabella[1]) - 1

        #Visualizzati da idPrimo e idUltimo compreso
        idPrimoDentro = floor(self._pointerCanvas / self.dimensioniElemento[1])
        idUltimoDentro = floor((self._pointerCanvas + self.__dimensioniTabella[1]) / self.dimensioniElemento[1])

        #Refresh attributes
        i = 0
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.SetPos(0, i * self.dimensioniElemento[1])
            elementoIntabellabile.SetDim(self.dimensioniElemento[0], self.dimensioniElemento[1])
            elementoIntabellabile.SetColore(self._coloreElementi, self._coloreBordoElementi)
            elementoIntabellabile.RefreshAttributiElemento()

            #Nascondo tutti tranne quelli che sono nella parte visualizzata
            if i < idPrimoDentro or i > idUltimoDentro:
                elementoIntabellabile.Hide()
            else:
                elementoIntabellabile.Show()
            i += 1


    def Show(self): #Cancella tutto e ricrea la finestra
        self.__fFrameInternoCanvasScorrevole.place(x = 0, 
                                                   y = 0, 
                                                   width = self.__dimensioniTabella[0], 
                                                   height = self._numOf_elementiIntabellabili * self.dimensioniElemento[1],
                                                   anchor= "nw")

        self.__cCanvasScorrevole.delete("all")
        altezzaElementi = self._numOf_elementiIntabellabili * self.dimensioniElemento[1]
        altezzaCanvas = (altezzaElementi-4) if altezzaElementi > self.__dimensioniTabella[1] else (self.__dimensioniTabella[1]-4)
        self.__cCanvasScorrevole.configure(scrollregion = (0, 0, self.__dimensioniTabella[0], altezzaCanvas))
        self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniTabella[0],
                                              height = altezzaElementi)



    # METODI PERSONALIZZAZIONE
    def CambioColore(self, coloreSfondo : str, coloreElementi : str, coloreBordoElementi : str, cambioColoreElementi : bool = False):
        #Imposto i colori
        self._coloreSfondo = coloreSfondo
        self._coloreElementi = coloreElementi
        self._coloreBordoElementi = coloreBordoElementi

        #Aggiorno i colori
        self.__cCanvasScorrevole.configure(background=coloreSfondo)
        self.__fFrameInternoCanvasScorrevole.configure(background=coloreSfondo)

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
        
        self.place(x = xPos, y = yPos, width = tableWidth, height = tableHeight)
        self.__dimensioniTabella = [tableWidth, tableHeight]
        self.dimensioniElemento = [elementWidth, elementHeight]
        self._pointerCanvas = 0
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi)
        self.RefreshAttributiElementi()
        self.Show()
        


    # UPDATE
    def Update(self, deltaTime : float = 0): #Lancia l'update di ogni elemento (per supporto elementi dinamici)
        return
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.Update(deltaTime)



    # EVENT METHODS
    def __Event_Scrolled(self, eventTk = None):
        #Controllo che si debba scrollare e salvo le variabilii che serviranno in seguito
        altezzaElementoSingolo = self.dimensioniElemento[1]
        altezzaElementi = len(self._elementiIntabellabili) * altezzaElementoSingolo
        altezzaSchermo = self.__dimensioniTabella[1]
        if altezzaElementi < altezzaSchermo:
            return
        
        #Calcolo il coefficente di scroll e scrollo
        kScroll = int(-eventTk.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella)
        self.__cCanvasScorrevole.yview_scroll(kScroll, "units")

        #Controllo chi è dentro e chi fuori dalla tabella prima
        idPrimoDentroPrima = floor(self._pointerCanvas / altezzaElementoSingolo)
        idUltimoDentroPrima = floor((self._pointerCanvas + altezzaSchermo) / altezzaElementoSingolo)

        #Aumento il ptr e borders check
        self._pointerCanvas += kScroll
        if self._pointerCanvas < 1:
            self._pointerCanvas = 1
        elif self._pointerCanvas + altezzaSchermo > altezzaElementi:
            self._pointerCanvas = (altezzaElementi - altezzaSchermo) - 1

        #Controllo chi è dentro e chi fuori dalla tabella dopo
        idPrimoDentroOra = floor(self._pointerCanvas / altezzaElementoSingolo) 
        idUltimoDentroOra = floor((self._pointerCanvas + altezzaSchermo) / altezzaElementoSingolo) 

        #Nascondo e mostro quelli entrati/usciti
        if kScroll < 0:
            for i in range(idPrimoDentroPrima - 1, idPrimoDentroOra - 1, -1): #primo escluso, ultimo incluso
                self._elementiIntabellabili[i].Show()
            for i in range(idUltimoDentroPrima, idUltimoDentroOra, -1):
                self._elementiIntabellabili[i].Hide()
        else:
            for i in range(idPrimoDentroPrima, idPrimoDentroOra):
                self._elementiIntabellabili[i].Hide()
            for i in range(idUltimoDentroPrima + 1, idUltimoDentroOra + 1):
                self._elementiIntabellabili[i].Show()

