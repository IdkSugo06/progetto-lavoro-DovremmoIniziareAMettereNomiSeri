from GestioneDispositivi.GestoreInvioEmail import *

#Lo status si aggiorna solo quando viene calcolato un ping, dopo 5 ping falliti, mail
class Dispositivo:

    param = '-n 1' if os.sys.platform.lower() == 'win32' else '-c 1'
    numOfDispositivi = 0
    funzioneNotificaStatoCambiato = lambda x,y : x #Dovra supportare self.__funzioneNotifica(dispositivo, stato)
    pausaFinitaEvent = Event()


    # COSTRUTTORE
    def __init__(self, nomeMacchina : str, host : str, porta : str, timeTraPing : float = 1): #command sarà una funzione chiamata ogni volta che lo stato viene aggiornato, note: deve prendere come parametro la referenza al Dispositivo
        Dispositivo.numOfDispositivi += 1
        self.__idPosizionale = Dispositivo.numOfDispositivi - 1
        
        #Attributi dispositivo
        self.__nomeMacchina = nomeMacchina
        self.__host = host
        self.__porta = porta

        #Attributi connessione
        self.__last5pigs = [False] * 5
        self.__status = [False, True] #(Era offline?, è offline?)
        self.__stabilitaConnessione = 0
        
        #Attributi aggiornamento
        self.__timeBetweenPing_sec = timeTraPing
        self.__idPosElementoDashboardAssociato = Dispositivo.numOfDispositivi - 1

        #Attributi thread
        self.__iBufferCircolare = 0
        self.__semaforoStatus = Lock()
        self.__eventoAttesaPing = Event()
        self.__running = False
        self.__funzioneNotificaStatoCambiato = Dispositivo.funzioneNotificaStatoCambiato

        #Inizializzo il thread
        self.InizializzazioneThreadInvioPing()
    
    def myDeconstructor(self):
        #Interrompo l'esecuzione del thread 
        self.__running = False
        #Setto l'evento per sbloccare l'attesa
        self.__eventoAttesaPing.set()

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
        self.__semaforoStatus.acquire()

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
        self.__semaforoStatus.release()
    
        #Se cè stato un cambio status, lo chiamo la notifica
        if self.__status[0] != self.__status[1]:
            self.__funzioneNotificaStatoCambiato(self, self.__status[1])
        return True

    def GetStatusConnessione(self) -> bool:
        self.__semaforoStatus.acquire()
        _b = self.__status
        self.__semaforoStatus.release()
        return _b
    def GetStatusConnessioneHasChanged(self) -> bool: #True se era connesso e ora no, e viceversa, ritorna (Changed?, (WasDown?, IsDown?))
        self.__semaforoStatus.acquire()
        _b = [self.__status[0] == (not self.__status[1]), self.__status.copy()]
        self.__semaforoStatus.release()
        return _b
    def GetStabilitaConnessione(self) -> float:
        self.__semaforoStatus.acquire()
        _f = self.__stabilitaConnessione
        self.__semaforoStatus.release()
        return _f
    

    
    # UPDATE PING
    def InizializzazioneThreadInvioPing(self):
        self.__running = True
        t = Thread(target=self.__ThreadInvioPing)
        t.start()
    
    def PingManuale(self):
        self.__eventoAttesaPing.set()


    # STATI INVIO PING
    def __ThreadInvioPing(self):
        #Finche runna
        while self.__running:

            #Attendo che non sia in pausa per inviare un nuovo pacchetto
            Dispositivo.pausaFinitaEvent.wait()

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
            self.SetPingResult(pingResult)
            setted = True
        else:
            setted = False
        
        #Attendo e ritorno
        self.__eventoAttesaPing.wait(attesa)
        self.__eventoAttesaPing.clear()
        return (pingResult, setted)

    def __ping(self):
        try:
            #Invio il ping
            command = f"ping {Dispositivo.param} {self.__host} -w 200"
            subprocessResult = subprocess.run(command, capture_output=True, text=True, timeout=1)

            # Se il returncode è 0, nessun errore
            return subprocessResult.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        
    def InvioMail(self):
        LOG.log("Mail inviata")
    