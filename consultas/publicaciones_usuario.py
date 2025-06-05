import streamlit as st
from db import get_session
from genera_tablas import Usuario, Publicacion
from collections import Counter
import pandas as pd

def ejecutar():
    st.subheader("Publicaciones por usuario")
    session = get_session()
    usuarios = session.query(Usuario).all()
    nombres = [u.nombre for u in usuarios]

    if not nombres:
        st.warning("No hay usuarios registrados.")
        session.close()
        return

    nombre_usuario = st.selectbox("Selecciona un usuario:", nombres)

    if nombre_usuario:
        publicaciones = (
            session.query(Publicacion)
            .join(Usuario)
            .filter(Usuario.nombre == nombre_usuario)
            .all()
        )

        if publicaciones:
            st.success(f"Publicaciones de {nombre_usuario}:")
            for pub in publicaciones:
                with st.expander(pub.contenido[:50] + ("..." if len(pub.contenido) > 50 else "")):
                    st.markdown(f"**Contenido completo:** {pub.contenido}")

                    tipos_emocion = [r.tipo_emocion for r in pub.reacciones]
                    conteo = Counter(tipos_emocion)

                    if conteo:
                        df_reacciones = pd.DataFrame(
                            [{"Emoción": emocion, "Cantidad": cantidad} for emocion, cantidad in conteo.items()]
                        )
                        st.table(df_reacciones)
                    else:
                        st.markdown("_Sin reacciones._")
        else:
            st.info(f"{nombre_usuario} no tiene publicaciones.")
    session.close()
