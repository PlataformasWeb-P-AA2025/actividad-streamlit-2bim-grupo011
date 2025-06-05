import streamlit as st
import pandas as pd
import altair as alt
import math
from db import get_session
from genera_tablas import Usuario, Publicacion, Reaccion
# Importa las consultas
from consultas import publicaciones_usuario, reacciones_publicacion, reacciones_usuario
from views.reacciones import mostrar_reacciones
from views.usuarios import listar_usuarios
from views.publicaciones import listar_publicaciones


st.set_page_config(page_title="Explorador de usuarios y reacciones", layout="wide")



def main():
    st.title("Explorador SQLAlchemy: Usuarios, Publicaciones y Reacciones")

    entidad = st.sidebar.radio("Selecciona entidad:", ["Usuarios", "Publicaciones", "Reacciones", "Consultas"])

    if entidad == "Usuarios":
        listar_usuarios()
    elif entidad == "Publicaciones":
        listar_publicaciones()
    elif entidad == "Reacciones":
        mostrar_reacciones()
    elif entidad == "Consultas":
        consulta = st.sidebar.selectbox("Selecciona una consulta:", [
            "Publicaciones por usuario",
            "Reacciones a una publicación",
            "Reacciones por usuario", 
            # "Top publicaciones",       ← para futuras
        ])

        if consulta == "Publicaciones por usuario":
            publicaciones_usuario.ejecutar()
        elif consulta == "Reacciones a una publicación":
            reacciones_publicacion.ejecutar()
        elif consulta == "Reacciones por usuario":
            reacciones_usuario.ejecutar()


if __name__ == "__main__":
    main()
