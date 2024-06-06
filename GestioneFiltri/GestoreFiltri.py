from GestioneFiltri.Filtri.Filtri import *

#Le tabelle potranno comunicare con un istanza di questa classe, che in base al filtro impostato attualmente 
#potranno accedere a funzioni interfaccia e comunicare con le liste filtrate ordinate
class GestoreFiltri:

    def myDistruttore(self):
        MyEventHandler.UnBindEvent(eventType = MyFilterChanged, functionToBind = self.__functionToBind_MyFilterChanged)
        MyEventHandler.UnBindEvent(eventType = MyFilterElementChanged, functionToBind = self.__functionToBind_MyFilterElementChanged)
        MyEventHandler.UnBindEvent(eventType = MyFilterRefreshed, functionToBind = self.__functionToBind_MyFilterRefreshed)
        MyEventHandler.UnBindEvent(eventType = MyFilterRebuilt, functionToBind = self.__functionToBind_MyFilterRebuilt)
        self.__filtroImpostato.myDistruttore()
        del self

    def ModificaCategoriaFiltrata(self, nomeCategoriaPrecedente : str, nomeCategoriaNuovo : str):

        if type(self.__filtroImpostato) == FiltroStatusCategoria:
            self.__filtroImpostato.ModificaCategoriaFiltrata(nomeCategoriaPrecedente, nomeCategoriaNuovo)
            self.__filtroImpostato = FiltroGenerico.GetIstanzaFiltro(NomeInternoPaginaCategoria(nomeCategoriaNuovo))
            
        
    def __init__(self,
                nomeFiltro : str,
                funzioneFiltroCambiatoGenerica : any = lambda x : x,
                funzioneElementoCambiato : any = lambda x,y,z : x, 
                funzioneRefreshTabella : any = lambda x : x,
                funzioneRebuildTabella : any = lambda x : x
                ):
        #Filtro
        self.__filtroImpostato : FiltroGenerico = FiltroGenerico.GetIstanzaFiltro(nomeFiltro)
        #Funzioni tabella
        self.__funzioneFiltroCambiatoGenerica = funzioneFiltroCambiatoGenerica
        self.__funzioneElementoCambiato = funzioneElementoCambiato
        self.__funzioneRefreshTabella = funzioneRefreshTabella
        self.__funzioneRebuildTabella = funzioneRebuildTabella
        #Bind eventi
        self.__functionToBind_MyFilterChanged = functionToBind = lambda tipoFiltro, args : self.__Notifica_FiltroCambiatoGenerico(tipoFiltro, args)
        self.__functionToBind_MyFilterElementChanged = functionToBind = lambda tipoFiltro, idElemento, stato : self.__Notifica_ElementoCambiato(tipoFiltro, idElemento, stato)
        self.__functionToBind_MyFilterRefreshed = functionToBind = lambda tipoFiltro : self.__Notifica_RefreshListaNecessario(tipoFiltro)
        self.__functionToBind_MyFilterRebuilt = functionToBind = lambda tipoFiltro : self.__Notifica_RebuildListaNecessario(tipoFiltro)
        
        self.__functionToBind__MyFilterChanged = self.__functionToBind_MyFilterChanged
        self.__functionToBind__MyFilterElementChanged = self.__functionToBind_MyFilterElementChanged
        self.__functionToBind__MyFilterRefreshed = self.__functionToBind_MyFilterRefreshed
        self.__functionToBind__MyFilterRebuilt = self.__functionToBind_MyFilterRebuilt
        MyEventHandler.BindEvent(eventType = MyFilterChanged, functionToBind = self.__functionToBind_MyFilterChanged)
        MyEventHandler.BindEvent(eventType = MyFilterElementChanged, functionToBind = self.__functionToBind_MyFilterElementChanged)
        MyEventHandler.BindEvent(eventType = MyFilterRefreshed, functionToBind = self.__functionToBind_MyFilterRefreshed)
        MyEventHandler.BindEvent(eventType = MyFilterRebuilt, functionToBind = self.__functionToBind_MyFilterRebuilt)


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
    