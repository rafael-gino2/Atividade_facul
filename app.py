import streamlit as st
import numpy as np
from PIL import Image
import base64
import io
from pymongo import MongoClient

# Config Streamlit
st.title("Reconhecimento Facial - Banco FEI (MongoDB Atlas)")
st.write("Compare sua foto com a base FEI e veja a face mais parecida.")

# Conexão MongoDB Atlas
client = MongoClient("mongodb+srv://rafaelgbarbosa_db_user:v9qqQ4mfxYhPBzOH@atividade.ncii3ci.mongodb.net/?appName=atividade ")
db = client["fei"]
col = db["faces"]

# Upload
uploaded_file = st.file_uploader("Envie uma imagem (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:

    # Mostrar imagem enviada
    img_user = Image.open(uploaded_file).convert("L")
    st.image(img_user, caption="Imagem enviada", width=250)

    # Converter para array para comparação
    arr_user = np.array(img_user)
    arr_user_flat = arr_user.flatten()

    st.write("Comparando com a base...")

    # Buscar todas as imagens do MongoDB
    data = list(col.find({}))

    best_diff = float("inf")
    best_match = None

    # Comparação por diferença absoluta (igual seu código)
    for d in data:
        vector = np.array(d["vector"])

        if len(vector) != len(arr_user_flat):
            # Pula se dimensões forem diferentes
            continue

        diff = np.sum(np.abs(vector - arr_user_flat))

        if diff < best_diff:
            best_diff = diff
            best_match = d

    st.subheader("Resultado:")

    if best_match:
        st.write(f"Imagem mais parecida: **{best_match['filename']}**")
        st.write(f"Diferença total: `{best_diff}`")

        # Recupera imagem do banco
        img_bytes = base64.b64decode(best_match["image_b64"])
        matched_img = Image.open(io.BytesIO(img_bytes))

        st.image(matched_img, caption="Face mais parecida", width=250)
    else:
        st.write("Nenhuma imagem compatível encontrada.")
