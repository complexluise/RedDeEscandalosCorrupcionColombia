import networkx as nx
import pandas as pd

# Load the GraphML file
G = nx.read_graphml('data\grafo_ind_ind_cat_main_component.graphml')


labels_colors = {
    'relacionesFamiliares': "#FFEBE9",
    'relacionesProfesionales': "#E1D0F2",
    'relacionesDeInvestigacion': "#BBDDF2",
    #'TratosFinancieros': "#330C2F",
    'relacionesDeInfluencia': "#17764D",
    'relacionesDeCorrupcion': "#616914" 
}

scandals_colors = {
    'AgroIngreso Seguro': "#FFEBE9",
    'Cartel de la toga': "#E1D0F2",
    'Escándalo de Reficar': "#BBDDF2",
    'Caso Odebrecht': "#330C2F",
    'Caso Centros Poblados': "#17764D",
    'Carrusel de la Contratación': "#616914",
    "Insight Crime": "#EEFCCE",
    "Wikipedia": "#A7C6DA"
    
}



my_list = []

for i, edge in enumerate(G.edges(data=True)):
    my_list.append(
        dict(
            Source=edge[0],
            Target=edge[1],
            Type="Directed",
            Id=i,
            Label=edge[2]["label"],
            Relacion=edge[2]["label"],
            Scandal=edge[2]["scandal"],
            Weight=1,
            Color_Relacion=labels_colors.get(edge[2]["label"]),
            Color_Scandal=scandals_colors.get(edge[2]["scandal"])
        )
        )

pd.DataFrame(my_list).to_csv("Nodos_colores.csv", index=False)