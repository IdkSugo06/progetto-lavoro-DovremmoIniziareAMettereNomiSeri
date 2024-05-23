from GestionePagine.Widgets.TabelleFolder.TabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameDashboardIntabellabile import *

class TabellaDashboard(TabellaScorribile):


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
        self.__numOf_dispositiviOffline = 0
        GestoreDispositivi.ISetFunzioneNotificaCambioStatus(self.__Notifica_CambioStatoDispositivo)



    # METODI MODIFICA LISTA
    def AggiungiDispositivo(self, idDispositivo : int):
        self.AggiungiElemento(FrameDashboardIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self.dimensioniElemento[1], 
                                                                    width = self.dimensioniElemento[0], 
                                                                    height = self.dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = idDispositivo))
    def RimuoviElemento(self, idPoszionaleElemento : int):
        self._numOf_elementiIntabellabili -= 1
        self._elementiIntabellabili.pop(idPoszionaleElemento)

    def ClearFrameDispositivi(self):
        self._elementiIntabellabili = []
        self._numOf_elementiIntabellabili = 0
    


    # AGGIORNA FRAMES E MOSTRA
    def CaricaTabella(self):
        self.RefreshFrameDispositivi(aggiornaAttributi = True)
        l = [(e.GetDispositivoAssociato().GetNome(), e.GetDispositivoAssociato().GetStatusConnessione()) for e in self._elementiIntabellabili]
        print(l)
        self.Show()
        s = [(e.GetDispositivoAssociato().GetNome(), e.GetDispositivoAssociato().GetStatusConnessione()) for e in self._elementiIntabellabili]
        print(s)


    #Aggiorna i frame e gli attributi di essi
    def RefreshFrameDispositivi(self, aggiornaAttributi : bool = False): 

        #Aggiorno il numero di frame
        numDispositiviRichiesto = len(GestoreDispositivi.IGetListaDispositivi())
        self.RefreshNumeroFrame(numDispositiviRichiesto, lambda i : FrameDashboardIntabellabile(master = self.GetFrameTabella(),
                                                                    x = 0, 
                                                                    y = self._numOf_elementiIntabellabili * self.dimensioniElemento[1], 
                                                                    width = self.dimensioniElemento[0], 
                                                                    height = self.dimensioniElemento[1],
                                                                    isShown = True,
                                                                    idDispositivo = i),
                                                                    aggiornaAttributi = False) #Li aggiornerò dopo aver riassegnato gli id

        self.ResetIds()

    def ResetIds(self):
        #Per ogni dispositivo, riassegna l'id del frame all'idPosizionale per evitare crash se sono stati rimossi dispositivi
        self.__numOf_dispositiviOffline = 0
        numOf_dispositiviTotali = GestoreDispositivi.IGetNumDispositivi()
        i_dispositiviOnline = numOf_dispositiviTotali - 1
        lista = [None] * numOf_dispositiviTotali
        i_dispositivo = 0
        for dispositivo in GestoreDispositivi.IGetListaDispositivi():
            #Ogni dispositivo online sarà posizionato in fondo alla lista, quelli offline sopra
            statusConnessione = dispositivo.GetStatusConnessione()[1]
            #Se lo stato connessioni è true, dal basso li inserisco
            if statusConnessione == True:
                dispositivo.SetIdPosElementoDashboardAssociato(i_dispositiviOnline)
                self._elementiIntabellabili[i_dispositiviOnline].AssociaDispositivo(i_dispositivo, aggiornamentoForzato = True)
                lista[i_dispositiviOnline] = True
                print(i_dispositiviOnline,True)
                i_dispositiviOnline -= 1
            #Altrimenti li inserisco dall'alto
            elif statusConnessione == False:
                dispositivo.SetIdPosElementoDashboardAssociato(self.__numOf_dispositiviOffline)
                self._elementiIntabellabili[self.__numOf_dispositiviOffline].AssociaDispositivo(i_dispositivo, aggiornamentoForzato = True)
                lista[self.__numOf_dispositiviOffline] = False
                print(self.__numOf_dispositiviOffline,False)
                self.__numOf_dispositiviOffline += 1

            #Aggiorno gli id dei frame
            i_dispositivo += 1  
        print(lista)
        print("Lunghezza: ", len(self._elementiIntabellabili))


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori
        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
        coloreBordoElementi = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.CambioColore(coloreSfondo, coloreElementi, coloreBordoElementi, cambioColoreElementi = False)
        
        #Per ogni elemento aggiorno i colori
        for elemento in self._elementiIntabellabili:
            elemento.AggiornaColoriTema()



    # PHYSICS UPDATE
    def Update(self, deltaTime : float = 0): #Disabled
        return
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.Update(deltaTime)



    # FUNZIONI NOTIFICA
    def __Notifica_CambioStatoDispositivo(self, dispositivo : Dispositivo, nuovoStato : bool): #Viene chiamata quando c'è un cambio stato nel dispositivo passato come parametro
        
        # Controllo il tipo di ordinamento : ON-OFF
        if Impostazioni.sistema.tipoOrdinamentoDashboard == "off_on":

            #Blocco il semaforo e getto se lo stato del dispositivo è stato cambiato
            #Se era offline e adesso è online
            if nuovoStato == True:                 
                #Decremento il numero di dispositivi online e swappo l'ultimo offline con il quello appena online
                self.__semaforoPosizionamentoDispositivi.acquire()
                self.__numOf_dispositiviOffline -= 1
                self.__SwapDispositivi(dispositivo, self._elementiIntabellabili[self.__numOf_dispositiviOffline].GetDispositivoAssociato())
                self.__semaforoPosizionamentoDispositivi.release()

            #Se era online e adesso è offline
            else:                 
                #Decremento il numero di dispositivi online e swappo il primo online con quello appena offline
                self.__semaforoPosizionamentoDispositivi.acquire()
                self.__SwapDispositivi(dispositivo, self._elementiIntabellabili[self.__numOf_dispositiviOffline].GetDispositivoAssociato())
                self.__numOf_dispositiviOffline += 1
                self.__semaforoPosizionamentoDispositivi.release()

        # Controllo il tipo di ordinamento : STABILITA CONNESSIONE
        elif Impostazioni.sistema.tipoOrdinamentoDashboard != "off_on":
            pass
    
    def __SwapDispositivi(self, dispositivo1 : Dispositivo, dispositivo2 : Dispositivo):

        #Salvo i frame dei dispositivi
        idFrameD1 = dispositivo1.GetIdPosElementoDashboardAssociato()
        idFrameD2 = dispositivo2.GetIdPosElementoDashboardAssociato()

        #Swappo i frame dei dispositivi
        dispositivo1.SetIdPosElementoDashboardAssociato(idFrameD2)
        dispositivo2.SetIdPosElementoDashboardAssociato(idFrameD1)

        #Associo i nuovi dispositivi 
        self._elementiIntabellabili[idFrameD2].AssociaDispositivo(dispositivo1.GetId())
        self._elementiIntabellabili[idFrameD1].AssociaDispositivo(dispositivo2.GetId())
