from collections import deque

#Para mudar a origem e destino, basta mudar a ultima linha do input.txt

f = list()
tabelaHeuristica = list()
tabelaReal = list()
tabelaLinhas = list()
VELOCIDADE = 0.5 #km/ minuto
TROCA_ESTACAO = 4 #4 minutos

class Estado:
    def __init__(self, estacao, linha, sentido):
        self.estacao = estacao
        self.linha = linha
        self.sentido = sentido

class Node:
    def __init__(self, atual, anterior, distancia,distanciaHeuristica):
        self.estadoAtual = atual
        self.nodeAnterior = anterior
        if anterior is None:
            self.distanciaReal=0
            self.tempoReal=0 #COMPLICADO
            self.heuristicaFim= distanciaHeuristica
        else:
            self.distanciaReal = anterior.distanciaReal + distancia
            self.heuristicaFim = distanciaHeuristica
            if anterior.estadoAtual.linha != atual.linha and (anterior.estadoAtual.linha is not None):
                self.tempoReal = anterior.tempoReal + TROCA_ESTACAO + distancia * VELOCIDADE
            else:
                self.tempoReal = anterior.tempoReal + distancia*VELOCIDADE

        self.custoTempo = self.tempoReal + distanciaHeuristica * VELOCIDADE


def print_Solution(node):
    curr = node
    lista = deque()
    while (curr is not None):
        lista.appendleft(curr)
        curr = curr.nodeAnterior
    lista[0].estadoAtual.linha = lista[1].estadoAtual.linha
    printPath(lista)

def printPath(list):
    troca =0
    for x in range(0,len(list)):
        z = len(list)
        if (x==0) or (int(list[x-1].estadoAtual.linha)!=int(list[x].estadoAtual.linha)):
            print("Linha ", list[x].estadoAtual.linha)
            if (troca==1):
                print("+", TROCA_ESTACAO, "minutos")
            troca = 1
        print("Estacao: ", list[x].estadoAtual.estacao, " kms rodados: ",list[x].distanciaReal, " / tempo acumulado: ", list[x].tempoReal, "minutos / tempo rodando: ", list[x].distanciaReal * VELOCIDADE," minutos")

def possibilidades(curr_node,fim):
    estacao = curr_node.estadoAtual.estacao
    linhas_possiveis = list()
    nodesPossiveis = list()
    for x in range(0, len(tabelaLinhas)):
        if str(estacao) in tabelaLinhas[x]:
            linhas_possiveis.append(x)
    for x in linhas_possiveis:
        pos = tabelaLinhas[x].index(str(estacao))
        if (pos == 0) or (pos != len(tabelaLinhas[x]) -1):
            #Ir pra frente
            newEstado = Estado(tabelaLinhas[x][pos+1], x, 1)
            newNode = Node(newEstado, curr_node, real_distance(curr_node.estadoAtual,newEstado),heuristic_distance(fim,newEstado))
            if (contem_repetido(curr_node,newNode) == 0):
                nodesPossiveis.append(newNode)
        if (pos != 0) or (pos == len(tabelaLinhas[x]) -1):
            #Ir pra tras
            newEstado = Estado(tabelaLinhas[x][pos - 1], x, -1)
            newNode = Node(newEstado, curr_node, real_distance(curr_node.estadoAtual, newEstado),
                           heuristic_distance(fim, newEstado))
            if (contem_repetido(curr_node, newNode) == 0):
                nodesPossiveis.append(newNode)

    return nodesPossiveis

def contem_repetido(curr_node, futuro_node):
    if curr_node is None:
        return 0 #Nao tem repetido
    if int(curr_node.estadoAtual.estacao) == int(futuro_node.estadoAtual.estacao):
        return 1  # Tem repetido
    return contem_repetido(curr_node.nodeAnterior, futuro_node)

def a_star(fim):
    curr = f.pop(0)
    #curr = f.popleft()
    if int(curr.estadoAtual.estacao) == int(fim.estacao):
        print_Solution(curr)
        return curr
    poss = possibilidades(curr,fim)
    f.extend(poss)
    f.sort(key= lambda x: x.custoTempo)
    return a_star(fim)

def heuristic_distance(origin, destiny):
    if int(tabelaHeuristica[int(origin.estacao)-1][int(destiny.estacao)-1]) != -1:
        return int(tabelaHeuristica[int(origin.estacao)-1][int(destiny.estacao)-1])
    return int(tabelaHeuristica[int(destiny.estacao)-1][int(origin.estacao)-1])

def real_distance(origin, destiny):
    a = int(tabelaReal[int(origin.estacao)-1][int(destiny.estacao)-1])
    b = int(tabelaReal[int(destiny.estacao)-1][int(origin.estacao)-1])
    c = tabelaReal[int(origin.estacao)-1]
    d = c[int(destiny.estacao) -1]
    if int(tabelaReal[int(origin.estacao)-1][int(destiny.estacao)-1]) != -1:
        return int(tabelaReal[int(origin.estacao)-1][int(destiny.estacao)-1])
    return int(tabelaReal[int(destiny.estacao)-1][int(origin.estacao)-1])

file = open("input.txt")
n_estacoes = int(file.readline())

for i in range (1,n_estacoes+1):
    l = file.readline().rstrip('\n').split()
    tabelaHeuristica.append(l)
file.readline()
for i in range (1,n_estacoes+1):
    l = file.readline().rstrip('\n').split()
    tabelaReal.append(l)
file.readline()

n_linhas = int(file.readline())

for i in range (1,n_linhas+1):
    l = deque(file.readline().rstrip('\n').split())
    tabelaLinhas.append(l)
origem,destino = file.readline().rstrip('\n').split()
origem = int(origem)
destino =int(destino)
startEstado = Estado(origem, None, None)
fim = Estado(destino, None, None)
startNode = Node(startEstado, None, 0,heuristic_distance(startEstado, fim))
f.append(startNode)
a_star(fim)



