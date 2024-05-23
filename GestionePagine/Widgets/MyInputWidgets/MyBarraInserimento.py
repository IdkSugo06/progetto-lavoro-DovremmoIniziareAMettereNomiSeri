from Utility.FUtility import * 

#Barra di inserimento personalizzata, contiene metodi per leggere e scrivere in qualsiasi momento
#Classe derivata da una classe di tkInter
class MyBarraInserimento(ttk.Entry):
    def __init__(self, master, text : str = "", coloreSelezione :str = "#000000", coloreDeselezione : str = "#969696", looseContentOnFirstFocus : bool = False, hover : bool = True):
        #Salvo i colori selezione e deselezione passati come parametro
        self.coloreSelezione = coloreSelezione
        self.coloreDeselezione = coloreDeselezione
        self.alreadyFocussedOnce = not looseContentOnFirstFocus
        self.hover = hover

        #Creo una variabile di supporto per settare e leggere il valore della barra di ricerca
        self.barraInserimento_str = tk.StringVar() 
        self.barraInserimento_str.set(text)

        #Inizializzo la barra di ricerca
        super().__init__(master = master,
                        text = text, 
                        textvariable = self.barraInserimento_str, 
                        foreground = self.coloreDeselezione
                        )
        
        #Associo gli eventi focus in e out con i metodi
        self.bind('<FocusIn>', lambda event, _self = self  : MyBarraInserimento.BarraRicercaSelezionata(_self, event))
        self.bind('<FocusOut>', lambda event, _self = self : MyBarraInserimento.BarraRicercaDeselezionata(_self, event))

        if not self.hover:
            self.configure(foreground = self.coloreSelezione)

    
    # GETTER E SETTER
    def Get(self):
        return self.barraInserimento_str.get()
    
    def Set(self, text : str):
        self.barraInserimento_str.set(text)

    def LoseContentOnNextFocus(self, _bool : bool):
        self.alreadyFocussedOnce = not _bool

    def Hover(self, _bool : bool):
        self.hover = _bool


    # METODI EVENTI
    def BarraRicercaSelezionata(self, event):
        if not self.alreadyFocussedOnce:
            self.barraInserimento_str.set("")

        if self.hover:
            self.configure(foreground = self.coloreSelezione)
    
    def BarraRicercaDeselezionata(self, event):
        if self.hover:
            self.configure(foreground = self.coloreDeselezione)

    def myBind(self, evento : str, funzione):
        self.bind(evento, funzione)