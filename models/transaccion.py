class Transaccion:
    """
    Clase que representa una transacción que puede ser atendida en un punto de atención.
    """
    
    def __init__(self, id_transaccion, nombre, tiempo_atencion):
        """
        Inicializa una transacción.
        
        Args:
            id_transaccion (str): Identificador único de la transacción
            nombre (str): Nombre descriptivo de la transacción
            tiempo_atencion (int): Tiempo en minutos necesario para atender la transacción
        """
        self.id = id_transaccion
        self.nombre = nombre
        self.tiempo_atencion = tiempo_atencion
    
    def __str__(self):
        """
        Representación en cadena de la transacción.
        
        Returns:
            str: Representación de la transacción
        """
        return f"{self.nombre} (ID: {self.id}, Tiempo: {self.tiempo_atencion} min)"
    
    def __eq__(self, other):
        """
        Compara si dos transacciones son iguales basándose en su ID.
        
        Args:
            other: Otra transacción para comparar
            
        Returns:
            bool: True si son iguales, False de lo contrario
        """
        if not isinstance(other, Transaccion):
            return False
        return self.id == other.id