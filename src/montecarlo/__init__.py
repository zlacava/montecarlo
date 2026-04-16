"""Top-level package for montecarlo."""
import numpy as np
import networkx as nx
import math      
import copy as cp           

from . import bitstring as BitString
from . import isingHamiltonian as IsingHamiltonian

# class BitString:
#     """
#     Simple class to implement a config of bits
#     """
#     def __init__(self, N):
#         self.N = N
#         self.config = np.zeros(N, dtype=int) 

#     def __repr__(self):
#         out = ""
#         for i in self.config:
#             out += str(i)
#         return out

#     def __eq__(self, other):        
#         return all(self.config == other.config)
    
#     def __len__(self):
#         return len(self.config)

#     def on(self):
#         """
#         Return number of bits that are on
#         """
#         sum = 0
#         for i in self.config:
#             if i == 1:
#                 sum += 1
#         return sum
                

#     def off(self):
#         """
#         Return number of bits that are off
#         """
#         sum = 0
#         for i in self.config:
#             if i == 0:
#                 sum += 1
#         return sum

#     def flip_site(self,i):
#         """
#         Flip the bit at site i
#         """
#         for k in range(self.__len__()):
#             if k == i:
#                 self.config[i] = (self.config[i] + 1) % 2
#                 break
        
    
#     def integer(self):
#         """
#         Return the decimal integer corresponding to BitString
#         """
#         len = self.__len__()

#         decNum = 0
#         for i in range(len):
#             decNum += self.config[i] * (2**(len - i - 1))
#         return decNum

 

#     def set_config(self, s:list[int]):
#         """
#         Set the config from a list of integers
#         """
#         for i in range(len(s)):
#             self.config[i] = s[i]
            

#     def set_integer_config(self, dec:int):
#         """
#         convert a decimal integer to binary
    
#         Parameters
#         ----------
#         dec    : int
#             input integer
            
#         Returns
#         -------
#         Bitconfig
#         """
#         i = self.__len__() - 1
#         while i >= 0:
#             self.config[i] = int(dec % 2)
#             dec = int(dec / 2)
#             i -= 1 
#         return self.config

# class IsingHamiltonian:
#     def __init__(self, G):
#         self.graph = G
#         self.mues = np.zeros(len(G))
#         self.J = []
#         # self.J = list(nx.get_edge_attributes(G, 'weight').values())
#         for u, v, w in G.edges.data('weight'):
#             self.J.append(w)  

#     def energy(self, config:BitString):
#         sum = 0.0
#         for u, v, w in self.graph.edges(data = 'weight'):
#             if int(repr(config)[u]) == 0 and int(repr(config)[v]) == 0:
#                 sum += w
#             elif int(repr(config)[u]) == 1 and int(repr(config)[v]) == 1:
#                 sum += w
#             else:
#                 sum += -1 * w

#         for n in range(len(self.graph)):
#             if int(repr(config)[n]) == 1:
#                 sum += self.mues[n]
#             else:
#                 sum += self.mues[n] * -1
       
#         return sum
    
#     def magnetism(self, config:BitString):
#         return config.on() - config.off()
    
#     def set_mu(self, mus: np.array):
#         self.mues = mus
#         return self

#     def compute_average_values(self, T: int):
#         B = 1 / T
#         E  = 0.0
#         M  = 0.0
#         Z  = 0.0
#         EE = 0.0
#         MM = 0.0
#         bs = BitString(len(self.graph))

#         # Write your function here!
#         for i in range(2**(len(bs))):
#             bs.set_integer_config(i)
#             Z += np.exp(-1 * B * self.energy(bs))

#         for i in range(2**(len(bs))):
#             bs.set_integer_config(i)
#             en = self.energy(bs)

#             P = np.exp(-1 * B * en) / Z
#             E += en * P
#             EE += (en**2) * P
#             M += (bs.on() - bs.off()) * P
#             MM += (bs.on() - bs.off())**2 * P
        
#         HC = (EE - E**2) * (T**(-2))
#         MS = (MM - M**2) * (T**(-1))

#         return E, M, HC, MS
    
#     def getGraph(self):
#         return self.graph
    
class MonteCarlo:
    def __init__(self, H):
        self.ham = H  

    def run(self, T, n_samples, n_burn):
        bs = BitString(len(self.ham.getGraph()))
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

            for j in range(len(bs)):

                # bs.set_integer_config(random.integers(0, 2**len(bs)))
                bs.flip_site(j)

                next_e = self.ham.energy(bs)

                if next_e < lowest:
                    lowest = next_e
                    lowest_config = bs.config
                bs.flip_site(j)

            bs.set_config(lowest_config)
            if lowest > curr_e:
                    visit_prob = np.exp(-1 * (lowest - curr_e) / (T * 1.0))
                    # print(visit_prob)
                    if visit_prob >= accepted:
                        # print(visit_prob)
                        if burns > 0:
                            burns -= 1
                            break
                        else:
                            # print("accepted,",visit_prob)
                            avg_E.append(lowest)
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
                    avg_E.append(lowest)
                    avg_M.append(self.ham.magnetism(bs))
                    break


        return avg_E, avg_M

    def J(self):
        return self.ham