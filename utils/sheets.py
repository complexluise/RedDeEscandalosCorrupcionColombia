import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import os

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = "gpt!A1"
CREDENTIALS_FILE = os.getenv("CREDENTIALS_GOOGLE_API")

import pandas as pd


class GoogleSheet:
    def __init__(self, spreadsheet_id):
        self.creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
        self.service = build("sheets", "v4", credentials=self.creds)

        self.spreadsheet_id = spreadsheet_id

    def add_csv_to_sheet(self, df, range_name, add_headers=False):
        # Convierte el DataFrame a lista de listas
        data = df.values.tolist()

        if add_headers:
            # Agrega los nombres de las columnas del DataFrame a la lista de datos
            data.insert(0, df.columns.tolist())

        # Construye el cuerpo para la solicitud de actualización
        body = {"values": data}

        # Llama a la API de Sheets para escribir los datos en la hoja
        result = (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        print("{0} celdas actualizadas.".format(result.get("updatedCells")))

    def read_sheet_to_df(self, range_name):
        # Llama a la API de Sheets para leer los datos de la hoja
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=range_name)
            .execute()
        )

        # Obtiene los valores de la hoja
        values = result.get("values", [])

        if not values:
            print("No data found.")
        else:
            # Convierte la lista de listas a DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            return df


if __name__ == "__main__":
    gsheet = GoogleSheet(SAMPLE_SPREADSHEET_ID)
    filename = "eluniversalrodolfo-campo-soto-exgerente-del.txt.csv"
    df = pd.read_csv(
        "G:/Shared drives/GEINCyR - Ciencias Sociales Computacionales Heterodoxas (CSCH)/Carpeta de trabajo/Corruption Network/data/extracted_relationships/"
        + filename,
        sep=";",
    )
    gsheet.add_csv_to_sheet(df, SAMPLE_RANGE_NAME)
