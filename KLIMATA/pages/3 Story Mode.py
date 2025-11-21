import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import json
import streamlit.components.v1 as components

st.title("ArcGIS Story Mode")
st.markdown("*Your Ultimate Guided Experience with KLIMATA!*")

st.markdown("""
<style>

/* --- Make sidebar text white --- */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* --- Make navigation tab text white --- */
[data-testid="stNavigation"] div[data-testid="stSidebarNav"] * {
    color: white !important;
}

/* Optional: Make sidebar background dark for contrast */
[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
}

</style>
""", unsafe_allow_html=True)

# Set page config to wide layout
st.set_page_config(layout="wide")

hide_streamlit_style = """
    <style>
    /* Hide header and hamburger menu */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.sidebar.image("klimata_logo.png", width=1000)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

components.html(
    """
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    ">
        <iframe 
            src="https://storymaps.arcgis.com/stories/47240a5087554d809c247692e43b3ab0"
            width="100%" 
            height="900px"
            style="border:none; border-radius: 10px;"
            allowfullscreen 
            allow="geolocation">
        </iframe>
    </div>
    """,
    height=950,  # slightly taller than iframe to include padding
)

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://encycolorpedia.com/d2e8ba.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

sidebar_bg = """
<style>
[data-testid="stSidebar"] {
    background-image: url("https://www.dictionary.com/e/wp-content/uploads/2016/01/hunter-green-color-paint-code-swatch-chart-rgb-html-hex.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
"""
st.markdown(sidebar_bg, unsafe_allow_html=True)
