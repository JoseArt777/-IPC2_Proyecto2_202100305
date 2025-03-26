import time
from models.estructuras.lista import ListaDoble

class Escritorio:
    """
    Clase que representa un escritorio de servicio donde se atienden clientes.
    """
    
    def __init__(self, id_escritorio, identificacion, encargado):
        """
        Inicializa un escritorio.
        
        Args:
            id_escritorio (str): ID único del escritorio
            identificacion (str): Nombre o identificación visible del escritorio
            encargado (str): Nombre del encargado del escritorio
        """
        self.id = id_escritorio
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False
        self.cliente_actual = None
        self.tiempo_restante = 0  # Tiempo restante para terminar la atención actual
        
        # Estadísticas
        self.clientes_atendidos = 0
        self.tiempos_atencion = ListaDoble()  # Lista de tiempos de atención para cada cliente
        self.hora_activacion = None
    
    def activar(self):
        """
        Activa el escritorio para atender clientes.
        """
        self.activo = True
        self.hora_activacion = time.time()
    
    def desactivar(self):
        """
        Desactiva el escritorio para que no atienda más clientes una vez
        termine con el cliente actual.
        """
        self.activo = False
    
    def esta_disponible(self):
        """
        Verifica si el escritorio está activo y disponible para atender.
        
        Returns:
            bool: True si el escritorio está activo y sin cliente actual, False de lo contrario
        """
        return self.activo and self.cliente_actual is None
    
    def asignar_cliente(self, cliente):
        """
        Asigna un cliente al escritorio para ser atendido.
        
        Args:
            cliente: Cliente a atender
            
        Returns:
            bool: True si se asignó correctamente, False si el escritorio no está disponible
        """
        if not self.esta_disponible():
            return False
        
        self.cliente_actual = cliente
        self.tiempo_restante = cliente.calcular_tiempo_total_atencion()
        cliente.iniciar_atencion(self)
        
        return True
    
    def atender_tiempo(self, minutos):
        """
        Procesa la atención del cliente durante un tiempo específico.
        
        Args:
            minutos (int): Minutos que avanza la atención
            
        Returns:
            bool: True si el cliente terminó de ser atendido, False si continúa en atención
        """
        if self.cliente_actual is None:
            return False
        
        self.tiempo_restante -= minutos
        
        # Si ya se completó la atención
        if self.tiempo_restante <= 0:
            self.finalizar_atencion()
            return True
        
        return False
    
    def finalizar_atencion(self):
        """
        Finaliza la atención del cliente actual.
        
        Returns:
            Cliente: El cliente que fue atendido
        """
        if self.cliente_actual is None:
            return None
        
        cliente = self.cliente_actual
        cliente.finalizar_atencion()
        
        # Actualizar estadísticas
        self.clientes_atendidos += 1
        tiempo_total = (cliente.hora_finalizacion - cliente.hora_atencion) / 60  # Convertir a minutos
        self.tiempos_atencion.agregar(tiempo_total)
        
        # Liberar el escritorio
        self.cliente_actual = None
        self.tiempo_restante = 0
        
        return cliente
    
    def tiempo_promedio_atencion(self):
        """
        Calcula el tiempo promedio de atención.
        
        Returns:
            float: Tiempo promedio de atención en minutos o 0 si no hay datos
        """
        if len(self.tiempos_atencion) == 0:
            return 0
        
        total = 0
        for tiempo in self.tiempos_atencion:
            total += tiempo
        
        return total / len(self.tiempos_atencion)
    
    def tiempo_maximo_atencion(self):
        """
        Obtiene el tiempo máximo de atención.
        
        Returns:
            float: Tiempo máximo de atención en minutos o 0 si no hay datos
        """
        if len(self.tiempos_atencion) == 0:
            return 0
        
        maximo = 0
        for tiempo in self.tiempos_atencion:
            if tiempo > maximo:
                maximo = tiempo
        
        return maximo
    
    def tiempo_minimo_atencion(self):
        """
        Obtiene el tiempo mínimo de atención.
        
        Returns:
            float: Tiempo mínimo de atención en minutos o 0 si no hay datos
        """
        if len(self.tiempos_atencion) == 0:
            return 0
        
        if len(self.tiempos_atencion) == 1:
            return self.tiempos_atencion.obtener(0)
        
        minimo = float('inf')
        for tiempo in self.tiempos_atencion:
            if tiempo < minimo:
                minimo = tiempo
        
        return minimo
    
    def __str__(self):
        """
        Representación en cadena del escritorio.
        
        Returns:
            str: Representación del escritorio
        """
        estado = "Activo" if self.activo else "Inactivo"
        cliente = str(self.cliente_actual) if self.cliente_actual else "Sin cliente"
        return f"Escritorio {self.identificacion} (ID: {self.id}) - {estado} - Encargado: {self.encargado} - {cliente}"
    
    def __eq__(self, other):
        """
        Compara si dos escritorios son iguales basándose en su ID.
        
        Args:
            other: Otro escritorio para comparar
            
        Returns:
            bool: True si son iguales, False de lo contrario
        """
        if not isinstance(other, Escritorio):
            return False
        return self.id == other.id