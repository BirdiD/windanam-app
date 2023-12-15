import streamlit as st
from st_pages import add_page_title, hide_pages
from audiorecorder import audiorecorder
from streamlit_extras.stateful_button import button
import time
from utils import upload_to_drive

add_page_title() 

language_options = ["French", "English"]

    # Initialize session state
if "language" not in st.session_state:
    st.session_state.language = language_options[0]

if "transcription" not in st.session_state:
    st.session_state.transcription = None

if "audio" not in st.session_state:
    st.session_state.audio = None

st.session_state.mapping = {"French" : {"ressource_spinner" : "Téléchargement du modèle de reconnaisance vocale", 
                                        "transcribe" : "Exécution du modèle. Cela peut prendre un certain temps", 
                                        "fetching_output" : "Récupération des résultats",
                                        "output_label" : "Sortie du modèle",
                                        "info_output" : "Pour nous aider à améliorer le modèle, vous pouvez rejoindre la plateforme Annote Fula de Cawoylel dédiée à la collecte et l'annotation de données dans tous les dialectes peul. \
                                           Votre implication est essentielle pour garantir que la technologie respecte et reflète les besoins, les aspirations ainsi que toutes les facettes de la diversité linguistique du peul. Rejoignez la communauté sur slack : https://join.slack.com/t/cawoylel/shared_invite/zt-27j4yeoc6-Lm9vptVwjIKqErMh3DQMiw",
                                        "authorize_button" : "Autoriser l'utilisation de mes enregistrements",
                                        "result_saved" : "Votre enregistrement a été bien pris en compte pour améliorer le modèle. Merci !",
                                        "info_recording" : "Assurez-vous de vous être bien enregistré en cliquant sur le bouton Commencer l'enregistrement. Une fois que vous avez fini, cliquez sur Arrêtez l'enregistrement. Vous pourrez ensuite écouter l'enregistrement. Attendez quelques secondes pour que le bouton Transcrire apparaisse. Cliquez dessus et attendez le résultat.\
                                        Si vous avez commencé à transcrire un audio et que vous souhaitez annuler, clickez à nouveau sur le bouton transcrire."
                                        },

"English" : {"ressource_spinner" : "Downloading model from Hugging Face...", 
            "transcribe":"Running model. This can take some some time",
            "fetching_output" : "Fetching output",
            "output_label" : "Model Output",
            "info_output" : "The results might not be perfect yet. You can contribute to improving this model by joining Cawoylel data annotation platform to help us collect more data. Your involvement is essential to ensuring that technology respects and reflects the needs and aspirations of Fula linguistic communities. \
               By joining the movement, you can help to create a world where technology is accessible and inclusive for all. Click to join Fula community driven platform and contribute : https://join.slack.com/t/cawoylel/shared_invite/zt-27j4yeoc6-Lm9vptVwjIKqErMh3DQMiw",
            "authorize_button" : "Allow my recordings to be used",
            "result_saved" : "Your recording has been saved to improve the model. Thanks a lot!",
            "info_recording" : "Make sure you have recorded yourself by clicking on Click to record button. Once you are done, Click to stop recording button, you will be able to listen to the recording. Wait some seconds for the Transcribe button to appear. Click on it and wait for the output.\
              If you have already run the model and want to stop, click again on the transcribe button."
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



error_message = {"French" : "Une erreur s'est produite. Veuillez rafraichir la page", 
                 "English" : "Something went wrong. Please reload the page"}

consent_message = {"French" : "Cliquez à nouveau sur le bouton pour autoriser l'enregristrement", 
                 "English" : "Click again on consent button."}
def main():
    """
    Main function to record audio from browser
    """
    if st.session_state.language == "French":
      wav_audio_data = audiorecorder("Commencer l'enregistrement", "Arrêtez l'enregistrement")
    else:
      wav_audio_data = audiorecorder("Click to record", "Click to stop recording")

    if len(wav_audio_data) > 0:
      st.session_state.audio = wav_audio_data
      st.audio(st.session_state.audio.export().read())
      st.session_state.audio.export("audio.wav", format="wav")
      
      # if button(st.session_state.mapping[st.session_state.language]["authorize_button"], key="saved"):
      #   try:
      #     with st.spinner("Saving audio"):
      #       upload_to_drive(st.session_state.audio.export().read())
      #       st.success(st.session_state.mapping[st.session_state.language]["result_saved"])

      #   except:
      #     st.warning(consent_message[st.session_state.language], icon="⚠️")
                
    else:
      st.info(st.session_state.mapping[st.session_state.language]["info_recording"])


if __name__ == "__main__":
    main()