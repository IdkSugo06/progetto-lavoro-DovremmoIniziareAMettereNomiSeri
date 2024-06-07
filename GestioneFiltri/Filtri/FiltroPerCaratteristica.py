from GestioneFiltri.Filtri.FiltroGenerico import *


#Filtro figlio del filtro generico, classe astratta
class FiltroPerCaratteristica(FiltroGenerico):

    # INTERFACCE
    def _Notifica_CambioStatoDispositivo(self, idDispositivo : int, nuovoStato : bool):
        self.GetFiltro()._CambioStatoDispositivo(idDispositivo, nuovoStato)
    def _Notifica_AggiuntoDispositivo(self, idDispositivo : int):
        self.GetFiltro()._RebuildLista()
    def _Notifica_RimossoDispositivo(self, idDispositivo : int):
        self.GetFiltro()._RebuildLista()
    def _Notifica_ModificatoDispositivo(self, idDispositivo : int):
        self.GetFiltro()._RebuildLista()
    def _Notifica_OrdinaLista(self):
        self.GetFiltro()._OrdinaLista()
    def _Notifica_RebuildLista(self):
        self.GetFiltro()._RebuildLista()
    
    @staticmethod
    def GetFiltro():
        return None

    def __init__(self, nomeFiltro : str, listaDiRiferimento : list[any], funzioneDiComparazione = lambda idDispositivo1,idDispositivo2 : (-1 or 0 or 1)):
        super().__init__(nomeFiltro)
        #Associo le funzioni
        self._listaDiRiferimento = listaDiRiferimento
        self.__funzioneDiComparazione = funzioneDiComparazione
        #Bindo gli eventi per ricevere aggiornamenti quando i dispositivi sono cambiati
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : self._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : self._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : self._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : self._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = self._Notifica_OrdinaLista)
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = self._Notifica_RebuildLista)


    # ORDINAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato = True):
        return
    
    def _AggiungiDispositivo(self, idDispositivo : int): # PROBLEMA: LISTA FA RIFERIMENTO AGLI ID
        #Trovo la nuova posizione e aggiorno le liste
        idSuListaOrdinata = 0
        for id in self._listaOrdinata:
            if self.__funzioneDiComparazione(idDispositivo, idSuListaOrdinata) != 1:
                break
            idSuListaOrdinata += 1

        idUltimoElemento = len(self._listaOrdinata) - 1
        while (self.__funzioneDiComparazione(idDispositivo, idSuListaOrdinata) == 1):
            if idSuListaOrdinata >= idUltimoElemento: break
            idSuListaOrdinata += 1

        for i in range(idSuListaOrdinata, self._numOf_elementi):
            self._idDispToIdListaOrdinata[self._listaOrdinata[i]] += 1
        #Lo aggiungo alla lista
        self._listaOrdinata = self._listaOrdinata[:idSuListaOrdinata] + [idDispositivo] + self._listaOrdinata[idSuListaOrdinata:]
        self._idDispToIdListaOrdinata.append(idSuListaOrdinata)
        #Aggiorno il contatore
        self._numOf_elementi += 1
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})

    def _ModificaDispositivo(self, idDispositivo : int):
        #Trovo la posizione
        idSuListaOrdinataPrima = self._idDispToIdListaOrdinata[idDispositivo]
        idSuListaOrdinataDopo = RicercaInListaOrdinata(self._listaOrdinata, idDispositivo, funzioneDiComparazione = self.__funzioneDiComparazione)[0]
        #Muovo il blocco di elementi ed imposto gli indici
        if idSuListaOrdinataPrima > idSuListaOrdinataDopo:
            #Aumento gli indici associati
            for i in range(idSuListaOrdinataDopo, idSuListaOrdinataPrima):
                self._idDispToIdListaOrdinata[self._listaOrdinata[i]] += 1
            self._idDispToIdListaOrdinata[self._listaOrdinata[idSuListaOrdinataPrima]] = idSuListaOrdinataDopo
            #Muovo il blocco a destra
            for i in range(idSuListaOrdinataDopo, idSuListaOrdinataPrima):
                self._listaOrdinata[i+1] = self._listaOrdinata[i]
            self._listaOrdinata[idSuListaOrdinataDopo] = idDispositivo 
        elif idSuListaOrdinataPrima < idSuListaOrdinataDopo:
            #Aumento gli indici associati
            for i in range(idSuListaOrdinataPrima + 1, idSuListaOrdinataDopo + 1):
                self._idDispToIdListaOrdinata[self._listaOrdinata[i]] -= 1
            self._idDispToIdListaOrdinata[self._listaOrdinata[idSuListaOrdinataPrima]] = idSuListaOrdinataDopo
            #Muovo il blocco a destra
            for i in range(idSuListaOrdinataPrima, idSuListaOrdinataDopo):
                self._listaOrdinata[i] = self._listaOrdinata[i+1]
            self._listaOrdinata[idSuListaOrdinataDopo] = idDispositivo 

        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})

    def _RimuoviDispositivo(self, idDispositivo : int):
        #Cambio gli id a tutti i dispositivi con id maggiore
        for i in range(idDispositivo + 1, self._numOf_elementi):
            self._listaOrdinata[self._idDispToIdListaOrdinata[i]] -= 1
        
        #Riassegno le liste
        self._listaOrdinata = self._listaOrdinata[:self._idDispToIdListaOrdinata[idDispositivo]] + self._listaOrdinata[self._idDispToIdListaOrdinata[idDispositivo] + 1:]
        self._idDispToIdListaOrdinata = self._idDispToIdListaOrdinata[:idDispositivo] + self._idDispToIdListaOrdinata[idDispositivo+1:] 
        #Aggiorno il contatore
        self._numOf_elementi -= 1
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})

    def _OrdinaLista(self):
        self._listaOrdinata = InsertionSort(inputArray = self._listaOrdinata, funzioneDiConfronto = self.__funzioneDiComparazione)
        MyEventHandler.Throw(MyFilterRefreshed, {"tipoFiltro" : type(self)})
    
    def _RebuildLista(self):
        self._numOf_elementi = 0
        self._listaOrdinata = []
        self._idDispToIdListaOrdinata = []
        for id in range(len(self._listaDiRiferimento)):
            self._AggiungiDispositivo(id)
        MyEventHandler.Throw(MyFilterRebuilt, {"tipoFiltro" : type(self)})