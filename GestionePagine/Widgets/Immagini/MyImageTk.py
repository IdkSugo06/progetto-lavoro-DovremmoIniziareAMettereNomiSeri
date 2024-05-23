import Utility.Impostazioni.Impostazioni as Impostazioni
from Utility.FUtility import *

class MyImageTk:
    

    def __init__(self, canvas : tk.Canvas, path = "", qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        
        #Attributi 
        self._parentCanvas = canvas #Per il draw dell'immagine 
        self._originalImage = None #Per i resize

        #Attributi resize immagine
        self._aspectRatio = None
        self._canvasWidth = canvas.winfo_reqwidth()
        self._canvasHeight = canvas.winfo_reqheight()
        self._canvasAspectratio = self._canvasWidth / self._canvasHeight 
        self._lastFrameInstanceId = None

        #Controllo la validità della path
        if path == "":
            LOG.log("Non è satata inserita una path nel costruttore delle immagini", LOG_WARNING)
        else:

            #Cerco di accedere alla path
            try:
                #Salvo attributi riguardo l'immagine default
                self._originalImage = Image.open(path)
                self._originalImage.resize(qualitaImmagineRichiesta) #Diminuisco la qualità per non avere problemi di prestazioni
                self._aspectRatio = self._originalImage.size[0] / self._originalImage.size[1]

                #Salvo altre copie dell'immagine
                self._resizedImage = Image.open(path)
                self._resizedImageTk = ImageTk.PhotoImage(self._resizedImage)
    
                #Salvo l'instanza dell'ultimo frame per non avere artefatti durante il riscalamento
                self._lastFrameInstanceId = self._parentCanvas.create_image(self._canvasWidth/2, self._canvasHeight/2, image = self._resizedImageTk, anchor = "center")
            except:
                LOG.log("È stata rilevata una path non valida nel costruttore di un immagine: " + str(path), LOG_FATAL_ERROR)



    # METODI IMMAGINI
    def Show(self, _anchor = "center"):
        #Cancello l'id del frame precedente, creo una nuova immagine cosi da evitare il flickering durante lo show
        thisImageId = self._parentCanvas.create_image(self._canvasWidth/2, self._canvasHeight/2, image = self._resizedImageTk, anchor = _anchor)
        self._parentCanvas.delete(self._lastFrameInstanceId)
        try:
            self._parentCanvas.delete(self._lastFrameInstanceId)
        except:
            pass
        self._lastFrameInstanceId = thisImageId

    def Hide(self):
        self._parentCanvas.delete(self._lastFrameInstanceId)

    def Resize(self, width : int, height : int, rispettaProporzioni : bool = True):
        #Cambio gli attributi e salvo i nuovi
        self._canvasWidth = width
        self._canvasHeight = height
        self._canvasAspectRatio = width / height

        #Controllo l'aspect ratio e ridimensiono l'immagine in base a quello
        if rispettaProporzioni:
            if self._aspectRatio < self._canvasAspectRatio: 
                dim = [(width), (int) (width / self._aspectRatio)]
            else:
                dim = [(int) (height * self._aspectRatio), (height)]
        else:
            dim = [width, height]
            
        #Ricalcolo l'immagine e l'immagine tk
        self._resizedImage = self._originalImage.resize(dim)
        self._resizedImageTk = ImageTk.PhotoImage(self._resizedImage)


    def ChangeImage(self, newPath : int, qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default ):
        #Cerco di accedere alla path
        try:
            #Salvo attributi riguardo l'immagine default
            self._originalImage = Image.open(newPath)
            self._originalImage.resize(qualitaImmagineRichiesta) #Diminuisco la qualità per non avere problemi di prestazioni
            self._aspectRatio = self._originalImage.size[0] / self._originalImage.size[1]
            
            #Salvo altre copie dell'immagine
            self._resizedImage = Image.open(newPath)
            self._resizedImageTk = ImageTk.PhotoImage(self._resizedImage)

            #Salvo l'instanza dell'ultimo frame per non avere artefatti durante il riscalamento
            self._lastFrameInstanceId = self._parentCanvas.create_image(self._canvasWidth/2, self._canvasHeight/2, image = self._resizedImageTk, anchor = "center")
        except:
            LOG.log("È stata rilevata una path non valida nel costruttore di un immagine: " + str(newPath), LOG_ERROR)
      