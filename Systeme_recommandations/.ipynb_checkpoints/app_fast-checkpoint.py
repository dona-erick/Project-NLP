from fastapi import FastAPI
from fastapi import Depends, HTTPException, Request
from typing import List, Optional, Union
import streamlit as st
import requests
from pydantic import BaseModel
from gensim.models import Word2Vec
import pandas as pd

app = FastAPI()

## chargement du modèle de recommandations
model = Word2Vec.load('recommandations.model')

### dataset
data = pd.read_csv('lifestring.csv')
#
@app.get('/')
def get_welcome():
    return {"Welcome on the application of recommandations similar songs artists "}
    
### endpoint of recommandations
@app.post('/recommandations')

def get_recommandations(song_name: str):
    if song_name not in data['track_artist'].values:
        raise HTTPException(status_code = 400, detail = 'Request Not found')
    try:
        similiar_song = model.wv.most_similar(song_name, topn = 5)
        recommandations = [sing[0] for sing in similiar_song]
        return {
            "message": f"Les chansons similaires à {song_name} sont :",
            "recommendations": recommandations
        }
    except KeyError:
        raise HTTPException(status_code=400, detail="Chanson non trouvée dans le modèle.")
