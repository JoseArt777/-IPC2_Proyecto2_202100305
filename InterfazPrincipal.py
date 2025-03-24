import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InterfazPrincipal:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.xml_controller = None  # Se debe asignar desde main con XMLController(sistema)

        self.root.title("Sistema de Atención al Cliente")
        self.root.geometry("600x500")

        self.crear_widgets()

    def crear_widgets(self):
        # --- Botones de carga ---
        tk.Button(self.root, text="Cargar Configuración XML", command=self.cargar_config_xml).pack(pady=5)
        tk.Button(self.root, text="Cargar Configuración Inicial", command=self.cargar_config_inicial).pack(pady=5)

        # --- Selección Empresa y Punto ---
        self.empresa_id_entry = self._crear_input("ID Empresa")
        tk.Button(self.root, text="Seleccionar Empresa", command=self.seleccionar_empresa).pack(pady=2)

        self.punto_id_entry = self._crear_input("ID Punto Atención")
        tk.Button(self.root, text="Seleccionar Punto Atención", command=self.seleccionar_punto).pack(pady=2)

        # --- Operaciones ---
        self.escritorio_id_entry = self._crear_input("ID Escritorio")
        tk.Button(self.root, text="Activar Escritorio", command=self.activar_escritorio).pack(pady=2)
        tk.Button(self.root, text="Desactivar Escritorio", command=self.desactivar_escritorio).pack(pady=2)

        tk.Button(self.root, text="Atender Cliente", command=self.atender_cliente).pack(pady=5)
        tk.Button(self.root, text="Ver Estado Punto", command=self.ver_estado_punto).pack(pady=5)

        # --- Resultados ---
        self.text_area = tk.Text(self.root, height=15, width=70)
        self.text_area.pack(pady=10)

    def _crear_input(self, label):
        tk.Label(self.root, text=label).pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    # ----------- Funciones XML -----------
    def cargar_config_xml(self):
        archivo = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if archivo:
            try:
                self.xml_controller.cargar_configuracion(archivo)
                messagebox.showinfo("Éxito", "Archivo de configuración cargado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def cargar_config_inicial(self):
        archivo = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if archivo:
            try:
                self.xml_controller.cargar_config_inicial(archivo)
                messagebox.showinfo("Éxito", "Configuración inicial cargada.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar: {e}")

    # ----------- Funciones de sistema -----------
    def seleccionar_empresa(self):
        id_empresa = self.empresa_id_entry.get()
        if self.sistema.seleccionar_empresa(id_empresa):
            messagebox.showinfo("Empresa", "Empresa seleccionada.")
        else:
            messagebox.showwarning("Error", "Empresa no encontrada.")

    def seleccionar_punto(self):
        id_punto = self.punto_id_entry.get()
        if self.sistema.seleccionar_punto(id_punto):
            messagebox.showinfo("Punto", "Punto de atención seleccionado.")
        else:
            messagebox.showwarning("Error", "Punto no encontrado.")

    def activar_escritorio(self):
        id_escritorio = self.escritorio_id_entry.get()
        if self.sistema.activar_escritorio(id_escritorio):
            messagebox.showinfo("Escritorio", "Escritorio activado.")
        else:
            messagebox.showwarning("Error", "No se pudo activar escritorio.")

    def desactivar_escritorio(self):
        id_escritorio = self.escritorio_id_entry.get()
        if self.sistema.desactivar_escritorio(id_escritorio):
            messagebox.showinfo("Escritorio", "Escritorio desactivado.")
        else:
            messagebox.showwarning("Error", "No se pudo desactivar escritorio.")

    def atender_cliente(self):
        self.sistema.atender_cliente()
        messagebox.showinfo("Cliente", "Atención procesada.")

    def ver_estado_punto(self):
        estado = self.sistema.ver_estado_punto()
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, str(estado))

