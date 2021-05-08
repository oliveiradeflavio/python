"""
Flávio Oliveira - 2021
https://github.com/oliveiradeflavio
"""
#importar as bibliotecas
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

#navegar até o whatsApp Web
#ch_option.add_argument, para usar o profile do google com cache, assim evita de ficar pedindo o qrcode.
ch_options = webdriver.ChromeOptions()
ch_options.add_argument("--user-data-dir=endereço url perfil chrome")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=ch_options)
driver.get('https://web.whatsapp.com/')
time.sleep(10)

#definir contatos e grupos e mensagem a ser enviadas
contatos = ['nome contato', 'nome do contato']
mensagem = 'Olá, eu sou um bot whatsApp.'

#buscar contatos ou grupos
#campo de pesquisa 'copyable-text selectable-text'
#campo digitar mensagem 'copyable-text selectable-text'
def buscar_contato(contato):
    campo_pesquisa = driver.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    #time.sleep(3)
    campo_pesquisa.click()
    campo_pesquisa.send_keys(contato)
    campo_pesquisa.send_keys(Keys.ENTER)

def enviar_mensagem(mensagem):
    campo_mensagem = driver.find_elements_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    campo_mensagem[1].click()
    campo_mensagem[1].send_keys(mensagem)
    campo_mensagem[1].send_keys(Keys.ENTER)

for contato in contatos:
    buscar_contato(contato)
    enviar_mensagem(mensagem)