# nodo para listas enlazadas
class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None
        self.anterior = None 

# lista simplemente enlazada
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamaño = 0
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamaño += 1
    
    def obtener(self, indice):
        if indice < 0 or indice >= self.tamaño:
            return None
        
        actual = self.cabeza
        contador = 0
        
        while contador < indice:
            actual = actual.siguiente
            contador += 1
        
        return actual.dato
    
    def eliminar_primero(self):
        if self.esta_vacia():
            return None
        
        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        self.tamaño -= 1
        
        if self.cabeza is None:
            self.cola = None
            
        return dato
    
    def buscar(self, criterio, valor):
        actual = self.cabeza
        while actual:
            if getattr(actual.dato, criterio, None) == valor:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
    
    def __len__(self):
        return self.tamaño

# Cola con lista enlazada
class Cola:
    def __init__(self):
        self.lista = ListaEnlazada()
    
    def encolar(self, dato):
        self.lista.insertar(dato)
    
    def desencolar(self):
        return self.lista.eliminar_primero()
    
    def esta_vacia(self):
        return self.lista.esta_vacia()
    
    def tamaño(self):
        return len(self.lista)
    
    def __iter__(self):
        return iter(self.lista)
    
    def __len__(self):
        return len(self.lista)

# Pila implementada con lista enlazada
class Pila:
    def __init__(self):
        self.tope = None
        self.tamaño = 0
    
    def apilar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.tope:
            nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1
    
    def desapilar(self):
        if not self.tope:
            return None
        
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return dato
    
    def ver_tope(self):
        if not self.tope:
            return None
        return self.tope.dato
    
    def esta_vacia(self):
        return self.tope is None
    
    def __len__(self):
        return self.tamaño

# Tabla Hash  (en lugar de diccionarios)
class TablaHash:
    def __init__(self, tamaño=100):
        self.tabla = [None] * tamaño
        self.tamaño = tamaño
        self.elementos = 0
    
    def _hash(self, clave):
        #  strings y números
        if isinstance(clave, str):
            valor = sum(ord(c) for c in clave)
        else:
            valor = int(clave)
            
        return valor % self.tamaño
    
    def insertar(self, clave, valor):
        indice = self._hash(clave)
        
        if self.tabla[indice] is None:
            self.tabla[indice] = ListaEnlazada()
            
        # Buscar si la clave ya existe
        actual = self.tabla[indice].cabeza
        while actual:
            if actual.dato[0] == clave:
                actual.dato = (clave, valor)
                return
            actual = actual.siguiente
        
        # Si no existe, se inserta
        self.tabla[indice].insertar((clave, valor))
        self.elementos += 1
        
        if self.elementos > self.tamaño * 0.7:
            self._redimensionar()
    
    def obtener(self, clave):
        indice = self._hash(clave)
        
        if self.tabla[indice] is None:
            return None
            
        actual = self.tabla[indice].cabeza
        while actual:
            if actual.dato[0] == clave:
                return actual.dato[1]
            actual = actual.siguiente
            
        return None
    
    def eliminar(self, clave):
        indice = self._hash(clave)
        
        if self.tabla[indice] is None:
            return False
            
        anterior = None
        actual = self.tabla[indice].cabeza
        
        while actual and actual.dato[0] != clave:
            anterior = actual
            actual = actual.siguiente
            
        if actual is None:
            return False
            
        if anterior is None:
            self.tabla[indice].cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
            
        self.elementos -= 1
        return True
    
    def _redimensionar(self):
        nuevo_tamaño = self.tamaño * 2
        nueva_tabla = [None] * nuevo_tamaño
        
        for bucket in self.tabla:
            if bucket:
                nodo = bucket.cabeza
                while nodo:
                    clave, valor = nodo.dato
                    indice = hash(clave) % nuevo_tamaño
                    
                    if nueva_tabla[indice] is None:
                        nueva_tabla[indice] = ListaEnlazada()
                        
                    nueva_tabla[indice].insertar((clave, valor))
                    nodo = nodo.siguiente
        
        self.tabla = nueva_tabla
        self.tamaño = nuevo_tamaño
    
    def claves(self):
        resultado = ListaEnlazada()
        for bucket in self.tabla:
            if bucket:
                nodo = bucket.cabeza
                while nodo:
                    resultado.insertar(nodo.dato[0])
                    nodo = nodo.siguiente
        return resultado
    
    def valores(self):
        resultado = ListaEnlazada()
        for bucket in self.tabla:
            if bucket:
                nodo = bucket.cabeza
                while nodo:
                    resultado.insertar(nodo.dato[1])
                    nodo = nodo.siguiente
        return resultado
    
    def items(self):
        resultado = ListaEnlazada()
        for bucket in self.tabla:
            if bucket:
                nodo = bucket.cabeza
                while nodo:
                    resultado.insertar(nodo.dato)
                    nodo = nodo.siguiente
        return resultado
    
    def __iter__(self):
        for bucket in self.tabla:
            if bucket:
                nodo = bucket.cabeza
                while nodo:
                    yield nodo.dato[0]
                    nodo = nodo.siguiente
    
    def __len__(self):
        return self.elementos