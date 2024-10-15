from fastapi import FastAPI, HTTPException
import requests, joblib, pickle
import streamlit as st
import pandas as pd
from gensim.models import Word2Vec

app = FastAPI()


## import data
df = pd.read_csv("/home/einstein/Portfolio/Systeme_recommandations/data/song.csv")

### loading the model
model = Word2Vec.load('/home/einstein/Portfolio/Systeme_recommandations/Recommandations/recommandations.model')

### first routers 

@app.get('/')
def get_welcome():
    return {"Message": "Welcome on HumourLife ! "}

@app.post('/recommandations')

def get_recommandations(artist_name: str):
    #filtrer selons le nom sdes artistes
    #artist_songs = df[df['Artist_inter'].str.contains(artist_name, na = False, case = False)]
    
    if artist_name not in df['Artist_inter'].values[0]:
        return HTTPException(status_code = 404, detail = "Chansons de l'artistes non trouvées")
    try:
        similar_songs = model.wv.most_similar(artist_name, topn = 5)
        recommandations = []
        
        for var, _ in similar_songs:
            songs_data = df[df['Artist_inter'].str.contains(var, case = False, na= False)].iloc[0]
            
            if not var.empty:
                # Prendre la première chanson et album de cet artiste pour la recommandation
                track_info = var.iloc[0]
                recommandations.append({
                    "Artiste": track_info['Artist_inter'],
                    "Chanson": track_info['Nom_chanson'],
                    "Album": track_info['Nom_album']
                })

        return {
            "message": f"Les artistes similaires à {artist_name} avec leurs chansons et albums sont :",
            "recommendations": recommandations
        }
    except:
        raise HTTPException(status_code = 400, detail = "Not found")
