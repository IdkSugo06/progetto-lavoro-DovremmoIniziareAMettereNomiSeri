from GestionePagine.Widgets.Immagini.MyImageTk import *

class MyImageButton(MyImageTk):
    
    def __init__(self, canvas : tk.Canvas, command, path = ""):
        super().__init__(canvas, path)
        self._parentCanvas.bind("<ButtonRelease-1>", command)