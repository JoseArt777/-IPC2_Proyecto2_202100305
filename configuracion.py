class ConfiguracionInicial:
    def __init__(self, id, id_empresa, id_punto):
        self.id = id
        self.id_empresa = id_empresa
        self.id_punto = id_punto
        self.escritorios_activos = None  # Lista de IDs de escritorios activos
        self.clientes = None  # Lista de clientes inicial