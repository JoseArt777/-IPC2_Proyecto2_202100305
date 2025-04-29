import xml.etree.ElementTree as ET
from modelo import Empresa, PuntoAtencion, EscritorioServicio, Transaccion, Cliente

class ProcesadorXML:
    def __init__(self, sistema):
        self.sistema = sistema
    
    def cargar_configuracion(self, ruta_archivo):
        """
        Carga el archivo de configuración del sistema.
        """
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            if root.tag != 'listaEmpresas':
                raise ValueError("Formato de archivo XML incorrecto. Se esperaba 'listaEmpresas' como elemento raíz.")
            
            for empresa_elem in root.findall('empresa'):
                id_empresa = empresa_elem.get('id')
                nombre = empresa_elem.find('nombre').text.strip()
                abreviatura = empresa_elem.find('abreviatura').text.strip()
                
                # crea una empresa
                empresa = Empresa(id_empresa, nombre, abreviatura)
                
                puntos_atencion_elem = empresa_elem.find('listaPuntosAtencion')
                if puntos_atencion_elem is not None:
                    for punto_elem in puntos_atencion_elem.findall('puntoAtencion'):
                        id_punto = punto_elem.get('id')
                        nombre_punto = punto_elem.find('nombre').text.strip()
                        direccion = punto_elem.find('direccion').text.strip()
                        
                        # Crea punto de atención
                        punto = PuntoAtencion(id_punto, nombre_punto, direccion)
                        
                        escritorios_elem = punto_elem.find('listaEscritorios')
                        if escritorios_elem is not None:
                            for escritorio_elem in escritorios_elem.findall('escritorio'):
                                id_escritorio = escritorio_elem.get('id')
                                identificacion = escritorio_elem.find('identificacion').text.strip()
                                encargado = escritorio_elem.find('encargado').text.strip()
                                
                                # Crea escritorio
                                escritorio = EscritorioServicio(id_escritorio, identificacion, encargado)
                                punto.agregar_escritorio(escritorio)
                        
                        empresa.agregar_punto_atencion(punto)
                
                transacciones_elem = empresa_elem.find('listaTransacciones')
                if transacciones_elem is not None:
                    for transaccion_elem in transacciones_elem.findall('transaccion'):
                        id_transaccion = transaccion_elem.get('id')
                        nombre_transaccion = transaccion_elem.find('nombre').text.strip()
                        tiempo_atencion = int(transaccion_elem.find('tiempoAtencion').text)
                        
                        # Crea transacción
                        transaccion = Transaccion(id_transaccion, nombre_transaccion, tiempo_atencion)
                        empresa.agregar_transaccion(transaccion)
                
                # Agregamos empresa al sistema
                self.sistema.agregar_empresa(empresa)
            
            return True, f"Archivo de configuración cargado correctamente. Se agregaron {len(root.findall('empresa'))} empresas."
        
        except Exception as e:
            return False, f"Error al cargar el archivo de configuración: {str(e)}"
    
    def cargar_configuracion_inicial(self, ruta_archivo):
        """
        Carga el archivo de configuración inicial para la prueba del sistema.
        """
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            if root.tag != 'listadoInicial':
                raise ValueError("Formato de archivo XML incorrecto. Se esperaba 'listadoInicial' como elemento raíz.")
            
            configuraciones_cargadas = 0
            
            for config_elem in root.findall('configInicial'):
                id_config = config_elem.get('id')
                id_empresa = config_elem.get('idEmpresa')
                id_punto = config_elem.get('idPunto')
                
                empresa = self.sistema.obtener_empresa(id_empresa)
                if empresa is None:
                    continue
                
                punto = empresa.obtener_punto_atencion(id_punto)
                if punto is None:
                    continue
                
                # Activar escritorios
                escritorios_elem = config_elem.find('escritoriosActivos')
                if escritorios_elem is not None:
                    for escritorio_elem in escritorios_elem.findall('escritorio'):
                        id_escritorio = escritorio_elem.get('idEscritorio')
                        punto.activar_escritorio(id_escritorio)
                
                # Cargar clientes
                clientes_elem = config_elem.find('listadoClientes')
                if clientes_elem is not None:
                    for cliente_elem in clientes_elem.findall('cliente'):
                        dpi = cliente_elem.get('dpi')
                        nombre = cliente_elem.find('nombre').text.strip()
                        prioridad = cliente_elem.get('prioridad', 'no')  # <- Nuevo
                        
                        cliente = Cliente(dpi, nombre, prioridad)
                        
                        transacciones_elem = cliente_elem.find('listadoTransacciones')
                        if transacciones_elem is not None:
                            for trans_elem in transacciones_elem.findall('transaccion'):
                                id_transaccion = trans_elem.get('idTransaccion')
                                cantidad = int(trans_elem.get('cantidad', 1))
                                
                                transaccion = empresa.obtener_transaccion(id_transaccion)
                                if transaccion:
                                    cliente.agregar_transaccion(transaccion, cantidad)
                        
                        punto.encolar_cliente(cliente)
                
                configuraciones_cargadas += 1
            
            for empresa in self.sistema.empresas.valores():
                for punto in empresa.puntos_atencion:
                    punto.asignar_clientes()
            
            return True, f"Configuración inicial cargada correctamente. Se procesaron {configuraciones_cargadas} configuraciones."

        except Exception as e:
            return False, f"Error al cargar la configuración inicial: {str(e)}"
