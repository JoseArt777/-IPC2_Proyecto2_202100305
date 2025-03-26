class Nodo:
    """
    Clase Nodo básica para estructuras de datos enlazadas.
    Almacena un dato y referencias a nodos siguiente y anterior.
    """
    
    def __init__(self, dato=None):
        """
        Inicializa un nodo con un dato y referencias a None.
        
        Args:
            dato: El valor a almacenar en el nodo
        """
        self.dato = dato
        self.siguiente = None
        self.anterior = None
    
    def __str__(self):
        """
        Representación en cadena del nodo, mostrando su dato.
        
        Returns:
            str: Representación del dato contenido en el nodo
        """
        return str(self.dato)