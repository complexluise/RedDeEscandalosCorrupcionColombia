import os
import json

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from utils.sheets import GoogleSheet

import spacy

import logging

# Create logger
LOG = logging.getLogger("Extract Network From Sheets")
logging.basicConfig(level=logging.INFO)

LOG.info("Extract Network From Sheets")

SPREADSHEET_ID = '1lnrxTIbBYYrMwodD7cEmolC7BQk1NVVrFjQiQon8tzQ'
# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)
df = gsheet.read_sheet_to_df('Relaciones Ind-Ind')
print(df)

# Limpieza de datos
# Captura solo las relaciones entre individuos

# Crear un grafo dirigido vacío
G = nx.DiGraph()

# Agregar los bordes y etiquetas al grafo
for _, row in df.iterrows():
    G.add_edge(row['Individuo A: String'], row['Individuo B: String'], label=row['Relación: String'])

# Dibujar el grafo
pos = nx.spring_layout(G)
plt.figure()    
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node:node for node in G.nodes()})

# Dibujar las etiquetas de los bordes
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

nx.write_graphml(G, "data/grafo.graphml")
plt.show()
