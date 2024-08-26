¡Claro! Aquí tienes una versión mejorada del README, con un tono más coloquial y accesible:

---

# Análisis de Redes de Corrupción en Escándalos

## ¿De qué va este proyecto?

Este proyecto se enfoca en analizar redes de corrupción utilizando artículos de noticias. Extraemos información relevante, procesamos los datos y visualizamos cómo se relacionan las diferentes entidades involucradas en escándalos de corrupción. Básicamente, tomamos artículos de noticias, identificamos quién es quién y cómo se conectan, y luego guardamos toda esta información en Google Sheets para un análisis más fácil.

## ¿Qué incluye el proyecto?

1. **Extractor de Noticias** (`get_txt_from_news.py` y `any_news_scrapper.py`)
   - Obtiene artículos de noticias de diversas fuentes.
   - Extrae detalles importantes como el título, autor, URL y contenido del artículo.

2. **Extracción de Conocimiento** (`extract_knowledge.py`)
   - Procesa los artículos para extraer entidades (personas y organizaciones).
   - Identifica las relaciones entre estas entidades usando un modelo de lenguaje (LLM).

3. **Almacenamiento de Datos** (`put_data_sheets.py`)
   - Guarda los datos procesados en Google Sheets.
   - Organiza la información en diferentes pestañas para entidades, relaciones y artículos.

4. **Análisis de Red** (`extract_network.py`)
   - Lee los datos de Google Sheets.
   - Crea grafos de red con NetworkX para visualizar cómo se conectan las entidades.
   - Genera visualizaciones de estas redes de corrupción.

## ¿Cómo lo configuro?

1. Clona este repositorio en tu máquina.
      ```bash
   git clone https://github.com/complexluise/RedDeEscandalosCorrupcionColombia.git
      ```
2. Instala las dependencias de Python:
   ```bash
   pip install pandas networkx matplotlib spacy google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
   ```
3. Descarga el modelo de lenguaje en español para spaCy:
   ```bash
   python -m spacy download es_core_news_md
   ```
4. Configura tus credenciales para la API de Google Sheets y mantenlas seguras.
5. Crea un archivo `.env` con estas variables:
   - `SPREADSHEET_ONTOLOGY`: ID de la hoja de Google para datos de ontología.
   - `SPREADSHEET_LINKS`: ID de la hoja de Google con enlaces a los artículos.

## ¿Cómo lo uso?

1. Ejecuta el extractor de noticias para recopilar artículos:
   ```bash
   python get_txt_from_news.py
   ```

2. Procesa los artículos para extraer entidades y relaciones:
   ```bash
   python extract_knowledge.py
   ```

3. Guarda los datos procesados en Google Sheets:
   ```bash
   python put_data_sheets.py
   ```

4. Analiza las redes y crea visualizaciones:
   ```bash
   python extract_network.py
   ```

## ¿Qué hay dentro del proyecto?

```
.
├── utils/
│   ├── any_news_scrapper.py
│   ├── llm_extract.py
│   ├── sheets.py
│   └── prompts
├── .gitignore
├── Redes_de_corrupción_proyecto_final.ipynb
├── extract_knowledge.py
├── extract_network.py
├── get_txt_from_news.py
└── put_data_sheets.py
```

## Cosas a tener en cuenta

- Asegúrate de tener los permisos necesarios para extraer y analizar los artículos de noticias.
- El proyecto usa Google Sheets como base de datos, así que necesitas tener los derechos de acceso adecuados.
- Dependiendo de las fuentes de noticias, es posible que se necesite configuración adicional.

## Mejoras a futuro

- Implementar manejo de errores y reintentos para las solicitudes de red.
- Añadir soporte para más fuentes de noticias.
- Mejorar la visualización de las redes con funciones interactivas.
- Automatizar las actualizaciones de datos de forma regular.

## Contribuyentes

[Aquí puedes listar a los principales contribuyentes del proyecto]

## Licencia

[Especifica aquí la licencia bajo la cual se publica este proyecto]

---

¡Listo! Con este README, cualquier persona interesada en el análisis de redes de corrupción puede entender y comenzar a trabajar en tu proyecto de forma rápida y sencilla.