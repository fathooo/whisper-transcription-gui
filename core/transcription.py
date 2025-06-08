from typing import Dict, Any, Callable, Optional
from models.whisper_model import WhisperModelManager
from core.file_manager import FileManager
from core.config import AppConfig

class TranscriptionService:
    """Servicio principal de transcripción"""
    
    def __init__(self, output_folder: str):
        self.config = AppConfig()
        self.whisper_manager = WhisperModelManager()
        self.file_manager = FileManager(output_folder)
    
    def set_output_folder(self, folder_path: str) -> None:
        """Cambia la carpeta de salida"""
        self.file_manager.set_output_folder(folder_path)
    
    def validate_inputs(self, 
                       audio_file: str, 
                       model: str, 
                       language: str, 
                       task: str) -> tuple[bool, str]:
        """
        Valida todas las entradas del usuario
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        if not audio_file:
            return False, "Por favor selecciona un archivo de audio"
        
        if not self.config.validate_audio_file(audio_file):
            return False, "El archivo de audio no existe o no es válido"
        
        if not self.config.validate_model(model):
            return False, f"Modelo inválido: {model}"
        
        if not self.config.validate_language(language):
            return False, f"Idioma inválido: {language}"
        
        if not self.config.validate_task(task):
            return False, f"Tarea inválida: {task}"
        
        return True, ""
    
    def transcribe_audio(self,
                        audio_file: str,
                        model: str,
                        language: str,
                        task: str,
                        progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """
        Realiza la transcripción completa del audio
        
        Args:
            audio_file: Ruta del archivo de audio
            model: Modelo Whisper a usar
            language: Idioma del audio
            task: Tarea (transcribe/translate)
            progress_callback: Callback para reportar progreso
        
        Returns:
            Dict con el resultado y la ruta del archivo guardado
        """
        
        # Validar entradas
        is_valid, error_msg = self.validate_inputs(audio_file, model, language, task)
        if not is_valid:
            raise ValueError(error_msg)
        
        try:
            # Reportar progreso: Cargando modelo
            if progress_callback:
                progress_callback("Cargando modelo Whisper...")
            
            # Cargar modelo
            self.whisper_manager.load_model(model)
            
            # Reportar progreso: Procesando
            if progress_callback:
                progress_callback("Procesando audio...")
            
            # Configurar opciones de transcripción
            options = self.config.get_transcription_options(language, task)
            
            # Realizar transcripción
            result = self.whisper_manager.transcribe(audio_file, options)
            
            # Reportar progreso: Guardando
            if progress_callback:
                progress_callback("Guardando transcripción...")
            
            # Guardar archivo
            output_file_path = self.file_manager.save_transcription(
                result, audio_file, model, language, task
            )
            
            # Reportar progreso: Completado
            if progress_callback:
                progress_callback(f"Transcripción completada. Archivo guardado en: {output_file_path}")
            
            return {
                'transcription': result["text"],
                'segments': result.get("segments", []),
                'output_file': output_file_path,
                'full_result': result
            }
            
        except Exception as e:
            error_msg = f"Error durante la transcripción: {str(e)}"
            raise RuntimeError(error_msg)
    
    def open_transcription_file(self, file_path: str) -> bool:
        """Abre el archivo de transcripción"""
        return self.file_manager.open_file(file_path)
    
    def open_output_folder(self) -> bool:
        """Abre la carpeta de salida"""
        return self.file_manager.open_folder(self.file_manager.output_folder)