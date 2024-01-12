import pyautogui
import time

# Você utiliza este codigo auxiliar para conseguir localizar onde o ponteiro do seu mouse se encontra.
# Como utilizar
# Execute o codigo de "auxiliar.py" e vá para a pagina do site da empresa e deixe seu mouse onde pede para escrever seu email
# Você precisara executar este codigo novamente na tela de produtos, onde pede o codigo do produto
# Após conseguir estas variaveis, adicione as coordenadas ao codigo

time.sleep(7)
print(pyautogui.position())