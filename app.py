import streamlit as st

# 1. Initialize session state variables
if "assessment_run" not in st.session_state:
  st.session_state.assessment_run = False
if "payload" not in st.session_state:
  st.session_state.payload = None
if "recommendation" not in st.session_state:
  st.session_state.recommendation = None

st.sidebar.header("📍 Spatial Target Configuration")
target_location = st.sidebar.text_input("Enter Location Name", "Powai, Mumbai")
mock_ndvi = st.sidebar.slider(
    "Satellite NDVI (Vegetation Index)", 0.2, 0.8, 0.58
)

# Use a checkbox so the state remains persistent and doesn't vanish
run_assessment = st.sidebar.checkbox("Run GeoAI Assessment", value=True)

if run_assessment:
  try:
    with st.spinner(
        "Querying spatial APIs, executing UHI physics models, and generating"
        " verified AI report..."
    ):
      lat, lon = fetch_openstreetmap_data(target_location)
      weather = fetch_openmeteo_data(lat, lon)
      uhi_results = calculate_advanced_uhi_stress(
          mock_ndvi, weather["temperature_c"], weather["relative_humidity"]
      )

      payload = {
          "location": target_location,
          "coordinates": {"lat": lat, "lon": lon},
          "atmospheric_telemetry": weather,
          "satellite_ndvi": mock_ndvi,
          "uhi_surface_metrics": uhi_results,
      }

      recommendation = generate_geospatial_report(payload)

    st.success(f"Assessment active for {target_location}!")

    st.write("### 🗺️ High-Resolution GIS Map")
    # (Your map display code here)

    st.write("### 📊 Guardrailed AI Assessment Report")
    st.write(recommendation)

  except Exception as e:
    st.error(f"Error executing assessment: {e}")
