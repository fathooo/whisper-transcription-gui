@echo off
echo Iniciando aplicacion de transcripcion Whisper...
echo.

REM Verificar si existe la carpeta venv
if exist "venv" (
    echo Entorno virtual encontrado. Activando...
    call venv\Scripts\activate.bat
) else (
    echo Entorno virtual no encontrado. Creando nuevo entorno...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Error: No se pudo crear el entorno virtual. Verifica que Python este instalado.
        pause
        exit /b 1
    )
    echo Entorno virtual creado. Activando...
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo Iniciando aplicacion GUI refactorizada...
python main.py
pause