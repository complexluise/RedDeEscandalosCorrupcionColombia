import os
import json

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from utils.sheets import GoogleSheet
from utils.data_cleaning import replace_chars

import spacy

import logging

# Create logger
LOG = logging.getLogger("Extract Network From Sheets")
logging.basicConfig(level=logging.INFO)

char_dict = {
    ":": "_",
    "á": "a",
    "é": "e",
    "í": "i",
    "ì": "i",
    "ó": "o",
    "ú": "u",
    "ñ": "n",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ñ": "N",
    "¿": "",
    "?": "",
    "¡": "",
    "!": "",
    "(": "",
    ")": "",
    '"': "",
    "'": "",
    "“": "",
    "”": "",
    " ": "_",
}

def identify_entity(row):
    doc_a = nlp(row['Individuo A: String'])
    doc_b = nlp(row['Individuo B: String'])

    # Asumimos que el primer nombre es el nombre principal
    # Si quieres, puedes modificar este código para manejar múltiples nombres
    ent_a = [ent.label_ for ent in doc_a.ents]
    ent_b = [ent.label_ for ent in doc_b.ents]

    return pd.Series([ent_a[0] if ent_a else 'Unknown', ent_b[0] if ent_b else 'Unknown'])

def normalize_names(raw_name):

    # lowercase
    raw_name = raw_name.lower()
    # replace chars
    clean_name = replace_chars(raw_name, char_dict)

    return clean_name

# clasifica las relaciones en categorias
def clasificar_relacion(relacion, relaciones):
    for categoria, lista_relaciones in relaciones.items():
        if relacion in lista_relaciones:
            return categoria
    return "Relación no reconocida"

LOG.info("Extract Network From Sheets")

SPREADSHEET_ID = '1lnrxTIbBYYrMwodD7cEmolC7BQk1NVVrFjQiQon8tzQ'
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)

# load spacy model
nlp = spacy.load("es_core_news_md")

# Obten las relaciones Ind Ind
df_list = []
df_list.append(gsheet.read_sheet_to_df('Relaciones Ind-Ind'))

df_ind_org = gsheet.read_sheet_to_df('Relaciones Ind-Org')
df_ind_org['Individuo B: String'] = df_ind_org['Organización A: String']
df_list.append(df_ind_org)
df = pd.concat(df_list)
print(df)


# Limpieza de datos

# Verifica que no esten vacias Individuo A: String, Individuo B: String, Relación: String
df = df[df['Individuo A: String'].notna() & df['Individuo B: String'].notna() & df['Relación: String'].notna()]


# Captura solo las relaciones entre individuos

df[['IndividuoA_Tipo', 'IndividuoB_Tipo']] = df.apply(identify_entity, axis=1)

# drop duplicates
df = df.drop_duplicates(subset=['Individuo A: String', 'Individuo B: String', 'Relación: String'])

# filter only PERSON-PERSON relations
df_filtered = df[(df['IndividuoA_Tipo'] == 'PER') & (df['IndividuoB_Tipo'] == 'PER')]

# normalize names with dictionary
df_ind_dict = gsheet.read_sheet_to_df('Diccionarios')
ind_dict = df_ind_dict.set_index('Individuo Presente')['Individuo Normalizado'].to_dict()
# normalice names dict
ind_dict = {key: normalize_names(value) for key, value in ind_dict.items()}
#replace dict
df_filtered[['Individuo A: String', 'Individuo B: String']] = df_filtered[['Individuo A: String', 'Individuo B: String']]\
                                                .applymap(lambda x: ind_dict[x] if x in ind_dict else x)
# Normalize names
df_filtered[['Individuo A: String', 'Individuo B: String']] = df_filtered[['Individuo A: String', 'Individuo B: String']].applymap(normalize_names)



# normalize relations with dictionary from json
with open('categorizer.json') as json_file:
    relations_dict = json.load(json_file)

df_filtered['Categorización_Relación'] = df_filtered['Relación: String'].apply(lambda x: clasificar_relacion(x, relations_dict))

#df_filtered = df_filtered.replace({'Individuo A: String': ind_dict, 'Individuo B: String': ind_dict})
df_filtered.to_csv('data/relations.csv', index=False)
exit()
# exclude self relations
df_filtered = df_filtered[df_filtered['Individuo A: String'] != df_filtered['Individuo B: String']]



# Crear un grafo dirigido vacío
G = nx.DiGraph()

# Agregar los bordes y etiquetas al grafo
for _, row in df_filtered.iterrows():
    G.add_edge(row['Individuo A: String'], row['Individuo B: String'], label=row['Relación: String'])

# Dibujar el grafo
#pos = nx.spring_layout(G)
#plt.figure()
#nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
#        node_size=500, node_color='pink', alpha=0.9,
#        labels={node: node for node in G.nodes()})
#
## Dibujar las etiquetas de los bordes
#edge_labels = nx.get_edge_attributes(G, 'label')
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

nx.write_graphml(G, "data/grafo_ind_ind.graphml")
plt.show()
