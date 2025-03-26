from models.estructuras.lista import ListaDoble

class Cola:
    """
    Implementación de una cola (FIFO) utilizando una lista enlazada.
    """
    
    def __init__(self):
        """
        Inicializa una cola vacía.
        """
        self.lista = ListaDoble()
    
    def encolar(self, dato):
        """
        Agrega un elemento al final de la cola.
        
        Args:
            dato: El elemento a agregar
        """
        self.lista.agregar(dato)
    
    def desencolar(self):
        """
        Remueve y retorna el elemento al inicio de la cola.
        
        Returns:
            El primer elemento de la cola o None si la cola está vacía
        """
        if self.esta_vacia():
            return None
        
        dato = self.lista.cabeza.dato
        self.lista.eliminar(dato)
        return dato
    
    def frente(self):
        """
        Retorna (sin eliminar) el elemento al inicio de la cola.
        
        Returns:
            El primer elemento de la cola o None si la cola está vacía
        """
        if self.esta_vacia():
            return None
        
        return self.lista.cabeza.dato
    
    def esta_vacia(self):
        """
        Verifica si la cola está vacía.
        
        Returns:
            bool: True si la cola está vacía, False de lo contrario
        """
        return self.lista.esta_vacia()
    
    def tamanio(self):
        """
        Retorna el número de elementos en la cola.
        
        Returns:
            int: Número de elementos en la cola
        """
        return len(self.lista)
    
    def __len__(self):
        """
        Retorna el tamaño de la cola.
        
        Returns:
            int: Número de elementos en la cola
        """
        return len(self.lista)
    
    def __str__(self):
        """
        Representación en cadena de la cola.
        
        Returns:
            str: Representación de la cola
        """
        return str(self.lista)
    
    def __iter__(self):
        """
        Permite iterar sobre los elementos de la cola.
        
        Returns:
            Iterator: Iterador de la cola
        """
        return iter(self.lista)