from GestionePagine.Widgets.Immagini.MySharedMultiImg import *

class MySharedMultiImgButton(MySharedMultiImg):

    def __init__(self, pathsDict : dict[str : str], qualitaImmagineRichiesta : tuple[int] = Impostazioni.personalizzazioni.qualita_immagini_default):
        super().__init__(pathsDict = pathsDict, qualitaImmagineRichiesta = qualitaImmagineRichiesta)

    
    def myBind(self, canvas : tk.Canvas, evento : str, command : any):
        canvas.bind(evento, command)