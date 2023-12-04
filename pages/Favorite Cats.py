import pandas as pd
import streamlit as st
from helpers import api_key, get_image_for_breed, create_favorite
import requests

st.header("My Favorite Cats")
favorites = set()

def get_favorites(api_key):
    favorites_url = f"https://api.thecatapi.com/v1/favourites?api_key={api_key}"
    favorites_dict = requests.get(favorites_url).json()
    return favorites_dict

def get_breed_by_image_id(image_id):
    image_id_url = f"https://api.thecatapi.com/v1/images/{image_id}"
    breed_for_img = requests.get(image_id_url).json()
    # st.write(breed_for_img)
    return breed_for_img

def display_favorites(api_key):
    list = get_favorites(api_key)

    if len(list)< 1: 
        st.write("Oh no! You don't have any favorites.")

    for i in list: 
        favorites.add(i["image_id"])

    for i in favorites: 
        breed = (get_breed_by_image_id(i))
        
        url = (breed["url"])
        img_id = (breed["id"])
        breed_id = [key["id"] for key in breed["breeds"]]
        capt = [key["name"] for key in breed["breeds"]]
        st.image(url, caption=capt, width=150)

display_favorites(api_key)