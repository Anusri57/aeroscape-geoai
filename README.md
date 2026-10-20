# AeroScape GeoAI
Built for the GeoAI Hackathon at CSRE, IIT Bombay.

## Key Innovations & Architecture
- Live Satellite Remote Sensing: Fuses OpenStreetMap vector data with real-time multispectral Sentinel-2 NDVI canopy greenness via Google Earth Engine.
- Gaussian Plume Atmospheric Dispersion Physics: Models directional wind-vector pollutant diffusion from major highways and industrial zones.
- Urban Heat Island (UHI) Thermal Corrections: Calculates localized microclimate temperature stress adjustments, surface emissivity, and physiological discomfort indices.
- Zero-Hallucination Guardrails: Powered by Qwen2.5-1.5B-Instruct grounded entirely on live verified APIs with robust network fallback error handling.
- Interactive GIS Visualization: Renders high-zoom, custom-styled Esri World Street Map layers via Folium featuring live clickable telemetry popup metadata.

## Live Data Sources
- OpenStreetMap contributors (Overpass & Nominatim APIs)
- Google Earth Engine (Sentinel-2 SR Harmonized Multispectral Imagery)
- Open-Meteo (Hourly Atmospheric Forecast & Air Quality APIs)
- OSRM Routing Machine (Live travel-time traffic impedance)

## How to Run
1. Clone the repository: `git clone https://github.com/Anusri57/aeroscape-geoai.git`
2. Install dependencies: `pip install transformers accelerate torch requests folium earthengine-api numpy`
3. Run the engine: `python "main (1).py"`
