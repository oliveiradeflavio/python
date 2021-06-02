"""
Curtir fotos
O teste foi feito, foi em um instagram que possui a autenticação 2 fatores, 
por isso temos a parte de digitação da verificação de código.

Flávio Oliviera - 2021
https://www.github.com/oliveiradeflavio
"""

#importação de lib
from typing import Sized
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from PySimpleGUI import PySimpleGUI as sg

class instagramBot:
    def __init__(self, username, password, hashtag_procurar, verificacaoCodigo):
        self.username = username
        self.password = password
        self.hashtag_procurar = hashtag_procurar
        self.verificacaoCodigo = verificacaoCodigo
        self.driver = webdriver.Firefox(executable_path="/Users/foliveira/github/python/instagrambot/geckodriver") #caminho de onde está a biblioteca geckodriver

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com")
        #input[@name=username] = login inspecionado na pagina instagram
        #input[@name=password] = senha inspecionado na pagina instagram
        #input[@name=verificationCode] = verificaçao de codigo em autenticaçao de dois fatores
        time.sleep(3)
        campo_usuario = driver.find_element_by_xpath("//input[@name='username']")
        campo_usuario.click()
        campo_usuario.clear()
        campo_usuario.send_keys(self.username)
        campo_senha = driver.find_element_by_xpath("//input[@name='password']")
        campo_senha.clear()
        campo_senha.send_keys(self.password)
        campo_senha.send_keys(Keys.RETURN)
        time.sleep(3)
        campo_verificacao_codigo = driver.find_element_by_xpath("//input[@name='verificationCode']")
        campo_verificacao_codigo.click()
        campo_verificacao_codigo.clear()
        campo_verificacao_codigo.send_keys(self.verificacaoCodigo)
        campo_verificacao_codigo.send_keys(Keys.RETURN)
        time.sleep(3)
        self.curtir_fotos(self.hashtag_procurar)

    def curtir_fotos(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/"+ hashtag + "/")
        time.sleep(3)
        
        #navegando página
        for i in range(1,10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
        
        #pegando os link das imagens que estão nas páginas
        hrefs = driver.find_elements_by_tag_name('a')
        imagem_hrefs = [elem.get_attribute('href') for elem in hrefs]
        [href for href in imagem_hrefs if hashtag in href]
        print('Hashtag: ' + hashtag + ' QNT Fotos: ' + str(len(imagem_hrefs)))
        qnt_likes = 1
        for imagem_href in imagem_hrefs:
            driver.get(imagem_href)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            try:
                time.sleep(5)
                driver.find_element_by_class_name('Ypffh').click()
                curtir_post = driver.find_element_by_xpath("//span[@class='fr66n']")
                curtir_post.click() #CURTI FOTO
                print("Quantidade de Likes: " + str(qnt_likes))
                qnt_likes = qnt_likes + 1
                time.sleep(2)
                time.sleep(random.randint(2,5))
            except Exception as e:
                print(e)
                time.sleep(5)

#Layout
sg.theme('Reddit')
layout = [
    [sg.Text('Username'),sg.Input(key='username', size=(30, 4))],
    [sg.Text('Password'),sg.Input(key='password',password_char='*', size=(30,4))],
    [sg.Text('hashtag'),sg.Input(key='hashtag', size=(30,4))],
    [sg.Text('Verificação 2 Fatores'),sg.Input(key='vefificacaoCodigo', size=(30,4))],
    [sg.Button('Logar')],
    [sg.Output(size=(50,20))]
]

#Janela
janela = sg.Window('BOT INSTAGRAM CURTIR FOTOS', layout)

#ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Logar':
        if valores['username'] == '' or valores['password'] == '' or valores['hashtag'] == '' or valores['vefificacaoCodigo'] == '':
            sg.Popup('Há campos vazios a serem preenchidos', title='Atenção')
        else:
            flavioBot = instagramBot(valores['username'], valores['password'], valores['hashtag'], valores['vefificacaoCodigo'] )
            flavioBot.login()

#verificacaoCodigo = input("Digite o código de verificação: ")
#flavioBot = instagramBot("SEU_USERNAME", "SEU_PASSWORD", verificacaoCodigo )
#flavioBot.login()