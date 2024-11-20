''' Sistema bancário com customTkinter '''
from datetime import datetime
import customtkinter as ctk


class ContasIterador:
    ''' Iterador de contas '''
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError as exc:
            raise StopIteration from exc
        finally:
            self._index += 1

class Usuario:
    ''' Classe de Usuario '''
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        ''' função usada para realizar transações '''
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Você excedeu o número de transações para hoje!")
            return
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        ''' Função usada para adicionar contas '''
        self.contas.append(conta)

class PessoaFisica(Usuario):
    ''' classe de pessoa fisica '''

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    ''' classe de conta '''
    def __init__(self, numero, usuario):
        self._agencia = "0001"
        self._numero = numero
        self._saldo = 0
        self._usuario = usuario
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, usuario):
        ''' função para inserir nova conta'''
        return cls(numero, usuario)

    @property
    def agencia(self):
        ''' função para retornar agência '''
        return self._agencia

    @property
    def numero(self):
        ''' função para retornar numero da conta'''
        return self._numero

    @property
    def saldo(self):
        ''' função para retornar saldo '''
        return self._saldo

    @property
    def usuario(self):
        ''' função para retornar usuario '''
        return self._usuario

    @property
    def historico(self):
        ''' função para retornar historico da conta '''
        return self._historico

    def sacar(self, valor):
        ''' função para sacar '''
        saldo = self.saldo
        valor_excedido = valor > saldo

        if valor_excedido:
            print("Operação falhou! Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("Operação realizada com sucesso!")
            return True

        else:
            print(f"Operação falhou! Valor informado ({valor}) é inválido.")
        return False

    def depositar(self, valor):
        ''' função para depositar '''
        if valor > 0:
            self._saldo += valor
            print("Operação realizada com sucesso!")

        else:
            print("Operação falhou! Valor informado é inválido.")
            return False
        return True

class ContaCorrente(Conta):
    ''' classe de conta corrente'''
    def __init__(self, numero, usuario, limite=500, limite_saque=3):
        super().__init__(numero, usuario)
        self.limite = limite
        self.limite_saque = limite_saque

    @classmethod
    def nova_conta(cls, numero, usuario, limite=500, limite_saque=3):
        return cls(numero, usuario, limite, limite_saque)

    def sacar(self, valor):
        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if transacao["tipo"] == "Saque"
        ])
        limite_excedido = valor > self.limite
        excedeu_limite_saque = numero_saques >= self.limite_saque

        if limite_excedido:
            print("Operação falhou! Limite de saque excedido.")
        elif excedeu_limite_saque:
            print(
                f"Operação falhou! Número máximo de saques excedido ({self.limite_saque}"
            )
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.usuario.nome}
        """

class Historico:
    ''' classe do historico '''
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        ''' historico de transações '''
        return self._transacoes

    def adicionar_transacao(self, transacao):
        ''' adicionar transações ao historico'''
        self._transacoes.append(
        {
          "tipo": transacao.__class__.__name__,
          "valor": transacao.valor,
          "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
      )

    def gerar_relatorio(self, tipo_transacao=None):
        ''' função para gerar relatorio do historico '''
        for transacao in self.transacoes:
            if(tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower()):
                yield transacao

    def transacoes_do_dia(self):
        ''' função que armazena as transações do dia '''
        data_atual = datetime.now().date()
        transacoes =[]
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_transacao == data_atual:
                transacoes.append(transacao)
        return transacoes

class Transacao:
    ''' classe para transacao '''
    @property
    def valor(self):
        ''' função para valor '''

    @classmethod
    def registrar(self, conta):
        ''' função para registrar '''

class Deposito(Transacao):
    ''' classe para deposito '''
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    ''' classe para saque '''
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor


    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(funcao):
    ''' função para fazer logs de transações '''
    def wrapper(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        print(f"{datetime.now()}: {funcao.__name__.upper()}")
        return resultado
    return wrapper

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(usuario):
    ''' função para pesquisar conta de usuarios '''
    if not usuario.contas:
        print("Cliente não possui conta!")
        return
    return usuario.contas[0]

# Front-end do sistema bancario
usuarios = []
contas = []

def criar_usuario_interface():
    '''função interface para criar usuarios '''
    def salvar_usuario():
        cpf = cpf_entry.get()
        nome = nome_entry.get()
        nascimento = nascimento_entry.get()
        endereco = endereco_entry.get()

        cliente = filtrar_usuario(cpf, usuarios)

        if cliente:
            resultado_label.configure(text="CPF já cadastrado!", text_color="red")

        cliente = PessoaFisica(nome=nome, data_nascimento=nascimento, cpf=cpf, endereco=endereco)
        usuarios.append(cliente)

        resultado_label.configure(text="Usuário criado com sucesso!", text_color="green")

    criar_usuario_window = ctk.CTkToplevel()
    criar_usuario_window.title("Novo Usuário")

    ctk.CTkLabel(criar_usuario_window, text="CPF (somente número):").pack(pady=5)
    cpf_entry = ctk.CTkEntry(criar_usuario_window)
    cpf_entry.pack(pady=5)

    ctk.CTkLabel(criar_usuario_window, text="Nome Completo:").pack(pady=5, padx=200)
    nome_entry = ctk.CTkEntry(criar_usuario_window)
    nome_entry.pack(pady=5)

    ctk.CTkLabel(criar_usuario_window, text="Data de Nascimento (dd-mm-aaaa):").pack(pady=5)
    nascimento_entry = ctk.CTkEntry(criar_usuario_window)
    nascimento_entry.pack(pady=5)

    ctk.CTkLabel(criar_usuario_window, text="Endereço (logradouro, nro - bairro - cidade/sigla estado):").pack(pady=5)
    endereco_entry = ctk.CTkEntry(criar_usuario_window)
    endereco_entry.pack(pady=5)

    resultado_label = ctk.CTkLabel(criar_usuario_window, text="")
    resultado_label.pack(pady=10)

    salvar_button = ctk.CTkButton(criar_usuario_window, text="Criar usuario", command=salvar_usuario)
    salvar_button.pack(pady=10)

def criar_conta_interface():
    ''' função interface para criar conta '''
    def salvar_conta():
        cpf = cpf_entry.get()
        usuario = filtrar_usuario(cpf, usuarios)
        numero_conta = len(contas) + 1

        if not usuario:
            resultado_label.configure(text="Usuario não encontrado!", text_color="red")

        conta = ContaCorrente.nova_conta(usuario=usuario, numero=numero_conta)
        contas.append(conta)
        usuario.contas.append(conta)
        resultado_label.configure(text="Conta criada com sucesso!", text_color="green")

    criar_conta_window = ctk.CTkToplevel()
    criar_conta_window.title("Nova Conta")

    ctk.CTkLabel(criar_conta_window, text="CPF:").pack(pady=5, padx=200)
    cpf_entry = ctk.CTkEntry(criar_conta_window)
    cpf_entry.pack(pady=5)

    resultado_label = ctk.CTkLabel(criar_conta_window, text="")
    resultado_label.pack(pady=10)

    salvar_button = ctk.CTkButton(criar_conta_window, text="Criar conta", command=salvar_conta)
    salvar_button.pack(pady=10)

def listar_contas_interface():
    """Interface para listar as contas."""
    listar_contas_window = ctk.CTkToplevel()
    listar_contas_window.title("Listar Contas")
    listar_contas_window.geometry("400x400")

    ctk.CTkLabel(listar_contas_window, text="Contas Registradas", font=("Arial", 16)).pack(pady=10)

    if not contas:
        ctk.CTkLabel(listar_contas_window, text="Nenhuma conta cadastrada.", font=("Arial", 12)).pack(pady=20)
    else:
        textbox = ctk.CTkTextbox(listar_contas_window, width=380, height=300)
        textbox.pack(pady=10)

        for conta in contas:
            titular = next((usuario.nome for usuario in usuarios if usuario.cpf == conta.usuario.cpf), "Desconhecido")
            texto_conta = (
                f"Agência: {conta.agencia}\n"
                f"Conta: {conta.numero}\n"
                f"Titular: {titular}\n"
                "--------------------------------\n"
            )
            textbox.insert("end", texto_conta)

        # Torna o texto apenas de leitura
        textbox.configure(state="disabled")


def depositar_interface():
    ''' função interface para depositar '''
    def salvar_deposito():
        cpf = cpf_entry.get()
        valor = valor_entry.get()

        try:
            valor = float(valor)
        except ValueError:
            resultado_label.configure(text="Valor inválido!", text_color="red")
            return

        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            resultado_label.configure(text="Usuario não encontrado!", text_color="red")

        transacao = Deposito(valor=valor)
        conta = recuperar_conta_cliente(usuario)

        if conta:
            usuario.realizar_transacao(conta, transacao)
            resultado_label.configure(text="Deposito concluido com sucesso!", text_color="green")
        else:
            resultado_label.configure(text="Conta não encontrada", text_color="red")

    deposito_window = ctk.CTkToplevel()
    deposito_window.title("Deposito")

    ctk.CTkLabel(deposito_window, text="CPF:").pack(pady=5)
    cpf_entry = ctk.CTkEntry(deposito_window)
    cpf_entry.pack(pady=5)

    ctk.CTkLabel(deposito_window, text="Valor de deposito:").pack(pady=5, padx=200)
    valor_entry = ctk.CTkEntry(deposito_window)
    valor_entry.pack(pady=5)

    resultado_label = ctk.CTkLabel(deposito_window, text="")
    resultado_label.pack(pady=10)

    salvar_button = ctk.CTkButton(deposito_window, text="Depositar", command=salvar_deposito)
    salvar_button.pack(pady=10)

def sacar_interface():
    ''' função interface para sacar '''
    def salvar_saque():
        cpf = cpf_entry.get()
        valor = valor_entry.get()

        try:
            valor = float(valor)
        except ValueError:
            resultado_label.configure(text="Valor inválido!", text_color="red")
            return

        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            resultado_label.configure(text="Usuario não encontrado!", text_color="red")

        transacao = Saque(valor=valor)
        conta = recuperar_conta_cliente(usuario)

        if conta:
            usuario.realizar_transacao(conta, transacao)
            resultado_label.configure(text="Saque concluido com sucesso!", text_color="green")
        else:
            resultado_label.configure(text="Saque não encontrada", text_color="red")

    saque_window = ctk.CTkToplevel()
    saque_window.title("Saque")

    ctk.CTkLabel(saque_window, text="CPF:").pack(pady=5)
    cpf_entry = ctk.CTkEntry(saque_window)
    cpf_entry.pack(pady=5)

    ctk.CTkLabel(saque_window, text="Valor de saque:").pack(pady=5, padx=200)
    valor_entry = ctk.CTkEntry(saque_window)
    valor_entry.pack(pady=5)

    resultado_label = ctk.CTkLabel(saque_window, text="")
    resultado_label.pack(pady=10)

    salvar_button = ctk.CTkButton(saque_window, text="Sacar", command=salvar_saque)
    salvar_button.pack(pady=10)

def extrato_interface():
    ''' função interface para extrato'''
    def exibir_extrato():
        cpf = cpf_entry.get()
        usuario = filtrar_usuario(cpf, usuarios)

        if not usuario:
            resultado_label.configure(text="Cliente não encontrado!", text_color="red")
            return

        conta = recuperar_conta_cliente(usuario)
        if not conta:
            resultado_label.configure(text="Conta não encontrada!", text_color="red")
            return

        extrato = ""
        existe_transacao = False
        for transacao in conta.historico.gerar_relatorio():
            existe_transacao = True
            extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

        if not existe_transacao:
            extrato = "Não foram realizadas movimentações."

        extrato_label.configure(text=extrato)
        saldo_label.configure(text=f"Saldo: R$ {conta.saldo:.2f}")

    extrato_window = ctk.CTkToplevel()
    extrato_window.title("Extrato")

    ctk.CTkLabel(extrato_window, text="CPF:").pack(pady=5)
    cpf_entry = ctk.CTkEntry(extrato_window)
    cpf_entry.pack(pady=5)

    resultado_label = ctk.CTkLabel(extrato_window, text="")
    resultado_label.pack(pady=10)

    extrato_button = ctk.CTkButton(extrato_window, text="Exibir Extrato", command=exibir_extrato)
    extrato_button.pack(pady=10)

    extrato_label = ctk.CTkLabel(extrato_window, text="", font=("Arial", 12), anchor="w", justify="left")
    extrato_label.pack(pady=30, padx=50)

    saldo_label = ctk.CTkLabel(extrato_window, text="", font=("Arial", 12), anchor="w", justify="left")
    saldo_label.pack(pady=10, padx=10)

def janela_principal():
    ''' Janela inicial do sistema '''
    root = ctk.CTk()
    root.title("Sistema Bancário")
    root.geometry("400x450")

    ctk.CTkLabel(root, text="Sistema Bancário", font=("Arial", 18)).pack(pady=20)

    ctk.CTkButton(root, text="Novo Usuário", command=criar_usuario_interface).pack(pady=10)
    ctk.CTkButton(root, text="Nova Conta", command=criar_conta_interface).pack(pady=10)
    ctk.CTkButton(root, text="Listar Contas", command=listar_contas_interface).pack(pady=10)
    ctk.CTkButton(root, text="Depositar", command=depositar_interface).pack(pady=10)
    ctk.CTkButton(root, text="Sacar", command=sacar_interface).pack(pady=10)
    ctk.CTkButton(root, text="Extrato", command=extrato_interface).pack(pady=10)
    ctk.CTkButton(root, text="Sair", command=root.destroy).pack(pady=20)

    root.mainloop()

janela_principal()
