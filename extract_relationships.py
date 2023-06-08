from utils.llm_extract import extract_relationship
from utils.sheets import GoogleSheet
import pandas as pd


SPREADSHEET_ID = '1wnLOldQ2qfqmk_zsJbddg4K4slP9_kSa4xTT02T8Gpo'

# Initialize Google Sheet
gsheet = GoogleSheet(SPREADSHEET_ID)

context = """
As a journalist and network scientist, you're analyzing the social network that emerged from a 
corruption scandal in Colombia. Your task is Named Entities Recognitizion of individuals and 
characterize the relationships between them from the details in the article. Create a csv table with ";" separator featuring
 the following column headers:

"Nombre Persona 1" (Person 1's Name), "Cargo Persona 1" (Person 1's Position), "Detalles Vinculo" (Connection Details), "Tipo de Vinculo" (Type of Connection) Relation Classifiers should have verbpharse  (born) + prepositional phrase (InCity) -> bornInCity, "Nombre Persona 2" (Person 2's Name), "Cargo Persona 2" (Person 2's Position)

Only consider each relationship once, treating the network as undirected. Please describe each relationship.
Based on the provided information, here's a table summarizing the relevant relationships and their descriptions:
This is the example of expected output.
Nombre Persona 1; Cargo Persona 1; Tipo de Vinculo; Detalles Vinculo; Nombre Persona 2; Cargo Persona 2
Luis Fernando Duque; Representante Legal Unión Temporal Centros Poblados; ColaboraciónEnFraude; Supuestamente implicado en el fraude contractual con Mintic; Juan José Laverde; Rave Agencia de SegurosONLY WRITE THE TABLE, NOT THE TEXT ABOVE

"""

# open file and return text
path_file = 'data/raw_article/eluniversalrodolfo-campo-soto-exgerente-del.txt'
filename = path_file.split("/")[-1]
with open(path_file, "r", encoding="utf-8") as file:
    text = file.read()
prompt = context + text
my_response = extract_relationship(prompt)
print(my_response)

# parse response into dataframe
# verify if response is not empty
if my_response:
    # split response into list of lines
    lines = my_response.split("\n")
    # remove empty lines
    lines = [line for line in lines if line]
    # remove first line
    lines = lines[1:]
    # split each line into list of elements
    lines = [line.split(";") for line in lines]
    # create dataframe
    df = pd.DataFrame(lines, columns=["Nombre Persona 1", "Cargo Persona 1", "Tipo de Vinculo", "Detalles Vinculo",
                                      "Nombre Persona 2", "Cargo Persona 2"])
    # save dataframe to csv
    df.to_csv("data/extracted_relationships/" + filename + ".csv", sep=";", index=False)

# Añade a la hoja de cálculo de Google
gsheet.add_csv_to_sheet(df, 'gpt')

# save file to txt
#with open("data/extracted_relationships/" + filename.replace("txt", "csv"), "w", encoding="utf-8") as file:
#    file.write(my_response)
