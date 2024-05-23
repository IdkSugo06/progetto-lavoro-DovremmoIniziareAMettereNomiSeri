from GestionePagine.Widgets.MyInputWidgets.MyInputWidget import *
import Utility.Impostazioni.Impostazioni as Impostazioni

class MySlider(MyInputWidget):


    def __init__(self, master : tk.Frame, width : int, height : int):
        
        #Attributi
        altezzaBarra = 10
        grandezzaTrascinatore = int(8)
        rapportiTrascinatore = 3
        self.__barriereScorrimentoX = (grandezzaTrascinatore//2, width - grandezzaTrascinatore//2)
        self.__scorrimentoY = height//2
        self.__isBeingDragged = False
        self.__posXTrascinatore = 0
        self.__dimensioni = (width, height)
        
        #Chiamo il costruttore della classe padre
        super().__init__(master = master)


        # FRAME PRINCIPALE
        self.place(x = 0, y = 0, width=width, height=height, anchor="nw")
        self.grid_propagate(False)


        # FRAME BARRA PRINCIPALE
        self.__fFrameBarraPrincipale = tk.Frame(master=self, bg = "blue")
        self.__fFrameBarraPrincipale.place(x = width//2, y = height//2, width= width - grandezzaTrascinatore, height=altezzaBarra, anchor="center")
        self.__fFrameBarraPrincipale.rowconfigure(0, weight=1)
        self.__fFrameBarraPrincipale.columnconfigure(0, weight=1)
        self.__fFrameBarraPrincipale.grid_propagate(False)
        # BARRA PRINCIPALE
        self.__fBarraPincipale = ctk.CTkFrame(master = self.__fFrameBarraPrincipale, corner_radius = 10, fg_color="#202020")
        self.__fBarraPincipale.grid(row = 0, column = 0, sticky = "nsew")
        # BARRA SECONDARIA
        self.__fBarraSecondaria = ctk.CTkFrame(master = self.__fFrameBarraPrincipale, corner_radius = 10, fg_color="#1515DD")

        # TRASCINATORE
        self.__fTrascinatore = ctk.CTkFrame(master = self, width = grandezzaTrascinatore, height = grandezzaTrascinatore * rapportiTrascinatore, corner_radius = grandezzaTrascinatore/2,  fg_color="#5555FF")
        self.__fTrascinatore.place(x = self.__barriereScorrimentoX[0], y = self.__scorrimentoY, anchor = "center")


        # BINDO GLI EVENTI
        self.__fTrascinatore.bind("<Button-1>", self.__Event_pressed)
        self.__fTrascinatore.bind("<ButtonRelease-1>", self.__Event_released)


    # AGGIORNAMENTO
    def Update(self, deltaTime):
        if self.__isBeingDragged:

            #Aggiorno la posizione e controllo sia compresa tra i margini
            self.__posXTrascinatore -= Impostazioni.IGetDeltaMousePos()[0]
            self.__posXTrascinatore = min(self.__posXTrascinatore, self.__barriereScorrimentoX[1])
            self.__posXTrascinatore = max(self.__posXTrascinatore, self.__barriereScorrimentoX[0])
            self.__fTrascinatore.place(x = self.__posXTrascinatore, y = self.__scorrimentoY)

            #Aggiorno la barra
            self.__fBarraSecondaria.configure(width = self.__posXTrascinatore, height = self.__dimensioni[1])
            self.__fBarraSecondaria.place(x = self.__posXTrascinatore//2, y = self.__scorrimentoY, anchor = "center")


            

    # GETTER E SETTER
    def Get(self) -> float: #Ritorna un float compreso tra 0 e 1
        return float(self.__posXTrascinatore / self.__dimensioni[1])
    def Set(self, value : float): #value deve essere compreso tra 0 e 1
        self.__posXTrascinatore = self.__dimensioni[1] * value
        self.__fTrascinatore.place(x = self.__posXTrascinatore, y = self.__scorrimentoY)
        self.__fBarraSecondaria.configure( width = self.__posXTrascinatore, height = self.__dimensioni[1], anchor = "center")
        


    # METODI EVENTI
    def __Event_pressed(self, eventTk = None):
        self.__isBeingDragged = True
        self.__fTrascinatore.configure(fg_color="#AAAAAA")

    def __Event_released(self, eventTk = None):
        self.__isBeingDragged = False
        self.__fTrascinatore.configure(fg_color="#353535")


    def myBind(self, evento: str, funzione):
        self.bind(evento, funzione)