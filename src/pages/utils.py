from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime
import io

current_dir = os.getcwd()


def authenticate():
    token_path = os.path.join(current_dir, 'src/creds', 'credentials.json')

    # Set the scope to access Google Drive
    scope = 'https://www.googleapis.com/auth/drive'

    # Authenticate using a service account
    credentials = ServiceAccountCredentials.from_json_keyfile_name(token_path, scope)
    return build('drive', 'v3', credentials=credentials)

# def upload_audio_to_drive(audio_data, filename):
#     """
#     Uploads the audio data to Google Drive with the specified filename
#     """
#     drive = authenticate()
#     file_metadata = {'name': filename}
#     media_content = {'mimeType': 'audio/wav'}
#     media_body = MediaBody(audio_data, media_content)

#     file = drive.files().create(body=file_metadata, media_body=media_body).execute()
#     return file['id']

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