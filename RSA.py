#-*- coding: utf-8 -*-
from math import log10,ceil,floor
from random import getrandbits,randrange,randint

# Tamaño de los primos generados en bits
# 336 bits genera numeros de 101 digitos
num_bits = 336

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
        y = x1 - (a//b) * y1
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
        if n & 1 == 0:
            return False
        # descomponemos a n en la forma (2^r)*d + 1
        r = 0
        d = n - 1
        # mientras d sea par
        while d & 1 == 0:
            r += 1
            d //= 2 # division entera
        # hace la prueba k veces
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a,d,n) #a^d mod n
            if x == 1 or x == n - 1:
                continue
            for _ in range(r-1):
                x = pow(x,2,n)
                if x == 1:
                    return False
                if x == n - 1:
                    break
            return False
        # si la prueba no detecta que sea compuesto k veces
        # devuelve verdadero
        return True

    # genera un numero aleatorio que ademas es impar y de 1024 bits
    def generarPosiblePrimo(self):
        # generamos un numero aleatorio de num_bits bits
        n = getrandbits(num_bits)
        # forzamos a que sea impar 
        # y que tenga al menos el numero de digitos especificado
        n |= (1 << num_bits - 1) | 1
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
        g,d,_ = self.euclidesExtendido(p,phi)
        while g != 1 or p > phi:
            p = self.generarPosiblePrimo()
            g,d,_ = self.euclidesExtendido(p,phi)
        d %= phi
        return p,d

    # encripta un mensaje (cadena), 
    #Recibe el mensaje en texto claro y la llave publica
    # devuelve un entero c = m^e mod n 
    def encriptar(self, mensaje, e,n):
        cipher = [pow(ord(char), e, n) for char in mensaje]
        return cipher


    # desencripta un mensaje (arreglo de bytes)
    # devuelve una cadena
    def desencriptar(self, mensaje, d,n):
        decipher = [ chr(pow(char, d, n)) for char in mensaje]
        return ''.join(decipher)



    def __init__(self):
        print("-------------------------------------")
        print ("|  Criptografía y seguridad\n|  Proyecto 02\n|  Gallardo Valdez José Jhovan\n|  Guerrero Chávez Diana Lucía")
        print("-------------------------------------\n")
        p = self.generarPrimo()
        q = self.generarPrimo()
        self.n = p*q
        phi = (p-1)*(q-1)
        self.e, self.d = self.generarED(phi)
        print("p = " + str(p))
        print("q = " + str(q))
        print("n = " + str(self.n))
        print("phi = " + str(phi))
        print("e = " + str(self.e))
        print("d = " + str(self.d))

mi_rsa = RSA()

# pruebas
print("\nPRUEBAS\n")
mensaje = "en esta casa obedecemos las leyes de la termodinámica"
print("Mensaje original: " + mensaje+"\n")
encriptado = mi_rsa.encriptar(mensaje,mi_rsa.e,mi_rsa.n)
print("Mensaje encriptado: " + str(encriptado))

desencriptado = mi_rsa.desencriptar(encriptado,mi_rsa.d,mi_rsa.n)
print("\nMensaje desencriptado: " + desencriptado)

