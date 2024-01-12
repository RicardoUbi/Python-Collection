import pyautogui
import pandas as pd
import time

# Variaveis
link = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"

email = "ricardofilho@gmail.com"
senha = "123456789"

tabela = pd.read_csv("produtos.csv")


pyautogui.PAUSE = 1

pyautogui.press("win")

pyautogui.write("chrome")

pyautogui.press("enter")

pyautogui.write(link)

pyautogui.press("enter")

time.sleep(3)

pyautogui.click(x=649, y=374) #Tela de Login

pyautogui.write(email)
pyautogui.press("tab")
pyautogui.write(senha)

pyautogui.press("enter")

for linha in tabela.index:

    pyautogui.click(x=604, y=255) #Tela de cadastro

    codigo = tabela.loc[linha, "codigo"] 

    pyautogui.write(codigo)
    pyautogui.press("tab")

    pyautogui.write(tabela.loc[linha, "marca"])
    pyautogui.press("tab")  


    pyautogui.write(tabela.loc[linha, "tipo"])
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "categoria"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "preco_unitario"]))
    pyautogui.press("tab")

    pyautogui.write(str(tabela.loc[linha, "custo"]))
    pyautogui.press("tab")

    obs = tabela.loc[linha, "obs"]
    if not pd.isna(obs):
        pyautogui.write(obs)
    
    pyautogui.press("tab")
    pyautogui.press("enter")

    pyautogui.scroll(50000)