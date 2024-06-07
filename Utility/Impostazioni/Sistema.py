from Utility.FUtility import *
import math

dimensioniFinestra = [LARGHEZZA_SCHERMO_INIZIALE, ALTEZZA_SCHERMO_INIZIALE]
#Impostazioni di sistema
running = True
cronometro = Chrono()
tempoLastUpdate = 0.001
mousePosFrameCorrente = [0,0]
mousePosFramePrecedente = [0,0]
semaforoSpegnimento = Lock()
semaforoUpdateThreadFinito = Lock()
sensibilita_scorrimento_rotella = (45/120)
coeff_stabilizzazione_connessione = 0.05
sleepTimeBetweenUpdate = 1
tipoOrdinamentoDashboard = "off_on"
# PERSONALIZZAZIONE FINESTRA
PROPORZIONE_MENU_PAGINA = round(1/4,2)


#tempoPerStabilizzareConnessione = 64
#coefficenteStabilizzazioneConnessione = 0.5 * tempoPerStabilizzareConnessione * tempoPerStabilizzareConnessione
#def CalcoloNuovaStabilitaConnessione(stabilitaConnessione : float, tempoPassatoDaUltimoPing : float, pingResult : bool):
#    if pingResult == True:
#        return FunzioneStabilitaConnessione(Inv_FunzioneInversaStabilitaConnessione(stabilitaConnessione) + tempoPassatoDaUltimoPing)
#    elif pingResult == False:
#        return (1 - FunzioneStabilitaConnessione((tempoPerStabilizzareConnessione - Inv_FunzioneInversaStabilitaConnessione(stabilitaConnessione)) + tempoPassatoDaUltimoPing))
#    return 0
#def FunzioneStabilitaConnessione(x : float) -> float:
#    return ((-((x*x)/2) + (tempoPerStabilizzareConnessione * x)) / coefficenteStabilizzazioneConnessione)
#def Inv_FunzioneInversaStabilitaConnessione(y : float) -> float:
#    return (tempoPerStabilizzareConnessione - math.sqrt(tempoPerStabilizzareConnessione - 2*y*coefficenteStabilizzazioneConnessione))

#This will call the notifier when it reads no changes in the time set
class ConfigureHandler:

    __notifier = lambda x : x
    __timeBetweenConfigures = 0.3
    __configureThreadStarted = False
    __changeCapted = False

    @staticmethod
    def SetNotifier(notifier : any):
        ConfigureHandler.__notifier = notifier

    @staticmethod
    def ChangeCapted():
        #Segno il flag del cambiamento a True
        ConfigureHandler.__changeCapted = True
        #E se il thread non è avviato lo avvio
        if ConfigureHandler.__configureThreadStarted == True:
            return
        #Altrimenti starto il thread
        t = Thread(target=ConfigureHandler.__Thread_StartConfigureMethods)
        t.start()


    @staticmethod
    def __Thread_StartConfigureMethods():
        #Finche capta cambiamenti nel frame, aspetta e riprova
        ConfigureHandler.__configureThreadStarted = True
        while ConfigureHandler.__changeCapted:
            
            ConfigureHandler.__changeCapted = False
            time.sleep(ConfigureHandler.__timeBetweenConfigures)
        #Altrimenti chiama il notificatore e finisce

        ConfigureHandler.__notifier()
        ConfigureHandler.__configureThreadStarted = False

