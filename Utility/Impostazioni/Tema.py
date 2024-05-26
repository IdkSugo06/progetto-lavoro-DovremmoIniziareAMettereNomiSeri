from Utility.FUtility import *
import Utility.Impostazioni.Impostazioni as Impostazioni
import json


class Tema:

    __keyTemaCaricatoAttualmente = "temaDefault"
    __temi_dictStrToTema = {}

    @staticmethod
    def Init():
        with open(PATH_JSON_TEMI, 'r') as file:
            temi = json.load(file).get("temi") #Dizionario di temi
        #Per ogni tema lo appendo ai temi
        for tema in temi:
            Tema.__temi_dictStrToTema[tema] = Tema(temi[tema])
            if Tema.__temi_dictStrToTema[tema] == None:
                LOG.log("Errore durante la lettura di un tema: " + str(tema), LOG_ERROR)
                del Tema.__temi_dictStrToTema[tema]

    #legge il file e ne "estrae" i dati, se non è stato passato un tema specifico imposto il primo/default, altrimnti imposto il tema passato come parametro e se non lo trova va nell'except    
    def __init__(self, tema : dict[str : dict[str : str]]):
        #Mi salvo i dizionari
        try:
            self.__coloriSfondo = tema["coloriSfondo"]
            self.__dictfont = tema["fonts"]
            #Cerco il modificatore path, se non trovato uso il default
            self.__modificatoreFinePath = self.__dictfont["modificatoreFinePath"]
            if self.__modificatoreFinePath == "":
                self.__modificatoreFinePath = "_temaDefault"
        except Exception as e:
            return None

    @staticmethod
    def __GetTemaCaricatoAttualmente(): #Returna tema, temaDefault se non trovato
        try:
            return Tema.__temi_dictStrToTema[Tema.__keyTemaCaricatoAttualmente]
        except:
            LOG.log("Impossibile impostare caricare il tema attuale: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_WARNING)
            Tema.Init()
            return Tema.__temi_dictStrToTema["temaDefault"]
        
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
            return ("#000000", "#FFFFFF")

    @staticmethod 
    def IGetFont_ctkFormat(fontCategory : str, dimensione : int = None) -> tuple:
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            if dimensione != None:
                font[1] = int(dimensione)
            result = (font[0], font[1], font[3][0]) if len(font[3]) > 0 else  (font[0], font[1]) 
            return result
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)
            return ("arial","9")
    @staticmethod    
    def IGetFont(fontCategory : str, dimensione : int = None) -> str: #esempio "arial 18 bold"
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            if dimensione != None:
                font[1] = int(dimensione)
            modificatore = (" " + font[3][0]) if len(font[3]) > 0 else ""
            return font[0] + " " + str(font[1]) + str(modificatore)
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)
            return "arial 9"

    @staticmethod    
    def IGetFontColor(fontCategory : str) -> str: #esempio "#FFFFFF"
        try:
            font = Tema.__GetTemaCaricatoAttualmente().__dictfont[fontCategory]
            return font[2]
        except:
            LOG.log("Errore durante la ricerca di un font: " + str(fontCategory) + "; per: " + str(Tema.__keyTemaCaricatoAttualmente), LOG_ERROR)
            return "#FFFFFF"

    @staticmethod
    def IGetPathTemaCorrente(pathOriginale : str) -> str: #ritorna la path relativa al tema
        listaPathEstensione = pathOriginale.split(".") #[path, estensione]
        return listaPathEstensione[0] + Tema.__GetTemaCaricatoAttualmente().__modificatoreFinePath + "." + listaPathEstensione[1]


#inizializzazione temi
Tema.Init()
Tema.IImpostaTemaAttuale("temaDefault")