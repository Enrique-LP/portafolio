import streamlit as st
import pandas as pd
st.set_page_config(page_title="Netflix Streamlit", page_icon="👋")

st.title("Limpieza de datos en títulos de Netflix")
st.write("Este es un Streamlit que habla sobre los títulos de Netflix.")

# Opción 1: Cargar desde URL
dataset_url = st.text_input("Cargar CSV desde URL", value="https://...")
if st.button("Cargar desde URL"):
    try:
        df = pd.read_csv(dataset_url)
        st.write("Filas:", df.shape[0])
        st.write("Columnas:", df.shape[1])
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error al cargar desde URL: {e}")

st.write("--- O ---")

# Opción 2: Cargar CSV desde local
uploaded_file = st.file_uploader("Cargar CSV desde local", type=["csv"])
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)
    st.write("Filas del archivo local:", df_uploaded.shape[0])
    st.write("Columnas del archivo local:", df_uploaded.shape[1])
    st.dataframe(df_uploaded.head())
