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
        Genera un diagrama de Graphviz para visualizar los escritorios de servicio,
        incluyendo tiempos de atención por escritorio.
        """
        if not self.punto_actual:
            return ""

        import graphviz
        dot = graphviz.Digraph(comment='Escritorios de Servicio')

        # Nodo principal del punto
        dot.node('punto', f'Punto de Atención: {self.punto_actual.nombre}', shape='box')

        # Nodos de escritorios
        for idx, escritorio in enumerate(self.punto_actual.escritorios):
            estado = "Inactivo"
            color = "lightgrey"
            cliente_info = ""
            tiempos_info = ""

            if escritorio.estado == escritorio.ACTIVO:
                estado = "Activo"
                color = "lightgreen"
            elif escritorio.estado == escritorio.OCUPADO:
                estado = "Ocupado"
                color = "orange"
                if escritorio.cliente_actual:
                    cliente_info = f"Cliente: {escritorio.cliente_actual.nombre}\\n"
                    tiempos_info += f"Tiempo restante: {escritorio.tiempo_restante} min\\n"

            if escritorio.clientes_atendidos > 0:
                tiempo_prom = escritorio.tiempo_promedio_atencion()
                tiempo_min = escritorio.tiempo_min_atencion if escritorio.tiempo_min_atencion != float('inf') else 0
                tiempo_max = escritorio.tiempo_max_atencion
                tiempos_info += f"Prom: {tiempo_prom:.1f} min\\nMin: {tiempo_min} min | Max: {tiempo_max} min"

            etiqueta = f"{escritorio.identificacion}\\nEstado: {estado}\\n{cliente_info}{tiempos_info}"
            dot.node(f'escritorio{idx}', etiqueta, style='filled', fillcolor=color)

            # Conexión desde el punto al escritorio
            dot.edge('punto', f'escritorio{idx}')

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
    def guardar_tablas_estadisticas(self, directorio="reportes"):
        """
        Genera tablas estadísticas con Graphviz que siguen exactamente el formato
        de las imágenes de referencia y las guarda como archivos de imagen en 
        el directorio especificado, sobrescribiendo archivos anteriores.
        
        Args:
            directorio (str): Directorio donde se guardarán las imágenes. Si no existe, se creará.
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        if not self.punto_actual:
            return False, "Debe seleccionar un punto de atención primero."
        
        import os
        
        # Crear directorio si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        try:
            # Generar tabla similar a la referencia exacta
            import graphviz
            
            # TABLA 1: Estado del punto de atención (Imagen 1 y 2)
            dot_estado = graphviz.Digraph(comment='Estado del Punto de Atención')
            dot_estado.attr(rankdir='TB')
            
            # Título principal con fondo celeste
            dot_estado.attr('node', shape='plaintext')
            header = f'''<
            <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4" WIDTH="100%">
                <TR>
                    <TD BGCOLOR="lightblue" ALIGN="CENTER"><FONT POINT-SIZE="14" FACE="Arial Bold">PUNTO DE ATENCION {self.punto_actual.id}</FONT></TD>
                </TR>
            </TABLE>
            >'''
            dot_estado.node('header', header)
            
            # Obtener estadísticas
            stats = self.punto_actual.obtener_estadisticas()
            
            # Crear tabla principal de estadísticas (formato exacto de las imágenes)
            main_table = f'''<
            <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">
                <TR>
                    <TD VALIGN="TOP">
                        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                            <TR>
                                <TD COLSPAN="2" ALIGN="CENTER">Escritorios</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">Activos</TD>
                                <TD ALIGN="CENTER">Inactivos</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">{stats['escritorios_activos']}</TD>
                                <TD ALIGN="CENTER">{stats['escritorios_inactivos']}</TD>
                            </TR>
                        </TABLE>
                    </TD>
                    <TD ALIGN="CENTER" WIDTH="50"></TD>
                    <TD VALIGN="TOP">
                        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                            <TR>
                                <TD COLSPAN="2" ALIGN="CENTER">Clientes</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">En espera</TD>
                                <TD ALIGN="CENTER">Atendidos</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">{stats['clientes_en_espera']}</TD>
                                <TD ALIGN="CENTER">{stats['clientes_atendidos']}</TD>
                            </TR>
                        </TABLE>
                    </TD>
                    <TD ALIGN="CENTER" WIDTH="50"></TD>
                    <TD VALIGN="TOP">
                        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                            <TR>
                                <TD COLSPAN="3" ALIGN="CENTER">Tiempo de Espera</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">Min</TD>
                                <TD ALIGN="CENTER">Prom</TD>
                                <TD ALIGN="CENTER">Máximo</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">{round(stats['tiempo_min_espera'])}</TD>
                                <TD ALIGN="CENTER">{round(stats['tiempo_promedio_espera'], 1)}</TD>
                                <TD ALIGN="CENTER">{round(stats['tiempo_max_espera'])}</TD>
                            </TR>
                        </TABLE>
                    </TD>
                    <TD ALIGN="CENTER" WIDTH="50"></TD>
                    <TD VALIGN="TOP">
                        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                            <TR>
                                <TD COLSPAN="3" ALIGN="CENTER">Tiempo de Atencion</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">Min</TD>
                                <TD ALIGN="CENTER">Prom</TD>
                                <TD ALIGN="CENTER">Max</TD>
                            </TR>
                            <TR>
                                <TD ALIGN="CENTER">{round(stats['tiempo_min_atencion'])}</TD>
                                <TD ALIGN="CENTER">{round(stats['tiempo_promedio_atencion'])}</TD>
                                <TD ALIGN="CENTER">{round(stats['tiempo_max_atencion'])}</TD>
                            </TR>
                        </TABLE>
                    </TD>
                </TR>
            </TABLE>
            >'''
            
            dot_estado.node('main_table', main_table)
            dot_estado.edge('header', 'main_table', style='invis')
            
            # Tablas para cada escritorio, como en las imágenes
            escritorios_table = f'''<
            <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20">
                <TR>'''
            
            # Añadir cada escritorio activo e inactivo
            for idx, escritorio in enumerate(self.punto_actual.escritorios):
                # Determinar color de fondo según si es par o impar
                bg_color = "#FFD6BA" if idx % 2 == 0 else "#F8C8DC"  # Salmón claro o rosa claro
                
                tiempo_prom = escritorio.tiempo_promedio_atencion() if escritorio.clientes_atendidos > 0 else 0
                tiempo_min = escritorio.tiempo_min_atencion if escritorio.tiempo_min_atencion != float('inf') else 0
                tiempo_max = escritorio.tiempo_max_atencion
                
                escritorios_table += f'''
                    <TD VALIGN="TOP">
                        <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">
                            <TR>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER" COLSPAN="4"><FONT POINT-SIZE="12" FACE="Arial Bold">{escritorio.identificacion}</FONT></TD>
                            </TR>
                            <TR>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER" COLSPAN="4">Tiempo de Atencion</TD>
                            </TR>
                            <TR>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">Min</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">Prom</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">Max</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">Atendidos</TD>
                            </TR>
                            <TR>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">{round(tiempo_min)}</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">{round(tiempo_prom)}</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">{round(tiempo_max)}</TD>
                                <TD BGCOLOR="{bg_color}" ALIGN="CENTER">{escritorio.clientes_atendidos}</TD>
                            </TR>
                        </TABLE>
                    </TD>'''
                
            escritorios_table += '''
                </TR>
            </TABLE>
            >'''
            
            dot_estado.node('escritorios_table', escritorios_table)
            dot_estado.edge('main_table', 'escritorios_table', style='invis')
            
            # Guardar archivo de imagen para Ver Estado (formato 1 y 2)
            filename_estado = f"{directorio}/estado_punto_atencion"
            dot_estado.render(filename_estado, format='png', cleanup=True)
            
            
            # TABLA 3: Simulación de actividad (formato de la imagen 3)
            dot_simulacion = graphviz.Digraph(comment='Simulación de Actividad')
            dot_simulacion.attr('node', shape='plaintext')
            
            # Título y empresa
            dot_simulacion.node('titulo', '<Simular Actividad del punto de Atención>', shape='box')
            empresa_nombre = self.empresa_actual.nombre if self.empresa_actual else "EMPRESA"
            dot_simulacion.node('empresa', f'<ID-NOMBRE EMPRESA<BR/>{empresa_nombre}>', shape='box')
            dot_simulacion.node('punto', f'<ID-Nombre Punto de Atención<BR/>{self.punto_actual.nombre}>', shape='box')
            
            # Crear tabla de estadísticas (formato de la imagen 3)
            tabla_info_sim = f'''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                <TR>
                    <TD COLSPAN="2" ALIGN="CENTER">Escritorios</TD>
                    <TD COLSPAN="2" ALIGN="CENTER">Clientes</TD>
                    <TD COLSPAN="3" ALIGN="CENTER">Tiempo de Espera</TD>
                    <TD COLSPAN="3" ALIGN="CENTER">Tiempo de Atencion</TD>
                </TR>
                <TR>
                    <TD ALIGN="CENTER">Activos/habilitados</TD>
                    <TD ALIGN="CENTER">En uso/ocupados</TD>
                    <TD ALIGN="CENTER">Atendidos</TD>
                    <TD ALIGN="CENTER">En espera</TD>
                    <TD ALIGN="CENTER">Mínimo</TD>
                    <TD ALIGN="CENTER">Promedio</TD>
                    <TD ALIGN="CENTER">Máximo</TD>
                    <TD ALIGN="CENTER">Promedio</TD>
                    <TD ALIGN="CENTER">Mínimo</TD>
                    <TD ALIGN="CENTER">Máximo</TD>
                </TR>
                <TR>
                    <TD ALIGN="CENTER">{stats['escritorios_activos']}</TD>
                    <TD ALIGN="CENTER">{sum(1 for e in self.punto_actual.escritorios if e.estado == e.OCUPADO)}</TD>
                    <TD ALIGN="CENTER">{stats['clientes_atendidos']}</TD>
                    <TD ALIGN="CENTER">{stats['clientes_en_espera']}</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_min_espera']:.2f} minutos</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_promedio_espera']:.2f} minutos</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_max_espera']:.2f} minutos</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_promedio_atencion']:.2f} minutos</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_min_atencion']:.2f} minutos</TD>
                    <TD ALIGN="CENTER">{stats['tiempo_max_atencion']:.2f} minutos</TD>
                </TR>
            </TABLE>
            >'''
            
            dot_simulacion.node('tabla_sim', tabla_info_sim)
            
            # Conexiones
            dot_simulacion.edge('titulo', 'empresa')
            dot_simulacion.edge('empresa', 'punto')
            dot_simulacion.edge('punto', 'tabla_sim')
            
            # Añadir escritorios con flechas verdes como en la imagen 3
            for i, escritorio in enumerate(self.punto_actual.escritorios):
                if escritorio.estado != escritorio.INACTIVO:
                    tiempo_prom = escritorio.tiempo_promedio_atencion() if escritorio.clientes_atendidos > 0 else 0
                    info = f'ID: {escritorio.id} | Caja {i+1} | Tiempo Promedio: {tiempo_prom:.2f} min | Tiempo Máximo: {escritorio.tiempo_max_atencion:.2f} | Tiempo Mínimo: {escritorio.tiempo_min_atencion if escritorio.tiempo_min_atencion != float("inf") else 0:.2f} | Clientes Atendidos: {escritorio.clientes_atendidos}'
                    
                    dot_simulacion.node(f'esc_{i}', f'<{info}>', shape='box', style='filled', fillcolor='lightgreen')
                    
                    if i == 0:
                        # Primera flecha verde curva desde la tabla a la primera caja
                        dot_simulacion.edge('tabla_sim', f'esc_{i}', color='green', penwidth='2.0')
                    else:
                        # Conectar cajas entre sí
                        dot_simulacion.edge(f'esc_{i-1}', f'esc_{i}', color='green', penwidth='2.0')
            
            # Guardar archivo de imagen para Simulación (formato 3)
            filename_simulacion = f"{directorio}/simulacion_punto_atencion"
            dot_simulacion.render(filename_simulacion, format='png', cleanup=True)
            
            return True, f"Tablas estadísticas generadas y guardadas en '{directorio}'."
        
        except Exception as e:
            return False, f"Error al generar tablas estadísticas: {str(e)}"