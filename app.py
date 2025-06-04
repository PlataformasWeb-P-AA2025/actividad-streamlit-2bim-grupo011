import streamlit as st
import math
from db import get_session
from genera_tablas import Usuario, Publicacion, Reaccion
# Importa las consultas
from consultas import publicaciones_usuario, reacciones_publicacion


st.set_page_config(page_title="Explorador de usuarios y reacciones", layout="wide")


def paginar(nombre_estado, total_items, label):
    st.sidebar.subheader(f"Paginación: {label}")
    por_pagina = st.sidebar.number_input(f"{label} por página", min_value=1, max_value=50, value=5, key=f"pp_{nombre_estado}")
    total_paginas = math.ceil(total_items / por_pagina)

    if nombre_estado not in st.session_state:
        st.session_state[nombre_estado] = 1

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Anterior", key=f"prev_{nombre_estado}", disabled=st.session_state[nombre_estado] == 1):
            st.session_state[nombre_estado] -= 1
    with col3:
        if st.button("Siguiente ➡", key=f"next_{nombre_estado}", disabled=st.session_state[nombre_estado] == total_paginas):
            st.session_state[nombre_estado] += 1

    st.markdown(f"**Página {st.session_state[nombre_estado]} de {total_paginas}**")
    offset = (st.session_state[nombre_estado] - 1) * por_pagina
    return offset, por_pagina


def listar_usuarios():
    st.header("Usuarios")
    session = get_session()
    total = session.query(Usuario).count()
    offset, por_pagina = paginar("pagina_usuarios", total, "Usuarios")

    usuarios = session.query(Usuario).offset(offset).limit(por_pagina).all()

    for user in usuarios:
        with st.expander(f"ID {user.id} → {user.nombre}", expanded=False):
            st.subheader("Publicaciones")
            if user.publicaciones:
                st.table([{"ID": p.id, "Contenido": p.contenido} for p in user.publicaciones])
            else:
                st.write("Sin publicaciones.")

            st.subheader("Reacciones hechas")
            if user.reacciones:
                st.table([
                    {
                        "ID": r.id,
                        "Tipo emoción": r.tipo_emocion,
                        "Publicación ID": r.publicacion.id,
                        "Contenido": r.publicacion.contenido[:30]
                    } for r in user.reacciones
                ])
            else:
                st.write("Sin reacciones.")
    session.close()


def listar_publicaciones():
    st.header("Publicaciones")
    session = get_session()
    total = session.query(Publicacion).count()
    offset, por_pagina = paginar("pagina_publicaciones", total, "Publicaciones")

    publicaciones = session.query(Publicacion).offset(offset).limit(por_pagina).all()

    for pub in publicaciones:
        with st.expander(f"ID {pub.id} → {pub.contenido[:30]}", expanded=False):
            st.write(f"**Contenido completo:** {pub.contenido}")
            st.write(f"**Autor:** {pub.usuario.nombre}")
            st.write("**Reacciones:**")
            if pub.reacciones:
                st.table([
                    {
                        "Usuario": r.usuario.nombre,
                        "Tipo emoción": r.tipo_emocion
                    } for r in pub.reacciones
                ])
            else:
                st.write("Sin reacciones.")
    session.close()


def listar_reacciones():
    st.header("Reacciones")
    session = get_session()
    total = session.query(Reaccion).count()
    offset, por_pagina = paginar("pagina_reacciones", total, "Reacciones")

    reacciones = session.query(Reaccion).offset(offset).limit(por_pagina).all()

    st.table([
        {
            "ID": r.id,
            "Usuario": r.usuario.nombre,
            "Publicación": r.publicacion.contenido[:30],
            "Emoción": r.tipo_emocion
        } for r in reacciones
    ])
    session.close()


def main():
    st.title("Explorador SQLAlchemy: Usuarios, Publicaciones y Reacciones")

    entidad = st.sidebar.radio("Selecciona entidad:", ["Usuarios", "Publicaciones", "Reacciones", "Consultas"])

    if entidad == "Usuarios":
        listar_usuarios()
    elif entidad == "Publicaciones":
        listar_publicaciones()
    elif entidad == "Reacciones":
        listar_reacciones()
    elif entidad == "Consultas":
        consulta = st.sidebar.selectbox("Selecciona una consulta:", [
            "Publicaciones por usuario",
            "Reacciones a una publicación",
            # "Reacciones por usuario",  ← para futuras
            # "Top publicaciones",       ← para futuras
        ])

        if consulta == "Publicaciones por usuario":
            publicaciones_usuario.ejecutar()
        elif consulta == "Reacciones a una publicación":
            reacciones_publicacion.ejecutar()


if __name__ == "__main__":
    main()
