# Sistema de Atención a Clientes Empresariales – Proyecto académico -IPC2_Proyecto2_202100305

## Descripción del Proyecto

Este software implementa un sistema de atención a clientes para empresas, basado en procesamiento de datos estructurados y simulación de puntos de atención. Permite gestionar empresas, puntos de servicio, escritorios, transacciones y flujo de clientes, optimizando recursos y automatizando reportes estadísticos. El sistema resuelve la problemática de organizar y monitorear múltiples servicios empresariales, facilitando la simulación y análisis en ambientes administrativos y educativos.

## Características Principales

- Carga de configuración empresarial desde archivos XML.
- Gestión de empresas, puntos de atención y escritorios para atención a clientes.
- Simulación del flujo de clientes y manejo de transacciones.
- Reportes estadísticos y visualización de información relevante por escritorio y punto de servicio.
- Generación y exportación de tablas y gráficos usando Graphviz e imágenes.
- Interfaz gráfica intuitiva en Python (Tkinter) con organización en pestañas.

## Tecnologías Utilizadas

- **Lenguaje Principal:** Python
- **Framework/Librerías:** Tkinter (interfaz gráfica), PIL (imágenes), Graphviz (visualización), ElementTree (XML), módulos estándares de Python
- **Estructuras de datos:** Listas enlazadas, pilas, colas, tablas hash (implementadas manualmente)
- **Persistencia:** Archivos XML para configuración y datos iniciales

## Requisitos Previos

- Python 3.7 o superior instalado.
- Instalación de librerías necesarias:
  ```bash
  pip install pillow graphviz
  ```
- Graphviz instalado en el sistema para generación de gráficos.
- Archivos XML de configuración y datos iniciales, según la estructura del proyecto.

## Instrucciones de Instalación y Ejecución

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/JoseArt777/-IPC2_Proyecto2_202100305.git
   ```
2. **Accede al directorio del proyecto**
   ```bash
   cd 'SOLUCIONES S.A'
   ```
3. **Ejecuta el sistema**
   ```bash
   python main.py
   ```
4. **Carga los archivos XML de configuración y empieza a gestionar empresas y puntos de atención desde la interfaz gráfica.**

## Estructura del Proyecto

- `main.py`: Archivo principal para iniciar el sistema.
- `interfaz_grafica.py`: Lógica de la interfaz gráfica con Tkinter.
- `procesador_xml.py`: Carga y validación de archivos XML de configuración.
- `sistema.py`: Lógica central de todas las operaciones del sistema.
- `modelo/`: Modelos de entidades (Empresa, PuntoAtención, EscritorioServicio, Transacción, Cliente).
- `estructuras/`: Implementaciones propias de estructuras de datos (Listas enlazadas, pilas, colas, tablas hash).
- Archivos XML: Configuración inicial y operativa del sistema.

## Endpoints

Este proyecto no expone endpoints ni APIs web. Toda la interacción se realiza de forma local mediante la interfaz gráfica.

## Capturas o Ejemplos de Uso

```python
# Inicialización y ejecución del sistema de atención
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
```

```python
# Ejemplo de carga de configuración empresarial desde XML
procesador = ProcesadorXML(sistema)
ok, mensaje = procesador.cargar_configuracion('configuracion_empresas.xml')
print(mensaje)
```

## Buenas Prácticas Implementadas

- Separación por módulos (UI, lógica, procesamiento de datos, modelos).
- Implementación clara y bien documentada de estructuras de datos.
- Validación extensiva de archivos XML y estados del sistema.
- Gestión eficiente de recursos y errores en la interfaz gráfica.
- Uso de convenciones y patrones estándar de Python.

## Aprendizajes Obtenidos

El desarrollo permitió aplicar conocimientos en programación orientada a objetos, diseño e implementación manual de estructuras de datos, manejo y validación de archivos XML, y construcción de interfaces gráficas profesionales. Se reforzaron competencias en simulación de sistemas empresariales y automatización de reportes estadísticos.

## Posibles Mejoras Futuras

- Incorporar persistencia avanzada (bases de datos relacionales o archivos JSON).
- Implementar funcionalidades multiusuario y control de acceso.
- Extender reportes y visualizaciones exportables.
- Agregar funciones de simulación de casos en tiempo real y exportación de resultados.
- Mejorar la experiencia de usuario con más opciones gráficas e interacción.

---
Consulta detalles y código fuente en el [repositorio GitHub](https://github.com/JoseArt777/-IPC2_Proyecto2_202100305).
