from GestioneFiltri.Filtri.Filtri import *

#Le tabelle potranno comunicare con un istanza di questa classe, che in base al filtro impostato attualmente 
#potranno accedere a funzioni interfaccia e comunicare con le liste filtrate ordinate
class GestoreFiltri:

    def __init__(self,
                nomeFiltro : str,
                funzioneFiltroCambiatoGenerica : any = lambda x : x,
                funzioneElementoCambiato : any = lambda x,y,z : x, 
                funzioneRefreshTabella : any = lambda x : x,
                funzioneRebuildTabella : any = lambda x : x
                ):
        #Filtro
        self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)
        #Funzioni tabella
        self.__funzioneFiltroCambiatoGenerica = funzioneFiltroCambiatoGenerica
        self.__funzioneElementoCambiato = funzioneElementoCambiato
        self.__funzioneRefreshTabella = funzioneRefreshTabella
        self.__funzioneRebuildTabella = funzioneRebuildTabella
        #Bind eventi
        MyEventHandler.BindEvent(eventType = MyFilterChanged, functionToBind = lambda tipoFiltro, args : self.__Notifica_FiltroCambiatoGenerico(tipoFiltro, args))
        MyEventHandler.BindEvent(eventType = MyFilterElementChanged, functionToBind = lambda tipoFiltro, idElemento, stato : self.__Notifica_ElementoCambiato(tipoFiltro, idElemento, stato))
        MyEventHandler.BindEvent(eventType = MyFilterRefreshed, functionToBind = lambda tipoFiltro : self.__Notifica_RefreshListaNecessario(tipoFiltro))
        MyEventHandler.BindEvent(eventType = MyFilterRebuilt, functionToBind = lambda tipoFiltro : self.__Notifica_RebuildListaNecessario(tipoFiltro))


    # FUNZIONI NOTIFICA
    def __Notifica_FiltroCambiatoGenerico(self, tipoFiltro : type, args): #Viene chiamata quando c'è un cambio stato
        if tipoFiltro != type(self.__filtroImpostato): return
        self.__funzioneFiltroCambiatoGenerica(args)
    def __Notifica_ElementoCambiato(self, tipoFiltro : type, idElemento : int, stato : bool):
        if tipoFiltro != type(self.__filtroImpostato): return
        self.__funzioneElementoCambiato(idElemento, stato)
    def __Notifica_RefreshListaNecessario(self, tipoFiltro : type):
        if tipoFiltro != type(self.__filtroImpostato): return
        self.__funzioneRefreshTabella()
    def __Notifica_RebuildListaNecessario(self, tipoFiltro : type):
        if tipoFiltro != type(self.__filtroImpostato): return
        self.__funzioneRebuildTabella()
    

    # METODI INTERFACCIA FILTRO
    def ImpostaFiltro(self, nomeFiltro : str):
        self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)


    # INTERFACCE GETTER E SETTER FILTRO IMPOSTATO
    def GetIdDispositivo(self, idElemento : int) -> int:
        return self.__filtroImpostato.GetIdDispositivo(idElemento)
    def GetIdElemento(self, idDispositivo : int) -> int:
        return self.__filtroImpostato.GetIdElemento(idDispositivo)
    def GetNumElementi(self) -> int:
        return self.__filtroImpostato.GetNumElementi()
    def GetListaOrdinata(self) -> list[int]:
        return self.__filtroImpostato.GetListaOrdinata()
    