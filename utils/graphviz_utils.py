import os
import subprocess

class GraphvizUtils:
    """
    Utilidades para generar gráficos con Graphviz.
    """
    
    @staticmethod
    def generar_grafico_cola_clientes(punto_atencion, ruta_salida):
        """
        Genera un gráfico de la cola de clientes en espera.
        
        Args:
            punto_atencion: Punto de atención con la cola de clientes
            ruta_salida (str): Ruta donde guardar el archivo de imagen
            
        Returns:
            bool: True si se generó correctamente, False de lo contrario
        """
        try:
            # Crear archivo DOT
            dot_path = ruta_salida.replace('.png', '.dot')
            with open(dot_path, 'w') as dot_file:
                dot_file.write('digraph ColaClientes {\n')
                dot_file.write('  rankdir=LR;\n')
                dot_file.write('  node [shape=record, style=filled, fillcolor=lightblue];\n')
                
                # Si la cola está vacía, mostrar un nodo vacío
                if punto_atencion.cola_clientes.esta_vacia():
                    dot_file.write('  cola [label="Cola vacía"];\n')
                else:
                    # Mostrar cabecera de la cola
                    dot_file.write('  cabecera [shape=plaintext, label="Cabecera"];\n')
                    
                    # Crear nodos para cada cliente en la cola
                    index = 0
                    clientes = list(punto_atencion.cola_clientes)
                    for cliente in clientes:
                        client_id = f'cliente_{index}'
                        label = f'{{{cliente.nombre}|DPI: {cliente.dpi}|Transacciones: {len(cliente.transacciones)}}}'
                        dot_file.write(f'  {client_id} [label="{label}"];\n')
                        index += 1
                    
                    # Conectar los nodos
                    dot_file.write('  cabecera -> cliente_0;\n')
                    for i in range(len(clientes) - 1):
                        dot_file.write(f'  cliente_{i} -> cliente_{i+1};\n')
                
                dot_file.write('  label="Cola de Clientes en Espera";\n')
                dot_file.write('}\n')
            
            # Generar imagen con Graphviz (requiere tener instalado Graphviz)
            subprocess.run(['dot', '-Tpng', dot_path, '-o', ruta_salida])
            
            # Opcionalmente, eliminar el archivo .dot
            os.remove(dot_path)
            
            return True
        
        except Exception as e:
            print(f"Error al generar gráfico de cola: {str(e)}")
            return False
    
    @staticmethod
    def generar_grafico_escritorios(punto_atencion, ruta_salida):
        """
        Genera un gráfico de los escritorios de servicio y su estado.
        
        Args:
            punto_atencion: Punto de atención con los escritorios
            ruta_salida (str): Ruta donde guardar el archivo de imagen
            
        Returns:
            bool: True si se generó correctamente, False de lo contrario
        """
        try:
            # Crear archivo DOT
            dot_path = ruta_salida.replace('.png', '.dot')
            with open(dot_path, 'w') as dot_file:
                dot_file.write('digraph Escritorios {\n')
                dot_file.write('  rankdir=TB;\n')
                dot_file.write('  node [shape=record, style=filled];\n')
                
                # Si no hay escritorios, mostrar un nodo vacío
                if len(punto_atencion.escritorios) == 0:
                    dot_file.write('  escritorios [label="No hay escritorios"];\n')
                else:
                    # Crear nodos para cada escritorio
                    for i, escritorio in enumerate(punto_atencion.escritorios):
                        color = "lightgreen" if escritorio.activo else "lightgrey"
                        estado = "Activo" if escritorio.activo else "Inactivo"
                        
                        # Información del cliente actual si existe
                        cliente_info = "Sin cliente"
                        if escritorio.cliente_actual:
                            cliente_info = f"{escritorio.cliente_actual.nombre}\\nDPI: {escritorio.cliente_actual.dpi}\\nTiempo restante: {escritorio.tiempo_restante} min"
                        
                        label = f'{{{escritorio.identificacion}|Encargado: {escritorio.encargado}|Estado: {estado}|{cliente_info}}}'
                        dot_file.write(f'  escritorio_{i} [label="{label}", fillcolor="{color}"];\n')
                    
                    # Si hay escritorios activos, resaltar el orden de desactivación
                    if not punto_atencion.escritorios_activos.esta_vacia():
                        dot_file.write('  subgraph cluster_activos {\n')
                        dot_file.write('    label="Orden de Desactivación";\n')
                        dot_file.write('    style=dashed;\n')
                        
                        # Conectar escritorios activos según el orden de activación (LIFO)
                        active_desk_ids = []
                        for i, escritorio in enumerate(punto_atencion.escritorios):
                            if escritorio.activo:
                                active_desk_ids.append(f'escritorio_{i}')
                        
                        for i in range(len(active_desk_ids) - 1):
                            dot_file.write(f'    {active_desk_ids[i]} -> {active_desk_ids[i+1]} [style=dashed, color=blue, label="Después de"];\n')
                        
                        dot_file.write('  }\n')
                
                dot_file.write('  label="Escritorios de Servicio";\n')
                dot_file.write('}\n')
            
            # Generar imagen con Graphviz
            subprocess.run(['dot', '-Tpng', dot_path, '-o', ruta_salida])
            
            # Opcionalmente, eliminar el archivo .dot
            os.remove(dot_path)
            
            return True
        
        except Exception as e:
            print(f"Error al generar gráfico de escritorios: {str(e)}")
            return False
    
    @staticmethod
    def generar_grafico_simulacion(estadisticas, ruta_salida):
        """
        Genera un gráfico con el resumen de la simulación.
        
        Args:
            estadisticas: Diccionario con las estadísticas de la simulación
            ruta_salida (str): Ruta donde guardar el archivo de imagen
            
        Returns:
            bool: True si se generó correctamente, False de lo contrario
        """
        try:
            # Crear archivo DOT
            dot_path = ruta_salida.replace('.png', '.dot')
            with open(dot_path, 'w') as dot_file:
                dot_file.write('digraph Simulacion {\n')
                dot_file.write('  rankdir=TB;\n')
                dot_file.write('  node [shape=box, style=filled, fillcolor=lightyellow];\n')
                
                # Nodo principal con resumen del punto
                punto_label = (
                    f'Punto de Atención\\n'
                    f'Escritorios Activos: {estadisticas["escritorios_activos"]}\\n'
                    f'Escritorios Inactivos: {estadisticas["escritorios_inactivos"]}\\n'
                    f'Clientes Atendidos: {estadisticas["clientes_atendidos"]}\\n'
                    f'Tiempo Promedio Espera: {estadisticas["tiempo_promedio_espera"]:.2f} min\\n'
                    f'Tiempo Máximo Espera: {estadisticas["tiempo_maximo_espera"]:.2f} min\\n'
                    f'Tiempo Mínimo Espera: {estadisticas["tiempo_minimo_espera"]:.2f} min\\n'
                    f'Tiempo Promedio Atención: {estadisticas["tiempo_promedio_atencion"]:.2f} min\\n'
                    f'Tiempo Máximo Atención: {estadisticas["tiempo_maximo_atencion"]:.2f} min\\n'
                    f'Tiempo Mínimo Atención: {estadisticas["tiempo_minimo_atencion"]:.2f} min'
                )
                dot_file.write(f'  punto [label="{punto_label}", fillcolor=lightblue];\n')
                
                # Nodos para cada escritorio
                for i, escritorio in enumerate(estadisticas["estadisticas_escritorios"]):
                    desk_label = (
                        f'Escritorio {escritorio["identificacion"]}\\n'
                        f'Clientes Atendidos: {escritorio["clientes_atendidos"]}\\n'
                        f'Tiempo Promedio: {escritorio["tiempo_promedio_atencion"]:.2f} min\\n'
                        f'Tiempo Máximo: {escritorio["tiempo_maximo_atencion"]:.2f} min\\n'
                        f'Tiempo Mínimo: {escritorio["tiempo_minimo_atencion"]:.2f} min'
                    )
                    dot_file.write(f'  escritorio_{i} [label="{desk_label}", fillcolor=lightgreen];\n')
                    
                    # Conectar con el punto de atención
                    dot_file.write(f'  punto -> escritorio_{i};\n')
                
                dot_file.write('  label="Resultado de Simulación";\n')
                dot_file.write('}\n')
            
            # Generar imagen con Graphviz
            subprocess.run(['dot', '-Tpng', dot_path, '-o', ruta_salida])
            
            # Opcionalmente, eliminar el archivo .dot
            os.remove(dot_path)
            
            return True
        
        except Exception as e:
            print(f"Error al generar gráfico de simulación: {str(e)}")
            return False