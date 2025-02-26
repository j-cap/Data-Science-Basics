from numpy import sum as npsum
from numpy import vstack, append, array

class glisp_function:
    """ 
    Preference query function.

    Values of f already computed are stored to save computations
    of expensive functions.

    (C) 2019 by A. Bemporad, September 23, 2019    
    """

    def __init__(self,f,comparetol):
        self.itest = 0
        self.Xtest = []
        self.Ftest = []
        self.f = f
        self.comparetol = comparetol

    def clear(self):
        self.itest = 0
        self.Xtest = []
        self.Ftest = []
        return

    def eval(self,x,y):

        xfound = False
        yfound = False
        
        itest = self.itest
        if itest>0:
            Xtest = self.Xtest
            Ftest = self.Ftest
        else:
            fx = self.f(x)
            itest = 1
            Xtest = array([x])
            Ftest = array([fx])
            xfound = True
        
    
        for i in range(itest):
            if not(xfound) and npsum(abs(Xtest[i,:]-x)) <= 1e-10:
                   xfound = True
                   fx = Ftest[i]
    
            if not(yfound) and npsum(abs(Xtest[i,:]-y)) <= 1e-10:
                   yfound = True
                   fy = Ftest[i]
    
        if not(xfound):
            fx = self.f(x)
            Xtest = vstack((Xtest,x))
            Ftest = append(Ftest,fx)
            itest = itest+1
        
        if not(yfound):
            fy = self.f(y)
            Xtest = vstack((Xtest,y))
            Ftest = append(Ftest,fy)
            itest = itest+1
            
        # Make comparison
        if fx<fy-self.comparetol:
            out = -1
        elif fx>fy+self.comparetol:
            out = 1
        else:
            out = 0

        self.Xtest = Xtest
        self.Ftest = Ftest
        self.itest = itest

        return out

    def value(self,x):
        # Compute function value, from available ones if available
        #
        # (C) 2019 A. Bemporad, September 22, 2019

        j = 0
        while j<self.itest:
            if npsum(abs(self.Xtest[j,:]-x)) <= 1e-10:
                val=self.Ftest[j]
                return val
            j = j+1


        # Value does not exist, compute it
        val = self.f(x)
        self.Xtest = vstack((self.Xtest,x))
        self.Ftest = append(self.Ftest,val)
        self.itest = self.itest+1
        return val




  