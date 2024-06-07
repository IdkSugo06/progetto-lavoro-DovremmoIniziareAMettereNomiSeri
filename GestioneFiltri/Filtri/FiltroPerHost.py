from GestioneFiltri.Filtri.FiltroPerCaratteristica import *


class FiltroPerHost(FiltroPerCaratteristica):
    _filtro = None

    # COSTRUTTORI STATICI
    @staticmethod
    def Init():
        if FiltroPerHost._filtro == None:
            FiltroPerHost._filtro = FiltroPerHost()
    @staticmethod
    def GetFiltro():
        if FiltroPerHost._filtro == None:
            FiltroPerHost._filtro = FiltroPerHost()
        return FiltroPerHost._filtro
    

    # ISTANZA STATICA
    _filtro = None
    @staticmethod
    def GetFiltro():
        return FiltroPerHost._filtro
    
    # FUNZIONI PRIVATE
    @staticmethod
    def FunzioneDiComparazione(id1 : int, id2 : int) -> int: #[-1,0,1]
        host1 = GestoreDispositivi.IGetDispositivo(id1).GetHost().lower() 
        host2 = GestoreDispositivi.IGetDispositivo(id2).GetHost().lower()
        return 0 if host1 == host2 else -1 if host1 < host2 else 1

    # COSTRUTTORE
    def __init__(self):
        super().__init__(nomeFiltro = NOME_INTERNO_FILTRO_HOST,
                         listaDiRiferimento = GestoreDispositivi.IGetListaDispositivi(),
                         funzioneDiComparazione = lambda id1,id2 : FiltroPerHost.FunzioneDiComparazione(id1, id2)
                         )
        

FiltroPerHost.Init()