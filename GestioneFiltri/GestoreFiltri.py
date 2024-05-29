from GestioneFiltri.Filtri.Filtri import *

#Le tabelle potranno comunicare con un istanza di questa classe, che in base al filtro impostato attualmente 
#potranno accedere a funzioni interfaccia e comunicare con le liste filtrate ordinate
class GestoreFiltri:

    def __init__(self):
        self.__filtroImpostato = FiltroGenerico()


    # METODI INTERFACCIA FILTRO
    def ImpostaFiltro(self, nomeFiltro : str):
        self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)

    def GetNumElementi(self):
        return self.__filtroImpostato.GetNumElementi()
    
    def GetListaOrdinata(self):
        return self.__filtroImpostato.GetListaOrdinata()
    