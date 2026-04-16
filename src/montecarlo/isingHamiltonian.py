import numpy as np
from . import bitstring as BitString

class IsingHamiltonian:
    def __init__(self, G):
        self.graph = G
        self.mues = np.zeros(len(G))
        self.J = []
        # self.J = list(nx.get_edge_attributes(G, 'weight').values())
        for u, v, w in G.edges.data('weight'):
            self.J.append(w)  

    def energy(self, config:BitString):
        sum = 0.0
        for u, v, w in self.graph.edges(data = 'weight'):
            if int(repr(config)[u]) == 0 and int(repr(config)[v]) == 0:
                sum += w
            elif int(repr(config)[u]) == 1 and int(repr(config)[v]) == 1:
                sum += w
            else:
                sum += -1 * w

        for n in range(len(self.graph)):
            if int(repr(config)[n]) == 1:
                sum += self.mues[n]
            else:
                sum += self.mues[n] * -1
       
        return sum
    
    def magnetism(self, config:BitString):
        return config.on() - config.off()
    
    def set_mu(self, mus: np.array):
        self.mues = mus
        return self

    def compute_average_values(self, T: int):
        B = 1 / T
        E  = 0.0
        M  = 0.0
        Z  = 0.0
        EE = 0.0
        MM = 0.0
        bs = BitString(len(self.graph))

        # Write your function here!
        for i in range(2**(len(bs))):
            bs.set_integer_config(i)
            Z += np.exp(-1 * B * self.energy(bs))

        for i in range(2**(len(bs))):
            bs.set_integer_config(i)
            en = self.energy(bs)

            P = np.exp(-1 * B * en) / Z
            E += en * P
            EE += (en**2) * P
            M += (bs.on() - bs.off()) * P
            MM += (bs.on() - bs.off())**2 * P
        
        HC = (EE - E**2) * (T**(-2))
        MS = (MM - M**2) * (T**(-1))

        return E, M, HC, MS
    
    def getGraph(self):
        return self.graph