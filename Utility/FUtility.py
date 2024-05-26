import sys
sys.path.append("c:\\users\\utente\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0\\localcache\\local-packages\\python312\\site-packages")

from Utility.Chrono import *
from Utility.Costanti import *
from Utility.Log import *
from Utility.EventHandler import *

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import font as tkFont
from PIL import Image, ImageTk

from math import *
import random

import smtplib
import pythonping

import os
from threading import * 


#Ritorna la posizione dell'elemento con lo stesso valore
def RicercaInListaOrdinata(lista : list, 
                            elemento, 
                            funzioneElementoLista = lambda a : a, #funzione da applicare ad agli elementi della lista prima della comparazione (returnType any)
                            funzioneElementoDato = lambda a : a, #funzione da applicare ad all'elemento dato prima della comparazione (returnType any)
                            funzioneDiComparazione = lambda t : 0 if t[0] == t[1] else 1 if t[0] > t[1] else -1 #a (dopo,in quel punto, o prima) di b se ... (returnType [1,0,-1])
                            ) -> list[int, bool]: 
    #Calcolo la lunghezza della lista
    lunghezzaLista = len(lista)
    if lunghezzaLista == 0: 
        return [0,False]
    #Inizializzo il puntatore alla metà della lista
    puntatore = lunghezzaLista//2

    #Se gli elementi sono uguali, ritorno la posizione
    variabileDiComparazione = [funzioneElementoDato(elemento), funzioneElementoLista(lista[puntatore])]
    if funzioneDiComparazione(variabileDiComparazione) == 0:
        return [puntatore,True]
    
    #Altrimenti analizzo richiamo la funzione 
    if funzioneDiComparazione(variabileDiComparazione) == 1:
        #Se la lista è di lunghezza 1 e l'elemento è maggiore, ritorno il puntatore successivo
        if lunghezzaLista == 1:
            return [puntatore+1,False]
        result = RicercaInListaOrdinata(lista[puntatore:lunghezzaLista], elemento, funzioneElementoLista, funzioneElementoDato, funzioneDiComparazione)
        return [puntatore + result[0], result[1]]
    elif funzioneDiComparazione(variabileDiComparazione) == -1:
        return RicercaInListaOrdinata(lista[0:puntatore], elemento, funzioneElementoLista, funzioneElementoDato, funzioneDiComparazione)
    else:
        LOG.IPrint("errore durante la ricerca di un elemento in una lista ordinata",2)
        return [-1,False]
    
#Ritorno la lista ordinata
def CountingSort(inputArray : list[int], minVal = None, maxVal = None, funzioneSuElemento = lambda x : x): #Per usare funzione su elemento, minimo e massimo devono essere specificati
    
    # Check if minmax insert
    if minVal == None or maxVal == None:
        maxVal = max(inputArray)
        minVal = min(inputArray)
        funzioneSuElemento = lambda x : x

    #Calcolo la lunghezza e alloco counting array e output array
    lenCountArray = (maxVal - minVal) + 1
    countArray = [0] * lenCountArray
    outputArray = [0] * len(inputArray)
    
    #Per ogni elemento conto quante volte è presente nella lista
    for inputElement in inputArray:
        countArray[funzioneSuElemento(inputElement) - minVal] += 1
    
    #Per ogni elemento, ciclo per il numero di volte presente nel counting e lo aggiungo all'output array
    iOutputElementPosition = 0
    iValue = minVal
    for countElement in countArray:
        #Ciclo per tutte le volte presente
        for i in range(countElement):
            outputArray[iOutputElementPosition] = iValue
            iOutputElementPosition += 1
        iValue += 1

    return outputArray


#Insertion sort
def InsertionSort(inputArray : list[int], funzioneDiConfronto = lambda t : t[0] > t[1]):
    for i in range(1, len(inputArray)):
        value = inputArray[i]
        j = i-1
        while j >= 0 and funzioneDiConfronto((inputArray[j], value)):
            inputArray[j + 1] = inputArray[j]
            j = j - 1
        inputArray[j + 1] = value
    return inputArray
