# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import math
import random
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Force light theme and centered layout without wide mode option
st.set_page_config(
    page_title="5G Site Estimator for Coverage & Capacity", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance UI and hide settings menu
st.markdown("""
<style>
    /* Hide settings menu */
    #MainMenu {visibility: hidden;}
    
    /* Hide "Made with Streamlit" footer */
    footer {visibility: hidden;}
    
    /* Hide header */
    header {visibility: hidden;}
    
    /* Enhance main title styling */
    .main-title {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* University info styling */
    .university-info {
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 50%, #f0f2f6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Results section styling */
    .results-container {
        background: transparent;
        padding: 1rem 0;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-title {
        font-weight: bold;
        color: #1f77b4;
        font-size: 1.1rem;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .final-recommendation {
        background: linear-gradient(45deg, #1f77b4, #17a2b8);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f77b4 0%, #17a2b8 50%, #28a745 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.3);
        position: relative;
        overflow: hidden;
        width: 100%;
        min-height: 60px;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 25px rgba(31, 119, 180, 0.4);
        background: linear-gradient(135deg, #17a2b8 0%, #28a745 50%, #20c997 100%);
        color: white !important;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 6px 15px rgba(31, 119, 180, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Logo and title
logo_path = "logo.png"
try:
    logo = Image.open(logo_path)
    
    # Create columns for better logo placement
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, caption="5G Site Estimator Logo", use_container_width=True)
except:
    st.info("📡 5G Site Estimator Logo")

# Main title with custom styling
st.markdown('<h1 class="main-title">📡 5G Site Estimator for Coverage & Capacity</h1>', unsafe_allow_html=True)

# University information with enhanced styling
st.markdown("""
<div style="margin: 1rem 0;">
    <div style="background: linear-gradient(135deg, #1f77b4, #17a2b8); color: white; padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 0.8rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15); text-align: center;">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: bold;">🎓 Faculty of Electronic Engineering</h2>
        <h3 style="margin: 0.3rem 0; font-size: 1.2rem; opacity: 0.95;">Menofia University</h3>
        <div style="height: 1px; background: rgba(255,255,255,0.3); margin: 0.5rem auto; width: 50%;"></div>
        <p style="margin: 0.3rem 0; font-size: 1rem; font-style: italic; opacity: 0.9;">Department of Telecommunication Engineering</p>
    </div>
    <div style="background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 0.8rem; border-radius: 10px; box-shadow: 0 3px 8px rgba(0,0,0,0.1); text-align: center;">
        <h4 style="margin: 0; font-size: 1.1rem; font-weight: 600;">🚀 Advanced 5G Network Planning & Optimization Tool</h4>
        <p style="margin: 0.2rem 0; font-size: 0.9rem; opacity: 0.9;">Professional RF Engineering Solution</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced header
st.sidebar.markdown("### 📥 Input Parameters")
st.sidebar.markdown("---")

# City and area selection
city_areas = {
    "Cairo": {"Nasr City": "Urban", "Heliopolis": "Urban", "Maadi": "Urban", "Zamalek": "Urban"},
    "Giza": {"Dokki": "Urban", "Mohandessin": "Urban", "6th of October": "Urban", "Sheikh Zayed": "Urban"},
    "Alexandria": {"Stanley": "Dense Urban", "Sidi Gaber": "Urban", "Smouha": "Urban"},
}

st.sidebar.markdown("**🏙️ Location Settings**")
city = st.sidebar.selectbox("Select City", list(city_areas.keys()))
area = st.sidebar.selectbox("Select Area", list(city_areas[city].keys()))
urban_type = city_areas[city][area]

st.sidebar.markdown("---")
st.sidebar.markdown("**📏 Area & Population**")
area_km2 = st.sidebar.number_input("Area Size (km²)", min_value=0.1, value=0.5, step=0.1)
population = st.sidebar.number_input("Population", min_value=0, value=10000, step=1000)
penetration_rate = st.sidebar.slider("5G Penetration Rate (%)", 0, 100, 30)
traffic_per_user = st.sidebar.number_input("Total Traffic(Mbps)", min_value=0.0, value=5.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 Antenna Configuration**")
antenna_type = st.sidebar.selectbox("Antenna Type", ["Directive", "Omni"])

st.sidebar.markdown("---")
st.sidebar.markdown("**📶 Frequency Band**")
band_option = st.sidebar.selectbox("Select 5G Frequency Band", [
    "Low-Band (e.g. 700 MHz)",
    "Mid-Band (e.g. 3.5 GHz)",
    "mmWave (e.g. 28 GHz)"
])

if band_option == "Low-Band (e.g. 700 MHz)":
    freq_mhz = 700
elif band_option == "Mid-Band (e.g. 3.5 GHz)":
    freq_mhz = 3500
else:
    freq_mhz = 28000

freq_ghz = freq_mhz / 1000

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 Link Budget Parameters**")
use_custom_mapl = st.sidebar.checkbox("Use Custom MAPL", value=False)
use_custom_link_budget = st.sidebar.checkbox("Customize Link Budget Parameters", value=False)

if use_custom_mapl:
    custom_mapl = st.sidebar.number_input("Custom MAPL (dB)", value=130.0, min_value=80.0, max_value=180.0, step=0.1)
    # Set default values for other parameters when using custom MAPL
    tx_power = 49
    tx_gain = 24
    cable_loss = 0
    penetration_loss = 24
    foliage_loss = 11
    body_loss = 3
    interference_margin = 6
    rain_margin = 0
    shadow_margin = 7
    rx_gain = 24
    noise_figure = 9
    required_sinr = 14
elif use_custom_link_budget:
    tx_power = st.sidebar.number_input("Tx Power (dBm)", value=49)
    tx_gain = st.sidebar.number_input("Tx Antenna Gain (dBi)", value=24)
    cable_loss = st.sidebar.number_input("Cable Loss (dB)", value=0)
    penetration_loss = st.sidebar.number_input("Penetration Loss (dB)", value=24)
    foliage_loss = st.sidebar.number_input("Foliage Loss (dB)", value=11)
    body_loss = st.sidebar.number_input("Body Loss (dB)", value=3)
    interference_margin = st.sidebar.number_input("Interference Margin (dB)", value=6)
    rain_margin = st.sidebar.number_input("Rain Margin (dB)", value=0)
    shadow_margin = st.sidebar.number_input("Shadow Margin (dB)", value=7)
    rx_gain = st.sidebar.number_input("Rx Antenna Gain (dBi)", value=24)
    noise_figure = st.sidebar.number_input("Receiver Noise Figure (dB)", value=9)
    required_sinr = st.sidebar.number_input("Required SINR (dB)", value=14)
else:
    tx_power = 49
    tx_gain = 24
    cable_loss = 0
    penetration_loss = 22
    foliage_loss = 7.5
    body_loss = 3
    interference_margin = 6
    rain_margin = 0
    shadow_margin = 6
    rx_gain = 0
    noise_figure = 9
    required_sinr = 14

st.sidebar.markdown("---")
st.sidebar.markdown("**⚙️ Capacity Parameters**")
bandwidth_mhz = int(st.sidebar.selectbox("Bandwidth (MHz)", options=[10, 20, 40, 60, 80, 100], index=3))
mod_order = st.sidebar.selectbox("Modulation Order (bits per symbol)", options=[2, 4, 6, 8, 10], index=3)
mimo_layers = st.sidebar.slider("Number of MIMO Layers", min_value=1, max_value=32, value=4)
utilization = st.sidebar.slider("Resource Utilization (%)", min_value=0, max_value=100, value=70) / 100.0
overhead = st.sidebar.slider("Overhead (%)", min_value=0, max_value=100, value=25) / 100.0
sectors_per_site = st.sidebar.selectbox("Sectors per Site", options=[1, 3], index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("**📶 Sub-Carrier Spacing**")
scs_khz = st.sidebar.selectbox("Sub-Carrier Spacing (kHz)", options=[15, 30, 60, 120, 240], index=1)
scs_hz = scs_khz * 1000  # Convert to Hz

duplex_mode = st.sidebar.selectbox("Duplex Mode", ["TDD", "FDD"], index=0)
if duplex_mode == "FDD":
    overhead = min(overhead, 0.12)

propagation_model = st.sidebar.selectbox("Select Propagation Model", ["UMi-Street Canyon", "UMa"])

# Calculate number of Resource Blocks dynamically based on bandwidth and SCS
bandwidth_hz = bandwidth_mhz * 1e6
n_rb = int(bandwidth_hz / (12 * scs_hz))

# Calculate MAPL (Maximum Allowable Path Loss)
thermal_noise = -174 + 10 * math.log10(bandwidth_hz)
receiver_sensitivity = thermal_noise + noise_figure + required_sinr

if use_custom_mapl:
    mapl = custom_mapl
else:
    mapl = (tx_power + tx_gain + rx_gain - cable_loss - penetration_loss - foliage_loss - body_loss
            - interference_margin - rain_margin - shadow_margin - receiver_sensitivity)

# Display calculated RB information
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Calculated Parameters**")
st.sidebar.info(f"**Resource Blocks:** {n_rb - math.floor(n_rb*0.05)}")
st.sidebar.info(f"**Total Subcarriers:** {n_rb * 12:,}")
st.sidebar.info(f"**Effective Bandwidth:** {(n_rb * 12 * scs_khz / 1000):.2f} MHz")
if use_custom_mapl:
    st.sidebar.info(f"**MAPL:** {mapl:.1f} dB (Custom)")
else:
    st.sidebar.info(f"**MAPL:** {mapl:.1f} dB (Calculated)")

def pl_umi(d_m, f_ghz, h_ue=1.5):
    d_km = d_m / 1000.0
    p_los = min(18/d_km, 1) * (1 - math.exp(-d_km/36)) + math.exp(-d_km/36)
    is_los = random.random() < p_los
    if is_los:
        pl = 32.4 + 21 * math.log10(d_m) + 20 * math.log10(f_ghz)
    else:
        pl_los = 32.4 + 21 * math.log10(d_m) + 20 * math.log10(f_ghz)
        pl_nlos = 22.4 + 35.3 * math.log10(d_m) + 21.3 * math.log10(f_ghz) - 0.3 * (h_ue - 1.5)
        pl = max(pl_los, pl_nlos)
    return pl

def pl_uma(d_m, f_ghz, h_ue=1.5):
    d_km = d_m / 1000.0
    p_los = min(18/d_km, 1) * (1 - math.exp(-d_km/63)) + math.exp(-d_km/63)
    is_los = random.random() < p_los
    if is_los:
        pl = 28 + 22 * math.log10(d_m) + 20 * math.log10(f_ghz)
    else:
        pl_los = 28 + 22 * math.log10(d_m) + 20 * math.log10(f_ghz)
        pl_nlos = 13.54 + 39.08 * math.log10(d_m) + 20 * math.log10(f_ghz) - 0.6 * (h_ue - 1.5)
        pl = max(pl_los, pl_nlos)
    return pl

def find_coverage_radius(link_budget_margin, f_ghz, model_func, max_radius_km=0.7, h_ue=1.5):
    low = 1.0
    high = max_radius_km * 1000
    for _ in range(30):
        mid = (low + high) / 2
        pl = model_func(mid, f_ghz, h_ue)
        if pl > link_budget_margin:
            high = mid
        else:
            low = mid
    return low / 1000.0

# Enhanced results section
if st.button("🚀 Calculate 5G Network Requirements", use_container_width=True):
    # Use already calculated values

    model_func = pl_umi if propagation_model == "UMi-Street Canyon" else pl_uma
    coverage_radius_km = find_coverage_radius(mapl, freq_ghz, model_func)
    coverage_radius_km *= 1.0 if antenna_type == "Directive" else 1.2
    a_site = (1.94 if antenna_type == "Directive" else 2.5) * coverage_radius_km ** 2
    num_sites_coverage = math.ceil(area_km2 / a_site)

    active_users = population * (penetration_rate / 100)
    total_traffic_mbps = traffic_per_user

    bps_per_sector = (
        n_rb * 12 * 14 * 1000 * mod_order * 0.93 * mimo_layers * utilization * (1 - overhead)
    )
    site_throughput_mbps = (bps_per_sector * sectors_per_site) / 1e6
    num_sites_capacity = math.ceil(total_traffic_mbps / site_throughput_mbps) if site_throughput_mbps > 0 else 0
    total_sites_required = max(num_sites_coverage, num_sites_capacity)
    
    # Enhanced Results Display
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("## 📊 Comprehensive Network Planning Results")
    
    # Executive Summary
    st.markdown("### 🎯 Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏗️ Total Sites Required",
            value=f"{total_sites_required}",
            delta=f"{total_sites_required - max(num_sites_coverage, num_sites_capacity)} vs minimum"
        )
    
    with col2:
        cost_estimate = total_sites_required * 250000  # $250k per site estimate
        st.metric(
            label="💰 Estimated Cost",
            value=f"${cost_estimate:,.0f}",
            delta="±15% typical range"
        )
    
    with col3:
        coverage_efficiency = (area_km2 / total_sites_required) / a_site * 100
        st.metric(
            label="📊 Coverage Efficiency",
            value=f"{coverage_efficiency:.1f}%",
            delta="vs theoretical maximum"
        )
    
    with col4:
        network_load = (total_traffic_mbps / (site_throughput_mbps * total_sites_required)) * 100
        st.metric(
            label="⚡ Network Load",
            value=f"{network_load:.1f}%",
            delta="busy hour utilization"
        )
    
    # Progress Indicators
    st.markdown("### 📈 Network Dimensioning Progress")
    col1, col2 = st.columns(2)
    
    with col1:
        coverage_progress = min(num_sites_coverage / total_sites_required, 1.0) if total_sites_required > 0 else 0
        coverage_percentage = coverage_progress * 100
        # Ensure minimum width for visibility - use larger minimum
        display_width = max(coverage_percentage, 25) if coverage_percentage > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <h4 style="color: #1f77b4; margin-bottom: 0.5rem;">📡 Coverage Requirement</h4>
            <div style="background: #f0f2f6; border-radius: 10px; padding: 0.5rem; min-height: 40px;">
                <div style="background: linear-gradient(90deg, #1f77b4, #17a2b8); width: {display_width:.1f}%; height: 25px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; min-width: 120px; white-space: nowrap;">
                    {num_sites_coverage} Sites ({coverage_percentage:.1f}%)
                </div>
            </div>
            <small style="color: #6c757d;">Coverage-driven sites: {num_sites_coverage} out of {total_sites_required} total</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        capacity_progress = min(num_sites_capacity / total_sites_required, 1.0) if total_sites_required > 0 else 0
        capacity_percentage = capacity_progress * 100
        # Ensure minimum width for visibility - use larger minimum
        display_width_capacity = max(capacity_percentage, 25) if capacity_percentage > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <h4 style="color: #ff7f0e; margin-bottom: 0.5rem;">⚡ Capacity Requirement</h4>
            <div style="background: #f0f2f6; border-radius: 10px; padding: 0.5rem; min-height: 40px;">
                <div style="background: linear-gradient(90deg, #ff7f0e, #ff6b35); width: {display_width_capacity:.1f}%; height: 25px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px; min-width: 120px; white-space: nowrap;">
                    {num_sites_capacity} Sites ({capacity_percentage:.1f}%)
                </div>
            </div>
            <small style="color: #6c757d;">Capacity-driven sites: {num_sites_capacity} out of {total_sites_required} total</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Metrics Grid
    st.markdown("### 📊 Detailed Network Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📡 Coverage Analysis")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Coverage Radius</div>
            <div class="metric-value">{coverage_radius_km:.3f} km</div>
            <small>Per site coverage radius</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Site Coverage Area</div>
            <div class="metric-value">{a_site:.3f} km²</div>
            <small>Effective area per site</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Population Density</div>
            <div class="metric-value">{population/area_km2:.0f}</div>
            <small>People per km²</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 👥 User & Traffic Analysis")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Active Users</div>
            <div class="metric-value">{int(active_users):,}</div>
            <small>Busy hour subscribers</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Traffic</div>
            <div class="metric-value">{total_traffic_mbps:.0f} Mbps</div>
            <small>Peak traffic demand</small>
        </div>
        """, unsafe_allow_html=True)
        
    
    with col3:
        st.markdown("#### 🏗️ Infrastructure Requirements")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Coverage Sites</div>
            <div class="metric-value">{num_sites_coverage}</div>
            <small>For area coverage</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Capacity Sites</div>
            <div class="metric-value">{num_sites_capacity}</div>
            <small>For traffic capacity</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Site Density</div>
            <div class="metric-value">{total_sites_required/area_km2:.1f}</div>
            <small>Sites per km²</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Site throughput and capacity details
    st.markdown("### 📊 Capacity Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🚀 Site Throughput</div>
            <div class="metric-value">{site_throughput_mbps:.0f} Mbps</div>
            <small>Per Site Capacity</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📡 Propagation Model</div>
            <div class="metric-value">{propagation_model}</div>
            <small>Selected Model</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Final recommendation with enhanced styling
    st.markdown(f"""
    <div class="final-recommendation">
        <h2 style="margin: 0; color: white;">🎯 Final Network Recommendation</h2>
        <h1 style="margin: 0.5rem 0; font-size: 3rem; color: white;">{total_sites_required}</h1>
        <h3 style="margin: 0; color: white;">Total Sites Required</h3>
        <p style="margin-top: 1rem; color: rgba(255,255,255,0.9);">
            Based on {propagation_model} propagation model with {antenna_type.lower()} antennas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced Visualizations
    st.markdown("### 📈 Advanced Network Analysis")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Site Requirements", "💰 Cost Analysis", "📡 Performance Metrics", "🔧 Technical Details"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sites comparison
            comparison_data = pd.DataFrame({
                'Requirement Type': ['Coverage', 'Capacity', 'Final Total'],
                'Number of Sites': [num_sites_coverage, num_sites_capacity, total_sites_required],
                'Color': ['#1f77b4', '#ff7f0e', '#28a745']
            })
            
            fig1 = px.bar(comparison_data, x='Requirement Type', y='Number of Sites', 
                         color='Requirement Type',
                         title='Site Requirements Breakdown',
                         color_discrete_map={'Coverage': '#1f77b4', 'Capacity': '#ff7f0e', 'Final Total': '#28a745'})
            
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11),
                title_font_size=14,
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Coverage vs Capacity gauge
            coverage_ratio = num_sites_coverage / total_sites_required * 100
            capacity_ratio = num_sites_capacity / total_sites_required * 100
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Indicator(
                mode = "gauge+number+delta",
                value = coverage_ratio,
                domain = {'x': [0, 0.48], 'y': [0.5, 1]},
                title = {'text': "Coverage Drive (%)"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1f77b4"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            
            fig2.add_trace(go.Indicator(
                mode = "gauge+number+delta",
                value = capacity_ratio,
                domain = {'x': [0.52, 1], 'y': [0.5, 1]},
                title = {'text': "Capacity Drive (%)"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#ff7f0e"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            
            # Network efficiency gauge
            efficiency = min((area_km2 / a_site) / total_sites_required * 100, 100)
            fig2.add_trace(go.Indicator(
                mode = "gauge+number",
                value = efficiency,
                domain = {'x': [0.25, 0.75], 'y': [0, 0.45]},
                title = {'text': "Network Efficiency (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#28a745"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ffcccc"},
                        {'range': [60, 80], 'color': "#ffffcc"},
                        {'range': [80, 100], 'color': "#ccffcc"}]}))
            
            fig2.update_layout(
                height=400,
                title="Network Planning Efficiency Metrics",
                font=dict(size=10),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Cost breakdown
            site_cost = 250000
            equipment_cost = total_sites_required * 150000
            installation_cost = total_sites_required * 50000
            maintenance_cost = total_sites_required * 25000
            total_capex = equipment_cost + installation_cost
            annual_opex = maintenance_cost
            
            cost_data = pd.DataFrame({
                'Cost Category': ['Equipment', 'Installation', 'Annual Maintenance'],
                'Amount': [equipment_cost, installation_cost, annual_opex],
                'Type': ['CAPEX', 'CAPEX', 'OPEX']
            })
            
            fig3 = px.pie(cost_data, values='Amount', names='Cost Category', 
                         title='Cost Breakdown (5-Year Projection)',
                         color_discrete_map={
                             'Equipment': '#1f77b4',
                             'Installation': '#ff7f0e', 
                             'Annual Maintenance': '#2ca02c'
                         })
            
            fig3.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.markdown("#### 💰 Financial Summary")
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total CAPEX</div>
                <div class="metric-value">${total_capex:,.0f}</div>
                <small>Equipment + Installation</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Annual OPEX</div>
                <div class="metric-value">${annual_opex:,.0f}</div>
                <small>Maintenance & Operations</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Cost per Site</div>
                <div class="metric-value">${site_cost:,.0f}</div>
                <small>Average site deployment</small>
            </div>
            """, unsafe_allow_html=True)
            
            roi_years = total_capex / (annual_opex * 0.3)  # Assuming 30% of opex as profit
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Payback Period</div>
                <div class="metric-value">{roi_years:.1f} years</div>
                <small>Estimated ROI timeline</small>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance metrics
            spectral_efficiency = (site_throughput_mbps / bandwidth_mhz) / sectors_per_site
            user_experience = min(site_throughput_mbps / (active_users / total_sites_required), 10)
            
            performance_data = pd.DataFrame({
                'Metric': ['Spectral Efficiency', 'User Experience', 'Network Load', 'Coverage Quality'],
                'Value': [spectral_efficiency, user_experience, network_load, coverage_efficiency],
                'Target': [4.0, 5.0, 70.0, 85.0],
                'Unit': ['bps/Hz/sector', 'Mbps/user', '%', '%']
            })
            
            fig4 = go.Figure()
            
            fig4.add_trace(go.Scatter(
                x=performance_data['Metric'],
                y=performance_data['Value'],
                mode='markers+lines',
                name='Actual',
                marker=dict(size=12, color='#1f77b4'),
                line=dict(width=3, color='#1f77b4')
            ))
            
            fig4.add_trace(go.Scatter(
                x=performance_data['Metric'],
                y=performance_data['Target'],
                mode='markers+lines',
                name='Target',
                marker=dict(size=10, color='#ff7f0e', symbol='diamond'),
                line=dict(width=2, color='#ff7f0e', dash='dash')
            ))
            
            fig4.update_layout(
                title='Network Performance vs Targets',
                xaxis_title='Performance Metrics',
                yaxis_title='Value',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Quality Indicators")
            
            # Traffic distribution
            peak_to_avg_ratio = 3.2
            avg_traffic = total_traffic_mbps / peak_to_avg_ratio
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Peak Traffic</div>
                <div class="metric-value">{total_traffic_mbps:.0f} Mbps</div>
                <small>Busy hour demand</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Average Traffic</div>
                <div class="metric-value">{avg_traffic:.0f} Mbps</div>
                <small>Daily average</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Spectral Efficiency</div>
                <div class="metric-value">{spectral_efficiency:.2f}</div>
                <small>bps/Hz per sector</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">User Experience</div>
                <div class="metric-value">{user_experience:.1f} Mbps</div>
                <small>Average per user</small>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📡 RF Performance")
            st.write(f"**Link Budget Analysis:**")
            st.write(f"- Maximum Allowable Path Loss: {mapl:.1f} dB")
            st.write(f"- Transmit Power: {tx_power} dBm")
            st.write(f"- Antenna Gains: {tx_gain + rx_gain} dB total")
            st.write(f"- System Losses: {cable_loss + penetration_loss + foliage_loss + body_loss:.1f} dB")
            st.write(f"- Margins: {interference_margin + shadow_margin + rain_margin} dB total")
            st.write(f"- Receiver Sensitivity: {receiver_sensitivity:.1f} dBm")
            st.write(f"- Thermal Noise: {thermal_noise:.1f} dBm")
            
        with col2:
            st.markdown("#### ⚙️ System Configuration")
            st.write(f"**Radio Parameters:**")
            st.write(f"- Frequency Band: {freq_ghz} GHz")
            st.write(f"- Channel Bandwidth: {bandwidth_mhz} MHz")
            st.write(f"- Resource Blocks: {n_rb}")
            st.write(f"- Modulation Order: {mod_order} bits/symbol")
            st.write(f"- MIMO Layers: {mimo_layers}")
            st.write(f"- Duplex Mode: {duplex_mode}")
            st.write(f"- Sectors per Site: {sectors_per_site}")
            st.write(f"- Antenna Type: {antenna_type}")
            st.write(f"- Propagation Model: {propagation_model}")
    
    # AI-Powered Recommendations
    st.markdown("### 🤖 Intelligent Network Recommendations")
    
    recommendations = []
    warnings = []
    
    # Generate intelligent recommendations
    if num_sites_coverage > num_sites_capacity * 1.5:
        recommendations.append("🔄 Consider using higher frequency bands or more directional antennas to improve coverage efficiency")
    elif num_sites_capacity > num_sites_coverage * 1.5:
        recommendations.append("📊 Network is capacity-limited. Consider deploying small cells or increasing spectral efficiency")
    
    if network_load > 80:
        warnings.append("⚠️ High network load detected. Consider increasing number of sites or bandwidth")
    elif network_load < 30:
        recommendations.append("💡 Network is under-utilized. Could potentially reduce sites or serve more users")
    
    if coverage_radius_km < 0.2:
        recommendations.append("📍 Very small coverage radius suggests dense urban deployment - consider small cells")
    elif coverage_radius_km > 2.0:
        recommendations.append("🌐 Large coverage radius indicates rural deployment - consider tower sharing")
    
    if total_sites_required / area_km2 > 10:
        recommendations.append("🏗️ High site density required. Consider indoor solutions or DAS systems")
    
    if penetration_rate < 20:
        recommendations.append("📈 Low 5G penetration rate. Plan for future growth and capacity expansion")
    
    # Display recommendations
    if recommendations:
        st.markdown("#### 💡 Optimization Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    
    if warnings:
        st.markdown("#### ⚠️ Network Warnings")
        for warning in warnings:
            st.warning(warning)
    

    # Quick comparison with industry benchmarks
    st.markdown("### 📏 Industry Benchmarks Comparison")
    
    benchmarks_data = pd.DataFrame({
        'Metric': ['Sites per km²', 'Cost per Site ($K)', 'Spectral Efficiency', 'User Experience'],
        'Your Network': [total_sites_required/area_km2, 250, spectral_efficiency, user_experience],
        'Industry Average': [8.5, 275, 3.2, 4.5],
        'Best Practice': [12.0, 200, 4.5, 6.0]
    })
    
    fig_benchmark = go.Figure()
    
    fig_benchmark.add_trace(go.Scatter(
        x=benchmarks_data['Metric'],
        y=benchmarks_data['Your Network'],
        mode='markers+lines',
        name='Your Network',
        marker=dict(size=12, color='#1f77b4'),
        line=dict(width=3, color='#1f77b4')
    ))
    
    fig_benchmark.add_trace(go.Scatter(
        x=benchmarks_data['Metric'],
        y=benchmarks_data['Industry Average'],
        mode='markers+lines',
        name='Industry Average',
        marker=dict(size=10, color='#ff7f0e'),
        line=dict(width=2, color='#ff7f0e', dash='dash')
    ))
    
    fig_benchmark.add_trace(go.Scatter(
        x=benchmarks_data['Metric'],
        y=benchmarks_data['Best Practice'],
        mode='markers+lines',
        name='Best Practice',
        marker=dict(size=10, color='#28a745'),
        line=dict(width=2, color='#28a745', dash='dot')
    ))
    
    fig_benchmark.update_layout(
        title='Network Performance vs Industry Benchmarks',
        xaxis_title='Performance Metrics',
        yaxis_title='Normalized Values',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_benchmark, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>🎓 <strong>Faculty of Electronic Engineering - Menofia University</strong></p>
    <p>Department of Telecommunication Engineering | 5G Network Planning Tool</p>
</div>
""", unsafe_allow_html=True) 