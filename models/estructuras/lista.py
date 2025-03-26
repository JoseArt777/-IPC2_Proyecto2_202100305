from models.estructuras.nodo import Nodo

class ListaDoble:
    """
    Implementación de una lista doblemente enlazada.
    """
    
    def __init__(self):
        """
        Inicializa una lista vacía.
        """
        self.cabeza = None
        self.cola = None
        self.tamanio = 0
    
    def esta_vacia(self):
        """
        Verifica si la lista está vacía.
        
        Returns:
            bool: True si la lista está vacía, False de lo contrario
        """
        return self.cabeza is None
    
    def agregar(self, dato):
        """
        Agrega un elemento al final de la lista.
        
        Args:
            dato: El elemento a agregar
        """
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        
        self.tamanio += 1
    
    def agregar_inicio(self, dato):
        """
        Agrega un elemento al inicio de la lista.
        
        Args:
            dato: El elemento a agregar
        """
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        
        self.tamanio += 1
    
    def eliminar(self, dato):
        """
        Elimina la primera ocurrencia del dato especificado.
        
        Args:
            dato: El dato a eliminar
            
        Returns:
            bool: True si se eliminó el elemento, False si no se encontró
        """
        if self.esta_vacia():
            return False
        
        actual = self.cabeza
        
        # Caso especial: eliminar la cabeza
        if actual.dato == dato:
            self.cabeza = actual.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:  # La lista quedó vacía
                self.cola = None
            self.tamanio -= 1
            return True
        
        # Buscar el elemento a eliminar
        while actual and actual.dato != dato:
            actual = actual.siguiente
        
        # No se encontró el elemento
        if not actual:
            return False
        
        # Caso especial: eliminar la cola
        if actual == self.cola:
            self.cola = actual.anterior
            self.cola.siguiente = None
            self.tamanio -= 1
            return True
        
        # Caso general: eliminar elemento del medio
        actual.anterior.siguiente = actual.siguiente
        actual.siguiente.anterior = actual.anterior
        self.tamanio -= 1
        return True
    
    def obtener(self, indice):
        """
        Obtiene el elemento en la posición especificada.
        
        Args:
            indice: Índice del elemento a obtener (0-based)
            
        Returns:
            El dato en la posición especificada o None si el índice está fuera de rango
        """
        if indice < 0 or indice >= self.tamanio:
            return None
        
        actual = self.cabeza
        contador = 0
        
        while contador < indice:
            actual = actual.siguiente
            contador += 1
        
        return actual.dato if actual else None
    
    def buscar(self, dato):
        """
        Busca un elemento en la lista.
        
        Args:
            dato: El dato a buscar
            
        Returns:
            int: Índice de la primera ocurrencia del dato, -1 si no se encuentra
        """
        if self.esta_vacia():
            return -1
        
        actual = self.cabeza
        indice = 0
        
        while actual:
            if actual.dato == dato:
                return indice
            actual = actual.siguiente
            indice += 1
        
        return -1
    
    def buscar_nodo(self, funcion_criterio):
        """
        Busca un nodo según un criterio personalizado.
        
        Args:
            funcion_criterio: Función que toma un dato y devuelve True/False
            
        Returns:
            Nodo: El primer nodo que cumple el criterio, o None si no se encuentra
        """
        if self.esta_vacia():
            return None
        
        actual = self.cabeza
        
        while actual:
            if funcion_criterio(actual.dato):
                return actual
            actual = actual.siguiente
        
        return None
    
    def __len__(self):
        """
        Retorna el tamaño de la lista.
        
        Returns:
            int: Número de elementos en la lista
        """
        return self.tamanio
    
    def __iter__(self):
        """
        Permite iterar sobre la lista.
        
        Returns:
            Iterator: Iterador de la lista
        """
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
    
    def __str__(self):
        """
        Representación en cadena de la lista.
        
        Returns:
            str: Representación de la lista
        """
        elementos = []
        actual = self.cabeza
        
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        
        return "[" + ", ".join(elementos) + "]"