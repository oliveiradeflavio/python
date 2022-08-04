#!/usr/bin/python3
#-*- encoding: utf-8 -*-

#Programa para decodificar string na base64

import os
import base64

def intro():
    print("\nFlávio Oliveira - Decifra Base64")
    print("www.github.com/oliveiradeflavio\n")

def decifra():
    while True:
        
        try:
            
            recebe = input("Digite a frase codificada (0 para sair):  ")
            if recebe == str(0):
                print("saindo")
                break            
            decodifica = base64.b64decode(recebe)
            print("\nFrase Decodificada: ", decodifica)
            input("Qualquer tecla continua")
            os.system("sleep 0.5")
            os.system("clear")
            intro()
        
        except:
            print("Frase não está na base64")
            os.system("sleep 1")
            os.system("clear")
            intro()
                    
intro()
decifra()
