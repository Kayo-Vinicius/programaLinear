from fractions import Fraction

#Classe que representa um numero fracionario, extendendo fractions.Fraction, e implentando a lógica o "M grande"
class NumFracionario(Fraction):
    def __init__(self,n,m=Fraction(0)):
        self.fraction = Fraction(n)
        self.m = Fraction(m)
   
    def __repr__(self):
        """repr(self)"""
        return str(float(self.fraction)) if self.m == 0 else str(float(self.fraction)) + ' + (' + str(float(self.m)) + '*M)'


    def __str__(self):
        """str(self)"""
        return str(float(self.fraction)) if self.m == 0 else str(float(self.fraction)) + ' + (' + str(float(self.m)) + '*M)'
        
    def __eq__(self, f):
        """a == b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        return self.fraction.__eq__(f.fraction) and self.m.__eq__(f.m)

    def __add__(self, f):
        """a + b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        return NumFracionario(self.fraction.__add__(f.fraction),self.m.__add__(f.m))

    def ___sub__(self, f):
        """a - b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        return NumFracionario(self.fraction.__sub__(f.fraction),self.m.___sub__(f.m))

    def __mul__(self, f):
        """a * b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
        
        if f.m == 0:
            return NumFracionario(self.fraction.__mul__(f.fraction))
        else:
            return NumFracionario(self.fraction.__mul__(f.fraction),self.m.__mul__(f.m)) 

    def __div__(self, f):
        """a / b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
        
        if f.m == 0:
            return NumFracionario(self.fraction.__div__(f.fraction))
        else:
            return NumFracionario(self.fraction.__div__(f.fraction),self.m.__div__(f.m))
    
    def __lt__(self, f):
        """a < b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        if self.m == f.m:
            return self.fraction.__lt__(f.fraction)
        
        else:   
            return self.m.__lt__(f.m)
        
    def __gt__(self, f):
        """a > b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        if self.m == f.m:
            return self.fraction.__gt__(f.fraction)
        
        else:   
            return self.m.__gt__(f.m)

    def __le__(self, f):
        """a <= b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        if self.m == f.m:
            return self.fraction.__le__(f.fraction)
        
        else:   
            return self.m.__le__(f.m)

    def __ge__(self, f):
        """a >= b"""
        if type(f) is not type(self):
            f = NumFracionario(f)
            
        if self.m == f.m:
            return self.fraction.__ge__(f.fraction)
        
        else:   
            return self.m.__ge__(f.m)