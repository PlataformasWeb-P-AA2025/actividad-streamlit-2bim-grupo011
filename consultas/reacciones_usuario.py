import streamlit as st
from db import get_session
from genera_tablas import Usuario
import pandas as pd
import altair as alt

def ejecutar():
    st.subheader("Publicaciones con reacciones hechas por un usuario")
    session = get_session()

    usuarios = session.query(Usuario).all()
    if not usuarios:
        st.warning("No hay usuarios.")
        session.close()
        return

    opciones = [f"{u.id} - {u.nombre}" for u in usuarios]
    seleccion = st.selectbox("Selecciona un usuario:", opciones)

    usuario_id = int(seleccion.split(" - ")[0])
    usuario = session.query(Usuario).filter_by(id=usuario_id).first()

    if not usuario:
        st.error("Usuario no encontrado.")
        session.close()
        return

    if not usuario.reacciones:
        st.info(f"{usuario.nombre} no ha hecho ninguna reacción.")
        session.close()
        return

    # Gráfico: conteo de emociones
    st.markdown("### Gráfico de emociones usadas")
    data = pd.DataFrame([
        {"Emoción": r.tipo_emocion} for r in usuario.reacciones
    ])
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("Emoción", sort="-y"),
        y="count()",
        tooltip=["count()"]
    ).properties(width=500, height=300)
    st.altair_chart(chart, use_container_width=True)

    # Filtro de emoción
    emociones_disponibles = sorted(data["Emoción"].unique())
    emocion_seleccionada = st.selectbox("Filtrar por emoción:", ["Todas"] + emociones_disponibles)

    # Filtro de búsqueda por contenido de publicación
    busqueda = st.text_input("Buscar en contenido de publicaciones reaccionadas:")

    # Filtrar reacciones por emoción y por texto en publicación
    reacciones_filtradas = usuario.reacciones
    if emocion_seleccionada != "Todas":
        reacciones_filtradas = [r for r in reacciones_filtradas if r.tipo_emocion == emocion_seleccionada]

    if busqueda:
        reacciones_filtradas = [
            r for r in reacciones_filtradas if busqueda.lower() in r.publicacion.contenido.lower()
        ]

    st.markdown("### Publicaciones con reacción")
    if reacciones_filtradas:
        st.table([
            {
                "Publicación": r.publicacion.contenido[:40],
                "Emoción": r.tipo_emocion
            } for r in reacciones_filtradas
        ])
    else:
        st.write("No se encontraron publicaciones con esos filtros.")

    session.close()
