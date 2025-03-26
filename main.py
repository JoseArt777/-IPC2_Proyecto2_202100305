#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proyecto 2 - Sistema de Atención al Cliente
Universidad San Carlos de Guatemala
Facultad de Ingeniería
Escuela de Ciencias y Sistemas
Introducción a la Programación y Computación 2
"""

import os
import sys
from models.sistema import Sistema
from controllers.xml_controller import XMLController
from views.main_window import MainWindow

def main():
    """
    Función principal del programa.
    """
    # Inicializar el sistema
    sistema = Sistema()
    xml_controller = XMLController(sistema)
    
    # Crear y mostrar la ventana principal
    ventana = MainWindow(sistema, xml_controller)
    ventana.iniciar()

if __name__ == "__main__":
    main()