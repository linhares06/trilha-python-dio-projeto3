from abc import ABC, abstractmethod

TAMANHO_DATA_NASCIMENTO = 8
TAMANHO_CPF = 11

class Cliente:
    def __init__(self, endereco: str):
        self.endereco: str = endereco
        self.contas: list = []

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self.cpf: str = cpf
        self.nome: str = nome
        self.data_nascimento: str = data_nascimento

    def __str__(self):
        return f'Nome: {self.nome}, CPF: {self.cpf}, Data de Nascimento: {self.data_nascimento}\nEndereço: {self.endereco}'

class Conta:
    def __init__(self, cliente: Cliente, numero: int):
        self._saldo: float = 0
        self._numero: int = numero
        self._agencia: str = '0001'
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return cls(cliente, numero)
    
    def sacar(self, valor: float) -> bool:
        saldo: float = self.saldo
        
        if valor <= 0:
            print('Apenas valores maiores do que 0 são permitidos.')
        elif valor > saldo:
            print('Saldo insuficiente.')
        else:
            self._saldo -= valor
            print(f'Saque de R${valor} realizado com sucesso!')
            return True
        
        return False
    
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print('Apenas valores maiores do que 0 são permitidos.')
            return False
        else:
            self._saldo += valor
            print(f'Deposito de R${valor} realizado com sucesso!')
            return True

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: int = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite: int = limite
        self.limite_saques: int = limite_saques
        self.numero_saques: int = 0
    
    def sacar(self, valor: float) -> bool:

        if self.numero_saques > self.limite_saques:
            print('Limite de saque diário atingido.')
        elif valor > self.limite:
            print(f'O valor do saque é maior do que o limite de R${self.limite} por saque.')
        else:
            self.numero_saques += 1
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'Agência: {self.agencia}, Conta Corrente: {self.numero}, Titular: {self.cliente.nome}, Saldo: {self.saldo:.2f}'

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao'):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta: Conta):
        pass

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def menu():
    menu = '''

[1] Cadastrar Cliente
[2] Cadastrar Conta Corrente
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar Clientes
[7] Listar Contas Correntes
[0] Sair

Opção: '''

    return input(menu)

def main():

    clientes: list = []
    contas: list = []

    while True:

        opcao = menu()

        if opcao == '1':
            criar_cliente(clientes)

        elif opcao == '2':
            criar_conta_corrente(contas, clientes)

        elif opcao == '3':
            transacao(contas, Deposito)

        elif opcao == '4':
            transacao(contas, Saque)

        elif opcao == '5':
            ver_extrato(contas)
        
        elif opcao == '6':
            listar(clientes)

        elif opcao == '7':
            listar(contas)

        elif opcao == '0':
            print('Sair')
            break

        else:
            print('Operação inválida, por favor selecione novament a operação desejada.')

def transacao(contas: list, transacao: Transacao):
    
    try:
        print(transacao.__name__)

        conta: Conta = buscar_conta_por_numero_conta(contas)

        if conta:
            valor: float = float(input('Valor: '))
            transacao(valor).registrar(conta)
        else:
            print('Conta inexistente.')
    
    except ValueError:
        print('Número da conta inválido.')

def ver_extrato(contas: list):

    conta: Conta = buscar_conta_por_numero_conta(contas)

    if conta:
        for transacoes in conta.historico.transacoes:
            tipo, valor = transacoes['tipo'], transacoes['valor']
            print(f'{tipo}: de R${valor:.2f}')
        print(f'Saldo: R${conta.saldo:.2f}')
    else:
        print('Nenhum registro encontrado.')

def validar_digitos(entrada: str, tamanho: int):
    while True:
        digitos: str = input(entrada)

        if digitos.isdigit() and len(digitos) == tamanho:
            digitos_validos: str = digitos
            break
        else:
            print(f"Entrada inválida. Certifique-se de inserir apenas números e ter {tamanho} dígitos.")

    return digitos_validos

def buscar_conta_por_numero_conta(contas: list):
    numero_conta = int(input('Número da conta: '))
    return next((conta for conta in contas if conta.numero == numero_conta), None)

def buscar_cliente_por_cpf(cpf: str, clientes: list):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

def criar_cliente(clientes: list):

    print('***Criação de Cliente do sistema bancario***\n')
    
    cpf = validar_digitos('Insira o CPF: ', TAMANHO_CPF)

    if not buscar_cliente_por_cpf(cpf, clientes):
        nome: str = input('Insira o nome do usuário: ')
        nascimento: str = validar_digitos('Insira a data de nascimento: ', TAMANHO_DATA_NASCIMENTO)
        endereco: str = input('Insira o endereco(Logradouro, nr - bairro - cidade/estado): ')

        cliente: PessoaFisica = PessoaFisica(cpf, nome, nascimento, endereco)
        
        clientes.append(cliente)
        print('Usuário criado com sucesso!')

    else:
        print('CPF já cadastrado.')

def criar_conta_corrente(contas_correntes: list, usuarios: list):

    def gerar_numero_conta():
        if not contas_correntes:
            return 1
        else:
            return contas_correntes[-1].numero + 1

    print('***Criação de conta corrente para o usuário do sistema bancario***\n')
    
    cpf: str = validar_digitos('Insira o CPF do usuário: ', TAMANHO_CPF)

    cliente: Cliente = buscar_cliente_por_cpf(cpf, usuarios)

    if not cliente:
        print('Cliente não cadastrado.')
    else:
        conta_corrente = ContaCorrente.nova_conta(cliente, gerar_numero_conta())
        contas_correntes.append(conta_corrente)
        cliente.contas.append(conta_corrente)
        print('Conta corrente criada com sucesso!')

def listar(lista: list):
    
    if lista:
        for obj in lista:
            print(obj)
    else:
        print('Nenhum registro encontrado.')

main()