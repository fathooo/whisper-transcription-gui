import threading
import functools
from typing import Callable, Any

class ThreadSafeCallback:
    """Wrapper para callbacks thread-safe con tkinter"""
    
    def __init__(self, root):
        self.root = root
    
    def run_in_main_thread(self, callback: Callable, *args, **kwargs):
        """Ejecuta un callback en el hilo principal de la GUI"""
        self.root.after(0, callback, *args, **kwargs)
    
    def create_safe_callback(self, callback: Callable) -> Callable:
        """Crea un callback thread-safe"""
        @functools.wraps(callback)
        def safe_callback(*args, **kwargs):
            self.run_in_main_thread(callback, *args, **kwargs)
        return safe_callback

class BackgroundTask:
    """Ejecutor de tareas en segundo plano"""
    
    def __init__(self, callback_manager: ThreadSafeCallback):
        self.callback_manager = callback_manager
        self.current_thread = None
    
    def run_async(self, 
                  task_func: Callable,
                  on_success: Callable = None,
                  on_error: Callable = None,
                  on_progress: Callable = None):
        """
        Ejecuta una tarea en segundo plano
        
        Args:
            task_func: Función a ejecutar
            on_success: Callback para éxito (recibe el resultado)
            on_error: Callback para error (recibe la excepción)
            on_progress: Callback para progreso (recibe mensaje)
        """
        def worker():
            try:
                # Ejecutar callback de progreso si existe
                if on_progress:
                    progress_callback = self.callback_manager.create_safe_callback(on_progress)
                    
                    # Pasar callback de progreso a la función si lo acepta
                    import inspect
                    sig = inspect.signature(task_func)
                    if 'progress_callback' in sig.parameters:
                        result = task_func(progress_callback=progress_callback)
                    else:
                        result = task_func()
                else:
                    result = task_func()
                
                # Ejecutar callback de éxito en el hilo principal
                if on_success:
                    self.callback_manager.run_in_main_thread(on_success, result)
                    
            except Exception as e:
                # Ejecutar callback de error en el hilo principal
                if on_error:
                    self.callback_manager.run_in_main_thread(on_error, e)
        
        # Iniciar hilo
        self.current_thread = threading.Thread(target=worker, daemon=True)
        self.current_thread.start()
    
    def is_running(self) -> bool:
        """Verifica si hay una tarea ejecutándose"""
        return self.current_thread is not None and self.current_thread.is_alive()