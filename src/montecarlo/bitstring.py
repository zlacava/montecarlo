import numpy as np

class BitString:
    """
    Simple class to implement a config of bits
    """
    def __init__(self, N):
        self.N = N
        self.config = np.zeros(N, dtype=int) 

    def __repr__(self):
        out = ""
        for i in self.config:
            out += str(i)
        return out

    def __eq__(self, other):        
        return all(self.config == other.config)
    
    def __len__(self):
        return len(self.config)

    def on(self):
        """
        Return number of bits that are on
        """
        sum = 0
        for i in self.config:
            if i == 1:
                sum += 1
        return sum
                

    def off(self):
        """
        Return number of bits that are off
        """
        sum = 0
        for i in self.config:
            if i == 0:
                sum += 1
        return sum

    def flip_site(self,i):
        """
        Flip the bit at site i
        """
        for k in range(self.__len__()):
            if k == i:
                self.config[i] = (self.config[i] + 1) % 2
                break
        
    
    def integer(self):
        """
        Return the decimal integer corresponding to BitString
        """
        len = self.__len__()

        decNum = 0
        for i in range(len):
            decNum += self.config[i] * (2**(len - i - 1))
        return decNum

 

    def set_config(self, s:list[int]):
        """
        Set the config from a list of integers
        """
        for i in range(len(s)):
            self.config[i] = s[i]
            

    def set_integer_config(self, dec:int):
        """
        convert a decimal integer to binary
    
        Parameters
        ----------
        dec    : int
            input integer
            
        Returns
        -------
        Bitconfig
        """
        i = self.__len__() - 1
        while i >= 0:
            self.config[i] = int(dec % 2)
            dec = int(dec / 2)
            i -= 1 
        return self.config