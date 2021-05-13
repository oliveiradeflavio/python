"""
Comentários em fotos através da pesquisa
de hashtag. 
O teste foi feito, foi em um instagram que possui a autenticação 2 fatores, 
por isso temos a parte de digitação da verificação de código.

Flávio Oliviera - 2021
https://www.github.com/oliveiradeflavio
"""


#importação de lib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class instagramBot:
    def __init__(self, username, password, verificacaoCodigo):
        self.username = username
        self.password = password
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
        self.comentar_nas_fotos_com_hastag('shotoniphone')

    #digitando os comentário na velocidade humanos, as vezes acelerando as vezes um pouco mais lento.
    @staticmethod
    def digitando_como_humano(frase, onde_digitar):
        for letra in frase:
            onde_digitar.send_keys(letra)
            time.sleep(random.randint(1,5)/30)

    def comentar_nas_fotos_com_hastag(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/"+ hashtag + "/")
        time.sleep(3)
        
        #navegando até a terceira página
        for i in range(1,3):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
        
        #pegando os link das imagens que estão nas páginas
        hrefs = driver.find_elements_by_tag_name('a')
        imagem_hrefs = [elem.get_attribute('href') for elem in hrefs]
        [href for href in imagem_hrefs if hashtag in href]
        print(hashtag + ' fotos ' + str(len(imagem_hrefs)))

        for imagem_href in imagem_hrefs:
            driver.get(imagem_href)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            #class="Ypffh" = campo de comentário foto
            try:
                comentarios = ["Caramba! Tá top!","Essa foto ficou demais viu!", "Só fooootão","Curti muito essa foto!","Que fotão!!!!","Tooooop!!!","Eitaaaaaa que foto =D"]
                driver.find_element_by_class_name('Ypffh').click()
                campo_comentario = driver.find_element_by_class_name('Ypffh')
                time.sleep(random.randint(2,5))
                #chama a função para que seja digitando mais lento ou mais rapido "como humano e não um bot"
                self.digitando_como_humano(random.choice(comentarios), campo_comentario)
                #o ideal é colocar um valor maior, para que não seja identificado como bot.
                time.sleep(random.randint(10,20))
                driver.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
                time.sleep(3)
            except Exception as e:
                print(e)
                time.sleep(5)

verificacaoCodigo = input("Digite o código de verificação: ")
flavioBot = instagramBot("SEU_USUÁRIO", "SUA_SENHA", verificacaoCodigo )
flavioBot.login()