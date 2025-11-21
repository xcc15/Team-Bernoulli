import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import json

# Set page config to wide layout
st.set_page_config(layout="wide")
st.title("KLIMATA ILOILO")
st.markdown("*A Climate Vulnerability Index for the Ilonggo People!*")

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
st.markdown(sidebar_bg, unsafe_allow_html=True)

st.set_page_config(layout="wide")  # Make the Streamlit page use full width

st.sidebar.image("klimata_logo.png", width=1000)
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

# --- Sidebar: layer selection ---
layer_option = st.sidebar.radio(
    "Select map layer",
    [
        "Climate Vulnerability",        # FIRST
        "Population Layer",
        "Amenity Risk Layer",
        "Climate Exposure Layer"
    ]
)

# --- Load GeoJSON files ---
with open("climate_risk.geojson", "r") as f:
    urban = json.load(f)

with open("iloilo_pop.geojson", "r") as f:
    barangays = json.load(f)

with open("iloilo_infra3.0.geojson", "r") as f:
    amenities = json.load(f)

with open("iloilo_cli3.0.geojson", "r") as f:
    climate = json.load(f)


# ======================================================
# QUANTILES FOR COLOR GRADIENTS
# ======================================================

# Population quantiles
pop_values = [f['properties']['pop_count_total'] for f in barangays['features']]
pop_quantiles = np.quantile(pop_values, [0, 0.33, 0.66, 1.0])

# Amenity index quantiles
infra_values = [f['properties'].get('infra_index', 0) for f in amenities['features']]
infra_quantiles = np.quantile(infra_values, [0, 0.33, 0.66, 1.0])

# Climate Exposure quantiles
clim_values = [f['properties'].get('climate_exposure_score', 0) for f in climate['features']]
clim_quantiles = np.quantile(clim_values, [0, 0.33, 0.66, 1.0])


# ======================================================
# COLOR FUNCTIONS
# ======================================================
def color_by_quantile(value, quantiles, colors):
    if value <= quantiles[1]:
        return colors[0]
    elif value <= quantiles[2]:
        return colors[1]
    else:
        return colors[2]

pop_colors = ['#c6dbef', '#6baed6', '#08306b']
infra_colors = ['#ff9999', '#ff4d4d', '#990000']
climate_colors = ['#d4f4dd', '#7ddf96', '#1b8f3b']

risk_colors = {
    "Low Risk": "#ffff66",     # Yellow
    "Medium Risk": "#ff8c00",  # Orange (fixed)
    "High Risk": "#cc0000"     # Red
}

# ======================================================
# BASE MAP
# ======================================================
m = folium.Map(location=[10.72, 122.5571], zoom_start=13.46)
# ======================================================
# --- 1. URBAN RISK LAYER (FIRST) ---
# ======================================================
if layer_option == "Climate Vulnerability":

    col1, col2, col3, col4 = st.columns(4)

# Common CSS for all boxes with image background
    kpi_box_style = """
<div style="
    background-image: url('https://encycolorpedia.com/d2e8ba.png');
    background-position: top;
    background-size: cover;
    border-radius:20px;
    padding:0px 20px 15px 20px;  /* increased top padding */
    text-align:center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 2px solid black;
    transition: transform 0.2s;
    height:150px;   /* slightly taller for spacing */
    display:flex;
    flex-direction:column;
    justify-content:flex-start; /* place text toward the top area but lower than before */
" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
    <h4 style="margin-top:10px; font-size:22px; color:#000000;">{title}</h4>
    <h2 style="margin-top:5px; font-size:55px; font-weight:bold; color:#000000;">{value}</h2>
</div>
"""

# Example boxes
    with col1:
        st.markdown(kpi_box_style.format(title="Barangays", value="180"), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_box_style.format(title="Low Risk", value="83"), unsafe_allow_html=True)

    with col3:
        st.markdown(kpi_box_style.format(title="Mid-Risk", value="82"), unsafe_allow_html=True)

    with col4:
        st.markdown(kpi_box_style.format(title="High Risk", value="15"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


    st.markdown(
    """
    <div style="
        border:1px solid #ccc; 
        padding:10px; 
        border-radius:5px; 
        background-color:#f9f9f9; 
        font-size:16px;
    ">
        The <b>Climate Vulnerability Index</b> combines factors like exposure, population, vegetation, infrastructure, wealth, and coastal proximity to measure risk levels. It helps identify which barangays are most vulnerable to climate impacts and guides adaptation planning.
    </div>
    """,
    unsafe_allow_html=True
)
    folium.GeoJson(
        urban,
        name="Climate Vulnerability Layer",
        style_function=lambda f: {
            "fillColor": risk_colors.get(f['properties'].get('risk_label', "Middle Risk"), "gray"),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6,
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
                "pop_risk"      # kept but renamed in alias
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


# ======================================================
# 2. POPULATION LAYER
# ======================================================
elif layer_option == "Population Layer":
        col1, col2, col3, col4 = st.columns(4)

# Common CSS for all boxes with image background
        kpi_box_style = """
<div style="
    background-image: url('https://encycolorpedia.com/d2e8ba.png');
    background-position: top;
    background-size: cover;
    border-radius:20px;
    padding:0px 20px 15px 20px;  /* increased top padding */
    text-align:center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 2px solid black;
    transition: transform 0.2s;
    height:150px;   /* slightly taller for spacing */
    display:flex;
    flex-direction:column;
    justify-content:flex-start; /* place text toward the top area but lower than before */
" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
    <h4 style="margin-top:10px; font-size:22px; color:#000000;">{title}</h4>
    <h2 style="margin-top:5px; font-size:55px; font-weight:bold; color:#000000;">{value}</h2>
</div>
"""

# Example boxes
        with col1:
            st.markdown(kpi_box_style.format(title="Population", value="473,728"), unsafe_allow_html=True)

        with col2:
            st.markdown(kpi_box_style.format(title="Average per Barangay", value="2315.16"), unsafe_allow_html=True)

        with col3:
            st.markdown(kpi_box_style.format(title="Highest Populated Barangay", value="10157.33"), unsafe_allow_html=True)

        with col4:
            st.markdown(kpi_box_style.format(title="Lowest Populated Barangay", value="153.71"), unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
   
        
        st.markdown(
    """
    <div style="
        border:1px solid #ccc; 
        padding:10px; 
        border-radius:5px; 
        background-color:#f9f9f9; 
        font-size:16px;
    ">
        The map shows that Iloilo City’s 473,000 residents are largely concentrated in <b>coastal barangays</b>, particularly in Molo and City Proper, where densities reach over 9,000 people per barangay.
    </div>
    """,
    unsafe_allow_html=True
)
        folium.GeoJson(
        barangays,
        name="Population",
        style_function=lambda f: {
            'fillColor': color_by_quantile(f['properties']['pop_count_total'], pop_quantiles, pop_colors),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['location_adm4_en', 'pop_count_total', 'brgy_total_area_y'],
            aliases=['Barangay:', 'Population:', 'Area (sq km):'],
            localize=True
        )
    ).add_to(m)


# ======================================================
# 3. AMENITY RISK LAYER
# ======================================================
elif layer_option == "Amenity Risk Layer":

    col1, col2, col3, col4 = st.columns(4)

# Common CSS for all boxes with image background
    kpi_box_style = """
<div style="
    background-image: url('https://encycolorpedia.com/d2e8ba.png');
    background-position: top;
    background-size: cover;
    border-radius:20px;
    padding:0px 20px 15px 20px;  /* increased top padding */
    text-align:center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 2px solid black;
    transition: transform 0.2s;
    height:150px;   /* slightly taller for spacing */
    display:flex;
    flex-direction:column;
    justify-content:flex-start; /* place text toward the top area but lower than before */
" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
    <h4 style="margin-top:10px; font-size:22px; color:#000000;">{title}</h4>
    <h2 style="margin-top:5px; font-size:55px; font-weight:bold; color:#000000;">{value}</h2>
</div>
"""

# Example boxes
    with col1:
        st.markdown(kpi_box_style.format(title="Avg. Distance to Shelter (m)", value="967.28m"), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_box_style.format(title="Avg. Distance to Community Center (m)", value="805.45m"), unsafe_allow_html=True)

    with col3:
            st.markdown(kpi_box_style.format(title="Population % near Health Center (5min)", value="88.17%"), unsafe_allow_html=True)

    with col4:
        st.markdown(kpi_box_style.format(title="Population % near Hospital (5min)", value="48.72%"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    st.markdown(
    """
    <div style="
        border:1px solid #ccc; 
        padding:10px; 
        border-radius:5px; 
        background-color:#f9f9f9; 
        font-size:16px;
    ">
        The <b>Amenity Risk Index</b> is a composite score that combines health access and amenity distances 
        for a barangay, weighted by their relative importance. Higher values indicate better protective 
        infrastructure. (m = meters)
    </div>
    """,
    unsafe_allow_html=True
)

    folium.GeoJson(
        amenities,
        name="Amenity Risk",
        style_function=lambda f: {
            'fillColor': color_by_quantile(f['properties'].get('infra_index', 0), infra_quantiles, infra_colors),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[
                'location_adm4_en', 'infra_index', 'college_nearest', 'community_centre_nearest',
                'school_nearest', 'shelter_nearest', 'town_hall_nearest', 'university_nearest',
                'brgy_healthcenter_pop_reached_pct_5min', 'brgy_healthcenter_pop_reached_pct_15min',
                'brgy_healthcenter_pop_reached_pct_30min', 'hospital_pop_reached_pct_5min',
                'hospital_pop_reached_pct_15min', 'hospital_pop_reached_pct_30min',
                'rhu_pop_reached_pct_5min', 'rhu_pop_reached_pct_15min', 'rhu_pop_reached_pct_30min'
            ],
            aliases=[
                'Barangay:', 'Amenity Risk Index:', 'College (m):', 'Community Centre (m):',
                'School (m):', 'Shelter (m):', 'Town Hall (m):', 'University (m):',
                '% Pop near Health Center (5 min):', '% Pop near Health Center (15 min):',
                '% Pop near Health Center (30 min):', '% Pop near Hospital (5 min):',
                '% Pop near Hospital (15 min):', '% Pop near Hospital (30 min):',
                '% Pop near RHU (5 min):', '% Pop near RHU (15 min):',
                '% Pop near RHU (30 min):'
            ],
            localize=True
        )
    ).add_to(m)


# ======================================================
# 4. CLIMATE EXPOSURE LAYER
# ======================================================
elif layer_option == "Climate Exposure Layer":

    col1, col2, col3, col4 = st.columns(4)

# Common CSS for all boxes with image background
    kpi_box_style = """
<div style="
    background-image: url('https://encycolorpedia.com/d2e8ba.png');
    background-position: top;
    background-size: cover;
    border-radius:20px;
    padding:0px 20px 15px 20px;  /* increased top padding */
    text-align:center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    border: 2px solid black;
    transition: transform 0.2s;
    height:150px;   /* slightly taller for spacing */
    display:flex;
    flex-direction:column;
    justify-content:flex-start; /* place text toward the top area but lower than before */
" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
    <h4 style="margin-top:10px; font-size:22px; color:#000000;">{title}</h4>
    <h2 style="margin-top:5px; font-size:55px; font-weight:bold; color:#000000;">{value}</h2>
</div>
"""

# Example boxes
    with col1:
        st.markdown(kpi_box_style.format(title="Avg. Heat Index", value="30.37°C"), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_box_style.format(title="Avg. Rainfall Estimate", value="6.45mm"), unsafe_allow_html=True)

    with col3:
            st.markdown(kpi_box_style.format(title="Avg. PM2.5", value="13.17"), unsafe_allow_html=True)

    with col4:
        st.markdown(kpi_box_style.format(title="Avg PM10", value="19.18"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
   

    st.markdown(
    """
    <div style="
        border:1px solid #ccc; 
        padding:10px; 
        border-radius:5px; 
        background-color:#f9f9f9; 
        font-size:16px;
    ">
        The <b>Climate Exposure Score</b> measures how much a specific area is exposed to climate-related hazards, such as heat, rainfall extremes, or air pollution. Higher scores indicate greater exposure.
    </div>
    """,
    unsafe_allow_html=True
)
    folium.GeoJson(
        climate,
        name="Climate Exposure Layer",
        style_function=lambda f: {
            'fillColor': color_by_quantile(f['properties'].get('climate_exposure_score', 0),
                                           clim_quantiles, climate_colors),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[
                'location_adm4_en',
                'climate_exposure_score',
                'heat_index',
                'pr',
                'ndvi',
                'co',
                'so2',
                'no2',
                'o3',
                'pm10',
                'pm25'
            ],
            aliases=[
                'Barangay Name:',
                'Climate Exposure Score:',
                'Heat Index:',
                'Rainfall Estimates (mm/day):',
                'NDVI:',
                'Carbon Oxide (ppm):',
                'Sulfur Dioxide (ppm):',
                'Nitrogen Dioxide (ppb):',
                'Ozone Mixing Ratio (ppb):',
                'PM10:',
                'PM2.5:'
            ],
            localize=True
        )
    ).add_to(m)


# ======================================================
# LAYER CONTROL
# ======================================================
folium.LayerControl().add_to(m)

# ======================================================
# DISPLAY MAP
# ======================================================

st_folium(m, width=2000, height=1000)



