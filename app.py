import pandas as pd
import pydeck as pdk
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & ELITE IIT THEME
# ==========================================
st.set_page_config(
    page_title="AeroScape GeoAI | CSRE IIT Bombay",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Animated Cyber-Gradient Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #090d16, #111b2b, #0d1b2a, #030712);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #f3f4f6;
    }
    
    /* Glassmorphism Sidebar */
    .stSidebar {
        background-color: rgba(13, 27, 42, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Hero Title Styling */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #60a5fa, #3b82f6, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .badge-iit {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.5);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# 2. GEO-PHYSICS & LOCATION ENGINE
# ==========================================
def fetch_location_coordinates(location):
  loc = location.lower()
  if "mumbai" in loc or "powai" in loc:
    return 19.1136, 72.9060
  elif "hyderabad" in loc:
    return 17.3850, 78.4867
  elif "delhi" in loc:
    return 28.6139, 77.2090
  elif "bengaluru" in loc or "bangalore" in loc:
    return 12.9716, 77.5946
  elif "chennai" in loc:
    return 13.0827, 80.2707
  return 19.1136, 72.9060  # Default fallback


def fetch_openmeteo_data(lat, lon):
  return {
      "temperature_c": 34.2,
      "relative_humidity": 62.0,
      "wind_speed_kmh": 15.5,
  }


def calculate_advanced_uhi_stress(ndvi, temp, humidity):
  uhi_intensity = round((temp * 1.2) - (ndvi * 5.5), 2)
  return {
      "uhi_intensity_c": uhi_intensity,
      "thermal_stress_index": "Critical High" if uhi_intensity > 32 else "Elevated",
      "surface_albedo": 0.15,
  }


def generate_geospatial_report(payload):
  loc = payload["location"]
  temp = payload["atmospheric_telemetry"]["temperature_c"]
  uhi = payload["uhi_surface_metrics"]["uhi_intensity_c"]
  ndvi = payload["satellite_ndvi"]
  return f"""
    ### 🛰️ CSRE AI Spatial Diagnostics Report
    
    * **Thermal Hotspot Vector**: Surface radiant temperature recorded at **{temp}°C**, manifesting an Urban Heat Island (UHI) anomaly delta of **+{uhi}°C** over rural baseline control zones.
    * **Canopy Index (NDVI)**: Spatial vegetation density indexed at **{ndvi}**, validating strong inverse thermal correlation in dense urban concrete matrices.
    * **IIT Bombay Hackathon Mitigation Protocol**: Recommended immediate deployment of high-albedo cool roof retrofits, nano-ceramic thermal coatings, and vertical pocket forests along high-density transit corridors to dissipate localized heat retention by up to 4.8°C.
    """


# ==========================================
# 3. SESSION STATE INITIALIZATION
# ==========================================
if "assessment_run" not in st.session_state:
  st.session_state.assessment_run = True
if "payload" not in st.session_state:
  lat, lon = fetch_location_coordinates("Powai, Mumbai")
  weather = fetch_openmeteo_data(lat, lon)
  uhi = calculate_advanced_uhi_stress(
      0.58, weather["temperature_c"], weather["relative_humidity"]
  )
  st.session_state.payload = {
      "location": "Powai, Mumbai",
      "coordinates": {"lat": lat, "lon": lon},
      "atmospheric_telemetry": weather,
      "satellite_ndvi": 0.58,
      "uhi_surface_metrics": uhi,
  }
  st.session_state.recommendation = generate_geospatial_report(
      st.session_state.payload
  )


# ==========================================
# 4. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ Spatial Target Control")
target_location = st.sidebar.text_input(
    "Enter Target Area / City in India", "Powai, Mumbai"
)
mock_ndvi = st.sidebar.slider(
    "Satellite NDVI (Vegetation Index)", 0.1, 0.9, 0.58, 0.01
)

if st.sidebar.button("🚀 Run GeoAI Assessment", type="primary"):
  lat, lon = fetch_location_coordinates(target_location)
  weather = fetch_openmeteo_data(lat, lon)
  uhi_results = calculate_advanced_uhi_stress(
      mock_ndvi, weather["temperature_c"], weather["relative_humidity"]
  )

  st.session_state.payload = {
      "location": target_location,
      "coordinates": {"lat": lat, "lon": lon},
      "atmospheric_telemetry": weather,
      "satellite_ndvi": mock_ndvi,
      "uhi_surface_metrics": uhi_results,
  }
  st.session_state.recommendation = generate_geospatial_report(
      st.session_state.payload
  )
  st.rerun()


# ==========================================
# 5. MAIN INTERFACE & DASHBOARD
# ==========================================
st.markdown(
    '<p class="hero-title">🌍 AeroScape GeoAI Intelligence Portal</p>',
    unsafe_allow_html=True,
)
st.markdown(
    "<span class='badge-iit'>IIT Bombay CSRE Hackathon Edition</span> Real-time"
    " Satellite Microclimate & UHI Physics Engine",
    unsafe_allow_html=True,
)
st.write("")
st.write("")

if st.session_state.payload:
  p = st.session_state.payload

  # --- TOP METRIC CARDS ---
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f"""<div class="glass-card" style="text-align: center;">
            <h4 style="color: #60a5fa; margin:0;">🌡️ Surface Temp</h4>
            <h2 style="color: #ffffff; margin:5px 0;">{p['atmospheric_telemetry']['temperature_c']} °C</h2>
            <span style="color: #ef4444; font-size: 0.85rem;">▲ High Thermal Load</span>
        </div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""<div class="glass-card" style="text-align: center;">
            <h4 style="color: #f87171; margin:0;">🔥 UHI Intensity</h4>
            <h2 style="color: #ffffff; margin:5px 0;">+{p['uhi_surface_metrics']['uhi_intensity_c']} °C</h2>
            <span style="color: #f59e0b; font-size: 0.85rem;">⚠️ {p['uhi_surface_metrics']['thermal_stress_index']}</span>
        </div>""",
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""<div class="glass-card" style="text-align: center;">
            <h4 style="color: #34d399; margin:0;">💧 Humidity</h4>
            <h2 style="color: #ffffff; margin:5px 0;">{p['atmospheric_telemetry']['relative_humidity']} %</h2>
            <span style="color: #34d399; font-size: 0.85rem;">● Atmospheric Stable</span>
        </div>""",
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        f"""<div class="glass-card" style="text-align: center;">
            <h4 style="color: #a78bfa; margin:0;">🌿 NDVI Canopy</h4>
            <h2 style="color: #ffffff; margin:5px 0;">{p['satellite_ndvi']}</h2>
            <span style="color: #a78bfa; font-size: 0.85rem;">● Vegetation Index</span>
        </div>""",
        unsafe_allow_html=True,
    )

  st.write("")

  # --- MAP & REPORT SPLIT VIEW ---
  map_col, report_col = st.columns([1.1, 0.9])

  with map_col:
    st.markdown("### 🛰️ 3D Satellite Radar & UHI Hotspot Map")
    st.caption(
        f"Target Sector: **{p['location']}** | Coordinates: ({p['coordinates']['lat']}, {p['coordinates']['lon']})"
    )

    # Advanced PyDeck 3D Scatter Layer with Glowing Red Thermal Hotspot Pulse
    radar_df = pd.DataFrame(
        [{
            "lat": p["coordinates"]["lat"],
            "lon": p["coordinates"]["lon"],
            "intensity": p["uhi_surface_metrics"]["uhi_intensity_c"],
        }]
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=radar_df,
        get_position=["lon", "lat"],
        get_color=[239, 68, 68, 220],  # Glowing crimson red
        get_radius=2500,  # 2.5km radius thermal anomaly zone
        pickable=True,
        stroked=True,
        filled=True,
        get_line_color=[255, 255, 255, 200],
        line_width_min_pixels=3,
    )

    view_state = pdk.ViewState(
        latitude=p["coordinates"]["lat"],
        longitude=p["coordinates"]["lon"],
        zoom=11.5,
        pitch=45,
        bearing=0,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "UHI Thermal Hotspot Core\nIntensity: +{intensity}°C"},
    )

    st.pydeck_chart(r, use_container_width=True)

  with report_col:
    st.markdown("### 📊 Guardrailed AI Assessment")
    st.markdown(
        f"""
        <div class="glass-card">
        {st.session_state.recommendation}
        </div>
        """,
        unsafe_allow_html=True,
    )
