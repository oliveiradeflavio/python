"""
Flávio Oliveira - 2021
https://github.com/oliveiradeflavio
"""

"""
Antes de executar o código, seu whatsapp Web precisa estar conectado no celular
e logado no navegador Chrome, no meu teste usei o Chrome. Depois que estiver
executando a aplicação, não mexer no mouse.
"""

#importar as bibliotecas
import pywhatkit
import keyboard
import time
from datetime import datetime

#definir para quais contatos ou de uma lista de excel
contatos = ["+5519999999999", "+5519999999999", "+5519999999999", "+5519999999999"]

#definindo intervalo de envio
while len(contatos) >= 1:
    #envia mensagem
    pywhatkit.sendwhatmsg(contatos[0], 'Olá, eu sou uma mensagem automática', datetime.now().hour,datetime.now().minute + 1)
    del contatos[0]
    keyboard.press_and_release('ctrl + w')
