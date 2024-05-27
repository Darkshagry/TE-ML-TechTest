"""This module is for text processing for model prediction."""


import os
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process  
from openai import OpenAI
import nltk
import fitz
from PIL import Image, ImageDraw
import json

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

os.environ["OPENAI_API_KEY"] = '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'

def load_model():
    Settings.embed_model=HugggtingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"

)

def es_numero(palabra):
    try:
        float(palabra)
        return True
    except ValueError:
        return False

def pregunta_RAG(texto_concatenado,query):
    lista=list(texto_concatenado)
    documents = [Document(text=t) for t in lista]
    index_book= VectorStoreIndex.from_documents(documents)
    query_engine_book=index_book.as_query_engine()
    response= query_engine_book.query(query)
    return response


def extraer_bloques_de_texto_sin_numeros(pagina, margen_izquierdo=50):
    bloques = pagina.get_text("dict")["blocks"]
    bloques_texto = []

    for bloque in bloques:
        if "lines" in bloque:  
            texto_bloque = ""
            for linea in bloque["lines"]:
                for span in linea["spans"]:
                    if not (es_numero(span["text"]) and span["bbox"][0] < margen_izquierdo):
                        texto_bloque += span["text"] + " "
            bloques_texto.append(texto_bloque.strip())
    
    return bloques_texto


def extract_names_from_text(texto_concatenado):
    client = OpenAI(
    # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "extract the proper names from this document, only the names of the buyer, don't answer anything different than that" + texto_concatenado,
            }
        ],
        model="gpt-3.5-turbo-16k",
    )

    respuesta= response.choices[0].message.content# Parsear el contenido JSON

    # Parsear el contenido JSON
    #data = json.loads(respuesta)

    # Extraer los nombres de "Buyer" y "Seller"
    buyer_names = respuesta
    #seller_names = data.get("Seller", [])

    return {
        "buyer_names": buyer_names,
    }

def dibujar_bounding_boxes(pagina, ancho, alto, escala=2, margen_izquierdo=50):
    # Crear una imagen en blanco
    imagen = Image.new("RGB", (int(ancho * escala), int(alto * escala)), "white")
    dibujante = ImageDraw.Draw(imagen)

    # Obtener las palabras en la página
    palabras = pagina.get_text("words")  # Lista de tuplas: (x0, y0, x1, y1, "word", block_no, line_no, word_no)

    # Dibujar cada bounding box excluyendo las palabras que están cerca del borde izquierdo
    for palabra in palabras:
        x0, y0, x1, y1, _ = palabra[:5]
        if x0 > margen_izquierdo:  # Filtrar palabras cerca del borde izquierdo
            x0, y0, x1, y1 = x0 * escala, y0 * escala, x1 * escala, y1 * escala
            dibujante.rectangle([x0, y0, x1, y1], outline="red", width=2)
    
    return imagen

def verificar_nombre(palabras, index, nombre_palabras):
    for i, palabra in enumerate(nombre_palabras):
        if index + i >= len(palabras) or palabras[index + i][4] != palabra:
            return False
    return True

def buscar_bounding(documento,nombre_a_buscar):
  resultados = []
  # Convertir el nombre a una lista de palabras
  palabras_nombre = nombre_a_buscar.split()
  # Recorrer cada página del documento
  for numero_pagina in range(documento.page_count):
      pagina = documento.load_page(numero_pagina)
      
      # Extraer las palabras de la página
      palabras = pagina.get_text("words")
      
      # Recorrer cada palabra
      # Recorrer cada palabra
      for index, palabra in enumerate(palabras):
          # Verificar si la secuencia de palabras coincide con el nombre
          if verificar_nombre(palabras, index, palabras_nombre):
              # Guardar el nombre encontrado junto con su bounding box
              bounding_boxes = [palabra[:4] for palabra in palabras[index:index + len(palabras_nombre)]]
              resultados.append((nombre_a_buscar, bounding_boxes))
              
  return resultados

def fuzzy_similarity(nombre1,nombre2):
    return fuzz.ratio(nombre1, nombre2)






