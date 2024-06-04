from GestioneDispositivi.GestoreDispositivi import *
from GestioneDispositivi.Dispositivo import *
import json


class GestoreDispositivi:

    #Istanza statica
    __gestoreConnessioni = None
    

    # GETTER ISTANZA STATICA
    @staticmethod
    def GetGestoreConnessioni():
        if GestoreDispositivi.__gestoreConnessioni == None:
            GestoreDispositivi.__gestoreConnessioni = GestoreDispositivi()
        return GestoreDispositivi.__gestoreConnessioni


    # INTERFACCE ADD MOD CLEAR
    @staticmethod
    def IAddInformazioneDispositivoConnessione(nome : str, host : str, porta : str, timeTraPing : float, tag : str):
        return GestoreDispositivi.GetGestoreConnessioni().__addConnessione(nome, host, porta, float(timeTraPing), tag)
    @staticmethod
    def IModificaInformazioneDispositivoConnessione(idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float, tag : str):
        return GestoreDispositivi.GetGestoreConnessioni().__modificaConnessione(idPosizionale, nome, host, porta, tempoTraPing, tag)
    @staticmethod
    def IRemoveInformazioneDispositivoConnessione(idDispositivo : int):
        return GestoreDispositivi.GetGestoreConnessioni().__rimuoviConnessione(idDispositivo)
    @staticmethod
    def IClearInformazioniConnessioniDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__clearConnessioni()

    # INTERFACCE GET INFO DISPOSITIVI
    @staticmethod
    def IGetDispositivo(idPosizionale : int) -> Dispositivo:
        return GestoreDispositivi.GetGestoreConnessioni().__dispositivi[idPosizionale]
    @staticmethod
    def IGetListaDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__dispositivi
    @staticmethod
    def IOrdinaListaDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__OrdinaDispositivi()
    @staticmethod
    def IGetNumDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__numOf_dispositivi

    # INTERFACCE COMUNICAZIONE CON DISPOSITIVI
    @staticmethod
    def IPingManuale(idDispositivo : int):
        GestoreDispositivi.GetGestoreConnessioni().__dispositivi[idDispositivo].PingManuale()
    

    # COSTRUTTORE E DECOSTRUTTORE
    @staticmethod
    def IDecostruttore():
        if GestoreDispositivi.__gestoreConnessioni == None: return
        GestoreDispositivi.GetGestoreConnessioni().__SalvaDispositiviSuFile()
        GestoreDispositivi.GetGestoreConnessioni().__clearConnessioni()
        Dispositivo.semaforoThreadAttivi.acquire()
        LOG.log("Semaforo thread ping attivi spento")
        Dispositivo.semaforoThreadAttivi.release()
        Dispositivo.pausaFinitaEvent.set() #Se sono in pausa, li faccio continuare, finiranno di distruggersi correttamente
        GestoreDispositivi.__gestoreConnessioni = None

    def __del__(self):
        GestoreDispositivi.IDecostruttore()

    def __init__(self):
        #Attributi dispositivi
        self.__dispositivi = []
        self.__numOf_dispositivi = 0
        #Metadata ordinamento dispositivi
        self.__precisioneCalcoloStabilita = 0.01
        #Semaforo per add mod e clear dispositivi
        self.__semaforoAccessiStatusConnessione = Lock()
        self.__semaforoPosizionamentoDispositivi = Lock()
        #Setto le funzioni di cambio stato e notifica cambio stato
        Dispositivo.funzioneNotificaStatoCambiato = self.__CambioStatusDispositivoRilevato
        #Inizializzerà la listaInformazioniConnessioni 
        self.__LeggiDispositiviDaFile() 
        self.__OrdinaDispositivi()


    # METODI ORDINAMENTO DISPOSITIVI    
    def __CambioStatusDispositivoRilevato(self, idDispositivo : int, nuovoStato : bool):
        self.__semaforoPosizionamentoDispositivi.acquire()
        MyEventHandler.Throw(MyStatoDispositivoCambiato, args = {"idDispositivo" : idDispositivo, "stato" : nuovoStato})
        self.__semaforoPosizionamentoDispositivi.release()
    
    def __OrdinaDispositivi(self):
        self.__semaforoPosizionamentoDispositivi.acquire()
        MyEventHandler.Throw(MyFiltroRebuildNeeded)
        self.__semaforoPosizionamentoDispositivi.release()


    # SALVATAGGIO SU FILE
    def __LeggiDispositiviDaFile(self):
        with open(PATH_JSON_DISPOSITIVI, 'r') as file:
            data = json.load(file)

        #Leggo il file dei dispositivi
        try:
            dispositiviJson = data["dispositivi"]
        except:
            LOG.log("Errore durante la ricerca dei dispositivi: ", LOG_ERROR)
            return
        #Inizializzo i dispositivi
        for key in dispositiviJson:
            try:
                dispositivoSingoloJson = dispositiviJson[key]
                self.__addConnessione(nome = dispositivoSingoloJson["nomeMacchina"],
                                      host = dispositivoSingoloJson["host"],
                                      porta = dispositivoSingoloJson["porta"],
                                      timeTraPing = float(dispositivoSingoloJson["timeTraPing"]),
                                      tag = dispositivoSingoloJson["tag"])
            except Exception as e:
                LOG.log("Errore durante il caricamento del dispositivo: " + str(key) + " errore: " + str(e), LOG_ERROR)
        
    def __SalvaDispositiviSuFile(self):
        #Creo la stringa dei dispositivi
        newStr = '{\n\t\"dispositivi\" : {'
        i_dispositivo = 0
        for dispositivo in self.__dispositivi:
            newLine = f'\n\t\t"{i_dispositivo}" : '
            newLine += '{\t\"nomeMacchina\" : \"' + dispositivo.GetNome() + "\""
            newLine += ',\"host\" : \"' + dispositivo.GetHost() + "\""
            newLine += ',\"porta\" : \"' + dispositivo.GetPorta() + "\""
            newLine += ',\"timeTraPing\" : \"' + str(dispositivo.GetTempoTraPing()) + "\""
            newLine += ',\"tag\" : \"' + str(dispositivo.GetTag()) + "\""
            newLine += "},"
            newStr += newLine
            i_dispositivo += 1
        newStr = newStr[:-1] +"\n\t}\n}"
        
        #Scrivo sul file la stringa calcolata
        filestream = open(PATH_JSON_DISPOSITIVI, "w")
        filestream.write(newStr)
        filestream.close()


    # METODI CATEGORIA
    @staticmethod 
    def IGetCategorie():
        return Dispositivo.categorie
    @staticmethod
    def IAddCategoria(nuovaCategoria : str):
        if nuovaCategoria in Dispositivo.categorie:
            LOG.log("Categoria già esistente")
            return False
        Dispositivo.categorie.append(nuovaCategoria)
        MyEventHandler.Throw(MyCategoriaAggiunta, args = {"idCategoria" : len(Dispositivo.categorie) - 1})
        return True
    @staticmethod
    def IModificaCategoria(idCategoria : int, nuovaCategoria : str):
        if nuovaCategoria in Dispositivo.categorie:
            LOG.log("Categoria già esistente")
            return False
        try:
            #Controllo ogni dispositivo per controllare se sia della categoria appena cambiata
            self = GestoreDispositivi.GetGestoreConnessioni()
            categoriaPrecedente = Dispositivo.categorie[idCategoria] 
            for dispositivo in self.__dispositivi:
                if dispositivo.GetTag() == categoriaPrecedente:
                    dispositivo.SetTag(nuovaCategoria)
            Dispositivo.categorie[idCategoria] = nuovaCategoria
            return True
        except:
            return False
    @staticmethod
    def IRimuoviCategoria(idCategoria : int):
        self = GestoreDispositivi.GetGestoreConnessioni()
        categoria = Dispositivo.categorie[idCategoria]
        for dispositivo in self.__dispositivi:
            if dispositivo.GetTag() == categoria:
                dispositivo.SetTag(Dispositivo.CATEGORIA_DEFAULT)
                MyEventHandler.Throw(MyDispositivoModificato, {"idDispositivo" : dispositivo.GetId()})
        try:
            Dispositivo.categorie.pop(idCategoria)
            MyEventHandler.Throw(MyCategoriaEliminata, {"idCategoria" : idCategoria})
        except:
            LOG.log("Tentata rimozione categoria non definita", LOG_ERROR)    

    # METODI ADD MOD CLEAR
    def __addConnessione(self, nome : str, host : str, porta : str, timeTraPing : float, tag = str): #Riordinamento NON necessario
        self.__semaforoAccessiStatusConnessione.acquire()
        #Se è il primo thread, acquisice il semaforo
        Dispositivo.ThreadInizializzato()

        #Aggiungo il dispositivo
        self.__dispositivi.append(Dispositivo(nome, host, porta, timeTraPing, tag, self.__numOf_dispositivi))

        #Lancio l'evento
        MyEventHandler.Throw(MyDispositivoAggiunto, args = {"idDispositivo" : self.__numOf_dispositivi - 1})
        self.__numOf_dispositivi += 1
        self.__semaforoAccessiStatusConnessione.release()

    def __modificaConnessione(self, idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float, tag : str):
        self.__semaforoAccessiStatusConnessione.acquire()
        self.__dispositivi[idPosizionale].Modifica(nome, host, porta, tempoTraPing, tag)
        MyEventHandler.Throw(MyDispositivoModificato, args = {"idDispositivo" : idPosizionale})
        self.__semaforoAccessiStatusConnessione.release()

    def __rimuoviConnessione(self, idDispositivo : int): #Riordinamento necessario
        self.__semaforoAccessiStatusConnessione.acquire()
        #Rimuovo il dispositivo dalla lista e chiamo il decostruttore
        dispositivo = self.__dispositivi.pop(idDispositivo)
        dispositivo.myDeconstructor()

        #Decremento gli id della lista
        for i in range(idDispositivo, self.__numOf_dispositivi - 1):
            self.__dispositivi[i].DecreseId()
        
        #Diminuisco il numero di elementi
        self.__numOf_dispositivi -= 1 
        MyEventHandler.Throw(MyDispositivoRimosso, args = {"idDispositivo" : self.__numOf_dispositivi})
        self.__semaforoAccessiStatusConnessione.release()

    def __clearConnessioni(self):
        self.__semaforoAccessiStatusConnessione.acquire()
        for dispositivo in self.__dispositivi:
            dispositivo.myDeconstructor()
        #Mi accerto che tutti i thread siano stati distrutti prima di svuotare la lista
        Dispositivo.semaforoThreadAttivi.acquire()
        Dispositivo.semaforoThreadAttivi.release()
        self.__dispositivi : list[Dispositivo] = []
        self.__numOf_dispositivi = 0
        self.__semaforoAccessiStatusConnessione.release()    
    
    
GestoreDispositivi.GetGestoreConnessioni()