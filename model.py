import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._colors = DAO.getColors()
        self._prodotti = []

        self._grafo = nx.Graph()
        self._idMap = {}

        self._bestPath = []
        self._bestLenght = 0



    def buildGraph(self, colore, anno):
        self._grafo.clear()
        self._prodotti = DAO.getProducts(colore)

        self._grafo.add_nodes_from(self._prodotti)

        for p in self._prodotti:
            self._idMap[p.Product_number] = p

        for p1 in self._grafo.nodes:
            for p2 in self._grafo.nodes:
                if p1 != p2:
                    cod1 = p1.Product_number
                    cod2 = p2.Product_number

                    peso = DAO.getEdges(cod1, cod2, anno)

                    if(peso):
                        self._grafo.add_edge(p1, p2, weight=peso[0])




    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getArchiPesoMaggiore(self):
        archi = []

        for (e1, e2) in self._grafo.edges:
            peso = self._grafo[e1][e2]["weight"]
            archi.append((e1, e2, peso))

        archi.sort(key=lambda x:x[2], reverse=True)

        risposta = []

        for i in range(3):
            risposta.append(archi[i])

        return risposta


    def getNumberOne(self, archiBest):
        nodoBest = []
        conto = 0

        nodi = []

        for arco in archiBest:
            nodi.append(arco[0])
            nodi.append(arco[1])

        for nodo in nodi:
            contoNodo = 0

            for nodo2 in nodi:
                if nodo2 == nodo:
                    contoNodo += 1

            if contoNodo > conto and nodo.Product_number not in nodoBest:
                nodoBest = [nodo.Product_number]
                conto = contoNodo

            elif conto == contoNodo and nodo.Product_number not in nodoBest:
                nodoBest.append(nodo.Product_number)

        return nodoBest, conto


    def getPercorso(self, input):
        self._bestPath = []
        self._bestLenght = 0

        # inizio la ricorsione con il nodo passato come parametro e il vicinbo che forma l'arco
        # di peso maggiore
        nodoInizio = self._idMap[input]

        parziale = [nodoInizio]

        archiVicini = []
        for nodo in self._grafo.neighbors(nodoInizio):
            pesoArco = self._grafo[nodoInizio][nodo]["weight"]
            archiVicini.append((nodo, pesoArco))
        archiVicini.sort(key=lambda x: x[1], reverse=True)

        parziale.append(archiVicini[0][0])

        self._ricorsione(parziale)

        return self._bestPath, self._bestLenght

    def _ricorsione(self, parziale):

        # condizione finale, controllo che la lunghezza di parziale sia maggiore della lunghezza migliore
        # ed eventualmente aggiorno, ma non voglio uscire dal ciclo perchè potrei trovare ancora nodi da aggiungere
        # e quindi un percorso potenzialmente più lungo
        if len(parziale) > self._bestLenght:
            self._bestLenght = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # ordino in ordine decrescente di peso tutti i nodi vicini all'ultimo nodo presente in parziale
        archiVicini = []
        for nodo in self._grafo.neighbors(parziale[-1]):
            pesoArco = self._grafo[parziale[-1]][nodo]["weight"]
            archiVicini.append((nodo, pesoArco))
        archiVicini.sort(key=lambda x: x[1], reverse=True)


        # controllo che il primo nodo della lista ordinata formi un arco di peso maggiore con l'ultimo nodo di parziale
        # e nel caso lo aggiungo a parziale, dopodichè esco dal ciclo poichè non voglio aggiungere altri nodi che
        # formeranno sicuramente archi di peso inferiore
        for nodo in archiVicini:
            if nodo[1] >= self._grafo[parziale[-1]][parziale[-2]]["weight"]:
                parziale.append(nodo[0])
                self._ricorsione(parziale)
                parziale.pop()
            return


    def getPeso(self, nodo1, nodo2):
        if (nodo1, nodo2) in self._grafo.edges:
            return self._grafo[nodo1][nodo2]["weight"]
        else:
            return 0





