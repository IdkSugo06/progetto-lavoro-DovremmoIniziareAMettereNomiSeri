FATAL_ERROR_VALUE = 3

# ABSTRACT CLASS
class MyEvent:
    def __init__(self, lvlErrore : int = 0, descrizione : str = ""):
        self.lvlErrore = lvlErrore
        self.descrizione = descrizione

# GENERIC ERROR
class MyFatalError(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]):
        super().__init__(FATAL_ERROR_VALUE)
        for function in MyFatalError.functionsBound:
            function()

# THEME
class MyThemeChanged(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]):
        super().__init__()
        for function in MyThemeChanged.functionsBound:
            function()

# DEVICES
class MyDispositivoAggiunto(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple(("idDispositivo")) : any]): 
        super().__init__()
        for function in MyDispositivoAggiunto.functionsBound:
            function(args["idDispositivo"])

class MyDispositivoRimosso(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple(("idDispositivo")) : any]): 
        super().__init__()
        for function in MyDispositivoRimosso.functionsBound:
            function(args["idDispositivo"])

class MyDispositivoModificato(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple(("idDispositivo")) : any]): 
        super().__init__()
        for function in MyDispositivoModificato.functionsBound:
            function(args["idDispositivo"])

class MyStatoDispositivoCambiato(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple(("idDispositivo", "stato")) : any]): 
        super().__init__()
        for function in MyStatoDispositivoCambiato.functionsBound:
            function(args["idDispositivo"], args["stato"])               

class MyFiltroRefreshNeeded(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]): 
        super().__init__()
        for function in MyFiltroRefreshNeeded.functionsBound:
            function()  

class MyFiltroRebuildNeeded(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]): 
        super().__init__()
        for function in MyFiltroRebuildNeeded.functionsBound:
            function()    

# FILTERS
class MyFilterChanged(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple(("tipoFiltro", "codice", "args")) : any]):
        super().__init__()
        for function in MyFilterChanged.functionsBound:
            function(args["tipoFiltro", args["codice"], args["args"]])

class MyFilterRefreshed(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]):
        super().__init__()
        for function in MyFilterRefreshed.functionsBound:
            function()

class MyFilterRebuilt(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[str : any]):
        super().__init__()
        for function in MyFilterRebuilt.functionsBound:
            function()

class MyFilterElementChanged(MyEvent):
    functionsBound = []
    def __init__(self, args : dict[tuple("idElemento") : any]):
        super().__init__()
        for function in MyFilterElementChanged.functionsBound:
            function(args["idElemento"])

            

#Singleton
class MyEventHandler:
    __myEventHandler = None

    # COSTRUTTORE
    def __init__(self):
        self.fatalErrorOccurred = False
        self.errors = []
    
    # METODI
    def __throw(self, event : MyEvent):
        if event.lvlErrore > 0:
            self.errors.append(event)
            if event.lvlErrore == FATAL_ERROR_VALUE:
                self.fatalErrorOccurred = True

    # METODI INTERFACCIA
    @staticmethod
    def Init():
        if MyEventHandler.__myEventHandler == None:
            MyEventHandler.__myEventHandler = MyEventHandler()

    @staticmethod
    def GetMyEventHandler():
        if MyEventHandler.__myEventHandler == None:
            MyEventHandler.__myEventHandler = MyEventHandler()
        return MyEventHandler.__myEventHandler
    
    @staticmethod
    def Throw(eventType : type, args : dict[str : any] = None):
        MyEventHandler.__myEventHandler.__throw(eventType(args))
    @staticmethod
    def CheckFatalErrorOccurred():
        return MyEventHandler.__myEventHandler.fatalErrorOccurred
    @staticmethod
    def GetErrors():
        return MyEventHandler.__myEventHandler.errors

    @staticmethod
    def BindEvent(eventType : type, functionToBind : any): #Has to be void
        eventType.functionsBound.append(functionToBind)
        
MyEventHandler.Init()