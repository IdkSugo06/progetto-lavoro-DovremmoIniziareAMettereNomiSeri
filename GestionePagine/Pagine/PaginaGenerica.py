import Utility.Impostazioni.Impostazioni as Impostazioni
from Utility.FUtility import *
from GestionePagine.Widgets.Widgets import *

#PaginaGenerica sarà una classe padre per derivare
#le pagine con un ruolo specifico in seguito
class PaginaGenerica():
    #Creo un dizionario per facilitare e generalizzare l'id delle pagine
    numOf_pagineEsistenti = 0
    PagNameToId_dict = dict()
    PagIdToName_dict = dict()

    def __init__(self, _istanzaGestorePagine):
        #Salviamo una referenza al gestorePagine (singleton) 
        self.gestorePagine = _istanzaGestorePagine
    
    # METODI STATICI
    @staticmethod
    def AggiungiPagina(nomePagina : str) -> int:
        PaginaGenerica.PagNameToId_dict[nomePagina] = PaginaGenerica.numOf_pagineEsistenti
        PaginaGenerica.PagIdToName_dict[PaginaGenerica.numOf_pagineEsistenti] = nomePagina
        PaginaGenerica.numOf_pagineEsistenti += 1
        return (PaginaGenerica.numOf_pagineEsistenti - 1)
        
    @staticmethod
    def GetIdPagina(nomePagina : str):
        try:
            return PaginaGenerica.PagNameToId_dict[nomePagina]
        except:
            LOG.log("Errore nella chiamata PaginaGenerica.GetIdPagina, nomePagina non trovato : " + str(nomePagina), LOG_ERROR)
            return 0
        
    @staticmethod
    def GetNomePagina(idPagina : str):
        try:
            return PaginaGenerica.PagIdToName_dict[idPagina]
        except:
            LOG.log("Errore nella chiamata PaginaGenerica.GetNomePagina, idPagina non trovato : " + str(idPagina), LOG_ERROR)
            return PAGINA_DEFAULT

    # METODI VIRTUALI (verrà eseguito l'override)
    def CaricaPagina(self, args): #Metodo virtuale
        return
    def NascondiPagina(self): #Metodo virtuale
        return
    def MostraPagina(self):
        return
    def UpdatePagina(self, deltaTime): #Metodo virtuale
        return
    def AggiornaColoriTema(self):
        return
    def CambioDimFrame(self):
        return