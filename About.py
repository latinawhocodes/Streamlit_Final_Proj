import streamlit as st
import pandas as pd
import numpy as np
from assets import *
import requests
from helpers import image_map, get_home_image 

st.set_page_config(
    page_title="About"
)


st.title("Welcome to the Cat Factstory!")


col1, col2, col3 = st.columns(3)
with col2:
    st.image(get_home_image(), width=200)

st.markdown("***Meow ~*** *Do you want to learn more about your cat's breed? Do you want to adopt a cat and not sure which breed is for you? Or do you just want to see pictures of adorable cats and learn random facts about them? The Cat Factstory is here for all your feline needs!*")

@st.cache_data
def generate_cat_facts():
    #No api key required for this API
    facts_url = "https://cat-fact.herokuapp.com/facts?animal_type=cat&category=history"
    facts = requests.get(facts_url).json()
    fact_list = []

    st.markdown(
    '''
     ### **Some Random Cat Facts** \:cat:
    '''
    )

    for i in facts:
        fact_list.append(i["text"])
        st.markdown('''    - ''' + (i["text"]))

generate_cat_facts()