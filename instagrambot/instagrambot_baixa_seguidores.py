"""
Esse bot irá pegar os seguidores da conta e fazer o comentário com esses seguidores (username)
em um post de sorteio do instagram

Flávio Oliviera - 2021
https://www.github.com/oliveiradeflavio
"""


#importação de lib
from http.server import executable
from typing import Sized
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from PySimpleGUI import PySimpleGUI as sg
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class instagramBot:
    def __init__(self, username, password, verificacaoCodigo):
        self.username = username
        self.password = password
        self.verificacaoCodigo = verificacaoCodigo
        self.lista_seguidores = []
        #self.driver = webdriver.Firefox(executable_path="C:\geckodriver") #caminho de onde está a biblioteca geckodriver
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

        ''' #verificaçao de autenticaçao de dois fatores, caso sua conta não tenha, basta comentar até o último time.sleep()'''
        # campo_verificacao_codigo = driver.find_element_by_xpath("//input[@name='verificationCode']")
        # campo_verificacao_codigo.click()
        # campo_verificacao_codigo.clear()
        # campo_verificacao_codigo.send_keys(self.verificacaoCodigo)
        # campo_verificacao_codigo.send_keys(Keys.RETURN)
        # time.sleep(3)

        self.seguidores(self.username)

    #digitando os comentário na velocidade humanos, as vezes acelerando as vezes um pouco mais lento.
    @staticmethod
    def digitando_como_humano(frase, onde_digitar):
        for letra in frase:
            onde_digitar.send_keys(letra)
            time.sleep(random.randint(1,5)/30)
    
    def seguidores(self, perfil_instagram):
        driver = self.driver
        driver.get("https://www.instagram.com/"+ perfil_instagram)
        time.sleep(3)        
        page = 'followers' # para seguidores followers || para seguindo following
        if page == 'followers':
            sessao_total_seguidores = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span')
        if page == 'following':
            sessao_total_seguidores = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span')
        
        total_seguidores = sessao_total_seguidores.text
        print(total_seguidores)
        total_seguidores = total_seguidores.replace("seguidores", "")

        driver.get("https://www.instagram.com/"+ perfil_instagram + "/" + page)
        time.sleep(5)
        print(total_seguidores)

        
        for i in range(1, int(total_seguidores)):
            time.sleep(3)
            sessao_nomes_seguidores = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/ul/div/li/div/div[2]/div[1]/div/div/span/a/span')                                                       
            #sessao_nomes_seguidores = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/ul/div/li[%s]/div/div[2]/div/div/div/span/a/span' % i)
            driver.execute_script("arguments[0].scrollIntoView();", sessao_nomes_seguidores)
            time.sleep(1)
            texto = sessao_nomes_seguidores.text
            lista_seguidores_extraida = texto.split()
            self.lista_seguidores.append(lista_seguidores_extraida[0])

        print(self.lista_seguidores)
        self.comentar_no_sorteio()
        
    def comentar_no_sorteio(self):
        driver = self.driver
        driver.get("https://www.instagram.com/p/CO6ipgjrhzV")
        time.sleep(2)
        #curti o post do sorteio
        curtir_post = driver.find_element_by_xpath("//span[@class='_aamw']")
        curtir_post.click()
        print("Like")
        time.sleep(2)
        try:
            contador = 0
           
            #a cada username dentro da lista, irá ser um comentário a ser publicado no post de sorteio.
            for perfil_seguidores in self.lista_seguidores:
                time.sleep(5)       
                driver.find_element_by_css_selector("[placeholder='Adicione um comentário...']").click()        
                campo_comentario = driver.find_element_by_css_selector("[placeholder='Adicione um comentário...']")
                time.sleep(random.randint(2,5))
                self.digitando_como_humano('@'+str(perfil_seguidores), campo_comentario)
                time.sleep(random.randint(10,20))
                campo_comentario.send_keys(Keys.RETURN)
                time.sleep(5)
                #quando o contador atingir o valor 50, o sistema irá pausar no comentário
                #e contador será zerado.A ssim tentamos evitar o bloqueio da conta. 
                contador = contador + 1
                driver.refresh()
                if contador == 50:
                    contador = 0
                    print('Sistema em espera, voltará a comentar em 30 minutos. Última pausa feita: ', datetime.now().hour,datetime.now().minute)
                    time.sleep(1800) #30minutos
            
            print("Comentarios Enviados. ", datetime.now().hour,datetime.now().minute)

        except Exception as e:
            print(e)
            time.sleep(5)

#Layout
sg.theme('Reddit')
layout = [
    [sg.Text('Username'),sg.Input(key='username', size=(30, 4))],
    [sg.Text('Password'),sg.Input(key='password',password_char='*', size=(30,4))],
    [sg.Text('Verificação 2 Fatores'),sg.Input(key='vefificacaoCodigo', size=(30,4))],
    [sg.Button('Logar')]
]

#Janela
janela = sg.Window('BOT INSTAGRAM SORTEIO', layout)

#ler os eventos
while True:
    eventos, valores = janela.read()
    valores['username'] = 'flavio_tech'
    valores['password'] = '102030qwerty.,'
    valores['vefificacaoCodigo'] = 'login'
    
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Logar':
       
        
        if valores['username'] == '' or valores['password'] == '' or valores['vefificacaoCodigo'] == '':
            sg.Popup('Há campos vazios a serem preenchidos', title='Atenção')
        else:
            valores['username'] = 'flavio_tech'
            valores['password'] = '102030qwerty.,'
            valores['verificaacao'] = 'login'
            flavioBot = instagramBot(valores['username'], valores['password'], valores['vefificacaoCodigo'] )
            flavioBot.login()
