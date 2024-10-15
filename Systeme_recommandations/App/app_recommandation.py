import streamlit as st
import pandas as pd
import requests

### title of application

st.title('HumourLife')
st.markdown("Bienvenue sur votre application d'écoute musicale HumourLife. Vos désirs, notre satisfaction")

st.write('Réalisé par:')
st.subheader("Eric KOULODJI D.")

df = pd.read_csv("/home/einstein/Portfolio/Systeme_recommandations/data/song.csv")

# Entrée utilisateur pour obtenir des recommandations
artist_name = st.text_input("Entrez le nom d'un artiste:")

# Lorsque l'utilisateur clique sur le bouton
if st.button("Recommandations"):
    if artist_name:
        url = 'http://127.0.0.1:8000/recommandations'
        params = {'artist_name': artist_name}
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            df = response.json()
            st.write(f"Les chansons similaires à l'artiste '{artist_name}' sont :")
            
            # Afficher les recommandations avec leurs albums et artistes
            for song in df.Blood:
                 st.write(f"Song: {song} ")
        else:
            st.write("Artiste non trouvé ou une erreur est survenue.")
            
    else:
        f"Veuillez entrer le nom d'un artiste"
