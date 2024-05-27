Clasificador de Valor de Cliente
-

Descripción
-
Este proyecto desarrolla un sistema de extracción de información de los documentos pdf de los contratos del cliente. En el cual, extrae el documento recibido por un api request, junto con un nombre, busca el nombre principal en el documento asistiendose de un modelo LLM GPT 3.5 turbo 16k. Para luego de encontrar el principal nombre, compararlo con el nombre enviado por el request con fuzzy match, verificar la similitud y devolver la información. La respuesta del API Request solo devuelve un indicador y un nombre si el fuzzy match da por encima de 90%. Además, si esta condición se cumple, devuelve tambien las coordenadas del nombre encontrado en el documento, y su bounding box. En caso de ser desplegada,se debe contar con un hardware similar al T4 Gpu de google, para procesar la vectorización de la base de datos. La base de datos vectorizara se realiza local.



Tecnologías
-
El proyecto está implementado usando las siguientes tecnologías:

Python 3.9+

Llama index para la arquitectura RAG

Pydantic y FastApi para la creación de las Rest api
Modelos y librerias de Open Ai 
PyMuPDF para el manejo de archivos PDF 
Docker y poetry para la gestión de environments y contenedor
Configuración del Entorno
-
Cómo Ejecutar!?

El primer paso es asegurarse de tener python 3.9+ y pip como gestor de archivos de descarga instalado en el equipo local, ademas de docker instalado y testeado en tu máquina local

Luego se debe instalar la libreria poetry, con el siguiente comando


```bash
   pip install poetry
--

Navega en el directorio en bash para ejecutar el entorno, una vez adentro de la carpeta, ejecutar:



   poetry install

   poetry shell
```

Una vez ejecutado el entorno, ejecutar el docker-compose

docker-compose build

docker-compose up

Luego, el contenedor se habrá ejecutado en local y estará listo para recibir los request


el cuerpo de los request en ambas APIS debe seguir la siguiente estructura

-value1: Name

-value2: Lastnames

-file: (pdf file here)

El cuerpo debe ser enviado al siguiente puerto y endpoint:

http://localhost:5004/predict


Como form-data, el api debe entregar los siguientes campos:


    "similarity": 84,
    "concatenated": "Extracted info from LLM",
    "bbox": [],

Para utilizar el endpoint de la RAG, debe ser enviado a este puerto y endpoint:

{
    "value1": "query"
}

http://localhost:5004/asemble

Con la estructura de respuesta:

{
    "respuesta": "Respuesta"
}


Navigate to the directory in bash to set up the environment. Once inside the folder, execute:


```bash
poetry install
poetry shell

Once the environment is set up, run Docker Compose:

```bash
docker-compose build
docker-compose up

After that, the container will be running locally and will be ready to receive requests.

API Request Structure
The body of the requests in both APIs should follow the following structure:

value1: Name
value2: Lastnames
file: (PDF file here)
The body should be sent to the following port and endpoint:

http://localhost:5004/predict


As form-data, the API should return the following fields:

```json
{
    "similarity": 84,
    "concatenated": "Extracted info from LLM",
    "bbox": []
}


To use the RAG endpoint, it should be sent to this port and endpoint:
```json
{
    "value1": "query"
}

http://localhost:5004/assemble

With the response structure:
```json
{
    "response": "Response"
}

