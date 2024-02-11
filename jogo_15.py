
import numpy as np
from queue import Queue
import time
import copy
import sys
import heapq

class jogo:

# Inicializacao
    def __init__(self):
        print("")
        print(" ________________________________")
        print("|         Jogo dos 15            |")
        print("|--------------------------------|")
        print("|        Deseja jogar?           |")
        print("|       1.Sim!   2.Não           |")
        print("|________________________________|")
        resposta=int(input())
        if resposta==1:
            print("Você escolheu jogar!\nInsira a sua configuração inicial.")
            n_inicial = list(map(int, input().split()))
            print("Agora insira a sua configuração final.")
            n_final = list(map(int, input().split()))
            self.final=n_final
        #Criacao de Matrizes
            matriz_i=np.array(n_inicial).reshape(4,4)
            self.matriz=matriz_i

            matriz_f=np.array(n_final).reshape(4,4)
            self.matrizfinal=matriz_f
            print("\nSerá possível chegar à configuração final a partir da configuração inicial?")
            print("Sim é!\n") if  self.isSolvable(n_inicial, n_final, matriz_i, matriz_f) else print("Não é...")
            if self.isSolvable(n_inicial, n_final, matriz_i, matriz_f):
                print("Escolha o modo de jogo:\n1.Iterativa em Profundidade Limitada\n2.A*\n3.Greedy\n4.Busca em Largura\n5.Busca em profundidade\n6.Sair")
                escolha=int(input())

                if escolha==1: # DLS - ITERATIVA EM PROFUNDIDADE LIMITADA
                    start = time.time()
                    res,nos=self.idfs(matriz_i, matriz_f)
                    end = time.time()
                    if len(res)!=0:
                        print("Jogo Resolvido!")
                        print(self.matrizfinal)
                        print("Caminho percorrido:")
                        print(res[0])
                        print("Número de nós:")
                        print(nos)
                        print("Profundidade:")
                        print(res[1])
                        print("Tempo de execução: %f segundos" % (end-start))
                        jogo()


                if escolha==2: # A*
                    print("Qual heurística quer utilizar:\n  1.Somatório do número de peças fora do lugar\n  2.Manhattan Distance")
                    heu=int(input())
                    if heu==1:
                        start = time.time()
                        nos, caminho=self.star_somatorio(matriz_i)
                        end = time.time()
                        print("Jogo Resolvido!")
                        print(self.matrizfinal)
                        print("Caminho percorrido:")
                        print(caminho)
                        print("Número de nós:")
                        print(nos)
                        print("Profundidade:")
                        print(len(caminho))
                        print("Tempo de execução: %f segundos" % (end-start))
                        jogo()
                    if heu==2:
                        start = time.time()
                        nos, caminho=self.star_manhattan(matriz_i)
                        end = time.time()
                        print("Jogo Resolvido!")
                        print(self.matrizfinal)
                        print("Caminho percorrido:")
                        print(caminho)
                        print("Número de nós:")
                        print(nos)
                        print("Profundidade:")
                        print(len(caminho))
                        print("Tempo de execução: %f segundos" % (end-start))
                        jogo()


                if escolha==3: # GULOSA
                    print("Qual heurística quer utilizar:\n  1.Somatório do número de peças fora do lugar\n  2.Manhattan Distance")
                    heu=int(input())
                    if heu==1:
                        start = time.time()
                        nos, caminho=self.greedy_somatorio(matriz_i)
                        end = time.time()
                        print("Jogo Resolvido!")
                        print(self.matrizfinal)
                        print("Caminho percorrido:")
                        print(caminho)
                        print("Número de nós:")
                        print(nos)
                        print("Profundidade:")
                        print(len(caminho))
                        print("Tempo de execução: %f segundos" % (end-start))
                        jogo()


                    if heu==2:
                        start = time.time()
                        nos, caminho=self.greedy_manhattan(matriz_i)
                        end = time.time()
                        print("Jogo Resolvido!")
                        print(self.matrizfinal)
                        print("Caminho percorrido:")
                        print(caminho)
                        print("Número de nós:")
                        print(nos)
                        print("Profundidade:")
                        print(len(caminho))
                        print("Tempo de execução: %f segundos" % (end-start))
                        jogo()

                if escolha==4: #BUSCA EM LARGURA
                    start = time.time()
                    res,nos = self.bfs(matriz_i)
                    end = time.time()
                    print("Jogo Resolvido!")
                    print(res[0])
                    print("Caminho percorrido:")
                    print(res[1])
                    print("Número de nós:")
                    print(nos)
                    print("Profundidade:")
                    print(len(res[1]))
                    print("Tempo de execução: %f segundos" % (end-start))
                    jogo()

                if escolha==5: #BUSCA EM PROFUNDIDADE
                    start = time.time()
                    res,nos=self.dfs(matriz_i)
                    end = time.time()
                    print("Jogo Resolvido!")
                    print(res[0])
                    print("Caminho percorrido:")
                    print(res[1])
                    print("Número de nós:")
                    print(nos)
                    print("Profundidade:")
                    print(len(res[1]))
                    print("Tempo de execução: %f segundos" % (end-start))
                    jogo()
                if escolha==6:
                    print("")

        else:
            print("")



#Resolubilidade do jogo
    # Para determinar se a configuracao do puzzle e possivel precisamos de dois termos:
    # inversoes: se um par (a,b) em que a>b esta na posicao incorreta
    # polaridade: se o numero total de inversoes e par(puzzle possivel) ou impar(puzzle impossivel)

    def inversoes(self,arr):
        N=4
        inv_count = 0
        for i in range(N * N - 1):
            for j in range(i + 1,N * N):# conta os pares(arr[i], arr[j]) tal que
                if (arr[i] > arr[j]) and arr[i]!=0 and arr[j]!=0:  # i < j e arr[i] > arr[j]
                    inv_count+=1
        return inv_count

    def findXPosition(self,puzzle): # encontra a posicao do espaco branco, 0
        N=4
        for i in range(N): # comeca em cima à direita da matriz
            for j in range(N ):
                if (puzzle[i][j] == 0):
                    return i
                #N-i

    def condI(self,inv,row): #verifica a configuracao inicial
        if (inv%2==0 and row%2!=0) or (inv%2!=0 and row%2==0):
            return True
        return False

    def isSolvable(self,inicial,final, matrizI,matrizF):
        N=4
        inicial_inv =self.inversoes(inicial)# Count inversoes dos vetores do input
        final_inv=self.inversoes(final)#count das inversoes da final
        inicial_blankRow=self.findXPosition(matrizI) #coluna do zero na inicial
        final_blankRow=self.findXPosition(matrizF)# coluna do zero na final

        CondI= self.condI(inicial_inv, inicial_blankRow)
        CondF = self.condI(final_inv, final_blankRow) #condicao final

        if (CondI and CondF) or(not CondI and not CondF) : #se ambas forem verdadeiras ou ambas falsas, entao e possivel
            return True
        return False # se tiverem valores logicos diferentes, nao e possivel


# Jogadas

    def avb_moves(self, matriz_curr):
        branco= self.pos_branco(matriz_curr)
        moves=[]
        if (branco[0]==0):
            moves.append('b')
        elif(branco[0]==3):
            moves.append('c')
        else:
            moves.append('c')
            moves.append('b')
        if (branco[1]==0):
            moves.append('d')
        elif(branco[1]==3):
            moves.append('e')
        else:
            moves.append('d')
            moves.append('e')
        return moves

    def pos_branco(self, matriz_curr):
        b = np.where(matriz_curr==0)
        return b


    def do_move(self,jogada, matriz_curr):
        blank=self.pos_branco(matriz_curr)
        if(jogada=='d'):
            matriz_curr[blank[0],blank[1]]=matriz_curr[blank[0],blank[1]+1]
            matriz_curr[blank[0],blank[1]+1]=0
        if(jogada=='e'):
            matriz_curr[blank[0],blank[1]]=matriz_curr[blank[0],blank[1]-1]
            matriz_curr[blank[0],blank[1]-1]=0
        if(jogada=='c'):
            matriz_curr[blank[0],blank[1]]=matriz_curr[blank[0]-1,blank[1]]
            matriz_curr[blank[0]-1,blank[1]]=0
        if(jogada=='b'):
            matriz_curr[blank[0],blank[1]]=matriz_curr[blank[0]+1,blank[1]]
            matriz_curr[blank[0]+1,blank[1]]=0
        return matriz_curr


#Heuristica
    def somatorio(self,matriz_curr,mat_fim):
        soma=0
        for i in range(4):
            for j in range(4):
                if((matriz_curr[i][j] != mat_fim[i][j]) and (matriz_curr[i][j]!=0)):
                    soma += 1
        return soma

    def manhattan(self,matriz_curr, matriz_final):
        sum=0
        for i in range(1,16):
            posat = np.where(matriz_curr==i)
            posfin = np.where(matriz_final==i)
            sum = sum + (abs(posat[0]-posfin[0]) + abs(posat[1]-posfin[1]))
        return sum


#Greedy  com heuristica somatorio
#heapq.heappush(fila,item): coloca item na fila
    def greedy_somatorio(self,matriz):
        fila=[]
        percurso=[]
        verificados=set()
        heapq.heappush(fila, (self.somatorio(self.matriz, self.matrizfinal),(matriz.tolist(), percurso))) # insere na fila o somatorio, matriz, e percurso dessa matriz
        while len(fila)!=0: #enquanto nao estiver vazia
            lista=heapq.heappop(fila)
            arrays=lista[1]
            matriz_curr=np.array(arrays[0])
            caminho=arrays[1]

            if np.array_equal(matriz_curr, self.matrizfinal):
                return len(verificados),caminho

            if matriz_curr.tobytes() in verificados:
                continue

            verificados.add(matriz_curr.tobytes())
            moves=self.avb_moves(matriz_curr)
            mem_percurso = copy.deepcopy(caminho)
            mem_matriz=copy.deepcopy(matriz_curr)

            for i in moves:
                matriz_curr= copy.deepcopy(mem_matriz)
                caminho = copy.deepcopy(mem_percurso)
                caminho.append(i)
                sucessora = self.do_move(i, matriz_curr)

                if sucessora.tobytes() in verificados:
                    continue

                custo=self.somatorio(sucessora, self.matrizfinal)
                heapq.heappush(fila,(custo,(sucessora.tolist(), caminho)))

#Greedy com heuristica manhattan
    def greedy_manhattan(self,matriz):
        fila=[]
        percurso=[]
        verificados=set()
        heapq.heappush(fila, (self.manhattan(self.matriz, self.matrizfinal),(matriz.tolist(), percurso)))
        while len(fila)!=0: #enquanto nao estiver vazia
            lista=heapq.heappop(fila)
            arrays=lista[1]
            matriz_curr=np.array(arrays[0])
            caminho=arrays[1]
            if np.array_equal(matriz_curr, self.matrizfinal):
                return len(verificados),caminho

            if matriz_curr.tobytes() in verificados:
                continue

            verificados.add(matriz_curr.tobytes())
            moves=self.avb_moves(matriz_curr)
            mem_percurso = copy.deepcopy(caminho)
            mem_matriz=copy.deepcopy(matriz_curr)
            for i in moves:
                matriz_curr= copy.deepcopy(mem_matriz)
                caminho = copy.deepcopy(mem_percurso)
                caminho.append(i)
                sucessora = self.do_move(i, matriz_curr)
                if sucessora.tobytes() in verificados:
                    continue

                custo=self.manhattan(sucessora, self.matrizfinal)
                heapq.heappush(fila,(custo,(sucessora.tolist(), caminho)))


# A*com heuristica somatorio
    def star_somatorio(self,matriz):
        fila=[]
        percurso=[]
        verificados=set()
        heapq.heappush(fila, (self.somatorio(self.matriz, self.matrizfinal),(matriz.tolist(), percurso))) # insere na fila o somatorio, matriz, e percurso dessa matriz
        while len(fila)!=0: #enquanto nao estiver vazia
            lista=heapq.heappop(fila)
            valor=lista[0]
            arrays=lista[1]
            matriz_curr=np.array(arrays[0])
            caminho=arrays[1]
            if np.array_equal(matriz_curr, self.matrizfinal):
                return len(verificados),caminho

            if matriz_curr.tobytes() in verificados:
                continue

            verificados.add(matriz_curr.tobytes())
            moves=self.avb_moves(matriz_curr)
            mem_percurso = copy.deepcopy(caminho)
            mem_matriz=copy.deepcopy(matriz_curr)
            for i in moves:
                matriz_curr= copy.deepcopy(mem_matriz)
                caminho = copy.deepcopy(mem_percurso)
                caminho.append(i)
                sucessora = self.do_move(i, matriz_curr)
                if sucessora.tobytes() in verificados:
                    continue
                # nos+=1
                custo=self.somatorio(sucessora, self.matrizfinal) + valor
                heapq.heappush(fila,(custo,(sucessora.tolist(), caminho)))

# A* com heuristica somatorio
    def star_manhattan(self,matriz):
        fila=[]
        percurso=[]
        verificados=set()
        heapq.heappush(fila, (self.manhattan(self.matriz, self.matrizfinal),(matriz.tolist(), percurso))) # insere na fila o somatorio, matriz, e percurso dessa matriz
        while len(fila)!=0: #enquanto nao estiver vazia
            lista=heapq.heappop(fila)
            valor=lista[0]
            arrays=lista[1]
            matriz_curr=np.array(arrays[0])
            caminho=arrays[1]
            if np.array_equal(matriz_curr, self.matrizfinal):
                return len(verificados),caminho

            if matriz_curr.tobytes() in verificados:
                continue

            verificados.add(matriz_curr.tobytes())
            moves=self.avb_moves(matriz_curr)
            mem_percurso = copy.deepcopy(caminho)
            mem_matriz=copy.deepcopy(matriz_curr)
            for i in moves:
                matriz_curr= copy.deepcopy(mem_matriz)
                caminho = copy.deepcopy(mem_percurso)
                caminho.append(i)
                sucessora = self.do_move(i, matriz_curr)
                if sucessora.tobytes() in verificados:
                    continue
                custo=self.manhattan(sucessora, self.matrizfinal) + valor
                heapq.heappush(fila,(custo,(sucessora.tolist(), caminho)))

# Busca em Largura
    def bfs(self, matriz_curr):
        # Utilizar fila
        #Tenho uma lista que conterá as matrizes que ja foram "visitadas". Terei uma fila com conterá todos os estados
         #com os diferentes movimentos feitos a partir da matriz anterior. Enquanto a matriz nao for equivalente à matriz final
         #fazer este processo ate chegar à final.
         #ficamos sempre com o caminho mais curto.

        verificados = set()  # conjunto para as matrizes que ja foram verificadas
        fila_estados = Queue(maxsize=0)  # cria uma fila para as matrizes sucessoras
        caminho = Queue(maxsize=0)  # cria uma fila que para o caminho feito ate a matriz correspondente
        mem = copy.deepcopy(matriz_curr)  # memoriza a matriz atual
        a_verificar = copy.deepcopy(mem)
        ret = []  # retorno
        while not np.array_equal(a_verificar, self.matrizfinal): # enquanto a matriz nao for a final

            if a_verificar.tobytes() not in verificados:# se a matriz ainda não foi verificada
                moves = self.avb_moves(a_verificar)  # averigua os movs possiveis da matriz
                verificados.add(a_verificar.tobytes())  # coloca a matriz que esta a ser verificada na lista

                if caminho.empty(): # para o inicio
                    percurso = []
                else:
                    percurso = caminho.get() # para quando ja ha caminhos

                mem_percurso = copy.deepcopy(percurso)
                for i in moves:  # percorre os moves possiveis
                    a_verificar = copy.deepcopy(mem)
                    percurso = copy.deepcopy(mem_percurso)
                    percurso.append(i)
                    sucessora = self.do_move(i, a_verificar)

                    if not np.array_equal(sucessora, self.matrizfinal): # se nao for a final
                        if sucessora.tobytes() not in verificados: # se ainda nao foi verificada
                            fila_estados.put(sucessora)
                            caminho.put(percurso)
                    else:
                        ret.append(sucessora)
                        ret.append(percurso)
                        return ret , len(verificados)

            if not fila_estados.empty():
                mem = fila_estados.get()
                a_verificar = copy.deepcopy(mem)
            else:
                break

        return ret, len(verificados)



# Busca em Profundidade
    def dfs(self,matriz_curr):

        verificados=set()# para matrizes já verificadas
        ret=[] #para retorno
        pilha=[] #para os estados
        caminho=[] #para o caminho
        mem = copy.deepcopy(matriz_curr)  # memoriza a matriz atual
        a_verificar = copy.deepcopy(mem)

        while not np.array_equal(a_verificar, self.matrizfinal): # enquanto a matriz nao for a final

            if a_verificar.tobytes() not in verificados:# se a matriz ainda não foi verificada
                moves = self.avb_moves(a_verificar)  # averigua os movs possiveis da matriz
                verificados.add(a_verificar.tobytes())  # coloca a matriz que esta a ser verificada na lista

                if len(caminho)==0: # para o inicio
                    percurso = []
                else:
                    percurso = caminho.pop() # para quando ja ha caminhos

                mem_percurso = copy.deepcopy(percurso)
                for i in moves:  # percorre os moves possiveis
                    a_verificar = copy.deepcopy(mem)
                    percurso = copy.deepcopy(mem_percurso)
                    percurso.append(i)
                    sucessora = self.do_move(i, a_verificar)

                    if not np.array_equal(sucessora, self.matrizfinal): # se nao for a final
                        if sucessora.tobytes() not in verificados: # se ainda nao foi verificada
                            pilha.append(sucessora)
                            caminho.append(percurso)
                    else:
                        ret.append(sucessora)
                        ret.append(percurso)
                        return ret, len(verificados)

            if len(pilha)!=0:
                mem = pilha.pop()
                a_verificar = copy.deepcopy(mem)
            else:
                break

        return ret, len(verificados)

#Iterative-Deepening Search
    def idfs(self, matriz_i, matriz_f):
        l = 0
        resultado, nos = self.dls(matriz_i, matriz_f, l)
        while(resultado[1] == None):
            l+=1
            resultado, nos = self.dls(matriz_i, matriz_f, l)

        return resultado, nos

#Depth-Limited Search
    def dls(self, matriz_i, matriz_f, depth):
        res=[None, None] #Resposta
        stack = [] #Pilha com as matrizes
        prof = [] #Pilha com as profundidades associadas a cada matriz
        pmoves = [] #Pilha que guarda as jogadas que dão origem a matrizes ainda não verificadas
        caminho = [] #Guardar o caminho da matriz até à matriz final
        verificadas = set() #Conjunto das matrizes ja verificadas

        n=0
        d=0 #Profundidade da matriz inicial é zero

        if(depth == 0):
            if np.array_equal(matriz_i, matriz_f):
                    res = [None, 0]
            return res, 1

        stack.append(matriz_i) #Adicionar a matriz inicial à pilha
        prof.append(d)


        #Começar o ciclo até a pilha ficar vazia ou até encontrar a solução
        while (bool(stack) == True):
            #Se chegou à depth maxima deixar de aprofundar, ou seja, retirar de todas as pilhas as matrizes/jogadas de profundidade 'depth' para
            # depois continuar o ciclo num nível anterior.
            if (d == depth): #Se chegar à depth máxima:
                for i in range(n):
                    prof.pop()
                    matriz = stack.pop()
                    aux = pmoves.pop()
                    if(np.array_equal(matriz, matriz_f)):
                        caminho.append(aux)   #Como não aprofunda mais, só vale a pena adicionar a jogada ao caminho se der origem à matriz final.
                        res[0]=caminho
                        res[1]=d
                        return res, len(verificadas)
                    verificadas.add(matriz.tobytes())
                if(bool(caminho)):
                    caminho.pop() #Tira a jogada que deu origem às jogadas acabadas de retirar

            #Se todos os elementos da pilha forem do nível limite (depth), então foram todos retirados no passo anterior, as listas stack e
            #prof ficam vazias e a solução não foi encontrada, logo:
            if bool(stack) == False:
                break

            if(bool(prof) == True):
                a = d - prof[-1]
                d = prof.pop()
                if(bool(caminho) and a>1):
                    caminho.pop()

            matriz = stack.pop()

            if(bool(pmoves) == True):
                caminho.append(pmoves.pop())

            if(np.array_equal(matriz, matriz_f)):
                res[0]=caminho
                res[1]=d
                return res, len(verificadas)
            verificadas.add(matriz.tobytes())

            moves = self.avb_moves(matriz) #Lista de moves possiveis a partir da matriz
            #print(moves)

            d+=1 #Aumentar a profundidade

            n=0 #Variavél que memoriza o nº de jogadas que dão origem a matrizes ainda não verificadas
            for i in range(len(moves)):
                auxi = copy.deepcopy(matriz)
                m = self.do_move(moves[i],auxi)
                if m.tobytes() not in verificadas:
                    stack.append(m)
                    prof.append(d)
                    pmoves.append(moves[i])
                    n+=1

        return res, len(verificadas) #Se não encontrar solução nesse limite retorna None, None


jogo()
