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
import uuid
import streamlit as st



def authenticate():
    #token_path = os.path.join(current_dir, 'src/creds', 'credentials.json')
    scope = 'https://www.googleapis.com/auth/drive'
    # Fetch Google Cloud credentials from GitHub secret
    credentials_dict = {"type" : st.secrets['type'],
                        "project_id" : st.secrets['project_id'],
                        "private_key_id" : st.secrets['private_key_id'],
                        "private_key" : st.secrets['private_key'],
                        "client_email" : st.secrets['client_email'],
                        "client_id" : st.secrets['client_id'],
                        "auth_uri" : st.secrets['auth_uri'],
                        "token_uri" : st.secrets['token_uri'],
                        "auth_provider_x509_cert_url" : st.secrets['auth_provider_x509_cert_url'],
                        "client_x509_cert_url" : st.secrets['client_x509_cert_url'],
                        "universe_domain" : st.secrets['universe_domain']}

    # Authenticate using a service account
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    return build('drive', 'v3', credentials=credentials)

def generate_unique_filename():
    """
    Generate a unique filename with a timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{str(uuid.uuid4())}_{timestamp}.wav"



def upload_to_drive(audio, drive_folder_id="1bkxELyDOA98Ok5uZP3Q0yBoMFE4jy0q5"):
    """
    Upload the audio bytes to Google Drive.
    """
    filename = generate_unique_filename()
    service = authenticate()
    file_metadata = {'name': filename, 'parents': [drive_folder_id]}
    media = MediaIoBaseUpload(io.BytesIO(audio), mimetype='audio/wav')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()