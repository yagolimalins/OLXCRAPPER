import os
import time
import smtplib
import requests
from getpass import getpass
from bs4 import BeautifulSoup
from email.message import EmailMessage

# DECLARAÇÃO E INICIALIZAÇÃO DE VARIÁVEIS:

EMAIL_ADDRESS = os.environ.get('EMAIL_USER') 
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

url = 'https://www.olx.com.br/celulares'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
timesleep = 15

# DECLARAÇÃO DE FUNÇÕES:

def banner():

    print()
    print("╔═══════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║  ██████╗ ██╗    ██╗     ██╗  ██╗      ██████╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗  ║")
    print("║ ██╔═══██╗██║    ╚═╝      ██╗██╔╝     ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗ ║")
    print("║ ██║   ██║██║              ███╔╝█████╗██║     ██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝ ║")
    print("║ ██║   ██║██║             ██╔██╗╚════╝██║     ██╔══██╗██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗ ║")
    print("║ ╚██████╔╝███████╗       ██╔╝ ██╗     ╚██████╗██║  ██║██║  ██║██║     ██║     ███████╗██║  ██║ ║")
    print("║  ╚═════╝ ╚══════╝       ╚═╝  ╚═╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝ ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════╝")
    print("  Ferramenta de busca por novos anúncios em categorias da OLX com notificações por email (GMail) ")
    print("Autor: Yago Lima Lins | yago.lima.lins@protonmail.com | https://github.com/yagolimalins/OLXCRAPPER")
    print("-------------------------------------------------------------------------------------------------\n")


def screen_clear():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')


def statuscode(url=url, headers=headers):

    result = requests.get(url, headers=headers)
    statuscodenumber = int(result.status_code)

    return(statuscodenumber)

def webscrap(url=url, headers=headers, ):

    result = requests.get(url, headers=headers)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    items = soup.find_all('a')
    lista = []

    for item in items:

            if ("Hoje" and "R$") in item.text:

                    title = item.get('title')
                    price = item.find('p').get_text()
                    url = item.attrs['href']
                    lista.append([title, price, url])

                    print(price + ' - ' + title)
        
    
    print("\n-------------------------------------------------------------------------------------------------"

    return(lista)

# EXECUÇÃO DO SCRIPT:

banner()

listaOld = webscrap()
print("O item mais recentemente adicionado é: " + listaOld[0][0] + " - " + listaOld[0][1])

time.sleep(timesleep)

while True:

    screen_clear()

    banner()
    
    statuscodenumber = statuscode()

    if statuscodenumber == 200:
        listaNew = webscrap()

        if listaNew[0][0] != listaOld[0][0]:
            print("O item mais recentemente anunciado é: " + listaNew[0][0] + " - " + listaNew[0][1])
            
            msg = EmailMessage()
            msg['Subject'] = "[OLXCRAPPER] " + listaNew[0][0] + " - " + listaNew[0][1]
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS
            msg.set_content('Link para o anuncio: ' + listaNew[0][2])

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            listaOld = listaNew
        
        elif listaNew[0][0] == listaOld[0][0]:
            print("O item mais recentemente anunciado continua sendo: " + listaOld[0][0] + " - " + listaOld[0][1])
    
    else:
        print("O site retornou código de status: " + str(statuscodenumber))

    time.sleep(timesleep)