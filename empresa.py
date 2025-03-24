from lista import Lista

class Empresa:
    def __init__(self, id, nombre, abreviatura):
        self.id = id
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = Lista()  # Lista de puntos de atención
        self.transacciones = Lista()    # Lista de transacciones
    
    def agregar_punto_atencion(self, punto_atencion):
        # Agregar punto de atención a la lista
        self.puntos_atencion.insertar(punto_atencion)
    
    def agregar_transaccion(self, transaccion):
        # Agregar transacción a la lista
        self.transacciones.insertar(transaccion)
    
    def buscar_punto_atencion(self, id_punto):
        # Buscar y retornar un punto de atención por ID
        return self.puntos_atencion.buscar(lambda p: p.id == id_punto)
    
    def buscar_transaccion(self, id_transaccion):
        # Buscar y retornar una transacción por ID
        return self.transacciones.buscar(lambda t: t.id == id_transaccion)