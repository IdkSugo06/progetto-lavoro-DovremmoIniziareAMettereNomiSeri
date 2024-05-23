FATAL_ERROR_VALUE = 3

class MyEvent:
    def __init__(self, lvlErrore : int = 0, descrizione : str = ""):
        self.lvlErrore = lvlErrore
        self.descrizione = descrizione

class MyFatalError(MyEvent):
    functionsBound = []
    def __init__(self):
        super().__init__(FATAL_ERROR_VALUE)
        for function in MyFatalError.functionsBound:
            function()

class MyThemeChanged(MyEvent):
    functionsBound = []
    def __init__(self):
        super().__init__()
        for function in MyThemeChanged.functionsBound:
            function()
    

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
    def Throw(eventType : type):
        MyEventHandler.__myEventHandler.__throw(eventType())
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