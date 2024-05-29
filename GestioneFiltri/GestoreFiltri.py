from GestioneFiltri.Filtri.Filtri import *

#Le tabelle potranno comunicare con un istanza di questa classe, che in base al filtro impostato attualmente 
#potranno accedere a funzioni interfaccia e comunicare con le liste filtrate ordinate
class GestoreFiltri:

    def __init__(self, nomeFiltro : str):
        self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)


    # METODI INTERFACCIA FILTRO
    def ImpostaFiltro(self, nomeFiltro : str):
        self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)


    # INTERFACCE GETTER E SETTER FILTRO IMPOSTATO
    def GetIdDispositivo(self, idElemento : int):
        return self.__filtroImpostato.GetIdDispositivo(idElemento)
    def GetIdElemento(self, idDispositivo : int):
        return self.__filtroImpostato.GetIdElemento(idDispositivo)
    def GetNumElementi(self):
        return self.__filtroImpostato.GetNumElementi()
    def GetListaOrdinata(self):
        return self.__filtroImpostato.GetListaOrdinata()
    