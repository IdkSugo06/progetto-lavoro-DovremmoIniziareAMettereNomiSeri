from GestioneFiltri.Filtri.FiltroGenerico import *

#Filtro figlio del filtro generico, questa classe permetterà di gestire i dispositivi
#Chiamerà eventi filtri generici, se ascoltati contengo informazioni sulla categoria filtrata che verranno ascoltati dalle tabelle interessate
#La lista ordinata conterrà gli id dei dispositivi e sarà lunga numElementi che rispettano la categoria

class FiltroStatusCategoria(FiltroGenerico):

    # Funzioni aggiornamento lista
    def _Notifica_CambioStatoDispositivo(self, idDispositivo : int, nuovoStato : bool):
        if GestoreDispositivi.IGetDispositivo(idDispositivo).GetTag() == self._categoriaFiltrata:
            self._CambioStatoDispositivo(idDispositivo, nuovoStato)

    def _Notifica_AggiuntoDispositivo(self, idDispositivo : int):
        if GestoreDispositivi.IGetDispositivo(idDispositivo).GetTag() == self._categoriaFiltrata:
            self._AggiungiDispositivo(idDispositivo)

    def _Notifica_RimossoDispositivo(self, idDispositivo : int):
        if GestoreDispositivi.IGetDispositivo(idDispositivo).GetTag() == self._categoriaFiltrata:
            self._AggiungiDispositivo(idDispositivo)

    def _Notifica_ModificatoDispositivo(self, idDispositivo : int):
        #Controllo se ce o se dovrebbe essere nella lista
        shouldBeInList = GestoreDispositivi.IGetDispositivo(idDispositivo).GetTag() == self._categoriaFiltrata #Dovrebbe essere nella lista?
        isInList = False
        for _idDispositivo in self._listaOrdinata:
            if idDispositivo == _idDispositivo:
                isInList = True
                break
        
        #Controllo se aggiungere o rimuovere il dispositivo
        if shouldBeInList == isInList: 
            return
        if isInList == True and shouldBeInList == False:
            self._RimuoviDispositivo(idDispositivo)
        if isInList == False and shouldBeInList == True:
            self._AggiungiDispositivo(idDispositivo)


    
    def __init__(self, nomeCategoria : str):
        self._categoriaFiltrata = nomeCategoria
        self._numOf_ElementiOffline = 0
        super().__init__(NOME_INTERNO_PAGINA_CATEGORIE + "_" + self._categoriaFiltrata)
        self._idDispToIdEl_dict = {}
        self._idElToIdListaOrdinata = []

        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : self._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : self._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : self._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : self._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = lambda idDispositivo : self._OrdinaLista(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = lambda idDispositivo : self._RebuildLista(idDispositivo))


    # FUNZIONI AGGIORNAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato : bool):
        #Trovo l'id posizionale del dispositivo da swappare
        if nuovoStato == True:
            self._numOf_ElementiOffline -= 1
            idDispositivo2 = self._listaOrdinata[self._numOf_ElementiOffline]
        elif nuovoStato == False:
            idDispositivo2 = self._listaOrdinata[self._numOf_ElementiOffline]
            self._numOf_ElementiOffline += 1

        #Salvo gli id degli elementi (dispositivi con categoria giusta, teoricamente messi in ordine di idDispositivo)
        idElemento1 = self._idDispToIdEl_dict[idDispositivo1]
        idElemento2 =  self._idDispToIdEl_dict[idDispositivo2]
        #Salvo gli id dei dispositivi sulla lista ordinata attuale
        idSuListaOrdinataDisp1 = self._idElToIdListaOrdinata[idElemento1] 
        idSuListaOrdinataDisp2 = self._idElToIdListaOrdinata[idElemento2] 
        #Se i dispositivi sono gli stessi cambio lo stato e basta
        if idSuListaOrdinataDisp1 == idSuListaOrdinataDisp2:
            MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato", "idElemento" : idElemento1, "idDispositivo" : idDispositivo1, "stato" : nuovoStato})
            return

        #Inverto gli id nella lista di associazione id
        self._idElToIdListaOrdinata[idElemento1] = idSuListaOrdinataDisp2
        self._idElToIdListaOrdinata[idElemento2] = idSuListaOrdinataDisp1
        #Inverto gli id nella lista ordinata
        self._listaOrdinata[idSuListaOrdinataDisp1] = idElemento2 
        self._listaOrdinata[idSuListaOrdinataDisp2] = idElemento1

        #Notifico il cambio
        MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato",  "idElemento" : idElemento1, "idDispositivo" : idDispositivo1, "stato" : nuovoStato})
        MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato",  "idElemento" : idElemento2, "idDispositivo" : idDispositivo2, "stato" : nuovoStato})


    def _AggiungiDispositivo(self, idDispositivo : int):
        #L'elmento inizializzato sarà offline, lo aggiungo come primo elemento alla lista
        self._numOf_ElementiOffline += 1
        self._numOf_elementi += 1
        #Aumento la capienza delle liste
        idElemento = self._numOf_elementi - 1
        self._idDispToIdEl_dict[idDispositivo] = idElemento
        self._listaOrdinata = [idElemento] + self._listaOrdinata
        self._idElToIdListaOrdinata.append(0) #0 perchè primo elemento della lista

        #Aumento tutti di un indice avanti
        for i in range(1, len(self._idElToIdListaOrdinata)):
            self._idElToIdListaOrdinata[i] += 1
        MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"})


    def _RimuoviDispositivo(self, idDispositivo : int):
        #Salvo gli id
        idElemento = self._idDispToIdEl_dict[idDispositivo]
        idElSuListaOrdinata = self._idElToIdListaOrdinata[idElemento]

        #Reimposto gli id posizionali
        for i_elemento in range(idElemento, self._numOf_elementi):
            self._listaOrdinata[self._idElToIdListaOrdinata[i_elemento]] -= 1
        for i in range(len(self._idElToIdListaOrdinata)):
            if self._idElToIdListaOrdinata[i] > idElSuListaOrdinata:
                self._idElToIdListaOrdinata[i] -= 1

        #Ricostruisco la lista ordinata  
        del self._idDispToIdEl_dict[idDispositivo]
        self._idElToIdListaOrdinata = self._idElToIdListaOrdinata[:idElemento] + self._idElToIdListaOrdinata[idElemento + 1:]
        self._listaOrdinata = self._listaOrdinata[:idElSuListaOrdinata] + self._listaOrdinata[idElSuListaOrdinata+1:]

        #Modifico i contatori
        if idElSuListaOrdinata <= self._numOf_ElementiOffline: #Se era offline
            self._numOf_ElementiOffline -= 1
        self._numOf_elementi -= 1
        MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"})

    def _OrdinaLista(self):
        #Resetto i contatori
        self._numOf_ElementiOffline = 0
        #Ciclo i dispositivi
        i_dispositivo = 0
        i_dispositivoOnline = self._numOf_elementi - 1
        for dispositivo in GestoreDispositivi.IGetListaDispositivi():
            if dispositivo.GetTag() != self._categoriaFiltrata:
                continue
            #Li ordino nella lista
            statusDispCorrente = dispositivo.GetStatusConnessione()
            #Se connesso lo inserisco alla fine della lista
            if statusDispCorrente == True:
                self._listaOrdinata[i_dispositivoOnline] = i_dispositivo
                self._idElToIdListaOrdinata[i_dispositivo] = i_dispositivoOnline
                i_dispositivoOnline -= 1
            elif statusDispCorrente == False:
                self._listaOrdinata[self._numOf_ElementiOffline] = i_dispositivo
                self._idElToIdListaOrdinata[i_dispositivo] = self._numOf_ElementiOffline
                self._numOf_ElementiOffline += 1
            i_dispositivo += 1
        MyEventHandler.Throw(MyFilterChanged, type(self), {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"})

    def _RebuildLista(self):
        #Ricostruisco lista e dizionario
        self._idElToIdListaOrdinata = {}
        self._listaOrdinata = [None] * self._numOf_elementi
        
        #Conto gli elementi e scarto quelli non della categoria giusta
        self._numOf_elementi = 0
        for dispositivo in GestoreDispositivi.IGetListaDispositivi():
            if dispositivo.GetTag() == self._categoriaFiltrata:
                self._numOf_elementi += 1
                self._idElToIdListaOrdinata[dispositivo.GetId()] = None

        self._OrdinaLista()
