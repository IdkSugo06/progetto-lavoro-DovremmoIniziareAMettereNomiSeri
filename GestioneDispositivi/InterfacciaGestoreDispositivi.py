
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
    def IAddDispositivo(nome : str, host : str, porta : str, timeTraPing : float, tag : str):
        GestoreDispositivi.IAddInformazioneDispositivoConnessione(str(nome), str(host), str(porta), timeTraPing, tag)

    @staticmethod
    def IModificaDispositivo(idDispositvo : int, nome : str, host : str, porta : str, tempoTraPing : float, tag : str):
        GestoreDispositivi.IModificaInformazioneDispositivoConnessione(idDispositvo, nome, host, porta, tempoTraPing, tag)

    @staticmethod
    def IRemoveDispositivo(idDispositivo : int):
        GestoreDispositivi.IRemoveInformazioneDispositivoConnessione(idDispositivo)

    @staticmethod
    def IClearDispositivo():
        GestoreDispositivi.IClearInformazioniConnessioniDispositivi()

    # COSTRUTTORE
    def __init__(self):
        pass


InterfacciaGestioneDispositivi.GetInterfacciaGestioneDispositivi()