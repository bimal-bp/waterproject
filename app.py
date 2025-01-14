import datetime
import math
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from branca.element import Figure
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static
from dateutil.relativedelta import relativedelta
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import geemap
from data_collection import get_data  # Import your custom data collection function
from predict import send_df, predict_quality  # Import your custom prediction functions

# Streamlit page configuration
st.set_page_config(
    page_title="Water Quality Monitoring Dashboard for Kutch Region",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Suppress warnings for pyplot
st.set_option('deprecation.showPyplotGlobalUse', False)

# Sidebar
st.sidebar.markdown('<h1 style="margin-left:8%; color:#FF9933 ">Kutch Water Quality Monitoring Dashboard </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About", "Features", "Select AOI Data Parameters", "Visualizations", "Conclusion", "Team")
)

# Home page
if add_selectbox == 'Home':
    LOGO_IMAGE = "omdena_india_logo.png"

    with open(LOGO_IMAGE, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{encoded_logo}" style="height: 100px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader('PROBLEM STATEMENT')
    st.markdown("""
        Our problem statement is to develop a centralized dashboard with different water quality parameters for analyzing, 
        interpretation, and visualization in near real-time using Remote Sensing and AI for better decision-making. 
        This will identify if any parameter is not within standard limits for immediate action and reinforce abilities 
        to monitor water quality more effectively and efficiently.
    """, unsafe_allow_html=True)

# About page
elif add_selectbox == 'About':
    st.subheader('ABOUT THE PROJECT')
    st.markdown("""
        <h4>Project Goals</h4>
        • Water Quality Indicator Dashboard for Analysis, Interpretation and Visualization near Real Time<br>
        • Compare Real Water Quality Parameters with Standard Water Quality Limits
    """, unsafe_allow_html=True)

    st.markdown("""
        <h4>Locations Chosen</h4>
        Harmisar Lake, Shinai Lake, Tappar Lake
    """, unsafe_allow_html=True)

    st.markdown("""
        <h4>Developments Made</h4>
        • Water Quality Parameters were identified which includes physical, biological, and chemical parameters.<br>
        • Research papers were reviewed and important points were noted for different remote sensing data used with machine learning.<br>
        • Various data sources were searched in Google Earth Engine and relevant sources were selected for our use-case.<br>
        • Analyzed the images from the selected sources and applied various standard formulae to analyze the colors of the water body regions.<br>
        • Final water quality parameters were selected and their names listed along with their band formulae.<br>
        • Various machine learning models were applied to the final dataframe, metrics were analyzed, and the best model was chosen.<br>
        • A visualization dashboard was created for the public to analyze and visualize water quality parameters.
    """, unsafe_allow_html=True)

# Features page
elif add_selectbox == 'Features':
    st.subheader('PROJECT ENDORSEMENTS')
    st.markdown("""
        • Projecting the quality of water bodies in the Kutch Region.<br>
        • Making it more centralized to analyze and monitor existing water-body conditions.<br>
        • Identification of parameters compared with standard threshold values.
    """, unsafe_allow_html=True)

# Select AOI Data Parameters page
elif add_selectbox == 'Select AOI Data Parameters':
    st.subheader('SELECT FOR AOI DATA PARAMETERS')
    col1, col2 = st.columns(2)

    area = st.text_input('Type Area Of Interest', 'Water Body')

    prm_type = col1.selectbox(
        "Data Visualization Parameters",
        ("All", "pH", "Salinity", "Turbidity", "Land Surface Temperature", "Chlorophyll",
         "Suspended matter", "Dissolved Organic Matter", "Dissolved Oxygen")
    )

    long = st.number_input('Longitude', min_value=72.6026, format="%.4f")
    lat = st.number_input('Latitude', min_value=23.0063, format="%.4f")

    col3, _ = st.columns((1, 2))
    start_date = datetime.date.today() - relativedelta(years=5)
    end_date = datetime.date.today()
    slider1 = col3.slider('Select Start Date', min_value=start_date, max_value=end_date, format="MMM DD, YYYY")
    slider2 = col3.slider('Select End Date', min_value=start_date, max_value=end_date, format="MMM DD, YYYY")

    # Visualization and prediction
    if st.button('Submit'):
        st.write("Processing your request...")
        try:
            df2 = get_data(long, lat, str(slider1), str(slider2))
            df_all, test = send_df(df2)
            prediction = predict_quality(df2, test)
            st.write(prediction)

            if prm_type == "Dissolved Oxygen":
                plot_do(df_all)
            elif prm_type == "Salinity":
                plot_salinity(df_all)
            else:
                st.write("Please choose valid parameters for visualization.")
        except Exception as e:
            st.error(f"Error: {e}")
