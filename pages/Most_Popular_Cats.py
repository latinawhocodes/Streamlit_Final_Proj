from helpers import api_key, breeds_map, get_breed_info, color_arr
import requests
import streamlit as st
import pandas as pd
from lat_long_by_country import *

@st.cache_data
def popular_breeds(breed_map, api_key):
    breed_info = {}

    for breed in breed_map.values():
        breed_data = get_breed_info(breed, api_key)
        breed_info[breed] = {"name": breed_data["name"], "description": breed_data["description"], "origin": breed_data["origin"], "life_expectancy": breed_data["life_span"], "weight_range": breed_data["weight"]["imperial"], "origin_lat": "", "origin_long": "", "adaptability": breed_data["adaptability"], "intelligence": breed_data["intelligence"], "affection": breed_data["affection_level"], "child_friendly": breed_data["child_friendly"], "energy_level": breed_data["energy_level"], "health_issues": breed_data["health_issues"], "shedding_level": breed_data["shedding_level"], "social_needs": breed_data["social_needs"], "vocalization": breed_data["vocalisation"], "hypoallergenic": breed_data["hypoallergenic"], "breed_id": breed}
    return breed_info

st.header("Most Popular Cat Breeds")
st.write("The most popular cat breeds around the world (Top 10)!")


data = popular_breeds(breeds_map, api_key)
df = pd.DataFrame(
    {
        "Breed": [data[i]["name"] for i in breeds_map.values()],
        "Origin": [data[i]["origin"] for i in breeds_map.values()],
        "Weight Range": [data[i]["weight_range"] for i in breeds_map.values()],
        "Life Expectancy": [data[i]["life_expectancy"] for i in breeds_map.values()],
    }
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

def set_lat_long(countries, cat_map):
    for i in countries["c_codes"]:
        for (key,value) in cat_map.items():
            if value['origin'] in i["country"]:
                value['origin_lat'] = i["latitude"]
                value['origin_long'] = i['longitude']
    return data

def prepare_data(countries, data):   
    data = set_lat_long(countries, data)
    # st.write(data)

prepare_data(countries, data)
lat_list = []
long_list = []

for i in data.values():
    lat_list.append(i["origin_lat"])
    long_list.append(i["origin_long"])


world_map = pd.DataFrame({
    "latitude": [i for i in lat_list],
    "longitude": [i for i in long_list],
    "col3": [i for i in color_arr]
})

st.map(world_map,
    latitude='latitude',
    longitude='longitude', 
    color="col3")

def generate_chart_data(breeds_map, data):
    attributes = ["Intelligence"]
    int_list = []
    breed_list = []

    for i in breeds_map.values():
        int_list.append(data[i]["intelligence"])
        breed_list.append(data[i]["name"])

    chart_data = pd.DataFrame(
        {
            "Scores": [i for i in int_list],
            "Breeds": [i for i in breed_list]
        }
    )

    st.write("Intelligence of Most Popular Cat Breeds")

    return(
        st.bar_chart(chart_data, x="Breeds", y="Scores", color="Breeds")
    )

generate_chart_data(breeds_map, data)
