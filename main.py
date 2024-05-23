from GestionePagine.Pagine.Pagine import *

#Definisco il main
def main():
        
    #Creo una funzione che verrà eseguita sempre da un thread separato
    def Update():
        chrono = Chrono()

        #Runna finchè la variabile "running" è settata su True
        Impostazioni.sistema.running = True
        while Impostazioni.sistema.running == True:
        
            #Se viene rilevato un evento di errore fatale, interrompi il programma
            if MyEventHandler.CheckFatalErrorOccurred():
                GestorePagine.ChiusuraFinestraEvento()
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
        LOG.log("Update thread concluso")
        
  
      #Creo la funzione start, che crea e avvia un thread separato prima di avviare il loop di tkInter
    def Start():
        t = Thread(target=Update)
        t.start()
        GestorePagine.ICaricaPagina(PaginaGenerica.GetIdPagina(PAGINA_DEFAULT))
        GestorePagine.IMainLoop()
        t.join()
  
      #Creo la funzione per distruggere la finestra
    def QuitEvento(tkInterEvent = None):
        t = Thread(target=GestorePagine.ChiusuraFinestraEvento)
        t.start()
    
      #Avvio il programma
    GestorePagine.IGetWindow().bind("<Escape>", QuitEvento)
    Start()  


#Avvio il main
def AvvioProgramma():
    if __name__ == '__main__':
        main()

#Inizializzo l'avvio
AvvioProgramma()
GestoreDispositivi.IDecostruttore()
LOG.IDecostruttore()
GestoreInvioMail.IDecostruttore()
LOG.log("Distruttori chiamati, fine programma")
GestorePagine.IGetWindow().destroy()