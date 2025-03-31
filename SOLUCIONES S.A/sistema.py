import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from estructuras import TablaHash
from modelo import Empresa
import graphviz

class SistemaAtencion:
    def __init__(self):
        self.empresas = TablaHash()
        self.empresa_actual = None
        self.punto_actual = None
    
    def limpiar_sistema(self):
        """
        Inicializa todas las estructuras de datos para iniciar una prueba desde cero.
        """
        self.empresas = TablaHash()
        self.empresa_actual = None
        self.punto_actual = None
        return True, "Sistema limpiado correctamente."
    
    def agregar_empresa(self, empresa):
        """
        Agrega una nueva empresa al sistema.
        """
        self.empresas.insertar(empresa.id, empresa)
        return True, f"Empresa '{empresa.nombre}' agregada correctamente."
    
    def crear_empresa(self, id_empresa, nombre, abreviatura):
        """
        Crea una nueva empresa y la agrega al sistema.
        """
        if self.empresas.obtener(id_empresa):
            return False, f"Ya existe una empresa con ID '{id_empresa}'."
        
        empresa = Empresa(id_empresa, nombre, abreviatura)
        self.empresas.insertar(id_empresa, empresa)
        return True, f"Empresa '{nombre}' creada correctamente."
    
    def obtener_empresa(self, id_empresa):
        """
        Obtiene una empresa por su ID.
        """
        return self.empresas.obtener(id_empresa)
    
    def seleccionar_empresa(self, id_empresa):
        """
        Selecciona una empresa como la empresa actual.
        """
        empresa = self.empresas.obtener(id_empresa)
        if empresa:
            self.empresa_actual = empresa
            self.punto_actual = None
            return True, f"Empresa '{empresa.nombre}' seleccionada."
        return False, f"No se encontró una empresa con ID '{id_empresa}'."
    
    def seleccionar_punto(self, id_punto):
        """
        Selecciona un punto de atención como el punto actual.
        """
        if not self.empresa_actual:
            return False, "Debe seleccionar una empresa primero."
        
        punto = self.empresa_actual.obtener_punto_atencion(id_punto)
        if punto:
            self.punto_actual = punto
            return True, f"Punto de atención '{punto.nombre}' seleccionado."
        return False, f"No se encontró un punto de atención con ID '{id_punto}'."
    
    def ver_estado_punto(self):
        """
        Muestra el estado actual del punto de atención seleccionado.
        """
        if not self.punto_actual:
            return False, "Debe seleccionar un punto de atención primero."
        
        stats = self.punto_actual.obtener_estadisticas()
        
        # Generar reporte Graphviz
        dot_escritorios = self.generar_dot_escritorios()
        dot_cola = self.generar_dot_cola()
        
        return True, {
            "estadisticas": stats,
            "dot_escritorios": dot_escritorios,
            "dot_cola": dot_cola
        }
    
    def activar_escritorio_auto(self):
        if not self.punto_actual:
            return False, "Selecciona un punto de atención primero."
        
        escritorio = self.punto_actual.activar_escritorio_auto()
        if escritorio:
            return True, f"Escritorio '{escritorio.identificacion}' activado automáticamente."
        return False, "No hay escritorios disponibles para activar."

    # En sistema.py
    def desactivar_escritorio_auto(self):
        if not self.punto_actual:
            return False, "Selecciona un punto de atención primero."
        
        escritorio = self.punto_actual.desactivar_escritorio_auto()
        if escritorio:
            return True, escritorio  # Devuelve el objeto escritorio
        return False, "No hay escritorios activos para desactivar."

    
    def atender_cliente(self):
        """
        Completa la atención del cliente que está más próximo a terminar.
        """
        if not self.punto_actual:
            return False, "Debe seleccionar un punto de atención primero."
        
        resultado = self.punto_actual.atender_cliente()
        if resultado:
            return True, "Cliente atendido correctamente."
        return False, "No hay clientes en atención actualmente."
    
    def solicitar_atencion(self, dpi, nombre, transacciones):
        """
        Agrega un cliente que solicita atención.
        transacciones = [(id_transaccion, cantidad), ...]
        """
        if not self.punto_actual or not self.empresa_actual:
            return False, "Debe seleccionar un punto de atención primero."
        
        # Crear cliente
        from modelo import Cliente
        cliente = Cliente(dpi, nombre)
        
        # Agregar transacciones
        tiempo_total = 0
        for id_transaccion, cantidad in transacciones:
            transaccion = self.empresa_actual.obtener_transaccion(id_transaccion)
            if transaccion:
                cliente.agregar_transaccion(transaccion, cantidad)
                tiempo_total += transaccion.tiempo_atencion * cantidad
        
        # Encolar cliente
        posicion = self.punto_actual.encolar_cliente(cliente)
        
        # Intentar asignar clientes
        self.punto_actual.asignar_clientes()
        
        # Estimar tiempo de espera (lógica simplificada)
        tiempo_espera = self.estimar_tiempo_espera(cliente)
        
        return True, {
            "posicion": posicion,
            "tiempo_espera": tiempo_espera,
            "tiempo_atencion": tiempo_total
        }
    
    def estimar_tiempo_espera(self, cliente):
        """
        Estima el tiempo de espera para un cliente según su posición en la cola.
        Esta es una implementación simplificada.
        """
        if not self.punto_actual:
            return 0
        
        # Contar escritorios activos
        escritorios_activos = 0
        for escritorio in self.punto_actual.escritorios:
            if escritorio.estado != escritorio.INACTIVO:
                escritorios_activos += 1
        
        if escritorios_activos == 0:
            return float('inf')  # No hay escritorios activos
        
        # Buscar la posición del cliente en la cola
        posicion = 0
        for i, cliente_cola in enumerate(self.punto_actual.cola_clientes):
            if cliente_cola == cliente:
                posicion = i
                break
        
        # Estimar tiempo basado en posición y escritorios activos
        # Esta es una estimación muy básica
        return posicion * 5  # 5 minutos por cliente en promedio
    
    def simular_actividad(self):
        """
        Simula la atención de todos los clientes pendientes.
        """
        if not self.punto_actual:
            return False, "Debe seleccionar un punto de atención primero."
        
        self.punto_actual.simular_actividad()
        stats = self.punto_actual.obtener_estadisticas()
        
        return True, stats
    
    def generar_dot_escritorios(self):
        """
        Genera un diagrama de Graphviz para visualizar los escritorios de servicio.
        """
        if not self.punto_actual:
            return ""
        
        dot = graphviz.Digraph(comment='Escritorios de Servicio')
        
        # Agregar nodo para el punto de atención
        dot.node('punto', f'Punto de Atención: {self.punto_actual.nombre}', shape='box')
        
        # Agregar nodos para los escritorios
        for escritorio in self.punto_actual.escritorios:
            estado = "Inactivo"
            color = "lightgrey"
            cliente_info = ""  # Inicializar cliente_info para todos los casos
            
            if escritorio.estado == escritorio.ACTIVO:
                estado = "Activo"
                color = "lightgreen"
            elif escritorio.estado == escritorio.OCUPADO:
                estado = "Ocupado"
                color = "orange"
                cliente_info = f"\\nCliente: {escritorio.cliente_actual.nombre}\\nTiempo restante: {escritorio.tiempo_restante} min"
            
            label = f"Escritorio: {escritorio.identificacion}\\nEncargado: {escritorio.encargado}\\nEstado: {estado}{cliente_info}"
            dot.node(f'escritorio_{escritorio.id}', label, shape='box', style='filled', fillcolor=color)
            dot.edge('punto', f'escritorio_{escritorio.id}')
        
        return dot.source
    
    def generar_dot_cola(self):
        """s
        Genera un diagrama de Graphviz para visualizar la cola de espera.
        """
        if not self.punto_actual:
            return ""
        
        dot = graphviz.Digraph(comment='Cola de Espera')
        
        # Agregar nodo para la cola
        dot.node('cola', f'Cola de Espera: {self.punto_actual.nombre}', shape='box')
        
        # Agregar nodos para los clientes en la cola
        nodo_anterior = 'cola'
        for i, cliente in enumerate(self.punto_actual.cola_clientes):
            transacciones_info = ""
            for trans, cantidad in cliente.transacciones:
                transacciones_info += f"\\n- {trans.nombre} x{cantidad} ({trans.tiempo_atencion * cantidad} min)"
            
            label = f"Cliente #{i+1}: {cliente.nombre}\\nDPI: {cliente.dpi}{transacciones_info}"
            dot.node(f'cliente_{i}', label, shape='box', style='filled', fillcolor='lightblue')
            dot.edge(nodo_anterior, f'cliente_{i}')
            nodo_anterior = f'cliente_{i}'
        
        return dot.source