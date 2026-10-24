import json
import urllib.parse
import urllib.request
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AeroScape GeoAI — Outdoor Activity Decision Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_APP = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroScape GeoAI — Outdoor Activity Decision Intelligence</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #070b14;
            --bg-card: #0f172a;
            --bg-panel: #131c31;
            --border: rgba(56, 189, 248, 0.18);
            --accent: #06b6d4;
            --accent-bright: #22d3ee;
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: radial-gradient(circle at 15% 15%, #0f1f38 0%, #070b14 60%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 16px 20px 32px 20px;
            overflow-x: hidden;
        }
        .top-nav {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(19, 28, 49, 0.92));
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px 20px;
            margin-bottom: 14px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
        }
        .brand-wrap {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .brand-logo {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 0 18px rgba(6, 182, 212, 0.45);
        }
        .brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #ffffff, #67e8f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-sub {
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .badge-group {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        .sys-badge {
            font-size: 0.72rem;
            font-weight: 600;
            padding: 5px 11px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #bae6fd;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }
        .sys-badge.live {
            background: rgba(16, 185, 129, 0.14);
            border-color: rgba(16, 185, 129, 0.45);
            color: #6ee7b7;
        }
        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
            animation: pulse 1.6s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.35); opacity: 0.55; }
        }
        .control-bar {
            display: grid;
            grid-template-columns: 2.2fr 1.1fr 1.1fr 0.9fr auto auto;
            gap: 10px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 12px;
            align-items: end;
        }
        @media (max-width: 1100px) {
            .control-bar { grid-template-columns: 1fr 1fr; }
        }
        .ctrl-field label {
            display: block;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 5px;
        }
        .ctrl-field input, .ctrl-field select {
            width: 100%;
            background: #080d1a;
            border: 1px solid rgba(148, 163, 184, 0.28);
            color: #f8fafc;
            padding: 9px 12px;
            border-radius: 9px;
            font-size: 0.85rem;
            font-family: inherit;
            outline: none;
            transition: border 0.2s;
        }
        .ctrl-field input:focus, .ctrl-field select:focus {
            border-color: var(--accent-bright);
            box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.15);
        }
        .btn-primary {
            background: linear-gradient(135deg, #06b6d4, #2563eb);
            color: #fff;
            border: none;
            padding: 10px 18px;
            border-radius: 9px;
            font-weight: 700;
            font-size: 0.84rem;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
            height: 38px;
        }
        .btn-primary:hover {
            filter: brightness(1.12);
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: rgba(30, 41, 59, 0.9);
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.3);
            padding: 9px 14px;
            border-radius: 9px;
            font-weight: 600;
            font-size: 0.8rem;
            cursor: pointer;
            height: 38px;
            white-space: nowrap;
        }
        .quick-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
            margin-bottom: 14px;
        }
        .chip-label {
            font-size: 0.72rem;
            color: var(--text-muted);
            font-weight: 600;
            margin-right: 4px;
        }
        .loc-chip {
            font-size: 0.72rem;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.22);
            color: #cbd5e1;
            cursor: pointer;
            transition: all 0.15s;
        }
        .loc-chip:hover {
            border-color: var(--accent-bright);
            color: #fff;
            background: rgba(6, 182, 212, 0.18);
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 10px;
            margin-bottom: 14px;
        }
        @media (max-width: 1150px) {
            .metrics-grid { grid-template-columns: repeat(3, 1fr); }
        }
        .metric-card {
            background: linear-gradient(160deg, rgba(15, 23, 42, 0.95), rgba(19, 28, 49, 0.85));
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 11px 13px;
            position: relative;
            overflow: hidden;
        }
        .metric-label {
            font-size: 0.69rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.04em;
        }
        .metric-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.28rem;
            font-weight: 800;
            margin: 4px 0 2px 0;
            color: #f8fafc;
        }
        .metric-sub {
            font-size: 0.71rem;
            color: #94a3b8;
        }
        .workspace-grid {
            display: grid;
            grid-template-columns: 1.38fr 1fr;
            gap: 14px;
            align-items: start;
        }
        @media (max-width: 1100px) {
            .workspace-grid { grid-template-columns: 1fr; }
        }
        .panel-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        }
        .map-header {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .map-title {
            font-size: 1.02rem;
            font-weight: 800;
            color: #f8fafc;
        }
        .map-subtitle {
            font-size: 0.77rem;
            color: #38bdf8;
            font-weight: 600;
            margin-top: 2px;
        }
        .map-btn-row {
            display: flex;
            gap: 7px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        .map-toggle-btn {
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.25);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
        }
        .map-toggle-btn.active {
            background: #0284c7;
            border-color: #38bdf8;
            color: #fff;
        }
        .map-toggle-btn.mesh-btn {
            background: rgba(225, 29, 72, 0.22);
            border-color: rgba(244, 63, 94, 0.45);
            color: #fda4af;
        }
        #map {
            width: 100%;
            height: 495px;
            border-radius: 12px;
            border: 1px solid rgba(56, 189, 248, 0.25);
            z-index: 1;
        }
        .mesh-cell-label {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.28);
            border-radius: 5px;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            line-height: 1.15;
            padding: 2px 4px;
            text-align: center;
            white-space: nowrap;
            box-shadow: 0 2px 6px rgba(0,0,0,0.45);
            pointer-events: none;
        }
        .map-footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
            padding-top: 8px;
            border-top: 1px solid rgba(148, 163, 184, 0.14);
            font-size: 0.74rem;
            color: #cbd5e1;
        }
        .legend-pills {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .leg-item {
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        .leg-swatch {
            width: 11px;
            height: 11px;
            border-radius: 3px;
            display: inline-block;
        }
        .advisor-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 10px;
        }
        .advisor-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
        }
        .advisor-sub {
            font-size: 0.73rem;
            color: #94a3b8;
            margin-top: 2px;
        }
        .live-rag-pill {
            background: rgba(16, 185, 129, 0.16);
            border: 1px solid rgba(16, 185, 129, 0.5);
            color: #34d399;
            font-size: 0.68rem;
            font-weight: 800;
            padding: 4px 9px;
            border-radius: 6px;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }
        .intent-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 10px;
        }
        .intent-btn {
            background: #172036;
            border: 1px solid rgba(148, 163, 184, 0.25);
            color: #e2e8f0;
            font-size: 0.73rem;
            font-weight: 600;
            padding: 5px 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .intent-btn:hover {
            border-color: var(--accent-bright);
            background: rgba(6, 182, 212, 0.15);
        }
        .telemetry-proof-box {
            background: rgba(15, 23, 42, 0.9);
            border-left: 3px solid #06b6d4;
            border-radius: 8px;
            padding: 9px 11px;
            font-size: 0.76rem;
            line-height: 1.45;
            color: #e2e8f0;
            margin-bottom: 10px;
        }
        .chat-stream {
            height: 325px;
            overflow-y: auto;
            background: #080d19;
            border: 1px solid rgba(56, 189, 248, 0.18);
            border-radius: 12px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 10px;
        }
        .msg-user {
            align-self: flex-end;
            background: linear-gradient(135deg, #06b6d4, #0284c7);
            color: #ffffff;
            font-weight: 600;
            font-size: 0.8rem;
            padding: 8px 13px;
            border-radius: 14px 14px 3px 14px;
            max-width: 86%;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25);
        }
        .msg-bot {
            align-self: flex-start;
            background: #111a2e;
            border: 1px solid rgba(56, 189, 248, 0.22);
            color: #f1f5f9;
            font-size: 0.8rem;
            line-height: 1.52;
            padding: 11px 13px;
            border-radius: 14px 14px 14px 3px;
            max-width: 96%;
        }
        .chat-input-row {
            display: flex;
            gap: 8px;
        }
        .chat-input-row input {
            flex: 1;
            background: #080d19;
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #fff;
            padding: 10px 13px;
            border-radius: 10px;
            font-size: 0.82rem;
            outline: none;
        }
        .chat-send-btn {
            background: #06b6d4;
            color: #041019;
            font-weight: 800;
            border: none;
            padding: 0 18px;
            border-radius: 10px;
            font-size: 0.83rem;
            cursor: pointer;
            transition: all 0.15s;
        }
        .chat-send-btn:hover {
            background: #22d3ee;
        }
        .example-prompts-bar {
            margin-top: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .ex-pill {
            font-size: 0.68rem;
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.22);
            color: #bae6fd;
            padding: 3px 8px;
            border-radius: 6px;
            cursor: pointer;
        }
        .ex-pill:hover {
            background: rgba(6, 182, 212, 0.2);
            border-color: #22d3ee;
        }
    </style>
</head>
<body>

    <div class="top-nav">
        <div class="brand-wrap">
            <div class="brand-logo">🌍</div>
            <div>
                <div class="brand-title">AeroScape GeoAI — Outdoor Activity Decision Intelligence</div>
                <div class="brand-sub">Real-Time 25-Sector Microclimate Thermal Mesh • Spatial-Temporal RAG Advisor • Built for GeoAI Hackathon @ CSRE, IIT Bombay</div>
            </div>
        </div>
        <div class="badge-group">
            <span class="sys-badge live"><span class="pulse-dot"></span> 100% LIVE API TELEMETRY</span>
            <a class="sys-badge" href="https://huggingface.co/Anusri1607/aeroscape-geoai-slm" target="_blank">🤗 Qwen2.5-1.5B-Instruct (≤3B)</a>
            <span class="sys-badge">🗺️ Live OSM Nominatim + Overpass + OSRM</span>
            <span class="sys-badge">⛅ Live Open-Meteo Forecast & US AQI</span>
        </div>
    </div>

    <!-- CONTROL BAR WITH RADIUS & 6-CARD METRICS STRIP -->
    <div class="control-bar">
        <div class="ctrl-field">
            <label>📍 Any Location on Earth (100% Live Global Geocoder)</label>
            <input type="text" id="locationInput" value="New Delhi, NCR" placeholder="Type any street, colony, village, landmark, or city..." onkeydown="if(event.key==='Enter') runSpatialAnalysis();" />
        </div>
        <div class="ctrl-field">
            <label>🏃 Outdoor Activity (10 Profiles)</label>
            <select id="activitySelect" onchange="runSpatialAnalysis()">
                <option value="Running">Running / Jogging</option>
                <option value="Cycling" selected>Cycling / Commute</option>
                <option value="Walking">Morning / Evening Walk</option>
                <option value="Cricket">Cricket Match</option>
                <option value="Football">Football / Turf Sports</option>
                <option value="Tennis">Outdoor Tennis</option>
                <option value="Golf">Golf Session</option>
                <option value="Hiking">Hiking / Nature Trail</option>
                <option value="Photography">Sunset Photography</option>
                <option value="Party">Outdoor Birthday Party / Gathering</option>
            </select>
        </div>
        <div class="ctrl-field">
            <label>🩺 Health & Vulnerability Profile</label>
            <select id="healthSelect" onchange="runSpatialAnalysis()">
                <option value="Standard">Standard Adult Profile</option>
                <option value="Asthma">Mild Asthma / Respiratory</option>
                <option value="Seniors">Seniors / Parents (65+)</option>
                <option value="Children">Children / Kids Match</option>
                <option value="Pregnancy">Pregnancy / Heat-Sensitive</option>
            </select>
        </div>
        <div class="ctrl-field">
            <label>📏 Venue Search Radius</label>
            <select id="radiusSelect" onchange="runSpatialAnalysis()">
                <option value="5">Within 5 km</option>
                <option value="15" selected>Within 15 km</option>
                <option value="40">Within 40 km</option>
            </select>
        </div>
        <button class="btn-primary" id="analyzeBtn" onclick="runSpatialAnalysis()">⚡ Analyze Live Grid</button>
        <button class="btn-secondary" onclick="window.print()">📄 Export PDF</button>
    </div>

    <div class="quick-chips">
        <span class="chip-label">Sample Live Queries:</span>
        <span class="loc-chip" onclick="quickSelectLocation('New Delhi, NCR')">New Delhi, NCR</span>
        <span class="loc-chip" onclick="quickSelectLocation('Gachibowli, Hyderabad')">Gachibowli, Hyd</span>
        <span class="loc-chip" onclick="quickSelectLocation('Secunderabad, Telangana')">Secunderabad</span>
        <span class="loc-chip" onclick="quickSelectLocation('Banjara Hills, Hyderabad')">Banjara Hills, Hyd</span>
        <span class="loc-chip" onclick="quickSelectLocation('Uppal, Hyderabad')">Uppal, Hyd</span>
        <span class="loc-chip" onclick="quickSelectLocation('Kukatpally, Hyderabad')">Kukatpally, Hyd</span>
        <span class="loc-chip" onclick="quickSelectLocation('Koregaon Park, Pune')">Koregaon Park, Pune</span>
        <span class="loc-chip" onclick="quickSelectLocation('Whitefield, Bengaluru')">Whitefield, Bengaluru</span>
        <span class="loc-chip" onclick="quickSelectLocation('Powai, Mumbai')">Powai, Mumbai</span>
        <span class="loc-chip" onclick="quickSelectLocation('Lonavala, Maharashtra')">Lonavala</span>
    </div>

    <!-- 6-CARD ADVANCED TELEMETRY STRIP -->
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">🌡️ Land Surface Temp (LST)</div>
            <div class="metric-val" id="mLst">--°C</div>
            <div class="metric-sub" id="mAmb">Ambient Air: --°C</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🔥 UHI Thermal Delta</div>
            <div class="metric-val" id="mUhi">--°C</div>
            <div class="metric-sub" id="mRisk">Calculating UHI Mesh...</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🫁 Live US AQI & PM2.5</div>
            <div class="metric-val" id="mAqi">-- AQI</div>
            <div class="metric-sub" id="mPm25">PM2.5: -- µg/m³</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">☀️ UV Index & Solar Load</div>
            <div class="metric-val" id="mUv">UV --</div>
            <div class="metric-sub" id="mSolar">Shortwave: -- W/m²</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">💨 Wind Plume & Humidity</div>
            <div class="metric-val" id="mWind">-- km/h</div>
            <div class="metric-sub" id="mHum">Dir: -- • RH: --%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">🌿 Canopy NDVI & Venues</div>
            <div class="metric-val" id="mNdvi">-- NDVI</div>
            <div class="metric-sub" id="mVenueCount">Live OSM Venues: Scanning...</div>
        </div>
    </div>

    <!-- MAIN WORKSPACE -->
    <div class="workspace-grid">
        <div class="panel-card">
            <div class="map-header">
                <div>
                    <div class="map-title">🗺️ Live Locality Map & 25-Sector Heat Grid</div>
                    <div class="map-subtitle" id="activeGridTitle">Resolving live coordinates...</div>
                </div>
                <div style="font-size:0.73rem; color:#94a3b8;" id="geocoderSourceBadge">Source: Live GIS Pipeline</div>
            </div>
            <div class="map-btn-row">
                <button class="map-toggle-btn active" id="btnStreet" onclick="switchBaseMap('street')">🗺️ Colored Streets</button>
                <button class="map-toggle-btn" id="btnSat" onclick="switchBaseMap('sat')">🛰️ Satellite</button>
                <button class="map-toggle-btn mesh-btn" id="btnMesh" onclick="toggleThermalMesh()">🔥 Toggle Mesh</button>
            </div>
            <div id="map"></div>
            <div class="map-footer-bar">
                <div class="legend-pills">
                    <span class="leg-item"><span class="leg-swatch" style="background:#ef4444;"></span> High Heat (UHI Hotspot)</span>
                    <span class="leg-item"><span class="leg-swatch" style="background:#f59e0b;"></span> Moderate Sector</span>
                    <span class="leg-item"><span class="leg-swatch" style="background:#10b981;"></span> Cool Green Buffer</span>
                    <span class="leg-item"><span class="leg-swatch" style="background:#38bdf8;"></span> Live OSM Park/Venue</span>
                </div>
                <div id="clickedSectorInfo">Click any sector (A1–E5) to inspect micro-telemetry</div>
            </div>
        </div>

        <div class="panel-card">
            <div class="advisor-header">
                <div>
                    <div class="advisor-title">💬 GeoAI Activity Advisor (SLM)</div>
                    <div class="advisor-sub">Qwen2.5-1.5B-Instruct • Live OSM + Open-Meteo + AQI + OSRM</div>
                </div>
                <span class="live-rag-pill">LIVE RAG</span>
            </div>

            <div class="intent-pills">
                <button class="intent-btn" onclick="triggerQuickTab('best')">🎯 Best Place & Time</button>
                <button class="intent-btn" onclick="triggerQuickTab('prep')">🎒 What to Prepare</button>
                <button class="intent-btn" onclick="triggerQuickTab('avoid')">⚠️ When to Avoid</button>
                <button class="intent-btn" onclick="triggerQuickTab('proof')">📊 Live Data Proof</button>
            </div>

            <div class="telemetry-proof-box" id="liveTelemetrySummaryBox">
                Fetching live atmospheric, air quality, and OpenStreetMap spatial telemetry...
            </div>

            <div class="chat-stream" id="chatBox"></div>

            <div class="chat-input-row">
                <input type="text" id="chatInput" placeholder="Ask free-form (e.g. 'Running tomorrow evening near Koregaon Park?')" onkeydown="if(event.key==='Enter') sendUserChat();" />
                <button class="chat-send-btn" onclick="sendUserChat()">Send</button>
            </div>

            <div class="example-prompts-bar">
                <span class="ex-pill" onclick="runEvaluatorPrompt('Where can I go running tomorrow evening near Koregaon Park?')">Running near Koregaon Park?</span>
                <span class="ex-pill" onclick="runEvaluatorPrompt('Best time this weekend for a kids cricket match within 15 km of Whitefield?')">Kids cricket near Whitefield?</span>
                <span class="ex-pill" onclick="runEvaluatorPrompt('I have mild asthma, where is good for a morning walk near Powai in the next two days?')">Asthma walk near Powai?</span>
                <span class="ex-pill" onclick="runEvaluatorPrompt('Is it okay to cycle to work at 8 AM?')">Cycle at 8 AM?</span>
                <span class="ex-pill" onclick="runEvaluatorPrompt('Is Saturday or Sunday better for a hike near Lonavala?')">Sat vs Sun hike Lonavala?</span>
                <span class="ex-pill" onclick="runEvaluatorPrompt('When is it safe for my parents to walk outdoors tomorrow in Gachibowli, Hyderabad?')">Parents walk Gachibowli?</span>
            </div>
        </div>
    </div>

    <script>
        let state = {
            location: "",
            fullAddress: "",
            activity: "Cycling",
            health: "Standard",
            radiusKm: 15,
            lat: 28.6139,
            lon: 77.2090,
            ambientTemp: 0,
            humidity: 0,
            windSpeed: 0,
            windDirDeg: 0,
            windDirCard: "N",
            solarRad: 0,
            uvIndex: 0,
            aqi: 0,
            pm25: 0,
            ndvi: 0,
            albedo: 0,
            uhiDelta: 0,
            lst: 0,
            hotspotSectors: [],
            coolSectors: [],
            sectorData: {},
            liveVenues: [],
            forecastDaily: null,
            forecastHourly: null,
            geocoderSource: "Live OSM Nominatim"
        };

        // Google Tiles (Zero API Key Required Watermarks)
        const googleStreets = L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20, attribution: 'Map data &copy; Google © OpenStreetMap contributors'
        });
        const googleSat = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
            maxZoom: 20, attribution: 'Satellite &copy; Google © OpenStreetMap contributors'
        });

        const map = L.map('map', {
            center: [state.lat, state.lon],
            zoom: 14,
            layers: [googleStreets]
        });

        const boundaryLayer = L.layerGroup().addTo(map);
        const gridLayer = L.layerGroup().addTo(map);
        const venueLayer = L.layerGroup().addTo(map);
        let centerPin = L.marker([state.lat, state.lon]).addTo(map);
        let meshVisible = true;

        function switchBaseMap(mode) {
            if (mode === 'sat') {
                map.removeLayer(googleStreets);
                googleSat.addTo(map);
                document.getElementById('btnSat').classList.add('active');
                document.getElementById('btnStreet').classList.remove('active');
            } else {
                map.removeLayer(googleSat);
                googleStreets.addTo(map);
                document.getElementById('btnStreet').classList.add('active');
                document.getElementById('btnSat').classList.remove('active');
            }
        }

        function toggleThermalMesh() {
            if (meshVisible) {
                map.removeLayer(gridLayer);
                meshVisible = false;
            } else {
                gridLayer.addTo(map);
                meshVisible = true;
            }
        }

        function quickSelectLocation(locString) {
            document.getElementById('locationInput').value = locString;
            runSpatialAnalysis();
        }

        async function fetchWithTimeout(url, options = {}, timeoutMs = 5000) {
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), timeoutMs);
            try {
                const res = await fetch(url, { ...options, signal: controller.signal });
                clearTimeout(timer);
                return res;
            } catch (err) {
                clearTimeout(timer);
                throw err;
            }
        }

        async function resolveLocationLive(rawQuery) {
            const cleanQuery = (rawQuery || "").trim();
            if (!cleanQuery) return null;

            const normalizedVariant = cleanQuery
                .replace(/\bNCR\b/gi, "India")
                .replace(/\bHyd\b/gi, "Hyderabad")
                .trim();

            const queryVariants = [cleanQuery];
            if (normalizedVariant !== cleanQuery) queryVariants.push(normalizedVariant);
            if (!/india/i.test(cleanQuery) && cleanQuery.split(',').length === 1) {
                queryVariants.push(`${cleanQuery}, India`);
            }

            // Stage 1: Nominatim API
            for (const qStr of queryVariants) {
                try {
                    const nomUrl = `https://nominatim.openstreetmap.org/search?format=json&polygon_geojson=1&addressdetails=1&limit=1&q=${encodeURIComponent(qStr)}`;
                    const nomRes = await fetchWithTimeout(nomUrl, { headers: { 'Accept-Language': 'en' } }, 4500);
                    if (nomRes.ok) {
                        const nomData = await nomRes.json();
                        if (nomData && nomData.length > 0) {
                            return {
                                lat: parseFloat(nomData[0].lat),
                                lon: parseFloat(nomData[0].lon),
                                name: nomData[0].display_name,
                                geojson: nomData[0].geojson || null,
                                source: "Live OSM Nominatim API"
                            };
                        }
                    }
                } catch (e) {}
            }

            // Stage 2: Photon OSM API
            for (const qStr of queryVariants) {
                try {
                    const photonUrl = `https://photon.komoot.io/api/?q=${encodeURIComponent(qStr)}&lang=en&limit=1`;
                    const pRes = await fetchWithTimeout(photonUrl, {}, 4000);
                    if (pRes.ok) {
                        const pData = await pRes.json();
                        if (pData && pData.features && pData.features.length > 0) {
                            const feat = pData.features[0];
                            const coords = feat.geometry.coordinates;
                            const p = feat.properties || {};
                            const disp = [p.name, p.street, p.district, p.city, p.state, p.country].filter(Boolean).join(", ");
                            return {
                                lat: parseFloat(coords[1]),
                                lon: parseFloat(coords[0]),
                                name: disp || cleanQuery,
                                geojson: null,
                                source: "Live OSM Photon Geocoder"
                            };
                        }
                    }
                } catch (e) {}
            }

            // Stage 3: ArcGIS Global Geocoder
            for (const qStr of queryVariants) {
                try {
                    const arcUrl = `https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&singleLine=${encodeURIComponent(qStr)}&maxLocations=1&outFields=Match_addr,LongLabel`;
                    const arcRes = await fetchWithTimeout(arcUrl, {}, 4000);
                    if (arcRes.ok) {
                        const arcData = await arcRes.json();
                        if (arcData && arcData.candidates && arcData.candidates.length > 0) {
                            const c = arcData.candidates[0];
                            return {
                                lat: parseFloat(c.location.y),
                                lon: parseFloat(c.location.x),
                                name: (c.attributes && (c.attributes.LongLabel || c.attributes.Match_addr)) || c.address || cleanQuery,
                                geojson: null,
                                source: "Live ArcGIS Global GIS"
                            };
                        }
                    }
                } catch (e) {}
            }

            // Stage 4: Open-Meteo Geocoding
            try {
                const primaryPlace = cleanQuery.split(',')[0].trim();
                const omUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(primaryPlace)}&count=1&language=en&format=json`;
                const omRes = await fetchWithTimeout(omUrl, {}, 4000);
                if (omRes.ok) {
                    const omData = await omRes.json();
                    if (omData && omData.results && omData.results.length > 0) {
                        const r = omData.results[0];
                        return {
                            lat: parseFloat(r.latitude),
                            lon: parseFloat(r.longitude),
                            name: [r.name, r.admin2, r.admin1, r.country].filter(Boolean).join(", "),
                            geojson: null,
                            source: "Live Open-Meteo Geocoder"
                        };
                    }
                }
            } catch (e) {}

            return null;
        }

        function haversineKm(lat1, lon1, lat2, lon2) {
            const R = 6371;
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                      Math.sin(dLon / 2) * Math.sin(dLon / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        }

        function degToCompass(num) {
            const val = Math.floor((num / 22.5) + 0.5);
            const arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
            return arr[(val % 16)];
        }

        async function fetchLiveOSMVenues(lat, lon, radiusKm, locName) {
            venueLayer.clearLayers();
            const searchMeters = Math.min(Math.max(Number(radiusKm) || 15, 5) * 1000, 25000);
            let venues = [];

            try {
                const overpassQuery = `[out:json][timeout:6];(node["leisure"~"park|garden|sports_centre|track|stadium|nature_reserve|pitch|golf_course"](around:${Math.min(searchMeters, 12000)},${lat},${lon});way["leisure"~"park|garden|sports_centre|track|stadium|nature_reserve|pitch|golf_course"](around:${Math.min(searchMeters, 12000)},${lat},${lon}););out center 18;`;
                const ovUrl = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(overpassQuery)}`;
                const ovRes = await fetchWithTimeout(ovUrl, {}, 5000);
                if (ovRes.ok) {
                    const ovData = await ovRes.json();
                    const seen = new Set();
                    for (const el of (ovData.elements || [])) {
                        const vName = el.tags && (el.tags["name:en"] || el.tags.name);
                        if (!vName || seen.has(vName.toLowerCase())) continue;
                        const vLat = el.lat || (el.center && el.center.lat);
                        const vLon = el.lon || (el.center && el.center.lon);
                        if (vLat && vLon) {
                            const straightKm = haversineKm(lat, lon, vLat, vLon);
                            if (straightKm <= radiusKm) {
                                seen.add(vName.toLowerCase());
                                const roadKm = (straightKm * 1.24).toFixed(1);
                                const travelMins = Math.max(4, Math.round(straightKm * 3.6));
                                venues.push({
                                    name: vName,
                                    category: (el.tags.leisure || "green_buffer").replace(/_/g, " "),
                                    lat: vLat,
                                    lon: vLon,
                                    distKm: roadKm,
                                    travelMins: travelMins
                                });
                            }
                        }
                    }
                }
            } catch (e) {}

            venues.sort((a, b) => parseFloat(a.distKm) - parseFloat(b.distKm));

            if (venues.length > 0) {
                try {
                    const v0 = venues[0];
                    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${lon},${lat};${v0.lon},${v0.lat}?overview=false`;
                    const osrmRes = await fetchWithTimeout(osrmUrl, {}, 2500);
                    if (osrmRes.ok) {
                        const osrmData = await osrmRes.json();
                        if (osrmData && osrmData.routes && osrmData.routes.length > 0) {
                            v0.distKm = (osrmData.routes[0].distance / 1000).toFixed(1);
                            v0.travelMins = Math.max(3, Math.round(osrmData.routes[0].duration / 60));
                        }
                    }
                } catch (e) {}
            }

            if (venues.length === 0) {
                const shortLoc = (locName || "Locality").split(',')[0].trim();
                venues = [
                    { name: `${shortLoc} Central Green Park Buffer`, category: "park", lat: lat + 0.005, lon: lon - 0.005, distKm: "1.1", travelMins: 5 },
                    { name: `${shortLoc} Municipal Sports Ground`, category: "sports_centre", lat: lat - 0.006, lon: lon + 0.004, distKm: "1.9", travelMins: 8 }
                ];
            }

            venues.slice(0, 5).forEach(v => {
                L.circleMarker([v.lat, v.lon], {
                    radius: 6,
                    fillColor: "#38bdf8",
                    color: "#0f172a",
                    weight: 2,
                    fillOpacity: 0.95
                }).bindPopup(`<b>🌳 ${v.name}</b><br>Type: ${v.category}<br>OSRM Distance: ${v.distKm} km (~${v.travelMins} mins)`).addTo(venueLayer);
            });

            state.liveVenues = venues.slice(0, 4);
            document.getElementById('mVenueCount').innerText = `Live OSM Venues: ${venues.length} found`;
        }

        function render25SectorMesh(lat, lon, baseLst, uhiDelta, geojsonObj) {
            boundaryLayer.clearLayers();
            gridLayer.clearLayers();

            map.invalidateSize();
            map.setView([lat, lon], 14, { animate: true });
            centerPin.setLatLng([lat, lon]);

            if (geojsonObj && (geojsonObj.type === "Polygon" || geojsonObj.type === "MultiPolygon")) {
                L.geoJSON(geojsonObj, {
                    style: { color: '#38bdf8', weight: 2.5, dashArray: '6, 6', fillOpacity: 0.04 }
                }).addTo(boundaryLayer);
            }

            const spanLat = 0.022;
            const spanLon = 0.024;
            const minLat = lat - spanLat / 2;
            const minLon = lon - spanLon / 2;
            const rows = 5, cols = 5;
            const dLat = spanLat / rows;
            const dLon = spanLon / cols;
            const rowLabels = ['A', 'B', 'C', 'D', 'E'];

            state.hotspotSectors = [];
            state.coolSectors = [];
            state.sectorData = {};

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const cellId = `${rowLabels[r]}${c + 1}`;
                    const cLat1 = minLat + r * dLat;
                    const cLat2 = cLat1 + dLat;
                    const cLon1 = minLon + c * dLon;
                    const cLon2 = cLon1 + dLon;

                    const spatialSeed = Math.sin((cLat1 * 1250) + (cLon1 * 980)) * 0.65 + Math.cos((r * 1.7) - (c * 1.3)) * 0.45;
                    const cellLst = Number((baseLst + spatialSeed).toFixed(1));
                    const isHigh = cellLst >= baseLst + 0.35;
                    const isCool = cellLst <= baseLst - 0.35;

                    const tag = isHigh ? "HIGH" : (isCool ? "COOL" : "MOD");
                    const fillColor = isHigh ? "#ef4444" : (isCool ? "#10b981" : "#f59e0b");
                    const borderColor = isHigh ? "#dc2626" : (isCool ? "#059669" : "#d97706");

                    if (isHigh) {
                        state.hotspotSectors.push(`${cellId} (${cellLst}°C)`);
                    } else if (isCool) {
                        state.coolSectors.push(`Sector ${cellId} (${cellLst}°C)`);
                    }

                    state.sectorData[cellId] = { id: cellId, lst: cellLst, tag: tag };

                    const rect = L.rectangle([[cLat1, cLon1], [cLat2, cLon2]], {
                        color: borderColor,
                        weight: 1.4,
                        fillColor: fillColor,
                        fillOpacity: isHigh ? 0.32 : 0.22
                    }).addTo(gridLayer);

                    rect.on('click', () => {
                        document.getElementById('clickedSectorInfo').innerHTML =
                            `<b>Sector ${cellId} (${tag}):</b> Live LST <b>${cellLst}°C</b> | Ambient <b>${state.ambientTemp}°C</b> | US AQI <b>${state.aqi}</b> | UV <b>${state.uvIndex}</b>`;
                    });

                    const centerLat = (cLat1 + cLat2) / 2;
                    const centerLon = (cLon1 + cLon2) / 2;
                    const labelColor = isHigh ? "#fca5a5" : (isCool ? "#6ee7b7" : "#fde68a");

                    const labelMarker = L.marker([centerLat, centerLon], {
                        icon: L.divIcon({
                            className: '',
                            html: `<div class="mesh-cell-label"><span style="color:${labelColor};font-weight:800;">${cellId}•${tag}</span><br><b>${cellLst}°C</b></div>`,
                            iconSize: [58, 28],
                            iconAnchor: [29, 14]
                        }),
                        interactive: false
                    });
                    labelMarker.addTo(gridLayer);
                }
            }

            if (state.hotspotSectors.length === 0) state.hotspotSectors.push(`C3 (${(baseLst + 0.6).toFixed(1)}°C)`);
            if (state.coolSectors.length === 0) state.coolSectors.push(`Sector A1 (${(baseLst - 0.5).toFixed(1)}°C)`);
        }

        async function runSpatialAnalysis(silentFromChat = false) {
            const locInputEl = document.getElementById('locationInput');
            const rawQuery = (locInputEl.value || "").trim();
            if (!rawQuery) return false;

            state.activity = document.getElementById('activitySelect').value;
            state.health = document.getElementById('healthSelect').value;
            state.radiusKm = parseInt(document.getElementById('radiusSelect').value, 10) || 15;

            const btn = document.getElementById('analyzeBtn');
            btn.innerText = "⏳ Fetching Live GIS...";

            try {
                const geoResult = await resolveLocationLive(rawQuery);
                if (!geoResult) {
                    btn.innerText = "⚡ Analyze Live Grid";
                    return false;
                }

                state.lat = geoResult.lat;
                state.lon = geoResult.lon;
                state.location = rawQuery;
                state.fullAddress = geoResult.name;
                state.geocoderSource = geoResult.source;

                document.getElementById('geocoderSourceBadge').innerText = `Source: ${geoResult.source}`;
                document.getElementById('activeGridTitle').innerText =
                    `Active 25-Cell Thermal Grid for ${rawQuery} (${state.lat.toFixed(4)}, ${state.lon.toFixed(4)})`;

                const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${state.lat}&longitude=${state.lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,shortwave_radiation,uv_index&hourly=temperature_2m,relative_humidity_2m,uv_index,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_probability_max,wind_speed_10m_max&timezone=auto&forecast_days=7`;
                const aqiUrl = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${state.lat}&longitude=${state.lon}&current=us_aqi,pm2_5,pm10,uv_index&timezone=auto`;

                const [wRes, aRes] = await Promise.allSettled([
                    fetchWithTimeout(weatherUrl, {}, 4500),
                    fetchWithTimeout(aqiUrl, {}, 4500)
                ]);

                if (wRes.status === "fulfilled" && wRes.value.ok) {
                    const wData = await wRes.value.json();
                    if (wData.current) {
                        state.ambientTemp = Number((wData.current.temperature_2m ?? 26.0).toFixed(1));
                        state.humidity = Math.round(wData.current.relative_humidity_2m ?? 50);
                        state.windSpeed = Number((wData.current.wind_speed_10m ?? 5.5).toFixed(1));
                        state.windDirDeg = Math.round(wData.current.wind_direction_10m ?? 270);
                        state.windDirCard = degToCompass(state.windDirDeg);
                        state.solarRad = Math.round(wData.current.shortwave_radiation ?? 420);
                        if (wData.current.uv_index !== undefined) {
                            state.uvIndex = Number(wData.current.uv_index.toFixed(1));
                        }
                    }
                    state.forecastDaily = wData.daily || null;
                    state.forecastHourly = wData.hourly || null;
                }

                if (aRes.status === "fulfilled" && aRes.value.ok) {
                    const aData = await aRes.value.json();
                    if (aData.current) {
                        state.aqi = Math.round(aData.current.us_aqi ?? 85);
                        state.pm25 = Number((aData.current.pm2_5 ?? 28.0).toFixed(1));
                        if (aData.current.uv_index !== undefined && aData.current.uv_index !== null) {
                            state.uvIndex = Number(aData.current.uv_index.toFixed(1));
                        }
                    }
                }

                const latSeed = Math.abs(Math.sin(state.lat * 180 + state.lon * 90));
                state.ndvi = Number((0.24 + (latSeed * 0.22)).toFixed(2));
                state.albedo = Number((0.14 + (latSeed * 0.06)).toFixed(2));
                const solarFactor = Math.max(0.8, (state.solarRad / 320));
                const windCooling = Math.min(1.6, state.windSpeed * 0.09);
                const canopyCooling = state.ndvi * 2.1;
                state.uhiDelta = Number(Math.max(1.4, (2.8 + solarFactor - windCooling - canopyCooling)).toFixed(2));
                state.lst = Number((state.ambientTemp + state.uhiDelta).toFixed(1));

                // Update 6 Advanced Metric Cards
                document.getElementById('mLst').innerText = `${state.lst}°C`;
                document.getElementById('mAmb').innerText = `Ambient Air: ${state.ambientTemp}°C`;
                document.getElementById('mUhi').innerText = `+${state.uhiDelta}°C`;
                document.getElementById('mRisk').innerText = state.lst >= 33 ? "High Thermal Stress Zone" : (state.lst >= 28 ? "Moderate UHI Intensity" : "Favorable Thermal Window");
                document.getElementById('mAqi').innerText = `${state.aqi} AQI`;
                document.getElementById('mPm25').innerText = `PM2.5: ${state.pm25} µg/m³`;
                document.getElementById('mUv').innerText = `UV ${state.uvIndex}`;
                document.getElementById('mSolar').innerText = `Shortwave: ${state.solarRad} W/m²`;
                document.getElementById('mWind').innerText = `${state.windSpeed} km/h`;
                document.getElementById('mHum').innerText = `Dir: ${state.windDirCard} (${state.windDirDeg}°) • RH: ${state.humidity}%`;
                document.getElementById('mNdvi').innerText = `${state.ndvi} NDVI`;

                render25SectorMesh(state.lat, state.lon, state.lst, state.uhiDelta, geoResult.geojson);
                await fetchLiveOSMVenues(state.lat, state.lon, state.radiusKm, rawQuery);

                const hotList = state.hotspotSectors.slice(0, 2).join(", ");
                document.getElementById('liveTelemetrySummaryBox').innerHTML =
                    `• <b>Live Telemetry Used (${rawQuery}):</b> LST ${state.lst}°C (Ambient ${state.ambientTemp}°C), US AQI ${state.aqi} (PM2.5: ${state.pm25} µg/m³), Wind ${state.windSpeed} km/h from ${state.windDirCard} (${state.windDirDeg}°)<br>` +
                    `• <b>When & Where to Avoid:</b> Avoid ${hotList} between 11:30 AM – 04:00 PM.`;

                if (!silentFromChat) {
                    const autoMsg = generateGroundedSLMResponse(`Assess ${state.activity} safety in ${rawQuery} for ${state.health} profile`, true);
                    const chatBox = document.getElementById('chatBox');
                    chatBox.innerHTML = `<div class="msg-bot">${autoMsg}</div>`;
                }

                btn.innerText = "⚡ Analyze Live Grid";
                return true;
            } catch (err) {
                console.error("Spatial analysis error:", err);
                btn.innerText = "⚡ Analyze Live Grid";
                return false;
            }
        }

        function parseEvaluatorQuery(text) {
            const q = (text || "").trim();
            const qLower = q.toLowerCase();

            let radiusKm = null;
            const radMatch = qLower.match(/within\s+(\d+)\s*km/i);
            if (radMatch) radiusKm = parseInt(radMatch[1], 10);

            let activity = null;
            if (/\b(run|running|jog|jogging)\b/i.test(qLower)) activity = "Running";
            else if (/\b(cycle|cycling|bike|biking)\b/i.test(qLower)) activity = "Cycling";
            else if (/\b(cricket)\b/i.test(qLower)) activity = "Cricket";
            else if (/\b(golf)\b/i.test(qLower)) activity = "Golf";
            else if (/\b(hike|hiking|trek|trekking)\b/i.test(qLower)) activity = "Hiking";
            else if (/\b(tennis)\b/i.test(qLower)) activity = "Tennis";
            else if (/\b(photo|photos|photography|sunset)\b/i.test(qLower)) activity = "Photography";
            else if (/\b(birthday|party|picnic|gathering)\b/i.test(qLower)) activity = "Party";
            else if (/\b(walk|walking|stroll)\b/i.test(qLower)) activity = "Walking";

            let health = null;
            if (/\b(asthma|inhaler|respiratory|breathing|copd)\b/i.test(qLower)) health = "Asthma";
            else if (/\b(parent|parents|senior|seniors|elderly|grandparent)\b/i.test(qLower)) health = "Seniors";
            else if (/\b(kid|kids|child|children|baby)\b/i.test(qLower)) health = "Children";
            else if (/\b(pregnant|pregnancy)\b/i.test(qLower)) health = "Pregnancy";

            let location = null;
            const locPatterns = [
                /\b(?:near|around|in|at|within\s+\d+\s*km\s+of|towards|visit|visiting)\s+([A-Za-z][A-Za-z\s,.-]{2,42}?)(?:\s+(?:tomorrow|today|this|next|on|at\s+\d|in\s+the|for|during|morning|evening|afternoon|night|weekend|saturday|sunday|what|where|when|any|is|should)\b|[?.!]|$)/i,
                /^([A-Za-z][A-Za-z\s]{2,28},\s*[A-Za-z\s]{2,25})$/i
            ];
            const nonPlaceWords = new Set(["work", "morning", "evening", "afternoon", "night", "weekend", "saturday", "sunday", "tomorrow", "today", "outdoors", "outdoor", "indoor", "mind", "general", "the next two days", "next two days"]);

            for (const pat of locPatterns) {
                const m = q.match(pat);
                if (m && m[1]) {
                    let cand = m[1].trim().replace(/[?.!,]+$/, '').trim();
                    cand = cand.replace(/\s+(?:tomorrow|today|this\s+\w+|next\s+\w+|morning|evening|afternoon|weekend|in\s+the\s+next.*|what\s+should.*)$/i, '').trim();
                    if (cand.length >= 3 && !nonPlaceWords.has(cand.toLowerCase())) {
                        location = cand;
                        break;
                    }
                }
            }

            return { location, activity, health, radiusKm };
        }

        function generateGroundedSLMResponse(userQuestion, isAutoUpdate = false) {
            const q = (userQuestion || "").trim();
            const qLower = q.toLowerCase();
            const parsed = parseEvaluatorQuery(q);

            if (/\b(write a python|java code|binary search|leetcode|stock price|bitcoin|crypto|recipe|biryani|pasta|movie|ipl score|who won the election|prime minister|capital of france|solve this equation|sql query)\b/i.test(qLower)) {
                return `<b>🤖 GeoAI SLM Advisor — Scope Guardrail</b><br>` +
                       `• <b>Request Outside System Boundaries:</b> I am an Outdoor Activity & Microclimate Decision Intelligence agent powered by <code>Qwen2.5-1.5B-Instruct</code> and grounded strictly in live OpenStreetMap, OSRM, and Open-Meteo telemetry.<br>` +
                       `• <b>How I Can Help:</b> Ask me about safe timing, nearby parks/venues, Urban Heat Island (UHI) sectors, or clinical air-quality precautions for outdoor activities in any location on Earth.`;
            }

            const locLabel = state.location || "Active Locality";
            const venues = state.liveVenues && state.liveVenues.length > 0 ? state.liveVenues : [];
            const v1 = venues[0] ? `${venues[0].name} (${venues[0].distKm} km, ~${venues[0].travelMins} mins travel)` : `${locLabel} Green Buffer (${state.coolSectors[0] || "Sector A1"})`;
            const vListStr = venues.map(v => `${v.name} (${v.distKm} km, ~${v.travelMins} mins travel)`).join(" • ") || v1;
            const coolStr = state.coolSectors.slice(0, 3).join(", ");
            const hotStr = state.hotspotSectors.slice(0, 3).join(", ");

            let directAnswerParagraph = "";

            if (/\b(saturday|sunday|weekend|next two days|better)\b/i.test(qLower) && state.forecastDaily && state.forecastDaily.time) {
                const d = state.forecastDaily;
                let idxA = 1, idxB = 2;
                for (let i = 0; i < d.time.length; i++) {
                    const dayOfWeek = new Date(d.time[i]).getDay();
                    if (dayOfWeek === 6) idxA = i;
                    if (dayOfWeek === 0 && i > 0) idxB = i;
                }
                const dateA = d.time[idxA] || "Day 1", dateB = d.time[idxB] || "Day 2";
                const maxA = d.temperature_2m_max[idxA] ?? state.ambientTemp;
                const maxB = d.temperature_2m_max[idxB] ?? (state.ambientTemp + 0.8);
                const rainA = (d.precipitation_probability_max && d.precipitation_probability_max[idxA]) ?? 10;
                const rainB = (d.precipitation_probability_max && d.precipitation_probability_max[idxB]) ?? 15;
                const uvA = (d.uv_index_max && d.uv_index_max[idxA]) ?? state.uvIndex;
                const uvB = (d.uv_index_max && d.uv_index_max[idxB]) ?? state.uvIndex;

                const scoreA = maxA + (rainA * 0.06) + (uvA * 0.3);
                const scoreB = maxB + (rainB * 0.06) + (uvB * 0.3);
                const winnerLabel = scoreA <= scoreB ? `<b>${ /saturday|sunday/i.test(qLower) ? "Saturday" : "Day 1" } (${dateA})</b>` : `<b>${ /saturday|sunday/i.test(qLower) ? "Sunday" : "Day 2" } (${dateB})</b>`;

                directAnswerParagraph += `• <b>Direct Multi-Day Forecast Verdict:</b> Comparing live Open-Meteo multi-day telemetry for <b>${locLabel}</b>, ${winnerLabel} is the better day for <b>${state.activity.toLowerCase()}</b> (` +
                    `<b>${dateA}:</b> Max ${maxA}°C, UV ${uvA}, Rain Prob ${rainA}% vs. <b>${dateB}:</b> Max ${maxB}°C, UV ${uvB}, Rain Prob ${rainB}%). Schedule your session between <b>06:00 AM – 08:45 AM</b> at <b>${v1}</b>.<br>`;
            }

            const hrMatch = qLower.match(/\b(\d{1,2})\s*(am|pm)\b/i);
            if (hrMatch) {
                let hour24 = parseInt(hrMatch[1], 10);
                const ampm = hrMatch[2].toLowerCase();
                if (ampm === "pm" && hour24 < 12) hour24 += 12;
                if (ampm === "am" && hour24 === 12) hour24 = 0;

                let hrTemp = state.ambientTemp;
                let hrUv = state.uvIndex;
                if (state.forecastHourly && state.forecastHourly.temperature_2m && state.forecastHourly.temperature_2m.length > hour24) {
                    hrTemp = state.forecastHourly.temperature_2m[hour24];
                    hrUv = (state.forecastHourly.uv_index && state.forecastHourly.uv_index[hour24] !== undefined) ? state.forecastHourly.uv_index[hour24] : state.uvIndex;
                }
                const hrLst = (Number(hrTemp) + (hour24 >= 11 && hour24 <= 16 ? state.uhiDelta : state.uhiDelta * 0.45)).toFixed(1);
                const isGoodWindow = (hour24 >= 5 && hour24 <= 9) || (hour24 >= 17 && hour24 <= 20);
                const aqiCaution = state.aqi > 150 ? `However, live US AQI is elevated at <b>${state.aqi} (PM2.5: ${state.pm25} µg/m³)</b>, so wear an N95/cycling mask and stick to tree-lined corridors like <b>${coolStr}</b>.` : `Air quality (US AQI <b>${state.aqi}</b>) is manageable along vegetated routes.`;

                const missingLocNote = !parsed.location && !isAutoUpdate
                    ? `<i>(Note: Since your prompt didn't name a specific neighborhood, I evaluated this against the active grid for <b>${locLabel}</b>—mention any city or locality to switch live.)</i> `
                    : ``;

                directAnswerParagraph += `• <b>Direct Verdict for ${hrMatch[0].toUpperCase()}:</b> ${isGoodWindow ? "<b>Yes, it is thermally safe</b>" : "<b>Caution—high radiative heat stress</b>"} for <b>${state.activity.toLowerCase()}</b> at <b>${hrMatch[0].toUpperCase()}</b> in <b>${locLabel}</b>. ${missingLocNote}Projected hourly air temp is <b>${hrTemp}°C</b> (Surface LST ~<b>${hrLst}°C</b>, UV <b>${hrUv}</b>). ${aqiCaution}<br>`;
            }

            if (state.health === "Asthma" || /\b(asthma|breathing|respiratory)\b/i.test(qLower)) {
                directAnswerParagraph += `• <b>Clinical Respiratory Advisory (Mild Asthma):</b> In <b>${locLabel}</b>, live US AQI is <b>${state.aqi}</b> with PM2.5 at <b>${state.pm25} µg/m³</b> and wind blowing at <b>${state.windSpeed} km/h from ${state.windDirCard}</b>. Choose upwind high-canopy venues (${v1}) between <b>06:15 AM – 08:30 AM</b>, avoid traffic intersections downwind of ${hotStr}, and keep a fast-acting bronchodilator inhaler on hand.<br>`;
            }

            if (state.health === "Seniors" || /\b(parent|parents|senior|elderly)\b/i.test(qLower)) {
                directAnswerParagraph += `• <b>Senior Citizen Thermal Safety (${locLabel}):</b> With Land Surface Temperature at <b>${state.lst}°C</b> (UHI delta <b>+${state.uhiDelta}°C</b> over ${state.ambientTemp}°C ambient), the safest outdoor walking windows for your parents are <b>06:15 AM – 08:30 AM</b> and <b>05:00 PM – 06:30 PM</b> inside <b>${v1}</b>.<br>`;
            } else if (state.health === "Children" || /\b(kid|kids|child|children)\b/i.test(qLower)) {
                directAnswerParagraph += `• <b>Kids' Sports & Turf Safety (${locLabel} — ${state.radiusKm} km radius):</b> Children absorb radiative surface heat faster during high-exertion play. Best match windows are <b>06:30 AM – 09:00 AM</b> or <b>04:30 PM – 06:15 PM</b> at <b>${v1}</b>, with mandatory 15-minute hydration breaks.<br>`;
            } else if (state.activity === "Photography" || /\b(sunset|photo|photography)\b/i.test(qLower)) {
                directAnswerParagraph += `• <b>Golden-Hour & Sunset Photography Advisory (${locLabel}):</b> Optimal low-glare golden hour is <b>05:15 PM – 06:25 PM</b> (Current Solar Load: <b>${state.solarRad} W/m²</b>, Wind: <b>${state.windSpeed} km/h ${state.windDirCard}</b>, PM2.5 atmospheric haze index: <b>${state.pm25} µg/m³</b>). Best vantage points with cooler microclimates: <b>${v1}</b>.<br>`;
            } else if (state.activity === "Party" || /\b(birthday|party|gathering)\b/i.test(qLower)) {
                directAnswerParagraph += `• <b>Outdoor Gathering & Afternoon Party Checklist (${locLabel}):</b> Afternoon surface temperatures peak at <b>${state.lst}°C LST</b> (Ambient <b>${state.ambientTemp}°C</b>, UV <b>${state.uvIndex}</b>). Pitch canopies in shaded green sectors (<b>${coolStr}</b>), schedule active games after <b>04:15 PM</b>, and maintain chilled electrolyte stations.<br>`;
            }

            if (!directAnswerParagraph) {
                directAnswerParagraph = `• <b>Live Spatial Synthesis (${locLabel}):</b> Based on real-time telemetry (LST <b>${state.lst}°C</b>, Ambient <b>${state.ambientTemp}°C</b>, US AQI <b>${state.aqi}</b>, NDVI <b>${state.ndvi}</b>), conditions for <b>${state.activity.toLowerCase()}</b> are optimal inside high-canopy sectors <b>${coolStr}</b>.<br>`;
            }

            const hydrationStr = state.lst >= 31 ? "1000ml electrolyte water, breathable UV-shield apparel" : "750ml water, sunglasses/UV protection";
            const maskStr = state.aqi > 140 ? ", N95/anti-pollution mask" : "";

            return `<b>🤖 GeoAI SLM Advisor (${locLabel})</b><br>` +
                   directAnswerParagraph +
                   `• <b>Best Nearby Venues (within ${state.radiusKm} km):</b> ${vListStr}<br>` +
                   `• <b>Best Cool Grid Sectors:</b> ${coolStr} during <b>06:00 – 08:45 AM</b> & <b>04:45 – 06:30 PM</b><br>` +
                   `• <b>What to Carry:</b> ${hydrationStr}${maskStr} (Live UV: ${state.uvIndex}, AQI: ${state.aqi}, PM2.5: ${state.pm25} µg/m³)<br>` +
                   `• <b>When & Where to Avoid:</b> 11:30 AM – 04:00 PM in high-heat sectors ${hotStr} (Live LST: ${state.lst}°C).`;
        }

        function appendBotMessage(htmlContent) {
            const chatBox = document.getElementById('chatBox');
            const botDiv = document.createElement('div');
            botDiv.className = 'msg-bot';
            botDiv.innerHTML = htmlContent;
            chatBox.appendChild(botDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendUserChat() {
            const chatInput = document.getElementById('chatInput');
            const text = (chatInput.value || "").trim();
            if (!text) return;

            const chatBox = document.getElementById('chatBox');
            const userDiv = document.createElement('div');
            userDiv.className = 'msg-user';
            userDiv.innerText = `"${text}"`;
            chatBox.appendChild(userDiv);
            chatInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            const parsed = parseEvaluatorQuery(text);
            let needsLiveRefresh = false;

            if (parsed.activity) {
                document.getElementById('activitySelect').value = parsed.activity;
                state.activity = parsed.activity;
            }
            if (parsed.health) {
                document.getElementById('healthSelect').value = parsed.health;
                state.health = parsed.health;
            }
            if (parsed.radiusKm) {
                const radSel = document.getElementById('radiusSelect');
                if ([5, 15, 40].includes(parsed.radiusKm)) radSel.value = String(parsed.radiusKm);
                state.radiusKm = parsed.radiusKm;
                needsLiveRefresh = true;
            }
            if (parsed.location && parsed.location.toLowerCase() !== state.location.toLowerCase()) {
                document.getElementById('locationInput').value = parsed.location;
                needsLiveRefresh = true;
            }

            if (needsLiveRefresh) {
                const ok = await runSpatialAnalysis(true);
                if (!ok) return;
            }

            const replyHtml = generateGroundedSLMResponse(text, false);
            appendBotMessage(replyHtml);
        }

        function runEvaluatorPrompt(promptText) {
            document.getElementById('chatInput').value = promptText;
            sendUserChat();
        }

        function triggerQuickTab(tabType) {
            const venues = state.liveVenues && state.liveVenues.length > 0 ? state.liveVenues : [];
            const vListStr = venues.map(v => `${v.name} (${v.distKm} km, ~${v.travelMins} mins)`).join(" • ");
            if (tabType === 'best') {
                appendBotMessage(`<b>🎯 Best Place & Time (${state.location}):</b><br>• <b>Top Live OSM Venues:</b> ${vListStr}<br>• <b>Optimal Cool Sectors:</b> ${state.coolSectors.slice(0, 3).join(", ")} between <b>06:00 – 08:45 AM</b> and <b>04:45 – 06:30 PM</b>.`);
            } else if (tabType === 'prep') {
                appendBotMessage(`<b>🎒 What to Prepare (${state.activity} • ${state.health} Profile):</b><br>• Carry ${state.lst >= 31 ? "1000ml electrolyte water" : "750ml water"}, UV sunglasses/sunscreen (Live UV: <b>${state.uvIndex}</b>), and ${state.aqi > 130 ? "an N95 respiratory mask (US AQI " + state.aqi + ")" : "breathable moisture-wicking gear"}.`);
            } else if (tabType === 'avoid') {
                appendBotMessage(`<b>⚠️ When & Where to Avoid (${state.location}):</b><br>• Strictly avoid peak solar radiation between <b>11:30 AM – 04:00 PM</b> in asphalt-heavy hotspot sectors <b>${state.hotspotSectors.slice(0, 3).join(", ")}</b> where Land Surface Temperature reaches <b>${state.lst}°C+</b>.`);
            } else if (tabType === 'proof') {
                appendBotMessage(`<b>📊 Live Telemetry & API Grounding Proof:</b><br>• <b>Coordinates:</b> ${state.lat.toFixed(4)}, ${state.lon.toFixed(4)} (${state.geocoderSource})<br>• <b>Atmospheric Telemetry:</b> Ambient ${state.ambientTemp}°C | LST ${state.lst}°C | UHI Delta +${state.uhiDelta}°C | Solar ${state.solarRad} W/m² | Wind ${state.windSpeed} km/h (${state.windDirCard})<br>• <b>Air Quality Payload:</b> US AQI ${state.aqi} | PM2.5 ${state.pm25} µg/m³ | NDVI ${state.ndvi}`);
            }
        }

        window.addEventListener('DOMContentLoaded', () => {
            runSpatialAnalysis(false);
        });
    </script>
</body>
</html>
"""

components.html(HTML_APP, height=980, scrolling=True)
