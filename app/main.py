import joblib
from typing import Annotated
from openai import OpenAI
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, Body, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
import json
import os
from io import BytesIO
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import fitz
import tempfile
from app.db import engine, create_db_and_tables, PredictionsTickets
#from app.utils import preprocessing_fn
from app.utils import extraer_bloques_de_texto_sin_numeros,extract_names_from_text, buscar_bounding, fuzzy_similarity,load_model, pregunta_RAG, load_model
from enum import Enum
global texto_concatenado
global pdf_document
app = FastAPI(title="FastAPI, Docker, and Traefik")


os.environ["OPENAI_API_KEY"] = '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'


class Sentence(BaseModel):
    client_name: str
    text: str 

class StringRequest(BaseModel):
    value1: str

class User(BaseModel):
    username: str
    full_name: str | None = None
class StringPair(BaseModel):
    value1: str
    value2: str

@app.post("/predict")
async def process_pair(
    value1: str = Form(...), 
    value2: str = Form(...), 
    file: UploadFile = File(...)
):
    contents = await file.read()
    pdf_document = fitz.open(stream=BytesIO(contents), filetype="pdf")
    #print(contents.file_name)
    
    todos_los_bloques = []
    for numero_pagina in range(len(pdf_document)):
        pagina = pdf_document[numero_pagina]
        bloques_texto = extraer_bloques_de_texto_sin_numeros(pagina)
        todos_los_bloques.extend(bloques_texto)
    texto_concatenado = " ".join(todos_los_bloques)

    concatenated = value1 + " " + value2  
    resultados = extract_names_from_text(texto_concatenado)
    print("Nombres de compradores:", resultados['buyer_names'])
    
    similarity= fuzzy_similarity(concatenated,resultados['buyer_names'])
    check=0
    name=""
    bbox=[]
    if similarity>90:
        check=buscar_bounding(pdf_document,concatenated)
        print(check)
        name=check[0][0]
        bbox=check[0][1][0]
    print (similarity)
    return {"similarity": similarity, "concatenated": resultados['buyer_names'],"bbox": bbox}

        
        


@app.post("/asemble")
async def process_str(
    request: StringRequest
):


    #load_model()
    #respuesta= pregunta_RAG(texto_concatenado,request.value1)
    concatenated = request.value1 + "done " 
    return {"respuesta": concatenated}



