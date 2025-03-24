class Escritorio:
    def __init__(self, id, identificacion, encargado):
        self.id = id
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False
        self.cliente_actual = None
        self.tiempo_restante = 0
        
        # Estadísticas
        self.clientes_atendidos = 0
        self.tiempo_total_atencion = 0
        self.tiempo_maximo_atencion = float('-inf')
        self.tiempo_minimo_atencion = float('inf')
    
    def asignar_cliente(self, cliente, tiempo_actual):
        # Asignar un cliente al escritorio
        self.cliente_actual = cliente
        self.tiempo_restante = cliente.calcular_tiempo_atencion()
        cliente.hora_atencion = tiempo_actual
        cliente.tiempo_espera = tiempo_actual - cliente.hora_llegada
    
    def atender_cliente(self, tiempo):
        # Procesar la atención del cliente por un tiempo determinado
        if self.cliente_actual is None:
            return 0
        
        tiempo_procesado = min(tiempo, self.tiempo_restante)
        self.tiempo_restante -= tiempo_procesado
        
        return tiempo_procesado
    
    def finalizar_atencion(self):
        # Finalizar la atención del cliente actual
        if self.cliente_actual is None:
            return None
        
        cliente_atendido = self.cliente_actual
        tiempo_atencion = cliente_atendido.tiempo_atencion
        
        # Actualizar estadísticas
        self.clientes_atendidos += 1
        self.tiempo_total_atencion += tiempo_atencion
        
        if tiempo_atencion > self.tiempo_maximo_atencion:
            self.tiempo_maximo_atencion = tiempo_atencion
            
        if tiempo_atencion < self.tiempo_minimo_atencion:
            self.tiempo_minimo_atencion = tiempo_atencion
        
        self.cliente_actual = None
        self.tiempo_restante = 0
        
        return cliente_atendido
    
    def activar(self):
        # Activar el escritorio
        self.activo = True
    
    def desactivar(self):
        # Desactivar el escritorio
        self.activo = False
    
    def calcular_estadisticas(self):
        # Actualizar estadísticas del escritorio
        tiempo_promedio = 0
        if self.clientes_atendidos > 0:
            tiempo_promedio = self.tiempo_total_atencion / self.clientes_atendidos
            
        # Corregir valores infinitos si no hay datos
        if self.tiempo_maximo_atencion == float('-inf'):
            self.tiempo_maximo_atencion = 0
        
        if self.tiempo_minimo_atencion == float('inf'):
            self.tiempo_minimo_atencion = 0
            
        return {
            'clientes_atendidos': self.clientes_atendidos,
            'tiempo_promedio': tiempo_promedio,
            'tiempo_maximo': self.tiempo_maximo_atencion,
            'tiempo_minimo': self.tiempo_minimo_atencion
        }