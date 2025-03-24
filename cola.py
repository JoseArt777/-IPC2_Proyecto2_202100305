from lista import Lista, Nodo

class Cola:
    def __init__(self):
        self.lista = Lista()
    
    def encolar(self, dato):
        self.lista.insertar(dato)
    
    def desencolar(self):
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
    
    def frente(self):
        if self.lista.esta_vacia():
            return None
        return self.lista.primero.dato
    
    def esta_vacia(self):
        return self.lista.esta_vacia()
    
    def tamano(self):
        return self.lista.size
    
    def recorrer(self):
        return self.lista.recorrer()