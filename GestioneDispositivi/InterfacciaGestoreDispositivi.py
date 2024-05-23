
from GestioneDispositivi.GestoreDispositivi import * 


class InterfacciaGestioneDispositivi:

    #Istanza statica
    __interfacciaGestoreDispositivi=None


    # COSTRUTTORE ISTANZA STATICA
    @staticmethod
    def GetInterfacciaGestioneDispositivi():
        if InterfacciaGestioneDispositivi.__interfacciaGestoreDispositivi==None:
            InterfacciaGestioneDispositivi.__interfacciaGestoreDispositivi=InterfacciaGestioneDispositivi()
        return InterfacciaGestioneDispositivi.__interfacciaGestoreDispositivi


    # INTERFACCIA
    @staticmethod
    def IAddDispositivo(nome : str, host : str, porta : str, timeTraPing : float):
        GestoreDispositivi.IAddInformazioneDispositivoConnessione(nome, host, porta, timeTraPing)

    @staticmethod
    def IModificaDispositivo(idDispositvo : int, nome : str, host : str, porta : str, tempoTraPing : float):
        GestoreDispositivi.IModificaInformazioneDispositivoConnessione(idDispositvo, nome, host, porta, tempoTraPing)

    @staticmethod
    def IRemoveDispositivo(idDispositivo : int):
        GestoreDispositivi.IRemoveInformazioneDispositivoConnessione(idDispositivo)

    @staticmethod
    def IClearDispositivo():
        GestoreDispositivi.IClearInformazioniConnessioniDispositivi()

    @staticmethod
    def IGetStatusConnessioni() -> list[tuple[int, bool, str, int]]:
        return GestoreDispositivi.IGetStatConnessioni()

    # COSTRUTTORE
    def __init__(self):
        InterfacciaGestioneDispositivi.IAddDispositivo("Router", "172.16.0.1", 0, 1)  
        InterfacciaGestioneDispositivi.IAddDispositivo("Router", "www.google.com", 0, 1)  
        InterfacciaGestioneDispositivi.IAddDispositivo("Router", "www.youtube.it", 0, 1)  
        for i in range(20):
            InterfacciaGestioneDispositivi.IAddDispositivo("Router", "www.youtube.it", 0, 1)  
        pass


InterfacciaGestioneDispositivi.GetInterfacciaGestioneDispositivi()