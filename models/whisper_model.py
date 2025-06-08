import sys
import subprocess
from typing import Dict, Any, Optional

try:
    import whisper
except ImportError:
    print("Instalando Whisper...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
    import whisper

class WhisperModelManager:
    """Gestor del modelo Whisper"""
    
    def __init__(self):
        self.model = None
        self.current_model_name = None
    
    def load_model(self, model_name: str) -> None:
        """Carga el modelo Whisper especificado"""
        if self.model is None or self.current_model_name != model_name:
            self.model = whisper.load_model(model_name)
            self.current_model_name = model_name
    
    def transcribe(self, audio_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza la transcripción del audio"""
        if self.model is None:
            raise RuntimeError("Modelo no cargado. Llama a load_model() primero.")
        
        return self.model.transcribe(audio_path, **options)
    
    def is_loaded(self) -> bool:
        """Verifica si hay un modelo cargado"""
        return self.model is not None
    
    def get_current_model(self) -> Optional[str]:
        """Retorna el nombre del modelo actual"""
        return self.current_model_name