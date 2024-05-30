from GestioneDispositivi.GestoreDispositivi import *

#Classe astratta
class FiltroGenerico:

    # ATTRIBUTI STATICI
    __filtri : dict[str : any] = {}

    # METODI STATICI
    @staticmethod
    def GetIstanzaFiltro(nomeFiltro : str):
        return FiltroGenerico.__filtri[nomeFiltro]

    # COSTRUTTORE ("ASTRATTO")
    def __init__(self, nomeFiltro):
        FiltroGenerico.__filtri[nomeFiltro] = self
        self._numOf_elementi = 0
        self._listaOrdinata = []
        self._idDispToIdListaOrdinata = []

    # GETTER E SETTER
    def GetIdDispositivo(self, idElemento : int):
        return self._listaOrdinata[idElemento]
    def GetIdElemento(self, idDispositivo : int):
        return self._idDispToIdListaOrdinata[idDispositivo]
    def GetNumElementi(self):
        return self._numOf_elementi
    def GetListaOrdinata(self):
        return self._listaOrdinata
