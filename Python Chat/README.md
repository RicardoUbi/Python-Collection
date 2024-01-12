# Python Chat

Este é um projeto de Chat Online desenvolvido em Python em conjunto com outras bibliotecas. Foi desenvolvido durante o evento Jornada Python da [Hashtag Programação](https://pages.hashtagtreinamentos.com/).

Nosso objetivo era criar um Chat Online onde as pessoas podem entrar e conversar como se fosse um chat normal, porém se você entrar no chat não vai conseguir visualizar o histórico anterior das conversas, pois a ideia é que seja um chat ao vivo, então só quem está ali na hora vai visualizar as mensagens, caso saia e entre de novo vai visualizar as mensagens a partir do 
momento em que entrou no chat.

## Tecnologias utilizadas:

* [Python](https://www.python.org/): linguagem de programação
* [Flask](https://flask.palletsprojects.com/): Biblioteca usada para construir sites, aplicativos web, API, etc.
* [ Socketio](https://socket.io/): Biblioteca para comunicação entre cliente e um servidor
* [ Simple Websocket](https://pypi.org/project/simple-websocket/): Biblioteca para criar servidores websocket e estabelecer conexões com clientes de forma simples e eficiente


## Imagens:

<div align="center">
  <p>Tela de Inicio </p>
  <img src="imgs/Py-C1.png" alt="Dados Visualização" style="display:block; margin:auto; margin-bottom:20px;">

  <p style="margin-top:20px;">Popup para inserir nome</p>
  <img src="imgs/Py-C2.png" alt="Grafico 1" style="display:block; margin:auto; margin-bottom:20px;">

  <p style="margin-top:20px;">Chat Público</p>
  <img src="imgs/Py-C3.png" alt="Grafico 2" style="display:block; margin:auto;">
</div>


## Como utilizar

1. Clone o repositório:

   ```terminal
   git clone https://github.com/RicardoUbi/Python-Collection.git

   cd Python-Collection

   git config core.sparseCheckout true

   echo "Python Chat/" >> .git/info/sparse-checkout

   git pull origin main


2. Instale as bibliotecas:
   
   ```terminal
    pip install flask
    pip install python-socketio
    pip install simple-websocket

3. Execute o programa

   ```terminal
    python codigo.py
   

### Divirta-se!
   
