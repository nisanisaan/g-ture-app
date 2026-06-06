import calendar
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import date, timedelta
from src.predictor import GoldPredictor
from src.utils import Localizer

# 1. Page Configuration
st.set_page_config(page_title="G-Ture | Gold Forecaster", page_icon="✨", layout="centered")

# 2. Inject Custom CSS from file
def load_css(file_name):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("assets/style.css")

# 2b. Inject Absolute Visibility Override for the CTA Button directly
st.markdown("""
    <style>
    /* Maximize Button Text Legibility */
    div.stButton > button:first-child {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        color: #FBF5D2 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        background-color: #441004 !important;
        border: 2px solid #AD6D15 !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        width: 100% !important; 
        display: block !important;
    }

    /* Crisp White on Hover for Elite Interactive Feedback */
    div.stButton > button:first-child:hover {
        color: #FFFFFF !important;
        background-color: #79380B !important;
        border: 2px solid #AD6D15 !important;
        letter-spacing: 4px !important;
        box-shadow: 0 4px 15px rgba(68, 16, 4, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Instantiate our OOP Objects
localizer = Localizer()

@st.cache_resource
def get_predictor():
    return GoldPredictor("models/gold_model.pkl")

predictor = get_predictor()

# 4. Language Selector
lang = st.radio("Language / Bahasa", ["EN", "ID"], horizontal=True, label_visibility="collapsed")

# 5. Main UI (The Glass Card Container)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

# --- Clean Unified Dynamic Brand Header ---
# Fix 1: Wrapping the white card container, SVG, and text in a SINGLE markdown block
# This prevents Streamlit from auto-closing the div, stopping the leakage completely.
st.markdown("""
    <div class='luxury-card' style='text-align: center; padding: 2rem; margin-bottom: 20px; background-color: #FFFFFF; border-radius: 12px; box-shadow: 0 4px 15px rgba(68, 16, 4, 0.05); border: 1px solid rgba(173, 109, 21, 0.3);'>
        <!-- Inline Geometric Gold SVG Logo -->
        <svg width="64" height="64" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 15px;">
            <!-- Outer Diamond -->
            <polygon points="50,5 95,50 50,95 5,50" fill="none" stroke="#AD6D15" stroke-width="3"/>
            <!-- Inner Diamond -->
            <polygon points="50,18 82,50 50,82 18,50" fill="none" stroke="#EFBB55" stroke-width="1.5"/>
            <!-- Geometric Intersecting Lines -->
            <line x1="50" y1="5" x2="50" y2="95" stroke="#FEE39F" stroke-width="1"/>
            <line x1="5" y1="50" x2="95" y2="50" stroke="#FEE39F" stroke-width="1"/>
            <!-- Center Core Glow -->
            <circle cx="50" cy="50" r="6" fill="#AD6D15"/>
        </svg>
        <!-- Premium Brand Typography -->
        <h3 style='color:#AD6D15; margin:0; font-family:"Cormorant Garamond", serif; font-weight: 700; letter-spacing: 6px; font-size: 1.5rem;'>
            G - T U R E
        </h3>
    </div>
""", unsafe_allow_html=True)

# --- High-Contrast Title & Subtitle ---
# Fix 2: Explicit inline styles to force max contrast, bold weights, and size
st.markdown(f"""
    <h1 style='text-align: center; margin-top: 15px; color: #441004 !important; font-weight: 700 !important; font-size: 42px !important; font-family: "Cormorant Garamond", serif;'>
        {localizer.get_text('title', lang)}
    </h1>
    <p style='text-align: center; color: #79380B !important; font-weight: 600 !important; font-family: "Montserrat", sans-serif; font-size: 16px; margin-bottom: 25px;'>
        {localizer.get_text('subtitle', lang)}
    </p>
""", unsafe_allow_html=True)

st.write("---")
# --- Mode Toggle & Date Selection ---
mode_options = ["Single Day", "Date Range"] if lang == "EN" else ["Satu Hari", "Rentang Hari"]
selected_mode = st.radio("Mode", mode_options, horizontal=True, label_visibility="collapsed")

min_date = date(2026, 1, 1)
max_date = date(2027, 12, 31)
default_date = date.today() if min_date <= date.today() <= max_date else min_date

# Single Day vs Date Range Logic
if selected_mode in ["Single Day", "Satu Hari"]:
    selected_date = st.date_input(
        localizer.get_text('select_date', lang), 
        value=default_date, 
        min_value=min_date, 
        max_value=max_date
    )
    tgl_mulai = selected_date
    tgl_selesai = selected_date
else:
    # Date Range Mode setup
    default_range = (default_date, default_date + timedelta(days=7))
    selected_dates = st.date_input(
        localizer.get_text('select_date', lang), 
        value=default_range, 
        min_value=min_date, 
        max_value=max_date
    )
    
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        tgl_mulai = selected_dates[0]
        tgl_selesai = selected_dates[1]
    else:
        tgl_mulai = selected_dates[0] if isinstance(selected_dates, tuple) else selected_dates
        tgl_selesai = None

# --- Prediction Action & Backend Loop Execution ---
if st.button(localizer.get_text('btn_predict', lang)):
    if predictor.model is None:
        st.error(localizer.get_text('error_model', lang))
    elif tgl_selesai is None:
        warning_msg = "Please select both start and end dates." if lang == "EN" else "Silakan pilih tanggal mulai dan selesai secara lengkap."
        st.warning(warning_msg)
    else:
        # 1. Smart Calendar & Monthly Chart Logic
        if selected_mode in ["Single Day", "Satu Hari"]:
            # Expand timeline to the FULL MONTH of the selected date
            target_year = tgl_mulai.year
            target_month = tgl_mulai.month
            _, last_day = calendar.monthrange(target_year, target_month)
            
            loop_start = date(target_year, target_month, 1)
            loop_end = date(target_year, target_month, last_day)
        else:
            # Keep strictly to the user's defined date range
            loop_start = tgl_mulai
            loop_end = tgl_selesai

        # Execute Prediction Loop
        count_days = (loop_end - loop_start).days + 1
        date_list = [loop_start + timedelta(days=x) for x in range(count_days)]
        
        results = []
        for d in date_list:
            pred_val = predictor.predict(d)
            results.append({'Tanggal': d, 'Harga_Prediksi': pred_val})
            
        # Construct the Pandas DataFrame
        df_hasil = pd.DataFrame(results)
        
        # 2. Extract Focal Price & Calculate Bounds
        if selected_mode in ["Single Day", "Satu Hari"]:
            # Extract the EXACT day the user selected for the focal card
            target_row = df_hasil[df_hasil['Tanggal'] == tgl_mulai]
            harga_fokus = target_row['Harga_Prediksi'].values[0] if not target_row.empty else df_hasil['Harga_Prediksi'].iloc[0]
            date_display = localizer.format_date(tgl_mulai, lang)
        else:
            # For ranges, focus on the final day of the trend
            harga_fokus = df_hasil['Harga_Prediksi'].iloc[-1]
            date_display = f"{localizer.format_date(tgl_mulai, lang)} - {localizer.format_date(tgl_selesai, lang)}"
        
        batas_bawah = harga_fokus * 0.98
        batas_atas = harga_fokus * 1.02
        
        # Premium Formatting
        formatted_valuation = localizer.format_currency(harga_fokus)
        tol_bawah_fmt = localizer.format_currency(batas_bawah)
        tol_atas_fmt = localizer.format_currency(batas_atas)
        tol_label = "2% Market Tolerance" if lang == "EN" else "Toleransi Pasar 2%"
        
        # Inject into our crisp, high-contrast white focal card
        st.markdown(f"""
            <div class="valuation-card">
                <p style="color: #79380B; font-size: 1.1rem; font-weight: 600; margin-bottom: 5px;">
                    {localizer.get_text('result_label', lang)} ({date_display})
                </p>
                <h2 style="color: #441004; font-size: 2.5rem; letter-spacing: 1px; margin-top: 0; margin-bottom: 5px;">
                    {formatted_valuation}
                </h2>
                <p style="color: #AD6D15; font-size: 0.95rem; margin-top: 0; font-weight: 600;">
                    {tol_label}: <br> {tol_bawah_fmt} — {tol_atas_fmt}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
# --- THE MASTERPIECE CHART ---
        if not df_hasil.empty:
            chart_title = "Valuation Trajectory" if lang == "EN" else "Lintasan Valuasi"
            
            # Format ledger dates and currency for the beautiful hover tooltip
            df_hasil['Formatted Date'] = df_hasil['Tanggal'].apply(lambda d: localizer.format_date(d, lang))
            df_hasil['Formatted Value'] = df_hasil['Harga_Prediksi'].apply(lambda v: localizer.format_currency(v))
            
            fig = go.Figure()
            
            # Add the elegantly curved line using our dynamic df_hasil
            fig.add_trace(go.Scatter(
                x=df_hasil['Tanggal'],
                y=df_hasil['Harga_Prediksi'],
                mode='lines+markers',
                line=dict(
                    color='#79380B', 
                    width=2, 
                    shape='spline',  
                    smoothing=1.3
                ), 
                marker=dict(
                    color='#EFBB55', 
                    size=6,
                    line=dict(color='#FBF5D2', width=1)
                ),
                fill='tozeroy',
                fillcolor='rgba(254, 227, 159, 0.15)', 
                name='Gold Price',
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>",
                customdata=df_hasil[['Formatted Date', 'Formatted Value']]
            ))
            
            # ======================================================
            # PERBAIKAN MUTLAK: PAKSA WARNA FONT SUMBU GRAFIK PLOTLY
            # ======================================================
            fig.update_layout(
                title=dict(
                    text=chart_title, 
                    font=dict(family="Cormorant Garamond", size=22, color="#441004", weight="bold")
                ),
                font=dict(color='#441004', family='Montserrat', size=11), 
                plot_bgcolor='rgba(255, 255, 255, 0.75)', 
                paper_bgcolor="rgba(0,0,0,0)",
                
                # Paksa warna teks Tanggal di bawah agar cokelat pekat tegas
                xaxis=dict(
                    showgrid=False, 
                    zeroline=False,
                    linecolor="#441004", 
                    linewidth=2,
                    ticks="outside", 
                    tickcolor="#441004",
                    tickfont=dict(color='#441004', family='Montserrat', size=11, weight='bold') # Kunci Sumbu X
                ),
                
                # Paksa warna teks Angka Nominal di kiri agar cokelat pekat tegas
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='rgba(68, 16, 4, 0.08)', 
                    zeroline=False,
                    linecolor="#441004", 
                    linewidth=2,
                    ticks="outside", 
                    tickcolor="#441004", 
                    tickformat=",.0f",
                    tickfont=dict(color='#441004', family='Montserrat', size=11, weight='bold') # Kunci Sumbu Y
                ), 
                margin=dict(l=65, r=30, t=50, b=40), # Margin disesuaikan agar angka jutaan tidak terpotong
                hoverlabel=dict(
                    bgcolor="#FFFFFF",
                    font_size=14,
                    font_family="Montserrat",
                    bordercolor="#AD6D15",
                    font=dict(color="#441004")
                )
            )
            
            # Render chart completely hiding the toolbar
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("</div>", unsafe_allow_html=True)