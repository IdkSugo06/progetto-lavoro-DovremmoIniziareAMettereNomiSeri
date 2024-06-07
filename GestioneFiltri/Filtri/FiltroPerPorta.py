from GestioneFiltri.Filtri.FiltroPerCaratteristica import *


class FiltroPerPorta(FiltroPerCaratteristica):
    _filtro = None

    # COSTRUTTORI STATICI
    @staticmethod
    def Init():
        if FiltroPerPorta._filtro == None:
            FiltroPerPorta._filtro = FiltroPerPorta()
    @staticmethod
    def GetFiltro():
        if FiltroPerPorta._filtro == None:
            FiltroPerPorta._filtro = FiltroPerPorta()
        return FiltroPerPorta._filtro
    

    # ISTANZA STATICA
    _filtro = None
    @staticmethod
    def GetFiltro():
        return FiltroPerPorta._filtro
    
    # FUNZIONI PRIVATE
    @staticmethod
    def FunzioneDiComparazione(id1 : int, id2 : int) -> int: #[-1,0,1]
        porta1 = GestoreDispositivi.IGetDispositivo(id1).GetPorta().lower() 
        porta2 = GestoreDispositivi.IGetDispositivo(id2).GetPorta().lower()
        return 0 if porta1 == porta2 else -1 if porta1 < porta2 else 1

    # COSTRUTTORE
    def __init__(self):
        super().__init__(nomeFiltro = NOME_INTERNO_FILTRO_PORTA,
                         listaDiRiferimento = GestoreDispositivi.IGetListaDispositivi(),
                         funzioneDiComparazione = lambda id1,id2 : FiltroPerPorta.FunzioneDiComparazione(id1, id2)
                         )
        

FiltroPerPorta.Init()