from GestioneFiltri.Filtri.FiltroPerCaratteristica import *


class FiltroPerCategoriaAlfabetica(FiltroPerCaratteristica):
    _filtro = None

    # COSTRUTTORI STATICI
    @staticmethod
    def Init():
        if FiltroPerCategoriaAlfabetica._filtro == None:
            FiltroPerCategoriaAlfabetica._filtro = FiltroPerCategoriaAlfabetica()
    @staticmethod
    def GetFiltro():
        if FiltroPerCategoriaAlfabetica._filtro == None:
            FiltroPerCategoriaAlfabetica._filtro = FiltroPerCategoriaAlfabetica()
        return FiltroPerCategoriaAlfabetica._filtro
    

    # ISTANZA STATICA
    _filtro = None
    @staticmethod
    def GetFiltro():
        return FiltroPerCategoriaAlfabetica._filtro
    
    # FUNZIONI PRIVATE
    @staticmethod
    def FunzioneDiComparazione(id1 : int, id2 : int) -> int: #[-1,0,1]
        categoria1 = GestoreDispositivi.IGetDispositivo(id1).GetTag().lower() 
        categoria2 = GestoreDispositivi.IGetDispositivo(id2).GetTag().lower()
        return 0 if categoria1 == categoria2 else -1 if categoria1 < categoria2 else 1

    # COSTRUTTORE
    def __init__(self):
        super().__init__(nomeFiltro = NOME_INTERNO_FILTRO_CATEGORIA,
                         listaDiRiferimento = GestoreDispositivi.IGetListaDispositivi(),
                         funzioneDiComparazione = lambda id1,id2 : FiltroPerCategoriaAlfabetica.FunzioneDiComparazione(id1, id2)
                         )
        

FiltroPerCategoriaAlfabetica.Init()