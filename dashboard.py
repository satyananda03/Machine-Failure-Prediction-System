import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
from datetime import datetime

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Machine Monitoring Dashboard",
    layout="wide"
)

# --- URL API ---
# Pastikan API Anda sedang berjalan di alamat ini
API_BASE_URL = "http://127.0.0.1:8000"
LOGS_URL = f"{API_BASE_URL}/machine-logs"
PREDICT_URL = f"{API_BASE_URL}/predict"

# --- Fungsi untuk Mengambil Data ---
@st.cache_data(ttl=60) # Cache data selama 60 detik
def load_data():
    """Mengambil data dari endpoint /machine-logs."""
    try:
        response = requests.get(LOGS_URL)
        response.raise_for_status()  # Cek jika ada error HTTP
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        # Konversi kolom timestamp menjadi tipe datetime dan hapus informasi timezone
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        # Urutkan data berdasarkan waktu terbaru
        df = df.sort_values(by='timestamp', ascending=False)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal terhubung ke API: {e}")
        return pd.DataFrame()

# --- SIDEBAR: Kontrol dan Form Input --
if st.sidebar.button('🔄 Refresh Data'):
    st.cache_data.clear()
    st.rerun()

auto_refresh = st.sidebar.checkbox('Auto-refresh setiap 5 menit', value=True)

st.sidebar.markdown("---")

# Form untuk input data manual
st.sidebar.header("Manual Data Input")
with st.sidebar.form(key='predict_form'):
    st.write("Masukkan data sensor untuk mendapatkan prediksi.")
    # machine_id = st.text_input("Machine ID", "MACHINE-001")
    # machine_type = st.selectbox("Machine Type", ["L", "M", "H"])
    # Input dalam dua kolom agar lebih rapi
    col1, col2 = st.columns(2)
    with col1:
        air_temperature = st.number_input("Air Temp (°C)", format="%.1f")
        rotational_speed = st.number_input("Rotational Speed (rpm)")
        tool_wear = st.number_input("Tool Wear (min)")
    with col2:
        process_temperature = st.number_input("Process Temp (°C)", format="%.1f")
        torque = st.number_input("Torque (Nm)", format="%.1f")

    submit_button = st.form_submit_button(label='🚀 Predict & Submit')

# Logika setelah form disubmit
if submit_button:
    # Buat payload JSON sesuai dengan skema PredictRequest
    payload = {
        "machine_id": "MACHINE-001",
        "machine_type": "L",
        "torque": torque,
        "air_temperature": air_temperature,
        "rotational_speed": rotational_speed,
        "process_temperature": process_temperature,
        "tool_wear": tool_wear
    }
    
    try:
        # Kirim request POST ke API
        response = requests.post(PREDICT_URL, json=payload)
        response.raise_for_status()
        
        # Tampilkan hasil prediksi
        prediction_result = response.json()
        st.sidebar.success("✅ Data berhasil dikirim!")
        
        status = "🔴 FAILURE PREDICTED" if prediction_result['failure_status'] else "🟢 Normal Operation"
        st.sidebar.metric("Prediction Result", status)
        
        # Hapus cache agar data baru bisa diambil
        st.cache_data.clear()
        
        # Tunda sedikit sebelum me-rerun untuk memastikan data sudah masuk database
        time.sleep(1) 
        st.rerun()

    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"❌ Gagal mengirim data: {e}")

# --- Fungsi Utama untuk Menampilkan Dashboard ---
def display_dashboard():
    st.title("⚙️ Real-Time Machine Monitoring Dashboard")
    st.markdown("Dashboard ini memvisualisasikan data sensor mesin dan prediksi kegagalan secara real-time.")

    # Placeholder untuk metrik dan grafik
    placeholder = st.empty()

    df = load_data()
    
    with placeholder.container():
        if df.empty:
            st.warning("Tidak ada data untuk ditampilkan. Pastikan API berjalan dan sudah ada data log.")
            return # Hentikan fungsi jika tidak ada data

        st.header("Ringkasan Status Mesin M-001(L)")
        
        # Ambil data terbaru
        latest_data = df.iloc[0]
        
        # Hitung total kegagalan
        total_failures = int(df['failure_status'].sum())
        failure_rate = (total_failures / len(df)) * 100 if len(df) > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Data Logs", f"{len(df):,}")
        col2.metric("Total Prediksi Gagal", f"{total_failures:,}")
        col3.metric("Tingkat Kegagalan", f"{failure_rate:.2f}%")
        col4.metric("Last Update", latest_data['timestamp'].strftime("%d/%m/%Y %H:%M:%S"))

        st.markdown("---")

        # --- Visualisasi Data ---
        st.header("Visualisasi Data")
        
        col_viz1, col_viz2 = st.columns([2, 1])

        with col_viz1:
            st.subheader("Tren Sensor dari Waktu ke Waktu")
            # Pilihan untuk sensor yang akan ditampilkan
            selected_sensors = st.multiselect(
                'Pilih parameter sensor untuk ditampilkan:',
                ['torque', 'air_temperature', 'process_temperature', 'rotational_speed', 'tool_wear'],
                default=['torque', 'rotational_speed'])
            if selected_sensors:
                # Line Chart untuk tren sensor
                fig_line = px.line(df, x='timestamp', y=selected_sensors, title="Performa Sensor Mesin")
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Pilih minimal satu parameter sensor untuk melihat grafiknya.")

        with col_viz2:
            st.subheader("Distribusi Tipe Kegagalan")
            failure_cols = ['failure_type_twf', 'failure_type_hdf', 'failure_type_pwf', 'failure_type_osf', 'failure_type_rnf']
            # Ganti nama kolom untuk legenda yang lebih baik
            failure_names = {
                'failure_type_twf': 'Tool Wear',
                'failure_type_hdf': 'Heat Dissipation',
                'failure_type_pwf': 'Power',
                'failure_type_osf': 'Overstrain',
                'failure_type_rnf': 'Random'
            }
            failure_counts = df[failure_cols].sum().rename(failure_names).reset_index()
            failure_counts.columns = ['Tipe Kegagalan', 'Jumlah']
            
            # Pie Chart untuk tipe kegagalan
            fig_pie = px.pie(failure_counts, values='Jumlah', names='Tipe Kegagalan', 
                            title="Proporsi Tipe Kegagalan", hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- Tabel Data Mentah ---
        st.markdown("---")
        st.header("Data Log Mesin (Terbaru)")
        st.dataframe(df.head(20)) # Tampilkan 20 data terbaru

# --- Main Loop untuk Auto-Refresh ---
if __name__ == "__main__":
    display_dashboard()
    if auto_refresh:
        time.sleep(300)
        st.rerun()