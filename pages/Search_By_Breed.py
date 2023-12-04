import streamlit as st
import requests
import pandas as pd
from helpers import *
import numpy as np

def generate_list_of_breeds():
    breeds_url = "https://api.thecatapi.com/v1/breeds/"
    all_breeds = requests.get(breeds_url).json()
    # st.write(all_breeds)
    return all_breeds

def generate_breeds():
    options_dict = generate_list_of_breeds()
    options_list = []
    for i in options_dict:
        options_list.append(i["name"])
    options_list.insert(0, "")

    return options_list

breed_selected = st.selectbox("Search By Breed", options=generate_breeds(), index=None)

def generate_breed_info(breed_selected):
    breed_id = generate_list_of_breeds()
    breed = []

    for i in breed_id:
        if breed_selected == i["name"]:
            breed.append(i)
    return breed

def generate_chart(breed):
    info_list = [breed[0]["adaptability"], breed[0]["intelligence"], breed[0]["affection_level"], breed[0]["child_friendly"], breed[0]["energy_level"], breed[0]["health_issues"], breed[0]["shedding_level"], breed[0]["social_needs"], breed[0]["vocalisation"], breed[0]["hypoallergenic"]]

    data = pd.DataFrame(
        {
            "Attributes": ["Adaptability", "Intelligence", "Affection", "Child-Friendly", "Energy Level", "Health Issues", "Shedding Level", "Social Needs", "Vocalization", "Hypoallergenic"],
            "Score": [i for i in info_list],
        }
    )
    return(
        st.bar_chart(data, x="Attributes", y="Score")
    )

if breed_selected:
    breed = generate_breed_info(breed_selected)
    st.header(breed[0]["name"])
    get_image_for_breed(breed[0]["reference_image_id"], breed)
    generate_chart(breed)
    st.write(breed[0]["description"])
    
    if st.button('Add to Favorites!'):
        img_id = (breed[0]["reference_image_id"])
        create_favorite(api_key, str(img_id))

else: 
    st.warning("No data available for this breed.")