
from models.estructuras.lista import ListaDoble
import time

class Cliente:
    """
    Clase que representa a un cliente que solicita atención.
    """
    
    def __init__(self, dpi, nombre):
        """
        Inicializa un cliente.
        
        Args:
            dpi (str): DPI o identificador único del cliente
            nombre (str): Nombre del cliente
        """
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = ListaDoble()  # Lista de objetos (transaccion, cantidad)
        self.tiempo_espera = 0  # Tiempo total que el cliente espera desde que solicita atención
        self.tiempo_atencion = 0  # Tiempo total estimado de atención para todas sus transacciones
        self.hora_llegada = time.time()  # Timestamp de llegada
        self.hora_atencion = None  # Timestamp de cuando comienza a ser atendido
        self.hora_finalizacion = None  # Timestamp de cuando termina de ser atendido
        self.escritorio_asignado = None  # Escritorio que atiende al cliente
    
    def agregar_transaccion(self, transaccion, cantidad=1):
        """
        Agrega una transacción a la lista de transacciones del cliente.
        
        Args:
            transaccion: Objeto Transaccion que el cliente desea realizar
            cantidad (int): Cantidad de veces que desea realizar la transacción
        """
        # Almacenamos una tupla (transaccion, cantidad)
        self.transacciones.agregar((transaccion, cantidad))
        # Actualizar tiempo total de atención
        self.tiempo_atencion += transaccion.tiempo_atencion * cantidad
    
    def calcular_tiempo_total_atencion(self):
        """
        Calcula el tiempo total necesario para atender todas las transacciones del cliente.
        
        Returns:
            int: Tiempo total en minutos
        """
        tiempo_total = 0
        for trans_tuple in self.transacciones:
            transaccion, cantidad = trans_tuple
            tiempo_total += transaccion.tiempo_atencion * cantidad
        
        return tiempo_total
    
    def iniciar_atencion(self, escritorio):
        """
        Marca al cliente como en atención por un escritorio específico.
        
        Args:
            escritorio: Escritorio que atenderá al cliente
        """
        self.hora_atencion = time.time()
        self.escritorio_asignado = escritorio
        self.tiempo_espera = self.hora_atencion - self.hora_llegada
    
    def finalizar_atencion(self):
        """
        Marca al cliente como atendido completamente.
        """
        self.hora_finalizacion = time.time()
    
    def __str__(self):
        """
        Representación en cadena del cliente.
        
        Returns:
            str: Representación del cliente
        """
        return f"{self.nombre} (DPI: {self.dpi}, Transacciones: {len(self.transacciones)})"
    
    def __eq__(self, other):
        """
        Compara si dos clientes son iguales basándose en su DPI.
        
        Args:
            other: Otro cliente para comparar
            
        Returns:
            bool: True si son iguales, False de lo contrario
        """
        if not isinstance(other, Cliente):
            return False
        return self.dpi == other.dpi