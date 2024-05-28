from GestioneDispositivi.GestoreInvioEmail import *

#Lo status si aggiorna solo quando viene calcolato un ping, dopo 5 ping falliti, mail
class Dispositivo:

    funzioneNotificaStatoCambiato = lambda x,y : x #Dovra supportare self.__funzioneNotifica(idDispositivo, status)
    pausaFinitaEvent = Event()
    numOf_threadAttivi = 0
    semaforoThreadAttivi = Lock()
    semaforoAccessoNumOf_threadAttivi = Lock()


    # COSTRUTTORE
    def __init__(self, nomeMacchina : str, host : str, porta : str, timeTraPing : float = 1, idPosizionale : int = 0): #command sarà una funzione chiamata ogni volta che lo stato viene aggiornato, note: deve prendere come parametro la referenza al Dispositivo
        self.__idPosizionale = idPosizionale
        
        #Attributi dispositivo
        self.__nomeMacchina = nomeMacchina
        self.__host = host
        self.__porta = porta

        #Attributi connessione
        self.__last5pigs = [False] * 5
        self.__status = [False, False] #(Era online?, è online?)
        self.__ultimoStatoRegistrato = False
        self.__stabilitaConnessione = 0
        
        #Attributi aggiornamento
        self.__timeBetweenPing_sec = timeTraPing
        self.__idPosElementoDashboardAssociato = idPosizionale

        #Attributi thread
        self.__iBufferCircolare = 0
        self.__semaforoStatus = Lock()
        self.__semaforoCambioStato = Lock()
        self.__eventoAttesaPing = Event()
        self.__running = False
        self.__funzioneNotificaStatoCambiato = Dispositivo.funzioneNotificaStatoCambiato

        #Inizializzo il thread
        self.InizializzazioneThreadInvioPing()
    
    def myDeconstructor(self):
        self.InizializzazioneDistruttoreThread()


    # GETTER E SETTER DI ATTRIBUTI DISPOSITIVO
    def GetHost(self):
        return self.__host
    def GetPorta(self):
        return self.__porta
    def GetNome(self):
        return self.__nomeMacchina
    def GetTempoTraPing(self):
        return self.__timeBetweenPing_sec
    def DecreseId(self):
        self.__idPosizionale -= 1
    def Modifica(self, nuovoNome : str, nuovoHost : str, nuovaPorta : str, tempoTraPing : float):
        self.__nomeMacchina = nuovoNome
        self.__host = nuovoHost
        self.__porta = nuovaPorta
        self.__timeBetweenPing_sec = float(tempoTraPing)
        self.ResetAttesaPing()
    def GetIdPosElementoDashboardAssociato(self) -> int:
        return self.__idPosElementoDashboardAssociato
    def SetIdPosElementoDashboardAssociato(self, value : int):
        self.__idPosElementoDashboardAssociato = value
    def GetId(self) -> int:
        return self.__idPosizionale
    def SetFunzioneNotificaCambioStatus(self, funzioneNotificaCambioStatus : any):
        self.__funzioneNotificaStatoCambiato = funzioneNotificaCambioStatus
    def ResetAttesaPing(self):
        self.__eventoAttesaPing.set()

    # GETTER E SETTER STATO CONNESSIONE E STABILITA
    def SetPingResult(self, pingResult : bool):
        #Semaforo per accedere alla zona critica
        self.__semaforoCambioStato.acquire()

        if not self.__running: #Interrotto durante l'acquire 
            return False
        self.__last5pigs[self.__iBufferCircolare] = pingResult
        self.__iBufferCircolare = (self.__iBufferCircolare + 1) % 5

        #Aggiorno la stabilita connessione
        if pingResult: self.__stabilitaConnessione += Impostazioni.sistema.coeff_stabilizzazione_connessione * (1-self.__stabilitaConnessione)
        else: self.__stabilitaConnessione -= Impostazioni.sistema.coeff_stabilizzazione_connessione * (self.__stabilitaConnessione)

        #Calcolo lo status
        self.__status[0] = self.__status[1]
        self.__status[1] = pingResult
    
        #Se cè stato un cambio status, lo chiamo la notifica
        if self.__status[0] != self.__status[1]:
            self.__funzioneNotificaStatoCambiato(self.__idPosizionale, self.__status[1])
            self.__ultimoStatoRegistrato = self.__status[1]
            
        self.__semaforoCambioStato.release()
        return True

    def GetStatusConnessione_senzaSemaforo(self) -> bool:
        return self.__status
    def GetStatusConnessione(self) -> bool:
        self.__semaforoStatus.acquire()
        _b = self.__ultimoStatoRegistrato
        self.__semaforoStatus.release()
        return _b
    def GetStatusConnessioneHasChanged(self) -> bool: #True se era connesso e ora no, e viceversa, ritorna (Changed?, (WasUp?, IsUp?))
        self.__semaforoStatus.acquire()
        _b = [self.__status[0] == (not self.__status[1]), self.__status.copy()]
        self.__semaforoStatus.release()
        return _b
    def GetStabilitaConnessione(self) -> float:
        _f = self.__stabilitaConnessione
        return _f
    
    
    # UPDATE PING
    def InizializzazioneThreadInvioPing(self):
        self.__running = True
        t = Thread(target=self.__AvvioThread)
        t.start()
	
    def InizializzazioneDistruttoreThread(self):
        self.__semaforoCambioStato.acquire()
        self.__semaforoStatus.acquire()
        self.__running = False
        self.__semaforoStatus.release()
        self.__semaforoCambioStato.release()
        self.__eventoAttesaPing.set()
        t = Thread(target=self.__DistruttoreThread)
        t.start()
    
    def PingManuale(self):
        self.__eventoAttesaPing.set()


    # STATI INVIO PING
    def __AvvioThread(self):
        #Se è il primo thread, acquisice il semaforo
        Dispositivo.semaforoAccessoNumOf_threadAttivi.acquire()
        Dispositivo.numOf_threadAttivi += 1
        if Dispositivo.numOf_threadAttivi == 1:
            Dispositivo.semaforoThreadAttivi.acquire()
        Dispositivo.semaforoAccessoNumOf_threadAttivi.release()
        self.__ThreadInvioPing()

    def __DistruttoreThread(self):
        #Se è l'ultimo thread, rilascia il semaforo
        Dispositivo.semaforoAccessoNumOf_threadAttivi.acquire()
        Dispositivo.numOf_threadAttivi -= 1
        if Dispositivo.numOf_threadAttivi == 0:
            Dispositivo.semaforoThreadAttivi.release()
        Dispositivo.semaforoAccessoNumOf_threadAttivi.release()

    def __ThreadInvioPing(self):
        #Attendo che il programma sia pronto e invio un pacchetto per aggiornare lo stato (parte da falso)
        Dispositivo.pausaFinitaEvent.wait()
        if not self.__running: 
            return
        result = self.InvioPing(setWhen = "WhenTrue")

        #Finche runna
        while self.__running:

            #Attendo che non sia in pausa per inviare un nuovo pacchetto
            Dispositivo.pausaFinitaEvent.wait()
            if not self.__running: 
                break

            #Controllo il ping
            result = self.InvioPing(setWhen = "WhenFalse")

            #Il ping è stato rilevato falso 
            if result[1] == True:
                self.__PingPerso_4pp() #Esce quando ping true trovato

    def __PingPerso_4pp(self): #4 ping protocol
        #Finche runna
        numOf_pingMissed = 0
        while self.__running:

            #Attendo che non sia in pausa per inviare un nuovo pacchetto
            Dispositivo.pausaFinitaEvent.wait()
            if not self.__running: return

            #Controllo il ping
            result = self.InvioPing(attesa = 1, setWhen = "WhenTrue")
            #Ritorno se trovato un ping vero
            if result[1] == True:
                return result

            numOf_pingMissed += 1
            if numOf_pingMissed == 4:
                return self.__HostDisconnesso() 

    def __HostDisconnesso(self):
        self.InvioMail()
        while self.__running:

            #Attendo che non sia in pausa per inviare un nuovo pacchetto
            Dispositivo.pausaFinitaEvent.wait()
            if not self.__running: return

            #Controllo il ping
            result = self.InvioPing(attesa = 1, setWhen = "WhenTrue")

            #Ritorno se trovato un ping vero
            if result[1] == True:
                return result

    # PROCEDURE INVIO PING
    def InvioPing(self, attesa : float = "", setWhen : str = "Always"): #setWhen must be in ("WhenTrue","WhenFalse","Always", "Never"), return is (pingResult, setted?) 
        #Se l'attesa non è specificata, default
        if attesa == "":
            attesa = self.__timeBetweenPing_sec
        
        #Invio il ping
        pingResult = self.__ping()

        #Se online aggiorno lo stato
        if (setWhen == "Always") or (setWhen == "WhenTrue") and pingResult or (setWhen == "WhenFalse" and not pingResult):
            setted = self.SetPingResult(pingResult) #True se ok, False se qualcosa è andato storto
        else:
            setted = False
        
        #Attendo e ritorno
        self.__eventoAttesaPing.wait(attesa)
        self.__eventoAttesaPing.clear()
        return (pingResult, setted)

    def __ping(self):
        try:
            #Invio il ping
            result = pythonping.ping(target=self.__host, timeout = 1, count = 1, size = 1)
            if result.success():
                return True
            else:
                return False
            
        except Exception as exception:
            LOG.log("Ping non andato a buon fine, errore: " + str(exception), LOG_ERROR)
            return False
        
    def InvioMail(self):
        LOG.log("Mail inviata (yet to be implemented)")
    
Dispositivo.pausaFinitaEvent.clear()