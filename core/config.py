import os
from pathlib import Path
from typing import Dict, List, Any

class AppConfig:
    """Gestión de configuración de la aplicación"""
    
    # Modelos disponibles de Whisper
    WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
    
    # Idiomas disponibles
    LANGUAGES = ["auto", "Spanish", "English", "French", "German", "Portuguese", "Chinese", "Japanese"]
    
    # Tareas disponibles
    TASKS = ["transcribe", "translate"]
    
    # Formatos de audio soportados
    AUDIO_FORMATS = [
        ("Archivos de Audio", "*.mp3 *.wav *.flac *.m4a *.ogg *.wma"),
        ("MP3", "*.mp3"),
        ("WAV", "*.wav"),
        ("FLAC", "*.flac"),
        ("Todos los archivos", "*.*")
    ]
    
    def __init__(self):
        self.default_output_folder = os.path.join(os.getcwd(), "transcripciones")
        self.default_model = "turbo"
        self.default_language = "auto"
        self.default_task = "transcribe"
        
        # Crear carpeta de salida por defecto
        os.makedirs(self.default_output_folder, exist_ok=True)
    
    def validate_model(self, model: str) -> bool:
        """Valida si el modelo es válido"""
        return model in self.WHISPER_MODELS
    
    def validate_language(self, language: str) -> bool:
        """Valida si el idioma es válido"""
        return language in self.LANGUAGES
    
    def validate_task(self, task: str) -> bool:
        """Valida si la tarea es válida"""
        return task in self.TASKS
    
    def validate_audio_file(self, file_path: str) -> bool:
        """Valida si el archivo de audio existe y es válido"""
        if not file_path:
            return False
        
        if not os.path.exists(file_path):
            return False
        
        # Verificar extensión
        valid_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.wma']
        file_ext = Path(file_path).suffix.lower()
        return file_ext in valid_extensions
    
    def get_transcription_options(self, language: str, task: str) -> Dict[str, Any]:
        """Genera opciones para la transcripción"""
        options = {}
        
        if language != "auto":
            options['language'] = language
        
        if task == "translate":
            options['task'] = 'translate'
        
        return options