import subprocess
import time
import asyncio
import httpx
import os
from dotenv import load_dotenv
from backend.utils.parameters_processor2 import ParameterProcessor

"""
async def get_status():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/get_status")
        return response.json()

async def get_parameters():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/get_params")
        return response.json()
"""

async def wait_for_parameters():

    GET_PARAMS_URL = "http://localhost:5000/get_params"

    while True:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(GET_PARAMS_URL, timeout=5.0)
                response.raise_for_status()
                parameters = response.json()

                if "message" in parameters:
                    print("No se han recibido parámetros aún.")
                else:
                    print(f"Parameters received: {parameters}")

                    # Crear una instancia de ParameterProcessor
                    load_dotenv()
                    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
                    processor = ParameterProcessor(parameters, OPENAI_API_KEY)

                    # Llamar al método asíncrono `process` para procesar los parámetroscls
                    await processor.process_parameters()
                
                await asyncio.sleep(1)  # Espera antes de la próxima verificación

            except httpx.RequestError as e:
                #pass
                print(f"Error al conectar con el servidor: {e}")


    """
    Verifica continuamente el estado y recibe parámetros solo cuando el estado cambia a 'ready'.
    while True:
        status = await get_status()
        current_status = status.get("status")

        # Solo obtiene e imprime parámetros cuando el estado cambia a "ready"
        if current_status != "awaiting":
            parameters = await get_parameters()
            print(f"Parameters received: {parameters}")

            # Crear una instancia de ParameterProcessor
            OPENAI_API_KEY = 
            processor = ParameterProcessor(parameters, OPENAI_API_KEY)

            # Llamar al método asíncrono `process` para procesar los parámetros
            await processor.process_parameters()
        
        await asyncio.sleep(1)  # Espera antes de la próxima verificación
    """

async def main_async():
    # Ejecuta la función que espera los parámetros en un ciclo continuo
    await wait_for_parameters()

def main():
    # Inicia el servicio de API usando Uvicorn en un subproceso
    print("Starting API service with Uvicorn...")
    api_process = subprocess.Popen(
        ["uvicorn", "src.backend.endpoints.parameters_api:app", "--reload", "--host", "localhost", "--port", "5000"]#, "--log-level", "warning"]
    )
    time.sleep(1)  # Pausa para dar tiempo a que la API se inicialice

    # Inicia el frontend de Streamlit en un subproceso
    # print("Starting Streamlit frontend...")
    # frontend_process = subprocess.Popen(["streamlit", "run", "src/frontend/app.py"])

    try:
        # Ejecuta la función principal asíncrona
        asyncio.run(main_async())
        
    except KeyboardInterrupt:
        print("\nManual shutdown requested.")
    finally:
        # Termina ambos procesos al final o en caso de error
        print("Shutting down services...")
        api_process.terminate()
        #frontend_process.terminate()

if __name__ == "__main__":
    main()
