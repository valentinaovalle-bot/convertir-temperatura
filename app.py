import streamlit as st
import pandas as pd

# --- Configuración básica ---
st.set_page_config(page_title="Conversor Celsius ↔ Fahrenheit", page_icon="🌡️", layout="centered")

st.title("🌡️ Conversor Celsius ↔ Fahrenheit")
st.write("Convierte temperaturas entre grados Celsius (°C) y Fahrenheit (°F).")

# --- Funciones de conversión ---
def c_to_f(c):
    return c * 9/5 + 32

def f_to_c(f):
    return (f - 32) * 5/9

# --- Pestañas ---
tab1, tab2 = st.tabs(["Celsius → Fahrenheit", "Fahrenheit → Celsius"])

with tab1:
    c = st.number_input("Celsius (°C)", value=0.0, step=0.1, format="%.2f")
    f = c_to_f(c)
    st.metric(label="Fahrenheit (°F)", value=f"{f:.2f}")
    st.caption(f"{c:.2f} °C equivalen a {f:.2f} °F")

with tab2:
    f_in = st.number_input("Fahrenheit (°F)", value=32.0, step=0.1, format="%.2f", key="f_in")
    c_out = f_to_c(f_in)
    st.metric(label="Celsius (°C)", value=f"{c_out:.2f}")
    st.caption(f"{f_in:.2f} °F equivalen a {c_out:.2f} °C")

# --- Conversión por lotes (CSV opcional) ---
with st.expander("📄 Conversión por lotes (CSV)"):
    st.write("Sube un CSV con una columna llamada **celsius** o **fahrenheit**.")
    uploaded = st.file_uploader("Sube tu archivo", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        if "celsius" in df.columns:
            df["fahrenheit"] = df["celsius"].astype(float).apply(c_to_f)
            st.success("Se agregó la columna 'fahrenheit'.")
        elif "fahrenheit" in df.columns:
            df["celsius"] = df["fahrenheit"].astype(float).apply(f_to_c)
            st.success("Se agregó la columna 'celsius'.")
        else:
            st.error("El CSV debe tener una columna 'celsius' o 'fahrenheit'.")
            df = None

        if df is not None:
            st.dataframe(df, use_container_width=True)
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button("Descargar CSV convertido", data=csv_bytes, file_name="convertido.csv", mime="text/csv")

# --- Info en la barra lateral ---
st.sidebar.header("ℹ️ Acerca de")
st.sidebar.write("""
Fórmulas de conversión:
- °F = (°C × 9/5) + 32  
- °C = (°F − 32) × 5/9
""")
st.sidebar.info("Ejemplo: 0 °C = 32 °F, 100 °C = 212 °F")
