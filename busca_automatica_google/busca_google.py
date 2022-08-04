# import das bibs
from random import random
from select import select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import requests
import random

class Busca:
    def __init__(self, url, palavra, quero_esse_link, total_paginas_busca):
        self.url = url
        self.palavra = palavra
        self.quero_esse_link = quero_esse_link
        self.total_paginas_busca = total_paginas_busca

        chrome_options = Options()
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)

    def pesquisar(self):
        driver = self.driver
         #mostrando IP externo de conexão com a internet
        try:
            ip_publico = requests.get("https://api.ipify.org").text
            print("IP externo: " + ip_publico)
            print("--------------------------")
        except:
            print("Não foi possível obter o IP externo")      

        driver.get(self.url)
        time.sleep(3)
        campo_pesquisa_google = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
        campo_pesquisa_google.click()
        campo_pesquisa_google.clear()

        palavra_random = random.choice(self.palavra) # escolhendo uma palavra randomica do array

        campo_pesquisa_google.send_keys(palavra_random)
        campo_pesquisa_google.send_keys(Keys.RETURN)
        time.sleep(3)       

        # verifica se o texto existe na página e se exister vou clicar nele, isso se ele for igual a variavel quero_esse_link
        if self.existe_texto(self.quero_esse_link):
            links = driver.find_elements_by_tag_name("a")
            for link in links:
                if self.quero_esse_link in link.text:
                    link.click()
                    time.sleep(5) # tempo para carregar a página
                    break
            
            print("Busca finalizada sem proxy")
            #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
            self.proxy()  
        else:
            print("Não encontrei o texto. Procurando nas próximas páginas") 
            for i in range(self.total_paginas_busca): # procurando nas próximas páginas
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                driver.find_element(By.ID, "pnnext").click()
                time.sleep(3)
                if self.existe_texto(self.quero_esse_link):
                    links = driver.find_elements_by_tag_name("a")
                    for link in links:
                        if self.quero_esse_link in link.text:
                            link.click()
                            time.sleep(5) # tempo para o link carregar
                            break
                    break
                else:
                    continue
            
            print("Busca finalizada sem proxy")
            #aqui vou começar novamente a busca com o proxy
            self.proxy()

    def proxy(self):
        driver = self.driver
        driver.get('https://www.proxysite.com/pt/') # abre a página do proxy
        time.sleep(5)
        select = Select(driver.find_element_by_class_name('server-option')) # seleciona o servidor
       
        # select.select_by_value('us1') # seleciona o servidor
        todos_servidores = [x.get_attribute('value') for x in select.options] # pega todos os servidores
        #print(todos_servidores)
        numero_servidor = random.randint(1,20) # numero do servidor
        nome_servidor = 'us'
       
        # aqui vou testar qual Servidor está no select, se não estiver ele vai para o próximo. As vezes o servidor us1 não tá na lista, ai ele vai para o próximo us2.
        # Depois que o numero de servidor chegar a 20, mudo o nome do servidor para eu e reseto o numero de servidor para 1
        for servidor in todos_servidores:
            if numero_servidor == 21:
                nome_servidor = "eu"
                numero_servidor = 1

            if servidor == nome_servidor+str(numero_servidor):
                select.select_by_value(servidor)
                break
            numero_servidor += 1

        campo_proxy_input = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[1]/div/div[3]/form/div[2]/input") # seleciona o campo de input do proxy
        campo_proxy_input.click()
        campo_proxy_input.clear()
        campo_proxy_input.send_keys(self.url)
        campo_proxy_input.send_keys(Keys.RETURN)
        time.sleep(3)

        #depedendo do servidor escolhido, o google irá pedir para aceitar alguns termos de cookies. Geralmente é servidores da França
        #neses caso, não continuo a busca, volto a escolher outro servidor e tento novamente
        if self.existe_texto("Avant d'accéder à Google"):
            time.sleep(2)
            driver.find_element(By.ID, "L2AGLb").click()
            time.sleep(5)
            self.proxy()
            time.sleep(5)

        campo_pesquisa_google = driver.find_element_by_css_selector('[title="Search"]')
        campo_pesquisa_google.click()
        campo_pesquisa_google.clear()

        palavra_random = random.choice(self.palavra) # escolhendo uma palavra randomica do array

        campo_pesquisa_google.send_keys(palavra_random)
        campo_pesquisa_google.send_keys(Keys.RETURN)
        time.sleep(3)     

        if self.existe_texto("Go to Google Home"):
    
            # verifica se o texto existe na página e se exister vou clicar nele, isso se ele for igual a variavel quero_esse_link
            if self.existe_texto(self.quero_esse_link):
                links = driver.find_elements_by_tag_name("a")
                for link in links:
                    if self.quero_esse_link in link.text:
                        link.click()
                        time.sleep(5) # espera 5 segundos para carregar a página
                        break

                print("Busca finalizada com proxy")
                #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
                self.proxy()     
            else:
                print("Não encontrei o texto. Procurando nas próximas páginas")
                for i in range(self.total_paginas_busca): # procurando nas próximas páginas
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    driver.find_element(By.ID, "pnnext").click()
                    time.sleep(3)
                    if self.existe_texto(self.quero_esse_link):
                        links = driver.find_elements_by_tag_name("a")
                        for link in links:
                            if self.quero_esse_link in link.text:
                                link.click()
                                time.sleep(5) #tempo para carregar o site quando é encontrado
                                break  
                        break    
                    else:
                        continue
        else:
            print("Estou na página errada")
            self.proxy()
             
        print("Busca finalizada com proxy")
        #aqui vou começar novamente a busca + trocando o servidor de conexão com a internet usando um proxy
        self.proxy()


    # procura dentro da página algum texto
    def existe_texto(self, text):
        return str(text) in self.driver.page_source


# fazendo a busca no google
url = "https://www.google.com.br/"

# um array de palavras a ser buscada no google (para buscar algumas palavras, basta adicionar mais palavras no array)
palavra = ["que horas tem ônibus + flavio oliveira + serra negra", "horário de ônibus em serra negra + flavio oliveira", "ônibus em serra negra que horas tem ônibus + flavio oliveira"]
#palavra = ["me guia serra negra  flavio oliveira guiaserranegra.com.br ", "guia online serra negra me guia serra negra guiaserranegra.com.br ", "ponto turístico serra negra  me guia serra negra  flavio oliveira"]
#palavra = ['farmacia de plantao em serra negra farmaciadeplantaosn flavio oliveira', 'farmacia de plantao farmaciadeplantaosn', 'farmacias de plantão serra negra farmaciadeplantaosn']

# o link exato que quero que seja clicado
quero_esse_link = "https://www.quehorastemonibus.com.br"
#quero_esse_link = "https://www.guiaserranegra.com.br"
#quero_esse_link = "https://www.farmaciadeplantaosn.com.br"

# quantas páginas de busca quero que seja feita
total_paginas_busca = 3

buscarPalavra = Busca(url, palavra, quero_esse_link, total_paginas_busca)
buscarPalavra.pesquisar()
