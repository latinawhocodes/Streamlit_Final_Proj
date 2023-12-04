from helpers import api_key2, breeds_map, get_breed_info, color_arr, get_home_image
import requests
import streamlit as st
import pandas as pd
from lat_long_by_country import *

st.info("You can search for breeds by characteristics too! If you're not sure which breed you want, search for characteristics you're interested in! Or, if you know which breed is for you, type the breed name to get more information!")

col1, col2, col3 = st.columns(3)
with col2:
    st.image(get_home_image(), width=200)

searched_name = st.text_input(
    'Search By Breed Name', max_chars=50, placeholder='Breed Name', help="You don't have to search the complete name, you can search for a portion of one too, at least two letters."
)

attribute_options = st.multiselect(
    'What attributes are most important to you? (Pick maximum of 2)',
    ['Fluffy', 'Playful', 'Serious', 'Affectionate' ], help="Optional"
)

max_weight = st.slider(
     'Weight Range',
     0, 50, help="Optional"
)

def send_req(api_key2, url):
    base_url = 'https://api.api-ninjas.com/v1/cats?'
    construct_url = base_url+url

    response = requests.get(construct_url, headers={'X-Api-Key': api_key2})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    # st.write(response)
    return response.json()

if searched_name:
    name_url = f"name={searched_name}"
    found = send_req(api_key2, name_url)

    if found:
        cat_dict = {} 
        for i in found:
            st.header(i["name"])
            st.write(f"The " + i["name"] + " originates in " + i["origin"] + " and has a weight range of " + str(i["min_weight"]) + " to " + str(i["max_weight"]) + " pounds.") 
            st.image(i["image_link"], caption=i["name"], width=150)
            st.write("General Attributes: ")
            st.markdown('''    - ''' + "Shedding Level: " + str(i["shedding"]))
            st.markdown('''    - ''' + "General Health Level: " + str(i["general_health"]))
            st.markdown('''    - ''' + "Playfulness: " + str(i["playfulness"]))
            st.markdown('''    - ''' + "Child Friendly: " + str(i["children_friendly"]))
            st.markdown('''    - ''' + "Pet Friendly: " + str(i["other_pets_friendly"]))
            st.markdown('''    - ''' + "Intelligence: " + str(i["intelligence"]))


if len(attribute_options) > 2:
    st.error("Sorry! You can only pick two options!")

if attribute_options:
    fluffy = []
    playful = []
    serious = []
    affectionate = []
    
    for i in attribute_options:
        if i == "Fluffy":
            url = f"shedding={5}"
            cats = send_req(api_key2, url)
            
            for c in cats: 
                fluffy.append(c["name"])

        if i == "Playful":
            if "Serious" in attribute_options:
                st.warning("No results found, please try again.")
            else: 
                url = f"playfulness={5}"
                cats = send_req(api_key2, url)
                
                for c in cats: 
                    playful.append(c["name"])

        if i == "Serious":
            if "Playful" in attribute_options or "Affectionate" in attribute_options:
                st.warning("No results found, please try again.")
            else:
                url = f"family_friendly={1}"
                cats = send_req(api_key2, url)

                for c in cats: 
                    serious.append(c["name"])
        
        if i == "Affectionate":
            st.write("Affectionate")
            url = f"family_friendly={5}"

            if "Serious" in attribute_options:
                st.warning("No results found, please try again.")
            else: 
                cats = send_req(api_key2, url)
                affectionate.append(cats)

                for c in cats: 
                    affectionate.append(c["name"])

    #search results for attribute_options
    def get_results(list1, list2):
        mySet = set(list1) - set(list2)

        st.write("Matching Breeds: ")
        for i in mySet:
            st.markdown('''    - ''' + (i))
    
    if fluffy and playful:
        get_results(fluffy, playful)

    if fluffy and serious:
        st.warning("No matches!")

    if fluffy and affectionate:
        get_results(fluffy, affectionate)

    if serious and fluffy:
        get_results(fluffy, serious)

if max_weight:
    max_url = f"max_weight={max_weight}"
    max_found = send_req(api_key2, max_url)

    if max_found:
        cat_dict = {}  
        for i in max_found:
            st.header(i["name"])
            st.write(f"The " + i["name"] + " originates in " + i["origin"] + " and has a weight range of " + str(i["min_weight"]) + " to " + str(i["max_weight"]) + " pounds.") 
            st.image(i["image_link"], caption=i["name"], width=150)
    else:
        st.warning("Oops! No available cats with that weight!")


display_slider = st.checkbox('Search By Friendliness to Other Pets');
if display_slider:
    pet_friendly = st.select_slider(
        'Friendliness to Other Pets', ["", "Not at All", "A Little", "Average", "Friendly", "Super Friendly"], help="Optional"
    )

    if pet_friendly:
        if pet_friendly == "Not at All":
            friendly_url = f"other_pets_friendly={1}"
            friendly_res = send_req(api_key2, friendly_url)

        if pet_friendly == "A Little":
            friendly_url = f"other_pets_friendly={2}"
            friendly_res = send_req(api_key2, friendly_url)

        if pet_friendly == "Average":
            friendly_url = f"other_pets_friendly={3}"
            friendly_res = send_req(api_key2, friendly_url)

        if pet_friendly == "Friendly":
            friendly_url = f"other_pets_friendly={4}"
            friendly_res = send_req(api_key2, friendly_url)

        if pet_friendly == "Super Friendly":
            friendly_url = f"other_pets_friendly={5}"

            friendly_res = send_req(api_key2, friendly_url)

        if friendly_res:
            cat_dict = {}  
            for i in friendly_res:
                st.header(i["name"])
                st.write(f"The " + i["name"] + " originates in " + i["origin"] + " and has a weight range of " + str(i["min_weight"]) + " to " + str(i["max_weight"]) + " pounds.") 
                st.image(i["image_link"], caption=i["name"], width=150)
        else:
            st.warning("Oops! No available cats with that temperament!")

