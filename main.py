from GestionePagine.Pagine.Pagine import *

#Definisco il main
def main():

    #Creo la funzione per distruggere la finestra
    def QuitEvento(eventTk = None):
        t = Thread(target = Exit)
        t.start()
         
    #Creo una funzione che verrà eseguita sempre da un thread separato
    def Update():
        chrono = Chrono()
        Impostazioni.sistema.semaforoUpdateThreadFinito.acquire()

        #Runna finchè la variabile "running" è settata su True
        Impostazioni.sistema.running = True
        while Impostazioni.sistema.running == True:
        
            #Se viene rilevato un evento di errore fatale, interrompi il programma
            if MyEventHandler.CheckFatalErrorOccurred():
                QuitEvento()
                return 
    
            #Controllo se continuare
            Impostazioni.sistema.semaforoSpegnimento.acquire()
            if Impostazioni.sistema.running == False:
                Impostazioni.sistema.semaforoSpegnimento.release()
                break

            #Altrimenti calcola il deltaTime e chiama l'update del gestore pagine
            GestorePagine.IUpdate(chrono.GetTimeFromCheckpoint())
            chrono.SetCheckpoint()
            Impostazioni.sistema.semaforoSpegnimento.release()
            time.sleep(Impostazioni.sistema.sleepTimeBetweenUpdate)
        
        LOG.log("Thread update pagine concluso")
        Impostazioni.sistema.semaforoUpdateThreadFinito.release()
        
  
      #Creo la funzione start, che crea e avvia un thread separato 'pri'ma di avviare il loop di tkInter
    def Start():
        t = Thread(target=Update)
        t.start()
        #Assegno la funzione di uscita
        GestorePagine.ICaricaPagina(PaginaGenerica.GetIdPagina(PAGINA_DEFAULT))
        GestorePagine.IGetWindow().protocol("WM_DELETE_WINDOW", QuitEvento)
        GestorePagine.IMainLoop()
        t.join()

    def Exit():
        #Chiamo tutti i distruttori prima di chiudere la finestra
        LOG.log("Avvio decostruttori")
        Impostazioni.sistema.semaforoSpegnimento.acquire()
        Impostazioni.sistema.running = False
        GestoreDispositivi.IDecostruttore()
        Impostazioni.sistema.semaforoSpegnimento.release()
        LOG.log("Decostruttore dispositivi eseguito")
        GestoreInvioMail.IDecostruttore()
        LOG.log("Distruttore gestore email eseguito")
        LOG.log("Distruttori chiamati")

        #Chiudo la finestra
        LOG.log("Richiesta autorizzazione chiusura finestra....")
        Impostazioni.sistema.semaforoSpegnimento.acquire()
        LOG.log("Autorizzazione chiusura finestra approvata")
        Impostazioni.sistema.semaforoUpdateThreadFinito.acquire()
        GestorePagine.IGetWindow().quit()
        Impostazioni.sistema.semaforoUpdateThreadFinito.release()
        LOG.log("Finestra chiusa, fine programma")
        Impostazioni.sistema.semaforoSpegnimento.release()

        #Decostruttore log
        LOG.IDecostruttore()
    
    #Avvio il programma
    Start()  
    GestorePagine.IGetWindow().bind("<Escape>", QuitEvento)


#Avvio il main
def AvvioProgramma():
    if __name__ == '__main__':
        main()

#Inizializzo l'avvio
AvvioProgramma()