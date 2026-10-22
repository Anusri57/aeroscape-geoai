# AeroScape GeoAI
Built for the GeoAI Hackathon at CSRE, IIT Bombay.

## Live Application URL
- **Render Endpoint:** https://aeroscape-geoai.onrender.com

## Small Language Model (SLM) Component
- **Model Disclosed:** `Qwen/Qwen2.5-1.5B-Instruct` (1.5 Billion parameters, strictly under the ≤3B hackathon model size limit).
- **Hugging Face Model Card Repository:** https://huggingface.co/Anusri1607/aeroscape-geoai-slm.
- **Intended Use:** Spatial-temporal reasoning over live JSON telemetry payloads fetched dynamically at query time from OpenStreetMap and Open-Meteo APIs.

## Key Innovations & Architecture
- **Live Vector Mapping:** Fuses OpenStreetMap vector data (Nominatim & Overpass APIs) with localized green canopy metrics.
- **Atmospheric & Wind Vector Reasoning:** Models directional wind-vector diffusion and pollutant/PM2.5 patterns relative to major roadways and urban zones.
- **Urban Heat Island (UHI) Thermal Corrections:** Calculates localized microclimate temperature stress adjustments (LST vs. ambient) and physiological discomfort indices for 10 distinct outdoor activities.
- **Zero-Hallucination Guardrails:** Powered by Qwen2.5-1.5B-Instruct grounded entirely on live verified APIs with strict safety thresholds for sensitive profiles (Asthma, Senior Citizens, Children, Pregnancy).
- **Interactive GIS Visualization:** Renders high-zoom custom tile layers featuring a live 25-sector clickable microclimate thermal mesh with real-time sector telemetry.

## Live Data Sources Disclosed
- **Maps & Venues:** OpenStreetMap contributors via Overpass & Nominatim APIs (**© OpenStreetMap contributors**)
- **Weather & Air Quality:** Open-Meteo (Hourly Atmospheric Forecast & Air Quality APIs for live US AQI, PM2.5, and UV Index)
- **Routing & Travel Time:** OSRM (Open Source Routing Machine for venue distance and travel impedance)

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
