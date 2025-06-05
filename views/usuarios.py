import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import get_session
from genera_tablas import Usuario, Publicacion
from utils.paginacion import paginar

def listar_usuarios():
    session = get_session()

    opcion = st.radio("Selecciona una vista", [
        "👤 Usuarios con publicaciones",
        "🚫 Usuarios sin publicaciones",
        "🏆 Top 5 usuarios con más publicaciones"
    ], horizontal=True)

    if opcion == "👤 Usuarios con publicaciones":
        st.subheader("Usuarios con publicaciones")

        total_con_publicaciones = (
            session.query(Usuario)
            .join(Usuario.publicaciones)
            .distinct()
            .count()
        )

        offset, por_pagina = paginar("pagina_con_pub", total_con_publicaciones, "Usuarios con publicaciones")

        usuarios = (
            session.query(Usuario)
            .join(Usuario.publicaciones)
            .distinct()
            .offset(offset)
            .limit(por_pagina)
            .all()
        )

        for user in usuarios:
            with st.expander(f"{user.nombre}", expanded=False):
                st.subheader("Publicaciones")
                st.table([{"Contenido": p.contenido} for p in user.publicaciones])

                st.subheader("Reacciones hechas")
                if user.reacciones:
                    st.table([
                        {
                            "Tipo emoción": r.tipo_emocion,
                            "Publicación": r.publicacion.contenido[:30]
                        } for r in user.reacciones
                    ])
                else:
                    st.write("Sin reacciones.")

    elif opcion == "🚫 Usuarios sin publicaciones":
        st.subheader("Usuarios sin publicaciones")

        total_sin_publicaciones = (
            session.query(Usuario)
            .outerjoin(Usuario.publicaciones)
            .filter(Publicacion.id == None)
            .count()
        )

        offset, por_pagina = paginar("pagina_sin_pub", total_sin_publicaciones, "Usuarios sin publicaciones")

        usuarios = (
            session.query(Usuario)
            .outerjoin(Usuario.publicaciones)
            .filter(Publicacion.id == None)
            .offset(offset)
            .limit(por_pagina)
            .all()
        )

        if usuarios:
            for usuario in usuarios:
                st.write(f"- {usuario.nombre}")
        else:
            st.info("Todos los usuarios tienen al menos una publicación.")

    elif opcion == "🏆 Top 5 usuarios con más publicaciones":
        st.subheader("Top 5 usuarios con más publicaciones")

        top_usuarios = (
            session.query(
                Usuario,
                func.count(Publicacion.id).label("cantidad")
            )
            .join(Usuario.publicaciones)
            .group_by(Usuario.id)
            .order_by(func.count(Publicacion.id).desc())
            .limit(5)
            .all()
        )

        from collections import Counter
        import pandas as pd

        for usuario, cantidad in top_usuarios:
            with st.expander(f"{usuario.nombre} → {cantidad} publicaciones", expanded=False):
                st.subheader("📝 Publicaciones")
                publicaciones = [{"Contenido": p.contenido} for p in usuario.publicaciones]
                st.table(publicaciones)

                st.subheader("📊 Reacciones recibidas por emoción")

                reacciones_contadas = []

                for pub in usuario.publicaciones:
                    conteo = Counter([r.tipo_emocion for r in pub.reacciones])
                    for emocion, cant in conteo.items():
                        reacciones_contadas.append({
                            "Publicación": pub.contenido[:30],
                            "Emoción": emocion,
                            "Cantidad": cant
                        })

                if reacciones_contadas:
                    df_reacciones = pd.DataFrame(reacciones_contadas)
                    st.table(df_reacciones)
                else:
                    st.write("Ninguna de sus publicaciones ha recibido reacciones.")


    session.close()
