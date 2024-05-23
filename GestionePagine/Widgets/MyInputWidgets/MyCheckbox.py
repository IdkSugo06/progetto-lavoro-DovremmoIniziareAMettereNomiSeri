from GestionePagine.Widgets.MyInputWidgets.MyInputWidget import *


#it will occupy the whole frame
class MyCheckbox(MyInputWidget):


    # COSTRUTTORE
    def __init__(self, 
                 master : tk.Frame, 
                 command : any = lambda : None, 
                 coloreInterno : str = "#FFFFFF", 
                 coloreFlag : str = "#000000", 
                 colorePremuto : str = ""):

        #Attributi
        self.__command = command

        #Se il colore non è specificato
        if colorePremuto == "": colorePremuto = coloreInterno

        #Chiamo il costruttore del frame principale
        super().__init__(master)
        self.grid(row = 0, column=0, sticky="nsew")        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(False)
                
        #Creo una variabile associata
        self.__cbCheckbox_bool = tk.BooleanVar()
        self.__cbCheckbox_bool.set(False)
        self.__cbCheckbox = tk.Checkbutton(master = self, bg = coloreInterno, activebackground = colorePremuto, fg = coloreFlag)
        self.__cbCheckbox.grid(row = 0, column=0, sticky="nsew")

        #Bind events
        self.myBind("<<ComboboxSelected>>", self.__Event_stateChanged)

    # GETTER E SETTER
    def Set(self, value : bool):
        self.__cbCheckbox_bool.set(value)
    def Get(self) -> bool:
        return self.__cbCheckbox_bool.get()
    
    def ChangeColor(self, coloreInterno : str, coloreFlag : str = "", colorePremuto : str = ""):
        self.__cbCheckbox.configure(bg = coloreInterno, activebackground = colorePremuto, fg = coloreFlag)

        
    # METHODS
    def Disable(self):
        self.__cbCheckbox.configure(state = "disabled")

    def Enable(self):
        self.__cbCheckbox.configure(state = "enabled")


     # EVENT METHODS
    def __Event_stateChanged(self, eventTk = None):
        self.__command()

    def myBind(self, evento: str, funzione):
        self.bind(evento, funzione)
        self.__cbCheckbox.bind(evento, funzione)
     