import os
import json

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from utils.sheets import GoogleSheet
from utils.cleaners import replace_chars

import spacy

import logging

from dotenv import load_dotenv
import os

load_dotenv()


# Create logger
LOG = logging.getLogger("Extract Network From Sheets")
logging.basicConfig(level=logging.INFO)


def identify_entity(row):
    doc_a = nlp(row["Individuo A: String"])
    doc_b = nlp(row["Individuo B: String"])

    # Asumimos que el primer nombre es el nombre principal
    # Si quieres, puedes modificar este código para manejar múltiples nombres
    ent_a = [ent.label_ for ent in doc_a.ents]
    ent_b = [ent.label_ for ent in doc_b.ents]

    return pd.Series(
        [ent_a[0] if ent_a else "Unknown", ent_b[0] if ent_b else "Unknown"]
    )


def normalize_names(raw_name):
    # lowercase
    raw_name = raw_name.lower()
    # replace chars
    clean_name = replace_chars(raw_name)

    return clean_name


# clasifica las relaciones en categorias
def clasificar_relacion(relacion_raw, relaciones):
    relacion = relacion_raw.lower().replace(" ", "")
    for categoria, lista_relaciones in relaciones.items():
        if relacion in lista_relaciones:
            return categoria
    return "relacionNoReconocida"


LOG.info("Extract Network From Sheets")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ONTOLOGY")  # Ontologia
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)

# load spacy model
nlp = spacy.load("es_core_news_md")

# Obten las relaciones Ind Ind
df_list = [gsheet.read_sheet_to_df("Relaciones Ind-Ind")]

df_ind_org = gsheet.read_sheet_to_df("Relaciones Ind-Org")
df_ind_org["Individuo B: String"] = df_ind_org["Organización A: String"]
df_list.append(df_ind_org)
df = pd.concat(df_list)
print(df)

# Limpieza de datos

# Verifica que no esten vacias Individuo A: String, Individuo B: String, Relación: String
df = df[
    df["Individuo A: String"].notna()
    & df["Individuo B: String"].notna()
    & df["Relación: String"].notna()
]

# exclude self relations
df = df[df["Individuo A: String"] != df["Individuo B: String"]]

# drop duplicates
df = df.drop_duplicates(
    subset=["Individuo A: String", "Individuo B: String", "Relación: String"]
)

# Captura solo las relaciones entre individuos
df_ind_ind = df.copy()
df_ind_ind[["IndividuoA_Tipo", "IndividuoB_Tipo"]] = df_ind_ind.apply(
    identify_entity, axis=1
)
# filter only PERSON-PERSON relations
df_ind_ind = df_ind_ind[
    (df_ind_ind["IndividuoA_Tipo"] == "PER") & (df_ind_ind["IndividuoB_Tipo"] == "PER")
]
# normalize names with dictionary
df_ind_dict = gsheet.read_sheet_to_df("Diccionarios")
ind_dict = df_ind_dict.set_index("Individuo Presente")[
    "Individuo Normalizado"
].to_dict()

# normalice names dict
ind_dict = {key: normalize_names(value) for key, value in ind_dict.items()}
# replace dict
df_ind_ind[["Individuo A: String", "Individuo B: String"]] = df_ind_ind[
    ["Individuo A: String", "Individuo B: String"]
].applymap(lambda x: ind_dict[x] if x in ind_dict else x)
# Normalize names
df_ind_ind[["Individuo A: String", "Individuo B: String"]] = df_ind_ind[
    ["Individuo A: String", "Individuo B: String"]
].applymap(normalize_names)

# categorize relations with dictionary from json
df_categories = df_ind_ind.copy()
with open("data/relations_categorized.json", encoding='utf8') as json_file:
    relations_dict = json.load(json_file)



df_categories["Relación: String"] = df_categories["Relación: String"].apply(
    lambda x: clasificar_relacion(x, relations_dict)
)

# remover categorias no reconocidas
mask = df_categories["Relación: String"] == 'relacionNoReconocida'
df_categories = df_categories[~mask]

# df_filtered = df_filtered.replace({'Individuo A: String': ind_dict, 'Individuo B: String': ind_dict})
# df_categories.to_csv('data/relations.csv', index=False)


networks = [
    {
        "name": "all",
        "dataframe": df,
    },
    {"name": "ind_ind", "dataframe": df_ind_ind},
    {"name": "ind_ind_cat", "dataframe": df_categories},
    {"name": "ind_ind_cat_main_component", "dataframe": df_categories},
]

for network in networks:
    # Crear un grafo dirigido vacío
    G = nx.DiGraph()
    network["dataframe"][
        ["Individuo A: String", "Individuo B: String", "Relación: String"]
    ] = network["dataframe"][
        ["Individuo A: String", "Individuo B: String", "Relación: String"]
    ].applymap(
        lambda x: replace_chars(x)
    )

    # Agregar los bordes y etiquetas al grafo
    for _, row in network["dataframe"].iterrows():
        G.add_edge(
            row["Individuo A: String"],
            row["Individuo B: String"],
            label=row["Relación: String"],
            scandal=row["mencionadoEnEscandalo: String"]
        )

    # Solo dejar la componente principal

    if "component" in network["name"]:
        largest = max(nx.connected_components(G.to_undirected()), key=len)
        G = G.subgraph(largest).copy()

    # Dibujar el grafo
    # pos = nx.spring_layout(G)
    # plt.figure()
    # nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
    #        node_size=500, node_color='pink', alpha=0.9,
    #        labels={node: node for node in G.nodes()})
    #
    ## Dibujar las etiquetas de los bordes
    # edge_labels = nx.get_edge_attributes(G, 'label')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    nx.write_graphml(G, f"data/grafo_{network['name']}.graphml")
    plt.show()
