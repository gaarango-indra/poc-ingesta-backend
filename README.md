# Project Name

Este es un proyecto en Python que incluye un frontend web construido con Streamlit, una API para comunicar el frontend y el backend, y generación de carpetas y archivos basada en un archivo `.schema` inicial. La aplicación también genera archivos `.conf` usando LangChain con OpenAI y cuenta con pruebas automatizadas para garantizar su funcionalidad.

## Tabla de Contenidos
- [Project Name](#project-name)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Requisitos](#requisitos)
  - [Configuración del Entorno](#configuración-del-entorno)
  - [Ejecución del Proyecto](#ejecución-del-proyecto)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Pruebas](#pruebas)

## Requisitos

Asegúrate de tener instalado Python 3.8 o superior y `pip`. Si no tienes `pip`, puedes instalarlo desde [aquí](https://pip.pypa.io/en/stable/installation/).

## Configuración del Entorno

1. **Clonar el repositorio**

   Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio

2. **Crear un entorno virtual**
   
   Crea un entorno virtual para aislar las dependencias del proyecto:

   ```bash 
   python -m venv venv

3. **Activar el entorno virtual**
   
* **En Windows:**
  
  ```bash
  venv\Scripts\activate

* **En macOS y Linux:**
  
  ```bash
  source venv/bin/activate

4. **Instalar dependencias**

   Una vez activado el entorno virtual, instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt

5. **Configurar la API Key de OpenAI**
   
   Para usar LangChain con OpenAI, necesitas configurar tu API Key de OpenAI. Crea un archivo .env en la raíz del proyecto y agrega tu API Key de la siguiente manera:

   ```bash
   OPENAI_API_KEY=tu_api_key_aqui

## Ejecución del Proyecto

Para iniciar la aplicación completa, es necesario ejecutar tanto el backend (API) como el frontend en paralelo.

1. **Iniciar la API (Backend)**

   En una terminal, inicia el servicio de API:

   ```bash
   uvicorn src.api.api_service:app --reload

   Esto iniciará el backend en http://localhost:8000.

2. **Iniciar el Frontend**

   En una nueva terminal, ejecuta la aplicación Streamlit:

   ```bash
   streamlit run src/frontend/app_frontend.py

   Esto abrirá el frontend en tu navegador en http://localhost:8501.

## Estructura del Proyecto

project_name/
├── src/
│   ├── main.py                     # Archivo principal para iniciar la aplicación.
│   ├── api/
│   │   ├── api_service.py           # Servicio de API para la comunicación Frontend-Backend.
│   ├── frontend/
│   │   ├── app_frontend.py          # Aplicación Streamlit.
│   ├── config/
│   │   ├── config_template.json     # Plantilla de archivo .conf.
│   │   ├── schema_template.json     # Plantilla de archivo JSON.
│   ├── schema/
│   │   ├── initial_schema.schema    # Archivo de esquema inicial (formato JSON).
│   ├── utils/
│   │   ├── folder_generator.py      # Lógica para lectura y creación de carpetas desde el archivo .schema.
│   │   ├── schema_reader.py         # Lee el esquema disponible en la carpeta schema.
│   │   ├── file_writer.py           # Lógica para escribir archivos .schema y JSON.
│   ├── openai_langchain/
│   │   ├── conf_generator.py        # Generación de archivos .conf usando LangChain.
│   └── tests/
│       ├── test_api.py              # Tests para API.
│       ├── test_folder_generator.py # Tests para la creación de carpetas y archivos.
│       ├── test_conf_generator.py   # Tests para la generación de archivos .conf.
├── requirements.txt                 # Librerías necesarias.
├── README.md                        # Documentación general del proyecto.
└── .gitignore

## Pruebas

El proyecto incluye pruebas automatizadas para asegurar la funcionalidad de los módulos críticos.

1. **Ejecutar todas las pruebas**

   Ejecuta las pruebas con pytest:

   ```bash
   pytest src/tests/

2. **Pruebas individuales**

   Puedes ejecutar archivos de prueba específicos, por ejemplo, para la API:

   ```bash
   pytest src/tests/test_api.py

**Nota: Asegúrate de que el entorno virtual esté activado y las dependencias instaladas antes de ejecutar las pruebas.**
