import Utility.Impostazioni.Impostazioni as Impostazioni
from Utility.FUtility import *

class GestoreInvioMail:

    __gestoreInvioMail = None
    
    @staticmethod
    def Init():
        if GestoreInvioMail.__gestoreInvioMail == None:
            GestoreInvioMail.__gestoreInvioMail = GestoreInvioMail()
    
    @staticmethod
    def GetGestoreMail():
        if GestoreInvioMail.__gestoreInvioMail == None:
            GestoreInvioMail.__gestoreInvioMail = GestoreInvioMail()
        return GestoreInvioMail.__gestoreInvioMail
    
    @staticmethod
    def IDecostruttore():
        if GestoreInvioMail.__gestoreInvioMail != None:
            return
        GestoreInvioMail.GetGestoreMail().__canaleCriptato.quit()
    
    @staticmethod
    def InvioMailDispositivoDisconnesso(nomeMacchina : str, host : str, porta : str):
        GestoreInvioMail.GetGestoreMail().InvioMail(f"Il dispositivo {nomeMacchina} (ip: {host}, porta: {porta}), sembra non essere raggiungibile.\n")
    
    # COSTRUTTORE
    def __init__(self):
        #Leggo le informazioni del server dal file
        self.__isAttivo = False
        try:
            with open(PATH_JSON_INVIOMAIL, 'r') as file:
                fileData = json.load(file).get("connectionInfo")
            self.__server = fileData["server"]
            self.__from_add = fileData["from"]
            self.__to_add = fileData["to"]
            self.__password = fileData["password"]
            self.__isAttivo = True if fileData["attivo"] == "True" else False
        except Exception as e:
            LOG.log("Costruttore Gestore mail fallito, unreadable. Error: " + str(e), LOG_ERROR)
            return

        if self.__isAttivo == False:
            return

        #Creo il canale di comunicazione
        try:
            self.__canaleCriptato = smtplib.SMTP(self.__server)
            self.__canaleCriptato.connect(host = self.__server, port = 587)
            self.__canaleCriptato.starttls()
            self.__canaleCriptato.login(user = self.__from_add, password = self.__password)
        except Exception as e:
            LOG.log("Costruttore Gestore mail fallito, connessione o login falliti. Error: " + str(e), LOG_ERROR)
            return
        LOG.log("Costruttore gestore mail concluso")
        
    def InvioMail(self, messaggio : str = ""):
        if self.__isAttivo == False: return
        fullMessaggio = self.__DecoratoreMail() + messaggio
        self.__canaleCriptato.sendmail(self.__from_add, self.__to_add, fullMessaggio)

    def __DecoratoreMail(self):
        return f"From:{self.__from_add}\nTo:{self.__to_add}\nSubject:[DISCONNESSIONE] dispositivo rilevata -- mail autogenerata\n\n" 

GestoreInvioMail.Init()