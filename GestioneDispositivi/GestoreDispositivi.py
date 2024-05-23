from GestioneDispositivi.GestoreDispositivi import *
from GestioneDispositivi.Dispositivo import *


class GestoreDispositivi:

    #Istanza statica
    __gestoreConnessioni = None
    

    # GETTER ISTANZA STATICA
    @staticmethod
    def GetGestoreConnessioni():
        if GestoreDispositivi.__gestoreConnessioni == None:
            GestoreDispositivi.__gestoreConnessioni = GestoreDispositivi()
        return GestoreDispositivi.__gestoreConnessioni


    # INTERFACCE
    @staticmethod
    def IAddInformazioneDispositivoConnessione(nome : str, host : str, porta : str, timeTraPing : float):
        return GestoreDispositivi.__gestoreConnessioni.__addConnessione(nome, host, porta, timeTraPing)
    @staticmethod
    def IModificaInformazioneDispositivoConnessione(idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float):
        return GestoreDispositivi.__gestoreConnessioni.__modificaConnessione(idPosizionale, nome, host, porta, tempoTraPing)
    @staticmethod
    def IRemoveInformazioneDispositivoConnessione(idDispositivo : int):
        return GestoreDispositivi.__gestoreConnessioni.__rimuoviConnessione(idDispositivo)
    @staticmethod
    def IClearInformazioniConnessioniDispositivi():
        return GestoreDispositivi.__gestoreConnessioni.__clearConnessioni()

    @staticmethod
    def IGetDispositivo(idPosizionale : int) -> Dispositivo:
        return GestoreDispositivi.__gestoreConnessioni.__informazioniConnessioniDispositivi[idPosizionale]
    
    @staticmethod
    def IGetStatConnessioni() -> list[tuple[int,bool,str,int]]: #Ritorna una lista (idDispositivo : int, status : bool, host : str, stabilitàConnessione : int)
        return GestoreDispositivi.__gestoreConnessioni.__getStatConnessioni()

    @staticmethod
    def IAggiornamentoStatusConnessioni():
        t = Thread(target=GestoreDispositivi.__gestoreConnessioni.__AggiornamentoStatusConnessioni)
        t.start()

    @staticmethod
    def IGetListaDispositivi():
        return GestoreDispositivi.__gestoreConnessioni.__informazioniConnessioniDispositivi
    @staticmethod
    def IGetNumDispositivi():
        return GestoreDispositivi.__gestoreConnessioni.__numOf_dispositivi

    @staticmethod
    def ISetFunzioneNotificaCambioStatus(funzioneNotificaStatoCambiato : any): #Aggiorna la funzione da chiamare quando il dispositivo cambia stato
        Dispositivo.funzioneNotificaStatoCambiato = funzioneNotificaStatoCambiato
        for dispositivo in GestoreDispositivi.__gestoreConnessioni.__informazioniConnessioniDispositivi:
            dispositivo.SetFunzioneNotificaCambioStatus(funzioneNotificaStatoCambiato)

    @staticmethod
    def IPingManuale(idDispositivo):
        GestoreDispositivi.__gestoreConnessioni.__informazioniConnessioniDispositivi[idDispositivo].PingManuale()

    @staticmethod
    def IDecostruttore():
        GestoreDispositivi.__gestoreConnessioni.__clearConnessioni()
        Dispositivo.semaforoThreadAttivi.acquire()
        Dispositivo.semaforoThreadAttivi.release()

    # COSTRUTTORE
    def __init__(self):
        self.__informazioniConnessioniDispositivi = []
        self.__numOf_dispositivi = 0
        self.__precisioneCalcoloStabilita=0.01
        self.__semaforoAccessiStatusConnessione = Lock()

    # METODI
    def __addConnessione(self, nome : str, host : str, porta : str, timeTraPing : float):
        self.__semaforoAccessiStatusConnessione.acquire()
        self.__informazioniConnessioniDispositivi.append(Dispositivo(nome, host, porta, timeTraPing))
        self.__numOf_dispositivi += 1
        self.__semaforoAccessiStatusConnessione.release()

    def __modificaConnessione(self, idPosizionale : int, nome : str, host : str, porta : str, tempoTraPing : float):
        self.__semaforoAccessiStatusConnessione.acquire()
        GestoreDispositivi.__gestoreConnessioni.__informazioniConnessioniDispositivi[idPosizionale].Modifica(nome, host, porta, tempoTraPing)
        self.__semaforoAccessiStatusConnessione.release()

    def __rimuoviConnessione(self, Iddisp): 
        self.__semaforoAccessiStatusConnessione.acquire()
        dispositivo = self.__informazioniConnessioniDispositivi.pop(Iddisp)
        dispositivo.myDeconstructor()
        self.__numOf_dispositivi -= 1
        for i in range(Iddisp, self.__numOf_dispositivi):
            self.__informazioniConnessioniDispositivi[i].DecreseId()
        self.__semaforoAccessiStatusConnessione.release()

    
    def __clearConnessioni(self):
        self.__semaforoAccessiStatusConnessione.acquire()
        for dispositivo in self.__informazioniConnessioniDispositivi:
            dispositivo.myDeconstructor()
        self.__informazioniConnessioniDispositivi = []
        self.__numOf_dispositivi = 0
        self.__semaforoAccessiStatusConnessione.release()


    #Ritorna le stabilità di connessioni
    def __getStatConnessioni(self) -> list[tuple[int,bool,str,int]]: #Ritorna una lista (idDispositivo : int, status : bool, host : str, stabilitàConnessione : int): 

        #Creo la lista di stabilità (ordinate in ordine crescente, il primo ha coefficente minore)
        outputArray = [None] * len(self.__informazioniConnessioniDispositivi) #La alloco prima per risparmiare prestazioni

        #Per ogni dispositivo
        i_idDispositivoAnalizzato = 0
        for informazioneConnessioneDispositivo in self.__informazioniConnessioniDispositivi:
            
            #Popolo l'output array
            stabilitaConnessioneDispAnalizzato = informazioneConnessioneDispositivo.GetStabilitaConnessione()
            stabilitaConnessione_int = int(round((stabilitaConnessioneDispAnalizzato/(100*self.__precisioneCalcoloStabilita)), 2)/self.__precisioneCalcoloStabilita)
            outputArray[i_idDispositivoAnalizzato] = (i_idDispositivoAnalizzato, 
                                                      informazioneConnessioneDispositivo.GetStatusConnessione(), 
                                                      GestoreDispositivi.IGetDispositivo(i_idDispositivoAnalizzato).GetHost(),
                                                      stabilitaConnessione_int)
            i_idDispositivoAnalizzato += 1

        #L'array avrà valore massimo 
        return InsertionSort(outputArray, lambda t : t[0][3] > t[1][3])


    # METODI PING
    def __ping_host(self, host) -> bool:
        try:
            param = '-n 1' if os.sys.platform.lower() == 'win32' else '-c 1'
            command = f"ping {param} {host} -w 200"
            result = subprocess.run(command, capture_output=True, text=True, timeout=1)

            # Se il returncode è 0, nessun errore
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        
    def __AggiornamentoStatusConnessioni(self):
        #Creo i threads
        threads = [Thread(target = self.__AggiornamentoStatusSingolaConnessione, args=[i]) for i in range(len(self.__informazioniConnessioniDispositivi))]

        #Blocco l'accesso agli status
        self.__semaforoAccessiStatusConnessione.acquire()
        for t in threads:
            t.start()
        #Aspetto che joinino prima di riconsentire l'accesso allo status dispositivi
        for t in threads:
            t.join()
        self.__semaforoAccessiStatusConnessione.release()

    def __AggiornamentoStatusSingolaConnessione(self, idPosizionaleDispositivo : int):
        risultatoConnessione = self.__ping_host(GestoreDispositivi.IGetDispositivo(idPosizionaleDispositivo).GetHost())
        self.__informazioniConnessioniDispositivi[idPosizionaleDispositivo].SetPingResult(risultatoConnessione)
    
    
    
GestoreDispositivi.GetGestoreConnessioni()