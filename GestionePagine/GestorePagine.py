from GestionePagine.Pagine.PaginaGenerica import *
from GestioneDispositivi.InterfacciaGestioneDispositivi import *


#Gestirà il caricamento pagina, conterra tutte le pagine, 
#la pagina corrente e l'istanza del widget finestra principale
class GestorePagine(): #Singleton

# ATTRIBUTI STATICI -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- ATTRIBUTI STATICI
    #Creo un istanza statica accessibile da tutti col metodo GetGestorePagine()
    __gestorePagine = None


# INTERFACCE -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- INTERFACCE
    @staticmethod
    def Init(): #Inizializzo l'istanza statica
        #Se l'istanza non è ancora stata creata, la creo
        if GestorePagine.__gestorePagine == None:
            GestorePagine.__gestorePagine = GestorePagine()

    @staticmethod
    def GetGestorePagine(): #Metodo per accedere all'istanza statica
        #Se l'istanza non è ancora stata creata, la creo
        if GestorePagine.__gestorePagine == None:
            GestorePagine.__gestorePagine = GestorePagine()
        #Ritorno l'istanza statica
        return GestorePagine.__gestorePagine
    
    @staticmethod 
    def IGetWindow(): #Chiamerà l'ononima funzione dell'istanza statica 
        return GestorePagine.GetGestorePagine().__GetWindow() 
    
    @staticmethod 
    def IGetFramePagina(): #Chiamerà l'ononima funzione dell'istanza statica 
        return GestorePagine.GetGestorePagine().__GetFramePagina() 
    @staticmethod 
    def IGetFrameMenu(): #Chiamerà l'ononima funzione dell'istanza statica 
        return GestorePagine.GetGestorePagine().__GetFrameMenu() 
    
    @staticmethod
    def ICaricaPagina(idPagina : int, *args): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__CaricaPagina(idPagina, list(args))

    @staticmethod
    def ICaricaPaginaConNome(nomePagina : str, *args): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__CaricaPagina(PaginaGenerica.GetIdPagina(nomePagina), list(args))

    @staticmethod
    def IRicaricaPagina(*args): #Chiamerà l'ononima funzione dell'istanza statica 
        idPaginaAttuale = GestorePagine.GetGestorePagine().__idPaginaCaricataAttualmente
        GestorePagine.GetGestorePagine().__CaricaPagina(idPaginaAttuale, list(args))

    @staticmethod
    def IChiusuraFinestra(): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().ChiusuraFinestraEvento()
    @staticmethod
    def IHidePagina():
        GestorePagine.GetGestorePagine().__Hide()
    @staticmethod
    def IMostraPagina():
        GestorePagine.GetGestorePagine().__Mostra()
    @staticmethod
    def IUpdate(deltaTime : float): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__Update(deltaTime)

    @staticmethod
    def IUpdateMenu(deltaTime : float): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__UpdateMenu(deltaTime)

    @staticmethod
    def IUpdatePaginaCorrente(deltaTime : float): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__UpdatePaginaCorrente(deltaTime)

    @staticmethod 
    def IAddPagina(paginaDaAggiungere : PaginaGenerica): #Chiamerà l'ononima funzione dell'istanza statica 
        GestorePagine.GetGestorePagine().__AddPagina(paginaDaAggiungere)

    @staticmethod
    def ISetMenu(menu):
        GestorePagine.GetGestorePagine().__menu = menu

    @staticmethod 
    def IMainLoop(): #Inizierà il loop di tkInter
        GestorePagine.GetGestorePagine().__window.mainloop()
        LOG.log("Main loop concluso")

    def Event_MyThemeChanged(self):
        self.__menu.AggiornaColoriTema()      
        for pagina in self.__pagine:
            pagina.AggiornaColoriTema()       
    @staticmethod
    def EventFocusIn(eventTk = None):
        Impostazioni.sleepTimeBetweenUpdate = 0.02
    @staticmethod
    def EventFocusOut(eventTk = None):
        Impostazioni.sleepTimeBetweenUpdate = 0.5
    @staticmethod
    def EventConfigureCalled(eventTk = None):
        #Quando il metodo quit viene chiamato, il configure viene chiamato as well, controllo se l'esecuzione del programma è finita
        Impostazioni.sistema.semaforoSpegnimento.acquire()
        if Impostazioni.sistema.running == False: 
            Impostazioni.sistema.semaforoSpegnimento.release()
            return
        Impostazioni.sistema.semaforoSpegnimento.release()

        #Se è il thread principale, chiamo i change
        if eventTk.widget == eventTk.widget.winfo_toplevel():
            Impostazioni.sistema.dimensioniFinestra[0] = eventTk.width
            Impostazioni.sistema.dimensioniFinestra[1] = eventTk.height
            Impostazioni.sistema.ConfigureHandler.ChangeCapted()
         #Finche non ho finito il resize, nn posso chiudere

    def __ResizeRequested(self):
        Impostazioni.sistema.semaforoSpegnimento.acquire()
        if Impostazioni.sistema.running == False: 
            Impostazioni.sistema.semaforoSpegnimento.release()
            return
        Impostazioni.sistema.semaforoSpegnimento.release()
        self.__menu.CambioDimFrame()
        self.__pagine[self.__idPaginaCaricataAttualmente].CambioDimFrame()

    
# METODI -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- METODI
    # COSTRUTTORI
    def __init__(self): #Costruttore dovrebbe essere privato
        

        #Salvo una referenza alle istanze delle pagine (singleton) così da poterle utilizzare quando necessario
        self.__idPaginaCaricataAttualmente = 0 #id posizionale della pagina caricata attualmente
        self.__pagine = [] #La lista sarà popolata durante la definizione delle classi Pagina (per problemi di accesso ai file)
        self.__menu = None #La classe sarà inizializzata durante la definizione della classe Menu (per problemi di accesso ai file)


        #Creo un istanza della finestra principale e setto qualche attributo
        self.__window = tk.Tk()
        self.__window.title('Titolo')
        self.__window.geometry(str(LARGHEZZA_SCHERMO_INIZIALE) + "x" + str(ALTEZZA_SCHERMO_INIZIALE) + "+" + str(OFFSET_ORIZZONTALE_SCHERMO) + "+" + str(OFFSET_VERTICALE_SCHERMO))
        self.__window.minsize(MIN_LARGHEZZA_SCHERMO, MIN_ALTEZZA_SCHERMO)
        self.__window.maxsize(MAX_LARGHEZZA_SCHERMO, MAX_ALTEZZA_SCHERMO)

        
        #Divido la finestra principale in due sezioni orizzontali per il supporto dei due frame
        self.__window.rowconfigure(0, weight=1)
        self.__window.columnconfigure(0, weight=int(100 * Impostazioni.PROPORZIONE_MENU_PAGINA))
        self.__window.columnconfigure(1, weight=int(100 * (1 - Impostazioni.PROPORZIONE_MENU_PAGINA)))
        self.__window.grid_propagate(False)
        

        # FRAME PARTE MENU
        self.__fFrameMenu = tk.Frame(master = self.__window)
        self.__fFrameMenu.columnconfigure(0, weight=1)
        self.__fFrameMenu.rowconfigure(0, weight=1)
        self.__fFrameMenu.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameMenu.grid_propagate(False)


        # FRAME PARTE PAGINA
        self.__fFramePagina = tk.Frame(master = self.__window)
        self.__fFramePagina.columnconfigure(0, weight=1)
        self.__fFramePagina.rowconfigure(0, weight=1)
        self.__fFramePagina.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameMenu.grid_propagate(False)

        Impostazioni.sistema.ConfigureHandler.SetNotifier(self.__ResizeRequested)
        self.__window.bind("<FocusIn>", self.EventFocusIn)
        self.__window.bind("<FocusOut>", self.EventFocusOut)
        self.__window.bind("<Configure>", lambda event: GestorePagine.EventConfigureCalled(event))
        MyEventHandler.BindEvent(MyThemeChanged, self.Event_MyThemeChanged)
        
    
    # GETTER    
    def __GetWindow(self):
        #Ritorno l'istanza della finestra (Tk)
        return self.__window
    
    def __GetFramePagina(self):
        #Ritorno l'istanza della frame principale (Tk)
        return self.__fFramePagina
    
    def __GetFrameMenu(self):
        #Ritorno l'istanza della frame principale (Tk)
        return self.__fFrameMenu
    
    # ADDER
    def __AddPagina(self, paginaDaAggiungere : PaginaGenerica):
        #Aggiungo la pagina alla lista di pagine
        self.__pagine.append(paginaDaAggiungere) 
        
    # METODI GENERALI
    def __CaricaPagina(self, idPagina : int, args = []):
        #Chiudo la pagina precedente e carico la nuova
        self.__pagine[self.__idPaginaCaricataAttualmente].NascondiPagina() 
        self.__pagine[idPagina].CaricaPagina(args) 
        self.__pagine[idPagina].CambioDimFrame()
        self.__idPaginaCaricataAttualmente = idPagina
        self.__menu.EvidenziaPaginaSelezionata(PaginaGenerica.GetNomePagina(idPagina))

    def __Hide(self):
        #Nasconde temporaneamente la pagina
        self.__pagine[self.__idPaginaCaricataAttualmente].NascondiPagina() 
    def __Mostra(self):
        #Nasconde temporaneamente la pagina
        self.__pagine[self.__idPaginaCaricataAttualmente].CaricaPagina() 
    
    def __Update(self, deltaTime : float):
        #Chiamo Update di menu, pagina corrente e impostazioni
        self.__pagine[self.__idPaginaCaricataAttualmente].UpdatePagina(deltaTime)

    def __UpdatePaginaCorrente(self, deltaTime : float): #Chiamerà l'ononima funzione dell'istanza statica 
        self.__pagine[self.__idPaginaCaricataAttualmente].UpdatePagina(deltaTime)
        Impostazioni.IUpdateMousePos(self.__window.winfo_pointerx(), self.__window.winfo_pointery())

    def __UpdateMenu(self, deltaTime : float): #Chiamerà l'ononima funzione dell'istanza statica 
        self.__pagine[self.__idPaginaCaricataAttualmente].UpdatePagina(deltaTime)
        Impostazioni.IUpdateMousePos(self.__window.winfo_pointerx(), self.__window.winfo_pointery())
    

#Inizializzo il gestore pagina
GestorePagine.Init()

    

        
    