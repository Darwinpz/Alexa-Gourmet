class User:

    def __init__(self, cedula,nombre,correo,clave,conf_clave,direccion,telefono,tipo,ciudad):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.conf_clave = conf_clave
        self.direccion = direccion
        self.telefono = telefono
        self.tipo = tipo
        self.ciudad = ciudad
    
    def validar_clave(self):
        if self.clave == self.conf_clave:
            return True

