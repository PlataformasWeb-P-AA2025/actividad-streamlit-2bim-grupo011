import pandas as pd
import altair as alt
import streamlit as st
from db import get_session
from genera_tablas import Reaccion
from sqlalchemy.orm import joinedload
from utils.paginacion import paginar

def mostrar_reacciones():
    st.header("Reacciones")

    opcion = st.radio(
        "¿Qué deseas ver?",
        ["📋 Ver todas las reacciones", "📊 Ver reporte de emociones"],
        horizontal=True
    )

    session = get_session()

    # Carga todas las reacciones con relaciones precargadas
    reacciones = session.query(Reaccion).options(
        joinedload(Reaccion.usuario),
        joinedload(Reaccion.publicacion)
    ).all()

    # Convierte a datos simples para evitar problemas con lazy-loading
    datos_reacciones = [{
        "ID": r.id,
        "Usuario": r.usuario.nombre,
        "Publicación": r.publicacion.contenido[:30],
        "Emoción": r.tipo_emocion
    } for r in reacciones]

    # Para el reporte gráfico
    df_emociones = pd.DataFrame([{"Emoción": r["Emoción"]} for r in datos_reacciones])
    conteo = df_emociones.value_counts().reset_index(name="Cantidad")

    if opcion == "📋 Ver todas las reacciones":
        st.subheader("Listado paginado")
        total = len(datos_reacciones)
        offset, por_pagina = paginar("pagina_reacciones", total, "Reacciones")
        pagina = datos_reacciones[offset: offset + por_pagina]
        st.table(pagina)

    elif opcion == "📊 Ver reporte de emociones":
        st.subheader("Uso total de emociones")
        if not conteo.empty:
            chart = alt.Chart(conteo).mark_bar().encode(
                x=alt.X("Emoción", sort="-y"),
                y="Cantidad",
                tooltip=["Emoción", "Cantidad"]
            ).properties(width=600, height=300)

            st.altair_chart(chart, use_container_width=True)

            with st.expander("Ver como tabla"):
                st.table(conteo)
        else:
            st.info("No hay reacciones registradas.")

    session.close()
