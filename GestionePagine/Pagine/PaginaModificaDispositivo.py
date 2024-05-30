from GestionePagine.GestorePagine import *
from GestionePagine.Widgets.Widgets import *

#PaginaRegistrazione sarà una delle molte pagine derivate da PaginaGenerica
#Verranno salvate e caricate quando necessario in una lista nel gestorePagine
#(useremo il polimorfismo)
class PaginaModificaDispositivo(PaginaGenerica): #Singleton
    #Creo un'istanza statica
    __paginaRegistrazione = None

    # INTERFACCE
    @staticmethod
    def Init(): #Inizializzo l'istanza statica (il costruttore aggiungerà l'istanza statica alla lista nel gestorePagine)
        #Se l'istanza non è ancora stata creata, la creo
        if PaginaModificaDispositivo.__paginaRegistrazione == None:
            PaginaModificaDispositivo.__paginaRegistrazione = PaginaModificaDispositivo()
    @staticmethod
    def GetPaginaRegistrazione(): #Metodo per accedere all'istanza statica
        #Se l'istanza non è ancora stata creata, la creo
        if PaginaModificaDispositivo.__paginaRegistrazione == None:
            PaginaModificaDispositivo.__paginaRegistrazione = PaginaModificaDispositivo()
        #Ritorno l'istanza statica
        return PaginaModificaDispositivo.__paginaRegistrazione 
    
    # COSTRUTTORE
    def __init__(self): #Definisco il layout e aggiungo la pagina al gestorePagine
        #Aggiungo poi la pagina al gestorePagine
        PaginaGenerica.AggiungiPagina(NOME_INTERNO_PAGINA_MODIFICA_DISPOSITIVO)
        GestorePagine.IAddPagina(self)

        #Attributi colore e font
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__coloreSfondoInterno = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreFontTesto = Impostazioni.Tema.IGetFontColor("testo")
        self.__fontTitolo = Impostazioni.Tema.IGetFont("titolo", dimensione = 32)
        self.__coloreFontTitolo = Impostazioni.Tema.IGetFontColor("titolo")


        self.__idDispositivoAssociato = 0

        #Definisco il layout della pagina
        #Creo il frame principale
        self.__fFramePrincipale = tk.Frame(master = GestorePagine.IGetFramePagina(), background = self.__coloreSfondo)
        self.__fFramePrincipale.columnconfigure(0, weight = 1)
        self.__fFramePrincipale.columnconfigure(1, weight = 10)
        self.__fFramePrincipale.columnconfigure(2, weight = 1)
        self.__fFramePrincipale.rowconfigure(0, weight = 2)
        self.__fFramePrincipale.rowconfigure(1, weight = 16)
        self.__fFramePrincipale.rowconfigure(2, weight = 2)
        self.__fFramePrincipale.rowconfigure(3, weight = 2)
        self.__fFramePrincipale.rowconfigure(4, weight = 3)
        self.__fFramePrincipale.grid_propagate(False)

        #Frame di supporto pulsante aggiunta dispositivo
        self.__fFrameSupportoPulsanteAggiungiDispositivo = tk.Frame(master = self.__fFramePrincipale,  background = self.__coloreSfondo)
        self.__fFrameSupportoPulsanteAggiungiDispositivo.rowconfigure(0, weight=1)
        self.__fFrameSupportoPulsanteAggiungiDispositivo.columnconfigure(0, weight=1)
        self.__fFrameSupportoPulsanteAggiungiDispositivo.grid(row = 3, column = 1, sticky="nsew")
        self.__fFrameSupportoPulsanteAggiungiDispositivo.grid_propagate(False)
        #Bottone aggiunta dispositivo
        self.__bPulsanteAggiungiDispositivo = ctk.CTkButton(master = self.__fFrameSupportoPulsanteAggiungiDispositivo,
                                                         command = self.__TentaModificaDispositivo,
                                                         text = "Aggiungi", 
                                                         fg_color = self.__coloreSfondoInterno,
                                                         font = Impostazioni.Tema.IGetFont_ctkFormat("testo"),
                                                         text_color = self.__coloreFontTesto,
                                                         hover_color = Impostazioni.Tema.IGetColoriSfondo("terziario")[1],
                                                         border_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[3],
                                                         border_width = 1,
                                                         corner_radius = 10
                                                        )
        self.__bPulsanteAggiungiDispositivo.grid(row = 0, column = 0, sticky = "nsew")
        #Creo frame scheda aggiunta dispositivo
        self.__fFrameSchedaModificaDispositivo = tk.Frame(master = self.__fFramePrincipale, background=self.__coloreSfondoInterno, highlightbackground=self.__coloreBordo, highlightthickness=1)
        self.__fFrameSchedaModificaDispositivo.grid(row = 1, column = 1, sticky = "nsew")
        self.__fFrameSchedaModificaDispositivo.columnconfigure(0, weight = 2)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(1, weight = 1)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(2, weight = 6)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(3, weight = 2)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(4, weight = 24)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(5, weight = 1)
        self.__fFrameSchedaModificaDispositivo.columnconfigure(6, weight = 2)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(0, weight = 3)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(1, weight = 2)

        self.__fFrameSchedaModificaDispositivo.rowconfigure(2, weight = 2)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(3, weight = 1)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(4, weight = 2)

        self.__fFrameSchedaModificaDispositivo.rowconfigure(5, weight = 2)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(6, weight = 1)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(7, weight = 2)

        self.__fFrameSchedaModificaDispositivo.rowconfigure(8, weight = 2)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(9, weight = 1)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(10, weight = 2)
        
        self.__fFrameSchedaModificaDispositivo.rowconfigure(11, weight = 2)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(12, weight = 1)
        self.__fFrameSchedaModificaDispositivo.rowconfigure(13, weight = 5)
        self.__fFrameSchedaModificaDispositivo.grid_propagate(False)


        # FRAME LOGO
        self.__fFrameLogo = tk.Frame(master = self.__fFrameSchedaModificaDispositivo, background=self.__coloreSfondoInterno, highlightthickness = 0) #Creo il logo in alto a sinistra
        self.__fFrameLogo.grid(row = 0, column=1, columnspan=2, sticky="nsew")
        self.__fFrameLogo.columnconfigure(0, weight = 1)
        self.__fFrameLogo.rowconfigure(0, weight = 5)
        self.__fFrameLogo.rowconfigure(1, weight = 16)
        self.__fFrameLogo.rowconfigure(2, weight = 1)
        self.__fFrameLogo.grid_propagate(False)
        #Frame secondario LOGO
        self.__fFrameSecondarioLogo = tk.Frame(master = self.__fFrameLogo) #Creo il logo in alto a sinistra
        self.__fFrameSecondarioLogo.grid(row = 1, column=0, sticky="nsew")
        self.__fFrameSecondarioLogo.grid_propagate(False)
        # LOGO
        self.__cCanvasLogo = tk.Canvas(master = self.__fFrameSecondarioLogo) #Creo il logo in alto a sinistra
        self.__cCanvasLogo.grid(row = 0, column = 0, sticky = "nsew") 
        self.__myImgLogo = MyImageTk(self.__cCanvasLogo, Impostazioni.Tema.IGetPathTemaCorrente(PATH_IMMAGINE_LOGO))
        self.__myImgLogo.Resize(int((1/18) * Impostazioni.sistema.dimensioniFinestra[0]),
                              int((1/12) * Impostazioni.sistema.dimensioniFinestra[1]))
        self.__myImgLogo.Show()

        
        #Creo la scritta registrazione
        self.__fFrameScrittaModificaDispositivo = tk.Label(master = self.__fFrameSchedaModificaDispositivo, background=self.__coloreSfondoInterno)
        self.__fFrameScrittaModificaDispositivo.grid(row = 0, column=4, columnspan=2, sticky="nsew")
        self.__fFrameScrittaModificaDispositivo.grid_propagate(False)
        self.__lScrittaModificaDispositivo = tk.Label(master = self.__fFrameScrittaModificaDispositivo, text = "Modifica dispositivo", background=self.__coloreSfondoInterno, font = self.__fontTitolo,  foreground = self.__coloreFontTitolo)
        #self.__lScrittaModificaDispositivo.grid(row = 0, column=0, sticky="nsew")
        self.__lScrittaModificaDispositivo.pack(side = "left", fill = "both")

        #Creo la scritta name
        self.__fFrameSupportoNome = tk.Frame(master = self.__fFrameSchedaModificaDispositivo, background = self.__coloreSfondoInterno)
        self.__fFrameSupportoNome.grid(row = 2, column = 2, columnspan=3, sticky= "nsew")
        self.__fFrameSupportoNome.rowconfigure(0, weight=1)
        self.__fFrameSupportoNome.columnconfigure(0,weight=1)
        self.__fFrameSupportoNome.grid_propagate(False)
        self.__fFrameSupportoNome.pack_propagate(False)
        self.__lScrittaNome = tk.Label(master = self.__fFrameSupportoNome, text = "Nome macchina:", background=self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaNome.pack(side = "left", fill = "both")

        #Creo l'entry inserimento name
        self.__myBarraInserimentoNome = MyBarraInserimento(master = self.__fFrameSchedaModificaDispositivo, text = "Nome macchina", looseContentOnFirstFocus = False, hover = False)
        self.__myBarraInserimentoNome.grid(row = 3, column = 2, columnspan=3, sticky="nsew")

        #Creo la scritta ipHost

        self.__fFrameSupportoIpHost = tk.Frame(master = self.__fFrameSchedaModificaDispositivo, background = self.__coloreSfondoInterno)
        self.__fFrameSupportoIpHost.grid(row = 5, column = 2, columnspan=3, sticky= "nsew")
        self.__fFrameSupportoIpHost.rowconfigure(0, weight=1)
        self.__fFrameSupportoIpHost.columnconfigure(0,weight=1)
        self.__fFrameSupportoIpHost.grid_propagate(False)
        self.__fFrameSupportoIpHost.pack_propagate(False)
        self.__lScrittaIpHost = tk.Label(master = self.__fFrameSupportoIpHost, text = "Ip host:", background= self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaIpHost.pack(side = "left", fill = "both")

        #Creo l'entry inserimento ipHost
        self.__myBarraInserimentoIpHost = MyBarraInserimento(master = self.__fFrameSchedaModificaDispositivo, text = "Ip host", looseContentOnFirstFocus = False, hover = False)
        self.__myBarraInserimentoIpHost.grid(row = 6, column = 2, columnspan=3, sticky="nsew")

        #Creo la scritta porta
        self.__fFrameSupportoPorta = tk.Frame(master = self.__fFrameSchedaModificaDispositivo, background = self.__coloreSfondoInterno)
        self.__fFrameSupportoPorta.grid(row = 8, column = 2, columnspan=3, sticky= "nsew")
        self.__fFrameSupportoPorta.rowconfigure(0, weight=1)
        self.__fFrameSupportoPorta.columnconfigure(0,weight=1)
        self.__fFrameSupportoPorta.grid_propagate(False)
        self.__fFrameSupportoPorta.pack_propagate(False)
        self.__lScrittaPorta = tk.Label(master = self.__fFrameSupportoPorta, text = "Porta:", background= self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaPorta.pack(side = "left", fill = "both")

        #Creo l'entry inserimento porta
        self.__myBarraInserimentoPorta = MyBarraInserimento(master = self.__fFrameSchedaModificaDispositivo, text = "Porta", looseContentOnFirstFocus = False, hover = False)
        self.__myBarraInserimentoPorta.grid(row = 9, column = 2, columnspan=3, sticky="nsew")
        #Creo la scritta tempoTraPing
        self.__fFrameSupportoTempoTraPing = tk.Frame(master = self.__fFrameSchedaModificaDispositivo, background = self.__coloreSfondoInterno)
        self.__fFrameSupportoTempoTraPing.grid(row = 11, column = 2, columnspan=3, sticky= "nsew")
        self.__fFrameSupportoTempoTraPing.rowconfigure(0, weight=1)
        self.__fFrameSupportoTempoTraPing.columnconfigure(0,weight=1)
        self.__fFrameSupportoTempoTraPing.grid_propagate(False)
        self.__fFrameSupportoTempoTraPing.pack_propagate(False)
        self.__lScrittaTempoTraPing = tk.Label(master = self.__fFrameSupportoTempoTraPing, text = "Tempo tra ping:", background= self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaTempoTraPing.pack(side = "left", fill = "both")

        #Creo l'entry inserimento porta
        self.__myBarraInserimentoTempoTraPing = MyBarraInserimento(master = self.__fFrameSchedaModificaDispositivo, text = "Tempo tra ping", looseContentOnFirstFocus = False, hover = False)
        self.__myBarraInserimentoTempoTraPing.grid(row = 12, column = 2, columnspan=3, sticky="nsew")


    # METODI
    #Override metodo virtuale classe PaginaGenerica, visualizzo il contenuto della pagina
    def CaricaPagina(self, args = []): 
        #Mostro la pagina
        self.MostraPagina()

        #Controllo e associo idDispositivo
        if len(args) == 1:
            self.__idDispositivoAssociato = args[0]
        else: LOG.log("Pagina modifica caricata senza referenza all'id dispositivo", LOG_ERROR)


        #Reset contenuto barre registrazione
        dispositivo = GestoreDispositivi.IGetDispositivo(self.__idDispositivoAssociato)
        self.__myBarraInserimentoNome.Set(dispositivo.GetNome())
        self.__myBarraInserimentoIpHost.Set(dispositivo.GetHost())
        self.__myBarraInserimentoPorta.Set(dispositivo.GetPorta())
        self.__myBarraInserimentoTempoTraPing.Set(dispositivo.GetTempoTraPing())

    #Override metodo virtuale classe PaginaGenerica, nascondo il contenuto della pagina
    def NascondiPagina(self):
        self.__fFramePrincipale.grid_forget()
    
    def MostraPagina(self):
        self.__fFramePrincipale.grid_propagate(True) #Causes the frame to disappear after the forget and not appear anymore....
        self.__fFramePrincipale.grid(row = 0, column = 0, sticky = "nsew")
        self.__fFramePrincipale.grid_propagate(False)


    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Aggiorno i colori 
        self.__coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1]
        self.__coloreSfondoInterno = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreBordo = Impostazioni.Tema.IGetColoriSfondo("terziario")[0]
        self.__fontTesto = Impostazioni.Tema.IGetFont("testo")
        self.__coloreFontTesto = Impostazioni.Tema.IGetFontColor("testo")
        self.__fontTitolo = Impostazioni.Tema.IGetFont("titolo", dimensione = 32)
        self.__coloreFontTitolo = Impostazioni.Tema.IGetFontColor("titolo")

        #Aggiornamento colore scritte
        self.__fFrameSupportoNome.configure(background=self.__coloreSfondoInterno)
        self.__fFrameSupportoIpHost.configure(background=self.__coloreSfondoInterno)
        self.__fFrameSupportoPorta.configure(background=self.__coloreSfondoInterno)
        self.__fFrameSupportoTempoTraPing.configure(background=self.__coloreSfondoInterno)
        self.__lScrittaNome.configure(background=self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaIpHost.configure(background=self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaPorta.configure(background=self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaTempoTraPing.configure(background=self.__coloreSfondoInterno, font = self.__fontTesto, foreground = self.__coloreFontTesto)
        self.__lScrittaModificaDispositivo.configure(background=self.__coloreSfondoInterno, font = self.__fontTitolo, foreground = self.__coloreFontTitolo)

        #Frame
        self.__fFramePrincipale.configure(background = self.__coloreSfondo)
        self.__fFrameSupportoPulsanteAggiungiDispositivo.configure(background = self.__coloreSfondo)
        self.__fFrameSchedaModificaDispositivo.configure(background = self.__coloreSfondoInterno)
        self.__fFrameScrittaModificaDispositivo.configure(background = self.__coloreSfondoInterno)
        self.__fFrameLogo.configure(background = self.__coloreSfondoInterno)
        self.__fFrameSecondarioLogo.configure(background = self.__coloreSfondoInterno)
        self.__cCanvasLogo.configure(background = self.__coloreSfondoInterno)

        #Bottone aggiunta
        self.__bPulsanteAggiungiDispositivo.configure(
                                                       fg_color = self.__coloreSfondoInterno,
                                                       font = Impostazioni.Tema.IGetFont_ctkFormat("testo"),
                                                       text_color = self.__coloreFontTesto,
                                                       hover_color = Impostazioni.Tema.IGetColoriSfondo("terziario")[1],
                                                       border_color = Impostazioni.Tema.IGetColoriSfondo("secondario")[3],
                                                       border_width = 1,
                                                       corner_radius = 10
                                                    )
    
        #Aggiornamento tema barre d'inserimento
        self.__myBarraInserimentoNome.AggiornaColoriTema()
        self.__myBarraInserimentoIpHost.AggiornaColoriTema()
        self.__myBarraInserimentoPorta.AggiornaColoriTema()
        self.__myBarraInserimentoTempoTraPing.AggiornaColoriTema()
    
    # METODI EVENTI
    def __TentaModificaDispositivo(self):
        tempFloat = 1
        try:
            tempFloat = float(self.__myBarraInserimentoTempoTraPing.Get())
        except:
            self.__myBarraInserimentoTempoTraPing.Set("1")
            return
        InterfacciaGestioneDispositivi.IModificaDispositivo(self.__idDispositivoAssociato,
                                                            self.__myBarraInserimentoNome.Get(), 
                                                            self.__myBarraInserimentoIpHost.Get(), 
                                                            self.__myBarraInserimentoPorta.Get(),
                                                            tempFloat
                                                            )
        GestorePagine.ICaricaPaginaConNome(NOME_INTERNO_PAGINA_DISPOSITIVI)

#Inizializzo la pagina home
PaginaModificaDispositivo.Init()

