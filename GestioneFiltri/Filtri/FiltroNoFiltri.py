from GestioneFiltri.Filtri.FiltroGenerico import *

#Filtro figlio del filtro generico, singleton
class FiltroNoFiltri(FiltroGenerico):

    # INTERFACCE
    @staticmethod
    def _Notifica_CambioStatoDispositivo(idDispositivo : int, nuovoStato : bool):
        FiltroNoFiltri.GetFiltro()._CambioStatoDispositivo(idDispositivo, nuovoStato)
    @staticmethod
    def _Notifica_AggiuntoDispositivo(idDispositivo : int):
        FiltroNoFiltri.GetFiltro()._AggiungiDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_RimossoDispositivo(idDispositivo : int):
        FiltroNoFiltri.GetFiltro()._RimuoviDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_ModificatoDispositivo(idDispositivo : int):
        FiltroNoFiltri.GetFiltro()._ModificaDispositivo(idDispositivo)
    @staticmethod
    def _Notifica_OrdinaLista():
        FiltroNoFiltri.GetFiltro()._OrdinaLista()
    @staticmethod
    def _Notifica_RebuildLista():
        FiltroNoFiltri.GetFiltro()._RebuildLista()

    # ISTANZA STATICA
    _filtroNoFiltri = None
    
    # COSTRUTTORI
    @staticmethod
    def Init():
        if FiltroNoFiltri._filtroNoFiltri == None:
            FiltroNoFiltri._filtroNoFiltri = FiltroNoFiltri()
    @staticmethod
    def GetFiltro():
        if FiltroNoFiltri._filtroNoFiltri == None:
            FiltroNoFiltri._filtroNoFiltri = FiltroNoFiltri()
        return FiltroNoFiltri._filtroNoFiltri
    
    def __init__(self):
        super().__init__("filtroNoFiltri")
        self._numOf_dispositiviOffline = 0
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : FiltroNoFiltri._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : FiltroNoFiltri._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : FiltroNoFiltri._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : FiltroNoFiltri._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = FiltroNoFiltri._Notifica_OrdinaLista)
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = FiltroNoFiltri._Notifica_RebuildLista)

    # OVERRIDE (FILTRO SPECIALE)
    def GetNumElementi(self):
        return GestoreDispositivi.IGetNumDispositivi()
    def GetIdDispositivo(self, idElemento : int):
        return idElemento
    
    # FUNZIONI AGGIORNAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo : int, nuovoStato : bool):
        return
    def _AggiungiDispositivo(self, idDispositivo : int):
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})
    def _ModificaDispositivo(self, idDispositivo : int):
        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})
    def _RimuoviDispositivo(self, idDispositivo : int):
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})
    def _OrdinaLista(self):
        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})
    def _RebuildLista(self):
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})

FiltroNoFiltri.Init()