from Utility.FUtility import *


#Classe astratta per permettere di avere widget diversi a seconda delle necessita
class MyInputWidget(tk.Frame): #it will occupy the whole frame


    # COSTRUTTORE
    def __init__(self, master : tk.Frame):
        super().__init__(master = master)


    # GETTER E SETTER
    def Get(self) -> int:
        return 0
    
    def Set(self, value : any) -> int:
        return 0
    
    # METODI EVENTO
    def myBind(self, evento : str, funzione):
        return