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
    def IAddInformazioneDispositivoConnessione(nome : str, host : str, porta : str, timeTraPing : float):
        return GestoreDispositivi.GetGestoreConnessioni().__addConnessione(nome, host, porta, float(timeTraPing))
    @staticmethod
    def IModificaInformazioneDispositivoConnessione(idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float):
        return GestoreDispositivi.GetGestoreConnessioni().__modificaConnessione(idPosizionale, nome, host, porta, tempoTraPing)
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
    def IGetListaIdDispositiviOrdinati():
        return GestoreDispositivi.GetGestoreConnessioni().__idDispositiviOrdinatiPerOffOn
    @staticmethod
    def IOrdinaListaDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__OrdinaDispositivi()
    @staticmethod
    def IGetNumDispositivi():
        return GestoreDispositivi.GetGestoreConnessioni().__numOf_dispositivi
    @staticmethod  
    def IGetIdDispositivoDaIdListaOrdinata(idSuListaOrdinata : int) -> int:
        return GestoreDispositivi.GetGestoreConnessioni().__GetIdDispositivoDaListaOrdinata(idSuListaOrdinata)
    @staticmethod  
    def IGetIdListaOrdinataDaIdDispositivo(idPosizionale : int) -> int:
        return GestoreDispositivi.GetGestoreConnessioni().__GetIdListaOrdinataDaIdDispositivo(idPosizionale)

    # INTERFACCE COMUNICAZIONE CON DISPOSITIVI
    @staticmethod
    def ISetFunzioneNotificaCambioStatus(funzioneNotificaStatoCambiato : any): #Non ritorna parametri, chiamata dopo che la lista è stata ordinata
        GestoreDispositivi.GetGestoreConnessioni().__funzioneNotificaStatoCambiato = funzioneNotificaStatoCambiato
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
        self.__posizioneDispositiviSuListaOrdinata = [] #List[int], per ogni elemento i, corrisponde la posizione sulla lista ordinata utilizzata attualmente del dispositivo_i; (es: lo: [idD3,idD1,idD2], pdSuLo: [1,2,0])
        #Attributi ordinamento dispositivi
        self.__idDispositiviOrdinatiPerOffOn = [] #List[int], idDispositivi ordinati per criterio off_on, la lista sarà grande abbastanza, no append needed; (es: ld: [D1,D2,D3], lo: [2,0,1])
        self.__numOf_dispositiviOffline = 0
        self.__numOf_dispositiviOnline = 0
        #Coefficente di calcolo di stabilita (piu piccolo piu lento)
        self.__precisioneCalcoloStabilita = 0.01
        #Semaforo per add mod e clear dispositivi
        self.__semaforoAccessiStatusConnessione = Lock()
        self.__semaforoPosizionamentoDispositivi = Lock()
        #Setto le funzioni di cambio stato e notifica cambio stato
        self.__funzioneNotificaStatoCambiato = lambda x,y : x
        Dispositivo.funzioneNotificaStatoCambiato = self.__CambioStatusDispositivoRilevato
        #Inizializzerà la listaInformazioniConnessioni 
        self.__LeggiDispositiviDaFile() 
        self.__OrdinaDispositivi()


    # METODI ORDINAMENTO DISPOSITIVI
    def __GetIdDispositivoDaListaOrdinata(self, idSuListaOrdinata : int):
        idDispositivo = 0
        if True:
            idDispositivo = self.__idDispositiviOrdinatiPerOffOn[idSuListaOrdinata] 
        return idDispositivo
    def __GetIdListaOrdinataDaIdDispositivo(self, idDispositivo : int):
        idSuListaOrdinata = 0
        if True:
            idSuListaOrdinata = self.__posizioneDispositiviSuListaOrdinata[idDispositivo] 
        return idSuListaOrdinata
    
    def __CambioStatusDispositivoRilevato(self, idPosDispositivo1 : int, nuovoStato : bool):
        self.__semaforoPosizionamentoDispositivi.acquire()
        self.__CambioStatusDispositivoRilevato_OffOn(idPosDispositivo1, nuovoStato)
        self.__semaforoPosizionamentoDispositivi.release()

    def __CambioStatusDispositivoRilevato_OffOn(self, idPosDispositivo1 : int, nuovoStato : bool):
        #Trovo l'id posizionale del dispositivo da swappare
        if nuovoStato == True:
            self.__numOf_dispositiviOffline -= 1
            idPosDispositivo2 = self.__idDispositiviOrdinatiPerOffOn[self.__numOf_dispositiviOffline]
        elif nuovoStato == False:
            idPosDispositivo2 = self.__idDispositiviOrdinatiPerOffOn[self.__numOf_dispositiviOffline]
            self.__numOf_dispositiviOffline += 1
        
        #Mi salvo lo stato del dispositivo 2
        statusDisp2 = self.__dispositivi[idPosDispositivo2].GetStatusConnessione()

        #Se i dispositivi sono gli stessi cambio lo stato e basta
        if idPosDispositivo1 == idPosDispositivo2:
            self.__funzioneNotificaStatoCambiato(idPosDispositivo1, nuovoStato)
            return

        #Mi salvo gli id dei dispositivi sulla lista ordinata attuale
        idSuListaOrdinataDisp1 = self.__posizioneDispositiviSuListaOrdinata[idPosDispositivo1] 
        idSuListaOrdinataDisp2 = self.__posizioneDispositiviSuListaOrdinata[idPosDispositivo2] 
        
        #Inverto gli id nella lista di associazione id
        self.__posizioneDispositiviSuListaOrdinata[idPosDispositivo1] = idSuListaOrdinataDisp2
        self.__posizioneDispositiviSuListaOrdinata[idPosDispositivo2] = idSuListaOrdinataDisp1
        #Inverto gli id nella lista ordinata
        self.__idDispositiviOrdinatiPerOffOn[idSuListaOrdinataDisp1] = idPosDispositivo2 
        self.__idDispositiviOrdinatiPerOffOn[idSuListaOrdinataDisp2] = idPosDispositivo1

        #Notifico il cambio
        self.__funzioneNotificaStatoCambiato(idPosDispositivo1, nuovoStato)
        self.__funzioneNotificaStatoCambiato(idPosDispositivo2, statusDisp2) #Verrà cambiato con lo stato opposto sempre

    
    def __OrdinaDispositivi(self):
        self.__semaforoPosizionamentoDispositivi.acquire()
        self.__OrdinaDispositivi_OffOn()
        self.__semaforoPosizionamentoDispositivi.release()

    def __OrdinaDispositivi_OffOn(self):
        #Resetto i contatori
        self.__numOf_dispositiviOffline = 0
        self.__numOf_dispositiviOnline = 0
        #Ciclo i dispositivi
        i_dispositivo = 0
        i_dispositivoOnline = self.__numOf_dispositivi - 1
        for dispositivo in self.__dispositivi:
            #Li ordino nella lista
            statusDispCorrente = dispositivo.GetStatusConnessione()
            #Se connesso lo inserisco alla fine della lista
            if statusDispCorrente == True:
                self.__idDispositiviOrdinatiPerOffOn[i_dispositivoOnline] = i_dispositivo
                self.__posizioneDispositiviSuListaOrdinata[i_dispositivo] = i_dispositivoOnline
                i_dispositivoOnline -= 1
            elif statusDispCorrente == False:
                self.__idDispositiviOrdinatiPerOffOn[self.__numOf_dispositiviOffline] = i_dispositivo
                self.__posizioneDispositiviSuListaOrdinata[i_dispositivo] = self.__numOf_dispositiviOffline
                self.__numOf_dispositiviOffline += 1
            
            i_dispositivo += 1
        #Calcolo il numero di dispositivi online    
        self.__numOf_dispositiviOnline = self.__numOf_dispositivi - (i_dispositivoOnline + 1)       


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
                                      timeTraPing = float(dispositivoSingoloJson["timeTraPing"]))
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
            newLine += "},"
            newStr += newLine
            i_dispositivo += 1
        newStr = newStr[:-1] +"\n\t}\n}"
        
        #Scrivo sul file la stringa calcolata
        filestream = open(PATH_JSON_DISPOSITIVI, "w")
        filestream.write(newStr)
        filestream.close()


    # METODI ADD MOD CLEAR
    def __addConnessione(self, nome : str, host : str, porta : str, timeTraPing : float): #Riordinamento NON necessario
        self.__semaforoAccessiStatusConnessione.acquire()
        #Se è il primo thread, acquisice il semaforo
        Dispositivo.ThreadInizializzato()

        #Aggiungo il dispositivo
        self.__dispositivi.append(Dispositivo(nome, host, porta, timeTraPing, self.__numOf_dispositivi))
    
        #Modifico gli attributi di ordinamento
        self.__posizioneDispositiviSuListaOrdinata.append(self.__numOf_dispositivi)
        self.__idDispositiviOrdinatiPerOffOn.append(self.__numOf_dispositivi)
        #Aumento il numero di dispositivi
        self.__numOf_dispositiviOffline += 1
        self.__numOf_dispositivi += 1
        self.__semaforoAccessiStatusConnessione.release()

    def __modificaConnessione(self, idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float):
        self.__semaforoAccessiStatusConnessione.acquire()
        GestoreDispositivi.GetGestoreConnessioni().__dispositivi[idPosizionale].Modifica(nome, host, porta, tempoTraPing)
        self.__semaforoAccessiStatusConnessione.release()

    def __rimuoviConnessione(self, Iddisp : int): #Riordinamento necessario
        self.__semaforoAccessiStatusConnessione.acquire()
        #Rimuovo il dispositivo dalla lista e chiamo il decostruttore
        dispositivo = self.__dispositivi.pop(Iddisp)
        dispositivo.myDeconstructor()

        #Rimuovo un elemento casuale dalle liste ordinamento, dovranno essere riordinate (gli id contenuti non sono piu validi)
        self.__idDispositiviOrdinatiPerOffOn.pop(self.__numOf_dispositivi - 1)
        self.__posizioneDispositiviSuListaOrdinata.pop(self.__numOf_dispositivi - 1)
        
        #Decremento gli id della lista
        for i in range(Iddisp, self.__numOf_dispositivi - 1):
            self.__dispositivi[i].DecreseId()
        
        #Diminuisco il numero di elementi
        self.__numOf_dispositivi -= 1
        self.__semaforoAccessiStatusConnessione.release()

    def __clearConnessioni(self):
        self.__semaforoAccessiStatusConnessione.acquire()
        for dispositivo in self.__dispositivi:
            dispositivo.myDeconstructor()
        #Mi accerto che tutti i thread siano stati distrutti prima di svuotare la lista
        Dispositivo.semaforoThreadAttivi.acquire()
        Dispositivo.semaforoThreadAttivi.release()
        self.__dispositivi = []
        self.__numOf_dispositivi = 0
        self.__semaforoAccessiStatusConnessione.release()    
    
    
GestoreDispositivi.GetGestoreConnessioni()