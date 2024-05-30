from smtplib import *

try:
    print("Constructor bt to be called")
    smtp = SMTP('hosting.dzcomputers.it')
    smtp.set_debuglevel(1)
    smtp.connect(host = 'hosting.dzcomputers.it', port = 587)
    print("Connected")
    smtp.starttls()
    print("TLS attivato")
    smtp.login(user = 'test@dysoft.cloud', password = 'a6K05ga4@')
    print("Logged in")
    msg = "From: test@dysoft.cloud\nTo: jamesscotti873@gmail.com\nSubject: prova\n\nprova\n\nBye\n"
    smtp.sendmail(from_addr = "test@dysoft.cloud", to_addrs = "jamesscotti873@gmail.com", msg = msg)
    print("Mail sent")
    smtp.quit()
    print("Quit")
except Exception as e:
    print(e)