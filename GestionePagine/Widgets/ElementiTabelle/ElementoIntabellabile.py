import Utility.Impostazioni.Impostazioni as Impostazioni
from Utility.FUtility import *
from GestionePagine.GestorePagine import * 


#Classe "astratta", verrà utilizzata per generare tabelle con frame semplici
class ElementoIntabellabile(tk.Frame): #Verrà posizionato col metodo place

    def __init__(self, 
                 master, 
                 x : int = 0, 
                 y : int = 0,
                 width : int = 250, 
                 height : int = 50,
                 isShown : bool = True,
                 colore : str = "#000000",
                 coloreBordo : str = "#000000",
                 spessoreBordo : int  = 0):
        
        # Attributi
        self._posizione = [x, y]
        self._dimensioni = [width, height]

        super().__init__(master = master, 
                         width = width,
                         height = height, 
                         bg = colore,
                         highlightbackground = coloreBordo,
                         highlightthickness = spessoreBordo)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(False)

        # Mostra 
        if (isShown == True): 
            self.Show()
        

    #Metodi "astratti"
    def SetPos(self, x : int, y : int):
        self._posizione[0] = x
        self._posizione[1] = y

    def SetDim(self, width : int, height : int):
        self._dimensioni[0] = width
        self._dimensioni[1] = height

    def SetColore(self, coloreElemento : str, coloreBordo : str):
        self.configure(background=coloreElemento, highlightcolor=coloreBordo)
    
    def AggiornaAttributiElemento(self, any : any): #Astratto
        return
    
    def RefreshAttributiElemento(self): #Astratta
        pass

    def Hide(self):
        self.place_forget()

    def Show(self):
        self.place(x = self._posizione[0], y = self._posizione[1], width= self._dimensioni[0], height= self._dimensioni[1])

    def CambioColore(self, coloreElemento : str, coloreBordoElemento : str):
        return
    
    def myDeconstructor(self):
        self.place_forget()
        
    def myBind(self, evento : str, funzione):
        self.bind(evento, funzione)


