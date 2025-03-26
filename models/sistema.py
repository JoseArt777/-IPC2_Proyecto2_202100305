from models.estructuras.lista import ListaDoble

class Sistema:
    """
    Clase principal que representa el sistema de atención al cliente de "Soluciones Guatemaltecas, S.A."
    """
    
    def __init__(self):
        """
        Inicializa el sistema.
        """
        self.empresas = ListaDoble()  # Lista de empresas suscritas
        self.empresa_actual = None    # Empresa seleccionada actualmente
        self.punto_actual = None      # Punto de atención seleccionado actualmente
    
    def limpiar_sistema(self):
        """
        Inicializa todas las estructuras de datos para comenzar una nueva prueba.
        """
        self.empresas = ListaDoble()
        self.empresa_actual = None
        self.punto_actual = None
    
    def agregar_empresa(self, empresa):
        """
        Agrega una empresa al sistema.
        
        Args:
            empresa: Empresa a agregar
        """
        self.empresas.agregar(empresa)
    
    def obtener_empresa(self, id_empresa):
        """
        Obtiene una empresa por su ID.
        
        Args:
            id_empresa (str): ID de la empresa a buscar
            
        Returns:
            Empresa: La empresa encontrada o None si no existe
        """
        for empresa in self.empresas:
            if empresa.id == id_empresa:
                return empresa
        return None
    
    def seleccionar_empresa(self, id_empresa):
        """
        Selecciona una empresa como la empresa actual.
        
        Args:
            id_empresa (str): ID de la empresa a seleccionar
            
        Returns:
            bool: True si se encontró y seleccionó la empresa, False de lo contrario
        """
        empresa = self.obtener_empresa(id_empresa)
        if empresa:
            self.empresa_actual = empresa
            self.punto_actual = None  # Limpiar selección de punto de atención
            return True
        return False
    
    def seleccionar_punto_atencion(self, id_punto):
        """
        Selecciona un punto de atención como el punto actual.
        
        Args:
            id_punto (str): ID del punto de atención a seleccionar
            
        Returns:
            bool: True si se encontró y seleccionó el punto, False de lo contrario
        """
        if not self.empresa_actual:
            return False
        
        punto = self.empresa_actual.obtener_punto_atencion(id_punto)
        if punto:
            self.punto_actual = punto
            return True
        return False
    
    def crear_empresa(self, id_empresa, nombre, abreviatura):
        """
        Crea y agrega una nueva empresa al sistema.
        
        Args:
            id_empresa (str): ID de la nueva empresa
            nombre (str): Nombre de la nueva empresa
            abreviatura (str): Abreviatura de la nueva empresa
            
        Returns:
            Empresa: La empresa creada, o None si ya existe una empresa con ese ID
        """
        # Verificar que no exista otra empresa con el mismo ID
        if self.obtener_empresa(id_empresa):
            return None
        
        from models.empresa import Empresa
        empresa = Empresa(id_empresa, nombre, abreviatura)
        self.agregar_empresa(empresa)
        return empresa
    
    def crear_punto_atencion(self, id_empresa, id_punto, nombre, direccion):
        """
        Crea y agrega un nuevo punto de atención a una empresa.
        
        Args:
            id_empresa (str): ID de la empresa
            id_punto (str): ID del nuevo punto de atención
            nombre (str): Nombre del punto de atención
            direccion (str): Dirección del punto de atención
            
        Returns:
            PuntoAtencion: El punto de atención creado, o None si no existe la empresa
            o ya existe un punto con ese ID
        """
        empresa = self.obtener_empresa(id_empresa)
        if not empresa:
            return None
        
        # Verificar que no exista otro punto con el mismo ID
        if empresa.obtener_punto_atencion(id_punto):
            return None
        
        from models.punto_atencion import PuntoAtencion
        punto = PuntoAtencion(id_punto, nombre, direccion)
        empresa.agregar_punto_atencion(punto)
        return punto
    
    def crear_escritorio(self, id_empresa, id_punto, id_escritorio, identificacion, encargado):
        """
        Crea y agrega un nuevo escritorio a un punto de atención.
        
        Args:
            id_empresa (str): ID de la empresa
            id_punto (str): ID del punto de atención
            id_escritorio (str): ID del nuevo escritorio
            identificacion (str): Identificación visible del escritorio
            encargado (str): Nombre del encargado del escritorio
            
        Returns:
            Escritorio: El escritorio creado, o None si no existe la empresa o punto
        """
        empresa = self.obtener_empresa(id_empresa)
        if not empresa:
            return None
        
        punto = empresa.obtener_punto_atencion(id_punto)
        if not punto:
            return None
        
        from models.escritorio import Escritorio
        escritorio = Escritorio(id_escritorio, identificacion, encargado)
        punto.agregar_escritorio(escritorio)
        return escritorio
    
    def crear_transaccion(self, id_empresa, id_transaccion, nombre, tiempo_atencion):
        """
        Crea y agrega una nueva transacción a una empresa.
        
        Args:
            id_empresa (str): ID de la empresa
            id_transaccion (str): ID de la nueva transacción
            nombre (str): Nombre de la transacción
            tiempo_atencion (int): Tiempo en minutos para atender la transacción
            
        Returns:
            Transaccion: La transacción creada, o None si no existe la empresa o ya existe la transacción
        """
        empresa = self.obtener_empresa(id_empresa)
        if not empresa:
            return None
        
        # Verificar que no exista otra transacción con el mismo ID
        if empresa.obtener_transaccion(id_transaccion):
            return None
        
        from models.transaccion import Transaccion
        transaccion = Transaccion(id_transaccion, nombre, tiempo_atencion)
        empresa.agregar_transaccion(transaccion)
        return transaccion
    
    def activar_escritorio(self, id_escritorio):
        """
        Activa un escritorio en el punto de atención actual.
        
        Args:
            id_escritorio (str): ID del escritorio a activar
            
        Returns:
            bool: True si se activó correctamente, False de lo contrario
        """
        if not self.punto_actual:
            return False
        
        return self.punto_actual.activar_escritorio(id_escritorio)
    
    def desactivar_escritorio(self, id_escritorio):
        """
        Desactiva un escritorio en el punto de atención actual.
        
        Args:
            id_escritorio (str): ID del escritorio a desactivar
            
        Returns:
            bool: True si se desactivó correctamente, False de lo contrario
        """
        if not self.punto_actual:
            return False
        
        return self.punto_actual.desactivar_escritorio(id_escritorio)
    
    def solicitar_atencion(self, cliente):
        """
        Registra una solicitud de atención en el punto actual.
        
        Args:
            cliente: Cliente que solicita atención
            
        Returns:
            tuple: (número_atención, tiempo_espera_estimado) o (None, None) si no hay punto seleccionado
        """
        if not self.punto_actual:
            return None, None
        
        return self.punto_actual.solicitar_atencion(cliente)
    
    def atender_cliente(self):
        """
        Finaliza la atención del próximo cliente que termine su tiempo en el punto actual.
        
        Returns:
            tuple: (cliente_atendido, escritorio) o (None, None) si no hay punto seleccionado
            o no hay clientes siendo atendidos
        """
        if not self.punto_actual:
            return None, None
        
        return self.punto_actual.atender_cliente()
    
    def simular_atencion_completa(self):
        """
        Simula la atención de todos los clientes en el punto actual.
        
        Returns:
            dict: Estadísticas de la simulación o None si no hay punto seleccionado
        """
        if not self.punto_actual:
            return None
        
        return self.punto_actual.simular_atencion_completa()
    
    def obtener_estado_punto_actual(self):
        """
        Obtiene el estado actual del punto de atención seleccionado.
        
        Returns:
            dict: Estado del punto o None si no hay punto seleccionado
        """
        if not self.punto_actual:
            return None
        
        return self.punto_actual.obtener_estado()