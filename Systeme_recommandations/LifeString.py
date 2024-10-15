import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


st.markdown("""Cette application est utilisée pour générer le nom des artistes similaires 
            à celle que vous ecoutez ou aimez. Top 5 des préféreés""")


# Titre de l'application
st.title("Système de recommandation de chansons")

data  = pd.read_csv('lifestring.csv')
# Tableau de bord
st.header("Tableau de bord")

# Métrique: Nombre total de chansons
total_songs = len(data)
st.metric("Nombre total de chansons", total_songs)

# Métrique: Nombre total d'artistes
total_artists = data['track_artist'].nunique()
st.metric("Nombre total d'artistes", total_artists)

# Artistes les plus fréquents (par nombre de chansons)
st.subheader("Top 5 des artistes les plus fréquents")
top_artists = data['track_artist'].value_counts()
st.bar_chart(top_artists)



# Entrée utilisateur
song_name = st.text_input("Entrez le nom d'une chanson:")

# Lorsque l'utilisateur clique sur le bouton
if st.button("Recommandations"):
    # Envoyer une requête POST à l'API FastAPI
    if song_name:
        url = 'http://127.0.0.1:8000/recommandations'
        params = {'song_name': song_name}
        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"Les chansons similaires à '{song_name}' sont :")
            for song in data['recommendations']:
                st.write(song)
                #data.append(song)
                #### afficher les recommandation sous forme de tableau
            st.subheader('Recommandations')
            st.table(pd.DataFrame(data['recommendations'], columns = ['chansons recommandeés']))
            #st.subheader("Répartition des artistes")
            #{fig, ax = plt.subplots()
           # data['chansons recommandeés'].value_counts().plot(kind='bar', ax=ax)
          #  st.pyplot(fig)
        
        
    
        else:
            st.write("Chanson non trouvée ou une erreur est survenue.")



##auteur 
st.markdown('Réalisé par: ')
st.subheader('Dona Eric KOULODJI')



# Graphique des artistes les plus fréquents
