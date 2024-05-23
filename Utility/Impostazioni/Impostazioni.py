import Utility.Impostazioni.Sistema as sistema 
import Utility.Impostazioni.Personalizzazioni as personalizzazioni 
from Utility.Impostazioni.Tema import *

def IGetDeltaMousePos():
        mousePosFrameCorrente = sistema.mousePosFramePrecedente
        mousePosFramePrecedente = sistema.mousePosFrameCorrente
        return [(mousePosFrameCorrente[0] - mousePosFramePrecedente[0]), (mousePosFrameCorrente[1] - mousePosFramePrecedente[1])]

def IGetMouseVelocity():
        deltaTime = sistema.tempoLastUpdate
        deltaMousePos = IGetDeltaMousePos()
        return [deltaMousePos[0] / deltaTime, deltaMousePos[1] / deltaTime]

def IUpdate(newMousePosx : float, newMousePosy : float):
        #Aggiorno infoConfig
        if sistema.infoConfigCalled[1] == True: #Se è vero, era vero e adesso è falso fino a nuovo update
            sistema.infoConfigCalled[0] = True
            sistema.infoConfigCalled[1] = False
        else:
            sistema.infoConfigCalled[0] = False
        #Aggiorno deltaTime
        sistema.tempoLastUpdate = sistema.cronometro.GetTimeFromCheckpoint()
        sistema.cronometro.SetCheckpoint()
        #Aggiorno posizione mouse
        sistema.mousePosFramePrecedente = sistema.mousePosFrameCorrente
        sistema.mousePosFrameCorrente = [newMousePosx, newMousePosy]