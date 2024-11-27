from langchain_openai.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain_openai.llms import AzureOpenAI
from langchain.agents import initialize_agent, Tool
import json

class AIConfGenerator:

    def __init__(self, api_key: str):
        self.client = AzureChatOpenAI(
            openai_api_key=api_key,
            azure_endpoint = 'https://oai-mnst-ariadna-dev-01.openai.azure.com/',
            api_version="2023-05-15",
            model="visor-cognitivo-chat",
            temperature=0
    )

    def fill_template(self, ingest_type: str, template: str, parameters: dict, rules: str, example_filling: str, grouped_fields=None) -> str:
        print(f"Ai conf generator, Ingest Type: {ingest_type}")
        """
        Fills the provided HOCON template based on input data, structured rules, and an example of the desired output format.

        Parameters:
        - template (str): The HOCON template as a string to be filled.
        - parameters (dict): The data to be used to fill the template.
        - rules (str): JSON-like dictionary defining rules for filling the template.
        - example_filling (str): Example showing the expected filled output format in HOCON.

        Returns:
        - str: A HOCON-formatted string with the filled template.
        """
        if ingest_type == "Ingesta RAW":
            
            # Crear el prompt con la estructura y el orden especificado
            prompt = f"""
            Context:
            You are a software developer, responsible for generating HOCON configurations for data transformations and applying specific replacement rules in templates. Follow these instructions strictly to ensure replacements and configurations are applied according to the established rules.
            
            Template:
            {template}
            
            Rules:
            {rules}
            
            Parameters:
            {parameters}
            
            Example of Desired Output Format:
            {example_filling}
            
            Please fill the template with the input data, applying the rules exactly as defined, and format the result according to the example.
            Output the result as a string in HOCON format that retains the original structure.
            """

        elif ingest_type=="Ingesta Master":
       
            # Crear el prompt con la estructura y el orden especificado
            prompt = f"""
            Context:
            You are a software developer, responsible for generating HOCON configurations for data transformations and applying specific replacement rules in templates. Follow these instructions strictly to ensure replacements and configurations are applied according to the established rules.
            
            Template:
            {template}
            
            Rules:
            {rules}
            
            parameters = 
            {parameters}

            grouped_fields:
            {grouped_fields}
            
            Example of Desired Output Format:
            {example_filling}
            
            Please fill the template with the input data, applying the rules exactly as defined, and format the result according to the example.
            Output the result as a string in HOCON format that retains the original structure.
            """
        
        # Realizar la llamada a Azure OpenAI
        response = self.client.invoke(prompt)
        
        # Devolver la respuesta en formato de cadena de texto (preservando la estructura HOCON)
        return response

    def create_agent(self):
        # Crear herramientas adicionales si necesitas ejecutar operaciones adicionales antes/después del llenado
        tools = [
            Tool(name="validate_data", func=self.validate_data, description="Validates data based on the schema"),
            # Puedes agregar más herramientas según sea necesario
        ]
        agent = initialize_agent(tools, self.client, verbose=True)
        return agent

    def validate_data(self, data: dict, rules: str) -> bool:
        """
        Validates input data based on defined rules. 

        Parameters:
        - data (dict): The input data to validate.
        - rules (str): The rules for data validation.

        Returns:
        - bool: True if data meets the rules, False otherwise.
        """
        # Aquí se puede añadir lógica personalizada para validar según las reglas
        return True  # Placeholder para validación, implementar según las necesidades específicas

'''
    def __init__(self, template_path):
        self.template_path = template_path
        self.openai = OpenAI(api_key="your_openai_api_key")

    def generate_conf(self, parameters):
        with open(self.template_path, 'r') as file:
            template = file.read()
        
        # Aquí puedes incluir lógica para modificar la plantilla según `parameters`
        generated_conf = template.format(**parameters)
        return generated_conf

    def save_conf(self, conf_content, output_path="output/generated_config.conf"):
        with open(output_path, 'w') as file:
            file.write(conf_content)
'''