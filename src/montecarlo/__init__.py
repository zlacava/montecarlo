"""Top-level package for montecarlo."""
import numpy as np
import networkx as nx
import math      
import copy as cp           

from . import bitstring as BitString
from . import isingHamiltonian as IsingHamiltonian
    

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
        bs = BitString(len(self.ham.graph))
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