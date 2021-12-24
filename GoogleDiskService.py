def add_sheet(service, title: str) -> str:
    sheet_body = {
        'properties': {
            'title': title,
            'locale': 'en_US',  # optional
            'autoRecalc': 'ON_CHANGE',
        }
    }
    sheets_file = service.spreadsheets().create(body=sheet_body).execute()
    return sheets_file['spreadsheetId']


columns = ['Район',	'Контакты',	'Кол-во филиалов', 'Дата звонка',
           'Письмо отправлено', 'Ответ из библиотеки', 'Распространено']


def update_sheet_column(service, id: str, values: list[str]):
    length = len(values)
    range = f"A2:A{length + 1}"
    columns_range = "A1:G1"

    # add values
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range,
                 "majorDimension": "COLUMNS",
                 "values": [values]},
                {"range": columns_range,
                 "majorDimension": "ROWS",
                 "values": [columns]},
            ]
        }
    ).execute()

    requests = []

    # styles
    requests.append({
        "repeatCell": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {
                                "fontSize": 11,
                                "bold": "true"
                            }
                        }
                    },
                    "fields": "userEnteredFormat(textFormat)"
                    }
    })

    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": 0,
                "gridProperties": {
                    "frozenRowCount": 1
                }
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })

    # columns width
    requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": 0,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": 7
            },
            "properties": {
                "pixelSize": 170
            },
            "fields": "pixelSize"
        }
    })

    requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": 0,
                "dimension": "COLUMNS",
                "startIndex": 1,
                "endIndex": 2
            },
            "properties": {
                "pixelSize": 250
            },
            "fields": "pixelSize"
        }
    })

    body = {
        'requests': requests
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=id,
        body=body).execute()
