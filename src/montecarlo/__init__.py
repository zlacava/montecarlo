"""Top-level package for montecarlo."""
import numpy as np
import networkx as nx
import math      
import copy as cp           

from . import bitstring as BitString
    
class IsingHamiltonian:
    """
    Class for representing a Hamiltonian from a graph
    """
    def __init__(self, G):
        self.graph = G
        self.mues = np.zeros(len(G))
        self.N = len(G)
        self.J = []
        # self.J = list(nx.get_edge_attributes(G, 'weight').values())
        for u, v, w in G.edges.data('weight'):
            self.J.append(w)  

    def energy(self, config:BitString.BitString):
        """
        Gets the energy of the Hamiltonian corresponding to the BitString configuration for the spins
        (Args):
            BitString -> bit string representing the spins of each vertex of the graph
        Returns the total energy from the bit string configuration
        """
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
    
    def magnetism(self, config:BitString.BitString):
        """
        Returns the magentism of the Hamiltonian of the given bit string configuration 
        """
        return config.on() - config.off()
    
    def set_mu(self, mus: np.array):
        """
        Congifures the mues of the Hamiltonian
        """
        self.mues = mus
        return self

    def compute_average_values(self, T: int):
        """
        Gets the average values of energy, magnetization, heat capacity and magnetic susceptibility
        (Args):
            T -> temperature in Kelvin
        """
        B = 1 / T
        E  = 0.0
        M  = 0.0
        Z  = 0.0
        EE = 0.0
        MM = 0.0
        bs = BitString.BitString(len(self.graph))

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
class MonteCarlo:
    """
    Class for running montecarlo simulations
    """
    def __init__(self, H):
        self.ham = H  

    def run(self, T, n_samples, n_burn):
        """
        Runs the simulation
        (Args):
            T -> Temperture in Kelvin
            n_samples -> Number of total samples
            n_burn -> Number of steps to burn
        
        Returns a tuple of the averge energy and magnetism
        """
        bs = BitString.BitString(len(self.ham.graph))
        random = np.random.default_rng()
        bs.set_integer_config(random.integers(0, 2**len(bs)))
        # accepted = random.random()
        # accepted = 0.9
        burns = n_burn
        avg_E = []
        avg_M = []
        

        for i in range(n_samples):
            lowest = np.finfo(np.float64).max
            # lowest = 1000
            
            accepted = random.random()
            curr_e = self.ham.energy(bs)
            curr_config = bs.config

            j = random.integers(0, len(bs))

            for k in range(len(bs)):

                # bs.set_integer_config(random.integers(0, 2**len(bs)))
                bs.flip_site(j)

                next_e = self.ham.energy(bs)

                if next_e > curr_e:
                    visit_prob = np.exp(-1 * (next_e - curr_e) / (T * 1.0))
                    # print(visit_prob)
                    if visit_prob >= accepted:
                        # print(visit_prob)
                        if burns > 0:
                            burns -= 1
                            break
                        else:
                            # print("accepted,",visit_prob)
                            avg_E.append(next_e)
                            avg_M.append(self.ham.magnetism(bs))
                            break
                    else:
                        # print("reject",visit_prob)
                        bs.set_config(curr_config)
                else:
                    if burns > 0:
                        burns -= 1
                        break
                    else:
                        # print("accepted2")
                        avg_E.append(next_e)
                        avg_M.append(self.ham.magnetism(bs))
                        break
                j = (j + 1) % len(bs)

        return avg_E, avg_M

    def J(self):
        """
        Returns the Hamiltonian for the montecarlo class
        """
        return self.ham