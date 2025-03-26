import xml.etree.ElementTree as ET
from models.sistema import Sistema
from models.empresa import Empresa
from models.punto_atencion import PuntoAtencion
from models.escritorio import Escritorio
from models.transaccion import Transaccion
from models.cliente import Cliente

class XMLController:
    """
    Controlador para manejar la carga y procesamiento de archivos XML.
    """
    
    def __init__(self, sistema):
        """
        Inicializa el controlador.
        
        Args:
            sistema: Instancia del sistema de atención al cliente
        """
        self.sistema = sistema
    
    def cargar_configuracion(self, ruta_archivo):
        """
        Carga un archivo XML de configuración del sistema.
        
        Args:
            ruta_archivo (str): Ruta al archivo XML de configuración
            
        Returns:
            tuple: (bool, str) indicando éxito/fracaso y mensaje
        """
        try:
            # Parsear el archivo XML
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            # Verificar que la raíz sea 'listaEmpresas'
            if root.tag != 'listaEmpresas':
                return False, "El archivo XML no tiene el formato correcto. La raíz debe ser 'listaEmpresas'."
            
            # Procesar cada empresa
            for empresa_element in root.findall('empresa'):
                id_empresa = empresa_element.get('id')
                nombre = empresa_element.find('nombre').text.strip()
                abreviatura = empresa_element.find('abreviatura').text.strip()
                
                # Crear o obtener empresa
                empresa = self.sistema.obtener_empresa(id_empresa)
                if not empresa:
                    empresa = self.sistema.crear_empresa(id_empresa, nombre, abreviatura)
                
                # Procesar puntos de atención
                puntos_element = empresa_element.find('listaPuntosAtencion')
                if puntos_element is not None:
                    for punto_element in puntos_element.findall('puntoAtencion'):
                        id_punto = punto_element.get('id')
                        nombre_punto = punto_element.find('nombre').text.strip()
                        direccion = punto_element.find('direccion').text.strip()
                        
                        # Crear o obtener punto de atención
                        punto = empresa.obtener_punto_atencion(id_punto)
                        if not punto:
                            punto = self.sistema.crear_punto_atencion(id_empresa, id_punto, nombre_punto, direccion)
                        
                        # Procesar escritorios
                        escritorios_element = punto_element.find('listaEscritorios')
                        if escritorios_element is not None:
                            for escritorio_element in escritorios_element.findall('escritorio'):
                                id_escritorio = escritorio_element.get('id')
                                identificacion = escritorio_element.find('identificacion').text.strip()
                                encargado = escritorio_element.find('encargado').text.strip()
                                
                                # Crear escritorio
                                self.sistema.crear_escritorio(id_empresa, id_punto, id_escritorio, identificacion, encargado)
                
                # Procesar transacciones
                transacciones_element = empresa_element.find('listaTransacciones')
                if transacciones_element is not None:
                    for transaccion_element in transacciones_element.findall('transaccion'):
                        id_transaccion = transaccion_element.get('id')
                        nombre_trans = transaccion_element.find('nombre').text.strip()
                        tiempo_atencion = int(transaccion_element.find('tiempoAtencion').text.strip())
                        
                        # Crear transacción
                        self.sistema.crear_transaccion(id_empresa, id_transaccion, nombre_trans, tiempo_atencion)
            
            return True, "Archivo de configuración cargado correctamente."
            
        except ET.ParseError:
            return False, "Error al parsear el archivo XML. Verifique que el formato sea correcto."
        except Exception as e:
            return False, f"Error al cargar el archivo de configuración: {str(e)}"
    
    def cargar_configuracion_inicial(self, ruta_archivo):
        """
        Carga un archivo XML de configuración inicial para la prueba.
        
        Args:
            ruta_archivo (str): Ruta al archivo XML de configuración inicial
            
        Returns:
            tuple: (bool, str) indicando éxito/fracaso y mensaje
        """
        try:
            # Parsear el archivo XML
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            # Verificar que la raíz sea 'listadoInicial'
            if root.tag != 'listadoInicial':
                return False, "El archivo XML no tiene el formato correcto. La raíz debe ser 'listadoInicial'."
            
            # Procesar cada configuración inicial
            for config_element in root.findall('configInicial'):
                id_config = config_element.get('id')
                id_empresa = config_element.get('idEmpresa')
                id_punto = config_element.get('idPunto')
                
                # Verificar que existan la empresa y el punto
                empresa = self.sistema.obtener_empresa(id_empresa)
                if not empresa:
                    return False, f"No existe la empresa con ID '{id_empresa}'."
                
                punto = empresa.obtener_punto_atencion(id_punto)
                if not punto:
                    return False, f"No existe el punto de atención con ID '{id_punto}' en la empresa '{id_empresa}'."
                
                # Activar escritorios
                escritorios_element = config_element.find('escritoriosActivos')
                if escritorios_element is not None:
                    for escritorio_element in escritorios_element.findall('escritorio'):
                        id_escritorio = escritorio_element.get('idEscritorio')
                        
                        # Activar escritorio en el punto de atención
                        for escritorio in punto.escritorios:
                            if escritorio.id == id_escritorio:
                                punto.activar_escritorio(id_escritorio)
                                break
                
                # Procesar clientes
                clientes_element = config_element.find('listadoClientes')
                if clientes_element is not None:
                    for cliente_element in clientes_element.findall('cliente'):
                        dpi = cliente_element.get('dpi')
                        nombre_cliente = cliente_element.find('nombre').text.strip()
                        
                        # Crear cliente
                        cliente = Cliente(dpi, nombre_cliente)
                        
                        # Procesar transacciones del cliente
                        trans_element = cliente_element.find('listadoTransacciones')
                        if trans_element is not None:
                            for trans_cliente_element in trans_element.findall('transaccion'):
                                id_trans = trans_cliente_element.get('idTransaccion')
                                cantidad = int(trans_cliente_element.get('cantidad'))
                                
                                # Buscar la transacción en la empresa
                                transaccion = empresa.obtener_transaccion(id_trans)
                                if transaccion:
                                    cliente.agregar_transaccion(transaccion, cantidad)
                        
                        # Solicitar atención para el cliente
                        self.sistema.seleccionar_empresa(id_empresa)
                        self.sistema.seleccionar_punto_atencion(id_punto)
                        self.sistema.solicitar_atencion(cliente)
            
            return True, "Archivo de configuración inicial cargado correctamente."
            
        except ET.ParseError:
            return False, "Error al parsear el archivo XML. Verifique que el formato sea correcto."
        except Exception as e:
            return False, f"Error al cargar el archivo de configuración inicial: {str(e)}"
    
    def generar_xml_estado(self, ruta_archivo):
        """
        Genera un archivo XML con el estado actual del sistema.
        
        Args:
            ruta_archivo (str): Ruta donde guardar el archivo XML
            
        Returns:
            tuple: (bool, str) indicando éxito/fracaso y mensaje
        """
        try:
            # Crear elemento raíz
            root = ET.Element('estadoSistema')
            
            # Agregar información de empresas
            empresas_element = ET.SubElement(root, 'empresas')
            for empresa in self.sistema.empresas:
                empresa_element = ET.SubElement(empresas_element, 'empresa', {'id': empresa.id})
                ET.SubElement(empresa_element, 'nombre').text = empresa.nombre
                ET.SubElement(empresa_element, 'abreviatura').text = empresa.abreviatura
                
                # Agregar puntos de atención
                puntos_element = ET.SubElement(empresa_element, 'puntosAtencion')
                for punto in empresa.puntos_atencion:
                    punto_element = ET.SubElement(puntos_element, 'puntoAtencion', {'id': punto.id})
                    ET.SubElement(punto_element, 'nombre').text = punto.nombre
                    ET.SubElement(punto_element, 'direccion').text = punto.direccion
                    
                    # Agregar estadísticas del punto
                    estado = punto.obtener_estado()
                    stats_element = ET.SubElement(punto_element, 'estadisticas')
                    ET.SubElement(stats_element, 'escritoriosActivos').text = str(estado['escritorios_activos'])
                    ET.SubElement(stats_element, 'escritoriosInactivos').text = str(estado['escritorios_inactivos'])
                    ET.SubElement(stats_element, 'clientesEspera').text = str(estado['clientes_espera'])
                    ET.SubElement(stats_element, 'tiempoPromedioEspera').text = str(estado['tiempo_promedio_espera'])
                    ET.SubElement(stats_element, 'tiempoMaximoEspera').text = str(estado['tiempo_maximo_espera'])
                    ET.SubElement(stats_element, 'tiempoMinimoEspera').text = str(estado['tiempo_minimo_espera'])
                    ET.SubElement(stats_element, 'tiempoPromedioAtencion').text = str(estado['tiempo_promedio_atencion'])
                    ET.SubElement(stats_element, 'tiempoMaximoAtencion').text = str(estado['tiempo_maximo_atencion'])
                    ET.SubElement(stats_element, 'tiempoMinimoAtencion').text = str(estado['tiempo_minimo_atencion'])
                    
                    # Agregar escritorios
                    escritorios_element = ET.SubElement(punto_element, 'escritorios')
                    for escritorio_info in estado['escritorios']:
                        escritorio_element = ET.SubElement(escritorios_element, 'escritorio', {'id': escritorio_info['id']})
                        ET.SubElement(escritorio_element, 'identificacion').text = escritorio_info['identificacion']
                        ET.SubElement(escritorio_element, 'encargado').text = escritorio_info['encargado']
                        ET.SubElement(escritorio_element, 'activo').text = 'true' if escritorio_info['activo'] else 'false'
                        if escritorio_info['cliente_actual']:
                            ET.SubElement(escritorio_element, 'clienteActual').text = escritorio_info['cliente_actual']
                        ET.SubElement(escritorio_element, 'tiempoRestante').text = str(escritorio_info['tiempo_restante'])
                        ET.SubElement(escritorio_element, 'tiempoPromedioAtencion').text = str(escritorio_info['tiempo_promedio_atencion'])
                        ET.SubElement(escritorio_element, 'tiempoMaximoAtencion').text = str(escritorio_info['tiempo_maximo_atencion'])
                        ET.SubElement(escritorio_element, 'tiempoMinimoAtencion').text = str(escritorio_info['tiempo_minimo_atencion'])
                
                # Agregar transacciones
                transacciones_element = ET.SubElement(empresa_element, 'transacciones')
                for transaccion in empresa.transacciones:
                    transaccion_element = ET.SubElement(transacciones_element, 'transaccion', {'id': transaccion.id})
                    ET.SubElement(transaccion_element, 'nombre').text = transaccion.nombre
                    ET.SubElement(transaccion_element, 'tiempoAtencion').text = str(transaccion.tiempo_atencion)
            
            # Crear el árbol XML y guardar el archivo
            tree = ET.ElementTree(root)
            tree.write(ruta_archivo, encoding='utf-8', xml_declaration=True)
            
            return True, f"Estado del sistema guardado en '{ruta_archivo}'."
            
        except Exception as e:
            return False, f"Error al generar el archivo XML de estado: {str(e)}"