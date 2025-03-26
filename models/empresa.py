from models.estructuras.lista import ListaDoble

class Empresa:
    """
    Clase que representa una empresa suscrita al sistema de atención al cliente.
    """
    
    def __init__(self, id_empresa, nombre, abreviatura):
        """
        Inicializa una empresa.
        
        Args:
            id_empresa (str): ID único de la empresa
            nombre (str): Nombre completo de la empresa
            abreviatura (str): Abreviatura o nombre corto de la empresa
        """
        self.id = id_empresa
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = ListaDoble()  # Lista de puntos de atención
        self.transacciones = ListaDoble()    # Lista de transacciones disponibles
    
    def agregar_punto_atencion(self, punto_atencion):
        """
        Agrega un punto de atención a la empresa.
        
        Args:
            punto_atencion: Punto de atención a agregar
        """
        self.puntos_atencion.agregar(punto_atencion)
    
    def agregar_transaccion(self, transaccion):
        """
        Agrega una transacción a la empresa.
        
        Args:
            transaccion: Transacción a agregar
        """
        self.transacciones.agregar(transaccion)
    
    def obtener_punto_atencion(self, id_punto):
        """
        Obtiene un punto de atención por su ID.
        
        Args:
            id_punto (str): ID del punto de atención a buscar
            
        Returns:
            PuntoAtencion: El punto de atención encontrado o None si no existe
        """
        for punto in self.puntos_atencion:
            if punto.id == id_punto:
                return punto
        return None
    
    def obtener_transaccion(self, id_transaccion):
        """
        Obtiene una transacción por su ID.
        
        Args:
            id_transaccion (str): ID de la transacción a buscar
            
        Returns:
            Transaccion: La transacción encontrada o None si no existe
        """
        for transaccion in self.transacciones:
            if transaccion.id == id_transaccion:
                return transaccion
        return None
    
    def __str__(self):
        """
        Representación en cadena de la empresa.
        
        Returns:
            str: Representación de la empresa
        """
        return f"Empresa: {self.nombre} (ID: {self.id}, Abreviatura: {self.abreviatura})"
    
    def __eq__(self, other):
        """
        Compara si dos empresas son iguales basándose en su ID.
        
        Args:
            other: Otra empresa para comparar
            
        Returns:
            bool: True si son iguales, False de lo contrario
        """
        if not isinstance(other, Empresa):
            return False
        return self.id == other.id