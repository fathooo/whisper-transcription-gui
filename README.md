# Transcriptor de Audio con Whisper

## Descripción
Aplicación de escritorio con interfaz gráfica para transcribir archivos de audio usando OpenAI Whisper.

## Características
- Interfaz gráfica intuitiva
- Soporte para múltiples formatos de audio (MP3, WAV, FLAC, M4A, etc.)
- Selección de diferentes modelos Whisper (tiny, base, small, medium, large, turbo)
- Transcripción y traducción automática
- Detección automática de idioma
- Guardado automático de transcripciones
- Acceso directo a archivos y carpetas de resultado

## Instalación y Uso

### Método 1: Automático (Recomendado)
1. Descarga todos los archivos del proyecto
2. Haz doble clic en `run.bat`
3. El script automáticamente:
   - Creará un entorno virtual Python si no existe
   - Instalará todas las dependencias necesarias
   - Iniciará la aplicación

### Método 2: Manual
1. Crear entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activar entorno virtual:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar aplicación:
   ```bash
   python main.py
   ```

## Requisitos del Sistema
- Python 3.8 o superior
- FFmpeg instalado en el sistema
- Al menos 2GB de RAM (recomendado 8GB para modelos grandes)
- Conexión a internet para la primera descarga de modelos

## Modelos Disponibles
- **tiny**: Más rápido, menor precisión (~1GB RAM)
- **base**: Balance entre velocidad y precisión (~1GB RAM)
- **small**: Buena precisión general (~2GB RAM)
- **medium**: Alta precisión (~5GB RAM)
- **large**: Máxima precisión (~10GB RAM)
- **turbo**: Optimizado para velocidad (~6GB RAM)

## Formatos de Audio Soportados
- MP3, WAV, FLAC, M4A, OGG, WMA
- Y cualquier formato soportado por FFmpeg

## Funcionalidades
- **Transcripción**: Convierte audio a texto en el mismo idioma
- **Traducción**: Convierte audio a texto y traduce al inglés
- **Detección automática**: Identifica el idioma automáticamente
- **Segmentación temporal**: Guarda marcas de tiempo para cada segmento

## Estructura de Archivos de Salida
Los archivos de transcripción incluyen:
- Información del archivo procesado
- Configuración utilizada
- Texto completo de la transcripción
- Segmentos detallados con marcas de tiempo

## Solución de Problemas

### Error de FFmpeg
Si aparece error relacionado con FFmpeg:
- Windows: Instalar desde https://ffmpeg.org/download.html
- Mac: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`

### Error de memoria
Si el modelo es muy grande para tu sistema:
- Usa un modelo más pequeño (tiny, base, small)
- Cierra otras aplicaciones que consuman memoria
- Considera usar el modelo turbo para mejor balance

### Error de instalación de dependencias
- Asegúrate de tener Python 3.8 o superior
- Actualiza pip: `pip install --upgrade pip`
- En Windows, puede requerir Visual Studio Build Tools

## Consejos de Uso
1. Para mejor precisión, usa modelos más grandes
2. Para audio en inglés, considera usar modelos .en específicos
3. Especifica el idioma manualmente si la detección automática falla
4. La calidad del audio afecta significativamente la precisión
5. Los archivos muy largos pueden tomar tiempo considerable

## Licencia
Este proyecto utiliza OpenAI Whisper.

## requirements.txt
- openai-whisper>=20231117
- torch>=1.10.0
- torchaudio>=0.10.0
- numpy>=1.21.0
- ffmpeg-python>=0.2.0
