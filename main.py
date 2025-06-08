import sys
import os
import tkinter as tk

# Agregar el directorio actual al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import WhisperTranscriptionGUI

def main():
    """Función principal de la aplicación"""
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Crear aplicación
        app = WhisperTranscriptionGUI(root)
        
        # Iniciar loop principal
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()