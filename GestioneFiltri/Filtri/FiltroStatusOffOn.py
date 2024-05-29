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
        return #La modifica non cambia lo stato


    _filtroStatus = None
    #Costruttore
    @staticmethod
    def GetFiltro():
        if FiltroStatusOffOn._filtroStatus == None:
            FiltroStatusOffOn._filtroStatus = FiltroStatusOffOn()
        return FiltroStatusOffOn._filtroStatus
    
    def _init_(self):
        super().__init__(self)
        self._numOf_dispositiviOffline = 0
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda args : FiltroStatusOffOn._Notifica_AggiuntoDispositivo(args))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda args : FiltroStatusOffOn._Notifica_RimossoDispositivo(args))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda args : FiltroStatusOffOn._Notifica_ModificatoDispositivo(args))
        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda args : FiltroStatusOffOn._Notifica_CambioStatoDispositivo(args))

    
    # ORDINAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato = True):
        #Trovo l'id posizionale del dispositivo da swappare
        if nuovoStato == True:
            self._numOf_dispositiviOffline -= 1
            idDispositivo2 = self._listaOrdinata[self._numOf_dispositiviOffline]
        elif nuovoStato == False:
            idDispositivo2 = self._listaOrdinata[self._numOf_dispositiviOffline]
            self._numOf_dispositiviOffline += 1
        
        #Se i dispositivi sono gli stessi cambio lo stato e basta
        if idDispositivo1 == idDispositivo2:
            MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : FiltroStatusOffOn, "codice" : "cambioStato", "args" : [idDispositivo1, nuovoStato]})
            return

        #Mi salvo gli id dei dispositivi sulla lista ordinata attuale
        idSuListaOrdinataDisp1 = self._idDispToIdListaOrdinata[idDispositivo1] 
        idSuListaOrdinataDisp2 = self._idDispToIdListaOrdinata[idDispositivo2] 
        
        #Inverto gli id nella lista di associazione id
        self._idDispToIdListaOrdinata[idDispositivo1] = idSuListaOrdinataDisp2
        self._idDispToIdListaOrdinata[idDispositivo2] = idSuListaOrdinataDisp1
        #Inverto gli id nella lista ordinata
        self._listaOrdinata[idSuListaOrdinataDisp1] = idDispositivo2 
        self._listaOrdinata[idSuListaOrdinataDisp2] = idDispositivo1

        #Notifico il cambio
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : FiltroStatusOffOn, "codice" : "cambioStato", "args" : [idDispositivo1, nuovoStato]})
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : FiltroStatusOffOn, "codice" : "cambioStato", "args" : [idDispositivo2, not nuovoStato]})
    
    def _AggiungiDispositivo(self, idDispositivo : int):
        #L'elmento inizializzato sarà offline, lo aggiungo come primo elemento alla lista
        self._numOf_dispositiviOffline += 1
        self._numOf_elementi += 1
        self._listaOrdinata = [idDispositivo] + self._listaOrdinata
        self._idDispToIdListaOrdinata.append(0) #0 perchè primo elemento
        #Aumento tutti di un indice avanti
        for i in range(1, len(self._idDispToIdListaOrdinata)):
            self._idDispToIdListaOrdinata[i] += 1

    def _RimuoviDispositivo(self, idDispositivo : int):
        #Riassegno le liste
        idDispositivoSuListaOrdinata = self._idDispToIdListaOrdinata[idDispositivo]
        self._listaOrdinata = self._listaOrdinata[:idDispositivoSuListaOrdinata] + self._listaOrdinata[idDispositivoSuListaOrdinata+1:]
        self._idDispToIdListaOrdinata = self._idDispToIdListaOrdinata[:idDispositivo] + self._idDispToIdListaOrdinata[idDispositivo+1:] 

        #Modifico i contatori
        if idDispositivoSuListaOrdinata <= self._numOf_dispositiviOffline: #Se era offline
            self._numOf_dispositiviOffline -= 1
        self._numOf_elementi -= 1

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
    
    def _RicreaLista(self):
        self._listaOrdinata = [None] * GestoreDispositivi.IGetNumDispositivi()
        self._idDispToIdListaOrdinata = [None] * GestoreDispositivi.IGetNumDispositivi()
        self._OrdinaLista()