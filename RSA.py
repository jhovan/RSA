from math import log10,ceil,floor
from random import getrandbits,randrange,randint

num_bits = 1024
min_digitos = 100

class RSA:

    # recibe dos enteros a y b
    # devuelve d,x,y donde:
    # d = mcd(a,b)
    # x = a^-1 mod b en caso de d=1
    # y = b^-1 mod a en caso de d=1
    # NOTA: x y y pueden ser negativos
    def euclidesExtendido(self,a,b):
        if b == 0:
            return a, 1, 0
        d1,x1,y1 = self.euclidesExtendido(b, a % b)
        d = d1
        x = y1
        y = x1 - floor(a/b) * y1
        return d, x, y

    # implementacion de Miller-Rabin
    # n es el numero que queremos saber si es primo
    # k es el numero de veces que se ejecutara la prueba
    # devuelve verdadero si un entero positivo es primo
    def esPrimo(self,n, k = 300):
        # si es 2 o 3, es primo
        if n == 2 or n == 3:
            return True
        # si es par, no es primo
        if n%2 == 0:
            return False
        s = 0
        r = n - 1
        while(r % 2 == 1):
            s += 1
            r //= 2 # division entera
        # hace la prueba k veces
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a,r,n) #a^r mod n
            if x != 1 and x != n - 1:
                j=1
                while x != n - 1 and j<s:
                    x = pow(x,2,n)
                    if(x == 1):
                        return False
                    j += 1
                if x != n - 1:
                    return False
        # si la prueba no detecta que sea compuesto k veces
        # devuelve verdadero
        return True


    # genera un numero aleatorio que ademas es impar 
    # de al menos 100 digitos
    # y a lo mas 1024 bits
    def generarPosiblePrimo(self):
        # numero de bits necesarios para representar un numero
        # del numero de digitos especificado
        bit_min_digitos = ceil((min_digitos)/log10(2))
        n = getrandbits(num_bits)
        # forzamos a que sea impar 
        # y que tenga al menos el numero de digitos especificado
        n |= (1 << randint(bit_min_digitos-1,num_bits-1)) | 1
        return n

   # genera un primo aleatorio de al menos 100 digitos
   # y a lo mas 1024 bits
    def generarPrimo(self):
        p = self.generarPosiblePrimo()
        while not self.esPrimo(p):
            p = self.generarPosiblePrimo()
        return p

    # regresa e, un numero menor que phi y coprimo con phi
    # d es su inverso modulo phi
    def generarED(self,phi):
        p = self.generarPosiblePrimo()
        g,x,_ = self.euclidesExtendido(p,phi)
        while g != 1 or p>self.phi:
            p = self.generarPosiblePrimo()
            g,d,_ = self.euclidesExtendido(p,phi)
        return p,d

    def __init__(self):
        p = self.generarPrimo()
        q = self.generarPrimo()
        self.n = p*q
        phi = (p-1)*(p-1)
        self.e, self.d = self.generarED(phi)
        print(self.n)
        print(self.e)
        print(self.d)

rsa = RSA()