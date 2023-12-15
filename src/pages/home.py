import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page

def main():
    st.set_page_config(
        page_title="Cawoylel Windanam",
        page_icon="❄️",
        layout="wide"
    )

    add_page_title()  # By default, this also adds indentation

    # Language options
    language_options = ["French", "English"]

    # Initialize session state
    if "language" not in st.session_state:
        st.session_state.language = language_options[0]

    # Language selection radio button
    language = st.radio("Select language:", language_options)
    if language != st.session_state.language:
        st.session_state.language = language


    if st.session_state.language == "French":
        show_pages(
            [
                Page("src/pages/home.py", "Accueil", "🏠"),
                Page("src/pages/speech_recognition.py", "Windanam", "🗣️"),
            ]
        )
        st.write("# 🇫🇷 Bienvenue sur Cawoylel! 👋")

        st.markdown(
            """
            Cawoylel est une initiative à but non lucratif qui se consacre à la conception d'outils technologiques et numériques pour la langue peule.
            Notre objectif est de relever les défis posés par la révolution numérique et technologique moderne pour les langues africaines. 

            Sur ce site, vous trouverez toutes les démos des technologies qui ont été dévevoppée pour la langue peul. Nous vous invitons à les tester et nous faire vos retours.

            Cawoylel aspire à être une initiative participative. De ce fait, toute personne concernée peut rejoindre le mouvement, indépendamment de ses compétences : que vous soyez un simple locuteur de la langue, un ingénieur, un linguiste, un sociologue, ou autre. [Rejoignez le Slack](%s)   
        """
        )
        switch = st.button("Tester le modèle !", type="primary")
        if switch:
            switch_page("Windanam")

    else:
        show_pages(
            [
                Page("src/pages/home.py", "About", "🏠"),
                Page("src/pages/speech_recognition.py", "Windanam", "🗣️"),
            ]
        )
        st.write("# 🇺🇸 Welcome to Cawoylel-Demo ! 👋")

        st.markdown(
            """
            Cawoylel is a non-profit initiative dedicated to the development of technological and digital tools for the Fula language. 
            Its goal is to address the challenges posed by the modern digital and technological revolution for African languages.

            On this page, you'll find demos of all the technologies that have been developed for the Fula language. We invite you to try them out and provide us your feedback.
            
            This project aims to be participatory. Individuals from diverse backgrounds, regardless of their expertise, are welcomed to actively contribute and shape meaningful solutions. 
            Whether you are a language speaker, an engineer, a linguist, a sociologist, or have any other expertise, you are invited to join Cawoylel and be a part of its journey. [Join Slack](%s).

        """)
        switch = st.button("Try Windanam ASR model", type="primary")
        if switch:
            switch_page("Windanam")

if __name__ == "__main__":
    main()