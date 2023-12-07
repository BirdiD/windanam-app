import streamlit as st
from st_pages import add_page_title, hide_pages
from st_audiorec import st_audiorec
from streamlit_extras.stateful_button import button
import time
#import upload_to_drive

import torch
from transformers import pipeline

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

add_page_title() 

if "transcription" not in st.session_state:
    st.session_state.transcription = None

if "audio" not in st.session_state:
    st.session_state.audio = None

if "language" not in st.session_state:
    st.session_state.language = "English"
    
st.session_state.mapping = {"French" : {"ressource_spinner" : "Téléchargement du modèle de reconnaisance vocale", 
                                        "transcribe" : "Exécution du modèle. Cela peut prendre un certain temps", 
                                        "fetching_output" : "Fetching output",
                                        "output_label" : "Sortie du modèle",
                                        "info_output" : "Pour nous aider à améliorer le modèle, vous pouvez cliquez sur le bouton ci-dessous afin de nous autoriser à utiliser vos enregistrements?",
                                        "authorize_button" : "Autoriser l'utilisation de mes enregistrements",
                                        "result_saved" : "Votre enregistrement a été bien pris en compte pour améliorer le modèle. Merci !",
                                        "info_recording" : "Assurez-vous de vous être bien enregistré en cliquant sur le bouton Start Recording. Une fois enregistré, vous pourrez l'écouter. Attendez quelques secondes pour que le bouton Transcrire apparaisse. Cliquez dessus et attendez la sortie"
                                        },

"English" : {"ressource_spinner" : "Downloading model from Hugging Face...", 
            "transcribe":"Running model. This can take some some time",
            "fetching_output" : "Récupération des résultats",
            "output_label" : "Model Output",
            "info_output" : "The results might not be perfect yet. In order to improve the model, would you allow us to use your recordings? If yes, click on the button below",
            "authorize_button" : "Allow my recordings to be used",
            "result_saved" : "Your recording has been saved to improve the model. Thanks a lot!",
            "info_recording" : "Make sure you have recorded yourself by clicking on Start Start Recording button. Once recorded, you will be able to listen to the recording. Wait some seconds for the Transcribe button to appear. Click on it and wait for the output"
            }
}  
if st.session_state.language == "French":
  st.markdown(
        """
        **Windanam** est le premier modèle de reconnaissance vocale multidialectale de Cawoylel.
        Comme tous les systèmes d'intelligence artificielle, il existe des risques que le modèle mal interprète ce que veut dire une personne ou produise des résultats inexacts.
        Nous vous encourageons à le tester et à nous faire vos retours afin de l'améliorer.
    """
    )
else: 
  st.markdown(
      """
      **Windanam** is Cawoylel's first multidialectal speech recognition model. 
      As with all AI systems, there are inherent risks that the model coud mis-transcribe what a person wants to say, or generate inaccurate outputs.
      We encourage you to test it and provides us some feedbacks on the model outputs.
  """
  )


@st.cache_resource(show_spinner=st.session_state.mapping[st.session_state.language]["ressource_spinner"])
def load_model(model_name = "cawoylel/windanam_mms-1b-tts_v2"):
  """
  Function to load model from hugging face
  """
  pipe = pipeline("automatic-speech-recognition", model=model_name)
  return pipe

pipeline = load_model()

st.cache_data(show_spinner=st.session_state.mapping[st.session_state.language]["transcribe"])
def transcribe_audio(sample):
  """
  Transcribe audio
  """
  transcription = pipeline(sample)
  return transcription["text"]

def main():
    """
    Main function to record audio from browser
    """
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
      st.session_state.audio = wav_audio_data
      if button("Transcribe", key="transcribe"):
        st.session_state.transcription = transcribe_audio(st.session_state.audio)
        with st.spinner(st.session_state.mapping[st.session_state.language]["fetching_output"]):
            st.text_area(label = st.session_state.mapping[st.session_state.language]["output_label"], 
                             value=st.session_state.transcription, height = 100)
                
        with st.container():
          st.info(st.session_state.mapping[st.session_state.language]["info_output"], icon="ℹ️") 
          if button(st.session_state.mapping[st.session_state.language]["authorize_button"], key="saved"):
            upload_to_drive(wav_audio_data)
            #Display a message indicating successful upload
            st.success(st.session_state.mapping[st.session_state.language]["result_saved"])

                
    else:
      st.info(st.session_state.mapping[st.session_state.language]["info_recording"])


if __name__ == "__main__":
    main()
