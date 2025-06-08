import os
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

class FileManager:
    """Gestor de archivos para transcripciones"""
    
    def __init__(self, output_folder: str):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def set_output_folder(self, folder_path: str) -> None:
        """Establece la carpeta de salida"""
        self.output_folder = folder_path
        os.makedirs(folder_path, exist_ok=True)
    
    def generate_output_filename(self, audio_file_path: str) -> str:
        """Genera un nombre único para el archivo de transcripción"""
        audio_filename = Path(audio_file_path).stem
        timestamp = int(time.time())
        output_filename = f"{audio_filename}_transcripcion_{timestamp}.txt"
        return os.path.join(self.output_folder, output_filename)
    
    def save_transcription(self, 
                          result: Dict[str, Any], 
                          audio_file_path: str,
                          model_name: str,
                          language: str,
                          task: str) -> str:
        """Guarda la transcripción en un archivo"""
        
        output_file_path = self.generate_output_filename(audio_file_path)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            # Escribir encabezado
            f.write("=== TRANSCRIPCIÓN DE AUDIO ===\n")
            f.write(f"Archivo: {os.path.basename(audio_file_path)}\n")
            f.write(f"Modelo: {model_name}\n")
            f.write(f"Idioma: {language}\n")
            f.write(f"Tarea: {task}\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Escribir texto completo
            f.write(result["text"])
            
            # Escribir segmentos detallados
            f.write("\n\n=== SEGMENTOS DETALLADOS ===\n")
            for segment in result.get("segments", []):
                start_time = segment.get("start", 0)
                end_time = segment.get("end", 0)
                text = segment.get("text", "")
                f.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")
        
        return output_file_path
    
    def open_file(self, file_path: str) -> bool:
        """Abre un archivo con la aplicación predeterminada del sistema"""
        try:
            if not os.path.exists(file_path):
                return False
            
            if sys.platform.startswith('win'):
                os.startfile(file_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
            
            return True
        except Exception:
            return False
    
    def open_folder(self, folder_path: str) -> bool:
        """Abre una carpeta con el explorador de archivos"""
        try:
            if not os.path.exists(folder_path):
                return False
            
            if sys.platform.startswith('win'):
                os.startfile(folder_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', folder_path])
            else:
                subprocess.run(['xdg-open', folder_path])
            
            return True
        except Exception:
            return False