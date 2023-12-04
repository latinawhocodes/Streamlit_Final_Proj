import requests
import random
import streamlit as st


api_key = "live_wTLlBlXnUcjiRp9WFHHkoyet18x2PbVcifg6VuKvX9OW1hfy0CHYqboPMs8FfJ3L"
api_key2 = "KStGn/8pRg7wd8H/DICRlA==9AzVau6ydtKXLpHe"

image_map = {
    1: 'assets/boba_cat_1.png', 
    2: 'assets/boba_cat_2.png',
    3: 'assets/boba_cat_3.png',
    4: 'assets/boba_cat_4.png',
    5: 'assets/boba_cat_5.png',
    6: 'assets/boba_cat_6.png',
    7: 'assets/boba_cat_7.png',
    8: 'assets/boba_cat_8.png',
    9: 'assets/boba_cat_9.png',
    10: 'assets/boba_cat_10.png',
    11: 'assets/1.png', 
    12: 'assets/2.png',
    13: 'assets/3.png',
    14: 'assets/4.png',
    15: 'assets/5.png',
    16: 'assets/6.png',
    17: 'assets/7.png',
    18: 'assets/8.png',
    19: 'assets/9.png',
    20: 'assets/10.png'
}

def get_home_image():
    img_key = random.randint(1, 20)
    return image_map.get(img_key)

breeds_map = {
    1: 'ragd',
    2: 'bsho',
    3: 'esho',
    4: 'pers',
    5: 'mcoo',
    6: 'asho',
    7: 'sfol',
    8: 'sphy',
    9: 'abys',
    10: 'drex'
}

color_arr = ["#ff0000", '#ff9600', '#007100', '#9f00a4', '#056265', '#f516ba', '#fbf4a4', '#049fa4', '#04d3a4', '#ff96b5']

def get_breed_info(breed, api_key):
    breed_url = f"https://api.thecatapi.com/v1/breeds/{breed}?{api_key}"
    breed_dict = requests.get(breed_url).json()
    return breed_dict

def get_image_for_breed(image_ref, breed):
    img_endpoint = (f"https://api.thecatapi.com/v1/images/{image_ref}")
    img_response = requests.get(img_endpoint).json()
    st.image(img_response["url"], caption=breed[0]["name"])

def post_favorites(api_key, image_id):
    post_favorites_url = f"https://api.thecatapi.com/v1/favourites?api_key={api_key}"
    post_data = {
        "image_id": image_id
    }
    post_response = requests.post(post_favorites_url, json=post_data)
    return post_response

def create_favorite(api_key, image_id):
    post = post_favorites(api_key, image_id)
    return post