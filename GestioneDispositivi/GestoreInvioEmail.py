import Utility.Impostazioni.Impostazioni as Impostazioni
from Utility.FUtility import *

class GestoreInvioMail:

    __gestoreInvioMail = None
    
    @staticmethod
    def Init():
        if GestoreInvioMail.__gestoreInvioMail == None:
            GestoreInvioMail.__gestoreInvioMail = GestoreInvioMail()
        return GestoreInvioMail.__gestoreInvioMail
    
    @staticmethod
    def IDecostruttore():
        if GestoreInvioMail.__gestoreInvioMail != None:
            return
            GestoreInvioMail.__gestoreInvioMail.__canaleCriptato.quit()
    
    @staticmethod
    def InvioMail(mittente : str, destinatario : str, messaggio : str = ""):
        return
    
    # COSTRUTTORE
    def __init__(self):
        return
        try:
            self.__canaleCriptato = smtplib.SMTP("smtp.mail.yahoo.com", 587)
            self.__canaleCriptato.set_debuglevel(1)
            self.__canaleCriptato.login("provaMailPytohn@yahoo.com", "PMP_0101!")
        except Exception as e:
            print(e)

GestoreInvioMail.Init()