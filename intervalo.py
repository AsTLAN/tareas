# -*- coding: utf-8 -*- 

# from sympy import mpmath as mp
# import numpy as np

import numpy
math = numpy    # NB!

class Intervalo(object):
    """
    Se define la clase 'Intervalo', y los mÃ©todos para la aritmÃ©tica bÃ¡sica de intervalos,
    es decir, suma, resta, multiplicaciÃ³n y divisiÃ³n. Se incluyen otras funciones
    que serÃ¡n Ãºtiles.
    """
    def __init__(self, lo, hi=None):
        """
        Definimos las propiedades del objeto Intervalo a partir de sus bordes,
        lo y hi, donde lo <= hi. En el caso en que el intervalo sÃ³lo tenga
        un nÃºmero, Ã©ste se interpreta como un intervalo 'delgado' o 'degenerado'.
        """
        if hi is None:
            hi = lo
        elif (hi < lo):
            lo, hi = hi, lo
        
        self.lo = lo
        self.hi = hi
        
    def __repr__(self):
        return "Intervalo [{},{}]".format(self.lo,self.hi)
    
    def __str__(self):
        # Esta funciÃ³n sirve con 'print'
        return "[{},{}]".format(self.lo,self.hi)

    def _repr_html_(self):
        reprn = "[{}, {}]".format(self.lo, self.hi)
        reprn = reprn.replace("inf", r"&infin;")
        return reprn
    
    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)

    # AquÃ­ vienen las operaciones aritmÃ©ticas
    def __add__(self, otro):
        """
        Suma de intervalos
        """
        try:
            return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        except:
            return self + Intervalo(otro)

    def __radd__(self, otro):
        return self + otro
        

        
    def __mul__(self, otro):
      
        return self._mul2(otro)
    
    def _mul1(self, otro):
        try:
            S=[self.lo*otro.lo , self.lo * otro.hi , self.hi * otro.lo , self.hi * otro.hi ]
            return Intervalo( min(S), max(S) )
        except:
            return self * Intervalo(otro)
            
    def _mul2(self, otro):
        """Multiplicacion de intervalos, evaluando todos los casos posibles """
        try:
            if self.lo >= 0 :
                if otro.lo >= 0:
                    return Intervalo(self.lo * otro.lo , self.hi * otro.hi)
                elif otro.hi <= 0 :
                    return Intervalo(self.hi * otro.lo , self.lo * otro.hi)
                elif otro.lo <= 0 and otro.hi >= 0:
                    return Intervalo(self.hi * otro.lo , self.hi * otro.hi)
                
            elif self.hi <= 0:
                if otro.hi <= 0:
                    return Intervalo(self.hi * otro.hi , self.lo * otro.lo)
                elif otro.lo >= 0:
                    return Intervalo(self.lo * otro.hi , self.hi * otro.lo)
                elif otro.lo <= 0 and otro.hi >= 0:
                    return Intervalo(self.lo * otro.hi , self.lo * otro.lo) 
                     
            elif self.lo <= 0 and self.hi >= 0:
                if otro.lo >= 0:
                    return Intervalo(self.lo * otro.hi , self.hi * otro.hi)
                elif otro.hi <= 0:
                    return Intervalo(self.hi * otro.lo , self.lo * otro.lo)         
                elif otro.lo <= 0 and otro.hi >= 0:   
                    return Intervalo(min(self.hi * otro.lo , self.lo * otro.hi) , max(self.hi * otro.hi , self.lo * otro.lo))
                    
        except:
            return self * Intervalo(otro)
     
    def __rmul__(self, otro):
        return self * otro

    # Ã‰sta es la funcion igualdad para intervalos
    def __eq__(self, otro):
        """
        funciÃ³n igualdad para intervalos 

        """
        try:
            if self.lo == otro.lo and self.hi == otro.hi:
                return True
            else:
                return False
        except:
            if self.lo == Intervalo(otro).lo and self.hi == Intervalo(otro).hi:
                return True
            else:
                return False
  

    # IntersecciÃ³n
    def __and__(self, otro):
        """
        IntersecciÃ³n de intervalos
        Funciona con la sintaxis & (como el AND bitwise)
        """
        if not isinstance(otro,Intervalo):
            otro = Intervalo(otro)

        if (self.lo > otro.hi) | (self.hi < otro.lo):
            return None

        else:
            a = max( self.lo, otro.lo )
            b = min( self.hi, otro.hi )
            return Intervalo(a,b)
    
    # IntersecciÃ³n por la izquierda
    def __rand__(self, otro):
        """
        Interseccion de intervalos (por la izquierda)
        """
        return self & otro
    
    # Negativo del intervalo
    def __neg__(self):
        """
        Devuelve el valor negativo del intervalo
        """
        return Intervalo(-self.hi, -self.lo)

    # Resta
    def __sub__(self, otro):
        """
        Resta de Intervalos
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
        
        return Intervalo(self.lo - otro.hi, self.hi - otro.lo)                
        
    # Resta reversa para poder hacer (float) - Intervalo
    def __rsub__(self, otro):
        
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
            
        return Intervalo.__sub__(otro, self)
    
    # FunciÃ³n contains
    def __contains__(self, otro):
        """
        Devuelve un true o false si 'otro' estÃ¡ dentro del intervalo.
        En el caso de que otro sea un intervalo, se requiere que todos sus elementos
        estÃ©n dentro para regresar true.
        """
        return otro & self == otro 
        
            
    # Funcion recÃ­proco
    def reciprocal(self):
        """
        Devuelve un intervalo con los valores recÃ­procos
        """
        if 0 in self:
            #si el intervalo contiene el cero debe de aparecer un error
            raise ZeroDivisionError
        else:
            return Intervalo(1.0/self.hi,1.0/self.lo)

    # division con denominadores que no contienen al cero    
    def __div__(self, otro):
        """
        DivisiÃ³n
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)

        if 0 in otro:
            raise ZeroDivisionError

        else:
            return self * otro.reciprocal()
    
    # divisiÃ³n reversa
    def __rdiv__(self, otro):
        """
        DivisiÃ³n revrsa para poder usar floats en el numerador
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)

        return Intervalo.__div__(otro, self)

    def __pow__(self, alpha):
        """
        Potencia con exponentes reales o enteros
        alpha: exponente
        """
        
        if alpha == int(alpha):
            # caso donde el exponente es entero, en este caso los flotantes que pueden ser
            # igualados a su forma entera entran en esta categorÃ­a (e.g. 2.0 == 2)
            
            return self.pow_int(alpha)
            
        elif isinstance(alpha, Intervalo):
            # caso donde el exponente es de la clase intervalo
            return self.pow_expint(alpha)
            
        else:
            # cualquier otro caso el exponente se toma como real
            return self.pow_real(alpha)


    def pow_int(self, n):
        """
        MÃ©todo para potencias enteras
        """
        # n: exponente
        if n > 0:
            if n % 2 != 0:
                return Intervalo(self.lo**n, self.hi**n)
            elif self.lo > 0:
                return Intervalo(self.lo**n, self.hi**n)
            elif self.hi < 0:
                return Intervalo(self.hi**n, self.lo**n)
            elif 0 in self:
                print 'Advertencia: El intervalo contiene el cero'
                return Intervalo(0, max(self.lo**n, self.hi**n))
        elif n == 0:
            return Intervalo(1)
        else: # n < 0:
            # para este caso es importante notar que la funcion reciprocal() no admite intervalos que contengan el cero,
            # por lo que primero restringiremos el intervalo a reales positivos
            restringido = self.restringir_dominio()
            
            return pow_int(restringido.reciprocal(), -n)
            # Por si no queremos llamar a la recursiÃ³n dejamos esto por aquÃ­
            # return Intervalo(self.reciprocal().lo**-n, self.reciprocal().hi**-n)

    def pow_real(self, n):
        """
        MÃ©todo para potencias con exponentes reales (que en este caso son flotantes)
        f(x) = x^a = exp(a*log(x))
        """
        return exp(n*log(self))
      
    #def pow_expint(self, otro):
    #    """
    #    Función exponienciación de Intervalos con exponente Intervalo
    #    """       
    #        
    #    res = self.restringir_dominio()
    #    
    #    S = math.exp(otro.hi * math.log(res.lo)), math.exp(otro.lo * math.log(res.hi)) , math.exp(otro.lo * math.log(res.lo)), math.exp(otro.hi * np.log(res.hi))
    #
    #    returnreturn Intervalo(min(S), max(S))
    
    def pow_expint(self, otro):
        """
        Función exponienciación de Intervalos con exponente Intervalo
        """       
            
        res = self.restringir_dominio()
        
        if otro.hi <= 0:
            if res.hi <= 1:
                return Intervalo(math.exp(otro.hi * math.log(res.hi)), math.exp(otro.lo * math.log(res.lo)))
            
            if res.lo <= 1 <= res.hi:
                return Intervalo(math.exp(otro.lo * math.log(res.hi)), math.exp(otro.lo * math.log(res.lo)))
            
            if 1 <= res.lo:
                return Intervalo(math.exp(otro.lo * math.log(res.hi)), math.exp(otro.hi * math.log(res.lo)))
        
        if otro.lo <= 0 <= otro.hi:
            
            if res.hi <= 1:
                return Intervalo(math.exp(otro.hi * math.log(res.lo)), math.exp(otro.lo * math.log(res.lo)))
            
            if res.lo <= 1 <= res.hi:
                return Intervalo(min( math.exp(otro.hi * math.log(res.lo)), math.exp(otro.lo * math.log(res.hi)) ), max( math.exp(otro.hi * np.log(res.hi)), math.exp(otro.lo * math.log(res.lo)) ))
            
            if 1 <= res.lo:
                return Intervalo(math.exp(otro.lo * np.log(res.hi)), math.exp(otro.hi * math.log(res.hi)))
            
        if 0 <= otro.lo:
            
            if res.hi <= 1:
                return Intervalo(math.exp(otro.hi * math.log(res.lo)), math.exp(otro.lo * math.log(res.hi)))
            
            if res.lo <= 1 <= res.hi:
                return Intervalo(math.exp(otro.hi * math.log(res.lo)), math.exp(otro.hi * math.log(res.hi)))
            
            if 1 <= res.lo:
                return Intervalo(math.exp(otro.lo * math.log(res.lo)), math.exp(otro.hi * math.log(res.hi)))


    def middle(self):
        """
        Calcula el punto medio del intervalo
        """
        return (self.lo+self.hi)/2.
        
    def radio(self):
        """
        Calcula el radio del intervalo
        """
        return (self.hi-self.lo)/2.
        
    def width(self):
        """
        Cacula la anchura
        """

        return abs(self.hi-self.lo)
        
    def abs(self):
        
        return max([abs(self.lo),abs(self.hi)])

    
    # RelaciÃ³n < de intervalos.
    def __lt__(self,otro):
        """RelaciÃ³n < de intervalos."""
        
        try:
            return self.hi < otro.lo
        except:
            return self < Intervalo(otro)

    # RelaciÃ³n > de intervalos.
    def __gt__(self,otro):
        """RelaciÃ³n > de intervalos."""
        
        try:
            return self.lo > otro.hi
        except:
            return self > Intervalo(otro)

    #RelaciÃ³n <= de intervalos.
    def __le__(self,otro):
        """RelaciÃ³n <= de intervalos"""
    
        try: 
            return (self.lo <= otro.lo) and self.hi <= otro.hi  
        except: 
            return self <= Intervalo(otro)

    #RelaciÃ³n >= de intervalos.
    def __ge__(self,otro):
        """RelaciÃ³n >= de intervalos"""
    
        try:
            return (self.lo >= otro.lo) and self.hi >= otro.hi
        except: 
            return self >= Intervalo(otro)
    
    def hull(self, otro):
        return Intervalo(min(self.lo,otro.lo),max(self.hi,otro.hi))

    # AquÃ­ se definirÃ¡n funciones sobre intervalos

    ## NOTA: ImplementaciÃ³n de David et al; me voy por la de AsTlan porque pasa
    ## un test correcto que la de David et al no pasa.
    #def cos(self):
    #
    #    pi = math.pi
    #    if self.width() >= 2*pi:
    #        return Intervalo(-1, 1)
    #                    
    #    num, num2 = math.mod(self.lo, 2*pi), math.mod(self.hi, 2*pi)
    #
    #    if num2 < num:
    #        if num >= pi:
    #            return Intervalo(min(math.cos(num), math.cos(num2)), 1.0)
    #        
    #        else: 
    #            return Intervalo(-1.0, 1.0)
    #
    #    if num2>pi and num<pi:
    #        return Intervalo(-1, max(math.cos(num), math.cos(num2)))
    #
    #
    #    num = math.cos(num)
    #    num2 = math.cos(num2)
    #
    #    if num2 < num:
    #        num, num2 = num2, num
    #
    #    return Intervalo(num, num2)
    
    def cos(self):  
        """
        Coseno
        """
        pi = math.pi
        if self.width() >= (2 * pi):
            return Intervalo(-1,1)
        
        else:
            k = math.floor( (self.lo) / (2 * (pi)) )
                    
            if ( self.hi - k*2*pi <= pi ):
                return Intervalo(math.cos(self.hi), math.cos(self.lo))
                
            elif ( self.lo - k*2*pi  <= pi <= self.hi - k*2*pi <= 2*pi ):
                return Intervalo(-1, max(math.cos(self.lo), math.cos(self.hi)))
                
            elif ( self.lo - k*2* pi <= pi <= 2*pi <= self.hi - k*2*pi ):
                return Intervalo(-1, 1)
                
            elif ( pi <=  self.lo - k*2*pi <= self.hi - k*2*pi <= 2*pi ):
                return Intervalo(math.cos(self.lo), math.cos(self.hi))
                
            elif ( pi <= self.lo - k*2*pi <= 2*pi <=  self.hi - k*2*pi <= 3*pi ):
                return Intervalo( min(math.cos(self.lo), math.cos(self.hi)), 1)
                
            elif ( pi <= self.lo - k*2*pi <= 2*pi <= 3*pi <= self.hi - k*2*pi ):
                return Intervalo(-1, 1)

    def sin(self):
        return (self - math.pi/2).cos()
        
    def tan(self):
        """
        FunciÃ³n tangente para intervalos
        """
        #from scipy import inf
        pi = math.pi        
        if self.width() >= pi:
            return Intervalo(float("-inf"), float("inf"))
        
        if math.floor((self.lo + pi/2)/pi) == math.floor((self.hi + pi/2)/pi):
            return Intervalo(math.tan(self.lo), math.tan(self.hi))
        
        else:
            print "Warning: se tiene un intervalo degenerado"
            return Intervalo(math.tan(self.lo), float("inf")), Intervalo(float("-inf"), math.tan(self.hi))     
       
       
    def restringir_dominio(self, dominio=None):
        """
        FunciÃ³n que restringe el dominio de un intervalo a valores no negativos.
        Levanta un error si el intervalo es completamente negativo.
        """

        if dominio is None:
            dominio = Intervalo(0, math.inf)

        restringido = self & dominio

        if restringido is None:
            
            raise ArithmeticError("""Advertencia: el intervalo {} tiene 
            interseccion vacia con el dominio {}.""".format(self, dominio))
            

        if restringido != self:
            if dominio.__contains__(self):
                pass
            else:
                print """Advertencia: el intervalo {} tiene interseccion no-vacia 
                con el dominio {}. Se considera la restriccion al intervalo 
                dado por (interseccion con el dominio) 
                {}""".format(self, dominio, restringido)
        
        return restringido


    def log(self):
        """
        Calcula el logaritmo de un intervalo.
        """
        #try:
        #   return Intervalo(math.log(self.lo), math.log(self.hi))

        #except:

        restringido = self.restringir_dominio()

        return Intervalo(math.log(restringido.lo), math.log(restringido.hi))


    def exp(self):
        """
        Calcula la exponencial de un intervalo.
        """
    
        return Intervalo(math.exp(self.lo), math.exp(self.hi))

        
    def sqrt(self):

        restringido = self.restringir_dominio()
        return Intervalo(math.sqrt(restringido.lo),math.sqrt(restringido.hi))
            
    def arctan(self):
        return Intervalo(math.arctan(self.lo),math.arctan(self.hi))
        
#----------
#funciones elementales para intervalos, para que funcionen cosas tipo funcion(a)
def exp(x):
    try:
        return x.exp()
    except:
        return math.exp(x)

def log(x):
    try:
        return x.log()
    except:
        return math.log(x)

def sqrt(x):
    try:
        return x.sqrt()
    except:
        return math.sqrt(x)

def arctan(x):
    try:
        return x.arctan()
    except:
        return math.arctan(x)

def cos(x):
    try:
        return x.cos()
    except:
        return math.cos(x)

def sin(x):
    try:
        return x.sin()
    except:
        return math.sin(x)

def tan(x):
    try:
        return x.tan()
    except:
        return math.tan(x)

# ----    
def chop(X):
        middle_pos = X.middle()
        right_part = Intervalo(X.lo, middle_pos)
        left_part = Intervalo(middle_pos,X.hi)
        return right_part, left_part
    

def chop_epsilon(X,f,epsilon,l=[]):
    if f(X) is not None:
        if f(X).width() < epsilon:
            l.append(X)
        else:
            right_part, left_part = chop(X)
            chop_epsilon(right_part,f,epsilon,l)
            chop_epsilon(left_part,f,epsilon,l)
    return l

        
def creater_bigest(list_of_X):
    hi = list_of_X[0].hi
    lo = list_of_X[0].lo
    for x in list_of_X:
        if x.lo <= lo:
            lo = x.lo
        if x.hi >= hi:
            hi = x.hi
    return Intervalo(lo,hi)

def plot_with_f(list_of_X,f,zoom=1):
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches
    from numpy import arange

    def get_verts(X,f):
        try:
            verts = [ (X.lo, f(X).lo),(X.lo, f(X).hi),(X.hi, f(X).hi),(X.hi, f(X).lo),(0., 0.),]
            return verts
        except AttributeError:
            return  [ (0., 0.),(0., 0.),(0., 0.),(0., 0.),(0., 0.),]
        
    
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for X in list_of_X:
        path = Path(get_verts(X,f), codes)
        patch = patches.PathPatch(path, facecolor='orange', lw=2)
        ax.add_patch(patch)
    
    big_X = creater_bigest(list_of_X)
    
    x = arange(big_X.lo,big_X.hi,.01)
    ax.plot(x,f(x))
    
    ax.set_xlim(big_X.lo,big_X.hi)
    ax.set_ylim(f(big_X).lo*zoom,f(big_X).hi*zoom) 
    plt.show()

def chop_parts(X,parts):
    l = []
    if str(parts).isdigit():
        from math import floor
        from numpy import arange
    
        spacing = X.width()/parts
        lo = X.lo
        hi = X.lo + spacing
        print spacing
        for x in arange(0,parts,1):
            l.append(Intervalo(lo,hi))
            lo = lo + spacing
            hi = hi + spacing
        return l
        
        
def heaviside(self):
    '''
    Funcion Heaviside para intervalos
    '''
    
    if self.lo<0 and self.hi<0:
        return Intervalo(0)
        
    if self.lo<0 and self.hi>=0:
        
        return Intervalo(0,1)
        
    return Intervalo(1)
        

    
def SymmetricInterval(a,b):
    
    '''
    Construye un intervalo simetrico donde la primera entrada es el
    centro del intervalo y la segunda el radio.
    '''
    
    hi=a+b
    lo=a-b
    
    return Intervalo(lo,hi)


