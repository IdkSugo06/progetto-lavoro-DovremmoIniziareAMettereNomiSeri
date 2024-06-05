from GestioneFiltri.Filtri.FiltroGenerico import *

#Filtro figlio del filtro generico, questa classe permetterà di gestire i dispositivi
#Chiamerà eventi filtri generici, se ascoltati contengo informazioni sulla categoria filtrata che verranno ascoltati dalle tabelle interessate
#La lista ordinata conterrà gli id dei dispositivi e sarà lunga numElementi che rispettano la categoria

class FiltroStatusCategoria(FiltroGenerico):

    @staticmethod
    def NotificaCategoriaCreata(nomeCategoria : str):
        FiltroStatusCategoria(nomeCategoria = nomeCategoria)

    # Funzioni aggiornamento lista
    def _Notifica_CambioStatoDispositivo(self, idDispositivo : int, nuovoStato : bool):
        print("Notifica ricevuta")
        if GestoreDispositivi.IGetDispositivo(idDispositivo).GetTag() == self._categoriaFiltrata:
            print("Notifica accettata")
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
        self._idElToIdDisp_dict = {}
        self._idElToIdListaOrdinata = []

        MyEventHandler.BindEvent(eventType = MyStatoDispositivoCambiato, functionToBind = lambda idDispositivo, nuovoStato : self._Notifica_CambioStatoDispositivo(idDispositivo, nuovoStato))
        MyEventHandler.BindEvent(eventType = MyDispositivoAggiunto, functionToBind = lambda idDispositivo : self._Notifica_AggiuntoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoModificato, functionToBind = lambda idDispositivo : self._Notifica_ModificatoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyDispositivoRimosso, functionToBind = lambda idDispositivo : self._Notifica_RimossoDispositivo(idDispositivo))
        MyEventHandler.BindEvent(eventType = MyFiltroRefreshNeeded, functionToBind = self._RebuildLista)
        MyEventHandler.BindEvent(eventType = MyFiltroRebuildNeeded, functionToBind = self._RebuildLista)


    def GetIdDispositivo(self, idElemento: int):
        print("idElementoAssociato", self._listaOrdinata[idElemento])
        print("idDispositivoAssociato", self._idElToIdDisp_dict[self._listaOrdinata[idElemento]]) 
        return self._idElToIdDisp_dict[self._listaOrdinata[idElemento]]

    # FUNZIONI AGGIORNAMENTO LISTA
    def _CambioStatoDispositivo(self, idDispositivo1 : int, nuovoStato : bool):
        print("\n\nNuovo cambio stato")
        print("idDispToIdEl_dict", self._idDispToIdEl_dict)
        print("idElToIdListaOrdinata", self._idElToIdListaOrdinata)
        print("listaOrdinata", self._listaOrdinata)
        print("idElToIdDisp_dict", self._idElToIdDisp_dict)
        #Trovo l'id posizionale del dispositivo da swappare
        if nuovoStato == True:
            print("Disp",idDispositivo1,"now ONLINE, numOff",self._numOf_ElementiOffline - 1)
            self._numOf_ElementiOffline -= 1
            idElemento2 = self._listaOrdinata[self._numOf_ElementiOffline]
            idDispositivo2 = self._idElToIdDisp_dict[idElemento2]
        elif nuovoStato == False:
            print("Disp",idDispositivo1,"now OFFLINE, numOff",self._numOf_ElementiOffline + 1)
            idElemento2 = self._listaOrdinata[self._numOf_ElementiOffline]
            idDispositivo2 = self._idElToIdDisp_dict[idElemento2]
            self._numOf_ElementiOffline += 1
        #Salvo gli id degli elementi (dispositivi con categoria giusta, teoricamente messi in ordine di idDispositivo)
        idElemento1 = self._idDispToIdEl_dict[idDispositivo1]
        print("idDisp 1/2", idDispositivo1, idDispositivo2, "idEl 1/2",idElemento1, idElemento2)

        #Salvo gli id dei dispositivi sulla lista ordinata attuale
        idSuListaOrdinataDisp1 = self._idElToIdListaOrdinata[idElemento1] 
        idSuListaOrdinataDisp2 = self._idElToIdListaOrdinata[idElemento2] 
        print("idSuListaOrdinata 1/2", idSuListaOrdinataDisp1, idSuListaOrdinataDisp2)

        #Se i dispositivi sono gli stessi cambio lo stato e basta
        if idSuListaOrdinataDisp1 == idSuListaOrdinataDisp2:
            print("No change")
            MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato", "idElemento" : idSuListaOrdinataDisp1, "idDispositivo" : idDispositivo1, "stato" : nuovoStato}})
            return

        #Inverto gli id nella lista di associazione id
        self._idElToIdListaOrdinata[idElemento1] = idSuListaOrdinataDisp2
        self._idElToIdListaOrdinata[idElemento2] = idSuListaOrdinataDisp1
        #Inverto gli id nella lista ordinata
        self._listaOrdinata[idSuListaOrdinataDisp1] = idElemento2 
        self._listaOrdinata[idSuListaOrdinataDisp2] = idElemento1
        
        print("idDispToIdEl_dict", self._idDispToIdEl_dict)
        print("idElToIdListaOrdinata", self._idElToIdListaOrdinata)
        print("listaOrdinata", self._listaOrdinata)
        print("idElToIdDisp_dict", self._idElToIdDisp_dict)
        #Notifico il cambio
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato",  "idElemento" : idSuListaOrdinataDisp1, "idDispositivo" : idDispositivo1, "stato" : not nuovoStato}})
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "cambioStato",  "idElemento" : idSuListaOrdinataDisp2, "idDispositivo" : idDispositivo2, "stato" : nuovoStato}})


    def _AggiungiDispositivo(self, idDispositivo : int):
        #L'elmento inizializzato sarà offline, lo aggiungo come primo elemento alla lista
        self._numOf_ElementiOffline += 1
        self._numOf_elementi += 1
        #Aumento la capienza delle liste
        idElemento = self._numOf_elementi - 1
        self._idDispToIdEl_dict[idDispositivo] = idElemento
        self._idElToIdDisp_dict[idElemento] = idDispositivo
        self._listaOrdinata = [idElemento] + self._listaOrdinata
        self._idElToIdListaOrdinata.append(0) #0 perchè primo elemento della lista

        #Aumento tutti di un indice avanti
        for i in range(1, len(self._idElToIdListaOrdinata)):
            self._idElToIdListaOrdinata[i] += 1
        
        print("\n\nAggiunta elemento")
        print("idDispToIdEl_dict", self._idDispToIdEl_dict)
        print("idElToIdListaOrdinata", self._idElToIdListaOrdinata)
        print("listaOrdinata", self._listaOrdinata)
        print("idElToIdDisp_dict", self._idElToIdDisp_dict)
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"}})


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
        del self._idElToIdDisp_dict[idElemento]
        self._idElToIdListaOrdinata = self._idElToIdListaOrdinata[:idElemento] + self._idElToIdListaOrdinata[idElemento + 1:]
        self._listaOrdinata = self._listaOrdinata[:idElSuListaOrdinata] + self._listaOrdinata[idElSuListaOrdinata+1:]

        #Modifico i contatori
        if idElSuListaOrdinata <= self._numOf_ElementiOffline: #Se era offline
            self._numOf_ElementiOffline -= 1
        self._numOf_elementi -= 1
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"}})

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
                print("Ordinamento -- online")
                self._listaOrdinata[i_dispositivoOnline] = i_dispositivo
                self._idElToIdListaOrdinata[i_dispositivo] = i_dispositivoOnline
                i_dispositivoOnline -= 1
            elif statusDispCorrente == False:
                print("Ordinamento -- offline")
                self._listaOrdinata[self._numOf_ElementiOffline] = i_dispositivo
                self._idElToIdListaOrdinata[i_dispositivo] = self._numOf_ElementiOffline
                self._numOf_ElementiOffline += 1
            i_dispositivo += 1

        print("\n\nOrdina lista")
        print("idDispToIdEl_dict", self._idDispToIdEl_dict)
        print("idElToIdListaOrdinata", self._idElToIdListaOrdinata)
        print("listaOrdinata", self._listaOrdinata)
        print("idElToIdDisp_dict", self._idElToIdDisp_dict)
        MyEventHandler.Throw(MyFilterChanged, {"tipoFiltro" : type(self), "args" : {"codiceFiltro" : self._categoriaFiltrata, "evento" : "refresh"}})

    def _RebuildLista(self):
        #Ricostruisco il dizionario
        self._idDispToIdEl_dict = {}
        self._idElToIdDisp_dict = {}
        
        #Conto gli elementi e scarto quelli non della categoria giusta
        self._numOf_elementi = 0
        for dispositivo in GestoreDispositivi.IGetListaDispositivi():
            if dispositivo.GetTag() == self._categoriaFiltrata:
                self._idDispToIdEl_dict[dispositivo.GetId()] = self._numOf_elementi
                self._idElToIdDisp_dict[self._numOf_elementi] = dispositivo.GetId()
                self._numOf_elementi += 1

        #Ricostruisco la lista
        self._idElToIdListaOrdinata = [None] * self._numOf_elementi
        self._listaOrdinata = [None] * self._numOf_elementi
        self._OrdinaLista()


MyEventHandler.BindEvent(MyCategoriaCreata, lambda nomeCategoria : FiltroStatusCategoria.NotificaCategoriaCreata(nomeCategoria = nomeCategoria))