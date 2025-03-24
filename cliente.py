from lista import Lista

class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = Lista()  # Lista de tuplas (transaccion, cantidad)
        self.tiempo_espera = 0
        self.tiempo_atencion = 0
        self.hora_llegada = 0
        self.hora_atencion = 0
    
    def agregar_transaccion(self, transaccion, cantidad):
        # Agregar una transacción al cliente
        self.transacciones.insertar((transaccion, cantidad))
    
    def calcular_tiempo_atencion(self):
        # Calcular el tiempo total de atención basado en las transacciones
        tiempo_total = 0
        for trans in self.transacciones.recorrer():
            transaccion, cantidad = trans
            tiempo_total += transaccion.tiempo_atencion * cantidad
        self.tiempo_atencion = tiempo_total
        return tiempo_total