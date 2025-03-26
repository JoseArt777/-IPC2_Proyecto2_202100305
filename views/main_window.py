
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from models.cliente import Cliente
from models.empresa import Empresa
from models.punto_atencion import PuntoAtencion
from models.escritorio import Escritorio
from models.transaccion import Transaccion
from utils.graphviz_utils import GraphvizUtils

class MainWindow:
    """
    Ventana principal de la aplicación.
    """
    
    def __init__(self, sistema, xml_controller):
        """
        Inicializa la ventana principal.
        
        Args:
            sistema: Instancia del sistema de atención al cliente
            xml_controller: Controlador para manejar archivos XML
        """
        self.sistema = sistema
        self.xml_controller = xml_controller
        
        # Configurar la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Atención al Cliente - Soluciones Guatemaltecas, S.A.")
        self.ventana.geometry("1200x800")
        self.ventana.resizable(True, True)
        
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_tab_configuracion()
        self.crear_tab_punto_atencion()
        
        # Barra de estado
        self.barra_estado = tk.Label(self.ventana, text="Sistema iniciado", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Directorio para gráficos
        if not os.path.exists("graficos"):
            os.makedirs("graficos")
    
    def iniciar(self):
        """
        Inicia la aplicación.
        """
        self.ventana.mainloop()
    
    def crear_tab_configuracion(self):
        """
        Crea la pestaña de configuración de empresas.
        """
        # Crear frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuración de Empresas")
        
        # Frame izquierdo para operaciones
        frame_izq = ttk.LabelFrame(frame, text="Operaciones")
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de operaciones
        btn_limpiar = ttk.Button(frame_izq, text="Limpiar Sistema", command=self.limpiar_sistema)
        btn_limpiar.pack(fill=tk.X, padx=5, pady=5)
        
        btn_cargar_config = ttk.Button(frame_izq, text="Cargar Archivo de Configuración", command=self.cargar_archivo_configuracion)
        btn_cargar_config.pack(fill=tk.X, padx=5, pady=5)
        
        btn_cargar_inicial = ttk.Button(frame_izq, text="Cargar Archivo de Configuración Inicial", command=self.cargar_archivo_inicial)
        btn_cargar_inicial.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Separator(frame_izq, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=10)
        
        btn_crear_empresa = ttk.Button(frame_izq, text="Crear Nueva Empresa", command=self.crear_empresa)
        btn_crear_empresa.pack(fill=tk.X, padx=5, pady=5)
        
        btn_crear_punto = ttk.Button(frame_izq, text="Crear Punto de Atención", command=self.crear_punto_atencion)
        btn_crear_punto.pack(fill=tk.X, padx=5, pady=5)
        
        btn_crear_escritorio = ttk.Button(frame_izq, text="Crear Escritorio de Servicio", command=self.crear_escritorio)
        btn_crear_escritorio.pack(fill=tk.X, padx=5, pady=5)
        
        btn_crear_transaccion = ttk.Button(frame_izq, text="Crear Transacción", command=self.crear_transaccion)
        btn_crear_transaccion.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame derecho para visualización
        frame_der = ttk.LabelFrame(frame, text="Empresas y Configuración")
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mostrar empresas
        self.tree_empresas = ttk.Treeview(frame_der)
        self.tree_empresas.heading("#0", text="Estructura del Sistema")
        self.tree_empresas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botón para actualizar el árbol
        btn_actualizar = ttk.Button(frame_der, text="Actualizar Visualización", command=self.actualizar_arbol_empresas)
        btn_actualizar.pack(fill=tk.X, padx=5, pady=5)
    
    def crear_tab_punto_atencion(self):
        """
        Crea la pestaña de manejo de puntos de atención.
        """
        # Crear frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Manejo de Puntos de Atención")
        
        # Frame superior para selección
        frame_sup = ttk.LabelFrame(frame, text="Selección de Empresa y Punto de Atención")
        frame_sup.pack(fill=tk.X, padx=10, pady=10)
        
        # Selección de empresa
        ttk.Label(frame_sup, text="Empresa:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_empresas = ttk.Combobox(frame_sup, state="readonly")
        self.combo_empresas.grid(row=0, column=1, padx=5, pady=5)
        self.combo_empresas.bind("<<ComboboxSelected>>", self.actualizar_puntos_atencion)
        
        # Selección de punto de atención
        ttk.Label(frame_sup, text="Punto de Atención:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_puntos = ttk.Combobox(frame_sup, state="readonly")
        self.combo_puntos.grid(row=0, column=3, padx=5, pady=5)
        self.combo_puntos.bind("<<ComboboxSelected>>", self.seleccionar_punto_atencion)
        
        # Botón para actualizar selección
        btn_actualizar = ttk.Button(frame_sup, text="Actualizar Selección", command=self.actualizar_seleccion_empresa_punto)
        btn_actualizar.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame izquierdo para operaciones
        frame_izq = ttk.LabelFrame(frame, text="Operaciones")
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de operaciones
        btn_ver_estado = ttk.Button(frame_izq, text="Ver Estado del Punto de Atención", command=self.ver_estado_punto)
        btn_ver_estado.pack(fill=tk.X, padx=5, pady=5)
        
        btn_activar = ttk.Button(frame_izq, text="Activar Escritorio de Servicio", command=self.activar_escritorio)
        btn_activar.pack(fill=tk.X, padx=5, pady=5)
        
        btn_desactivar = ttk.Button(frame_izq, text="Desactivar Escritorio", command=self.desactivar_escritorio)
        btn_desactivar.pack(fill=tk.X, padx=5, pady=5)
        
        btn_atender = ttk.Button(frame_izq, text="Atender Cliente", command=self.atender_cliente)
        btn_atender.pack(fill=tk.X, padx=5, pady=5)
        
        btn_solicitud = ttk.Button(frame_izq, text="Solicitud de Atención", command=self.solicitar_atencion)
        btn_solicitud.pack(fill=tk.X, padx=5, pady=5)
        
        btn_simular = ttk.Button(frame_izq, text="Simular Actividad del Punto", command=self.simular_actividad)
        btn_simular.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame derecho para visualización
        frame_der = ttk.LabelFrame(frame, text="Estado Actual")
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto para mostrar información
        self.txt_estado = tk.Text(frame_der, wrap=tk.WORD)
        self.txt_estado.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para visualización de gráficos
        frame_graficos = ttk.LabelFrame(frame, text="Visualización Gráfica")
        frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para mostrar gráficos de Graphviz
        self.canvas_graficos = tk.Canvas(frame_graficos, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas_graficos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones para mostrar gráficos
        btn_grafico_cola = ttk.Button(frame_graficos, text="Mostrar Cola de Clientes", command=lambda: self.mostrar_grafico("cola"))
        btn_grafico_cola.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_grafico_escritorios = ttk.Button(frame_graficos, text="Mostrar Escritorios", command=lambda: self.mostrar_grafico("escritorios"))
        btn_grafico_escritorios.pack(side=tk.LEFT, padx=5, pady=5)
    
    def limpiar_sistema(self):
        """
        Limpia todas las estructuras del sistema.
        """
        self.sistema.limpiar_sistema()
        self.actualizar_arbol_empresas()
        self.actualizar_seleccion_empresa_punto()
        messagebox.showinfo("Limpiar Sistema", "El sistema ha sido inicializado correctamente.")
        self.barra_estado.config(text="Sistema inicializado")
    
    def cargar_archivo_configuracion(self):
        """
        Carga un archivo XML de configuración del sistema.
        """
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar Archivo de Configuración",
            filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            exito, mensaje = self.xml_controller.cargar_configuracion(ruta_archivo)
            
            if exito:
                messagebox.showinfo("Cargar Configuración", mensaje)
                self.actualizar_arbol_empresas()
                self.actualizar_seleccion_empresa_punto()
                self.barra_estado.config(text=f"Archivo de configuración cargado: {os.path.basename(ruta_archivo)}")
            else:
                messagebox.showerror("Error", mensaje)
    
    def cargar_archivo_inicial(self):
        """
        Carga un archivo XML de configuración inicial para la prueba.
        """
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar Archivo de Configuración Inicial",
            filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            exito, mensaje = self.xml_controller.cargar_configuracion_inicial(ruta_archivo)
            
            if exito:
                messagebox.showinfo("Cargar Configuración Inicial", mensaje)
                self.actualizar_arbol_empresas()
                self.actualizar_seleccion_empresa_punto()
                self.barra_estado.config(text=f"Archivo de configuración inicial cargado: {os.path.basename(ruta_archivo)}")
            else:
                messagebox.showerror("Error", mensaje)
    
    def crear_empresa(self):
        """
        Crea una nueva empresa en el sistema.
        """
        # Solicitar datos de la empresa
        id_empresa = simpledialog.askstring("Nueva Empresa", "ID de la empresa:")
        if id_empresa is None:
            return
        
        nombre = simpledialog.askstring("Nueva Empresa", "Nombre de la empresa:")
        if nombre is None:
            return
        
        abreviatura = simpledialog.askstring("Nueva Empresa", "Abreviatura de la empresa:")
        if abreviatura is None:
            return
        
        # Crear la empresa
        empresa = self.sistema.crear_empresa(id_empresa, nombre, abreviatura)
        
        if empresa:
            messagebox.showinfo("Nueva Empresa", f"Empresa '{nombre}' creada correctamente.")
            self.actualizar_arbol_empresas()
            self.actualizar_seleccion_empresa_punto()
            self.barra_estado.config(text=f"Empresa creada: {nombre}")
        else:
            messagebox.showerror("Error", f"No se pudo crear la empresa. Posiblemente ya existe una empresa con ID '{id_empresa}'.")
    
    def crear_punto_atencion(self):
        """
        Crea un nuevo punto de atención para una empresa.
        """
        # Seleccionar empresa
        empresas_dict = {}
        for empresa in self.sistema.empresas:
            empresas_dict[f"{empresa.nombre} (ID: {empresa.id})"] = empresa.id
        
        if not empresas_dict:
            messagebox.showerror("Error", "No hay empresas registradas. Cree una empresa primero.")
            return
        
        empresa_seleccionada = simpledialog.askstring(
            "Nuevo Punto de Atención",
            "Seleccione la empresa:",
            initialvalue=list(empresas_dict.keys())[0] if empresas_dict else ""
        )
        
        if empresa_seleccionada is None or empresa_seleccionada not in empresas_dict:
            return
        
        id_empresa = empresas_dict[empresa_seleccionada]
        
        # Solicitar datos del punto de atención
        id_punto = simpledialog.askstring("Nuevo Punto de Atención", "ID del punto de atención:")
        if id_punto is None:
            return
        
        nombre = simpledialog.askstring("Nuevo Punto de Atención", "Nombre del punto de atención:")
        if nombre is None:
            return
        
        direccion = simpledialog.askstring("Nuevo Punto de Atención", "Dirección del punto de atención:")
        if direccion is None:
            return
        
        # Crear el punto de atención
        punto = self.sistema.crear_punto_atencion(id_empresa, id_punto, nombre, direccion)
        
        if punto:
            messagebox.showinfo("Nuevo Punto de Atención", f"Punto de atención '{nombre}' creado correctamente.")
            self.actualizar_arbol_empresas()
            self.barra_estado.config(text=f"Punto de atención creado: {nombre}")
        else:
            messagebox.showerror("Error", f"No se pudo crear el punto de atención. Verifique que no exista un punto con ID '{id_punto}' en la empresa seleccionada.")
    
    def crear_escritorio(self):
        """
        Crea un nuevo escritorio de servicio para un punto de atención.
        """
        # Seleccionar empresa
        empresas_dict = {}
        for empresa in self.sistema.empresas:
            empresas_dict[f"{empresa.nombre} (ID: {empresa.id})"] = empresa.id
        
        if not empresas_dict:
            messagebox.showerror("Error", "No hay empresas registradas. Cree una empresa primero.")
            return
        
        empresa_seleccionada = simpledialog.askstring(
            "Nuevo Escritorio",
            "Seleccione la empresa:",
            initialvalue=list(empresas_dict.keys())[0] if empresas_dict else ""
        )
        
        if empresa_seleccionada is None or empresa_seleccionada not in empresas_dict:
            return
        
        id_empresa = empresas_dict[empresa_seleccionada]
        empresa = self.sistema.obtener_empresa(id_empresa)
        
        # Seleccionar punto de atención
        puntos_dict = {}
        for punto in empresa.puntos_atencion:
            puntos_dict[f"{punto.nombre} (ID: {punto.id})"] = punto.id
        
        if not puntos_dict:
            messagebox.showerror("Error", "La empresa seleccionada no tiene puntos de atención. Cree un punto de atención primero.")
            return
        
        punto_seleccionado = simpledialog.askstring(
            "Nuevo Escritorio",
            "Seleccione el punto de atención:",
            initialvalue=list(puntos_dict.keys())[0] if puntos_dict else ""
        )
        
        if punto_seleccionado is None or punto_seleccionado not in puntos_dict:
            return
        
        id_punto = puntos_dict[punto_seleccionado]
        
        # Solicitar datos del escritorio
        id_escritorio = simpledialog.askstring("Nuevo Escritorio", "ID del escritorio:")
        if id_escritorio is None:
            return
        
        identificacion = simpledialog.askstring("Nuevo Escritorio", "Identificación visible del escritorio:")
        if identificacion is None:
            return
        
        encargado = simpledialog.askstring("Nuevo Escritorio", "Nombre del encargado:")
        if encargado is None:
            return
        
        # Crear el escritorio
        escritorio = self.sistema.crear_escritorio(id_empresa, id_punto, id_escritorio, identificacion, encargado)
        
        if escritorio:
            messagebox.showinfo("Nuevo Escritorio", f"Escritorio '{identificacion}' creado correctamente.")
            self.actualizar_arbol_empresas()
            self.barra_estado.config(text=f"Escritorio creado: {identificacion}")
        else:
            messagebox.showerror("Error", f"No se pudo crear el escritorio. Verifique que no exista un escritorio con ID '{id_escritorio}' en el punto de atención seleccionado.")
    
    def crear_transaccion(self):
        """
        Crea una nueva transacción para una empresa.
        """
        # Seleccionar empresa
        empresas_dict = {}
        for empresa in self.sistema.empresas:
            empresas_dict[f"{empresa.nombre} (ID: {empresa.id})"] = empresa.id
        
        if not empresas_dict:
            messagebox.showerror("Error", "No hay empresas registradas. Cree una empresa primero.")
            return
        
        empresa_seleccionada = simpledialog.askstring(
            "Nueva Transacción",
            "Seleccione la empresa:",
            initialvalue=list(empresas_dict.keys())[0] if empresas_dict else ""
        )
        
        if empresa_seleccionada is None or empresa_seleccionada not in empresas_dict:
            return
        
        id_empresa = empresas_dict[empresa_seleccionada]
        
        # Solicitar datos de la transacción
        id_transaccion = simpledialog.askstring("Nueva Transacción", "ID de la transacción:")
        if id_transaccion is None:
            return
        
        nombre = simpledialog.askstring("Nueva Transacción", "Nombre de la transacción:")
        if nombre is None:
            return
        
        tiempo_atencion = simpledialog.askinteger("Nueva Transacción", "Tiempo de atención (minutos):", minvalue=1)
        if tiempo_atencion is None:
            return
        
        # Crear la transacción
        transaccion = self.sistema.crear_transaccion(id_empresa, id_transaccion, nombre, tiempo_atencion)
        
        if transaccion:
            messagebox.showinfo("Nueva Transacción", f"Transacción '{nombre}' creada correctamente.")
            self.actualizar_arbol_empresas()
            self.barra_estado.config(text=f"Transacción creada: {nombre}")
        else:
            messagebox.showerror("Error", f"No se pudo crear la transacción. Verifique que no exista una transacción con ID '{id_transaccion}' en la empresa seleccionada.")
    
    def actualizar_arbol_empresas(self):
        """
        Actualiza el árbol de empresas en la interfaz.
        """
        # Limpiar árbol actual
        for item in self.tree_empresas.get_children():
            self.tree_empresas.delete(item)
        
        # Agregar empresas al árbol
        for empresa in self.sistema.empresas:
            # Crear nodo de empresa
            id_empresa = self.tree_empresas.insert("", "end", text=f"{empresa.nombre} ({empresa.abreviatura})", values=(empresa.id,))
            
            # Crear nodo de puntos de atención
            id_puntos = self.tree_empresas.insert(id_empresa, "end", text="Puntos de Atención")
            
            # Agregar cada punto de atención
            for punto in empresa.puntos_atencion:
                id_punto = self.tree_empresas.insert(id_puntos, "end", text=f"{punto.nombre}", values=(punto.id,))
                
                # Crear nodo de escritorios
                id_escritorios = self.tree_empresas.insert(id_punto, "end", text="Escritorios")
                
                # Agregar cada escritorio
                for escritorio in punto.escritorios:
                    self.tree_empresas.insert(id_escritorios, "end", text=f"{escritorio.identificacion} - {escritorio.encargado}", values=(escritorio.id,))
            
            # Crear nodo de transacciones
            id_transacciones = self.tree_empresas.insert(id_empresa, "end", text="Transacciones")
            
            # Agregar cada transacción
            for transaccion in empresa.transacciones:
                self.tree_empresas.insert(id_transacciones, "end", text=f"{transaccion.nombre} - {transaccion.tiempo_atencion} min", values=(transaccion.id,))
    
    def actualizar_seleccion_empresa_punto(self):
        """
        Actualiza los combos de selección de empresa y punto de atención.
        """
        # Actualizar combo de empresas
        self.combo_empresas["values"] = []
        valores_empresas = []
        for empresa in self.sistema.empresas:
            valores_empresas.append(f"{empresa.nombre} (ID: {empresa.id})")
        
        if valores_empresas:
            self.combo_empresas["values"] = valores_empresas
            self.combo_empresas.current(0)  # Seleccionar la primera empresa
            
            # Actualizar puntos de atención de la empresa seleccionada
            self.actualizar_puntos_atencion(None)
    
    def actualizar_puntos_atencion(self, event):
        """
        Actualiza el combo de puntos de atención según la empresa seleccionada.
        
        Args:
            event: Evento de selección (puede ser None)
        """
        # Obtener la empresa seleccionada
        seleccion = self.combo_empresas.get()
        if not seleccion:
            return
        
        # Extraer el ID de la empresa
        id_empresa = seleccion.split("ID: ")[1].rstrip(")")
        
        # Seleccionar la empresa
        self.sistema.seleccionar_empresa(id_empresa)
        
        # Actualizar combo de puntos de atención
        self.combo_puntos["values"] = []
        valores_puntos = []
        
        if self.sistema.empresa_actual:
            for punto in self.sistema.empresa_actual.puntos_atencion:
                valores_puntos.append(f"{punto.nombre} (ID: {punto.id})")
        
        if valores_puntos:
            self.combo_puntos["values"] = valores_puntos
            self.combo_puntos.current(0)  # Seleccionar el primer punto
            
            # Seleccionar el punto de atención
            self.seleccionar_punto_atencion(None)
    
    def seleccionar_punto_atencion(self, event):
        """
        Selecciona un punto de atención en el sistema.
        
        Args:
            event: Evento de selección (puede ser None)
        """
        # Obtener el punto seleccionado
        seleccion = self.combo_puntos.get()
        if not seleccion:
            return
        
        # Extraer el ID del punto
        id_punto = seleccion.split("ID: ")[1].rstrip(")")
        
        # Seleccionar el punto
        self.sistema.seleccionar_punto_atencion(id_punto)
        
        # Actualizar visualización del estado
        self.ver_estado_punto()
    
    def ver_estado_punto(self):
        """
        Muestra el estado actual del punto de atención seleccionado.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Obtener estado del punto
        estado = self.sistema.obtener_estado_punto_actual()
        
        # Limpiar área de texto
        self.txt_estado.delete(1.0, tk.END)
        
        # Mostrar información del punto
        self.txt_estado.insert(tk.END, f"ESTADO DEL PUNTO DE ATENCIÓN: {estado['nombre']}\n")
        self.txt_estado.insert(tk.END, f"ID: {estado['id']}\n\n")
        
        # Estadísticas generales
        self.txt_estado.insert(tk.END, "Estadísticas Generales:\n")
        self.txt_estado.insert(tk.END, f"- Escritorios Activos: {estado['escritorios_activos']}\n")
        self.txt_estado.insert(tk.END, f"- Escritorios Inactivos: {estado['escritorios_inactivos']}\n")
        self.txt_estado.insert(tk.END, f"- Clientes en Espera: {estado['clientes_espera']}\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Promedio de Espera: {estado['tiempo_promedio_espera']:.2f} min\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Máximo de Espera: {estado['tiempo_maximo_espera']:.2f} min\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Mínimo de Espera: {estado['tiempo_minimo_espera']:.2f} min\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Promedio de Atención: {estado['tiempo_promedio_atencion']:.2f} min\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Máximo de Atención: {estado['tiempo_maximo_atencion']:.2f} min\n")
        self.txt_estado.insert(tk.END, f"- Tiempo Mínimo de Atención: {estado['tiempo_minimo_atencion']:.2f} min\n\n")
        
        # Información de escritorios
        self.txt_estado.insert(tk.END, "Escritorios de Servicio:\n")
        for escritorio_info in estado['escritorios']:
            estado_escritorio = "Activo" if escritorio_info['activo'] else "Inactivo"
            self.txt_estado.insert(tk.END, f"- Escritorio {escritorio_info['identificacion']} ({estado_escritorio}):\n")
            self.txt_estado.insert(tk.END, f"  * Encargado: {escritorio_info['encargado']}\n")
            if escritorio_info['activo']:
                self.txt_estado.insert(tk.END, f"  * Cliente Actual: {escritorio_info['cliente_actual'] or 'Sin cliente'}\n")
                self.txt_estado.insert(tk.END, f"  * Tiempo Restante: {escritorio_info['tiempo_restante']} min\n")
            self.txt_estado.insert(tk.END, f"  * Tiempo Promedio de Atención: {escritorio_info['tiempo_promedio_atencion']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"  * Tiempo Máximo de Atención: {escritorio_info['tiempo_maximo_atencion']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"  * Tiempo Mínimo de Atención: {escritorio_info['tiempo_minimo_atencion']:.2f} min\n\n")
        
        # Actualizar barra de estado
        self.barra_estado.config(text=f"Estado actualizado: {time.strftime('%H:%M:%S')}")
        
        # Generar y mostrar gráficos
        self.mostrar_grafico("cola")
    
    def activar_escritorio(self):
        """
        Activa un escritorio de servicio en el punto de atención actual.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Obtener escritorios inactivos
        escritorios_inactivos = []
        for escritorio in self.sistema.punto_actual.escritorios:
            if not escritorio.activo:
                escritorios_inactivos.append(f"{escritorio.identificacion} (ID: {escritorio.id})")
        
        if not escritorios_inactivos:
            messagebox.showinfo("Activar Escritorio", "No hay escritorios inactivos disponibles.")
            return
        
        # Seleccionar escritorio a activar
        escritorio_seleccionado = simpledialog.askstring(
            "Activar Escritorio",
            "Seleccione el escritorio a activar:",
            initialvalue=escritorios_inactivos[0] if escritorios_inactivos else ""
        )
        
        if escritorio_seleccionado is None or escritorio_seleccionado not in escritorios_inactivos:
            return
        
        # Extraer ID del escritorio
        id_escritorio = escritorio_seleccionado.split("ID: ")[1].rstrip(")")
        
        # Activar el escritorio
        if self.sistema.activar_escritorio(id_escritorio):
            messagebox.showinfo("Activar Escritorio", f"Escritorio activado correctamente.")
            self.ver_estado_punto()
            self.barra_estado.config(text=f"Escritorio {id_escritorio} activado")
        else:
            messagebox.showerror("Error", "No se pudo activar el escritorio.")
    
    def desactivar_escritorio(self):
        """
        Desactiva un escritorio de servicio en el punto de atención actual.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Obtener escritorios activos
        escritorios_activos = []
        for escritorio in self.sistema.punto_actual.escritorios:
            if escritorio.activo:
                escritorios_activos.append(f"{escritorio.identificacion} (ID: {escritorio.id})")
        
        if not escritorios_activos:
            messagebox.showinfo("Desactivar Escritorio", "No hay escritorios activos para desactivar.")
            return
        
        # Seleccionar escritorio a desactivar
        escritorio_seleccionado = simpledialog.askstring(
            "Desactivar Escritorio",
            "Seleccione el escritorio a desactivar:",
            initialvalue=escritorios_activos[0] if escritorios_activos else ""
        )
        
        if escritorio_seleccionado is None or escritorio_seleccionado not in escritorios_activos:
            return
        
        # Extraer ID del escritorio
        id_escritorio = escritorio_seleccionado.split("ID: ")[1].rstrip(")")
        
        # Desactivar el escritorio
        if self.sistema.desactivar_escritorio(id_escritorio):
            messagebox.showinfo("Desactivar Escritorio", f"Escritorio desactivado correctamente. No atenderá más clientes después de finalizar al cliente actual.")
            self.ver_estado_punto()
            self.barra_estado.config(text=f"Escritorio {id_escritorio} desactivado")
        else:
            messagebox.showerror("Error", "No se pudo desactivar el escritorio.")
    
    def atender_cliente(self):
        """
        Finaliza la atención del próximo cliente que termine su tiempo.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Verificar si hay clientes siendo atendidos
        hay_clientes = False
        for escritorio in self.sistema.punto_actual.escritorios:
            if escritorio.cliente_actual:
                hay_clientes = True
                break
        
        if not hay_clientes:
            messagebox.showinfo("Atender Cliente", "No hay clientes siendo atendidos actualmente.")
            return
        
        # Atender al próximo cliente
        cliente, escritorio = self.sistema.atender_cliente()
        
        if cliente:
            messagebox.showinfo("Atender Cliente", f"Cliente {cliente.nombre} atendido en el escritorio {escritorio.identificacion}.")
            self.ver_estado_punto()
            self.barra_estado.config(text=f"Cliente atendido: {cliente.nombre}")
        else:
            messagebox.showerror("Error", "No se pudo atender al cliente.")
    
    def solicitar_atencion(self):
        """
        Registra un nuevo cliente que solicita atención.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Solicitar datos del cliente
        dpi = simpledialog.askstring("Solicitud de Atención", "DPI del cliente:")
        if dpi is None:
            return
        
        nombre = simpledialog.askstring("Solicitud de Atención", "Nombre del cliente:")
        if nombre is None:
            return
        
        # Crear el cliente
        cliente = Cliente(dpi, nombre)
        
        # Obtener transacciones disponibles
        transacciones_disponibles = {}
        for transaccion in self.sistema.empresa_actual.transacciones:
            transacciones_disponibles[f"{transaccion.nombre} ({transaccion.tiempo_atencion} min) - ID: {transaccion.id}"] = transaccion
        
        if not transacciones_disponibles:
            messagebox.showerror("Error", "No hay transacciones disponibles en la empresa seleccionada.")
            return
        
        # Ventana para seleccionar transacciones
        ventana_trans = tk.Toplevel(self.ventana)
        ventana_trans.title("Seleccionar Transacciones")
        ventana_trans.geometry("500x400")
        ventana_trans.resizable(False, False)
        ventana_trans.grab_set()  # Hacer modal
        
        # Lista de transacciones disponibles
        ttk.Label(ventana_trans, text="Transacciones Disponibles:").pack(padx=10, pady=5)
        frame_lista = ttk.Frame(ventana_trans)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox para selección múltiple
        lista_trans = tk.Listbox(frame_lista, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        lista_trans.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lista_trans.yview)
        
        # Llenar lista con transacciones
        for trans_desc in transacciones_disponibles.keys():
            lista_trans.insert(tk.END, trans_desc)
        
        # Frame para cantidades
        frame_cantidades = ttk.LabelFrame(ventana_trans, text="Cantidad de cada transacción")
        frame_cantidades.pack(fill=tk.X, padx=10, pady=5)
        
        cantidades = {}
        
        def actualizar_cantidades(*args):
            # Limpiar frame de cantidades
            for widget in frame_cantidades.winfo_children():
                widget.destroy()
            
            # Crear spinners para cada transacción seleccionada
            for index in lista_trans.curselection():
                trans_desc = lista_trans.get(index)
                ttk.Label(frame_cantidades, text=trans_desc).grid(row=index, column=0, padx=5, pady=2, sticky=tk.W)
                
                var_cantidad = tk.IntVar(value=1)
                cantidades[trans_desc] = var_cantidad
                
                spinner = ttk.Spinbox(frame_cantidades, from_=1, to=10, width=5, textvariable=var_cantidad)
                spinner.grid(row=index, column=1, padx=5, pady=2)
        
        # Vincular evento de selección
        lista_trans.bind("<<ListboxSelect>>", actualizar_cantidades)
        
        # Función para confirmar selección
        def confirmar_seleccion():
            if not lista_trans.curselection():
                messagebox.showerror("Error", "Debe seleccionar al menos una transacción.")
                return
            
            # Agregar transacciones al cliente
            for index in lista_trans.curselection():
                trans_desc = lista_trans.get(index)
                transaccion = transacciones_disponibles[trans_desc]
                cantidad = cantidades[trans_desc].get()
                cliente.agregar_transaccion(transaccion, cantidad)
            
            # Solicitar atención
            numero, tiempo_espera = self.sistema.solicitar_atencion(cliente)
            
            # Mostrar resultado
            ventana_trans.destroy()
            messagebox.showinfo(
                "Solicitud de Atención",
                f"Cliente registrado correctamente.\n\n"
                f"Número de atención: {numero}\n"
                f"Tiempo estimado de espera: {tiempo_espera:.2f} minutos"
            )
            
            self.ver_estado_punto()
            self.barra_estado.config(text=f"Cliente {cliente.nombre} en espera")
        
        # Botones de acción
        frame_botones = ttk.Frame(ventana_trans)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana_trans.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=5)
        
        btn_confirmar = ttk.Button(frame_botones, text="Confirmar", command=confirmar_seleccion)
        btn_confirmar.pack(side=tk.RIGHT, padx=5)
    
    def simular_actividad(self):
        """
        Simula la atención de todos los clientes pendientes en el punto actual.
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        # Confirmar simulación
        confirmar = messagebox.askyesno(
            "Simular Actividad",
            "¿Está seguro que desea simular la atención de todos los clientes pendientes?\n\n"
            "Esta operación puede tardar unos momentos dependiendo de la cantidad de clientes."
        )
        
        if not confirmar:
            return
        
        # Realizar simulación
        estadisticas = self.sistema.simular_atencion_completa()
        
        if estadisticas:
            # Mostrar resultados
            self.txt_estado.delete(1.0, tk.END)
            
            self.txt_estado.insert(tk.END, "RESULTADOS DE LA SIMULACIÓN\n\n")
            
            # Estadísticas generales
            self.txt_estado.insert(tk.END, "Estadísticas del Punto de Atención:\n")
            self.txt_estado.insert(tk.END, f"- Escritorios Activos: {estadisticas['escritorios_activos']}\n")
            self.txt_estado.insert(tk.END, f"- Escritorios Inactivos: {estadisticas['escritorios_inactivos']}\n")
            self.txt_estado.insert(tk.END, f"- Clientes Atendidos: {estadisticas['clientes_atendidos']}\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Promedio de Espera: {estadisticas['tiempo_promedio_espera']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Máximo de Espera: {estadisticas['tiempo_maximo_espera']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Mínimo de Espera: {estadisticas['tiempo_minimo_espera']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Promedio de Atención: {estadisticas['tiempo_promedio_atencion']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Máximo de Atención: {estadisticas['tiempo_maximo_atencion']:.2f} min\n")
            self.txt_estado.insert(tk.END, f"- Tiempo Mínimo de Atención: {estadisticas['tiempo_minimo_atencion']:.2f} min\n\n")
            
            # Estadísticas por escritorio
            self.txt_estado.insert(tk.END, "Estadísticas por Escritorio:\n")
            for escritorio_info in estadisticas['estadisticas_escritorios']:
                self.txt_estado.insert(tk.END, f"- Escritorio {escritorio_info['identificacion']}:\n")
                self.txt_estado.insert(tk.END, f"  * Clientes Atendidos: {escritorio_info['clientes_atendidos']}\n")
                self.txt_estado.insert(tk.END, f"  * Tiempo Promedio de Atención: {escritorio_info['tiempo_promedio_atencion']:.2f} min\n")
                self.txt_estado.insert(tk.END, f"  * Tiempo Máximo de Atención: {escritorio_info['tiempo_maximo_atencion']:.2f} min\n")
                self.txt_estado.insert(tk.END, f"  * Tiempo Mínimo de Atención: {escritorio_info['tiempo_minimo_atencion']:.2f} min\n\n")
            
            # Generar gráfico de la simulación
            ruta_grafico = os.path.join("graficos", "simulacion.png")
            GraphvizUtils.generar_grafico_simulacion(estadisticas, ruta_grafico)
            
            # Mostrar el gráfico
            self.mostrar_imagen(ruta_grafico)
            
            self.barra_estado.config(text=f"Simulación completada: {time.strftime('%H:%M:%S')}")
        else:
            messagebox.showerror("Error", "No se pudo realizar la simulación.")
    
    def mostrar_grafico(self, tipo_grafico):
        """
        Genera y muestra un gráfico usando Graphviz.
        
        Args:
            tipo_grafico (str): Tipo de gráfico a mostrar ("cola" o "escritorios")
        """
        if not self.sistema.punto_actual:
            messagebox.showerror("Error", "No hay punto de atención seleccionado.")
            return
        
        if tipo_grafico == "cola":
            # Generar gráfico de cola de clientes
            ruta_grafico = os.path.join("graficos", "cola_clientes.png")
            GraphvizUtils.generar_grafico_cola_clientes(self.sistema.punto_actual, ruta_grafico)
            
            # Mostrar el gráfico
            self.mostrar_imagen(ruta_grafico)
            
            self.barra_estado.config(text="Mostrando gráfico de cola de clientes")
        
        elif tipo_grafico == "escritorios":
            # Generar gráfico de escritorios
            ruta_grafico = os.path.join("graficos", "escritorios.png")
            GraphvizUtils.generar_grafico_escritorios(self.sistema.punto_actual, ruta_grafico)
            
            # Mostrar el gráfico
            self.mostrar_imagen(ruta_grafico)
            
            self.barra_estado.config(text="Mostrando gráfico de escritorios")
    
    def mostrar_imagen(self, ruta_imagen):
        """
        Muestra una imagen en el canvas.
        
        Args:
            ruta_imagen (str): Ruta al archivo de imagen
        """
        try:
            # Limpiar canvas
            self.canvas_graficos.delete("all")
            
            # Cargar imagen
            from PIL import Image, ImageTk
            
            imagen = Image.open(ruta_imagen)
            
            # Ajustar tamaño
            ancho_canvas = self.canvas_graficos.winfo_width()
            alto_canvas = self.canvas_graficos.winfo_height()
            
            if ancho_canvas <= 1 or alto_canvas <= 1:
                # Si el canvas aún no está dibujado, usar tamaños predeterminados
                ancho_canvas = 800
                alto_canvas = 400
            
            # Calcular nueva dimensión manteniendo la relación de aspecto
            ancho_img, alto_img = imagen.size
            ratio_img = ancho_img / alto_img
            ratio_canvas = ancho_canvas / alto_canvas
            
            if ratio_img > ratio_canvas:
                # La imagen es más ancha proporcionalmente
                nuevo_ancho = ancho_canvas
                nuevo_alto = int(nuevo_ancho / ratio_img)
            else:
                # La imagen es más alta proporcionalmente
                nuevo_alto = alto_canvas
                nuevo_ancho = int(nuevo_alto * ratio_img)
            
            # Redimensionar imagen
            imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            
            # Convertir a PhotoImage
            img_tk = ImageTk.PhotoImage(imagen_redimensionada)
            
            # Guardar referencia para evitar que sea eliminada por el garbage collector
            self.imagen_actual = img_tk
            
            # Mostrar imagen en el canvas
            self.canvas_graficos.create_image(ancho_canvas//2, alto_canvas//2, image=img_tk, anchor=tk.CENTER)
            
        except Exception as e:
            print(f"Error al mostrar la imagen: {str(e)}")
            messagebox.showerror("Error", f"No se pudo mostrar la imagen: {str(e)}")