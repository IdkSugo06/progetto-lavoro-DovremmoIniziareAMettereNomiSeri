from Utility.Costanti import *
import json


# LOG CONSTANTS
LOG_DEBUG = -1
LOG_WARNING = 1
LOG_ERROR = 2
LOG_FATAL_ERROR = 3
LOG_PRINTENABLED = True
LOG_ISENABLED = True
LOG_DEBUG_LEVEL = 1


try:
    with open(PATH_JSON_LOG, 'r') as file:
        fileData = json.load(file).get("LOG_INFO")
    LOG_ISENABLED = fileData["LOG_ISENABLED"]

    debugLevel_str = fileData["LOG_DEBUG_LEVEL"]
    LOG_DEBUG_LEVEL = -1 if debugLevel_str == "DEBUG" else 0 if debugLevel_str == "COMMENTS" else 1 if "WARNINGS" else 2
except:
    if LOG_PRINTENABLED:
        print("Lettura info log fallita")


#Log sarà una classe singleton che si occuperà di gestire i feedback all'interno del programma
class LOG: #singleton
    #Istanza statica
    __log = None

    #Costruttore
    def __init__(self):
        self.msgs = []

    @staticmethod
    def IDecostruttore():
        LOG.GetLog().__SalvaSuFile()
    
    # METODI ACCESSO AD ISTANZA STATICA
    @staticmethod
    def Init():
        if LOG.__log == None:
            LOG.__log = LOG()
    @staticmethod
    def GetLog():
        if LOG.__log == None:
            LOG.__log = LOG()
        return LOG.__log
    
    # METODI INTERFACCIA
    @staticmethod 
    def IPrint(testo : str, lvlErrore : int = 0):
        if lvlErrore >= LOG_DEBUG_LEVEL:
            LOG.GetLog().__Print(testo, lvlErrore)
    @staticmethod 
    def log(testo : str, lvlErrore : int = 0):
        LOG.IPrint(testo, lvlErrore)
    @staticmethod
    def ConversioneErrore_intToStr(lvlErrore : int):
        if lvlErrore == -1:    return "[DEBUG 1]"
        elif lvlErrore == 0:    return ""
        elif lvlErrore == 1:  return "[AVVISO]"
        elif lvlErrore == 2:  return "[ERRORE]"
        elif lvlErrore == 3:  return "[ERRORE FATALE]"
        return "[UNKNOWN]"

    # METODI 
    def __Print(self, testo : str, lvlErrore : int = 0):
        if LOG_ISENABLED == True: 
            self.msgs.append([lvlErrore,testo])
        if LOG_PRINTENABLED == True:
            avviso = LOG.ConversioneErrore_intToStr(lvlErrore)
            print(avviso, testo)

    def __SalvaSuFile(self):
        #Apro la stream
        fileStream = open(LOG_PATH, "w")
        
        #Se disabilitato lo mostro
        if LOG_ISENABLED == False:
            fileStream.write("FILE_LOG: " + "LOG DISABLED" * int(LOG_ISENABLED))
            fileStream.close()
            return
        
        #Creo la stringa degli errori
        _str = ""
        for msg in self.msgs: 
            _str += str(LOG.ConversioneErrore_intToStr(msg[0]) + ": " + str(msg[1]) + "\n")

        #Salvo gli errori nel file
        fileStream.write(_str)
        fileStream.close()
        if LOG_PRINTENABLED: 
            print("Log salvato su file")
    

LOG.Init()