from GestionePagine.Widgets.Immagini.MyImageButton import *

class MyMultiImage:

    # COSTRUTTORE
    def __init__(self, canvas : tk.Canvas, pathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        self.__key_imgShown = None
        self.__parentCanvas = canvas
        #Creo tutte le immagini
        self.__imagesTk_strToImgDict = {} #Dizionario
        for key in pathsDict:
            self.__imagesTk_strToImgDict[key] = MyImageTk(canvas = canvas, path = pathsDict[key], qualitaImmagineRichiesta = qualitaImmagineRichiesta) 

    # METODI SET 
    def ResizeAll(self, width : int, height : int):
        for key in self.__imagesTk_strToImgDict:
            self.__imagesTk_strToImgDict[key].Resize(width, height) 
        self.ShowCurrentImg()

    def ChangePaths(self, newPathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        for key in newPathsDict:
            try:
                self.__imagesTk_strToImgDict[key].ChangeImage(newPathsDict[key])
            except:
                self.__imagesTk_strToImgDict[key] = ImageTk(canvas = self.__parentCanvas, path = newPathsDict[key], qualitaImmagineRichiesta = qualitaImmagineRichiesta)

    def ShowImg(self, imgKey : str) -> bool:
        #Se mostrata un immagine la nascondo
        self.HideCurrentImg()
        #Provo a mostrare la successiva
        try:
            self.__key_imgShown = imgKey
            self.__imagesTk_strToImgDict[imgKey].Show()
            return True
        except:
            return False

    #Nascondo l'immagine
    def HideCurrentImg(self):
        #Se non è mostrata nessun immagine ritorno
        if self.__key_imgShown == None:
            return False
        self.__imagesTk_strToImgDict[self.__key_imgShown].Hide()
        return True
    def ShowCurrentImg(self):
        #Nascondo l'immagine precedente
        self.HideCurrentImg()
        #Se non è mostrata nessun immagine ritorno
        if self.__key_imgShown == None:
            return False
        self.__imagesTk_strToImgDict[self.__key_imgShown].Show()
        return True