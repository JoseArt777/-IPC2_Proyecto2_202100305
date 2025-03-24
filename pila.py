from lista import Lista, Nodo

class Pila:
    def __init__(self):
        self.lista = Lista()
    
    def apilar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.lista.esta_vacia():
            self.lista.primero = nuevo_nodo
            self.lista.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.lista.primero
            self.lista.primero.anterior = nuevo_nodo
            self.lista.primero = nuevo_nodo
        self.lista.size += 1
    
    def desapilar(self):
        if self.lista.esta_vacia():
            return None
        
        dato = self.lista.primero.dato
        
        # Si es el único elemento
        if self.lista.primero == self.lista.ultimo:
            self.lista.primero = None
            self.lista.ultimo = None
        else:
            self.lista.primero = self.lista.primero.siguiente
            self.lista.primero.anterior = None
        
        self.lista.size -= 1
        return dato
    
    def tope(self):
        if self.lista.esta_vacia():
            return None
        return self.lista.primero.dato
    
    def esta_vacia(self):
        return self.lista.esta_vacia()
    
    def tamano(self):
        return self.lista.size
    
    def recorrer(self):
        return self.lista.recorrer()