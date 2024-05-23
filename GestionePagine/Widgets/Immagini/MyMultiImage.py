from GestionePagine.Widgets.Immagini.MyImageButton import *

class MyMultiImage:

    # COSTRUTTORE
    def __init__(self, canvas : tk.Canvas, pathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        self.__key_imgShown = None
        #Creo tutte le immagini
        self.__imagesTk_strToImgDict = {} #Dizionario
        for key in pathsDict:
            self.__imagesTk_strToImgDict[key] = MyImageTk(canvas = canvas, path = pathsDict[key], qualitaImmagineRichiesta = qualitaImmagineRichiesta) 

    # METODI SET 
    def ResizeAll(self, width : int, height : int):
        for key in self.__imagesTk_strToImgDict:
            self.__imagesTk_strToImgDict[key].Resize(width, height) 

    def ShowImg(self, imgKey : str) -> bool:
        #Se mostrata un immagine la nascondo
        if self.__key_imgShown != None:
            self.__imagesTk_strToImgDict[self.__key_imgShown].Hide()
        #Provo a mostrare la successiva
        try:
            self.__key_imgShown = imgKey
            self.__imagesTk_strToImgDict[imgKey].Show()
            return True
        except:
            self.HideAll()
            return False

    #Nascondo tutto
    def HideAll(self):
        #Se non è mostrata nessun immagine ritorno
        if self.__key_imgShown == None:
            return False
        self.__imagesTk_strToImgDict[self.__key_imgShown].Hide()
        return True