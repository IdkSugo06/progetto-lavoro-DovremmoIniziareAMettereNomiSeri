from GestionePagine.Widgets.TabelleFolder.TabellaScorribile import *
from GestionePagine.Widgets.ElementiTabelle.FrameImpostazioniIntabellabile import *


class  TabellaImpostazioni(TabellaScorribile):

    # COSTRUTTORE
    def __init__(self, 
                 master : tk.Frame,
                 xPos : int = 0,
                 yPos : int = 0,
                 tableWidth : int = 250,
                 tableHeight : int = 250,
                 elementWidth : int = 50,
                 elementHeight : int = 50):


        #Chiamo il costruttore della classe padre
        super().__init__(
                        master = master,
                        xPos = xPos,
                        yPos = yPos,
                        tableWidth = tableWidth,
                        tableHeight = tableHeight,
                        elementWidth = elementWidth,
                        elementHeight = elementHeight,
                        coloreSfondo = Impostazioni.Tema.IGetColoriSfondo("secondario")[1],
                        coloreElementi = Impostazioni.Tema.IGetColoriSfondo("secondario")[2]
                        )
        

        # IMPOSTAZIONE SISTEMA (elementi della tabella)
        #self.__AggiungiImpostazione("SISTEMA", MyCheckbox,ProporzionePeso = 0.1,args=[None,Impostazioni.Tema.IGetColoriSfondo("secondario")[1], Impostazioni.Tema.IGetColoriSfondo("primario"),Impostazioni.Tema.IGetColoriSfondo("secondario")[0]]) 
        self.__AggiungiImpostazione(
                                    tipoImpostazione = "TEMA",
                                    tipoWidget = MyCombobox,
                                    argomentiCostruttoreWidget = {
                                                            "values" : Impostazioni.Tema.IGetKeyTemi_listFormat(),
                                                            "command" : self.__CheckBox_TemaCambiato, 
                                                            "coloreInterno" : Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                                            "coloreFont" : Impostazioni.Tema.IGetFontColor("testo"),
                                                            "coloreSelezione" : Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
                                                            },
                                    proporzionePeso = 0.15
                                    )
        
        self.__AggiungiImpostazione(
                                    tipoImpostazione = "FPS", 
                                    tipoWidget = MyCombobox, 
                                    argomentiCostruttoreWidget = {
                                                            "values" : ["50","30","10"],
                                                            "command" : self.__CheckBox_FPSCambiato,
                                                            "coloreInterno" : Impostazioni.Tema.IGetColoriSfondo("secondario")[2],
                                                            "coloreFont" : Impostazioni.Tema.IGetFontColor("testo"),
                                                            "coloreSelezione" : Impostazioni.Tema.IGetColoriSfondo("terziario")[1]
                                                            },
                                    proporzionePeso = 0.15
                                    )
        

    # ADD IMPOSTAZIONE
    def __AggiungiImpostazione(self, tipoImpostazione : str, tipoWidget : object, argomentiCostruttoreWidget : dict[str : any], proporzionePeso : float):
        self.AggiungiElemento(FrameImpostazioniIntabellabile(tipoWidget = tipoWidget,
                                                             proporzionePeso = proporzionePeso,
                                                             argomentiCostruttoreWidget = argomentiCostruttoreWidget,
                                                             tipoImpostazione = tipoImpostazione, 
                                                             master = self, x = 0, 
                                                             y = self._numOf_elementiIntabellabili * self.dimensioniElemento[1], 
                                                             width = self.dimensioniElemento[0], 
                                                             height = self.dimensioniElemento[1],
                                                            ))  


    # METODI UPDATE FRAME
    def Update(self, deltaTime : float = 0):
        return
        for elementoIntabellabile in self._elementiIntabellabili:
            elementoIntabellabile.Update(deltaTime)


    # METODI EVENTO
    def __CheckBox_TemaCambiato(self):
        Impostazioni.Tema.IImpostaTemaAttuale(self._elementiIntabellabili[0].GetWidget().Get())

    def __CheckBox_FPSCambiato(self):
        Impostazioni.Tema.IImpostaTemaAttuale(self._elementiIntabellabili[0].GetWidget().Get())
