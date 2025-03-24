class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class Lista:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def esta_vacia(self):
        return self.primero is None
    
    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
        self.size += 1
        return nuevo_nodo
    
    def eliminar(self, dato):
        if self.esta_vacia():
            return False
        
        actual = self.primero
        while actual is not None:
            if actual.dato == dato:
                # Si es el único nodo
                if self.primero == self.ultimo:
                    self.primero = None
                    self.ultimo = None
                # Si es el primero
                elif actual == self.primero:
                    self.primero = actual.siguiente
                    self.primero.anterior = None
                # Si es el último
                elif actual == self.ultimo:
                    self.ultimo = actual.anterior
                    self.ultimo.siguiente = None
                # Si está en medio
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                
                self.size -= 1
                return True
            actual = actual.siguiente
        return False
    
    def buscar(self, condicion):
        if self.esta_vacia():
            return None
        
        actual = self.primero
        while actual is not None:
            if condicion(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None
    
    def buscar_nodo(self, condicion):
        if self.esta_vacia():
            return None
        
        actual = self.primero
        while actual is not None:
            if condicion(actual.dato):
                return actual
            actual = actual.siguiente
        return None
    
    def recorrer(self):
        resultado = []
        actual = self.primero
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado