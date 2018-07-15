from collections import deque

f = deque() #Fronteira
counter = 0

class Estado:
    def __init__(self, ilha1, barco, ilha2, acao):
        self.ilha1 = ilha1
        self.barco = barco
        self.ilha2 = ilha2
        self.acao = acao

class Node:
    def __init__(self, atual, anterior):
        self.estadoAtual = atual
        self.nodeAnterior = anterior
        if anterior is None:
            self.custo = 0
        else:
            self.custo = self.nodeAnterior.custo + 1

def possivel(curr_estado, futuro_estado):
    #  i, j,   k, l,    m, n     i2, j2,    k2, l2,    m2, n2
    #Caso não haver mudança.
    if futuro_estado.ilha1 == curr_estado.ilha1 and futuro_estado.barco == curr_estado.barco:
        return 0
    # Se esta "carregando" do lado esquerdo, a sua direita deve ser fixada. Não permitte desvantagem na ilha1.  Remove viagem de uma pessoa só.
    if (futuro_estado.acao == 1) and (curr_estado.ilha2 == futuro_estado.ilha2) and (futuro_estado.ilha1[0] == 0 or (
            futuro_estado.ilha1[0] > 0 and futuro_estado.ilha1[0] >= futuro_estado.ilha1[1])) and ((futuro_estado.ilha1[0] + futuro_estado.ilha1[1] != 0 and futuro_estado.barco[0] + futuro_estado.barco[
            1] > 1) or (futuro_estado.ilha1[0] + futuro_estado.ilha1[1] == 0)):
        if ((futuro_estado.ilha2[0]>0 or futuro_estado.barco[0] >0) and futuro_estado.ilha2[0] + futuro_estado.barco[0] >= futuro_estado.barco[1]+futuro_estado.ilha2[1] ) or (futuro_estado.ilha2[0]==0 and futuro_estado.barco[0]==0):
            return 1
    # Se esta "carregando" do lado direito, a sua esquerda deve ser fixada. Não permitte desvantagem na ilha2.  Remove viagem de duas pessoas.
    if (futuro_estado.acao == -1) and (curr_estado.ilha1 == futuro_estado.ilha1) and (futuro_estado.ilha2[0] == 0 or (
            futuro_estado.ilha2[0] > 0 and futuro_estado.ilha2[0] >= futuro_estado.ilha2[1])):
        if ((futuro_estado.ilha1[0] > 0 or futuro_estado.barco[0] >0) and futuro_estado.ilha1[0] + futuro_estado.barco[0] >= futuro_estado.barco[1]+futuro_estado.ilha1[1] ) or (futuro_estado.ilha1[0]==0 and futuro_estado.barco[0]==0):
            return 1
    return 0

def possivel_2(curr_estado, futuro_estado):
    #  i, j,   k, l,    m, n     i2, j2,    k2, l2,    m2, n2
    #Caso não haver mudança.
    if futuro_estado.ilha1 == curr_estado.ilha1 and futuro_estado.barco == curr_estado.barco:
        return 0
    # Se esta "carregando" do lado esquerdo, a sua direita deve ser fixada. Não permitte desvantagem na ilha1.  Remove viagem de uma pessoa só.
    if (futuro_estado.acao == 1) and (curr_estado.ilha2 == futuro_estado.ilha2) and (futuro_estado.ilha1[0] == 0 or (
            futuro_estado.ilha1[0] > 0 and futuro_estado.ilha1[0] >= futuro_estado.ilha1[1])) and ((futuro_estado.ilha1[0] + futuro_estado.ilha1[1] != 0 and futuro_estado.barco[0] + futuro_estado.barco[
            1] > 1) or (futuro_estado.ilha1[0] + futuro_estado.ilha1[1] == 0)):
        return 1
    # Se esta "carregando" do lado direito, a sua esquerda deve ser fixada. Não permitte desvantagem na ilha2.  Remove viagem de duas pessoas.
    if (futuro_estado.acao == -1) and (curr_estado.ilha1 == futuro_estado.ilha1) and (futuro_estado.ilha2[0] == 0 or (
            futuro_estado.ilha2[0] > 0 and futuro_estado.ilha2[0] >= futuro_estado.ilha2[1])) and (futuro_estado.barco[0] + futuro_estado.barco[1] != 2):
        return 1
    return 0

def verificaRepetidos(curr_node, futuro_state):
    if curr_node.estadoAtual == futuro_state:
        return 1  # Tem repetido
    if curr_node.nodeAnterior is None:
        return 0  # Nao tem repetido
    return verificaRepetidos(curr_node.nodeAnterior, futuro_state)


def possibilidades(curr_node):
    #   i,j   k, l    m, n
    currState = curr_node.estadoAtual
    new_action = -1 * currState.acao
    puss = list()
    for i in range(0, 4):
        for j in range(0, 4):
            for k in range(0, 4 - i):
                for l in range(0, 4 - j):
                    m = 3 - i - k
                    n = 3 - l - j
                    if (k + l <= 2) and (k + l != 0 or i + j == 6 or m + n == 6):
                        futuro = Estado((i, j), (k, l), (m, n), new_action)
                        if possivel_2(currState, futuro) == 1:
                            if verificaRepetidos(curr_node, futuro) == 0:
                                puss.append(Node(futuro, curr_node))
    return puss


def busca_largura(fim):
    curr = f.popleft()
    if curr.estadoAtual.ilha1 == fim.ilha1 and curr.estadoAtual.barco == fim.barco:
        return curr
    puss = possibilidades(curr)
    f.extend(puss)
    return busca_largura(fim)


def print_Solution(node):
    curr = node
    lista = deque()
    while (curr is not None):
        lista.appendleft(curr.estadoAtual)
        curr = curr.nodeAnterior
    printPath(lista)


def printPath(list):
    for x in list:
        print("(", x.ilha1[0], ",", x.ilha1[1], ") (", x.barco[0], ",", x.barco[1], ") (", x.ilha2[0], ",", x.ilha2[1],
              ") ", end='', sep='')
        if (x.acao == -1):
            print("<-")
        else:
            print("->")

#Definicao do Inicio
inicio = Estado((3, 3), (0, 0), (0, 0), -1)
#Definição do Fim
fim = Estado((0, 0), (0, 0), (3, 3), -1)
f.append(Node(inicio, None))
solution = busca_largura(fim)
#Impressão da Solução
print_Solution(solution)
