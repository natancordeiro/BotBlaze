# Importações
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import urlparse
import clipboard
import smtplib
import email.message
import os
import schedule

def enviar_email(nome_bot, numero_bot):

    corpo_email = f"""
    <p>Já tirei do Redirect para você, beijos! 😘</p>
    """
    msg = email.message.Message()
    msg['Subject'] = f"{nome_bot}! n°:{numero_bot} foi banido!"
    msg['From'] = 'businessmaster1337ho@gmail.com'
    msg['To'] = 'rodrigo.unity@protonmail.com'
    password = 'pcqqenanswiwtuyb'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    #Login
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To'], 'autofinanciarbryan@gmail.com', 'o.natan1907@gmail.com'], msg.as_string().encode('utf-8'))
    print("Email enviado.")

def main():

    usuario = 'o.natan1907@gmail.com'
    senha = 'Blade653'

    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico)

    print("Iniciando automação...")
    driver.maximize_window()
    driver.get("https://www.app.botconversa.com.br/login")
    sleep(2.5)

    # ---- Login ----
    print("Fazendo Login no BotConversa.")
    driver.find_element(By.NAME, 'email').send_keys(usuario)
    sleep(0.7)

    driver.find_element(By.NAME, 'password').send_keys(senha)
    sleep(0.7)

    driver.find_element(By.XPATH, '//form/div[3]/button[1]').click()
    sleep(3)
    print("\033[32mLogin efetuado com sucesso!\033[m")
    sleep(0.5)

    print("\033[33mVerificando Bots...\033[m")
    # ---- Bots ativos ----
    driver.get('https://www.app.botconversa.com.br')
    sleep(2)

    # abrir bots laterais
    driver.find_element(By.XPATH, '//ul/div').click()

    # pegar numeros, ID, Companhia
    numeros = driver.find_elements(By.CLASS_NAME, 'company-item__text-mail')
    lista_numeros = []
    for numero in numeros:
        id, c, num = numero.text.split()
        lista_numeros.append(num)

    # Acessar os bots 1 por 1
    for numero in lista_numeros:
        driver.get(f"https://www.app.botconversa.com.br/{numero}")
        sleep(2)
        nome = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[1]/ul/div/div/div[2]/div[1]/div[1]').text

    # se não estiver ativo :
        span = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/span')

        if span.text == 'Ativo':
            print(f'\033[32m{nome} Já está ativo.\033[m')
        if span.text == 'Escanear QR CODE':
            print(f'\033[31m{nome} está fora do ar\033[m')
            # ir para campanhas 
            driver.get(f"https://www.app.botconversa.com.br/{numero}/campaigns")
            sleep(2)

            # Botão copiar link
            driver.find_element(By.CSS_SELECTOR, 'button.purple').click()

            # Pegar número do Whats 
            link = clipboard.paste()
            separado = urlparse(link)
            query = separado.query
            igual = query.split('=')
            e = igual[1].split('&')
            zap = e[0]

            zap_formatado = '+{} ({}) {}-{}'.format(zap[:2], zap[2:4], zap[4:9], zap[9:]) 
            print(f'{nome}: {zap_formatado}')

            # entrar página Link
            driver.get('https://botcompany.pro/urlredirect/public/dashboard')
            sleep(2)
            try:
                # Fazer login
                driver.find_element(By.NAME, 'email').send_keys("blade2@gmail.com")
                sleep(0.7)
                driver.find_element(By.NAME, 'password').send_keys("blade2")
                sleep(0.7)
                driver.find_element(By.XPATH, '//form/button').click()
                sleep(3)
            except:
                pass

            driver.get('https://botcompany.pro/urlredirect/public/links')
            sleep(2)
            c = 2 
            
            # Ver os 3 links 10k
            for i in range(0, 3):
                driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/div/div/div[4]/div[2]/div/div[{c}]/div/div[2]/div/div[2]/a').click()
                driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/div/div/div[4]/div[2]/div/div[{c}]/div/div[2]/div/div[2]/div/a[1]').click()
                c += 1
                sleep(1)

                # pegar links
                numeros = []
                inputs = driver.find_elements(By.TAG_NAME, 'input')
                for i in inputs:
                    i.get_attribute('value')
                    if 'whatsapp' in i.get_attribute('value'):
                        numeros.append(i.get_attribute('value'))

                lista_zap = []        
                for n in numeros:
                    w = n.split('=')
                    ws = w[1].split('&')
                    num = ws[0]
                    lista_zap.append(num)
                
                # se o numero do bot for igual ao numero da lista de links:
                for i, n in enumerate(numeros):
                    if zap in n:
                        sleep(3)
                        print(f'\033[035m O Bot {nome} foi identificado no BotCompany!\033[m')
                        salvar = driver.find_element(By.NAME, 'submit')

                        if i == 0:
                            # Substituir o input para depois excluir
                            # pegar numeros[2] e colcoar no topo
                            driver.find_element(By.XPATH, '//*[@id="i-url"]').clear()
                            driver.find_element(By.XPATH, '//*[@id="i-url"]').send_keys(numeros[1])
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[2]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click() 
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)
                                        
                        elif i == 1:
                            # apagar input 2
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[2]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()  
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)
                        
                        elif i == 2:
                            # apagar input 3
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[3]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 3:
                            #apagar input 4
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[4]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 4:
                            #apagar input 5
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[5]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 5:
                            #apagar input 6
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[6]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 6:
                            #apagar input 7
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[7]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 7:
                            #apagar input 8
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[8]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                        elif i == 8:
                            #apagar input 9
                            botao_excluir = driver.find_element(By.XPATH, '//*[@id="rotation-container"]/div/div[9]/div/div/div[2]/button')
                            driver.execute_script("arguments[0].scrollIntoView();", botao_excluir)
                            sleep(1)
                            botao_excluir.click()
                            salvar.click()
                            sleep(2)
                            print(f"\033[032m{nome} foi exluido com sucesso!\033[m")
                            enviar_email(nome, zap_formatado)

                driver.get('https://botcompany.pro/urlredirect/public/links')
    print("\033[31mFluxo encerrado!\033[m")

# A cada 5min faça:
schedule.every(5).seconds.do(main)

while 1:
    schedule.run_pending()
    sleep(1)
