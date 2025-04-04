import sys
import os

# se agrega la ruta del directorio actual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from interfaz_grafica import VentanaPrincipal

def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
