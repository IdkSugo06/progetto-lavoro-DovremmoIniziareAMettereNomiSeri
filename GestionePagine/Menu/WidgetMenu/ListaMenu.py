from GestionePagine.Menu.WidgetMenu.ElementoMenu import *


class ListaMenu(tk.Frame): #Occuperà tutto il frame master occupabile

    def __init__(self,
                 master : tk.Frame,
                 listaPagine : list = [] #Formato ("nomePaginaInterno", "pathImmagine", "nomePaginaMostrato")
                 ):
        
        #Attributi colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]

        #Imposto alcuni attributi 
        self.__master = master
        self.__altezzaElemento = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu
        self.__dimensioniListaMenu = [int(Impostazioni.sistema.dimensioniFinestra[0] * PROPORZIONE_MENU_PAGINA),
                                  int(Impostazioni.sistema.dimensioniFinestra[1] * PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA)]
        self.__listaPagine = listaPagine #Se vuota riassegno la lista in modo che non sia statica (statica se default come parametro)
        if len(listaPagine) == 0:  
            self.__listaPagine = [] 
           
        
        # FRAME PRINCIPALE
        super().__init__(master = self.__master, bg = self.__coloreSfondo)
        self.grid(row = 0, column = 0, sticky = "nsew")
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.grid_propagate(False)
        self.__listaElementi = []
        self.__elementoImpostazione = None

        # CREO IL CANVAS
        configurazioneCanvas = max(len(listaPagine) * Impostazioni.personalizzazioni.altezza_elemento_tabella_menu, self.__dimensioniListaMenu[1])
        self.__cCanvasScorrevole = tk.Canvas(master = self, 
                                             scrollregion = (0, 0, self.__dimensioniListaMenu[0], configurazioneCanvas),
                                             bg = self.__coloreSfondo,
                                             highlightthickness=0)
        self.__cCanvasScorrevole.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasScorrevole.grid_propagate(False)
        self.__cCanvasScorrevole.pack_propagate(False)

        # CREO IL FRAME CONTENUTO DA CANVAS
        self.__fFrameInternoCanvasScorrevole = tk.Frame(master = self, bg = self.__coloreSfondo)
        self.__fFrameInternoCanvasScorrevole.place(x = 0, y = 0, width = self.__dimensioniListaMenu[0], height = len(listaPagine) * Impostazioni.personalizzazioni.altezza_elemento_tabella_menu,anchor= "nw")
        self.__fFrameInternoCanvasScorrevole.columnconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.rowconfigure(0, weight = 1)
        self.__fFrameInternoCanvasScorrevole.grid_propagate(False)
        self.__fFrameInternoCanvasScorrevole.pack_propagate(False)
        # GENERO IL FRAME
        self.__ultimoCanvasId = self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniListaMenu[0],
                                              height = len(listaPagine) * Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)
                                            
        
        # LISTA ELEMENTI MENU
        self.__listaElementi = []
        self.RefreshMenu()

        # BIND
        self.__cCanvasScorrevole.bind("<MouseWheel>", lambda event : self.Scroll(event))


    def AddPagina(self, nomeInterno : str, pathImmagine : str, nomeEsterno : str):
        self.__listaPagine.append((nomeInterno, pathImmagine, nomeEsterno))
        self.RefreshMenu()
        self.CambioDimFrame()

    # METODI START UPDATE FINISH
    def Update(self, deltaTime : float = 0): #Disabled
        return

    # METODI
    def EvidenziaPaginaSelezionata(self, nomePaginaInternoSelezionato : str):
        
        if self.__elementoImpostazione.GetNomePaginaInterno() != nomePaginaInternoSelezionato:
            self.__elementoImpostazione.ElementoDeselezionato() 

        for elementoMenu in self.__listaElementi:
            if elementoMenu.GetNomePaginaInterno() != nomePaginaInternoSelezionato:
                elementoMenu.ElementoDeselezionato()

    # METODI EVENTI
    def Scroll(self, event):
        self.__cCanvasScorrevole.yview_scroll(int(-event.delta * Impostazioni.sistema.sensibilita_scorrimento_rotella), "units")

    # METODI RICONFIGURAZIONE
    def RefreshMenu(self):
        self.__listaElementi = []
        contatoreElementi = 0
        self.__elementoImpostazione = ElementoMenu(master = self.__cCanvasScorrevole, 
                                            nomePaginaInterno = TUPLA_PAGINA_IMPOSTAZIONI[0],
                                            pathImmagine = TUPLA_PAGINA_IMPOSTAZIONI[1], 
                                            nomePaginaMostrato = TUPLA_PAGINA_IMPOSTAZIONI[2],  
                                            xPos = 0, 
                                            yPos = self.__dimensioniListaMenu[1] - Impostazioni.personalizzazioni.altezza_elemento_tabella_menu - 4,
                                            width = self.__dimensioniListaMenu[0],
                                            height = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)
        
        for pagina_tupla in self.__listaPagine:
            self.__listaElementi.append(ElementoMenu(
                                            master = self.__fFrameInternoCanvasScorrevole, 
                                            nomePaginaInterno = pagina_tupla[0],
                                            pathImmagine = pagina_tupla[1], 
                                            nomePaginaMostrato = pagina_tupla[2], 
                                            xPos = 0, 
                                            yPos = contatoreElementi * self.__altezzaElemento,
                                            width = self.__dimensioniListaMenu[0],
                                            height = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)
                                        )                           
            self.__listaElementi[contatoreElementi].myBind("<MouseWheel>", lambda event : self.Scroll(event))
            contatoreElementi += 1
        


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.AggiornaColore()
    
        #Per ogni elemento aggiorno i colori
        for elemento in self.__listaElementi:
            elemento.AggiornaColoriTema()
        self.__elementoImpostazione.AggiornaColoriTema()
        self.EvidenziaPaginaSelezionata(NOME_INTERNO_PAGINA_IMPOSTAZIONI)

    def AggiornaColore(self):
        self.__fFrameInternoCanvasScorrevole.configure(background = self.__coloreSfondo)
        self.__cCanvasScorrevole.configure(background = self.__coloreSfondo)
            
    def CambioFont(self):
        pass 
    
    def CambioDimFrame(self):
        #Ricalcolo le dimensioni del menu
        self.__dimensioniListaMenu = [int(Impostazioni.sistema.dimensioniFinestra[0] * Impostazioni.PROPORZIONE_MENU_PAGINA),
                                      int(Impostazioni.sistema.dimensioniFinestra[1] * PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA)]
        altezzaListaMenu = max(len(self.__listaPagine) * Impostazioni.personalizzazioni.altezza_elemento_tabella_menu, self.__dimensioniListaMenu[1])

        #Ricreo il canvas
        self.__cCanvasScorrevole.configure(scrollregion = (0, 0, self.__dimensioniListaMenu[0], altezzaListaMenu))
        thisCanvasId = self.__cCanvasScorrevole.create_window((0,0),
                                              window = self.__fFrameInternoCanvasScorrevole,
                                              anchor = "nw", 
                                              width = self.__dimensioniListaMenu[0],
                                              height = len(self.__listaElementi) * Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)

        self.__cCanvasScorrevole.delete(self.__ultimoCanvasId)
        self.__ultimoCanvasId = thisCanvasId
        #Refresho il menu
        self.__elementoImpostazione.SetPos(x = 0, y = self.__dimensioniListaMenu[1] - Impostazioni.personalizzazioni.altezza_elemento_tabella_menu - 4)
        self.__elementoImpostazione.CambioDimFrame(width = self.__dimensioniListaMenu[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)
        for elementoMenu in self.__listaElementi:
            elementoMenu.CambioDimFrame(width = self.__dimensioniListaMenu[0], height = Impostazioni.personalizzazioni.altezza_elemento_tabella_menu)