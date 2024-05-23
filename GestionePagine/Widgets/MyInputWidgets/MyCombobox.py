from GestionePagine.Widgets.MyInputWidgets.MyInputWidget import *


#it will occupy the whole frame
class MyCombobox(MyInputWidget):

    @staticmethod
    def Init(args: dict): #Il dizionario dev'essere completo
        return MyCombobox(master = args["master"],
                           values = args["values"], 
                           command = args["command"])

    # COSTRUTTORE
    def __init__(self, master : tk.Frame,
                 values : list[str] = (),
                 command : any = lambda : None     #command dev'essere void
                ):

        #Attributi
        self.__values = values
        self.__command = command

        #Colori
        self.__coloreInterno = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreFont =  Impostazioni.Tema.IGetFontColor("testo")
        self.__coloreSelezione = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]

        #Se values è vuoto
        if len(self.__values) == 0:
            self.__values = ("")

        #Chiamo il costruttore del frame principale
        super().__init__(master)
        self.grid(row = 0, column=0, sticky="nsew")        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(False)
                
        #Creo una variabile associata
        self.__cbCombobox_str = tk.StringVar()
        self.__cbCombobox_str.set(self.__values[0])
        self.__cbCombobox = ttk.Combobox(master = self,
                                         textvariable = self.__cbCombobox_str,
                                         state = 'readonly',
                                         foreground = "#000000",
                                         background = self.__coloreInterno)
        self.__cbCombobox.option_add("*TCombobox*Listbox*Foreground", self.__coloreFont)
        self.__cbCombobox.option_add("*TCombobox*Listbox*Background", self.__coloreInterno)

        self.__cbCombobox.grid(row=0,column=0,sticky="nsew")
        self.__cbCombobox["values"] = self.__values
        self.__cbCombobox.set(self.__values[0])

        #Bind events
        self.myBind("<<ComboboxSelected>>", self.__Event_stateChanged)



    # GETTER E SETTER
    def Set(self, value : any):
        self.__cbCombobox.set(value)
    def Get(self):
        return self.__cbCombobox_str.get()
    
    def ChangeColor(self, coloreInterno : str, coloreFlag : str = "", colorePremuto : str = ""):
        self.__cbCheckbox.configure(bg = coloreInterno, activebackground = colorePremuto, fg = coloreFlag)



    # METHODS
    def Disable(self):
        self.__cbCombobox["state"] = "readonly"

    def Enable(self):
        self.__cbCombobox["state"] = "normal"        
    

    
    # METODI PERSONALIZZAZIONE
    def AggiornaColoriTema(self):
        #Colori
        self.__coloreInterno = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
        self.__coloreFont =  Impostazioni.Tema.IGetFontColor("testo")
        self.__coloreSelezione = Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
        #Combobox
        self.__cbCombobox.configure(foreground = "#000000", background = self.__coloreInterno)
        self.__cbCombobox.option_add("*TCombobox*Listbox*Foreground", self.__coloreFont)
        self.__cbCombobox.option_add("*TCombobox*Listbox*Background", self.__coloreInterno)
        



    # EVENT METHODS
    def __Event_stateChanged(self, eventTk = None):
        self.__command()

    def myBind(self, evento: str, funzione):
        self.bind(evento, funzione)
        self.__cbCombobox.bind(evento, funzione)

    def SetCommand(self, function: any):
        self.__command = function