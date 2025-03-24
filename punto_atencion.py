from cola import Cola
from lista import Lista
from pila import Pila

class PuntoAtencion:
    def __init__(self, id, nombre, direccion):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = Lista()  # Lista de todos los escritorios
        self.escritorios_activos = Pila()  # Pila de escritorios activos (LIFO)
        self.escritorios_inactivos = Lista()  # Lista de escritorios inactivos
        self.clientes_espera = Cola()  # Cola de clientes en espera (FIFO)
        self.clientes_atendidos = Lista()  # Lista de clientes ya atendidos
        
        # Tiempo global de la simulación
        self.tiempo_actual = 0
        
        # Estadísticas
        self.tiempo_promedio_espera = 0
        self.tiempo_maximo_espera = 0
        self.tiempo_minimo_espera = float('inf')
        self.tiempo_promedio_atencion = 0
        self.tiempo_maximo_atencion = 0
        self.tiempo_minimo_atencion = float('inf')
    
    def agregar_escritorio(self, escritorio):
        # Agregar escritorio a la lista
        self.escritorios.insertar(escritorio)
        self.escritorios_inactivos.insertar(escritorio)
    
    def activar_escritorio(self, id_escritorio):
        # Activar un escritorio y asignarle cliente si hay en espera
        escritorio = self.escritorios.buscar(lambda e: e.id == id_escritorio)
        if escritorio and not escritorio.activo:
            escritorio.activar()
            # Remover de inactivos
            self.escritorios_inactivos.eliminar(escritorio)
            # Agregar a activos (LIFO - último en activarse, primero en ser desactivado)
            self.escritorios_activos.apilar(escritorio)
            
            # Asignar cliente si hay en espera
            if not self.clientes_espera.esta_vacia():
                cliente = self.clientes_espera.desencolar()
                escritorio.asignar_cliente(cliente, self.tiempo_actual)
            
            return True
        return False
    
    def desactivar_escritorio(self, id_escritorio):
        # Desactivar un escritorio
        # Buscar en la pila de activos
        escritorios_activos = self.escritorios_activos.recorrer()
        for escritorio in escritorios_activos:
            if escritorio.id == id_escritorio:
                escritorio.desactivar()
                # No removemos de la pila, solo cuando termine su cliente actual
                # pasará a inactivos
                return True
        return False
    
    def solicitar_atencion(self, cliente):
        # Agregar cliente a la cola de espera o asignarle un escritorio disponible
        cliente.hora_llegada = self.tiempo_actual
        
        # Buscar un escritorio disponible (activo y sin cliente)
        escritorio_disponible = None
        escritorios_activos = self.escritorios_activos.recorrer()
        
        for escritorio in escritorios_activos:
            if escritorio.activo and escritorio.cliente_actual is None:
                escritorio_disponible = escritorio
                break
        
        # Si hay escritorio disponible, asignar cliente directamente
        if escritorio_disponible:
            escritorio_disponible.asignar_cliente(cliente, self.tiempo_actual)
            return 0  # Tiempo de espera es cero
        else:
            # Si no hay escritorio disponible, ponerlo en la cola
            self.clientes_espera.encolar(cliente)
            
            # Calcular tiempo estimado de espera
            tiempo_espera = self._calcular_tiempo_espera_estimado()
            return tiempo_espera
    
    def _calcular_tiempo_espera_estimado(self):
        # Calcular tiempo estimado de espera para el último cliente en la cola
        if self.clientes_espera.esta_vacia():
            return 0
        
        # Sumar tiempos restantes de escritorios activos
        tiempo_total = 0
        clientes_en_espera = self.clientes_espera.tamano() - 1  # Restar el último cliente
        
        # Contar escritorios activos con cliente
        escritorios_ocupados = []
        escritorios_activos = self.escritorios_activos.recorrer()
        
        for escritorio in escritorios_activos:
            if escritorio.activo and escritorio.cliente_actual is not None:
                escritorios_ocupados.append(escritorio)
                tiempo_total += escritorio.tiempo_restante
        
        num_escritorios = len(escritorios_ocupados)
        if num_escritorios == 0:
            return 0
        
        # Distribuir clientes en espera entre escritorios activos
        tiempo_estimado = tiempo_total / num_escritorios
        
        # Agregar tiempo por clientes en espera
        if clientes_en_espera > 0:
            # Obtener promedio de tiempo de atención de clientes en espera
            tiempo_atencion_promedio = 0
            clientes = self.clientes_espera.recorrer()
            for i, cliente in enumerate(clientes):
                if i < clientes_en_espera:  # Solo contar los que están antes del último
                    tiempo_atencion_promedio += cliente.calcular_tiempo_atencion()
            
            if clientes_en_espera > 0:
                tiempo_atencion_promedio /= clientes_en_espera
                
            tiempo_estimado += (clientes_en_espera / num_escritorios) * tiempo_atencion_promedio
            
        return tiempo_estimado
    
    def atender_cliente(self, tiempo=1):
        # Simular atención de cliente por un tiempo determinado
        self.tiempo_actual += tiempo
        
        # Procesar escritorios activos
        escritorios_procesados = []
        escritorios_finalizados = []
        
        escritorios_activos = self.escritorios_activos.recorrer()
        for escritorio in escritorios_activos:
            if escritorio.activo and escritorio.cliente_actual is not None:
                tiempo_procesado = escritorio.atender_cliente(tiempo)
                if tiempo_procesado > 0:
                    escritorios_procesados.append(escritorio)
                
                # Verificar si terminó atención
                if escritorio.tiempo_restante <= 0:
                    cliente_atendido = escritorio.finalizar_atencion()
                    if cliente_atendido:
                        self.clientes_atendidos.insertar(cliente_atendido)
                        escritorios_finalizados.append(escritorio)
            
        # Reasignar clientes a escritorios que finalizaron
        for escritorio in escritorios_finalizados:
            if escritorio.activo:
                if not self.clientes_espera.esta_vacia():
                    cliente = self.clientes_espera.desencolar()
                    escritorio.asignar_cliente(cliente, self.tiempo_actual)
            else:
                # Si está marcado como inactivo, pasar a lista de inactivos
                self.escritorios_activos.lista.eliminar(escritorio)
                self.escritorios_inactivos.insertar(escritorio)
        
        return len(escritorios_procesados)
    
    def simular_actividad(self):
        # Simular la atención de todos los clientes en espera y en atención
        while not self.clientes_espera.esta_vacia() or self._hay_clientes_en_atencion():
            self.atender_cliente()
        
        # Calcular estadísticas finales
        self.calcular_estadisticas()
    
    def _hay_clientes_en_atencion(self):
        # Verificar si hay clientes siendo atendidos
        escritorios_activos = self.escritorios_activos.recorrer()
        for escritorio in escritorios_activos:
            if escritorio.activo and escritorio.cliente_actual is not None:
                return True
        return False
    
    def calcular_estadisticas(self):
        # Actualizar estadísticas del punto de atención
        clientes = self.clientes_atendidos.recorrer()
        total_clientes = len(clientes)
        
        if total_clientes > 0:
            # Estadísticas de tiempo de espera
            tiempo_espera_total = 0
            tiempo_espera_max = 0
            tiempo_espera_min = float('inf')
            
            # Estadísticas de tiempo de atención
            tiempo_atencion_total = 0
            tiempo_atencion_max = 0
            tiempo_atencion_min = float('inf')
            
            for cliente in clientes:
                # Tiempo de espera
                tiempo_espera = cliente.tiempo_espera
                tiempo_espera_total += tiempo_espera
                
                if tiempo_espera > tiempo_espera_max:
                    tiempo_espera_max = tiempo_espera
                if tiempo_espera < tiempo_espera_min:
                    tiempo_espera_min = tiempo_espera
                
                # Tiempo de atención
                tiempo_atencion = cliente.tiempo_atencion
                tiempo_atencion_total += tiempo_atencion
                
                if tiempo_atencion > tiempo_atencion_max:
                    tiempo_atencion_max = tiempo_atencion
                if tiempo_atencion < tiempo_atencion_min:
                    tiempo_atencion_min = tiempo_atencion
            
            # Actualizar estadísticas globales
            self.tiempo_promedio_espera = tiempo_espera_total / total_clientes
            self.tiempo_maximo_espera = tiempo_espera_max
            self.tiempo_minimo_espera = tiempo_espera_min if tiempo_espera_min != float('inf') else 0
            
            self.tiempo_promedio_atencion = tiempo_atencion_total / total_clientes
            self.tiempo_maximo_atencion = tiempo_atencion_max
            self.tiempo_minimo_atencion = tiempo_atencion_min if tiempo_atencion_min != float('inf') else 0
        else:
            # Sin clientes atendidos
            self.tiempo_promedio_espera = 0
            self.tiempo_maximo_espera = 0
            self.tiempo_minimo_espera = 0
            
            self.tiempo_promedio_atencion = 0
            self.tiempo_maximo_atencion = 0
            self.tiempo_minimo_atencion = 0
        
        # Calcular estadísticas para cada escritorio
        escritorios = self.escritorios.recorrer()
        for escritorio in escritorios:
            escritorio.calcular_estadisticas()
    
    def estado_actual(self):
        # Retornar información del estado actual
        self.calcular_estadisticas()
        
        # Contar escritorios activos e inactivos
        num_escritorios_activos = self.escritorios_activos.tamano()
        num_escritorios_inactivos = self.escritorios_inactivos.tamano()
        num_clientes_espera = self.clientes_espera.tamano()
        num_clientes_atendidos = self.clientes_atendidos.tamano()
        
        estado = {
            "punto_atencion": {
                "nombre": self.nombre,
                "escritorios_activos": num_escritorios_activos,
                "escritorios_inactivos": num_escritorios_inactivos,
                "clientes_espera": num_clientes_espera,
                "clientes_atendidos": num_clientes_atendidos,
                "tiempo_promedio_espera": self.tiempo_promedio_espera,
                "tiempo_maximo_espera": self.tiempo_maximo_espera,
                "tiempo_minimo_espera": self.tiempo_minimo_espera,
                "tiempo_promedio_atencion": self.tiempo_promedio_atencion,
                "tiempo_maximo_atencion": self.tiempo_maximo_atencion,
                "tiempo_minimo_atencion": self.tiempo_minimo_atencion
            },
            "escritorios_activos": []
        }
        
        # Agregar información de escritorios activos
        escritorios_activos = self.escritorios_activos.recorrer()
        for escritorio in escritorios_activos:
            estadisticas = escritorio.calcular_estadisticas()
            info_escritorio = {
                "id": escritorio.id,
                "identificacion": escritorio.identificacion,
                "encargado": escritorio.encargado,
                "cliente_actual": escritorio.cliente_actual.nombre if escritorio.cliente_actual else None,
                "tiempo_restante": escritorio.tiempo_restante,
                "clientes_atendidos": estadisticas["clientes_atendidos"],
                "tiempo_promedio": estadisticas["tiempo_promedio"],
                "tiempo_maximo": estadisticas["tiempo_maximo"],
                "tiempo_minimo": estadisticas["tiempo_minimo"]
            }
            estado["escritorios_activos"].append(info_escritorio)
        
        return estado