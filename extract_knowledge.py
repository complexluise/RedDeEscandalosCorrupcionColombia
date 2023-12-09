import os
import json

from utils.llm_extract import extract_relations, extract_entities

import logging


def configurar_logger(nombre):
    """
    Configura y devuelve un logger con el nivel de registro establecido en INFO.

    Args:
        nombre (str): Nombre del logger.

    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    return logger


def listar_archivos_en_directorio(directorio, extension):
    """
    Lista todos los archivos en un directorio que terminen con una extensión específica.

    Args:
        directorio (str): Ruta al directorio.
        extension (str): Extensión de los archivos.

    Returns:
        Lista de nombres de archivos.
    """
    lista_archivos = os.listdir(directorio)
    return [archivo for archivo in lista_archivos if archivo.endswith(extension)]


def abrir_y_cargar_archivo_json(ruta_archivo):
    """
    Abre y carga un archivo JSON.

    Args:
        ruta_archivo (str): Ruta al archivo JSON.

    Returns:
        Datos cargados desde el archivo JSON.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def extraer_y_guardar_entidades(raw_article, nombre_archivo, directorio):
    """
    Extrae entidades y las guarda en un archivo.

    Args:
        raw_article (dict): Entrada para la función de extracción de entidades.
        nombre_archivo (str): Nombre del archivo para guardar la salida.
        directorio (str): Directorio para guardar el archivo.

    Returns:
        Respuesta de la función de extracción de entidades o None si ocurre una excepción.
    """
    LOG.info("Extrayendo entidades")
    try:
        chat_completion_NER = extract_entities(raw_article)
    except Exception as e:
        LOG.error(e)
        LOG.info("Continuando con el siguiente archivo")
        return None
    with open(directorio + nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(chat_completion_NER["text"])
    return chat_completion_NER


def extraer_y_guardar_relaciones(raw_article, nombre_archivo, directorio):
    """
    Extrae relaciones y las guarda en un archivo.

    Args:
        raw_article (dict): Entrada para la función de extracción de relaciones.
        nombre_archivo (str): Nombre del archivo para guardar la salida.
        directorio (str): Directorio para guardar el archivo.

    Returns:
        Respuesta de la función de extracción de relaciones o None si ocurre una excepción.
    """
    LOG.info("Extrayendo relaciones")
    try:
        chat_completion_ER = extract_relations(raw_article)
    except Exception as e:
        LOG.error(e)
        LOG.info("Continuando con el siguiente archivo")
        return None

    with open(directorio + nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(chat_completion_ER["text"])

    return chat_completion_ER


def guardar_y_eliminar_archivo(
    json_noticias, ruta_archivo_origen, ruta_archivo_destino
):
    """
    Guarda las noticias en un nuevo archivo y elimina el archivo original.

    Args:
        json_noticias (dict): Noticias en formato JSON.
        ruta_archivo_origen (str): Ruta al archivo original.
        ruta_archivo_destino (str): Ruta al nuevo archivo.
    """
    with open(ruta_archivo_destino, "w", encoding="utf-8") as archivo:
        archivo.write(json.dumps(json_noticias))
    os.remove(ruta_archivo_origen)


if __name__ == "__main__":
    # configuración
    LOG = configurar_logger("ExtractRelationships")
    LOG.info("Iniciando la Extracción de la Red de Corrupción en Escándalos")
    lista_archivos = listar_archivos_en_directorio("data/raw_article", ".json")

    # ciclo principal
    for nombre_archivo in lista_archivos:
        LOG.info("Procesando el archivo: %s", nombre_archivo)
        ruta_archivo = f"data/raw_article/{nombre_archivo}"

        json_noticias = abrir_y_cargar_archivo_json(ruta_archivo)
        raw_article = {"article": json_noticias["Contenido"]}

        chat_completion_NER = extraer_y_guardar_entidades(
            raw_article, nombre_archivo, "data/extracted_entities/"
        )
        if not chat_completion_NER:
            continue

        json_NER = json.loads(chat_completion_NER["text"])
        individuos = [item["Nombre"] for item in json_NER["Individuos"]]
        individuos = ", ".join(individuos)
        raw_article.update({"individuos": individuos})

        chat_completion_ER = extraer_y_guardar_relaciones(
            raw_article, nombre_archivo, "data/extracted_relations/"
        )
        if not chat_completion_ER:
            continue

        guardar_y_eliminar_archivo(
            json_noticias, ruta_archivo, f"data/processed_article/{nombre_archivo}"
        )
