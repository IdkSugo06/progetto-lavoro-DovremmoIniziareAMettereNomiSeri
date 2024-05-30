from GestioneFiltri.Filtri.FiltroGenerico import *

#Filtro figlio del filtro generico, singleton
class FiltroStatusOffOn(FiltroGenerico):

    # INTERFACCE
    @staticmethod
    def _Notifica_CambioStatoDispositivo(idDispositivo : int, nuovoStato : bool):
        FiltroStatusOffOn.GetFiltro()._CambioStatoDispositivo(idDispositivo, nuovoStato)
    @staticmethod
    def _Notifica_AggiuntoDispositivo(idDispositivo : int):
        FiltroStatusOffOn.GetFiltro()._AggiungiDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_RimossoDispositivo(idDispositivo : int):
        FiltroStatusOffOn.GetFiltro()._RimuoviDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_ModificatoDispositivo(idDispositivo : int):
        MyEventHandler.Throw(MyFilterElementChanged, {"tipoFiltro" : MyFilterElementChanged, "idElemento" : FiltroStatusOffOn.GetFiltro().GetIdElemento(idDispositivo), "stato" : None})
    @staticmethod
    def _Notifica_OrdinaLista():
        FiltroStatusOffOn.GetFiltro()._OrdinaLista()
    @staticmethod
    def _Notifica_RebuildLista():
        FiltroStatusOffOn.GetFiltro()._RebuildLista()

    # ISTANZA STATICA
    _filtroStatus = None
    
    # COSTRUTTORI
    @staticmethod
    def Init():
        if FiltroStatusOffOn._filtroStatus == None:
            FiltroStatusOffOn._filtroStatus = FiltroStatusOffOn()
    @staticmethod
    def GetFiltro():
        if FiltroStatusOffOn._filtroStatus == None:
            FiltroStatusOffOn._filtroStatus = FiltroStatusOffOn()
        return FiltroStatusOffOn._filtroStatus
    
    def __init__(self):
        super().__init__("statusOffOn")
        self._numOf_dispositiviOffline = 0
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : FiltroStatusOffOn._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : FiltroStatusOffOn._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : FiltroStatusOffOn._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : FiltroStatusOffOn._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = FiltroStatusOffOn._Notifica_OrdinaLista)
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = FiltroStatusOffOn._Notifica_RebuildLista)


    # ORDINAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato = True):
        #Trovo l'id posizionale del dispositivo da swappare
        if nuovoStato == True:
            self._numOf_dispositiviOffline -= 1
            idDispositivo2 = self._listaOrdinata[self._numOf_dispositiviOffline]
        elif nuovoStato == False:
            idDispositivo2 = self._listaOrdinata[self._numOf_dispositiviOffline]
            self._numOf_dispositiviOffline += 1
        

        #Mi salvo gli id dei dispositivi sulla lista ordinata attuale
        idSuListaOrdinataDisp1 = self._idDispToIdListaOrdinata[idDispositivo1] 
        idSuListaOrdinataDisp2 = self._idDispToIdListaOrdinata[idDispositivo2] 
        #Se i dispositivi sono gli stessi cambio lo stato e basta
        if idSuListaOrdinataDisp1 == idSuListaOrdinataDisp2:
            MyEventHandler.Throw(MyFilterElementChanged, {"tipoFiltro" : type(self), "idElemento" : idSuListaOrdinataDisp1, "stato" : nuovoStato})
            return
        
        #Inverto gli id nella lista di associazione id
        self._idDispToIdListaOrdinata[idDispositivo1] = idSuListaOrdinataDisp2
        self._idDispToIdListaOrdinata[idDispositivo2] = idSuListaOrdinataDisp1
        #Inverto gli id nella lista ordinata
        self._listaOrdinata[idSuListaOrdinataDisp1] = idDispositivo2 
        self._listaOrdinata[idSuListaOrdinataDisp2] = idDispositivo1

        #Notifico il cambio
        MyEventHandler.Throw(MyFilterElementChanged, {"tipoFiltro" : type(self), "idElemento" : self._idDispToIdListaOrdinata[idDispositivo1], "stato" : nuovoStato})
        MyEventHandler.Throw(MyFilterElementChanged, {"tipoFiltro" : type(self), "idElemento" : self._idDispToIdListaOrdinata[idDispositivo2], "stato" : not nuovoStato})
    
    def _AggiungiDispositivo(self, idDispositivo : int):
        #L'elmento inizializzato sarà offline, lo aggiungo come primo elemento alla lista
        self._numOf_dispositiviOffline += 1
        self._numOf_elementi += 1
        self._listaOrdinata = [idDispositivo] + self._listaOrdinata
        self._idDispToIdListaOrdinata.append(0) #0 perchè primo elemento
        #Aumento tutti di un indice avanti
        for i in range(1, len(self._idDispToIdListaOrdinata)):
            self._idDispToIdListaOrdinata[i] += 1

        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})

    def _RimuoviDispositivo(self, idDispositivo : int):
        #Riassegno le liste
        idDispositivoSuListaOrdinata = self._idDispToIdListaOrdinata[idDispositivo]

        #Reimposto gli id posizionali
        for i_dispositivo in range(idDispositivo, self._numOf_elementi):
            i_elemento = self._idDispToIdListaOrdinata[i_dispositivo]
            self._listaOrdinata[i_elemento] -= 1
        for i in range(len(self._idDispToIdListaOrdinata)):
            if self._idDispToIdListaOrdinata[i] > idDispositivoSuListaOrdinata:
                self._idDispToIdListaOrdinata[i] -= 1
        #Ricostruisco la lista ordinata  
        self._idDispToIdListaOrdinata = self._idDispToIdListaOrdinata[:idDispositivo] + self._idDispToIdListaOrdinata[idDispositivo+1:] 
        self._listaOrdinata = self._listaOrdinata[:idDispositivoSuListaOrdinata] + self._listaOrdinata[idDispositivoSuListaOrdinata+1:]

        #Modifico i contatori
        if idDispositivoSuListaOrdinata <= self._numOf_dispositiviOffline: #Se era offline
            self._numOf_dispositiviOffline -= 1
        self._numOf_elementi -= 1
        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})

    def _OrdinaLista(self):
        #Resetto i contatori
        self._numOf_dispositiviOffline = 0
        #Ciclo i dispositivi
        i_dispositivo = 0
        i_dispositivoOnline = self._numOf_elementi - 1
        for dispositivo in GestoreDispositivi.IGetListaDispositivi():
            #Li ordino nella lista
            statusDispCorrente = dispositivo.GetStatusConnessione()
            #Se connesso lo inserisco alla fine della lista
            if statusDispCorrente == True:
                self._listaOrdinata[i_dispositivoOnline] = i_dispositivo
                self._idDispToIdListaOrdinata[i_dispositivo] = i_dispositivoOnline
                i_dispositivoOnline -= 1
            elif statusDispCorrente == False:
                self._listaOrdinata[self._numOf_dispositiviOffline] = i_dispositivo
                self._idDispToIdListaOrdinata[i_dispositivo] = self._numOf_dispositiviOffline
                self._numOf_dispositiviOffline += 1
            i_dispositivo += 1
        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})
    
    def _RebuildLista(self):
        self._numOf_elementi = GestoreDispositivi.IGetNumDispositivi()
        self._listaOrdinata = [None] * self._numOf_elementi
        self._idDispToIdListaOrdinata = [None] * self._numOf_elementi
        self._OrdinaLista()


FiltroStatusOffOn.Init()