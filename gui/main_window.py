import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.transcription import TranscriptionService
from core.config import AppConfig
from utils.threading_utils import ThreadSafeCallback, BackgroundTask

class WhisperTranscriptionGUI:
    """Interfaz gráfica para la transcripción con Whisper"""
    
    def __init__(self, root):
        self.root = root
        self.config = AppConfig()
        
        # Inicializar servicios
        self.transcription_service = TranscriptionService(self.config.default_output_folder)
        self.callback_manager = ThreadSafeCallback(root)
        self.background_task = BackgroundTask(self.callback_manager)
        
        # Variables de la interfaz
        self.audio_file = tk.StringVar()
        self.output_folder = tk.StringVar(value=self.config.default_output_folder)
        self.model_var = tk.StringVar(value=self.config.default_model)
        self.language_var = tk.StringVar(value=self.config.default_language)
        self.task_var = tk.StringVar(value=self.config.default_task)
        
        # Variable para el archivo de salida actual
        self.current_output_file = None
        
        # Configurar ventana
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("Transcriptor de Audio con Whisper")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configurar icono si es posible
        try:
            self.root.iconbitmap(default="")
        except:
            pass
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Crear widgets
        self.create_title(main_frame)
        self.create_audio_selection(main_frame)
        self.create_model_selection(main_frame)
        self.create_language_selection(main_frame)
        self.create_task_selection(main_frame)
        self.create_output_selection(main_frame)
        self.create_transcription_button(main_frame)
        self.create_progress_bar(main_frame)
        self.create_status_label(main_frame)
        self.create_results_area(main_frame)
    
    def create_title(self, parent):
        """Crea el título de la aplicación"""
        title_label = ttk.Label(parent, text="🎵 Transcriptor de Audio con Whisper", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    def create_audio_selection(self, parent):
        """Crea la sección de selección de archivo de audio"""
        ttk.Label(parent, text="Archivo de Audio:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        audio_frame = ttk.Frame(parent)
        audio_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        audio_frame.columnconfigure(0, weight=1)
        
        self.audio_entry = ttk.Entry(audio_frame, textvariable=self.audio_file, width=50)
        self.audio_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(audio_frame, text="Buscar", command=self.browse_audio_file).grid(row=0, column=1)
    
    def create_model_selection(self, parent):
        """Crea la selección de modelo Whisper"""
        ttk.Label(parent, text="Modelo Whisper:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        model_combo = ttk.Combobox(parent, textvariable=self.model_var, 
                                  values=self.config.WHISPER_MODELS,
                                  state="readonly", width=15)
        model_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
    
    def create_language_selection(self, parent):
        """Crea la selección de idioma"""
        ttk.Label(parent, text="Idioma:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        language_combo = ttk.Combobox(parent, textvariable=self.language_var,
                                     values=self.config.LANGUAGES,
                                     state="readonly", width=15)
        language_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
    
    def create_task_selection(self, parent):
        """Crea la selección de tarea"""
        ttk.Label(parent, text="Tarea:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        task_combo = ttk.Combobox(parent, textvariable=self.task_var,
                                 values=self.config.TASKS,
                                 state="readonly", width=15)
        task_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
    
    def create_output_selection(self, parent):
        """Crea la selección de carpeta de salida"""
        ttk.Label(parent, text="Carpeta de salida:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Cambiar", command=self.browse_output_folder).grid(row=0, column=1)
    
    def create_transcription_button(self, parent):
        """Crea el botón de transcripción"""
        self.transcribe_button = ttk.Button(parent, text="🎯 Iniciar Transcripción", 
                                          command=self.start_transcription, style="Accent.TButton")
        self.transcribe_button.grid(row=6, column=0, columnspan=3, pady=20)
    
    def create_progress_bar(self, parent):
        """Crea la barra de progreso"""
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
    
    def create_status_label(self, parent):
        """Crea la etiqueta de estado"""
        self.status_label = ttk.Label(parent, text="Listo para transcribir", 
                                     font=('Arial', 10))
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)
    
    def create_results_area(self, parent):
        """Crea el área de resultados"""
        results_frame = ttk.LabelFrame(parent, text="Resultados", padding="10")
        results_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        parent.rowconfigure(9, weight=1)
        
        # Text widget para mostrar transcripción
        self.result_text = tk.Text(results_frame, height=8, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Botones de resultado
        self.create_result_buttons(results_frame)
    
    def create_result_buttons(self, parent):
        """Crea los botones de resultados"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.open_file_button = ttk.Button(button_frame, text="📁 Abrir Archivo", 
                                          command=self.open_transcription_file, state="disabled")
        self.open_file_button.pack(side=tk.LEFT, padx=5)
        
        self.open_folder_button = ttk.Button(button_frame, text="📂 Abrir Carpeta", 
                                           command=self.open_output_folder, state="disabled")
        self.open_folder_button.pack(side=tk.LEFT, padx=5)
    
    def browse_audio_file(self):
        """Abre el diálogo para seleccionar archivo de audio"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=self.config.AUDIO_FORMATS
        )
        if filename:
            self.audio_file.set(filename)
    
    def browse_output_folder(self):
        """Abre el diálogo para seleccionar carpeta de salida"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder:
            self.output_folder.set(folder)
            self.transcription_service.set_output_folder(folder)
    
    def update_status(self, message: str):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_transcription(self):
        """Inicia el proceso de transcripción"""
        if self.background_task.is_running():
            return
        
        # Actualizar carpeta de salida si cambió
        self.transcription_service.set_output_folder(self.output_folder.get())
        
        # Preparar UI para transcripción
        self.transcribe_button.config(state="disabled")
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        self.open_file_button.config(state="disabled")
        self.open_folder_button.config(state="disabled")
        
        # Crear función de transcripción
        def transcribe_task(progress_callback):
            return self.transcription_service.transcribe_audio(
                audio_file=self.audio_file.get(),
                model=self.model_var.get(),
                language=self.language_var.get(),
                task=self.task_var.get(),
                progress_callback=progress_callback
            )
        
        # Ejecutar en segundo plano
        self.background_task.run_async(
            task_func=transcribe_task,
            on_success=self.on_transcription_success,
            on_error=self.on_transcription_error,
            on_progress=self.update_status
        )
    
    def on_transcription_success(self, result):
        """Maneja el éxito de la transcripción"""
        # Actualizar UI
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result['transcription'])
        
        # Guardar archivo actual
        self.current_output_file = result['output_file']
        
        # Rehabilitar controles
        self.progress.stop()
        self.transcribe_button.config(state="normal")
        self.open_file_button.config(state="normal")
        self.open_folder_button.config(state="normal")
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", 
                           f"Transcripción completada exitosamente.\n\nArchivo guardado en:\n{self.current_output_file}")
    
    def on_transcription_error(self, error):
        """Maneja errores en la transcripción"""
        # Rehabilitar controles
        self.progress.stop()
        self.transcribe_button.config(state="normal")
        self.update_status("Error en la transcripción")
        
        # Mostrar error
        messagebox.showerror("Error", str(error))
    
    def open_transcription_file(self):
        """Abre el archivo de transcripción actual"""
        if not self.current_output_file:
            messagebox.showerror("Error", "No hay archivo de transcripción disponible")
            return
        
        success = self.transcription_service.open_transcription_file(self.current_output_file)
        if not success:
            messagebox.showerror("Error", "No se pudo abrir el archivo de transcripción")
    
    def open_output_folder(self):
        """Abre la carpeta de salida"""
        success = self.transcription_service.open_output_folder()
        if not success:
            messagebox.showerror("Error", "No se pudo abrir la carpeta de salida")