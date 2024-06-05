from GestioneFiltri.Filtri.FiltroPerCaratteristica import *


class FiltroPerNome(FiltroPerCaratteristica):
    _filtro = None

    # COSTRUTTORI STATICI
    @staticmethod
    def Init():
        if FiltroPerNome._filtro == None:
            FiltroPerNome._filtro = FiltroPerNome()
    @staticmethod
    def GetFiltro():
        if FiltroPerNome._filtro == None:
            FiltroPerNome._filtro = FiltroPerNome()
        return FiltroPerNome._filtro
    

    # ISTANZA STATICA
    _filtro = None
    @staticmethod
    def GetFiltro():
        return FiltroPerNome._filtro
    
    # FUNZIONI PRIVATE
    @staticmethod
    def FunzioneDiComparazione(id1 : int, id2 : int) -> int: #[-1,0,1]
        nome1 = GestoreDispositivi.IGetDispositivo(id1).GetNome().lower() 
        nome2 = GestoreDispositivi.IGetDispositivo(id2).GetNome().lower()
        return 0 if nome1 == nome2 else -1 if nome1 < nome2 else 1

    # COSTRUTTORE
    def __init__(self):
        super().__init__(nomeFiltro = NOME_INTERNO_FILTRO_NOME,
                         listaDiRiferimento = GestoreDispositivi.IGetListaDispositivi(),
                         funzioneDiComparazione = lambda id1,id2 : FiltroPerNome.FunzioneDiComparazione(id1, id2)
                         )
        

FiltroPerNome.Init()