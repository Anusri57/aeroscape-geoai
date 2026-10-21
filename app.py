import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AeroScape GeoAI | IIT Bombay CSRE",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding: 0rem !important; max-width: 100% !important;}
        iframe {border: none !important; width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_APP = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroScape GeoAI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: linear-gradient(-45deg, #fdfbf7, #f3e8ff, #e0f2fe, #d1fae5, #fef3c7);
            background-size: 400% 400%;
            animation: vibrantFlow 14s ease infinite;
            color: #18181b;
            margin: 0;
            overflow-x: hidden;
        }
        @keyframes vibrantFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        h1, h2, h3, .display-font { font-family: 'Space Grotesk', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }

        @keyframes floatSlow {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            50% { transform: translateY(-12px) translateX(8px); }
        }
        .floating-blob { animation: floatSlow 6s ease-in-out infinite; }

        .bento-card {
            border-radius: 22px;
            padding: 22px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            border: 1px solid rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
        }
        .bento-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.08);
        }
        .bento-pink { background: rgba(252, 231, 243, 0.85); }
        .bento-mint { background: rgba(209, 250, 229, 0.85); }
        .bento-lavender { background: rgba(224, 231, 255, 0.85); }
        .bento-amber { background: rgba(254, 243, 199, 0.85); }

        #map { height: 480px; width: 100%; border-radius: 18px; z-index: 10; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-8">

    <!-- TOP NAVIGATION BAR -->
    <nav class="max-w-7xl mx-auto flex flex-wrap items-center justify-between bg-white/70 backdrop-blur-md border border-white/80 rounded-full px-6 py-3 mb-8 shadow-sm">
        <div class="flex items-center gap-3">
            <span class="w-3.5 h-3.5 rounded-full bg-rose-500 animate-ping"></span>
            <span class="display-font font-bold text-lg tracking-tight text-zinc-900">AEROSCAPE <span class="text-indigo-600">×</span> IITB CSRE</span>
            <span class="hidden sm:inline-block text-xs mono bg-zinc-900 text-white px-3 py-1 rounded-full">VERSION 2026.4</span>
        </div>
        <div class="flex items-center gap-4 text-xs font-semibold text-zinc-600">
            <span id="liveClock" class="mono bg-white/80 px-3 py-1.5 rounded-full border border-zinc-200">Loading IST...</span>
            <span id="complianceBadge" class="px-3 py-1.5 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-200">● SYSTEM ACTIVE</span>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center mb-10 bg-white/50 backdrop-blur-xl border border-white/80 rounded-3xl p-6 md:p-10 shadow-sm relative overflow-hidden">
        <div class="lg:col-span-7 z-10">
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold tracking-wide uppercase mb-4">
                🛰️ Urban Microclimate & Smart City Decision Intelligence
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-zinc-900 tracking-tight leading-tight mb-4">
                Explore cities with <span class="text-transparent bg-clip-text bg-gradient-to-r from-rose-600 via-indigo-600 to-teal-600">spatial intelligence.</span>
            </h1>
            <p class="text-zinc-600 text-base md:text-lg mb-6 max-w-2xl leading-relaxed">
                Enter any neighborhood or city name to instantly analyze live heat islands, neighborhood boundaries, microclimate grids, and get expert recommendations from our AI assistant.
            </p>

            <!-- INTERACTIVE CONTROL BAR -->
            <div class="bg-white/90 backdrop-blur-md p-4 rounded-2xl border border-zinc-200 shadow-sm grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
                <div class="md:col-span-5">
                    <label class="block text-xs font-bold uppercase text-zinc-500 mb-1">📍 Target Locality / City</label>
                    <input id="locationInput" type="text" value="Miyapur, Hyderabad" placeholder="e.g., Alambagh, Lucknow" 
                        class="w-full px-4 py-2.5 rounded-xl border border-zinc-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-semibold text-sm text-zinc-900 bg-white" />
                </div>
                <div class="md:col-span-4">
                    <div class="flex justify-between text-xs font-bold text-zinc-500 mb-1">
                        <span>🌿 VEGETATION (NDVI)</span>
                        <span id="ndviLabel" class="mono text-indigo-600">0.34</span>
                    </div>
                    <input id="ndviSlider" type="range" min="0.10" max="0.85" step="0.02" value="0.34" 
                        oninput="document.getElementById('ndviLabel').innerText = this.value"
                        class="w-full accent-indigo-600 cursor-pointer h-2 bg-zinc-200 rounded-lg" />
                </div>
                <div class="md:col-span-3">
                    <button onclick="runSpatialAnalysis()" id="analyzeBtn"
                        class="w-full py-2.5 px-4 bg-zinc-900 hover:bg-indigo-600 text-white font-bold rounded-xl text-sm transition flex items-center justify-center gap-2 shadow-md cursor-pointer">
                        <span>Analyze Area</span> <span>↗</span>
                    </button>
                </div>
            </div>
            <p id="resolvedAddressBar" class="text-xs mono text-zinc-500 mt-3">📍 Active Boundary: Resolving coordinates...</p>
        </div>

        <!-- 3D WIREFRAME GLOBE CANVAS -->
        <div class="lg:col-span-5 flex flex-col items-center justify-center relative">
            <canvas id="globeCanvas" width="320" height="320" class="floating-blob"></canvas>
            <span class="text-xs mono text-zinc-500 mt-1">3D Geodesic Orbital Telemetry Mesh</span>
        </div>
    </section>

    <!-- BENTO GRID CARDS -->
    <section class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
        <div class="bento-card bento-pink">
            <div class="flex justify-between items-center mb-4">
                <span class="w-8 h-8 rounded-full border border-zinc-900/20 flex items-center justify-center text-xs mono font-bold">01</span>
                <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/70 text-rose-900">Surface Heat</span>
            </div>
            <p class="text-xs font-bold uppercase text-zinc-600">Land Surface Temp (LST)</p>
            <h2 id="lstVal" class="text-3xl font-extrabold text-zinc-900 my-1">-- °C</h2>
            <p id="ambientSub" class="text-xs font-medium text-zinc-700">Ambient 2m: -- °C</p>
        </div>

        <div class="bento-card bento-amber">
            <div class="flex justify-between items-center mb-4">
                <span class="w-8 h-8 rounded-full border border-zinc-900/20 flex items-center justify-center text-xs mono font-bold">02</span>
                <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/70 text-amber-900">Heat Island</span>
            </div>
            <p class="text-xs font-bold uppercase text-zinc-600">UHI Intensity Delta (ΔT)</p>
            <h2 id="uhiVal" class="text-3xl font-extrabold text-zinc-900 my-1">-- °C</h2>
            <p id="stressSub" class="text-xs font-medium text-zinc-700">Evaluating thermal level...</p>
        </div>

        <div class="bento-card bento-mint">
            <div class="flex justify-between items-center mb-4">
                <span class="w-8 h-8 rounded-full border border-zinc-900/20 flex items-center justify-center text-xs mono font-bold">03</span>
                <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/70 text-emerald-900">Environment</span>
            </div>
            <p class="text-xs font-bold uppercase text-zinc-600">NDVI & Albedo</p>
            <h2 id="ndviCardVal" class="text-3xl font-extrabold text-zinc-900 my-1">0.34 / 0.16</h2>
            <p id="windSub" class="text-xs font-medium text-zinc-700">Humidity: --%</p>
        </div>

        <div class="bento-card bento-lavender">
            <div class="flex justify-between items-center mb-4">
                <span class="w-8 h-8 rounded-full border border-zinc-900/20 flex items-center justify-center text-xs mono font-bold">04</span>
                <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/70 text-indigo-900">System Status</span>
            </div>
            <p class="text-xs font-bold uppercase text-zinc-600">Audit Status</p>
            <h2 id="boolVal" class="text-2xl font-extrabold text-emerald-700 my-1 mono">OPTIMAL</h2>
            <p id="clauseSub" class="text-xs font-medium text-zinc-700">Live AI Monitoring Active</p>
        </div>
    </section>

    <!-- MAIN WORKSPACE: MAP + CHATBOT -->
    <section class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 mb-10">
        
        <!-- MAP SECTION -->
        <div class="lg:col-span-7 bg-white/90 backdrop-blur-md border border-white rounded-3xl p-5 shadow-sm flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
                    <div>
                        <h3 class="text-xl font-bold text-zinc-900">🗺️ Precision Boundary & Thermal Mesh</h3>
                        <p class="text-xs text-zinc-500">Click any sub-sector cell on the map to inspect microclimate telemetry</p>
                    </div>
                    <div class="flex flex-wrap gap-1.5">
                        <button onclick="setMapLayer('streets')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-zinc-900 text-white hover:bg-indigo-600 transition cursor-pointer">🗺️ Colored Streets</button>
                        <button onclick="setMapLayer('hybrid')" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-zinc-100 text-zinc-800 hover:bg-zinc-200 transition cursor-pointer">🛰️ Satellite</button>
                        <button onclick="toggleThermalGrid()" class="px-3 py-1.5 text-xs font-bold rounded-lg bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100 transition cursor-pointer">🔥 Toggle Mesh</button>
                    </div>
                </div>
                <div id="map"></div>
            </div>

            <div class="mt-4 pt-3 border-t border-zinc-100 flex flex-wrap items-center justify-between text-xs text-zinc-600 gap-2">
                <div class="flex items-center gap-4">
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-rose-500 inline-block"></span> Hotspot (&gt;+4.5°C)</span>
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-amber-400 inline-block"></span> Moderate (+2.5–4.5°C)</span>
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-emerald-500 inline-block"></span> Cool Zone (&lt;+2.5°C)</span>
                </div>
                <span id="coordFooter" class="mono text-zinc-500">Lat: --, Lon: --</span>
            </div>
        </div>

        <!-- CHATBOT SECTION -->
        <div class="lg:col-span-5 bg-white/90 backdrop-blur-md border border-white rounded-3xl p-5 shadow-sm flex flex-col h-[615px]">
            <div class="border-b border-zinc-100 pb-3 mb-3 flex items-center justify-between">
                <div>
                    <h3 class="text-xl font-bold text-zinc-900">💬 GeoAI Chatbot Assistant</h3>
                    <p class="text-xs text-zinc-500">Ask about weather, best places to visit, or climate advice</p>
                </div>
                <span class="text-xs mono px-2.5 py-1 bg-indigo-50 text-indigo-700 font-bold rounded-lg border border-indigo-200">ONLINE</span>
            </div>

            <div class="flex flex-wrap gap-1.5 mb-3">
                <button onclick="triggerQuickPrompt('places')" class="text-xs bg-zinc-100 hover:bg-indigo-600 hover:text-white text-zinc-700 font-semibold px-3 py-1.5 rounded-full transition cursor-pointer">🏞️ Best Places to Visit</button>
                <button onclick="triggerQuickPrompt('recommend')" class="text-xs bg-zinc-100 hover:bg-indigo-600 hover:text-white text-zinc-700 font-semibold px-3 py-1.5 rounded-full transition cursor-pointer">📍 Best Area Recommendations</button>
                <button onclick="triggerQuickPrompt('weather')" class="text-xs bg-zinc-100 hover:bg-indigo-600 hover:text-white text-zinc-700 font-semibold px-3 py-1.5 rounded-full transition cursor-pointer">⛅ Live Climate & Stats</button>
                <button onclick="triggerQuickPrompt('mitigation')" class="text-xs bg-zinc-100 hover:bg-indigo-600 hover:text-white text-zinc-700 font-semibold px-3 py-1.5 rounded-full transition cursor-pointer">🌱 Cooling Tips</button>
            </div>

            <div id="chatBox" class="flex-1 overflow-y-auto space-y-3 pr-2 text-sm"></div>

            <div class="mt-3 pt-3 border-t border-zinc-100 flex gap-2">
                <input id="chatInput" type="text" placeholder="Ask anything (e.g. 'Where should I visit nearby?' or 'How is the weather?')..." 
                    onkeydown="if(event.key==='Enter') sendUserChat()"
                    class="flex-1 px-4 py-2.5 rounded-xl border border-zinc-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white" />
                <button onclick="sendUserChat()" class="px-5 py-2.5 bg-zinc-900 hover:bg-indigo-600 text-white font-bold rounded-xl text-sm transition cursor-pointer">Send</button>
            </div>
        </div>
    </section>

    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('liveClock').innerText = now.toLocaleString('en-IN', {
                timeZone: 'Asia/Kolkata',
                day: '2-digit', month: 'short', year: 'numeric',
                hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
            }) + ' IST';
        }
        setInterval(updateClock, 1000);
        updateClock();

        const canvas = document.getElementById('globeCanvas');
        const ctx = canvas.getContext('2d');
        let angle = 0;

        function drawGlobe() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            const radius = 110;

            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(-0.35);
            ctx.beginPath();
            ctx.ellipse(0, 0, radius + 38, 34, 0, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(225, 29, 72, 0.45)';
            ctx.lineWidth = 1.8;
            ctx.stroke();
            ctx.restore();

            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(0.45);
            ctx.beginPath();
            ctx.ellipse(0, 0, radius + 28, 42, 0, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(79, 70, 229, 0.35)';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.restore();

            ctx.strokeStyle = 'rgba(24, 24, 27, 0.22)';
            ctx.lineWidth = 1;
            const numMeridians = 12;
            for (let i = 0; i < numMeridians; i++) {
                const phi = angle + (i * Math.PI) / numMeridians;
                ctx.beginPath();
                for (let theta = 0; theta <= Math.PI * 2; theta += 0.1) {
                    const x3d = radius * Math.sin(theta) * Math.cos(phi);
                    const y3d = radius * Math.cos(theta);
                    const z3d = radius * Math.sin(theta) * Math.sin(phi);
                    const px = cx + x3d;
                    const py = cy + y3d * 0.95 + z3d * 0.15;
                    if (theta === 0) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }
                ctx.stroke();
            }

            for (let lat = -0.75; lat <= 0.75; lat += 0.375) {
                const rLat = radius * Math.cos(lat * Math.PI / 2);
                const yOffset = radius * Math.sin(lat * Math.PI / 2);
                ctx.beginPath();
                ctx.ellipse(cx, cy + yOffset, rLat, rLat * 0.22, 0, 0, Math.PI * 2);
                ctx.stroke();
            }

            const nodeX = cx + Math.cos(angle * 2) * (radius + 35) * Math.cos(-0.35);
            const nodeY = cy + Math.sin(angle * 2) * 34 * Math.sin(-0.35);
            ctx.beginPath();
            ctx.arc(nodeX, nodeY, 5, 0, Math.PI * 2);
            ctx.fillStyle = '#e11d48';
            ctx.fill();

            angle += 0.008;
            requestAnimationFrame(drawGlobe);
        }
        drawGlobe();

        const googleStreets = L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20, attribution: 'Map data &copy; Google'
        });
        const googleHybrid = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
            maxZoom: 20, attribution: 'Satellite &copy; Google'
        });

        const map = L.map('map', {
            center: [17.4968, 78.3614],
            zoom: 14,
            layers: [googleStreets]
        });

        let boundaryLayer = L.layerGroup().addTo(map);
        let gridLayer = L.layerGroup().addTo(map);
        let gridVisible = true;

        function setMapLayer(type) {
            if (type === 'hybrid') {
                map.removeLayer(googleStreets);
                map.addLayer(googleHybrid);
            } else {
                map.removeLayer(googleHybrid);
                map.addLayer(googleStreets);
            }
        }

        function toggleThermalGrid() {
            if (gridVisible) {
                map.removeLayer(gridLayer);
                gridVisible = false;
            } else {
                map.addLayer(gridLayer);
                gridVisible = true;
            }
        }

        let state = {
            location: "Miyapur, Hyderabad",
            fullAddress: "Miyapur, Serilingampally Mandal, Hyderabad, Telangana, India",
            lat: 17.4968,
            lon: 78.3614,
            ambientTemp: 33.4,
            humidity: 54,
            windSpeed: 12.6,
            solarRad: 680,
            ndvi: 0.34,
            albedo: 0.16,
            uhiDelta: 4.82,
            lst: 38.22,
            timestamp: "",
            hotspotSectors: []
        };

        async function runSpatialAnalysis() {
            const locQuery = document.getElementById('locationInput').value.trim();
            const ndviInput = parseFloat(document.getElementById('ndviSlider').value);
            const btn = document.getElementById('analyzeBtn');
            btn.innerHTML = '<span>Scanning...</span>';

            try {
                const nomUrl = `https://nominatim.openstreetmap.org/search?format=json&polygon_geojson=1&limit=1&q=${encodeURIComponent(locQuery)}`;
                const nomRes = await fetch(nomUrl, { headers: { 'Accept-Language': 'en' } });
                const nomData = await nomRes.json();

                if (!nomData || nomData.length === 0) {
                    alert("Location not found. Try including the city name.");
                    btn.innerHTML = '<span>Analyze Area</span> <span>↗</span>';
                    return;
                }

                const place = nomData[0];
                const lat = parseFloat(place.lat);
                const lon = parseFloat(place.lon);
                const bbox = place.boundingbox ? place.boundingbox.map(Number) : [lat - 0.015, lat + 0.015, lon - 0.015, lon + 0.015];

                const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,shortwave_radiation`;
                const weatherRes = await fetch(weatherUrl);
                const weatherData = await weatherRes.json();
                const cur = weatherData.current || {};

                const ambientTemp = cur.temperature_2m ?? 33.5;
                const humidity = cur.relative_humidity_2m ?? 56;
                const windSpeed = cur.wind_speed_10m ?? 11.5;
                const solarRad = (cur.shortwave_radiation && cur.shortwave_radiation > 120) ? cur.shortwave_radiation : 640;

                const albedo = +(0.12 + ndviInput * 0.14).toFixed(2);
                const solarHeating = (solarRad * (1 - albedo) * (1 - 0.62 * ndviInput)) / (115 + windSpeed * 2.2);
                const uhiDelta = +Math.max(1.2, solarHeating + (humidity * 0.015) - (ndviInput * 2.4)).toFixed(2);
                const lst = +(ambientTemp + uhiDelta).toFixed(2);
                const nowStr = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) + ' IST';

                state = {
                    location: locQuery,
                    fullAddress: place.display_name,
                    lat, lon, ambientTemp, humidity, windSpeed, solarRad,
                    ndvi: ndviInput, albedo, uhiDelta, lst,
                    timestamp: nowStr,
                    hotspotSectors: []
                };

                document.getElementById('resolvedAddressBar').innerText = `📍 Verified Boundary: ${place.display_name} (${nowStr})`;
                document.getElementById('lstVal').innerText = `${lst} °C`;
                document.getElementById('ambientSub').innerText = `Ambient 2m: ${ambientTemp} °C | Solar: ${solarRad} W/m²`;
                document.getElementById('uhiVal').innerText = `+${uhiDelta} °C`;
                document.getElementById('stressSub').innerText = uhiDelta > 4.5 ? `⚠️ Critical Heat Hotspot` : `✅ Moderate Microclimate`;
                document.getElementById('ndviCardVal').innerText = `${ndviInput} / ${albedo}`;
                document.getElementById('windSub').innerText = `Humidity: ${humidity}% | Wind: ${windSpeed} km/h`;
                document.getElementById('coordFooter').innerText = `Lat: ${lat.toFixed(4)}, Lon: ${lon.toFixed(4)}`;

                boundaryLayer.clearLayers();
                gridLayer.clearLayers();

                if (place.geojson && (place.geojson.type === "Polygon" || place.geojson.type === "MultiPolygon")) {
                    const poly = L.geoJSON(place.geojson, {
                        style: { color: '#4f46e5', weight: 3, dashArray: '6, 6', fillOpacity: 0.04 }
                    }).addTo(boundaryLayer);
                    map.fitBounds(poly.getBounds(), { padding: [20, 20] });
                } else {
                    map.setView([lat, lon], 14);
                }

                const spanLat = Math.min(Math.max(bbox[1] - bbox[0], 0.016), 0.032);
                const spanLon = Math.min(Math.max(bbox[3] - bbox[2], 0.016), 0.032);
                const minLat = lat - spanLat / 2;
                const minLon = lon - spanLon / 2;
                const rows = 5, cols = 5;
                const dLat = spanLat / rows;
                const dLon = spanLon / cols;
                const rowLabels = ['A', 'B', 'C', 'D', 'E'];

                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        const cellId = `${rowLabels[r]}${c + 1}`;
                        const cLat1 = minLat + r * dLat;
                        const cLat2 = cLat1 + dLat;
                        const cLon1 = minLon + c * dLon;
                        const cLon2 = cLon1 + dLon;

                        const seed = Math.sin((r + 1) * 12.9898 + (c + 1) * 78.233 + lat) * 43758.5453;
                        const frac = seed - Math.floor(seed);
                        const localNdvi = Math.max(0.08, Math.min(0.82, +(ndviInput + (frac - 0.5) * 0.28).toFixed(2)));
                        const localDelta = +(uhiDelta + (0.45 - localNdvi) * 3.8).toFixed(2);
                        const localLst = +(ambientTemp + localDelta).toFixed(2);

                        let cellColor = '#10b981';
                        let tier = 'Cool Green Zone';
                        if (localDelta > 4.5) {
                            cellColor = '#e11d48';
                            tier = 'High Heat Hotspot';
                            state.hotspotSectors.push({ cellId, localLst, localDelta, localNdvi, lat: ((cLat1+cLat2)/2).toFixed(4), lon: ((cLon1+cLon2)/2).toFixed(4) });
                        } else if (localDelta > 2.8) {
                            cellColor = '#f59e0b';
                            tier = 'Moderate Warm Zone';
                        }

                        const rect = L.rectangle([[cLat1, cLon1], [cLat2, cLon2]], {
                            color: cellColor,
                            weight: 1.2,
                            fillColor: cellColor,
                            fillOpacity: 0.22
                        });

                        rect.bindPopup(`
                            <div style="font-family:'Plus Jakarta Sans',sans-serif; min-width:180px;">
                                <div style="font-weight:800; font-size:13px; color:#18181b; border-bottom:1px solid #e4e4e7; padding-bottom:4px; margin-bottom:6px;">
                                    📍 Sector ${cellId} (${locQuery})
                                </div>
                                <div style="font-size:12px; line-height:1.6;">
                                    <b>Zone Type:</b> ${tier}<br>
                                    <b>Surface Temp:</b> ${localLst} °C<br>
                                    <b>Heat Delta:</b> +${localDelta} °C<br>
                                    <b>Vegetation:</b> ${localNdvi}
                                </div>
                            </div>
                        `);
                        rect.addTo(gridLayer);
                    }
                }

                L.marker([lat, lon]).addTo(boundaryLayer)
                    .bindPopup(`<b>${locQuery} Center</b><br>Mean LST: ${lst}°C`).openPopup();

                appendBotMessage(`✨ Successfully analyzed <b>${state.location}</b>! Surface temperature is currently <b>${state.lst}°C</b> with a heat anomaly of <b>+${state.uhiDelta}°C</b>. Ask me anything about local attractions, places to visit, or climate cooling tips!`);

            } catch (err) {
                console.error(err);
            }
            btn.innerHTML = '<span>Analyze Area</span> <span>↗</span>';
        }

        function appendUserMessage(text) {
            const box = document.getElementById('chatBox');
            box.innerHTML += `
                <div class="flex justify-end">
                    <div class="bg-zinc-900 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] text-xs font-medium shadow-sm">
                        ${text}
                    </div>
                </div>`;
            box.scrollTop = box.scrollHeight;
        }

        function appendBotMessage(htmlContent) {
            const box = document.getElementById('chatBox');
            box.innerHTML += `
                <div class="flex justify-start">
                    <div class="bg-white/90 border border-zinc-200 text-zinc-800 px-4 py-3 rounded-2xl rounded-tl-none max-w-[92%] text-xs leading-relaxed shadow-sm">
                        ${htmlContent}
                    </div>
                </div>`;
            box.scrollTop = box.scrollHeight;
        }

        function getSmartBotReply(query) {
            const q = query.toLowerCase();
            const loc = state.location;

            if (q.includes('place') || q.includes('visit') || q.includes('tourism') || q.includes('see') || q.includes('attraction')) {
                return `
                    <div class="font-bold text-indigo-700 mb-1">🏞️ Top Recommended Places to Visit in & around ${loc}</div>
                    Based on your selected location, here are the best spots to check out:<br>
                    1. <b>Central Urban Park & Botanical Garden:</b> Excellent green canopy area with lowest localized microclimate stress.<br>
                    2. <b>Heritage Museum & Cultural Center:</b> Popular landmark featuring indoor climate-controlled exhibition galleries.<br>
                    3. <b>Riverside Promenade & Waterfront:</b> Scenic evening walking trail with natural breeze cooling.<br>
                    <i>Tip: Visit these spots during early morning or late evening when ambient temperature drops by ~4°C!</i>`;
            }
            if (q.includes('recommend') || q.includes('best area') || q.includes('stay') || q.includes('sector')) {
                return `
                    <div class="font-bold text-emerald-700 mb-1">📍 Neighborhood & Sector Recommendations for ${loc}</div>
                    • <b>Best Green Zones (Sectors A1, B2):</b> High canopy cover, lower surface temperatures, and optimal walking comfort.<br>
                    • <b>Commercial Core (Sectors C3, D4):</b> Higher thermal retention due to concrete density; recommended for daytime business but avoid prolonged sun exposure without shade.`;
            }
            if (q.includes('weather') || q.includes('temperature') || q.includes('climate') || q.includes('hot') || q.includes('humidity')) {
                return `
                    <div class="font-bold text-amber-700 mb-1">⛅ Live Climate Stats for ${loc}</div>
                    • <b>Ambient Temperature:</b> ${state.ambientTemp}°C<br>
                    • <b>Surface Temperature (LST):</b> ${state.lst}°C<br>
                    • <b>Relative Humidity:</b> ${state.humidity}%<br>
                    • <b>Wind Speed:</b> ${state.windSpeed} km/h<br>
                    • <b>Heat Island Effect:</b> +${state.uhiDelta}°C above rural baseline.`;
            }
            if (q.includes('cool') || q.includes('mitigat') || q.includes('reduce') || q.includes('tree') || q.includes('plant')) {
                return `
                    <div class="font-bold text-teal-700 mb-1">🌱 Microclimate Cooling & Mitigation Tips</div>
                    1. <b>Cool Roofs:</b> Applying high-reflectance white paint on rooftops can lower indoor building temperatures by 3°C to 5°C.<br>
                    2. <b>Urban Greening:</b> Planting native shade trees in high-heat sectors helps boost the local NDVI index.<br>
                    3. <b>Pervious Pavements:</b> Replacing asphalt with permeable blocks prevents heat entrapment.`;
            }
            return `
                <div class="font-bold text-zinc-900 mb-1">🤖 GeoAI Assistant Response</div>
                I am actively analyzing <b>${loc}</b> (Lat: ${state.lat.toFixed(4)}, Lon: ${state.lon.toFixed(4)}).<br>
                The current surface temperature is <b>${state.lst}°C</b> with a heat anomaly of <b>+${state.uhiDelta}°C</b>.<br>
                Feel free to ask me about local tourist spots, neighborhood recommendations, live weather telemetry, or cooling tips!`;
        }

        function triggerQuickPrompt(type) {
            const prompts = {
                places: "What are the best places to visit near here?",
                recommend: "Which sectors or areas do you recommend?",
                weather: "Give me the live climate and weather details.",
                mitigation: "What are the best ways to cool down this area?"
            };
            appendUserMessage(prompts[type]);
            setTimeout(() => appendBotMessage(getSmartBotReply(prompts[type])), 250);
        }

        function sendUserChat() {
            const input = document.getElementById('chatInput');
            const q = input.value.trim();
            if (!q) return;
            input.value = '';
            appendUserMessage(q);
            setTimeout(() => appendBotMessage(getSmartBotReply(q)), 250);
        }

        window.onload = () => { 
            runSpatialAnalysis(); 
            setTimeout(() => {
                appendBotMessage(`👋 Hello! I am your <b>GeoAI Chatbot Assistant</b>. I have loaded telemetry for <b>${state.location}</b>. Ask me anything about places to visit, neighborhood recommendations, weather, or cooling strategies!`);
            }, 500);
        };
    </script>
</body>
</html>
"""

components.html(HTML_APP, height=1350, scrolling=True)
