from models.estructuras.lista import ListaDoble
from models.estructuras.cola import Cola
import time

class PuntoAtencion:
    """
    Clase que representa un punto de atención de una empresa.
    """
    
    def __init__(self, id_punto, nombre, direccion):
        """
        Inicializa un punto de atención.
        
        Args:
            id_punto (str): ID único del punto de atención
            nombre (str): Nombre del punto de atención
            direccion (str): Dirección física del punto de atención
        """
        self.id = id_punto
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = ListaDoble()  # Lista de todos los escritorios
        self.escritorios_activos = ListaDoble()  # Lista de escritorios activos
        self.cola_clientes = Cola()  # Cola de clientes en espera
        
        # Estadísticas
        self.clientes_atendidos = 0
        self.tiempos_espera = ListaDoble()  # Lista de tiempos de espera para cada cliente
        self.tiempos_atencion = ListaDoble()  # Lista de tiempos de atención para cada cliente
    
    def agregar_escritorio(self, escritorio):
        """
        Agrega un escritorio al punto de atención.
        
        Args:
            escritorio: Escritorio a agregar
        """
        self.escritorios.agregar(escritorio)
    
    def activar_escritorio(self, id_escritorio):
        """
        Activa un escritorio para que atienda clientes.
        
        Args:
            id_escritorio (str): ID del escritorio a activar
            
        Returns:
            bool: True si se activó correctamente, False si no se encontró o ya estaba activo
        """
        for escritorio in self.escritorios:
            if escritorio.id == id_escritorio and not escritorio.activo:
                escritorio.activar()
                self.escritorios_activos.agregar(escritorio)
                
                # Asignar un cliente en espera si hay disponible
                if not self.cola_clientes.esta_vacia() and escritorio.esta_disponible():
                    cliente = self.cola_clientes.desencolar()
                    escritorio.asignar_cliente(cliente)
                
                return True
        
        return False
    
    def desactivar_escritorio(self, id_escritorio):
        """
        Desactiva un escritorio para que no atienda más clientes.
        
        Args:
            id_escritorio (str): ID del escritorio a desactivar
            
        Returns:
            bool: True si se desactivó correctamente, False si no se encontró o ya estaba inactivo
        """
        for escritorio in self.escritorios_activos:
            if escritorio.id == id_escritorio and escritorio.activo:
                escritorio.desactivar()
                
                # Eliminar de la lista de activos (cuando termine con el cliente actual)
                if escritorio.cliente_actual is None:
                    self.escritorios_activos.eliminar(escritorio)
                
                return True
        
        return False
    
    def solicitar_atencion(self, cliente):
        """
        Registra un cliente que solicita atención.
        
        Args:
            cliente: Cliente que solicita atención
            
        Returns:
            tuple: (número_atención, tiempo_espera_estimado)
        """
        # Asignar a un escritorio disponible o poner en cola
        escritorio_disponible = None
        for escritorio in self.escritorios_activos:
            if escritorio.esta_disponible():
                escritorio_disponible = escritorio
                break
        
        if escritorio_disponible:
            escritorio_disponible.asignar_cliente(cliente)
            return (self.clientes_atendidos + self.cola_clientes.tamanio() + 1, 0)
        else:
            # Poner en cola
            self.cola_clientes.encolar(cliente)
            
            # Estimar tiempo de espera basado en clientes actuales y sus tiempos restantes
            tiempo_espera = self.estimar_tiempo_espera()
            
            return (self.clientes_atendidos + self.cola_clientes.tamanio(), tiempo_espera)
    
    def estimar_tiempo_espera(self):
        """
        Estima el tiempo de espera para un nuevo cliente.
        
        Returns:
            int: Tiempo estimado de espera en minutos
        """
        if self.escritorios_activos.esta_vacia():
            return 0
        
        # Calcular el tiempo restante para cada escritorio activo
        tiempos_restantes = []
        for escritorio in self.escritorios_activos:
            if escritorio.cliente_actual:
                tiempos_restantes.append(escritorio.tiempo_restante)
            else:
                tiempos_restantes.append(0)
        
        # Calcular tiempos totales para cada escritorio, distribuyendo clientes en cola
        tiempos_totales = tiempos_restantes.copy()
        clientes_en_cola = list(self.cola_clientes.lista)
        
        if clientes_en_cola:
            # Organizar escritorios por tiempo restante (menor a mayor)
            indices_ordenados = sorted(range(len(tiempos_totales)), key=lambda i: tiempos_totales[i])
            
            # Distribuir clientes en cola a los escritorios
            for cliente in clientes_en_cola:
                # Asignar al escritorio con menor tiempo total
                indice_menor = indices_ordenados[0]
                tiempos_totales[indice_menor] += cliente.calcular_tiempo_total_atencion()
                
                # Reorganizar índices
                indices_ordenados.sort(key=lambda i: tiempos_totales[i])
        
        # El tiempo de espera es el tiempo total del último cliente en ser atendido
        if tiempos_totales:
            return max(tiempos_totales)
        
        return 0
    
    def atender_cliente(self):
        """
        Finaliza la atención del próximo cliente que termine su tiempo.
        
        Returns:
            tuple: (cliente_atendido, escritorio) o (None, None) si no hay clientes siendo atendidos
        """
        # Encontrar el escritorio con menor tiempo restante
        escritorio_min = None
        tiempo_min = float('inf')
        
        for escritorio in self.escritorios_activos:
            if escritorio.cliente_actual and 0 < escritorio.tiempo_restante < tiempo_min:
                escritorio_min = escritorio
                tiempo_min = escritorio.tiempo_restante
        
        if escritorio_min is None:
            return None, None
        
        # Avanzar el tiempo para todos los escritorios
        for escritorio in self.escritorios_activos:
            if escritorio.cliente_actual:
                escritorio.atender_tiempo(tiempo_min)
        
        # Finalizar la atención del cliente con tiempo mínimo
        cliente_atendido = escritorio_min.finalizar_atencion()
        
        if cliente_atendido:
            # Actualizar estadísticas
            self.clientes_atendidos += 1
            self.tiempos_espera.agregar(cliente_atendido.tiempo_espera / 60)  # Convertir a minutos
            self.tiempos_atencion.agregar(
                (cliente_atendido.hora_finalizacion - cliente_atendido.hora_atencion) / 60
            )
            
            # Si el escritorio sigue activo, asignarle el siguiente cliente
            if escritorio_min.activo and not self.cola_clientes.esta_vacia():
                proximo_cliente = self.cola_clientes.desencolar()
                escritorio_min.asignar_cliente(proximo_cliente)
            elif not escritorio_min.activo:
                # Eliminar de la lista de activos si está marcado como inactivo
                self.escritorios_activos.eliminar(escritorio_min)
        
        return cliente_atendido, escritorio_min
    
    def simular_atencion_completa(self):
        """
        Simula la atención de todos los clientes en cola.
        
        Returns:
            dict: Estadísticas de la simulación
        """
        clientes_atendidos_inicial = self.clientes_atendidos
        
        # Mientras haya clientes en la cola o siendo atendidos
        while not self.cola_clientes.esta_vacia() or any(e.cliente_actual for e in self.escritorios_activos):
            self.atender_cliente()
        
        # Reunir estadísticas
        nuevos_atendidos = self.clientes_atendidos - clientes_atendidos_inicial
        
        estadisticas = {
            "escritorios_activos": len(self.escritorios_activos),
            "escritorios_inactivos": len(self.escritorios) - len(self.escritorios_activos),
            "clientes_atendidos": nuevos_atendidos,
            "tiempo_promedio_espera": self.tiempo_promedio_espera(),
            "tiempo_maximo_espera": self.tiempo_maximo_espera(),
            "tiempo_minimo_espera": self.tiempo_minimo_espera(),
            "tiempo_promedio_atencion": self.tiempo_promedio_atencion(),
            "tiempo_maximo_atencion": self.tiempo_maximo_atencion(),
            "tiempo_minimo_atencion": self.tiempo_minimo_atencion(),
            "estadisticas_escritorios": []
        }
        
        # Estadísticas por escritorio
        for escritorio in self.escritorios:
            estadisticas_escritorio = {
                "id": escritorio.id,
                "identificacion": escritorio.identificacion,
                "clientes_atendidos": escritorio.clientes_atendidos,
                "tiempo_promedio_atencion": escritorio.tiempo_promedio_atencion(),
                "tiempo_maximo_atencion": escritorio.tiempo_maximo_atencion(),
                "tiempo_minimo_atencion": escritorio.tiempo_minimo_atencion()
            }
            estadisticas["estadisticas_escritorios"].append(estadisticas_escritorio)
        
        return estadisticas
    
    def tiempo_promedio_espera(self):
        """
        Calcula el tiempo promedio de espera.
        
        Returns:
            float: Tiempo promedio de espera en minutos o 0 si no hay datos
        """
        if len(self.tiempos_espera) == 0:
            return 0
        
        total = 0
        for tiempo in self.tiempos_espera:
            total += tiempo
        
        return total / len(self.tiempos_espera)
    
    def tiempo_maximo_espera(self):
        """
        Obtiene el tiempo máximo de espera.
        
        Returns:
            float: Tiempo máximo de espera en minutos o 0 si no hay datos
        """
        if len(self.tiempos_espera) == 0:
            return 0
        
        maximo = 0
        for tiempo in self.tiempos_espera:
            if tiempo > maximo:
                maximo = tiempo
        
        return maximo
    
    def tiempo_minimo_espera(self):
        """
        Obtiene el tiempo mínimo de espera.
        
        Returns:
            float: Tiempo mínimo de espera en minutos o 0 si no hay datos
        """
        if len(self.tiempos_espera) == 0:
            return 0
        
        if len(self.tiempos_espera) == 1:
            return self.tiempos_espera.obtener(0)
        
        minimo = float('inf')
        for tiempo in self.tiempos_espera:
            if tiempo < minimo:
                minimo = tiempo
        
        return minimo
    
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
    
    def obtener_estado(self):
        """
        Obtiene el estado actual del punto de atención.
        
        Returns:
            dict: Estado actual del punto de atención
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "escritorios_activos": len(self.escritorios_activos),
            "escritorios_inactivos": len(self.escritorios) - len(self.escritorios_activos),
            "clientes_espera": self.cola_clientes.tamanio(),
            "tiempo_promedio_espera": self.tiempo_promedio_espera(),
            "tiempo_maximo_espera": self.tiempo_maximo_espera(),
            "tiempo_minimo_espera": self.tiempo_minimo_espera(),
            "tiempo_promedio_atencion": self.tiempo_promedio_atencion(),
            "tiempo_maximo_atencion": self.tiempo_maximo_atencion(),
            "tiempo_minimo_atencion": self.tiempo_minimo_atencion(),
            "escritorios": [
                {
                    "id": escritorio.id,
                    "identificacion": escritorio.identificacion,
                    "encargado": escritorio.encargado,
                    "activo": escritorio.activo,
                    "cliente_actual": str(escritorio.cliente_actual) if escritorio.cliente_actual else None,
                    "tiempo_restante": escritorio.tiempo_restante,
                    "tiempo_promedio_atencion": escritorio.tiempo_promedio_atencion(),
                    "tiempo_maximo_atencion": escritorio.tiempo_maximo_atencion(),
                    "tiempo_minimo_atencion": escritorio.tiempo_minimo_atencion()
                } 
                for escritorio in self.escritorios
            ]
        }
    
    def __str__(self):
        """
        Representación en cadena del punto de atención.
        
        Returns:
            str: Representación del punto de atención
        """
        return f"Punto de Atención: {self.nombre} (ID: {self.id}) - Dirección: {self.direccion}"
    
    def __eq__(self, other):
        """
        Compara si dos puntos de atención son iguales basándose en su ID.
        
        Args:
            other: Otro punto de atención para comparar
            
        Returns:
            bool: True si son iguales, False de lo contrario
        """
        if not isinstance(other, PuntoAtencion):
            return False
        return self.id == other.id