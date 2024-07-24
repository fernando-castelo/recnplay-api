import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def handler(pd: "pipedream"):
    # Load credentials from the environment variable
    credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    # Build the service
    service = build('sheets', 'v4', credentials=credentials)

    # The ID of the spreadsheet to retrieve data from
    spreadsheet_id = '1uPItDRVWib24R8Jt7ynUq-NQF8u5dQ2r0vfU6EiSj8Y'
    range_name = 'A:E'

    card_body = pd.steps["trigger"]["event"]["body"]

    # Call the Sheets API
    values = [
      [
          card_body["nome"],
          card_body["descricao"],
          card_body["data"],
          card_body["duracao"],
          card_body["participantes"]
      ],
  ]

    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result