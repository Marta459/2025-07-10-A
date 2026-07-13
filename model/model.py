from itertools import combinations

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = None
        self._prodotti_id = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getTutteCategorie()

    def creaGrafo(self,categoria,start_date, end_date):
        self._grafo = nx.DiGraph()
        self._prodotti_id = {}

        prodotti = DAO.getProdotti(categoria)

        for p in prodotti:
            product_id = p["product_id"]
            self._prodotti_id[product_id] = p
            self._grafo.add_node(product_id)

        vendite_dati = DAO.getVendite(start_date, end_date)
        vendite = {}
        for v in vendite_dati:
            vendite[v["product_id"]] = v["num_vendite"]

#===================================================================================
        nodi_grafo = list(self._grafo.nodes())
        for id1, id2 in combinations(nodi_grafo, 2):
            if id1 not in vendite or id2 not in vendite:
                continue
#Questo è un modulo della libreria standard di Python
# che ci dà una funzione già pronta per generare tutte
# le possibili coppie (senza ripetizioni, senza considerare l'ordine)
#Con due cicli annidati genererebbe ogni coppia due volte.
#combinations(lista, 2) fa già questo lavoro:  dà ogni coppia una sola volta,
# in un formato pulito.
#combinations(nodi_grafo, 2)
#Il secondo parametro (2) dice "dammi coppie di 2 elementi alla volta"
# ===================================================================================
            v1 = vendite[id1]
            v2 = vendite[id2]
            peso = v1 + v2

            if v1 > v2:
                self._grafo.add_edge(id1, id2, weight=peso)
            elif v2 > v1:
                self._grafo.add_edge(id2, id1, weight=peso)
            else:
                self._grafo.add_edge(id1, id2, weight=peso)
                self._grafo.add_edge(id2, id1, weight=peso)

        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()


# Ora devo trovare i prodotti più venduti
# devo fare in modo che il controller possa accedere al grafo

    def getGrafo(self):
        return self._grafo

#Devo fare in modo che il controller possa accedere ai dati dei prodotti
    def getProdottoDati(self,product_id):
        return self._prodotti_id[product_id]

#visualizzare i 5 prodotti più venduti, ovvero i nodi la cui somma dei pesi
#degli archi uscenti meno la somma dei pesi degli archi entranti è massima

    def getMigliori5(self):
        punteggi = []

        for nodo in self._grafo.nodes():
            peso_uscenti = 0
            for u, v, dati in self._grafo.out_edges(nodo, data=True):
                peso_uscenti += dati["weight"]

            peso_entranti = 0
            for u, v, dati in self._grafo.in_edges(nodo, data=True):
                peso_entranti += dati["weight"]

            punteggio = peso_uscenti - peso_entranti
            punteggi.append((nodo, punteggio))

        punteggi_ordinati = sorted(punteggi, key=lambda x: x[1], reverse=True)
        primi_5 = punteggi_ordinati[:5]
        return primi_5