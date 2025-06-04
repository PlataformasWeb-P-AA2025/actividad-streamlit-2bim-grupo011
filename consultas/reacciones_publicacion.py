import streamlit as st
from db import get_session
from genera_tablas import Publicacion

def ejecutar():
    st.subheader("Reacciones a una publicación")
    session = get_session()

    publicaciones = session.query(Publicacion).all()
    if not publicaciones:
        st.warning("No hay publicaciones.")
        session.close()
        return

    # Crear lista de opciones con ID + preview del contenido
    opciones = [f"{p.id} - {p.contenido[:30]}" for p in publicaciones]
    seleccion = st.selectbox("Selecciona una publicación:", opciones)

    # Obtener el ID de la publicación seleccionada
    publicacion_id = int(seleccion.split(" - ")[0])
    publicacion = session.query(Publicacion).filter_by(id=publicacion_id).first()

    if publicacion:
        st.markdown(f"**Contenido completo:** {publicacion.contenido}")

        if publicacion.reacciones:
            tipos_emocion = list(sorted({r.tipo_emocion for r in publicacion.reacciones}))
            tipos_emocion.insert(0, "Todos")

            tipo_filtrado = st.radio("Filtrar por emoción:", tipos_emocion, horizontal=True)

            reacciones_filtradas = [
                r for r in publicacion.reacciones
                if tipo_filtrado == "Todos" or r.tipo_emocion == tipo_filtrado
            ]

            if reacciones_filtradas:
                st.markdown("**Reacciones:**")
                st.table([
                    {
                        "Usuario": r.usuario.nombre,
                        "Emoción": r.tipo_emocion
                    } for r in reacciones_filtradas
                ])
            else:
                st.info("No hay reacciones con ese tipo de emoción.")
        else:
            st.info("Esta publicación no tiene reacciones.")
    else:
        st.error("Publicación no encontrada.")
    
    session.close()
