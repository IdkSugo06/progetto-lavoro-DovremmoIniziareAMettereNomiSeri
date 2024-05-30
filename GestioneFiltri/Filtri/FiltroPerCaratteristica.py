from GestioneFiltri.Filtri.FiltroGenerico import *


#Filtro figlio del filtro generico, classe astratta
class FiltroPerCaratteristica(FiltroGenerico):

    # INTERFACCE
    @staticmethod
    def _Notifica_CambioStatoDispositivo(idDispositivo : int, nuovoStato : bool):
        FiltroPerCaratteristica.GetFiltro()._CambioStatoDispositivo(idDispositivo, nuovoStato)
    @staticmethod
    def _Notifica_AggiuntoDispositivo(idDispositivo : int):
        FiltroPerCaratteristica.GetFiltro()._AggiungiDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_RimossoDispositivo(idDispositivo : int):
        FiltroPerCaratteristica.GetFiltro()._RimuoviDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_ModificatoDispositivo(idDispositivo : int):
        return
    @staticmethod
    def _Notifica_OrdinaLista():
        FiltroPerCaratteristica.GetFiltro()._OrdinaLista()
    @staticmethod
    def _Notifica_RebuildLista():
        FiltroPerCaratteristica.GetFiltro()._RebuildLista()

    # ISTANZA STATICA
    _filtroStatus = None
    
    # COSTRUTTORI
    @staticmethod
    def Init():
        if FiltroPerCaratteristica._filtroStatus == None:
            FiltroPerCaratteristica._filtroStatus = FiltroPerCaratteristica()
    @staticmethod
    def GetFiltro():
        if FiltroPerCaratteristica._filtroStatus == None:
            FiltroPerCaratteristica._filtroStatus = FiltroPerCaratteristica()
        return FiltroPerCaratteristica._filtroStatus
    
    def __init__(self, funzioneDiOrdinamento = lambda idDispositivo1,idDispositivo2 : """tuple((-1,0,1))""", funzioneScarto = lambda idDispositivo : """tuple((False, True))"""):
        super().__init__("statusOffOn")
        self._numOf_dispositiviOffline = 0
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : FiltroPerCaratteristica._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : FiltroPerCaratteristica._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : FiltroPerCaratteristica._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : FiltroPerCaratteristica._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = FiltroPerCaratteristica._Notifica_OrdinaLista)
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = FiltroPerCaratteristica._Notifica_RebuildLista)


    # ORDINAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato = True):
        return
    
    def _AggiungiDispositivo(self, idDispositivo : int):
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


FiltroPerCaratteristica.Init()