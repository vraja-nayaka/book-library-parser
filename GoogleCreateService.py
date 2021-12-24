import os
from Google import Create_Service

FOLDER_PATH = '../'
CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret.json')
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def create_service():
    service = Create_Service(
        CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
    return service
