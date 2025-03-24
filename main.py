import tkinter as tk
from sistema_controller import SistemaController
from xml_controller import XMLController
from InterfazPrincipal import InterfazPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    sistema = SistemaController()
    app = InterfazPrincipal(root, sistema)
    app.xml_controller = XMLController(sistema)
    root.mainloop()
