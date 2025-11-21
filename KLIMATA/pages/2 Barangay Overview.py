import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import json
import streamlit.components.v1 as components
import math 
import os

st.set_page_config(layout="wide")
st.title("Barangay Overview")
st.markdown("*An In-depth look of Iloilo City's Barangays!*")
hide_streamlit_style = """
    <style>
    /* Hide header and hamburger menu */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


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
st.sidebar.image("klimata_logo.png", width=1000)
st.markdown(sidebar_bg, unsafe_allow_html=True)

st.markdown("""
<style>

/* --- NAVIGATION TABS (white text) --- */
[data-testid="stSidebarNav"] * {
    color: white !important;
}

/* --- SELECTBOX TEXT (black text only) --- */

/* Selected value */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    color: black !important;
}

/* Dropdown options */
section[data-testid="stSidebar"] .stSelectbox span {
    color: black !important;
}

/* Placeholder text */
section[data-testid="stSidebar"] .stSelectbox .css-1wa3eu0-placeholder {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# --- Load Urban Risk GeoJSON ---
with open("climate_risk.geojson", "r") as f:
    urban = json.load(f)

# --- Sidebar: search for barangay ---
barangay_names = [feature['properties']['location_adm4_en'] for feature in urban['features']]
selected_barangay = st.sidebar.selectbox("Select Barangay", barangay_names)

street_view_urls = {
    "Abeto Mirasol Taft South (Quirino Abeto)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763696870421!5m2!1sen!2sph!6m8!1m7!1stjjgARVYVGHayI6K7yuAVw!2m2!1d10.71777077160674!2d122.5442758454376!3f142.47798!4f0!5f0.7820865974627469",
    "Aguinaldo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763696940219!5m2!1sen!2sph!6m8!1m7!1sPWf07XwAgL0qJbe6BVWvyw!2m2!1d10.70657547668952!2d122.5721818934322!3f25.830337940041392!4f0!5f0.7820865974627469",
    "Airport (Tabucan Airport)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697038367!5m2!1sen!2sph!6m8!1m7!1srjS_Mwm7EXc0bE8WzKA5ow!2m2!1d10.70591713350941!2d122.5417542060075!3f122.20980908212748!4f0!5f0.7820865974627469",
    "Alalasan Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697110784!5m2!1sen!2sph!6m8!1m7!1saS8snGU-gV9_8Qi7F9KsoA!2m2!1d10.70679970173169!2d122.5740446812991!3f261.19787746321293!4f12.566308577926577!5f0.7820865974627469",
    "Arguelles": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697189517!5m2!1sen!2sph!6m8!1m7!1s3XlC41QlP-H3ADAWNgCv1Q!2m2!1d10.72840068196367!2d122.5528658769542!3f240.59607055245235!4f0!5f0.7820865974627469",
    "Arsenal Aduana": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697224511!5m2!1sen!2sph!6m8!1m7!1s5ZP8MKkq2nJUsXO3SxWn5A!2m2!1d10.69518709377865!2d122.5715041782461!3f157.92361!4f0!5f0.7820865974627469",
    "Bakhaw": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697268723!5m2!1sen!2sph!6m8!1m7!1s3vC9YDBBNwDItbj91lKWPw!2m2!1d10.71889104580178!2d122.5534488654633!3f62.87062264335152!4f0!5f0.7820865974627469",
    "Balabago": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697314758!5m2!1sen!2sph!6m8!1m7!1svM7GtGZkfUKg-bimv5KTKg!2m2!1d10.742494761058158!2d122.57410801618764!3f229.36908!4f0!5f0.7820865974627469",
    "Balantang": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697355980!5m2!1sen!2sph!6m8!1m7!1sOl117soHX4DaSZr1TDiAMA!2m2!1d10.75821630047038!2d122.5753876487525!3f91.94799!4f0!5f0.7820865974627469",
    "Baldoza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697384083!5m2!1sen!2sph!6m8!1m7!1s_CX_pVOWXOJDkNg-kQlbOw!2m2!1d10.71306820414766!2d122.5788531904911!3f114.54025!4f0!5f0.7820865974627469",
    "Bantud": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697404658!5m2!1sen!2sph!6m8!1m7!1sCAoSFkNJSE0wb2dLRUlDQWdJRHEtYWYzTnc.!2m2!1d10.70991359492768!2d122.5649915354568!3f223.1795!4f0!5f0.7820865974627469",
    "Banuyao": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697451192!5m2!1sen!2sph!6m8!1m7!1sSTJDErbSuJit3vW2WuUsYg!2m2!1d10.7102230275178!2d122.5648456969986!3f69.08924953421811!4f-2.3754994754034584!5f0.7820865974627469",
    "Baybay Tanza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697494015!5m2!1sen!2sph!6m8!1m7!1skTF_80HP3S5ilL9lvhy6_w!2m2!1d10.69316530908415!2d122.5572558595011!3f277.07953!4f0!5f0.7820865974627469",
    "Benedicto (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697865319!5m2!1sen!2sph!6m8!1m7!1shnIP1_2WcdZdj_7DILazww!2m2!1d10.72485544217268!2d122.5588312782558!3f13.353957!4f0!5f0.7820865974627469",
    "Bito-on": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697937051!5m2!1sen!2sph!6m8!1m7!1smkQYhHAvZvJIT9TG-7B8ig!2m2!1d10.75505343311181!2d122.5877997809645!3f212.63654!4f0!5f0.7820865974627469",
    "Bolilao": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763697971429!5m2!1sen!2sph!6m8!1m7!1suL1DtiTrd5hQz3Dbsa0oIQ!2m2!1d10.71274780358624!2d122.5556575466019!3f311.606253755745!4f0!5f0.7820865974627469",
    "Bonifacio (Arevalo)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698042592!5m2!1sen!2sph!6m8!1m7!1sMAN3v65mjiekRJ_DWREYMA!2m2!1d10.68590356735969!2d122.5100218926592!3f268.8216143843202!4f1.605090521798644!5f0.7820865974627469",
    "Bonifacio Tanza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698089460!5m2!1sen!2sph!6m8!1m7!1s-RgzdkMc_URpxXJqvkcA7Q!2m2!1d10.69233151772085!2d122.559007934237!3f240.57015232078626!4f-2.110397665228348!5f0.7820865974627469",
    "Buhang": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698155569!5m2!1sen!2sph!6m8!1m7!1s2Bd3d6LLW2zQHG8Yd0OPzA!2m2!1d10.75721411597473!2d122.5747367897426!3f291.2955898802865!4f0!5f0.7820865974627469",
    "Buhang Taft North": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698209408!5m2!1sen!2sph!6m8!1m7!1sL_BQ5DONGIUc7cV9-Il8hQ!2m2!1d10.71789007864341!2d122.5495998724342!3f292.40549231383636!4f1.0630415776667803!5f0.7820865974627469",
    "Buntatala": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698241927!5m2!1sen!2sph!6m8!1m7!1ssDdhPJY703yF6Bj29nynjw!2m2!1d10.76951403714786!2d122.5802150776215!3f77.1401933393845!4f0!5f0.7820865974627469",
    "Burgos-Mabini-Plaza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698276915!5m2!1sen!2sph!6m8!1m7!1sxeXroT8QJxqIcX6LKbt4pA!2m2!1d10.71281538890926!2d122.5691957369266!3f23.245701812489017!4f-2.2666767420702314!5f0.7820865974627469",
    "Caingin": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698321159!5m2!1sen!2sph!6m8!1m7!1sBPEiZNlQDL8yjtBxpB1FNQ!2m2!1d10.71873053880343!2d122.5754023174089!3f224.2141951602436!4f-5.276416701656743!5f0.7820865974627469",
    "Calahunan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698387476!5m2!1sen!2sph!6m8!1m7!1s6wX8YUSquFCrypWsBZs9Lg!2m2!1d10.71309571998749!2d122.5286718571979!3f310.2909912890628!4f-8.787673111475044!5f0.7820865974627469",
    "Calaparan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698470510!5m2!1sen!2sph!6m8!1m7!1sfAjYfryaQOZYVfmhPDGmKg!2m2!1d10.68077993958947!2d122.5300436402363!3f94.9658522292129!4f-25.552052054193595!5f0.7820865974627469",
    "Calubihan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698550695!5m2!1sen!2sph!6m8!1m7!1s2_DhAUuZln0QGLxQBxMxiQ!2m2!1d10.72052545971662!2d122.5520256945591!3f354.3393549424847!4f-10.304319668602076!5f0.7820865974627469",
    "Calumpang": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15682.594979431116!2d122.52669944010596!3d10.684348830635193!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aef002652c2f97%3A0x3489bd92d895b41a!2sCalumpang%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763698576808!5m2!1sen!2sph",
    "Camalig": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698615803!5m2!1sen!2sph!6m8!1m7!1s045bbycyddVlB9Rz8aWYfA!2m2!1d10.75593202817633!2d122.5707021146257!3f140.0087732661205!4f0!5f0.7820865974627469",
    "Cochero": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698676058!5m2!1sen!2sph!6m8!1m7!1sKna34SKZBaV_uW-KBNL5rg!2m2!1d10.6932224055548!2d122.5525340337706!3f334.58965830121576!4f0!5f0.7820865974627469",
    "Compania": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698751670!5m2!1sen!2sph!6m8!1m7!1ssPf5FkkL1w1VsRTKsLO-3A!2m2!1d10.68952549965432!2d122.5394495906439!3f277.19712402464785!4f-1.4488818614303085!5f0.7820865974627469",
    "Concepcion-Montes": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7841.0498554473015!2d122.57595539996167!3d10.693935157623098!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee5783e854561%3A0x62c8ae08d5a607fe!2sConcepcion-Montes%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763698767561!5m2!1sen!2sph",
    "Cuartero": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698791576!5m2!1sen!2sph!6m8!1m7!1sASrPXbq96-RnLuIBFG9Kzw!2m2!1d10.72464559702345!2d122.5522658829894!3f251.06507756094754!4f-11.750423629397346!5f0.7820865974627469",
    "Cubay": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15680.309295888375!2d122.55586599012331!3d10.728519479967943!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee4e3cdf4a3b7%3A0xa2f4183241e3681e!2sCubay%2C%20Jaro%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763698814338!5m2!1sen!2sph",
    "Danao": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698837390!5m2!1sen!2sph!6m8!1m7!1sglwzecVP3_SD9L2hjxaagA!2m2!1d10.70080670540231!2d122.5676975351133!3f316.0333!4f0!5f0.7820865974627469",
    "Delgado-Jalandoni-Bagumbayan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698881109!5m2!1sen!2sph!6m8!1m7!1s58WapU_SfWaznLCnE_00KQ!2m2!1d10.69604590933308!2d122.5606250948539!3f67.68237427150478!4f0!5f0.7820865974627469",
    "Democracia": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698899033!5m2!1sen!2sph!6m8!1m7!1sU0QZdbIO78H3hxicqcGhKQ!2m2!1d10.7275363425233!2d122.5575572232974!3f254.81575!4f0!5f0.7820865974627469",
    "Desamparados": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698926450!5m2!1sen!2sph!6m8!1m7!1sPmyHZEisutNmdSS8uWjYaA!2m2!1d10.72167630433334!2d122.5552079950836!3f123.6978!4f0!5f0.7820865974627469",
    "Divinagracia": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763698960401!5m2!1sen!2sph!6m8!1m7!1sdDb2LXUTzStY4VPEL3rnCw!2m2!1d10.70962396482581!2d122.5714515416633!3f278.5085285084558!4f-11.771241173755826!5f0.7820865974627469",
    "Don Esteban-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699090453!5m2!1sen!2sph!6m8!1m7!1sz2Owmgk9BFxntwvROs7DRQ!2m2!1d10.70451963941386!2d122.5766282645981!3f263.84958621035787!4f0!5f0.7820865974627469",
    "Dulonan": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15682.419340888002!2d122.51538299010726!3d10.687749430583787!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aef008a228fb85%3A0x138743dc675a464a!2sDulonan%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763699113439!5m2!1sen!2sph",
    "Dungon": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699140180!5m2!1sen!2sph!6m8!1m7!1sfKgo2aq4I1KEFHc8aB6axg!2m2!1d10.68614570256319!2d122.5263411398171!3f155.80072442497823!4f0!5f0.7820865974627469",
    "Dungon A": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699159933!5m2!1sen!2sph!6m8!1m7!1sEvi3_kRg0cgObw6ITdt8wA!2m2!1d10.72821678883949!2d122.5488560700194!3f219.46144817779947!4f0!5f0.7820865974627469",
    "Dungon B": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699185657!5m2!1sen!2sph!6m8!1m7!1s4_ezLk7qPp1oAoI6XUFXXw!2m2!1d10.72994090517128!2d122.5442808515409!3f153.02004696121645!4f2.2799526354039443!5f0.7820865974627469",
    "East Baluarte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699212687!5m2!1sen!2sph!6m8!1m7!1smsRArb1rNCY_wWbtJsP0Ew!2m2!1d10.69285419225631!2d122.5492582659998!3f16.72994924563109!4f-8.91899090915551!5f0.7820865974627469",
    "East Timawa": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699238766!5m2!1sen!2sph!6m8!1m7!1sZo6ER5DbwalNx2q47NJNOQ!2m2!1d10.69637494175967!2d122.5513627785097!3f40.81669709147673!4f0!5f0.7820865974627469",
    "Edganzon": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699271175!5m2!1sen!2sph!6m8!1m7!1siosyOBHsK20bCj8wcf3Xvw!2m2!1d10.69694724846848!2d122.5663448030034!3f18.74418341330299!4f0!5f0.7820865974627469",
    "El 98 Castilla (Claudio Lopez)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699290068!5m2!1sen!2sph!6m8!1m7!1sCHtwPY66k7RLdrhqgzaSlQ!2m2!1d10.72269969509654!2d122.5554795040663!3f202.09416!4f0!5f0.7820865974627469",
    "Fajardo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699309092!5m2!1sen!2sph!6m8!1m7!1si0igzG3S38cckrRKhJ8t9A!2m2!1d10.72688342494282!2d122.5532185185077!3f200.59676!4f0!5f0.7820865974627469",
    "Flores": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1960.2711287526083!2d122.5606887738985!3d10.692593940583688!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee566d10d0cdf%3A0xc79299b732c5f23!2sFlores%2C%20Iloilo%20City%20Proper%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763699323830!5m2!1sen!2sph",
    "General Hughes-Montes": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699344520!5m2!1sen!2sph!6m8!1m7!1se0lZFP5hYijRzFrxi_dRIA!2m2!1d10.69076522183911!2d122.5748765742049!3f142.93538!4f0!5f0.7820865974627469",
    "Gloria": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699370182!5m2!1sen!2sph!6m8!1m7!1srWnxR9q_o2eRmoc6hC8KHQ!2m2!1d10.69321714857247!2d122.5626936497748!3f345.15566757377337!4f0!5f0.7820865974627469",
    "Gustilo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699441337!5m2!1sen!2sph!6m8!1m7!1sJPH-x6fxaJYhrmuQzgQ45g!2m2!1d10.71610741952914!2d122.5702239799298!3f3.8891047468928264!4f-10.027728310966168!5f0.7820865974627469",
    "Guzman-Jesena": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699470928!5m2!1sen!2sph!6m8!1m7!1s8GxPfaoRJEbeLYFof4rU5g!2m2!1d10.7214560765273!2d122.5330846160639!3f245.00418!4f0!5f0.7820865974627469",
    "Habog-habog Salvacion": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699494459!5m2!1sen!2sph!6m8!1m7!1sF78ZLDlGW43CqpvKFUI56Q!2m2!1d10.69206146611806!2d122.5454014357863!3f305.2093174753038!4f-16.061595964874712!5f0.7820865974627469",
    "Hibao-an Norte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699512749!5m2!1sen!2sph!6m8!1m7!1swxV_TDELeHdsHwMj8AS5Uw!2m2!1d10.73782563700113!2d122.5188205748938!3f136.81363184142577!4f-3.9903176591452905!5f0.7820865974627469",
    "Hibao-an Sur": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699531492!5m2!1sen!2sph!6m8!1m7!1s26ocYsiObGFazhC4kQXG1Q!2m2!1d10.72694556033042!2d122.527267511059!3f58.969807!4f0!5f0.7820865974627469",
    "Hinactacan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699567857!5m2!1sen!2sph!6m8!1m7!1sS9vyQbbvQv9Zq-GItFrDng!2m2!1d10.73310812796962!2d122.592841964716!3f316.02370283900615!4f2.211192131862589!5f0.7820865974627469",
    "Hipodromo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699602310!5m2!1sen!2sph!6m8!1m7!1saTRXaG1CX_LD31pYujjmSQ!2m2!1d10.6958136298433!2d122.5622981507899!3f279.46343018442053!4f-14.768873195726115!5f0.7820865974627469",
    "Inday": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699660558!5m2!1sen!2sph!6m8!1m7!1sk9prhx4aZeQcOlBoa97VMA!2m2!1d10.70004558372196!2d122.55588616209!3f272.74992764272685!4f5.680003501822455!5f0.7820865974627469",
    "Infante": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699751954!5m2!1sen!2sph!6m8!1m7!1sS4IMHazOLWiqYRtUygT5eA!2m2!1d10.69400015554533!2d122.5551282510515!3f80.62911374920306!4f0!5f0.7820865974627469",
    "Jalandoni Estate-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699777990!5m2!1sen!2sph!6m8!1m7!1soFlTCXNMtjZ8isyQCon7QA!2m2!1d10.70176608417472!2d122.5760076996773!3f211.2277362363925!4f0!5f0.7820865974627469",
    "Jalandoni-Wilson": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699804094!5m2!1sen!2sph!6m8!1m7!1sqJXV52et1GRYU_F8snP4aw!2m2!1d10.69487260157491!2d122.5609796948733!3f114.37224312049077!4f-6.031940938080538!5f0.7820865974627469",
    "Javellana": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699974641!5m2!1sen!2sph!6m8!1m7!1sZ6LLNTK6upXbyPTegEq4eQ!2m2!1d10.71708734786604!2d122.56271168580422!3f313.89072!4f0!5f0.7820865974627469",
    "Jereos": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763699995593!5m2!1sen!2sph!6m8!1m7!1s_tKYlJAk-8fKlssLUxpmcw!2m2!1d10.71801342914855!2d122.5675532537346!3f90.02239!4f0!5f0.7820865974627469",
    "Kahirupan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700015421!5m2!1sen!2sph!6m8!1m7!1s7DLrMhqFEydrU6Bncg3kXw!2m2!1d10.6929952302461!2d122.5616847489852!3f271.55522899665533!4f0!5f0.7820865974627469",
    "Kasingkasing": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700094957!5m2!1sen!2sph!6m8!1m7!1s4fTjCMefPImT_0VTYPMs1g!2m2!1d10.69583239491801!2d122.5476249608725!3f181.90039286087028!4f0!5f0.7820865974627469",
    "Katilingban": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700128205!5m2!1sen!2sph!6m8!1m7!1s9S3ATXoQt_4s1sVgDPJCSA!2m2!1d10.69622718046497!2d122.5442015306693!3f260.40697201727215!4f0!5f0.7820865974627469",
    "Kauswagan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700153195!5m2!1sen!2sph!6m8!1m7!1s2lD0MOzvns9v6yh0N5duTg!2m2!1d10.6945971385017!2d122.5663307371199!3f34.83821246542381!4f-10.26447537175946!5f0.7820865974627469",
    "Laguda": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700179785!5m2!1sen!2sph!6m8!1m7!1sRez7T_WPrnJgvxWd-oiJFg!2m2!1d10.70736552921003!2d122.5681352104103!3f63.910661326380385!4f-17.601628449224464!5f0.7820865974627469",
    "Lanit": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700230754!5m2!1sen!2sph!6m8!1m7!1s_jMFwQ8xpQkdJ42Weifg8g!2m2!1d10.768463202148276!2d122.56741794661309!3f25.73943974872272!4f0!5f0.7820865974627469",
    "Lapuz Norte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700256405!5m2!1sen!2sph!6m8!1m7!1s0QGfyOxxb4W3KpZEZV3uBw!2m2!1d10.70231303662692!2d122.5783858789157!3f60.25129008286681!4f0!5f0.7820865974627469",
    "Lapuz Sur": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700292660!5m2!1sen!2sph!6m8!1m7!1scEvEPnkTvIXrbGziJY6s2g!2m2!1d10.70380785001617!2d122.5714922703003!3f173.77384128677238!4f-8.522480804652034!5f0.7820865974627469",
    "Legaspi dela Rama": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700331897!5m2!1sen!2sph!6m8!1m7!1sNAGVNSPXeft4Ce5s4XUcmg!2m2!1d10.69728644239121!2d122.5757741240136!3f347.9206667056076!4f3.954849367377733!5f0.7820865974627469",
    "Liberation": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700360314!5m2!1sen!2sph!6m8!1m7!1sWJZJYPmXk6suVWeY8fsQng!2m2!1d10.69656410960624!2d122.5642251477484!3f17.118225639637416!4f-5.315329211199568!5f0.7820865974627469",
    "Libertad, Santa Isabel": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700391626!5m2!1sen!2sph!6m8!1m7!1sRu7xAArwFHtVs9CGLXbymQ!2m2!1d10.72485424539999!2d122.5556641919064!3f243.11988496695716!4f0!5f0.7820865974627469",
    "Libertad-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700405730!5m2!1sen!2sph!6m8!1m7!1sXiGjDNUoHw5wQDEccjr_ag!2m2!1d10.69994539813631!2d122.5750451781756!3f284.73526!4f0!5f0.7820865974627469",
    "Loboc-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700424404!5m2!1sen!2sph!6m8!1m7!1sdQNfvptbbJC5cLfNQz6COQ!2m2!1d10.70641661339909!2d122.5815231074273!3f8.290879334851455!4f-14.344310224775057!5f0.7820865974627469",
    "Lopez Jaena (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700438528!5m2!1sen!2sph!6m8!1m7!1sJ1sA8O_md8PUFprsjWfWsA!2m2!1d10.73049789525393!2d122.5524084595452!3f227.56807!4f0!5f0.7820865974627469",
    "Lopez Jaena Norte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700455147!5m2!1sen!2sph!6m8!1m7!1szeb6fqu1F20t5k4F7DhJzQ!2m2!1d10.71405758815471!2d122.5740695320502!3f135.52534791273155!4f0!5f0.7820865974627469",
    "Lopez Jaena Sur": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700470650!5m2!1sen!2sph!6m8!1m7!1ssWwkzTmzVX_EgOwM15F16Q!2m2!1d10.71113675451006!2d122.5747096094086!3f164.42772!4f0!5f0.7820865974627469",
    "Luna (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700483387!5m2!1sen!2sph!6m8!1m7!1skarMLzTndWxZaCJ5OC8_QQ!2m2!1d10.72240197270984!2d122.558860102457!3f312.41483!4f0!5f0.7820865974627469",
    "Luna (La Paz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700495391!5m2!1sen!2sph!6m8!1m7!1s2aca0JMPTWb30Wur-GT22A!2m2!1d10.70613380682376!2d122.5648599356737!3f216.52397!4f0!5f0.7820865974627469",
    "M. V. Hechanova": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15679.32231044498!2d122.55376269013085!3d10.74753742968083!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee494a04a3245%3A0x8bede94fe0ab0fd!2sM.%20V.%20Hechanova%2C%20Jaro%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763700505462!5m2!1sen!2sph",
    "Mabolo-Delgado": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3920.484351690779!2d122.55531840745513!3d10.697074839402852!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee55d2e5fe6d9%3A0x6beb071d7ef6ca55!2sMabolo-delgado%2C%20Iloilo%20City%20Proper%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763700516860!5m2!1sen!2sph",
    "Macarthur": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700570226!5m2!1sen!2sph!6m8!1m7!1swMOQ4BHavSiclOdM4OyLuA!2m2!1d10.70889298173737!2d122.5702363194742!3f231.77795!4f0!5f0.7820865974627469",
    "Magdalo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700590335!5m2!1sen!2sph!6m8!1m7!1szqmW5_aeYHPuKih-umM3jQ!2m2!1d10.71107330783436!2d122.5667041295866!3f68.007576!4f0!5f0.7820865974627469",
    "Magsaysay": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700625528!5m2!1sen!2sph!6m8!1m7!1sDVqq6cYHlr97bTK8hTCT7A!2m2!1d10.69455527421243!2d122.5690633658619!3f165.35103!4f0!5f0.7820865974627469",
    "Magsaysay Village": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700640291!5m2!1sen!2sph!6m8!1m7!1sGIr-syYVQdAYs9wDZC5DcA!2m2!1d10.71128466467206!2d122.5619576217614!3f62.436085!4f0!5f0.7820865974627469",
    "Malipayon-Delgado": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700826773!5m2!1sen!2sph!6m8!1m7!1syEspeF1bqlIWbqbXLyqHIw!2m2!1d10.69670023610473!2d122.5593045464602!3f232.27788277756565!4f0!5f0.7820865974627469",
    "Mansaya-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700844797!5m2!1sen!2sph!6m8!1m7!1sOTvhI00GIT7poJBEJzCjMw!2m2!1d10.70029868945154!2d122.5853046527923!3f95.47804996376253!4f0!5f0.7820865974627469",
    "Marcelo H. del Pilar": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700860407!5m2!1sen!2sph!6m8!1m7!1sH1sSK2bYkQjvliYi1e9STw!2m2!1d10.72445698654891!2d122.5649843729812!3f282.78403!4f0!5f0.7820865974627469",
    "Maria Clara": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700877604!5m2!1sen!2sph!6m8!1m7!1sW-Myu0JwhCbMPBejCA2yoQ!2m2!1d10.6911114146711!2d122.5694160385906!3f29.950165!4f0!5f0.7820865974627469",
    "Maria Cristina": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3920.0707780115345!2d122.55261245745601!3d10.729024439372713!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee4df3981485f%3A0x7330cca027bdd873!2sMaria%20Cristina%2C%20Jaro%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763700889779!5m2!1sen!2sph",
    "Mohon": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700914147!5m2!1sen!2sph!6m8!1m7!1sQvw47ETlZCBB1bRyxRyBMQ!2m2!1d10.69298486928199!2d122.5013135637865!3f196.6535!4f0!5f0.7820865974627469",
    "Molo Boulevard": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700953049!5m2!1sen!2sph!6m8!1m7!1s7YxYodUMUI9fBL_9TPVfAQ!2m2!1d10.68842137666339!2d122.5502028162658!3f49.38902795891063!4f0!5f0.7820865974627469",
    "Monica Blumentritt": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763700976544!5m2!1sen!2sph!6m8!1m7!1sKowiJJ1TcxivImFJj46T6w!2m2!1d10.69657937958003!2d122.5783517968404!3f344.3187975465571!4f0!5f0.7820865974627469",
    "Montinola": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701022109!5m2!1sen!2sph!6m8!1m7!1sygsnFdJaTx9ncIvVLkNVcA!2m2!1d10.71464876830419!2d122.5607911330769!3f45.569633!4f0!5f0.7820865974627469",
    "Muelle Loney-Montes": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701034967!5m2!1sen!2sph!6m8!1m7!1symFA16hbyFesDVaaXKCmSA!2m2!1d10.69489428875703!2d122.5743709332191!3f149.30173!4f0!5f0.7820865974627469",
    "Nabitasan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701056294!5m2!1sen!2sph!6m8!1m7!1seWKk3mDeguIWhLREbiYJ7g!2m2!1d10.70514112798444!2d122.5631009698657!3f30.35691831400534!4f9.49063433997135!5f0.7820865974627469",
    "Navais": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701075106!5m2!1sen!2sph!6m8!1m7!1srPY5r4OvAnNl7cYqcWuM5w!2m2!1d10.70498372794727!2d122.5318940640832!3f50.47564587418835!4f0!5f0.7820865974627469",
    "Nonoy": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701162335!5m2!1sen!2sph!6m8!1m7!1s1COxt7TFKvlr-qGMZAVV4A!2m2!1d10.69317654529774!2d122.5678784906014!3f110.310135!4f0!5f0.7820865974627469",
    "North Avanceña": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701192298!5m2!1sen!2sph!6m8!1m7!1sFq_rSBy9AGClmnJuYNjo-A!2m2!1d10.69602318194677!2d122.5410408164938!3f162.5517!4f0!5f0.7820865974627469",
    "North Baluarte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701205520!5m2!1sen!2sph!6m8!1m7!1sDG1EH1PQVPEdTM5po6wRsg!2m2!1d10.69159829308442!2d122.5548557055091!3f79.66096879447306!4f0!5f0.7820865974627469",
    "North Fundidor": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701220444!5m2!1sen!2sph!6m8!1m7!1siizt4LwYF8vnLLeqx8mjzg!2m2!1d10.69343166314666!2d122.5369609801887!3f287.66664515188984!4f0!5f0.7820865974627469",
    "North San Jose": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701240380!5m2!1sen!2sph!6m8!1m7!1sMRSjz-R9iCjYHy6ZAWlVnQ!2m2!1d10.69805777085033!2d122.5425905874701!3f245.86626862542903!4f0!5f0.7820865974627469",
    "Obrero-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701252751!5m2!1sen!2sph!6m8!1m7!1sg_Dck95yOn4Le_fwVDHKHg!2m2!1d10.69852267679152!2d122.5874234449494!3f137.90599!4f0!5f0.7820865974627469",
    "Ortiz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701264727!5m2!1sen!2sph!6m8!1m7!1seyTYZl875HOJoql3FiO8Dw!2m2!1d10.69188941465128!2d122.5719435632347!3f191.49666!4f0!5f0.7820865974627469",
    "Osmeña": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701280132!5m2!1sen!2sph!6m8!1m7!1sOra6a1AjciBY9ftgL20Glw!2m2!1d10.69225836845142!2d122.5647564679234!3f11.780926555415249!4f-0.5480911080388893!5f0.7820865974627469",
    "Our Lady Of Fatima": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701293050!5m2!1sen!2sph!6m8!1m7!1sUJ66TLWNx0SsG0UwqWPTBg!2m2!1d10.71971858493861!2d122.5626566284414!3f220.43666730929178!4f0!5f0.7820865974627469",
    "Our Lady Of Lourdes": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701309209!5m2!1sen!2sph!6m8!1m7!1sT8nSPhMKZiP_MLOkNF8fSw!2m2!1d10.71632919904923!2d122.5585680628744!3f132.29773030217424!4f0!5f0.7820865974627469",
    "Oñate de Leon": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701336284!5m2!1sen!2sph!6m8!1m7!1s-p1eFheoI8p7lWRydoheAA!2m2!1d10.71286891085611!2d122.5383375738565!3f224.68163475861041!4f5.3072690709502695!5f0.7820865974627469",
    "PHHC Block 17": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701354089!5m2!1sen!2sph!6m8!1m7!1sHkrVGiB1zOGFmPg7CSUGrA!2m2!1d10.723385206363494!2d122.5404160679667!3f67.86759263350466!4f0!5f0.7820865974627469",
    "PHHC Block 22 NHA": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701369275!5m2!1sen!2sph!6m8!1m7!1sAfWtSrIOzULAdU7lkWsy_Q!2m2!1d10.72225413321613!2d122.5422840013634!3f347.17987544650634!4f0!5f0.7820865974627469",
    "Pale Benedicto Rizal (Mandurriao)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701380650!5m2!1sen!2sph!6m8!1m7!1sm0F71nLUrHcZmaRsMXQ4Fg!2m2!1d10.73990185549241!2d122.5216672029844!3f4.480559240452401!4f-2.6343028172595524!5f0.7820865974627469",
    "Poblacion Molo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701397666!5m2!1sen!2sph!6m8!1m7!1s-U1TO89jlg8iiVd4gSGVAQ!2m2!1d10.6964050258445!2d122.5454678090712!3f351.3491959883566!4f-15.644288840658064!5f0.7820865974627469",
    "President Roxas": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701412588!5m2!1sen!2sph!6m8!1m7!1sMIm5Jx4bLrtmP9V9zoeg8Q!2m2!1d11.43487347703365!2d122.9370953124593!3f334.91153!4f0!5f0.7820865974627469",
    "Progreso-Lapuz": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7840.934471539858!2d122.56811924996221!3d10.698398957606242!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee571b4c49661%3A0xbfd77d354fe66753!2sProgreso-Lapuz%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763701421267!5m2!1sen!2sph",
    "Punong-Lapuz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701434022!5m2!1sen!2sph!6m8!1m7!1sQlTI7UcjbDUMDZpme7QL6Q!2m2!1d10.70380244425233!2d122.5731492736945!3f16.060587216995025!4f0!5f0.7820865974627469",
    "Quezon": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701457020!5m2!1sen!2sph!6m8!1m7!1sfYfavhGkWFyi3Qtkwyrt4Q!2m2!1d10.68743326234897!2d122.5202963454098!3f95.96585345081934!4f0!5f0.7820865974627469",
    "Quintin Salas": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701471994!5m2!1sen!2sph!6m8!1m7!1sssw6Hz9RJlFDJApRA2BVOQ!2m2!1d10.74075609088262!2d122.5643025548039!3f277.5878256326846!4f0!5f0.7820865974627469",
    "Railway": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701485802!5m2!1sen!2sph!6m8!1m7!1sJMApgXzXvewC_zQhujRZHg!2m2!1d10.70996805540148!2d122.5678460446239!3f333.45623078432027!4f0!5f0.7820865974627469",
    "Rima-Rizal": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701498098!5m2!1sen!2sph!6m8!1m7!1sws3CZmYJ5fv489PoioaVTQ!2m2!1d10.69176997786655!2d122.5659353383143!3f198.32841001180483!4f0!5f0.7820865974627469",
    "Rizal (La Paz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701509082!5m2!1sen!2sph!6m8!1m7!1soHM-3YIiyAOYkWRlsIRlyg!2m2!1d10.7069803879403!2d122.5695700682653!3f355.6841808191251!4f0!5f0.7820865974627469",
    "Rizal Estanzuela": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701522904!5m2!1sen!2sph!6m8!1m7!1stuUEpm0ai5DxHYsQM9GmkA!2m2!1d10.69263641974345!2d122.5611583320482!3f166.90258899899356!4f0!5f0.7820865974627469",
    "Rizal Ibarra": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701599881!5m2!1sen!2sph!6m8!1m7!1s4ppSZ6eYwOoeBnp-qQ6a3Q!2m2!1d10.69189337624298!2d122.5674737780807!3f321.3152753078451!4f-20.811976306082414!5f0.4000000000000002",
    "Rizal Palapala I": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701658455!5m2!1sen!2sph!6m8!1m7!1skn7F0KNMpdsMOYlw9sJF6A!2m2!1d10.69230745696223!2d122.562545305471!3f128.16989232779662!4f-16.442990361728818!5f0.4000000000000002",
    "Rizal Palapala II": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701686093!5m2!1sen!2sph!6m8!1m7!1sE-K13IBYtSVrPpW5Zie4mQ!2m2!1d10.69195809326208!2d122.5640952729042!3f231.97334273363623!4f0!5f0.7820865974627469",
    "Roxas Village": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701778875!5m2!1sen!2sph!6m8!1m7!1se1HkyvegESvDGFFZLx9sgg!2m2!1d10.6942989251017!2d122.5647442140212!3f42.20208665858548!4f10.697208307545552!5f0.7820865974627469",
    "Sambag": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701833008!5m2!1sen!2sph!6m8!1m7!1sDO3vSLJdz_N2j3LEA3mhTA!2m2!1d10.73717145240501!2d122.5385692485991!3f200.07239702123547!4f-7.253365223641339!5f0.7820865974627469",
    "Sampaguita": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701850132!5m2!1sen!2sph!6m8!1m7!1sktcfW-9dqJqn2nZ8cLN_mw!2m2!1d10.701177678865!2d122.5655839481483!3f142.66159!4f0!5f0.7820865974627469",
    "San Agustin": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701868184!5m2!1sen!2sph!6m8!1m7!1sSWpbBkeZtFeWVKA_4l1gTw!2m2!1d10.69942180807698!2d122.5617270348198!3f36.164874640452126!4f-12.426303039156508!5f0.7820865974627469",
    "San Antonio": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701881976!5m2!1sen!2sph!6m8!1m7!1sjqXva9r5Yzc0R-8e3OYfSg!2m2!1d10.69392120516973!2d122.5427218702643!3f125.42560641333245!4f0!5f0.7820865974627469",
    "San Felix": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701900303!5m2!1sen!2sph!6m8!1m7!1s96DaNWUQws1C9Z_wpjflqw!2m2!1d10.69913362849763!2d122.5579484253377!3f39.896836843627646!4f0!5f0.7820865974627469",
    "San Isidro (Jaro)": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15679.835318186364!2d122.53709664012699!3d10.737656579830043!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee4cfe49cb323%3A0xcc03c8cfefdd540f!2sSan%20Isidro%20(Jaro)%2C%20Jaro%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763701916465!5m2!1sen!2sph",
    "San Isidro (La Paz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701947091!5m2!1sen!2sph!6m8!1m7!1swqhW6qapkKhnRnQo5Irq2w!2m2!1d10.722514897742!2d122.5818101642616!3f178.71921!4f0!5f0.7820865974627469",
    "San Jose (Arevalo)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763701964919!5m2!1sen!2sph!6m8!1m7!1s62XmPnmecVabZqngz91l4A!2m2!1d10.68894679812933!2d122.5193784590138!3f283.03630199680987!4f0!5f0.7820865974627469",
    "San Jose (City Proper)": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3920.5217876451493!2d122.559062122744!3d10.694178162329024!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee566f372e869%3A0xc582a99ae491c9e6!2sSan%20Jose%20(City%20Proper)%2C%20Iloilo%20City%20Proper%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763701985160!5m2!1sen!2sph",
    "San Jose (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702024043!5m2!1sen!2sph!6m8!1m7!1sWUu_O-8iB27MVOhlE_ooFA!2m2!1d10.71680347613002!2d122.563287024866!3f328.55746!4f0!5f0.7820865974627469",
    "San Juan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702013104!5m2!1sen!2sph!6m8!1m7!1sl-QRhR8vj7G2Me8su0Fu7Q!2m2!1d10.68819297062791!2d122.5442698899006!3f65.32645!4f0!5f0.7820865974627469",
    "San Nicolas": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702048733!5m2!1sen!2sph!6m8!1m7!1swL2WbmKuHUZQzQ6jBrBHJg!2m2!1d10.71367882362904!2d122.5653046128265!3f197.94030633912826!4f-1.298936269369591!5f0.7820865974627469",
    "San Pedro (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702074069!5m2!1sen!2sph!6m8!1m7!1snSm-1oMA1fic9ngicb3ySw!2m2!1d10.71917610195638!2d122.5651645565568!3f27.082506!4f0!5f0.7820865974627469",
    "San Pedro (Molo)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702083912!5m2!1sen!2sph!6m8!1m7!1s7CEhnh6gV_6QHIoBARHCLg!2m2!1d10.69863718560022!2d122.5461576916883!3f339.23456!4f0!5f0.7820865974627469",
    "San Rafael": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702095577!5m2!1sen!2sph!6m8!1m7!1sujoDGuNbmIUDz3q170LuiA!2m2!1d10.70938709036927!2d122.5511389862087!3f317.4711748424792!4f0!5f0.7820865974627469",
    "San Roque": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702108033!5m2!1sen!2sph!6m8!1m7!1sPONE3nW8XwIyyDDiHB8eiw!2m2!1d10.731043052196178!2d122.55394200818083!3f220.3946!4f0!5f0.7820865974627469",
    "San Vicente": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702144287!5m2!1sen!2sph!6m8!1m7!1skcU5wIubEChpwue85CBsUA!2m2!1d10.71972583674858!2d122.5586867256291!3f145.27050794163284!4f-6.760298252938043!5f0.7820865974627469",
    "Santa Cruz": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702169629!5m2!1sen!2sph!6m8!1m7!1sIQYjZGZDUqJ1WDkMZ7wRdQ!2m2!1d10.68651519524713!2d122.5018461556033!3f169.775339362915!4f0!5f0.7820865974627469",
    "Santa Filomena": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702193190!5m2!1sen!2sph!6m8!1m7!1sJ-O9YGsiI1Wts7RvdTppgQ!2m2!1d10.6865526830051!2d122.5159716241841!3f56.17831!4f0!5f0.7820865974627469",
    "Santa Rosa": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702209339!5m2!1sen!2sph!6m8!1m7!1sItWBLH91jlvSlsnwfZlxkw!2m2!1d10.72588711889457!2d122.5457403792808!3f131.97380895455478!4f0!5f0.7820865974627469",
    "Santo Domingo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702236000!5m2!1sen!2sph!6m8!1m7!1snBXiMpYm188fBB1QZi3ehw!2m2!1d10.69174271521316!2d122.5059063879324!3f14.040817475899601!4f3.2574895234898094!5f1.5855049184751469",
    "Santo Niño Norte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702255324!5m2!1sen!2sph!6m8!1m7!1s0uppICM6-Jgt7rKdtF3gIA!2m2!1d10.68036895186263!2d122.52099131608367!3f7.0137134!4f0!5f0.7820865974627469",
    "Santo Niño Sur": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702255324!5m2!1sen!2sph!6m8!1m7!1s0uppICM6-Jgt7rKdtF3gIA!2m2!1d10.68036895186263!2d122.52099131608367!3f7.0137134!4f0!5f0.7820865974627469",
    "Santo Rosario-Duran": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702276311!5m2!1sen!2sph!6m8!1m7!1szszQ02KgZm7atQOQOaGXgQ!2m2!1d10.69081746092677!2d122.5764841682366!3f10.332932!4f0!5f0.7820865974627469",
    "Seminario (Burgos Jalandoni)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702286053!5m2!1sen!2sph!6m8!1m7!1ss6bpISp7MHm5RmUXfg8jWA!2m2!1d10.72253250660206!2d122.5565493944301!3f48.673637!4f0!5f0.7820865974627469",
    "Simon Ledesma": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702326626!5m2!1sen!2sph!6m8!1m7!1sP0X9uPbZ6RgXqUMKJn56fQ!2m2!1d10.72932474958192!2d122.557624538115!3f234.93839651642102!4f-3.3594987495457644!5f0.7820865974627469",
    "Sinikway (Bangkerohan Lapuz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702336610!5m2!1sen!2sph!6m8!1m7!1sd0aGK87-3x6R1NCFfAHGEw!2m2!1d10.70696871268112!2d122.5758112269433!3f244.62022!4f0!5f0.7820865974627469",
    "So-oc": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702371573!5m2!1sen!2sph!6m8!1m7!1s2f0uPOAOBFQO6tW8S6PuHQ!2m2!1d10.70160500433804!2d122.5208091565175!3f286.0160432558114!4f-5.1132928886939055!5f1.7742071054934323",
    "South Baluarte": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702386911!5m2!1sen!2sph!6m8!1m7!1snUrUNXJTMVDmL4nF9jUpSQ!2m2!1d10.6909393986204!2d122.5498092547002!3f291.9193900446208!4f0!5f0.7820865974627469",
    "South Fundidor": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702403514!5m2!1sen!2sph!6m8!1m7!1samFVJahMPxSx5UrdWekrLQ!2m2!1d10.68982844998457!2d122.5302099000426!3f344.66733!4f0!5f0.7820865974627469",
    "South San Jose": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7840.961682990286!2d122.53236559996205!3d10.697346407610146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aefaacc4a96f51%3A0xf03a5a7125c0b74e!2sSouth%20San%20Jose%2C%20Molo%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763702414874!5m2!1sen!2sph",
    "Taal": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7840.917168122769!2d122.54596804996214!3d10.69906820760371!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33aee54522bdbf0d%3A0xdac50c2f1f4cc564!2sTaal%2C%20Iloilo%20City%2C%20Iloilo!5e0!3m2!1sen!2sph!4v1763702425805!5m2!1sen!2sph",
    "Tabuc Suba (Jaro)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702440586!5m2!1sen!2sph!6m8!1m7!1s_nCRn8_kTr6iyKNlCrvM9A!2m2!1d10.73334239995593!2d122.5582572089632!3f122.59427!4f0!5f0.7820865974627469",
    "Tabuc Suba (La Paz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702448797!5m2!1sen!2sph!6m8!1m7!1s6g5amr-0NVf7QA1XQk4K4Q!2m2!1d10.71750056925469!2d122.5721805990989!3f55.756336!4f0!5f0.7820865974627469",
    "Tabucan": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702460735!5m2!1sen!2sph!6m8!1m7!1sqccFhDNYOtI5WfYxnXfHyg!2m2!1d10.70454823785286!2d122.5447684275794!3f148.84090526249884!4f0!5f0.7820865974627469",
    "Tacas": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702477377!5m2!1sen!2sph!6m8!1m7!1swC4bMyFIZIfUGjcqKvqjxw!2m2!1d10.75518383477156!2d122.553189692738!3f209.68748403648226!4f-17.638395740454484!5f0.7820865974627469",
    "Tagbac": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702491738!5m2!1sen!2sph!6m8!1m7!1sCAoSF0NJSE0wb2dLRUlDQWdJRE1uOVRjdEFF!2m2!1d10.76771570703917!2d122.578278800763!3f227.60925106475727!4f12.923358733032728!5f0.7820865974627469",
    "Tanza-Esperanza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702509712!5m2!1sen!2sph!6m8!1m7!1sHZjtUUj2nI-6mAlTghGg0w!2m2!1d10.69540821161991!2d122.5588568230573!3f195.46710853417432!4f-7.599665667564196!5f0.7820865974627469",
    "Tap-oc": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702565979!5m2!1sen!2sph!6m8!1m7!1sFS-5PZQeoayEfA3vmMVgXg!2m2!1d10.69874457676371!2d122.5440039618804!3f100.74237566188077!4f2.5590629303147097!5f0.7820865974627469",
    "Taytay Zone II": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702579085!5m2!1sen!2sph!6m8!1m7!1so1gzILOB_t1DkIHF4jA01Q!2m2!1d10.72253659210404!2d122.5532071262883!3f204.01909!4f0!5f0.7820865974627469",
    "Ticud (La Paz)": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702595718!5m2!1sen!2sph!6m8!1m7!1syx1H23lTmap9sDvX7MluGg!2m2!1d10.71729826629814!2d122.5802095555609!3f220.00824386667267!4f0!5f0.7820865974627469",
    "Timawa Tanza I": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702609025!5m2!1sen!2sph!6m8!1m7!1skj81VQc7kisPt9LXbsKzXQ!2m2!1d10.69398810049311!2d122.5558840045283!3f349.5082423071542!4f-4.8328296560451065!5f0.7820865974627469",
    "Timawa Tanza II": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702629351!5m2!1sen!2sph!6m8!1m7!1sMvv31K5LIjegaJXRH4aX9g!2m2!1d10.6943971366615!2d122.5569079782678!3f61.17304298075897!4f0!5f0.7820865974627469",
    "Ungka": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702643490!5m2!1sen!2sph!6m8!1m7!1s37eaIEqFKr11vv48nr_gBQ!2m2!1d10.74548724111714!2d122.5387384295302!3f197.70888!4f0!5f0.7820865974627469",
    "Veterans Village": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702652899!5m2!1sen!2sph!6m8!1m7!1sMtJUO0XtYvy95jcoEfx_AQ!2m2!1d10.690634726942385!2d122.58033181736548!3f24.910862!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "Villa Anita": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702662941!5m2!1sen!2sph!6m8!1m7!1szXb0kwngsshplmugYC0PzA!2m2!1d10.69899390666287!2d122.5606412326762!3f350.58713!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "West Habog-habog": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702677503!5m2!1sen!2sph!6m8!1m7!1saYZwx9aUSUE07Eq44f6oxA!2m2!1d10.69031661720794!2d122.5466803871368!3f175.03795909419875!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "West Timawa": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702691590!5m2!1sen!2sph!6m8!1m7!1sgldtVXiAzczy_vTabKP-mg!2m2!1d10.69517180924159!2d122.5487094320841!3f14.988905093672187!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "Yulo Drive": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702706393!5m2!1sen!2sph!6m8!1m7!1sA-wy4gREOv3nKC807uYqSg!2m2!1d10.68449468664266!2d122.5172508514664!3f207.23872219874212!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "Yulo-Arroyo": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702719766!5m2!1sen!2sph!6m8!1m7!1sH8Ibibdukwk0ZAS91itpnA!2m2!1d10.69686051024598!2d122.5703277010891!3f331.51022!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>",
    "Zamora-Melliza": "https://www.google.com/maps/embed?pb=!3m2!1sen!2sph!4v1763702731199!5m2!1sen!2sph!6m8!1m7!1sd0z4PeFnrMAtarGCfIgGzw!2m2!1d10.69441401823461!2d122.5761452389978!3f224.19936!4f0!5f0.7820865974627469\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>"
}


# --- Find selected barangay feature + extract KPI values ---
if selected_barangay != "--Select--":
    selected_feature = next(
        f for f in urban['features']
        if f['properties']['location_adm4_en'] == selected_barangay
    )
    props = selected_feature['properties']
    brgy_name_val = props.get("location_adm4_en", "N/A")

    # ---------- formatting helper ----------
    def clean_string_for_number(s):
        """Remove common noise so float() can parse it."""
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() in ("nan", "n/a", "none"):
            return None
        # remove commas, percent sign, and surrounding whitespace
        s = s.replace(",", "").replace("%", "")
        return s

    def format_number(x, decimals=3, mode="round", preserve_int=True):
        """
        mode: "round" or "trunc"
        preserve_int: if True, integers show as '83' instead of '83.000'
        Returns a string or "-" if not numeric.
        """
        try:
            if x is None:
                return "-"
            # clean common formatting
            s = clean_string_for_number(x)
            if s is None:
                return "-"
            # ensure it's numeric
            v = float(s)
            if not np.isfinite(v):
                return "-"
            scale = 10 ** decimals
            if mode == "trunc":
                # truncation preserving sign
                v_trunc = math.trunc(v * scale) / scale
                v_out = v_trunc
            else:
                # rounding
                v_out = round(v, decimals)
            # if preserve_int and it's effectively an integer, show without decimals
            if preserve_int and abs(v_out - int(v_out)) < (1 / (10 ** (decimals + 1))):
                return str(int(v_out))
            # otherwise format with fixed decimals
            return f"{v_out:.{decimals}f}"
        except Exception:
            return str(x)

    # ---------- choose mode: "round" or "trunc" ----------
    # If you want strict truncation (take the first 3 decimals) use "trunc".
    # If you want rounding use "round".
    # Change below to "round" if that's what you prefer.
    MODE = "round"   # <-- set "round" or "trunc"

    # Extract & format KPIs
    urban_risk_val = format_number(props.get("urban_risk_index", None), decimals=3, mode=MODE, preserve_int=True)
    # risk_label typically text; keep as-is
    risk_label_val = props.get("risk_label", "-")
    amenity_risk_val = format_number(props.get("infra_risk", None), decimals=3, mode=MODE, preserve_int=True)

else:
    brgy_name_val = "-"
    urban_risk_val = "-"
    risk_label_val = "-"
    amenity_risk_val = "-"


col1, col2, col3, col4 = st.columns(4)

kpi_box_style = """
<div style="
    background-image: url('https://encycolorpedia.com/d2e8ba.png');
    background-position: top;
    background-size: cover;
    border-radius:20px;
    padding:0px 20px 15px 20px;
    text-align:center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 2px solid black;
    transition: transform 0.2s;
    height:150px;
    display:flex;
    flex-direction:column;
    justify-content:flex-start;
" onmouseover="this.style.transform='scale(1.05)'" 
  onmouseout="this.style.transform='scale(1)'">
    <h4 style="margin-top:10px; font-size:22px; color:#000000;">{title}</h4>
    <h2 style="margin-top:5px; font-size:55px; font-weight:bold; color:#000000;">{value}</h2>
</div>
"""

with col1:
    st.markdown(kpi_box_style.format(title="Barangay Name", value=brgy_name_val), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_box_style.format(title="Climate Vulnerability Index", value=urban_risk_val), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_box_style.format(title="Risk Label", value=risk_label_val), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_box_style.format(title="Amenity Risk (Relative)", value=amenity_risk_val), unsafe_allow_html=True)


st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
# --- Base Map ---
m = folium.Map(location=[10.72, 122.55], zoom_start=13)

# --- Function to get bounds of a feature ---
def get_bounds(feature):
    geom = feature['geometry']
    if geom['type'] == "Polygon":
        coords = geom['coordinates'][0]
    elif geom['type'] == "MultiPolygon":
        coords = geom['coordinates'][0][0]
    else:
        coords = [(0,0)]
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    return [[min(lats), min(lons)], [max(lats), max(lons)]]

# --- Add Urban Risk Layer ---
for feature in urban['features']:
    name = feature['properties']['location_adm4_en']
    if selected_barangay == "--Select--" or selected_barangay == name:
        folium.GeoJson(
            feature,
            name=name,
            style_function=lambda f, name=name: {
                "fillColor": "#D2E8BA" if name == selected_barangay else "#cccccc",
                "color": "black",
                "weight": 2 if name == selected_barangay else 1,
                "fillOpacity": 0.7 if name == selected_barangay else 0.3,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "location_adm4_en",
                    "urban_risk_index",
                    "risk_label",
                    "climate_exposure_score",
                    "infra_risk",
                    "rwi_risk",
                    "ndvi_risk",
                    "coast_risk",
                    "pop_risk"
                ],
                aliases=[
                    "Barangay:",
                    "Climate Vulnerability Index:",
                    "Risk Category:",
                    "Climate Exposure Score:",
                    "Amenity Risk (Relative):",
                    "Relative Wealth Index Risk:",
                    "NDVI Risk:",
                    "Coast Distance Risk:",
                    "Population Risk:"
                ],
                localize=True
            )
        ).add_to(m)

# --- Zoom to selected barangay ---
if selected_barangay != "--Select--":
    selected_feature = next(f for f in urban['features'] if f['properties']['location_adm4_en'] == selected_barangay)
    bounds = get_bounds(selected_feature)
    m.fit_bounds(bounds)

# --- Display Map ---
st_folium(m, width=2000, height=1000)

if selected_barangay in street_view_urls:
    components.html(f"""
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    ">
        <iframe 
            src="{street_view_urls[selected_barangay]}" 
            width="100%" 
            height="600" 
            style="border:0; border-radius:10px;" 
            allowfullscreen="" 
            loading="lazy" 
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>
    """, height=650)  # slightly taller to account for padding
