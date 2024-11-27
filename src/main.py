import subprocess
import time
import asyncio
import httpx
import os
from backend.utils.parameters_processor import ParameterProcessor

async def get_status():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/get_status")
        return response.json()

async def get_parameters():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/get_parameters")
        return response.json()

async def wait_for_parameters():
    """Verifica continuamente el estado y recibe parámetros solo cuando el estado cambia a 'ready'."""
    while True:
        status = await get_status()
        current_status = status.get("status")

        # Solo obtiene e imprime parámetros cuando el estado cambia a "ready"
        if current_status == "ready":
            parameters = await get_parameters()
            print(f"Parameters received: {parameters}")

            # Crear una instancia de ParameterProcessor
            OPENAI_API_KEY = "a2b9bd7e7e234582b5c866e97802e3e1"
            processor = ParameterProcessor(parameters, OPENAI_API_KEY)

            # Llamar al método asíncrono `process` para procesar los parámetros
            await processor.process_parameters()
        
        await asyncio.sleep(1)  # Espera antes de la próxima verificación

async def main_async():
    # Ejecuta la función que espera los parámetros en un ciclo continuo
    await wait_for_parameters()

def main():
    # Inicia el servicio de API usando Uvicorn en un subproceso
    print("Starting API service with Uvicorn...")
    api_process = subprocess.Popen(
        ["uvicorn", "src.backend.endpoints.parameters_api:app", "--reload"]#, "--log-level", "warning"]
    )
    time.sleep(1)  # Pausa para dar tiempo a que la API se inicialice

    # Inicia el frontend de Streamlit en un subproceso
    print("Starting Streamlit frontend...")
    frontend_process = subprocess.Popen(["streamlit", "run", "src/frontend/app.py"])

    try:
        # Ejecuta la función principal asíncrona
        asyncio.run(main_async())
        
    except KeyboardInterrupt:
        print("\nManual shutdown requested.")
    finally:
        # Termina ambos procesos al final o en caso de error
        print("Shutting down services...")
        api_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
