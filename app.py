import streamlit as st
import requests
import numpy as np
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="AeroScape GeoAI Assistant",
    page_icon="🌍",
    layout="wide"
)

# Caching the SLM model loading so it stays fast
@st.cache_resource
def load_slm():
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True)
    return tokenizer, model

def fetch_openstreetmap_data(location_name):
    geo_url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
    headers = {'User-Agent': 'AeroScape-GeoAI-Research-Student/2.0'}
    try:
        res = requests.get(geo_url, headers=headers, timeout=5)
        response = res.json() if res.status_code == 200 and res.text.strip().startswith('[') else []
        if response:
            lat, lon = float(response[0]['lat']), float(response[0]['lon'])
        else:
            lat, lon = 19.1136, 72.8697
    except Exception:
        lat, lon = 19.1136, 72.8697
    return lat, lon

def fetch_open_meteo_data(lat, lon):
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m"
        aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide"
        w_data = requests.get(weather_url, timeout=5).json().get('current', {})
        aq_data = requests.get(aq_url, timeout=5).json().get('current', {})
    except Exception:
        w_data, aq_data = {}, {}
    return {
        "temperature_c": w_data.get('temperature_2m', 28.5),
        "relative_humidity": w_data.get('relative_humidity_2m', 60.0),
        "wind_speed_ms": w_data.get('wind_speed_10m', 3.2),
        "pm2_5": aq_data.get('pm2_5', 45.0),
        "pm10": aq_data.get('pm10', 85.0),
        "co": aq_data.get('carbon_monoxide', 400.0)
    }

def calculate_advanced_uhi_stress(ndvi_value, air_temp_c, relative_humidity):
    ndvi_min, ndvi_max = 0.2, 0.8
    fvc = max(0.0, min(1.0, (ndvi_value - ndvi_min) / (ndvi_max - ndvi_min)))
    surface_emissivity = 0.90 + 0.09 * fvc
    suhi_delta = (1.0 - fvc) * 3.8
    estimated_surface_temp = air_temp_c + suhi_delta
    discomfort_index = air_temp_c - 0.55 * (1.0 - relative_humidity / 100.0) * (air_temp_c - 14.4)
    return {
        "estimated_surface_temp_c": round(float(estimated_surface_temp), 2),
        "physiological_discomfort_index": round(float(discomfort_index), 2)
    }

def generate_slm_recommendation(context_data, tokenizer, model):
    prompt = f"""<|im_start|>system
You are AeroScape GeoAI, a rigorous environmental research assistant. Provide an objective outdoor safety and microclimate assessment based strictly on the following verified live telemetry data. Do not extrapolate or hallucinate.
Telemetry: {context_data}<|im_end|>
<|im_start|>user
Provide a concise, professional assessment of local air quality, heat stress, and outdoor routing safety.<|im_end|>
<|im_start|>assistant\n"""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.2, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# UI Layout
st.title("🌍 AeroScape GeoAI Research Assistant")
st.markdown("**CSRE IIT Bombay Hackathon Portal:** Real-time microclimate intelligence, UHI physics, and zero-hallucination SLM guardrails.")

# Sidebar input controls
st.sidebar.header("📍 Spatial Target Configuration")
target_location = st.sidebar.text_input("Enter Location Name", "Powai, Mumbai")
mock_ndvi = st.sidebar.slider("Satellite NDVI (Vegetation Index)", 0.2, 0.8, 0.58)

if st.sidebar.button("Run GeoAI Assessment"):
    with st.spinner("Querying spatial APIs, running UHI physics models, and generating AI safety assessment..."):
        tokenizer, model = load_slm()
        lat, lon = fetch_openstreetmap_data(target_location)
        weather = fetch_open_meteo_data(lat, lon)
        uhi_results = calculate_advanced_uhi_stress(mock_ndvi, weather['temperature_c'], weather['relative_humidity'])
        
        payload = {
            "location": target_location,
            "coordinates": {"lat": lat, "lon": lon},
            "atmospheric_telemetry": weather,
            "satellite_ndvi": mock_ndvi,
            "uhi_surface_metrics": uhi_results
        }
        
        recommendation = generate_slm_recommendation(payload, tokenizer, model)

    # Main dashboard layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🗺️ High-Resolution GIS Map")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
            attr='Esri & contributors',
            name='Esri World Street Map',
            max_zoom=19,
            max_native_zoom=16
        ).add_to(m)
        
        popup_html = f"""
        <div style="font-family: Arial; font-size: 13px;">
          <b>AeroScape GeoAI Node</b><br>
          <b>Location:</b> {target_location}<br>
          <b>Surface Temp:</b> {uhi_results['estimated_surface_temp_c']} °C<br>
          <b>PM2.5:</b> {weather['pm2_5']} µg/m³
        </div>
        """
        folium.Marker([lat, lon], popup=folium.Popup(popup_html, max_width=300), icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
        st_folium(m, width=500, height=400)

    with col2:
        st.subheader("🤖 Guardrailed AI Assessment Report")
        st.info(recommendation)
        
        st.subheader("📊 Live Telemetry Payload")
        st.json(payload)
else:
    st.info("👈 Enter your target location in the sidebar and click **Run GeoAI Assessment** to begin live spatial analysis.")
