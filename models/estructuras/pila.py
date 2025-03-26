from models.estructuras.lista import ListaDoble

class Pila:
    """
    Implementación de una pila (LIFO) utilizando una lista enlazada.
    """
    
    def __init__(self):
        """
        Inicializa una pila vacía.
        """
        self.lista = ListaDoble()
    
    def apilar(self, dato):
        """
        Agrega un elemento a la cima de la pila.
        
        Args:
            dato: El elemento a agregar
        """
        self.lista.agregar_inicio(dato)
    
    def desapilar(self):
        """
        Remueve y retorna el elemento en la cima de la pila.
        
        Returns:
            El elemento en la cima de la pila o None si la pila está vacía
        """
        if self.esta_vacia():
            return None
        
        dato = self.lista.cabeza.dato
        self.lista.eliminar(dato)
        return dato
    
    def cima(self):
        """
        Retorna (sin eliminar) el elemento en la cima de la pila.
        
        Returns:
            El elemento en la cima de la pila o None si la pila está vacía
        """
        if self.esta_vacia():
            return None
        
        return self.lista.cabeza.dato
    
    def esta_vacia(self):
        """
        Verifica si la pila está vacía.
        
        Returns:
            bool: True si la pila está vacía, False de lo contrario
        """
        return self.lista.esta_vacia()
    
    def tamanio(self):
        """
        Retorna el número de elementos en la pila.
        
        Returns:
            int: Número de elementos en la pila
        """
        return len(self.lista)
    
    def __len__(self):
        """
        Retorna el tamaño de la pila.
        
        Returns:
            int: Número de elementos en la pila
        """
        return len(self.lista)
    
    def __str__(self):
        """
        Representación en cadena de la pila.
        
        Returns:
            str: Representación de la pila
        """
        return str(self.lista)
    
    def __iter__(self):
        """
        Permite iterar sobre los elementos de la pila.
        
        Returns:
            Iterator: Iterador de la pila
        """
        return iter(self.lista)