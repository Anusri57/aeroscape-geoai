import streamlit as st

# 1. Initialize session state variables
if "assessment_active" not in st.session_state:
  st.session_state.assessment_active = False
if "payload" not in st.session_state:
  st.session_state.payload = None
if "recommendation" not in st.session_state:
  st.session_state.recommendation = None

st.sidebar.header("📍 Spatial Target Configuration")
target_location = st.sidebar.text_input("Enter Location Name", "Powai, Mumbai")
mock_ndvi = st.sidebar.slider(
    "Satellite NDVI (Vegetation Index)", 0.2, 0.8, 0.58
)

# 2. Use a callback or direct toggle state when button is clicked
if st.sidebar.button("Run GeoAI Assessment"):
  st.session_state.assessment_active = True
  with st.spinner(
      "Querying spatial APIs, executing UHI physics models, and generating"
      " verified AI report..."
  ):
    lat, lon = fetch_openstreetmap_data(target_location)
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

# 3. Persistent Render Block (Independent of the button click state)
if st.session_state.assessment_active and st.session_state.payload:
  st.success(
      f"Active Assessment: {st.session_state.payload['location']}"
  )

  # --- PUT YOUR MAP DISPLAY CODE HERE ---
  # Example: st.pyplot(fig) or st.map(...)
  st.write("### 🗺️ High-Resolution GIS Map")
  # Ensure your map code is rendered here using st.session_state.payload

  # --- PUT YOUR REPORT DISPLAY CODE HERE ---
  st.write("### 📊 Guardrailed AI Assessment Report")
  st.write(st.session_state.recommendation)
