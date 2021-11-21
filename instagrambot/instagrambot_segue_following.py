"""
Esse bot irá clicar no botão seguir dos seguindos da conta especifica. 
Irá navegar até o perfil da conta, clicar nos seguindos e nesse modal que abrir, irá clicar no botão seguir de cada username.

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
from datetime import datetime


class instagramBot:
    def __init__(self, username, password, verificacaoCodigo):
        self.username = username
        self.password = password
        self.verificacaoCodigo = verificacaoCodigo
        self.lista_seguidores = []
        self.perfil = 'sorteiode_premios' #perfil do insta onde vai ser preciso seguir os seguindos
        #self.driver = webdriver.Firefox(executable_path="C:\geckodriver") #caminho de onde está a biblioteca geckodriver pasta windows
        self.driver = webdriver.Firefox(executable_path="/Users/foliveira/github/python/instagrambot/geckodriver") #caminho de onde está a biblioteca geckodriver pasta macOS

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
        self.seguindo(self.perfil)
  
    def seguindo(self, perfil_instagram):
        driver = self.driver
        driver.get("https://www.instagram.com/"+ perfil_instagram)
        time.sleep(3)
        #seguidores = driver.find_elements_by_xpath('//li[contains(@class,"Y8-fY")]')
        #seguidores[1].click()
        
        page = 'following' # para seguidores followers || para seguindo following
        driver.find_element_by_xpath('//a[contains(@href, "%s")]' % page).click()
        sessao_total_seguindo = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        total_seguindo = sessao_total_seguindo.text
        print(total_seguindo)
        total_seguindo = total_seguindo.replace("seguindo", "")
    

        for i in range(1, int(total_seguindo)):
            time.sleep(3)
            i = i + 3 #a cada usuário o scroll do modal vai abaixando, 
            sessao_nomes_seguindo = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/ul/div/li[%s]' % i) #captura o nome do seguidor
            driver.execute_script("arguments[0].scrollIntoView();", sessao_nomes_seguindo)
            driver.switch_to_active_element
            seguindo = driver.find_elements_by_xpath('//*[contains(text(), "Seguir")]')
            seguindo[1].click() #clica no botão para seguir #### TESTEI ATÉ O VALOR 48, QUE SERIA 48 SEGUIDORES ####
            i = i - 3 # preciso voltar ao valor original, para que possa fazer o laço novamente e o seguir os @ do modal sem pular
            print(i)
            time.sleep(1)
 
#Layout
sg.theme('Reddit')
layout = [
    [sg.Text('Username'),sg.Input(key='username', size=(30, 4))],
    [sg.Text('Password'),sg.Input(key='password',password_char='*', size=(30,4))],
    [sg.Text('Verificação 2 Fatores'),sg.Input(key='vefificacaoCodigo', size=(30,4))],
    [sg.Button('Logar')]
]

#Janela
janela = sg.Window('BOT INSTAGRAM SEGUE SEGUIDORES', layout)

#ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Logar':
        if valores['username'] == '' or valores['password'] == '' or valores['vefificacaoCodigo'] == '':
            sg.Popup('Há campos vazios a serem preenchidos', title='Atenção')
        else:
            flavioBot = instagramBot(valores['username'], valores['password'], valores['vefificacaoCodigo'] )
            flavioBot.login()
