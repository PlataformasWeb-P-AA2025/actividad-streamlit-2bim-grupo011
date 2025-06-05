import streamlit as st
from db import get_session
from genera_tablas import Publicacion
from utils.paginacion import paginar

def listar_publicaciones():
    st.header("📝 Publicaciones")
    session = get_session()

    # Barra de búsqueda
    busqueda = st.text_input("Buscar en contenido de publicaciones")

    query = session.query(Publicacion)
    if busqueda:
        query = query.filter(Publicacion.contenido.ilike(f"%{busqueda}%"))

    total = query.count()
    offset, por_pagina = paginar("pagina_publicaciones", total, "Publicaciones")

    publicaciones = query.offset(offset).limit(por_pagina).all()

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
