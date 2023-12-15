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
    return f"{str(uuid.uuid4())}_{timestamp}.wav", f"{str(uuid.uuid4())}_{timestamp}.txt"



def upload_to_drive(audio, text="Neddo ko banndum", audio_folder_id="1bkxELyDOA98Ok5uZP3Q0yBoMFE4jy0q5", text_folder_id = "1r0ksPIs8ooe2mpm3-WvK9iQBTaybYojg"):
    """
    Upload the audio bytes  and text to Google Drive.
    Params:
        audio : Recorded audio from browser
        text : Model transcription
        audio_folder_id : Folder where audio are stored
        text_folder_id : Folder where transcripts are stored
    """
    service = authenticate()
    audio_filename, txt_filename = generate_unique_filename()
    

    audio_file_metadata = {'name': audio_filename, 'parents': [audio_folder_id]}
    audio_media = MediaIoBaseUpload(io.BytesIO(audio), mimetype='audio/wav')

    txt_file_metadata = {'name': txt_filename, 'parents': [text_folder_id]}
    txt_media = MediaIoBaseUpload(io.BytesIO(text.encode('utf-8')), mimetype='text/plain')

    service.files().create(body=audio_file_metadata, media_body=audio_media, fields='id').execute()
    service.files().create(body=txt_file_metadata, media_body=txt_media, fields='id').execute().get('id')



