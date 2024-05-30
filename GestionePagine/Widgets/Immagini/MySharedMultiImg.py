from GestionePagine.Widgets.Immagini.MyMultiImage import *

class MySharedMultiImg:

    # COSTRUTTORE
    def __init__(self, pathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):

        #Carico immagine e immagine 
        self.__pathKeys = pathsDict
        #Lista id istanze
        self.__numOf_immaginiShared = 0
        self.__lastInstanceId_listInt = []
        #Dizionari immagini
        self.__images_strToImgDict = {}
        self.__resizedImages_strToImgDict = {}
        self.__imagesTk_strToImgDict = {}
        for pathKey in pathsDict:
            self.__images_strToImgDict[pathKey] = Image.open(pathsDict[pathKey]).resize(qualitaImmagineRichiesta)
            self.__resizedImages_strToImgDict[pathKey] = Image.open(pathsDict[pathKey]).resize(qualitaImmagineRichiesta)
            self.__imagesTk_strToImgDict[pathKey] = ImageTk.PhotoImage(self.__resizedImages_strToImgDict[pathKey])

    
    def Show(self, canvas : tk.Canvas, pathKey : str, instanceId : int = None) -> int:
        #Controllo che lidIstanza esista
        if instanceId == None: 
            instanceId = self.__numOf_immaginiShared
            self.__numOf_immaginiShared += 1
            self.__lastInstanceId_listInt.append(canvas.create_image(0, 0, image = self.__imagesTk_strToImgDict[pathKey], anchor = "nw"))
            return instanceId
        else:
            #Distruggo e ricreo listanza dellimmagine
            previousInstanceId = self.__lastInstanceId_listInt[instanceId] 
            self.__lastInstanceId_listInt[instanceId] = canvas.create_image(0, 0, image = self.__imagesTk_strToImgDict[pathKey], anchor = "nw")
            self.Hide(canvas = canvas, instanceId = previousInstanceId)
            return instanceId
    
    def Hide(self, canvas : tk.Canvas, instanceId : int):
        try: canvas.delete(instanceId)
        except: pass

    def ResizeAll(self, width : int, height : int):
        for pathKey in self.__pathKeys:
            self.__resizedImages_strToImgDict[pathKey] = self.__images_strToImgDict[pathKey].resize((width, height))
            self.__imagesTk_strToImgDict[pathKey] = ImageTk.PhotoImage(self.__resizedImages_strToImgDict[pathKey])

    def ChangePaths(self, newPathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        #Per ogni immagine resizo
        for pathKey in newPathsDict:
            self.__images_strToImgDict[pathKey] = Image.open(newPathsDict[pathKey]).resize(qualitaImmagineRichiesta)
            self.__resizedImages_strToImgDict[pathKey] = Image.open(newPathsDict[pathKey]).resize(qualitaImmagineRichiesta)
            self.__imagesTk_strToImgDict[pathKey] = ImageTk.PhotoImage(self.__resizedImages_strToImgDict[pathKey])

