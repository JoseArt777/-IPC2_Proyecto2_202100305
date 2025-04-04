import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estructuras import ListaEnlazada, Cola, TablaHash, Pila

class Transaccion:
    def __init__(self, id_transaccion, nombre, tiempo_atencion):
        self.id = id_transaccion
        self.nombre = nombre
        self.tiempo_atencion = tiempo_atencion  # en minutos
    
    def __str__(self):
        return f"Transaccion[{self.id}]: {self.nombre} ({self.tiempo_atencion} min)"

# Clase para escritorio de servicio
class EscritorioServicio:
    INACTIVO = 0
    ACTIVO = 1
    OCUPADO = 2
    
    def __init__(self, id_escritorio, identificacion, encargado):
        self.id = id_escritorio
        self.identificacion = identificacion
        self.encargado = encargado
        self.estado = self.INACTIVO
        self.cliente_actual = None
        self.tiempo_restante = 0
        self.pendiente_desactivar = False  # Añadir esta línea

        
        # Estadística
        self.clientes_atendidos = 0
        self.tiempo_total_atencion = 0
        self.tiempo_min_atencion = float('inf')
        self.tiempo_max_atencion = 0
    
    def activar(self):
        if self.estado == self.INACTIVO:
            self.estado = self.ACTIVO
            return True
        return False
    
    def desactivar(self):
        if self.estado == self.ACTIVO:
            self.estado = self.INACTIVO
            return True
        elif self.estado == self.OCUPADO:
            self.pendiente_desactivar = True
            return True
        return False

    
    def asignar_cliente(self, cliente):
        if self.estado == self.ACTIVO and self.cliente_actual is None:
            self.cliente_actual = cliente
            self.tiempo_restante = cliente.calcular_tiempo_total()
            self.estado = self.OCUPADO
            return True
        return False
    
    def actualizar_tiempo(self, tiempo_transcurrido=1):
        if self.estado == self.OCUPADO and self.cliente_actual:
            self.tiempo_restante -= tiempo_transcurrido
            if self.tiempo_restante <= 0:
                self.completar_atencion()
            return True
        return False
    
    def completar_atencion(self):
        if self.cliente_actual:
            tiempo_total = self.cliente_actual.calcular_tiempo_total()
            self.clientes_atendidos += 1
            self.tiempo_total_atencion += tiempo_total
            self.tiempo_min_atencion = min(self.tiempo_min_atencion, tiempo_total)
            self.tiempo_max_atencion = max(self.tiempo_max_atencion, tiempo_total)
            
            self.cliente_actual = None
            self.tiempo_restante = 0
            
            if self.pendiente_desactivar:
                self.estado = self.INACTIVO
                self.pendiente_desactivar = False
            else:
                self.estado = self.ACTIVO
            
            return True
        return False

    
    def esta_disponible(self):
        return self.estado == self.ACTIVO and self.cliente_actual is None
    
    def tiempo_promedio_atencion(self):
        if self.clientes_atendidos == 0:
            return 0
        return self.tiempo_total_atencion / self.clientes_atendidos
    
    def __str__(self):
        estado_str = "Inactivo"
        if self.estado == self.ACTIVO:
            estado_str = "Activo"
        elif self.estado == self.OCUPADO:
            estado_str = "Ocupado"
            
        cliente_str = "Ninguno"
        if self.cliente_actual:
            cliente_str = str(self.cliente_actual)
            
        return f"Escritorio[{self.id}]: {self.identificacion} ({estado_str}) - Cliente: {cliente_str}"

# Clase punto de atención

class PuntoAtencion:
    def __init__(self, id_punto, nombre, direccion):
        self.id = id_punto
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = ListaEnlazada()
        self.cola_clientes = Cola()
        self.pila_escritorios_activos = Pila()  
        self.siguiente_indice_activar = 0 


        # Estadísticas (no cambian)
        self.tiempo_total_espera = 0
        self.tiempo_min_espera = float('inf')
        self.tiempo_max_espera = 0
        self.clientes_atendidos = 0

    def activar_escritorio_auto(self):
        num_escritorios = len(self.escritorios)
        contador = 0

        # Intenta activar escritorios comenzando desde el siguiente índice
        while contador < num_escritorios:
            indice_actual = (self.siguiente_indice_activar + contador) % num_escritorios
            escritorio = self.escritorios.obtener(indice_actual)

            if escritorio.estado == escritorio.INACTIVO and not escritorio.pendiente_desactivar:
                if escritorio.activar():
                    self.pila_escritorios_activos.apilar(escritorio)
                    self.asignar_clientes()
                    self.siguiente_indice_activar = (indice_actual + 1) % num_escritorios
                    return escritorio
            contador += 1

        return None



    def desactivar_escritorio_auto(self):
        """
        Desactiva el último escritorio activado (LIFO)
        """
        if self.pila_escritorios_activos.esta_vacia():
            for escritorio in self.escritorios:
                if escritorio.estado == escritorio.ACTIVO or escritorio.estado == escritorio.OCUPADO:
                    escritorio.desactivar()
                    return escritorio
            return None  

        temp_pila = Pila()
        escritorio_desactivado = None

        # Buscar el primer escritorio que se pueda desactivar (LIFO)
        while not self.pila_escritorios_activos.esta_vacia():
            escritorio = self.pila_escritorios_activos.desapilar()
            
            if escritorio.estado == escritorio.INACTIVO:
                continue
                
            # Si se puede desactivar
            escritorio.desactivar()  # desactivar el escritorio
            escritorio_desactivado = escritorio
            break
            
        # Reconstruir la pila con los escritorios que no desactivamos
        while not temp_pila.esta_vacia():
            self.pila_escritorios_activos.apilar(temp_pila.desapilar())
            
        # Si no encontramos ningún escritorio para desactivar, busquemos uno manualmente
        if escritorio_desactivado is None:
            for escritorio in self.escritorios:
                if escritorio.estado == escritorio.ACTIVO or escritorio.estado == escritorio.OCUPADO:
                    escritorio.desactivar()
                    return escritorio
                    
        return escritorio_desactivado
    
    def agregar_escritorio(self, escritorio):
        self.escritorios.insertar(escritorio)
    
    def activar_escritorio(self, id_escritorio):
        for escritorio in self.escritorios:
            if escritorio.id == id_escritorio:
                return escritorio.activar()
        return False
    
    def desactivar_escritorio(self, id_escritorio):
        for escritorio in self.escritorios:
            if escritorio.id == id_escritorio:
                return escritorio.desactivar()
        return False
    
    def encolar_cliente(self, cliente):
        self.cola_clientes.encolar(cliente)
        return len(self.cola_clientes) 
    
    def asignar_clientes(self, tiempo_actual=0):
        """
        Asigna clientes a escritorios disponibles.
        Ahora recibe el tiempo actual para calcular tiempos de espera.
        """
        clientes_asignados = 0
        
        # Verificar si hay escritorios disponibles y clientes en espera
        if self.cola_clientes.esta_vacia():
            return clientes_asignados
        
        # Asignar clientes a escritorios disponibles
        for escritorio in self.escritorios:
            if escritorio.esta_disponible() and not self.cola_clientes.esta_vacia():
                cliente = self.cola_clientes.desencolar()
                
                # Calcular tiempo de espera real
                tiempo_espera = tiempo_actual - cliente.hora_llegada
                if tiempo_espera < 0:  # Protección contra errores
                    tiempo_espera = 0
                    
                # Registrar estadísticas de espera
                self.tiempo_total_espera += tiempo_espera
                self.clientes_atendidos += 1
                
                if tiempo_espera < self.tiempo_min_espera:
                    self.tiempo_min_espera = tiempo_espera
                    
                if tiempo_espera > self.tiempo_max_espera:
                    self.tiempo_max_espera = tiempo_espera
                
                # Asignar cliente al escritorio
                escritorio.asignar_cliente(cliente)
                clientes_asignados += 1
        
        return clientes_asignados
    
    def atender_cliente(self):
     
        # Buscar el escritorio con menor tiempo restante
        escritorio_min = None
        tiempo_min = float('inf')
        
        for escritorio in self.escritorios:
            if escritorio.estado == EscritorioServicio.OCUPADO and escritorio.tiempo_restante < tiempo_min:
                escritorio_min = escritorio
                tiempo_min = escritorio.tiempo_restante
        
        # Si encontramos un escritorio ocupado, completar la atención
        if escritorio_min:
            escritorio_min.completar_atencion()
            self.asignar_clientes()
            return True
        
        return False
    
    def simular_actividad(self, tiempo_inicial=0):
            """
            Simula la atención de todos los clientes pendientes.
            Ahora recibe el tiempo inicial para cálculos de espera.
            """
            # Primero asignar clientes disponibles con el tiempo actual
            self.asignar_clientes(tiempo_inicial)
            
            tiempo_actual = tiempo_inicial
            iteraciones = 0
            clientes_atendidos_total = 0
            
            while not self.cola_clientes.esta_vacia() or self._hay_escritorios_ocupados():
                # Avanzar 1 minuto en todos los escritorios ocupados
                for escritorio in self.escritorios:
                    if escritorio.estado == EscritorioServicio.OCUPADO:
                        escritorio.actualizar_tiempo(1)
                
                # Avanzar el tiempo de simulación
                tiempo_actual += 1
                
                # Asigna nuevos clientes si hay escritorios disponibles
                self.asignar_clientes(tiempo_actual)
                
                iteraciones += 1
                if iteraciones > 1000: # Evitar bucle infinito
                    break
            
            return clientes_atendidos_total
    
    def _hay_escritorios_ocupados(self):
        for escritorio in self.escritorios:
            if escritorio.estado == EscritorioServicio.OCUPADO:
                return True
        return False
    
    def obtener_estadisticas(self):
        """
        Retorna estadísticas generales del punto de atención.
        """
        escritorios_activos = 0
        escritorios_inactivos = 0
        
        for escritorio in self.escritorios:
            if escritorio.estado == EscritorioServicio.INACTIVO:
                escritorios_inactivos += 1
            else:
                escritorios_activos += 1
        
        tiempo_promedio_espera = 0
        if self.clientes_atendidos > 0:
            tiempo_promedio_espera = self.tiempo_total_espera / self.clientes_atendidos
        
        # Cálculo de tiempos de atención
        tiempo_total_atencion = 0
        tiempo_min_atencion = float('inf')
        tiempo_max_atencion = 0
        total_clientes_atendidos = 0
        
        for escritorio in self.escritorios:
            if escritorio.clientes_atendidos > 0:
                tiempo_total_atencion += escritorio.tiempo_total_atencion
                total_clientes_atendidos += escritorio.clientes_atendidos
                
                if escritorio.tiempo_min_atencion < tiempo_min_atencion:
                    tiempo_min_atencion = escritorio.tiempo_min_atencion
                    
                if escritorio.tiempo_max_atencion > tiempo_max_atencion:
                    tiempo_max_atencion = escritorio.tiempo_max_atencion
        
        tiempo_promedio_atencion = 0
        if total_clientes_atendidos > 0:
            tiempo_promedio_atencion = tiempo_total_atencion / total_clientes_atendidos
        
        return {
            "escritorios_activos": escritorios_activos,
            "escritorios_inactivos": escritorios_inactivos,
            "clientes_en_espera": len(self.cola_clientes),
            "clientes_atendidos": total_clientes_atendidos,
            "tiempo_promedio_espera": tiempo_promedio_espera,
            "tiempo_min_espera": self.tiempo_min_espera if self.tiempo_min_espera != float('inf') else 0,
            "tiempo_max_espera": self.tiempo_max_espera,
            "tiempo_promedio_atencion": tiempo_promedio_atencion,
            "tiempo_min_atencion": tiempo_min_atencion if tiempo_min_atencion != float('inf') else 0,
            "tiempo_max_atencion": tiempo_max_atencion
        }
    
    def __str__(self):
        return f"PuntoAtencion[{self.id}]: {self.nombre} - {self.direccion}"

# Clase que representa una empresa
class Empresa:
    def __init__(self, id_empresa, nombre, abreviatura):
        self.id = id_empresa
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = ListaEnlazada()
        self.transacciones = TablaHash()
    
    def agregar_punto_atencion(self, punto_atencion):
        self.puntos_atencion.insertar(punto_atencion)
    
    def agregar_transaccion(self, transaccion):
        self.transacciones.insertar(transaccion.id, transaccion)
    
    def obtener_punto_atencion(self, id_punto):
        for punto in self.puntos_atencion:
            if punto.id == id_punto:
                return punto
        return None
    
    def obtener_transaccion(self, id_transaccion):
        return self.transacciones.obtener(id_transaccion)
    
    def __str__(self):
        return f"Empresa[{self.id}]: {self.nombre} ({self.abreviatura})"

# Clase que representa un cliente
class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = ListaEnlazada() 
        self.hora_llegada = 0 
    
    def agregar_transaccion(self, transaccion, cantidad=1):
        self.transacciones.insertar((transaccion, cantidad))
    
    def calcular_tiempo_total(self):
        """
        Calcula el tiempo total necesario para atender todas las transacciones del cliente.
        """
        tiempo_total = 0
        for transaccion, cantidad in self.transacciones:
            tiempo_total += transaccion.tiempo_atencion * cantidad
        return tiempo_total
    
    def __str__(self):
        return f"Cliente[{self.dpi}]: {self.nombre}"