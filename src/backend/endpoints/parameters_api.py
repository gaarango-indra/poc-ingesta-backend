from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, RootModel
from typing import Optional, Any, Dict

app = FastAPI()
all_parameters_received = 0
collected_parameters = {}
user_parameters = {}

class DataModel(BaseModel):
    key: str
    value: str

@app.post("/post_parameters")
async def post_parameters(data: DataModel):
    '''FrontEnd send botons parameters. 
    Example: requests.post(uri, json={"key": "process_type", "value": value})
    Used for send:
     * json={"key": "process_type", "value": value} // process_type.py
     * json={"key": "ingest_type", "value": value} // ingest_type.py
     * json={"key": "folder_path", "value": value} // folder_selector.py
     * json={"key": "schema_file_path", "value": value} // schema_file_selector.py
     * json={"key": "data_sample_file_path", "value": value} // sample_data_file_selector.py
    '''
    collected_parameters[data.key] = data.value
    return {"status": "success", "message": f"Dato {data.key} recibido."}

@app.get("/get_parameters")
async def get_parameters():
    global all_parameters_received
    ingest_parameters = {**user_parameters.model_dump(), **collected_parameters}
    if all_parameters_received:
        all_parameters_received = False
        return ingest_parameters
    else:
        raise HTTPException(status_code=400, detail="Parameters not ready yet")

class UserParameters(BaseModel):
    castmode: Optional[str] = "notPermissive"
    input_mode: Optional[str] = "FAILFAST"
    input_path: str
    code_schema: Optional[str] = "co"
    reprocess_status: bool

@app.post("/post_user_parameters")
async def post_user_parameters(params: UserParameters):
    '''FrontEnd send form parameters {Dict}.                            # Valores para probar
        castmode": castmode,                            #Optional       #'notPermissive'
        "input_mode": input_mode,                       #Optional       #'FAILFAST'
        "input_path": input_path,                                       #/src/data/raw
        "code_schema": code_schema,                     #Optional       #co
        "reprocess_status": reprocess_status                            #True
    '''
    global user_parameters
    user_parameters = params
    response_data = {
        "message": "Datos recibidos correctamente",
        "received_data": params.model_dump()
    }
    return response_data

@app.get("/get_user_parameters")
async def get_user_parameters():
    return {"status": "success", "user_parameters": user_parameters.model_dump()}

# Definir el modelo de datos para la solicitud POST
class StatusFlag(BaseModel):
    flag: bool

@app.post("/post_status")
async def post_status(status: StatusFlag):
    '''
    FrontEnd send start signal. Triggers the creation of folders and files
    Use True (bool)
    '''
    global all_parameters_received
    all_parameters_received = status.flag
    return {"status": "all_parameters_received set", "new_value": all_parameters_received}

@app.get("/get_status")
async def get_status():
    # Devuelve el estado de si todos los parámetros han sido recibidos
    if all_parameters_received:
        return {"status": "ready"}
    else:
        return {"status": "waiting"}
    
class FrontParams(RootModel[dict]):
    pass
    # Ajustar según la estructura esperada de params
    # castmode: str
    # code_schema: str
    # folder_path: str
    # data_sample_file_path: str
    # schema_file_path: str
    # input_mode: str
    # input_path: str
    # process_type: str
    # O bien, si es dinámico o muy variable, puedes representarlo genéricamente:
    # __root__: Dict[str, Any]


# Variable global para almacenar los parámetros recibidos por /run_process
last_received_params = None

@app.post("/run_process")
def run_process(params: FrontParams):
    global last_received_params
    print(f"Parámetros recibidos por la API")
    try:
        # Convertir a diccionario
        params_dict = params.model_dump()
        print(f"Params recibidos en API. {params_dict}")
        # Guardar globalmente
        last_received_params = params_dict
        return {"status": "ready"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get_params")
def get_params():
    global last_received_params
    if last_received_params is not None:
        # Guardar los parámetros actuales en una variable temporal
        returned_params = last_received_params
        # Resetear la variable a None
        last_received_params = None
        # Devolver los parámetros recuperados
        return returned_params
    else:
        return {"message": "Awaiting"}
