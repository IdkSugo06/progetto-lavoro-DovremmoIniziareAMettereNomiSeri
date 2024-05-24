import subprocess
import threading
import time

numOfThread = 100


def InvioPing_semplice():
    try:
        #Invio il ping
        subprocessResult = subprocess.run("ping -n 1 -l 1 www.google.com -w 200", capture_output=True, text=True, timeout=0.2)
        # Se il returncode è 0, nessun errore
        #print(subprocessResult.returncode == 0)
    except subprocess.TimeoutExpired:
        #print("TimeOut")
        pass
def AvvoInvioPing_parallelizzato_semplice():
    global numOfThread
    tl = [threading.Thread(target = InvioPing_semplice) for i in range(numOfThread)]
    for t in tl:
        t.start()
    for t in tl:
        t.join()
def Start_semplice():
    for i in range(20):
        startTime = time.time()
        AvvoInvioPing_parallelizzato_semplice()
        deltaTime = time.time() - startTime
        print(deltaTime)
        time.sleep(max(1 - deltaTime, 0))


def InvioPing():
    for i in range(20):
        startTime = time.time()
        InvioPing_semplice()
        deltaTime = time.time() - startTime
        time.sleep(max(1 - deltaTime, 0))
    print("finito")
def AvvoInvioPing_parallelizzato():
    global numOfThread
    tl = [threading.Thread(target = InvioPing) for i in range(numOfThread)]
    for t in tl:
        t.start()
    for t in tl:
        t.join()
def Start():
    AvvoInvioPing_parallelizzato()

Start()
