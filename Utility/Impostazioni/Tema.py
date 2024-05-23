from Utility.FUtility import *
import json


class Tema:

    __keyTemaCaricatoAttualmente = "temaDefault"
    __temi_dictStrToTema = {}

    @staticmethod
    def Init():
        Tema.__temi_dictStrToTema["temaDefault"] = Tema("temaDefault")

    #legge il file e ne "estrae" i dati, se non è stato passato un tema specifico imposto il primo/default, altrimnti imposto il tema passato come parametro e se non lo trova va nell'except
    def __init__(self, themeName=None):
        with open(PATH_JSON_TEMI, 'r') as file:
            data = json.load(file)
        if themeName == None:
            self.__coloriSfondo = data.get("coloriSfondo_temaDefault")
            self.__dictfont = data.get("fonts_temaDefault")

            #Provo ad accedere al modificatore, se non cè lo imposto default
            
        else:
            try:
                self.__coloriSfondo = data.get("coloriSfondo_"+themeName)
                self.__dictfont = data.get("fonts_"+themeName)

                #Provo ad accedere al modificatore, se non specificato lo imposto default
                self.__modificatoreFinePath = self.__dictfont["modificatoreFinePath"]
                if self.__modificatoreFinePath == "":
                    self.__modificatoreFinePath = "_temaDefault"
            except:
                LOG.log("Errore durante la ricerca del tema: " + str(themeName), LOG_ERROR)


    @staticmethod
    def __GetTemaCaricatoAttualmente(): #Returna tema, temaDefault se non trovato
        try:
            return Tema.__temi_dictStrToTema[Tema.__keyTemaCaricatoAttualmente]
        except:
            LOG.log("Impossibile impostare caricare il tema attuale: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_WARNING)
            Tema.Init()
            return Tema.__temi_dictStrToTema["temaDefault"]
        
    @staticmethod
    def ICaricaNuovoTema(nomeTema : str, impostaComeAttuale : bool = True) -> None:
        Tema.__temi_dictStrToTema[nomeTema] = Tema(nomeTema)
        if impostaComeAttuale: Tema.__keyTemaCaricatoAttualmente = nomeTema

    @staticmethod
    def IImpostaTemaAttuale(nomeTema : str) -> None:
        Tema.__keyTemaCaricatoAttualmente = nomeTema
        MyEventHandler.Throw(MyThemeChanged)

    @staticmethod
    def IGetKeyTemi_listFormat() -> list[str]:
        lista = []
        for key in Tema.__temi_dictStrToTema:
            lista.append(key)
        return lista
    @staticmethod
    def IGetKeyTemi() -> dict[str : any]: #strToTema
        return Tema.__temi_dictStrToTema

    @staticmethod    
    def IGetColoriSfondo(tipoColore : str) ->list: # esempio ["#A0A0A0","#202020"]
        try:
            return Tema.__GetTemaCaricatoAttualmente().__coloriSfondo[tipoColore]
        except:
            LOG.log("Errore durante la ricerca del colore: " + str(tipoColore) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)

    @staticmethod 
    def IGetFont_ctkFormat(fontCategory : str) -> tuple:
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            result = (font[0], font[1], font[3][0]) if len(font[3]) > 0 else  (font[0], font[1]) 
            return result
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)
    @staticmethod    
    def IGetFont(fontCategory : str) -> str: #esempio "arial 18 bold"
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            modificatore = (" " + font[3][0]) if len(font[3]) > 0 else ""
            return font[0] + " " + str(font[1]) + str(modificatore)
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)

    @staticmethod    
    def IGetFontColor(fontCategory : str) -> str: #esempio "#FFFFFF"
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            return font[2]
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)

    @staticmethod
    def IGetPathTemaCorrente(pathOriginale : str) -> str: #ritorna la path relativa al tema
        listaPathEstensione = pathOriginale.split(".") #[path, estensione]
        return listaPathEstensione[0] + Tema.__GetTemaCaricatoAttualmente().__modificatoreFinePath + "." + listaPathEstensione[1]


#inizializzazione temi
Tema.Init()
Tema.ICaricaNuovoTema("temaChiaro", False)
Tema.ICaricaNuovoTema("temaCaprio", False)
Tema.IImpostaTemaAttuale("temaDefault")