import os
# PATH DATABASE



# PATH IMMAGINI UTILITY
PATH_CARTELLA_CORRENTE = os.getcwd()
PATH_IMMAGINI  = os.path.join(PATH_CARTELLA_CORRENTE, "Immagini")
PATH_IMMAGINE_LOGO = os.path.join(PATH_IMMAGINI, "ImmagineLogo.png")
PATH_IMG_STATUS_ONLINE_PAG_DASHBOARD = os.path.join(PATH_IMMAGINI, "ImmagineDashboardStatusOnline.png")
PATH_IMG_STATUS_OFFLINE_PAG_DASHBOARD = os.path.join(PATH_IMMAGINI, "ImmagineDashboardStatusOffline.png")
PATH_IMG_BOTTONE_MODIFICA_PAG_DISPOSITIVI = os.path.join(PATH_IMMAGINI, "ImmagineBottoneModificaPagDispositivo.png")
PATH_IMG_BOTTONE_ELIMINAZIONE_PAG_DISPOSITIVI = os.path.join(PATH_IMMAGINI, "ImmagineBottoneEliminaPagDispositivo.png")
PATH_IMG_ICONA_DISPOSITIVO = os.path.join(PATH_IMMAGINI, "ImmagineDispositivo.png")
PATH_JSON_TEMI = os.path.join(PATH_CARTELLA_CORRENTE,"UtilityFiles","ThemeData.json")
PATH_JSON_INVIOMAIL = os.path.join(PATH_CARTELLA_CORRENTE,"UtilityFiles","InfoEmail.json")
PATH_JSON_DISPOSITIVI = os.path.join(PATH_CARTELLA_CORRENTE,"UtilityFiles","DispositiviData.json")
LOG_PATH = os.path.join(PATH_CARTELLA_CORRENTE,"UtilityFiles","log.txt")


DIMENSIONI_IMMAGINE_LOGO = (25,25)


# COSTANTI PAGINA DISPOSITIVI
SPAZIO_LATI_PAGINA_DISPOSITIVI = 25
SPAZIO_ALTO_PAGINA_DISPOSITIVI = 150
ALTEZZA_PAGINA_DISPOSITIVI = 3500
PROPORZIONE_LARGHEZZA_TABELLA_DISPOSITIVI_LARGHEZZA_PAGINA = round(95/100, 2)

PROPORZIONI_NOME_DISPOSITIVO_FRAMEDISPOSITIVO = round(26/100,2)
PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDISPOSITIVO = round(26/100,2)
PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDISPOSITIVO = round(12/100,2)
PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDISPOSITIVO = round(26/100,2)
PROPORZIONI_TASTI_MODDEL_TABELLA_DISPOSITIVI = round(10/100, 2)

DIMENSIONI_PULSANTI_MODIFICA_ELIMINA = (20,20)

# COSTANTI PAGINA DASHBOARD
SPAZIO_LATI_PAGINA_DASHBOARD = 25
SPAZIO_ALTO_PAGINA_DASHBOARD = 150
ALTEZZA_PAGINA_DASHBOARD = 3500
#PROPORZIONE_LARGHEZZA_TABELLA_DASHBOARD_LARGHEZZA_PAGINA = round(95/100, 2) #Non usato
ALTEZZA_TABELLA_PAGINADASHBOARD = 500

PROPORZIONI_NOME_DISPOSITIVO_FRAMEDASHBOARD = round(24/100,2)
PROPORZIONI_INDIRIZZO_DISPOSITIVO_FRAMEDASHBOARD = round(24/100,2)
PROPORZIONI_PORTA_DISPOSITIVO_FRAMEDASHBOARD = round(12/100,2)
PROPORZIONI_TEMPOPING_DISPOSITIVO_FRAMEDASHBOARD = round(24/100,2)
PROPORZIONI_STATUS_DISPOSITIVO_TABELLA_DASHBOARD = round(6/100, 2)
PROPORZIONI_PINGMANUALE_DISPOSITIVO_TABELLA_DASHBOARD = round(10/100, 2)
DIMENSIONI_IMMAGINE_STATUS_DASHBOARD = (25,25)

# COSTANTI PAGINA IMPOSTAZIONI
SPAZIO_LATI_PAGINA_IMPOSTAZIONI = 25
SPAZIO_ALTO_PAGINA_IMPOSTAZIONI = 150
ALTEZZA_PAGINA_IMPOSTAZIONI = 3500

# COSTANTI GESTORE PAGINA
NOME_INTERNO_PAGINA_DISPOSITIVI = "paginaDispositivi"
NOME_INTERNO_PAGINA_DASHBOARD = "paginaDashboard"
NOME_INTERNO_PAGINA_AGGIUNGI_DISPOSITIVO = "paginaAggiungiDispositivo"
NOME_INTERNO_PAGINA_MODIFICA_DISPOSITIVO = "paginaModifica"
NOME_INTERNO_PAGINA_IMPOSTAZIONI = "paginaImpostazioni"


# COSTANTI MENU
PROPORZIONE_MENU_PAGINA = round(1/7,2)
PROPORZIONE_IMMAGINE_SCRITTA_ELEMENTO_MENU = round(1/15,2)
PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_LARGHEZZA = round(1/60,2)
PROPORZIONE_ELEMENTO_MENU_SPAZI_VUOTI_ALTEZZA = round(1/20,2)
PROPORZIONE_LISTA_MENU_ALTEZZA_PAGINA = round(6/8,2)
DIMENSIONI_IMMAGINE_ELEMENTO_MENU = (25,25)

PAGINA_DEFAULT = NOME_INTERNO_PAGINA_DASHBOARD
TUPLA_PAGINA_IMPOSTAZIONI = (NOME_INTERNO_PAGINA_IMPOSTAZIONI, os.path.join(PATH_IMMAGINI,"ImmagineImpostazioni.png"), "Impostazioni")
LISTA_PAGINE_MENU = [
    #("nomePaginaInterno", "pathImmagine", "nomePaginaMostrato") 
    (NOME_INTERNO_PAGINA_DISPOSITIVI, os.path.join(PATH_IMMAGINI,"ImmagineDispositivo.png"), "Dispositivi"),
    (NOME_INTERNO_PAGINA_DASHBOARD, os.path.join(PATH_IMMAGINI,"ImmagineDashboard.png"), "Dashboard")
]

# IMPOSTAZIONI GENERALI FINESTRA
LARGHEZZA_SCHERMO_INIZIALE = 1200
ALTEZZA_SCHERMO_INIZIALE = 700
MIN_LARGHEZZA_SCHERMO = 700
MIN_ALTEZZA_SCHERMO = 394
MAX_LARGHEZZA_SCHERMO = 2560
MAX_ALTEZZA_SCHERMO = 1440
OFFSET_ORIZZONTALE_SCHERMO = (int((1/20) * LARGHEZZA_SCHERMO_INIZIALE))
OFFSET_VERTICALE_SCHERMO = ((int(1/20) * ALTEZZA_SCHERMO_INIZIALE))