from Utility.Costanti import *

# LOG CONSTANTS
LOG_WARNING = 1
LOG_ERROR = 2
LOG_FATAL_ERROR = 3
LOG_PRINTENABLED = False
LOG_ISENABLED = True

#Log sarà una classe singleton che si occuperà di gestire i feedback all'interno del programma
class LOG: #singleton
    #Istanza statica
    __log = None
    __livelloFiltroDebug = 0 #incluso

    #Costruttore
    def __init__(self):
        self.debug = True
        self.msgs = []
        fileStream = open(LOG_PATH, "w")
        fileStream.write("FILE_LOG: " + "LOG DISABLED" * int(True))
        fileStream.close()

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
        if LOG_PRINTENABLED == False:
            return
        if lvlErrore >= LOG.__livelloFiltroDebug:
            LOG.GetLog().__Print(testo, lvlErrore)
    @staticmethod 
    def log(testo : str, lvlErrore : int = 0):
        LOG.IPrint(testo, lvlErrore)
    @staticmethod
    def ConversioneErrore_intToStr(lvlErrore : int):
        if lvlErrore == 0:    return ""
        elif lvlErrore == 1:  return "[AVVISO]"
        elif lvlErrore == 2:  return "[ERRORE]"
        elif lvlErrore == 3:  return "[ERRORE FATALE]"
        return "[UNKNOWN]"

    # METODI 
    def __Print(self, testo : str, lvlErrore : int = 0):
        self.msgs.append([lvlErrore,testo])

        if self.debug == False: 
            return
        avviso = LOG.ConversioneErrore_intToStr(lvlErrore)
        print(avviso, testo)

    def __SalvaSuFile(self):
        if LOG_ISENABLED == False:
            return
        #Creo la stringa
        _str = ""
        for msg in self.msgs: 
            _str += str(LOG.ConversioneErrore_intToStr(msg[0]) + ": " + str(msg[1]) + "\n")

        #Salvo gli errori nel file
        fileStream = open(LOG_PATH, "w")
        fileStream.write(_str)
        fileStream.close()
        if LOG_PRINTENABLED: 
            print("Log salvato su file")
    

LOG.Init()