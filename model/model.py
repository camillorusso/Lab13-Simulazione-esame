import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self.nodes = None
        self.edges = None
        self.idMap = {}
        self.grafo = nx.DiGraph()
        self.lista1 = []
        self.anni = []
        self.lista2 = []
        self.classifica = []

        self._bestPath = []
        self._bestScore = 0

    def buildGraph(self,year):
        self.grafo.clear()
        self.nodes = DAO.getAllNodes(year)
        for element in self.nodes:
            self.idMap[element.driverId] = element
        self.grafo.add_nodes_from(self.nodes)
        self.edges = DAO.getAllEdges(year)
        for element in self.edges:
            self.grafo.add_edge(self.idMap[element.driverId1], self.idMap[element.driverId2], weight=element.peso)

    def getAllFinal(self):
        for element in self.grafo.nodes():
            punteggio = 0
            for e_out in self.grafo.out_edges(element, data=True):
                punteggio -= e_out[2]["weight"]
            for e_in in self.grafo.in_edges(element, data=True):
                punteggio += e_in[2]["weight"]
            self.lista2.append((element,punteggio))
        self.classifica = sorted(self.lista2, key=lambda p: p[1], reverse=True)
        return self.classifica

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def getAllAnni(self):
        self.lista1 = DAO.getAllAnni()
        for element in self.lista1:
            if element.year not in self.anni:
                self.anni.append(element.year)
        return self.anni

    def getDreamTeam(self, k):
        self._bestPath = []
        self._bestScore = 1000

        parziale = []
        self._ricorsione(parziale, k)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, k):
        if len(parziale) == k:
            if self.getScore(parziale) < self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self.grafo.nodes():
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, k)
                parziale.pop()

    def getScore(self, team):
        score = 0
        for e in self.grafo.edges(data=True):
            if e[0] not in team and e[1] in team:
                score += e[2]["weight"]
        return score
