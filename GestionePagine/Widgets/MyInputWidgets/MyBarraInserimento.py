from Utility.FUtility import * 
import Utility.Impostazioni.Impostazioni as Impostazioni

#Barra di inserimento personalizzata, contiene metodi per leggere e scrivere in qualsiasi momento
#Classe derivata da una classe di tkInter
class MyBarraInserimento(ttk.Entry):
    def __init__(self, master, text : str = "", looseContentOnFirstFocus : bool = False, hover : bool = True):
        #Salvo i colori selezione e deselezione passati come parametro
        self.coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
        self.coloreSfondoDisabilitato  = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.font = Impostazioni.Tema.IGetFont("testo")
        self.coloreFont = "#555555"
        self.coloreFontDisabilitato = "#AAAAAA"
        #self.coloreFont = Impostazioni.Tema.IGetFontColor("testo")
        #self.coloreFontDisabilitato = Impostazioni.Tema.IGetFontColor("testoDisabilitato")

        self.alreadyFocussedOnce = not looseContentOnFirstFocus
        self.hover = hover

        #Creo una variabile di supporto per settare e leggere il valore della barra di ricerca
        self.barraInserimento_str = tk.StringVar() 
        self.barraInserimento_str.set(text)

        #Inizializzo la barra di ricerca
        super().__init__(master = master,
                        textvariable = self.barraInserimento_str, 
                        foreground = self.coloreFontDisabilitato,
                        font = self.font,
                        background = self.coloreSfondo
                        )
        
        #Associo gli eventi focus in e out con i metodi
        self.bind('<FocusIn>', lambda event, _self = self  : MyBarraInserimento.BarraRicercaSelezionata(_self, event))
        self.bind('<FocusOut>', lambda event, _self = self : MyBarraInserimento.BarraRicercaDeselezionata(_self, event))

        if not self.hover:
            self.configure(foreground = self.coloreSfondo)

    
    # GETTER E SETTER
    def Get(self):
        return self.barraInserimento_str.get()
    
    def Set(self, text : str):
        self.barraInserimento_str.set(text)

    def LoseContentOnNextFocus(self, _bool : bool):
        self.alreadyFocussedOnce = not _bool

    def Hover(self, _bool : bool):
        self.hover = _bool


    # METODI PERSONALIZZAZIONE 
    def AggiornaColoriTema(self):
        #Aggiorno gli attributi dei colori
        self.coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
        self.coloreSfondoDisabilitato  = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.font = Impostazioni.Tema.IGetFont("testo")
        self.coloreFont = "#555555"
        self.coloreFontDisabilitato = "#AAAAAA"
        #self.coloreFont = Impostazioni.Tema.IGetFontColor("testo")
        #self.coloreFontDisabilitato = Impostazioni.Tema.IGetFontColor("testoDisabilitato")
        #Configuro la barra
        self.configure(foreground = self.coloreFontDisabilitato, font = self.font, background = self.coloreSfondo)


    # METODI EVENTI
    def BarraRicercaSelezionata(self, event):
        if not self.alreadyFocussedOnce:
            self.barraInserimento_str.set("")

        if self.hover:
            self.configure(foreground = self.coloreFont, background = self.coloreSfondo)
    
    def BarraRicercaDeselezionata(self, event):
        if self.hover:
            self.configure(foreground = self.coloreFontDisabilitato, background = self.coloreSfondoDisabilitato)

    def myBind(self, evento : str, funzione):
        self.bind(evento, funzione)