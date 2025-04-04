import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import tempfile
from PIL import Image, ImageTk
import subprocess
from sistema import SistemaAtencion
from procesador_xml import ProcesadorXML

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención a Clientes")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f7f9f9")

        
        self.sistema = SistemaAtencion()
        self.procesador = ProcesadorXML(self.sistema)
        
        self.setup_ui()

    # Añadir este método a la clase VentanaPrincipal en interfaz_grafica.py

    def guardar_tablas_estadisticas(self):
        """
        Genera y guarda tablas estadísticas como archivos de imagen.
        """
        if not self.sistema.punto_actual:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un punto de atención.")
            return
        
        # Solicitar directorio al usuario
        directorio = filedialog.askdirectory(
            title="Seleccionar directorio para guardar reportes",
            initialdir="."
        )
        
        if not directorio:  # Si el usuario cancela la selección
            return
        
        # Generar y guardar tablas estadísticas
        resultado, mensaje = self.sistema.guardar_tablas_estadisticas(directorio)
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    # Modificar el método setup_tab_puntos para añadir el botón
    # Encontrar la sección donde se definen los botones en frame_ops_punto
    # y añadir el siguiente código después del último botón:

    
    def setup_ui(self):
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de configuración
        self.tab_config = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_config, text="Configuración de Empresas")
        self.setup_tab_config()
        
        # Pestaña de manejo de puntos de atención
        self.tab_puntos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_puntos, text="Manejo de Puntos de Atención")
        self.setup_tab_puntos()

        style = ttk.Style()
        style.theme_use("clam")  # Puedes probar también 'alt', 'default' o 'vista'

        # Estilo de botones
        style.configure("TButton", font=("Segoe UI", 10), padding=6, foreground="white", background="#2c3e50")
        style.map("TButton",
            background=[("active", "#34495e"), ("disabled", "#bdc3c7")],
            foreground=[("disabled", "#ecf0f1")]
        )

        # Estilo de labels y frames
        style.configure("TLabel", font=("Segoe UI", 10), foreground="#2c3e50")
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground="#2980b9")
        style.configure("TLabelframe", background="#ecf0f1")

        # Estilo de Combobox
        style.configure("TCombobox", padding=4)

        # Treeview
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2980b9", foreground="white")

    
    def setup_tab_config(self):
        # Marco para operaciones de configuración
        frame_ops = ttk.LabelFrame(self.tab_config, text="Operaciones")
        frame_ops.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones para operaciones
        ttk.Button(frame_ops, text="Limpiar Sistema", command=self.limpiar_sistema).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_ops, text="Cargar Archivo de Configuración", command=self.cargar_config).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_ops, text="Crear Nueva Empresa", command=self.crear_empresa).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame_ops, text="Cargar Configuración Inicial", command=self.cargar_config_inicial).grid(row=0, column=3, padx=5, pady=5)
        
        # Marco para la lista de empresas
        frame_empresas = ttk.LabelFrame(self.tab_config, text="Empresas Registradas")
        frame_empresas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mostrar empresas
        self.tree_empresas = ttk.Treeview(frame_empresas, columns=("nombre", "abreviatura", "puntos", "transacciones"), show="headings")
        self.tree_empresas.heading("nombre", text="Nombre")
        self.tree_empresas.heading("abreviatura", text="Abreviatura")
        self.tree_empresas.heading("puntos", text="Puntos de Atención")
        self.tree_empresas.heading("transacciones", text="Transacciones")
        self.tree_empresas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(frame_empresas, orient=tk.VERTICAL, command=self.tree_empresas.yview)
        self.tree_empresas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones para gestionar empresas
        frame_ops_empresa = ttk.Frame(frame_empresas)
        frame_ops_empresa.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_ops_empresa, text="Ver Detalles", command=self.ver_detalles_empresa).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ops_empresa, text="Crear Punto de Atención", command=self.crear_punto_atencion).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ops_empresa, text="Crear Transacción", command=self.crear_transaccion).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_ops_empresa, text="Crear Escritorio", command=self.crear_escritorio).pack(side=tk.LEFT, padx=5)
    def setup_tab_puntos(self):
        # Marco para selección de empresa y punto
        frame_seleccion = ttk.LabelFrame(self.tab_puntos, text="Selección")
        frame_seleccion.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_seleccion, text="Empresa:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_empresas = ttk.Combobox(frame_seleccion, state="readonly")
        self.combo_empresas.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.combo_empresas.bind("<<ComboboxSelected>>", self.actualizar_puntos)
        
        ttk.Label(frame_seleccion, text="Punto de Atención:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_puntos = ttk.Combobox(frame_seleccion, state="readonly")
        self.combo_puntos.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.combo_puntos.bind("<<ComboboxSelected>>", self.seleccionar_punto)
        
        ttk.Button(frame_seleccion, text="Actualizar", command=self.actualizar_empresas).grid(row=0, column=2, padx=5, pady=5)
        
        # Marco para operaciones de punto de atención
        frame_ops_punto = ttk.LabelFrame(self.tab_puntos, text="Operaciones")
        frame_ops_punto.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_ops_punto, text="Guardar Estadísticas", command=self.guardar_tablas_estadisticas).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Ver Estado", command=self.ver_estado).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Activar Escritorio", command=self.activar_escritorio).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Desactivar Escritorio", command=self.desactivar_escritorio).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Atender Cliente", command=self.atender_cliente).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Solicitud de Atención", command=self.solicitar_atencion).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_ops_punto, text="Simular Actividad", command=self.simular_actividad).grid(row=0, column=5, padx=5, pady=5)
        
        # Marco para mostrar información
        frame_info = ttk.LabelFrame(self.tab_puntos, text="Información")
        frame_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook para información
        self.notebook_info = ttk.Notebook(frame_info)
        self.notebook_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de estadísticas
        self.tab_stats = ttk.Frame(self.notebook_info)
        self.notebook_info.add(self.tab_stats, text="Estadísticas")
        
        # Texto para estadísticas
        self.text_stats = tk.Text(self.tab_stats, height=10, width=80)
        self.text_stats.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_stats = ttk.Scrollbar(self.tab_stats, orient=tk.VERTICAL, command=self.text_stats.yview)
        self.text_stats.configure(yscroll=scrollbar_stats.set)
        scrollbar_stats.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pestaña de visualización de escritorios
        self.tab_escritorios = ttk.Frame(self.notebook_info)
        self.notebook_info.add(self.tab_escritorios, text="Escritorios")
        
        # Canvas para mostrar imagen de escritorios
        self.canvas_escritorios = tk.Canvas(self.tab_escritorios)
        self.canvas_escritorios.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de visualización de cola
        self.tab_cola = ttk.Frame(self.notebook_info)
        self.notebook_info.add(self.tab_cola, text="Cola de Espera")
        
        # Canvas para mostrar imagen de cola
        self.canvas_cola = tk.Canvas(self.tab_cola)
        self.canvas_cola.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inicializar combos
        self.actualizar_empresas()
    
    def limpiar_sistema(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar el sistema? Se perderán todos los datos."):
            resultado, mensaje = self.sistema.limpiar_sistema()
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_empresas()
                self.actualizar_puntos(None)
                self.limpiar_info()
            else:
                messagebox.showerror("Error", mensaje)
    
    def cargar_config(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración",
            filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
        )
        if filename:
            resultado, mensaje = self.procesador.cargar_configuracion(filename)
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_empresas()
            else:
                messagebox.showerror("Error", mensaje)
    
    def cargar_config_inicial(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración inicial",
            filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
        )
        if filename:
            resultado, mensaje = self.procesador.cargar_configuracion_inicial(filename)
            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                # Actualizar información si hay un punto seleccionado
                if self.sistema.punto_actual:
                    self.ver_estado()
            else:
                messagebox.showerror("Error", mensaje)
    
    def crear_empresa(self):
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nueva Empresa")
        dialog.geometry("400x200")
        dialog.grab_set()  # Modal
        
        # Campos del formulario
        ttk.Label(dialog, text="ID Empresa:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        id_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=id_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        nombre_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=nombre_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Abreviatura:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        abrev_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=abrev_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Botones
        def guardar():
            id_empresa = id_var.get().strip()
            nombre = nombre_var.get().strip()
            abreviatura = abrev_var.get().strip()
            
            if not id_empresa or not nombre or not abreviatura:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                return
            
            resultado, mensaje = self.sistema.crear_empresa(id_empresa, nombre, abreviatura)
            if resultado:
                messagebox.showinfo("Éxito", mensaje, parent=dialog)
                dialog.destroy()
                self.actualizar_empresas()
            else:
                messagebox.showerror("Error", mensaje, parent=dialog)
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=3, column=1, padx=5, pady=10)
        
        # Hacer que el grid sea expansible
        dialog.columnconfigure(1, weight=1)
    
    def crear_transaccion(self):
        seleccion = self.tree_empresas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa.")
            return
        
        id_empresa = seleccion[0]
        empresa = self.sistema.obtener_empresa(id_empresa)
        if not empresa:
            messagebox.showerror("Error", "La empresa seleccionada no está disponible.")
            return
        
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Crear Transacción para {empresa.nombre}")
        dialog.geometry("400x200")
        dialog.grab_set()  # Modal
        
        # Campos del formulario
        ttk.Label(dialog, text="ID Transacción:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        id_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=id_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        nombre_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=nombre_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Tiempo de Atención (min):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        tiempo_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=tiempo_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Botones
        def guardar():
            id_trans = id_var.get().strip()
            nombre = nombre_var.get().strip()
            
            try:
                tiempo = int(tiempo_var.get().strip())
                if tiempo <= 0:
                    raise ValueError("El tiempo debe ser un número positivo.")
            except ValueError as e:
                messagebox.showerror("Error", f"Tiempo inválido: {str(e)}", parent=dialog)
                return
            
            if not id_trans or not nombre:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                return
            
            from modelo import Transaccion
            trans = Transaccion(id_trans, nombre, tiempo)
            empresa.agregar_transaccion(trans)
            
            messagebox.showinfo("Éxito", f"Transacción '{nombre}' creada correctamente.", parent=dialog)
            dialog.destroy()
            
            # Actualizar árbol de empresas
            num_puntos = len(empresa.puntos_atencion)
            num_trans = len(empresa.transacciones)
            self.tree_empresas.item(id_empresa, values=(empresa.nombre, empresa.abreviatura, num_puntos, num_trans))
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=3, column=1, padx=5, pady=10)
        
        # Hacer que el grid sea expansible
        dialog.columnconfigure(1, weight=1)
    
    def crear_escritorio(self):
        seleccion = self.tree_empresas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa.")
            return

        id_empresa = seleccion[0]
        empresa = self.sistema.obtener_empresa(id_empresa)
        if not empresa:
            messagebox.showerror("Error", "La empresa seleccionada no está disponible.")
            return

        if not empresa.puntos_atencion:
            messagebox.showwarning("Advertencia", "La empresa no tiene puntos de atención.")
            return

        # Diálogo para seleccionar el punto de atención
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Escritorio")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text="Seleccionar Punto de Atención:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        combo_puntos = ttk.Combobox(dialog, state="readonly")
        puntos = [p.nombre for p in empresa.puntos_atencion]
        ids_puntos = [p.id for p in empresa.puntos_atencion]
        combo_puntos['values'] = puntos
        combo_puntos.grid(row=0, column=1, padx=5, pady=5)
        combo_puntos.current(0)

        ttk.Label(dialog, text="ID Escritorio:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        id_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=id_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Identificación:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ident_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=ident_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Encargado:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        encargado_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=encargado_var).grid(row=3, column=1, padx=5, pady=5)

        def guardar():
            idx = combo_puntos.current()
            id_punto = ids_puntos[idx]
            punto = empresa.obtener_punto_atencion(id_punto)

            id_esc = id_var.get().strip()
            ident = ident_var.get().strip()
            encargado = encargado_var.get().strip()

            if not id_esc or not ident or not encargado:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                return

            from modelo import EscritorioServicio
            nuevo = EscritorioServicio(id_esc, ident, encargado)
            punto.agregar_escritorio(nuevo)

            messagebox.showinfo("Éxito", f"Escritorio '{ident}' agregado a '{punto.nombre}'.", parent=dialog)
            dialog.destroy()

        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=4, column=1, padx=5, pady=10)

    def actualizar_empresas(self):
        """
        Actualiza la lista de empresas en el combo y en el árbol.
        """
        # Limpiar árbol
        for item in self.tree_empresas.get_children():
            self.tree_empresas.delete(item)
        
        # Llenar árbol
        ids_empresas = []
        nombres_empresas = []
        
        for id_empresa, empresa in self.sistema.empresas.items():
            ids_empresas.append(id_empresa)
            nombres_empresas.append(f"{empresa.nombre} ({empresa.abreviatura})")
            
            num_puntos = len(empresa.puntos_atencion)
            num_trans = len(empresa.transacciones)
            
            self.tree_empresas.insert("", "end", id_empresa, values=(empresa.nombre, empresa.abreviatura, num_puntos, num_trans))
        
        # Actualizar combo
        self.combo_empresas['values'] = nombres_empresas
        
        # Si hay empresas, seleccionar la primera
        if ids_empresas:
            self.sistema.seleccionar_empresa(ids_empresas[0])
            self.combo_empresas.current(0)
            self.actualizar_puntos(None)
    
    def actualizar_puntos(self, event):
        """
        Actualiza la lista de puntos de atención en el combo.
        """
        if not self.sistema.empresa_actual:
            self.combo_puntos['values'] = []
            return
        
        # Obtener puntos de la empresa actual
        puntos = []
        ids_puntos = []
        
        for punto in self.sistema.empresa_actual.puntos_atencion:
            puntos.append(punto.nombre)
            ids_puntos.append(punto.id)
        
        # Actualizar combo
        self.combo_puntos['values'] = puntos
        
        # Si hay puntos, seleccionar el primero
        if puntos:
            self.combo_puntos.current(0)
            self.sistema.seleccionar_punto(ids_puntos[0])
        else:
            self.sistema.punto_actual = None
    
    def seleccionar_punto(self, event):
        """
        Selecciona el punto de atención actual.
        """
        if not self.sistema.empresa_actual:
            return
        
        index = self.combo_puntos.current()
        if index < 0:
            return
        
        # Obtener ID del punto seleccionado
        id_punto = None
        i = 0
        
        for punto in self.sistema.empresa_actual.puntos_atencion:
            if i == index:
                id_punto = punto.id
                break
            i += 1
        
        if id_punto:
            self.sistema.seleccionar_punto(id_punto)
    
    def ver_estado(self):
        """
        Muestra el estado actual del punto de atención.
        """
        if not self.sistema.punto_actual:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un punto de atención.")
            return
        
        # Obtener estado
        resultado, datos = self.sistema.ver_estado_punto()
        if not resultado:
            messagebox.showerror("Error", datos)
            return
        
        # Actualizar estadísticas
        stats = datos["estadisticas"]
        self.mostrar_estadisticas(stats)
        
        # Generar y mostrar diagramas
        self.generar_diagrama_escritorios(datos["dot_escritorios"])
        self.generar_diagrama_cola(datos["dot_cola"])
    
    def mostrar_estadisticas(self, stats):
        """
        Muestra las estadísticas en el área de texto.
        """
        self.text_stats.delete(1.0, tk.END)
        
        # Información general
        self.text_stats.insert(tk.END, "INFORMACIÓN DEL PUNTO DE ATENCIÓN\n")
        self.text_stats.insert(tk.END, "=" * 50 + "\n\n")
        
        self.text_stats.insert(tk.END, f"Nombre: {self.sistema.punto_actual.nombre}\n")
        self.text_stats.insert(tk.END, f"Dirección: {self.sistema.punto_actual.direccion}\n\n")
        
        # Estadísticas del punto
        self.text_stats.insert(tk.END, "ESTADÍSTICAS GENERALES\n")
        self.text_stats.insert(tk.END, "-" * 50 + "\n")
        self.text_stats.insert(tk.END, f"Escritorios activos: {stats['escritorios_activos']}\n")
        self.text_stats.insert(tk.END, f"Escritorios inactivos: {stats['escritorios_inactivos']}\n")
        self.text_stats.insert(tk.END, f"Clientes en espera: {stats['clientes_en_espera']}\n")
        self.text_stats.insert(tk.END, f"Clientes atendidos: {stats['clientes_atendidos']}\n\n")
        
        # Tiempos
        self.text_stats.insert(tk.END, "TIEMPOS DE ESPERA\n")
        self.text_stats.insert(tk.END, "-" * 50 + "\n")
        self.text_stats.insert(tk.END, f"Tiempo promedio: {stats['tiempo_promedio_espera']:.2f} min\n")
        self.text_stats.insert(tk.END, f"Tiempo mínimo: {stats['tiempo_min_espera']:.2f} min\n")
        self.text_stats.insert(tk.END, f"Tiempo máximo: {stats['tiempo_max_espera']:.2f} min\n\n")
        
        self.text_stats.insert(tk.END, "TIEMPOS DE ATENCIÓN\n")
        self.text_stats.insert(tk.END, "-" * 50 + "\n")
        self.text_stats.insert(tk.END, f"Tiempo promedio: {stats['tiempo_promedio_atencion']:.2f} min\n")
        self.text_stats.insert(tk.END, f"Tiempo mínimo: {stats['tiempo_min_atencion']:.2f} min\n")
        self.text_stats.insert(tk.END, f"Tiempo máximo: {stats['tiempo_max_atencion']:.2f} min\n\n")
        
        # Estadísticas por escritorio
        self.text_stats.insert(tk.END, "ESTADÍSTICAS POR ESCRITORIO\n")
        self.text_stats.insert(tk.END, "-" * 50 + "\n")
        
        for escritorio in self.sistema.punto_actual.escritorios:
            estado = "Inactivo"
            if escritorio.estado == escritorio.ACTIVO:
                estado = "Activo"
            elif escritorio.estado == escritorio.OCUPADO:
                estado = "Ocupado"
            
            self.text_stats.insert(tk.END, f"Escritorio: {escritorio.identificacion} ({estado})\n")
            self.text_stats.insert(tk.END, f"  Encargado: {escritorio.encargado}\n")
            self.text_stats.insert(tk.END, f"  Clientes atendidos: {escritorio.clientes_atendidos}\n")
            
            if escritorio.clientes_atendidos > 0:
                tiempo_prom = escritorio.tiempo_promedio_atencion()
                self.text_stats.insert(tk.END, f"  Tiempo promedio: {tiempo_prom:.2f} min\n")
                self.text_stats.insert(tk.END, f"  Tiempo mínimo: {escritorio.tiempo_min_atencion if escritorio.tiempo_min_atencion != float('inf') else 0:.2f} min\n")
                self.text_stats.insert(tk.END, f"  Tiempo máximo: {escritorio.tiempo_max_atencion:.2f} min\n")
            
            self.text_stats.insert(tk.END, "\n")
    
    def generar_diagrama_escritorios(self, dot_source):
        """
        Genera y muestra el diagrama de escritorios.
        """
        if not dot_source:
            return
        
        try:
            # Crear archivo temporal para el dot
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dot') as dot_file:
                dot_file.write(dot_source.encode('utf-8'))
                dot_filename = dot_file.name
            
            # Crear archivo temporal para la imagen
            img_filename = dot_filename + '.png'
            
            # Generar imagen
            subprocess.run(['dot', '-Tpng', dot_filename, '-o', img_filename], check=True)
            
            # Mostrar imagen
            img = Image.open(img_filename)
            photo = ImageTk.PhotoImage(img)
            
            # Limpiar canvas
            self.canvas_escritorios.delete("all")
            
            # Mostrar imagen en canvas
            self.canvas_escritorios.config(width=img.width, height=img.height)
            self.canvas_escritorios.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas_escritorios.photo = photo  # Guardar referencia
            
            # Eliminar archivos temporales
            os.unlink(dot_filename)
            os.unlink(img_filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar diagrama de escritorios: {str(e)}")
    
    def generar_diagrama_cola(self, dot_source):
        """
        Genera y muestra el diagrama de cola.
        """
        if not dot_source:
            return
        
        try:
            # Crear archivo temporal para el dot
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dot') as dot_file:
                dot_file.write(dot_source.encode('utf-8'))
                dot_filename = dot_file.name
            
            # Crear archivo temporal para la imagen
            img_filename = dot_filename + '.png'
            
            # Generar imagen
            subprocess.run(['dot', '-Tpng', dot_filename, '-o', img_filename], check=True)
            
            # Mostrar imagen
            img = Image.open(img_filename)
            photo = ImageTk.PhotoImage(img)
            
            # Limpiar canvas
            self.canvas_cola.delete("all")
            
            # Mostrar imagen en canvas
            self.canvas_cola.config(width=img.width, height=img.height)
            self.canvas_cola.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas_cola.photo = photo  # Guardar referencia
            
            # Eliminar archivos temporales
            os.unlink(dot_filename)
            os.unlink(img_filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar diagrama de cola: {str(e)}")
    
    def activar_escritorio(self):
        resultado, mensaje = self.sistema.activar_escritorio_auto()
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.ver_estado()
        else:
            messagebox.showwarning("Advertencia", mensaje)

    def desactivar_escritorio(self):
        resultado, mensaje_o_escritorio = self.sistema.desactivar_escritorio_auto()
        
        if resultado:
            # Aquí mensaje_o_escritorio es un objeto escritorio
            escritorio = mensaje_o_escritorio
            if escritorio.pendiente_desactivar:
                messagebox.showinfo("Aviso", f"Escritorio '{escritorio.identificacion}' se desactivará cuando termine con su cliente actual.")
            else:
                messagebox.showinfo("Éxito", f"Escritorio '{escritorio.identificacion}' desactivado correctamente.")
            self.ver_estado()
        else:
            # Aquí mensaje_o_escritorio es un mensaje de error
            messagebox.showwarning("Advertencia", mensaje_o_escritorio)

    def atender_cliente(self):
        """
        Completa la atención del cliente que está más próximo a terminar.
        """
        if not self.sistema.punto_actual:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un punto de atención.")
            return
        
        resultado, mensaje = self.sistema.atender_cliente()
        
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.ver_estado()  # Actualizar vista
        else:
            messagebox.showwarning("Advertencia", mensaje)
    
    def solicitar_atencion(self):
        """
        Agrega un cliente que solicita atención.
        """
        if not self.sistema.punto_actual or not self.sistema.empresa_actual:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un punto de atención.")
            return
        
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Solicitar Atención")
        dialog.geometry("500x400")
        dialog.grab_set()  # Modal
        
        # Datos del cliente
        frame_cliente = ttk.LabelFrame(dialog, text="Datos del Cliente")
        frame_cliente.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_cliente, text="DPI:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        dpi_var = tk.StringVar()
        ttk.Entry(frame_cliente, textvariable=dpi_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(frame_cliente, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        nombre_var = tk.StringVar()
        ttk.Entry(frame_cliente, textvariable=nombre_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Transacciones
        frame_trans = ttk.LabelFrame(dialog, text="Transacciones")
        frame_trans.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Lista de transacciones disponibles
        ttk.Label(frame_trans, text="Transacciones disponibles:").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        tree_trans = ttk.Treeview(frame_trans, columns=("id", "nombre", "tiempo", "cantidad"), show="headings", height=6)
        tree_trans.heading("id", text="ID")
        tree_trans.heading("nombre", text="Nombre")
        tree_trans.heading("tiempo", text="Tiempo de Atención (min)")
        tree_trans.heading("cantidad", text="Cantidad")
        tree_trans.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Llenar transacciones
        for id_trans, trans in self.sistema.empresa_actual.transacciones.items():
            tree_trans.insert("", "end", id_trans, values=(id_trans, trans.nombre, trans.tiempo_atencion, 0))
        
        # Botones para modificar cantidad
        def aumentar_cantidad():
            seleccion = tree_trans.selection()
            if not seleccion:
                return
            
            id_trans = seleccion[0]
            values = tree_trans.item(id_trans, "values")
            cantidad = int(values[3]) + 1
            tree_trans.item(id_trans, values=(values[0], values[1], values[2], cantidad))
        
        def disminuir_cantidad():
            seleccion = tree_trans.selection()
            if not seleccion:
                return
            
            id_trans = seleccion[0]
            values = tree_trans.item(id_trans, "values")
            cantidad = max(0, int(values[3]) - 1)
            tree_trans.item(id_trans, values=(values[0], values[1], values[2], cantidad))
        
        frame_btns = ttk.Frame(frame_trans)
        frame_btns.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Button(frame_btns, text="+", command=aumentar_cantidad).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btns, text="-", command=disminuir_cantidad).pack(side=tk.LEFT, padx=5)
        
        # Botones de confirmación
        def solicitar():
            dpi = dpi_var.get().strip()
            nombre = nombre_var.get().strip()
            
            if not dpi or not nombre:
                messagebox.showerror("Error", "Debe ingresar DPI y nombre del cliente.", parent=dialog)
                return
            
            # Recolectar transacciones
            transacciones = []
            for id_trans in tree_trans.get_children():
                values = tree_trans.item(id_trans, "values")
                cantidad = int(values[3])
                if cantidad > 0:
                    transacciones.append((id_trans, cantidad))
            
            if not transacciones:
                messagebox.showerror("Error", "Debe seleccionar al menos una transacción.", parent=dialog)
                return
            
            # Solicitar atención
            resultado, datos = self.sistema.solicitar_atencion(dpi, nombre, transacciones)
            
            if resultado:
                mensaje = f"Cliente registrado en posición {datos['posicion']}.\n\n"
                mensaje += f"Tiempo estimado de espera: {datos['tiempo_espera']} minutos.\n"
                mensaje += f"Tiempo de atención: {datos['tiempo_atencion']} minutos."
                
                messagebox.showinfo("Éxito", mensaje, parent=dialog)
                dialog.destroy()
                self.ver_estado()  # Actualizar vista
            else:
                messagebox.showerror("Error", datos, parent=dialog)
        
        frame_confirm = ttk.Frame(dialog)
        frame_confirm.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_confirm, text="Solicitar Atención", command=solicitar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_confirm, text="Cancelar", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Hacer que los frames sean expansibles
        frame_cliente.columnconfigure(1, weight=1)
        frame_trans.columnconfigure(1, weight=1)
        frame_trans.rowconfigure(1, weight=1)
    
    def simular_actividad(self):
        """
        Simula la atención de todos los clientes pendientes.
        """
        if not self.sistema.punto_actual:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un punto de atención.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea simular la actividad? Se atenderán todos los clientes pendientes."):
            resultado, stats = self.sistema.simular_actividad()
            
            if resultado:
                # Mostrar resultados
                dialog = tk.Toplevel(self.root)
                dialog.title("Resultados de la Simulación")
                dialog.geometry("500x500")
                dialog.grab_set()  # Modal
                
                # Crear texto para mostrar estadísticas
                text = tk.Text(dialog, wrap=tk.WORD)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Estadísticas generales
                text.insert(tk.END, "RESULTADOS DE LA SIMULACIÓN\n")
                text.insert(tk.END, "=" * 50 + "\n\n")
                
                text.insert(tk.END, f"Punto de atención: {self.sistema.punto_actual.nombre}\n\n")
                
                text.insert(tk.END, "ESTADÍSTICAS GENERALES\n")
                text.insert(tk.END, "-" * 50 + "\n")
                text.insert(tk.END, f"Escritorios activos: {stats['escritorios_activos']}\n")
                text.insert(tk.END, f"Escritorios inactivos: {stats['escritorios_inactivos']}\n")
                text.insert(tk.END, f"Clientes atendidos: {stats['clientes_atendidos']}\n\n")
                
                # Tiempos
                text.insert(tk.END, "TIEMPOS DE ESPERA\n")
                text.insert(tk.END, "-" * 50 + "\n")
                text.insert(tk.END, f"Tiempo promedio: {stats['tiempo_promedio_espera']:.2f} min\n")
                text.insert(tk.END, f"Tiempo mínimo: {stats['tiempo_min_espera']:.2f} min\n")
                text.insert(tk.END, f"Tiempo máximo: {stats['tiempo_max_espera']:.2f} min\n\n")
                
                text.insert(tk.END, "TIEMPOS DE ATENCIÓN\n")
                text.insert(tk.END, "-" * 50 + "\n")
                text.insert(tk.END, f"Tiempo promedio: {stats['tiempo_promedio_atencion']:.2f} min\n")
                text.insert(tk.END, f"Tiempo mínimo: {stats['tiempo_min_atencion']:.2f} min\n")
                text.insert(tk.END, f"Tiempo máximo: {stats['tiempo_max_atencion']:.2f} min\n\n")
                
                # Estadísticas por escritorio
                text.insert(tk.END, "ESTADÍSTICAS POR ESCRITORIO\n")
                text.insert(tk.END, "-" * 50 + "\n")
                
                for escritorio in self.sistema.punto_actual.escritorios:
                    if escritorio.estado != escritorio.INACTIVO:
                        text.insert(tk.END, f"Escritorio: {escritorio.identificacion}\n")
                        text.insert(tk.END, f"  Clientes atendidos: {escritorio.clientes_atendidos}\n")
                        
                        if escritorio.clientes_atendidos > 0:
                            tiempo_prom = escritorio.tiempo_promedio_atencion()
                            text.insert(tk.END, f"  Tiempo promedio: {tiempo_prom:.2f} min\n")
                            text.insert(tk.END, f"  Tiempo mínimo: {escritorio.tiempo_min_atencion if escritorio.tiempo_min_atencion != float('inf') else 0:.2f} min\n")
                            text.insert(tk.END, f"  Tiempo máximo: {escritorio.tiempo_max_atencion:.2f} min\n")
                        
                        text.insert(tk.END, "\n")
                
                # Botón de cerrar
                ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)
                
                # Actualizar vista
                self.ver_estado()
            else:
                messagebox.showerror("Error", stats)
    
    def limpiar_info(self):
        """
        Limpia las áreas de información.
        """
        self.text_stats.delete(1.0, tk.END)
        self.canvas_escritorios.delete("all")
        self.canvas_cola.delete("all")
    
    def ver_detalles_empresa(self):
        seleccion = self.tree_empresas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa.")
            return
        
        id_empresa = seleccion[0]
        empresa = self.sistema.obtener_empresa(id_empresa)
        if not empresa:
            messagebox.showerror("Error", "La empresa seleccionada no está disponible.")
            return
        
        # Crear ventana con detalles
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Detalles de Empresa: {empresa.nombre}")
        dialog.geometry("600x500")
        dialog.grab_set()  # Modal
        
        # Información general
        frame_info = ttk.LabelFrame(dialog, text="Información General")
        frame_info.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_info, text=f"ID: {empresa.id}").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(frame_info, text=f"Nombre: {empresa.nombre}").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(frame_info, text=f"Abreviatura: {empresa.abreviatura}").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        
        # Notebook para puntos y transacciones
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de puntos de atención
        tab_puntos = ttk.Frame(notebook)
        notebook.add(tab_puntos, text="Puntos de Atención")
        
        # Treeview para puntos
        tree_puntos = ttk.Treeview(tab_puntos, columns=("nombre", "direccion", "escritorios"), show="headings")
        tree_puntos.heading("nombre", text="Nombre")
        tree_puntos.heading("direccion", text="Dirección")
        tree_puntos.heading("escritorios", text="Escritorios")
        tree_puntos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Llenar puntos
        for punto in empresa.puntos_atencion:
            tree_puntos.insert("", "end", punto.id, values=(punto.nombre, punto.direccion, str(len(punto.escritorios))))
        
        # Pestaña de transacciones
        tab_trans = ttk.Frame(notebook)
        notebook.add(tab_trans, text="Transacciones")
        
        # Treeview para transacciones
        tree_trans = ttk.Treeview(tab_trans, columns=("nombre", "tiempo"), show="headings")
        tree_trans.heading("nombre", text="Nombre")
        tree_trans.heading("tiempo", text="Tiempo de Atención (min)")
        tree_trans.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Llenar transacciones
        for id_trans, trans in empresa.transacciones.items():
            tree_trans.insert("", "end", id_trans, values=(trans.nombre, trans.tiempo_atencion))
        
        # Botón de cerrar
        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)
    
    def crear_punto_atencion(self):
        seleccion = self.tree_empresas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa.")
            return
        
        id_empresa = seleccion[0]
        empresa = self.sistema.obtener_empresa(id_empresa)
        if not empresa:
            messagebox.showerror("Error", "La empresa seleccionada no está disponible.")
            return
        
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Crear Punto de Atención para {empresa.nombre}")
        dialog.geometry("400x200")
        dialog.grab_set()  # Modal
        
        # Campos del formulario
        ttk.Label(dialog, text="ID Punto:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        id_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=id_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        nombre_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=nombre_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(dialog, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        dir_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=dir_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Botones
        def guardar():
            id_punto = id_var.get().strip()
            nombre = nombre_var.get().strip()
            direccion = dir_var.get().strip()
            
            if not id_punto or not nombre or not direccion:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                return
            
            from modelo import PuntoAtencion
            punto = PuntoAtencion(id_punto, nombre, direccion)
            empresa.agregar_punto_atencion(punto)
            
            messagebox.showinfo("Éxito", f"Punto de atención '{nombre}' creado correctamente.", parent=dialog)
            dialog.destroy()
            
            # Actualizar árbol de empresas
            num_puntos = len(empresa.puntos_atencion)
            num_trans = len(empresa.transacciones)
            self.tree_empresas.item(id_empresa, values=(empresa.nombre, empresa.abreviatura, num_puntos, num_trans))
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=3, column=1, padx=5, pady=10)
        
        # Hacer que el grid sea expansible
        dialog.columnconfigure(1, weight=1)