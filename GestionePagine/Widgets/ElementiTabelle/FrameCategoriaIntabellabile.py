from GestionePagine.Widgets.ElementiTabelle.ElementoIntabellabile import *

class FrameCategoriaIntabellabile(ElementoIntabellabile):
    
    def myDistruttore(self):
        self.place_forget()

    def __init__(self,
                 master, 
                 x : int = 0, 
                 y : int = 0,
                 width : int = 250, 
                 height : int = 50,
                 isShown : bool = True,
                 idCategoria : int = 0):
        
        #Salvo i colori
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreSfondoEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreTesto = Impostazioni.Tema.IGetFontColor("testo")

        # Chiamo il costruttore della classe padre
        super().__init__(
                 master,
                 x, 
                 y,
                 width, 
                 height,
                 False,
                 colore = self.__coloreSfondo,
                 coloreBordo = self.__coloreBordo,
                 spessoreBordo = 0)
        
        #Attributi 
        self.__idCategoriaAssociato = None    
        self.__modalitaModificaAttiva = False

        # CREO IL FRAME PRINCIPALE - MOSTRA ATTRIBUTI 
        self.__fFrameMostraAttributi = tk.Frame(self, bg = self.__coloreSfondo)
        self.__fFrameMostraAttributi.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameMostraAttributi.rowconfigure(0, weight = 1)
        self.__fFrameMostraAttributi.columnconfigure(0, weight = int(100 * (1 - PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI)))
        self.__fFrameMostraAttributi.columnconfigure(1, weight = int(100 * PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI))
        self.__fFrameMostraAttributi.grid_propagate(False)
        
        # FRAME SUPPORTO SCRITTA NOME
        self.__fFrameScrittaNome = tk.Frame(master = self.__fFrameMostraAttributi, bg = self.__coloreSfondo, highlightbackground= self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameScrittaNome.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameScrittaNome.rowconfigure(0, weight = 1)
        self.__fFrameScrittaNome.columnconfigure(0, weight = 1)
        self.__fFrameScrittaNome.grid_propagate(False)
        self.__fFrameScrittaNome.pack_propagate(False)
        #Creo la variabile della scritta
        self.__vScrittaNome_str = tk.StringVar() 
        self.__vScrittaNome_str.set("Nome categoria")
        #Creo la scritta 
        self.__lScrittaNome = tk.Label(master = self.__fFrameScrittaNome, 
                                         textvariable = self.__vScrittaNome_str, 
                                         font = self.__fontTesto, 
                                         fg = self.__coloreTesto,
                                         bg = self.__coloreSfondo)
        self.__lScrittaNome.pack(side = "left")


        # DEFINISCO PROPORZIONI BOTTONI SPAZIO BOTTONI
        self.__rapportoSpaziAltoBottoni = 0.05
        self.__rapportoSpaziLatoBottoni = 0.10
        self.__mantieniProporzioniImmagine = False
        dimBottoni = (20,20)

        # SUPPORTO BOTTONI
        self.__fFrameSupportoBottoni = tk.Frame(master = self.__fFrameMostraAttributi, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameSupportoBottoni.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameSupportoBottoni.rowconfigure(0, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoni.rowconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziAltoBottoni * 2)))
        self.__fFrameSupportoBottoni.rowconfigure(2, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoni.columnconfigure(0, weight = int(100 * self.__rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoni.columnconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoni.columnconfigure(2, weight = int(100 * self.__rapportoSpaziLatoBottoni * 1.5))
        self.__fFrameSupportoBottoni.columnconfigure(3, weight = int(100 * (1 - self.__rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoni.columnconfigure(4, weight = int(100 * self.__rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoni.grid_propagate(False)
        self.__fFrameSupportoBottoni.pack_propagate(False)

        # FRAME SUPPORTO BOTTONE MODIFICA
        self.__fFrameBottoneModifica = tk.Frame(master = self.__fFrameSupportoBottoni, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneModifica.grid(row = 1, column = 1, sticky = "nsew")
        self.__fFrameBottoneModifica.rowconfigure(0, weight = 1)
        self.__fFrameBottoneModifica.columnconfigure(0, weight = 1)
        self.__fFrameBottoneModifica.grid_propagate(False)
        self.__fFrameBottoneModifica.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneModifica = tk.Canvas(master = self.__fFrameBottoneModifica, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneModifica.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneModifica.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneModifica.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneModifica.grid_propagate(False)
        self.__cCanvasBottoneModifica.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneModifica = MyImageButton(canvas = self.__cCanvasBottoneModifica, command = lambda event : self.__ModificaCategoriaAssociata(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_MODIFICA_PAG_DISPOSITIVI))
        self.__myImgbBottoneModifica.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneModifica.Show()
        

        # FRAME SUPPORTO BOTTONE ELIMINA
        self.__fFrameBottoneElimina = tk.Frame(master = self.__fFrameSupportoBottoni, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneElimina.grid(row = 1, column = 3, sticky = "nsew")
        self.__fFrameBottoneElimina.rowconfigure(0, weight = 1)
        self.__fFrameBottoneElimina.columnconfigure(0, weight = 1)
        self.__fFrameBottoneElimina.grid_propagate(False)
        self.__fFrameBottoneElimina.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneElimina = tk.Canvas(master = self.__fFrameBottoneElimina, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneElimina.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneElimina.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneElimina.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneElimina.grid_propagate(False)
        self.__cCanvasBottoneElimina.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneElimina = MyImageButton(canvas = self.__cCanvasBottoneElimina, command = lambda event : self.__EliminaCategoriaAssociata(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneElimina.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneElimina.Show()


        # CREO IL FRAME PRINCIPALE - MODIFICA ATTRIBUTI
        self.__fFrameModificaAttributi = tk.Frame(self, bg =  self.__coloreSfondo)
        self.__fFrameModificaAttributi.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameModificaAttributi.rowconfigure(0, weight = 1)
        self.__fFrameModificaAttributi.columnconfigure(0, weight = int(100 * (1 - (PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI/2))))
        self.__fFrameModificaAttributi.columnconfigure(1, weight = int(100 * (PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI/2)))
        self.__fFrameModificaAttributi.grid_propagate(False)

        # BARRA INSERIMENTO NOME
        self.__myBarraInserimentoNome = MyBarraInserimento(master = self.__fFrameModificaAttributi, text = "Categoria", looseContentOnFirstFocus = True, hover = True)
        self.__myBarraInserimentoNome.grid(row = 0, column = 0, sticky="nsew")

        # SUPPORTO BOTTONE
        self.__fFrameSupportoBottoneConfermaModifica = tk.Frame(master = self.__fFrameModificaAttributi, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo, highlightthickness=0.5)
        self.__fFrameSupportoBottoneConfermaModifica.grid(row = 0, column = 1, sticky = "nsew")
        self.__fFrameSupportoBottoneConfermaModifica.rowconfigure(0, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoneConfermaModifica.rowconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziAltoBottoni * 2)))
        self.__fFrameSupportoBottoneConfermaModifica.rowconfigure(2, weight = int(100 * self.__rapportoSpaziAltoBottoni))
        self.__fFrameSupportoBottoneConfermaModifica.columnconfigure(0, weight = int(100 * self.__rapportoSpaziLatoBottoni))
        self.__fFrameSupportoBottoneConfermaModifica.columnconfigure(1, weight = int(100 * (1 - self.__rapportoSpaziLatoBottoni * 3.5) * 0.5))
        self.__fFrameSupportoBottoneConfermaModifica.columnconfigure(2, weight = int(100 * self.__rapportoSpaziLatoBottoni * 1.5))
        self.__fFrameSupportoBottoneConfermaModifica.grid_propagate(False)
        self.__fFrameSupportoBottoneConfermaModifica.pack_propagate(False)
        # IMMAGINE CONFERMA
        self.__fFrameBottoneConfermaModifica = tk.Frame(master = self.__fFrameSupportoBottoneConfermaModifica, bg =  self.__coloreSfondo, highlightbackground=  self.__coloreBordo)
        self.__fFrameBottoneConfermaModifica.grid(row = 1, column = 1, sticky = "nsew")
        self.__fFrameBottoneConfermaModifica.rowconfigure(0, weight = 1)
        self.__fFrameBottoneConfermaModifica.columnconfigure(0, weight = 1)
        self.__fFrameBottoneConfermaModifica.grid_propagate(False)
        self.__fFrameBottoneConfermaModifica.pack_propagate(False)
        #Creo il canvas di supporto
        self.__cCanvasBottoneConfermaModifica = tk.Canvas(master = self.__fFrameBottoneConfermaModifica, bg =  self.__coloreSfondo, highlightthickness = 0)
        self.__cCanvasBottoneConfermaModifica.grid(row = 0, column = 0, sticky = "nsew")
        self.__cCanvasBottoneConfermaModifica.rowconfigure(0, weight = 1)
        self.__cCanvasBottoneConfermaModifica.columnconfigure(0, weight = 1)
        self.__cCanvasBottoneConfermaModifica.grid_propagate(False)
        self.__cCanvasBottoneConfermaModifica.pack_propagate(False)
        #Creo il bottone
        self.__myImgbBottoneConfermaModifica = MyImageButton(canvas = self.__cCanvasBottoneConfermaModifica, command = lambda event : self.__ConfermaModificaCategoriaAssociata(event), path = Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneConfermaModifica.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneConfermaModifica.Show()


        #Associo il dispositivo specificato
        self.AssociaCategoria(idCategoria)
        self.Show()
        self.__ImpostaModalitaMostraAttributi()


        # METODI EVENTI
        self.myBind("<Return>", lambda event : self.__ConfermaModificaCategoriaAssociata(event))
        self.myBind("<Enter>", lambda event : self.__CursorEntered(event))
        self.myBind("<Leave>", lambda event : self.__CursorExited(event))



    # METODI MODIFICA
    def __ImpostaModalitaModifica(self):
        self.__modalitaModificaAttiva = True
        self.__fFrameMostraAttributi.grid_forget()
        self.__fFrameModificaAttributi.grid_propagate(True)
        self.__fFrameModificaAttributi.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameModificaAttributi.grid_propagate(False)
        self.__myBarraInserimentoNome.Set(Dispositivo.categorie[self.__idCategoriaAssociato])
    def __ImpostaModalitaMostraAttributi(self):
        self.__modalitaModificaAttiva = False
        self.__fFrameModificaAttributi.grid_forget()
        self.__fFrameMostraAttributi.grid_propagate(True)
        self.__fFrameMostraAttributi.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFrameMostraAttributi.grid_propagate(False)
        self.__vScrittaNome_str.set(Dispositivo.categorie[self.__idCategoriaAssociato])

    def Show(self):
        self.place(x = self._posizione[0], y = self._posizione[1], width = self._dimensioni[0], height = self._dimensioni[1])        
        self.__ImpostaModalitaMostraAttributi()

    # METODI GESTIONE DISPOSITIVI
    def AggiornaAttributiElemento(self, i_categoria : int):
        self.AssociaCategoria(i_categoria, aggiornamentoForzato = True)
        
    def AssociaCategoria(self, i_categoria : int, aggiornamentoForzato : bool = False):
        #Controllo se è un nuovo dispositivo
        if ((self.__idCategoriaAssociato == i_categoria) and not aggiornamentoForzato):
            return
        #Se no aggiorno i valori
        self.__idCategoriaAssociato = i_categoria
        self.RefreshAttributiElemento()

    def RefreshAttributiElemento(self):
        nomeCategoria = Dispositivo.categorie[self.__idCategoriaAssociato]
        self.__vScrittaNome_str.set(nomeCategoria)

    def __ModificaCategoriaAssociata(self, eventTk = None):
        self.__ImpostaModalitaModifica()

    def __EliminaCategoriaAssociata(self, eventTk = None):
        nomeCategoria = Dispositivo.categorie[self.__idCategoriaAssociato]
        GestoreDispositivi.IRimuoviCategoria(self.__idCategoriaAssociato)
        MyEventHandler.Throw(MyCategoriaEliminata, {"nomeCategoria" : nomeCategoria})
        GestorePagine.IRicaricaMenu()
        GestorePagine.ICaricaPagina(PaginaGenerica.GetIdPagina(NOME_INTERNO_PAGINA_CATEGORIE))

    def __ConfermaModificaCategoriaAssociata(self, eventTk = None):
        if self.__modalitaModificaAttiva != True: return
        nomePrecedente = Dispositivo.categorie[self.__idCategoriaAssociato]
        GestoreDispositivi.IModificaCategoria(self.__idCategoriaAssociato, self.__myBarraInserimentoNome.Get())
        MyEventHandler.Throw(MyCategoriaModificata, {"nomeCategoriaPrecedente" : nomePrecedente, "nomeCategoriaNuovo" : self.__myBarraInserimentoNome.Get()})
        self.__ImpostaModalitaMostraAttributi()

    # METODI START UPDATE FINISH
    def Update(self, deltaTime : float = 0): #Disabled
        return
    


    # METODI PERSONALIZZAZIONE
    @staticmethod 
    def AggiornaImmagineTema():
        return
    def AggiornaColoriTema(self):
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreSfondoEvidenziato = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("secondario")[3]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreTesto = Impostazioni.Tema.IGetFontColor("testo")
        dimBottoni = (20,20)
        self.__myImgbBottoneModifica.ChangeImage(Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_MODIFICA_PAG_DISPOSITIVI))
        self.__myImgbBottoneModifica.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneModifica.Show()
        self.__myImgbBottoneElimina.ChangeImage(Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneElimina.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneElimina.Show()
        self.__myImgbBottoneConfermaModifica.ChangeImage(Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI))
        self.__myImgbBottoneConfermaModifica.Resize(dimBottoni[0], dimBottoni[1], self.__mantieniProporzioniImmagine)
        self.__myImgbBottoneConfermaModifica.Show()
        self.AggiornaColori()

    def AggiornaColori(self):
        #Frame
        self.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameSupportoBottoni.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameBottoneModifica.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        self.__fFrameBottoneElimina.configure(background=self.__coloreSfondo, highlightcolor=self.__coloreBordo)
        #Canvas
        self.__cCanvasBottoneElimina.configure(background=self.__coloreSfondo)
        self.__cCanvasBottoneModifica.configure(background=self.__coloreSfondo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo, font = self.__fontTesto, foreground=self.__coloreTesto, highlightcolor=self.__coloreBordo)


    # METODI EVENTI
    def __Evidenzia(self):
        #Frame
        self.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameSupportoBottoni.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameBottoneModifica.configure(background=self.__coloreSfondoEvidenziato)
        self.__fFrameBottoneElimina.configure(background=self.__coloreSfondoEvidenziato)
        #Canvas
        self.__cCanvasBottoneElimina.configure(background=self.__coloreSfondoEvidenziato)
        self.__cCanvasBottoneModifica.configure(background=self.__coloreSfondoEvidenziato)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondoEvidenziato)

    def __TogliEvidenziatura(self):
        #Frame
        self.configure(background=self.__coloreSfondo)
        self.__fFrameScrittaNome.configure(background=self.__coloreSfondo)
        self.__fFrameSupportoBottoni.configure(background=self.__coloreSfondo)
        self.__fFrameBottoneModifica.configure(background=self.__coloreSfondo)
        self.__fFrameBottoneElimina.configure(background=self.__coloreSfondo)
        #Canvas
        self.__cCanvasBottoneElimina.configure(background=self.__coloreSfondo)
        self.__cCanvasBottoneModifica.configure(background=self.__coloreSfondo)
        #Labels
        self.__lScrittaNome.configure(background=self.__coloreSfondo)

        
    def __CursorEntered(self, tkEvent = None):
        self.__Evidenzia()
        
    def __CursorExited(self, tkEvent = None):
        self.__TogliEvidenziatura()

    def myBind(self, evento : str, funzione):

        #Frame principali
        self.bind(evento, funzione)
        self.__fFrameMostraAttributi.bind(evento, funzione)
        
        #Frame scritte
        self.__fFrameScrittaNome.bind(evento, funzione)

        #Scritte
        self.__lScrittaNome.bind(evento, funzione)
        self.__myBarraInserimentoNome.myBind(evento, funzione)

        #Frame bottoni
        self.__fFrameSupportoBottoni.bind(evento, funzione)
        self.__fFrameBottoneElimina.bind(evento, funzione)
        self.__fFrameBottoneModifica.bind(evento, funzione)
        self.__fFrameBottoneConfermaModifica.bind(evento, funzione)
        self.__fFrameModificaAttributi.bind(evento, funzione)
        self.__fFrameSupportoBottoneConfermaModifica.bind(evento, funzione)

        #Canvas
        self.__cCanvasBottoneElimina.bind(evento, funzione)
        self.__cCanvasBottoneModifica.bind(evento, funzione)



    # METODI DI SPECIFICA LAYOUTd