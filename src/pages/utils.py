from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import datetime
import io
import json

current_dir = os.getcwd()


def authenticate():
    #token_path = os.path.join(current_dir, 'src/creds', 'credentials.json')
    scope = 'https://www.googleapis.com/auth/drive'
    # Fetch Google Cloud credentials from GitHub secret
    credentials_json = os.environ['GOOGLE_DRIVE_CREDENTIALS']
    if not credentials_json:
        raise ValueError("ENV_SECRET environment variable is not set.")

    try:
        credentials_dict = json.loads(credentials_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
    
    # Authenticate using a service account
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    return build('drive', 'v3', credentials=credentials)


def generate_unique_filename():
    """
    Generate a unique filename with a timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"recorded_audio_{timestamp}.wav"

def upload_to_drive(audio, drive_folder_id="1bkxELyDOA98Ok5uZP3Q0yBoMFE4jy0q5"):
    """
    Upload the audio bytes to Google Drive.
    """
    filename = generate_unique_filename()
    service = authenticate()
    file_metadata = {'name': filename, 'parents': [drive_folder_id]}
    media = MediaIoBaseUpload(io.BytesIO(audio), mimetype='audio/wav')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()